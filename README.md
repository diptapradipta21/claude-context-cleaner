# 🧹 Claude Context Cleaner

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Designed%20for-Claude%20Code-purple.svg)](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen.svg)](#)

> **Zero-dependency CLI tool to audit token bloat, scan wasteful files, generate optimized `.claudeignore` rules, and safely prune cache artifacts for Claude Code and autonomous AI agents.**

---

## 💡 The Problem
When using **Claude Code CLI** or AI coding agents across large repositories, Claude frequently hits rate limits or wastes thousands of tokens because it ingests:
* Massive lockfiles (`package-lock.json`, `poetry.lock`, `pnpm-lock.yaml`)
* Minified bundles & source maps (`*.min.js`, `*.map`)
* Hidden build caches (`.next`, `.turbo`, `__pycache__`, `.pyc`)
* Large binaries, SQLite databases, and transient logs

A single untracked `package-lock.json` can quietly eat **50,000+ tokens** in a single prompt!

## 🚀 The Solution
`claude-context-cleaner` scans your project tree, calculates estimated token waste per file, safely prunes ephemeral bytecode caches, and generates a tailored `.claudeignore` rule file so Claude only reads high-signal source code.

---

## ⚡ Quick Start

### 1. Audit Token Waste in Your Repository
```bash
python3 cleaner.py /path/to/your/project
```

### 2. View Top 5 Offenders Only
```bash
python3 cleaner.py /path/to/your/project --top 5
```

### 3. Machine-Readable JSON Output (for CI/CD or Agent Tool Calls)
```bash
python3 cleaner.py /path/to/your/project --json
```

### 4. Generate or Append `.claudeignore`
```bash
# Create fresh .claudeignore
python3 cleaner.py /path/to/your/project --init-ignore

# Append to existing .claudeignore without overwriting
python3 cleaner.py /path/to/your/project --append-ignore
```

### 5. Safely Prune Ephemeral Bytecode & Cache Files
```bash
# Dry-run preview
python3 cleaner.py /path/to/your/project --prune-cache --dry-run

# Execute safe cache pruning (.pyc, .DS_Store, empty __pycache__)
python3 cleaner.py /path/to/your/project --prune-cache
```

### 6. CI/CD Pre-Commit Guardrail
```bash
# Fail CI build (exit code 2) if total context waste exceeds 5.0 MB
python3 cleaner.py /path/to/your/project --fail-on-waste-mb 5.0
```

---

## 📊 Example Scan Output

```text
[*] Scanning workspace for token bloat: /my-saas-app
[!] Found 42 potential context-bloating files.
[!] Total potential waste: 14.80 MB (~3,880,120 tokens)

Path                                                              | Size       | Est. Tokens
-----------------------------------------------------------------------------------------------
frontend/package-lock.json                                        | 1.82 MB    | ~477,120
backend/poetry.lock                                               | 420.5 KB   | ~107,648
dist/bundle.min.js                                                | 890.2 KB   | ~227,891
data/test_database.sqlite                                         | 4.50 MB    | ~1,179,648
[✓] Successfully generated optimized .claudeignore!
```

---

## 🧪 Running Tests

```bash
python3 -m unittest discover tests/
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
