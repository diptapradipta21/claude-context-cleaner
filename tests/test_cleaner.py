import unittest
import tempfile
import os
import shutil
from pathlib import Path
from cleaner import estimate_tokens, scan_directory, generate_claudeignore, prune_cache


class TestClaudeContextCleaner(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_estimate_tokens(self):
        # 390 bytes should approximate ~100 tokens
        tokens = estimate_tokens(390)
        self.assertEqual(tokens, 100)

    def test_scan_directory_detects_bloat_files(self):
        # Create dummy bloat files
        lock_file = Path(self.test_dir) / "package-lock.json"
        lock_file.write_text('{"name": "test", "lockfileVersion": 2}', encoding="utf-8")

        large_file = Path(self.test_dir) / "data.raw"
        large_file.write_bytes(b"0" * 150 * 1024)  # 150 KB

        bloat, tokens, total_bytes = scan_directory(self.test_dir, size_threshold_kb=100, top_n=5)
        self.assertTrue(len(bloat) >= 2)
        paths = [b["path"] for b in bloat]
        self.assertIn("package-lock.json", paths)
        self.assertIn("data.raw", paths)

    def test_generate_claudeignore_create_and_append(self):
        ignore_path = Path(self.test_dir) / ".claudeignore"
        self.assertFalse(ignore_path.exists())

        # Test creation
        created = generate_claudeignore(self.test_dir)
        self.assertTrue(created)
        self.assertTrue(ignore_path.exists())

        # Test duplicate skip without force
        skipped = generate_claudeignore(self.test_dir)
        self.assertFalse(skipped)

        # Test append mode
        appended = generate_claudeignore(self.test_dir, append=True)
        self.assertTrue(appended)

    def test_prune_cache_dry_run_and_execution(self):
        pycache = Path(self.test_dir) / "__pycache__"
        pycache.mkdir(parents=True)
        pyc_file = pycache / "module.cpython-312.pyc"
        pyc_file.write_bytes(b"\x00" * 2048)

        # Dry run: should count but not remove
        count, freed, pruned = prune_cache(self.test_dir, dry_run=True)
        self.assertEqual(count, 1)
        self.assertTrue(pyc_file.exists())

        # Real run: should remove file and empty __pycache__ directory
        count, freed, pruned = prune_cache(self.test_dir, dry_run=False)
        self.assertEqual(count, 1)
        self.assertFalse(pyc_file.exists())
        self.assertFalse(pycache.exists())


if __name__ == "__main__":
    unittest.main()

    def test_bloat_filenames_lookup(self):
        from cleaner import BLOAT_FILENAMES
        self.assertIn("package-lock.json", BLOAT_FILENAMES)
        self.assertIn("poetry.lock", BLOAT_FILENAMES)
        self.assertIn("pnpm-lock.yaml", BLOAT_FILENAMES)
