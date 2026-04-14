# CLAUDE.md — AI Assistant Guide for Business-Development-

## Project Overview

**AlliTrade Portfolio Tracker** is a single-file Python educational project. It serves two purposes simultaneously:

1. A **functional CLI application** — an interactive crypto portfolio tracker
2. A **structured Python tutorial** — 7 inline lessons teaching core Python fundamentals

The project is intentionally minimal: no dependencies, no build system, no tests. The goal is accessibility for a beginner learner.

---

## Repository Structure

```
Business-Development-/
├── CLAUDE.md                  # This file
└── portfolio_tracker.py       # The entire application (313 lines)
```

There are no subdirectories, configuration files, or additional source files. This is a deliberate design choice to keep the project approachable.

---

## Running the Application

```bash
python portfolio_tracker.py
```

No installation, no virtual environment, no dependencies required. The script uses only Python's standard library. Python 3 is assumed (f-strings, type hints in docstrings).

---

## Codebase Structure (`portfolio_tracker.py`)

The file is organized into 7 clearly marked lesson sections, each preceded by a `# ===...===` banner:

| Lines     | Lesson | Concept Taught                        |
|-----------|--------|---------------------------------------|
| 1–14      | 1      | Variables & data types                |
| 17–30     | 2      | Lists                                 |
| 33–54     | 3      | Dictionaries                          |
| 57–116    | 4      | Functions, docstrings, return values  |
| 119–196   | 5      | User input, loops, error handling     |
| 224–273   | 6      | Main program loop (everything together) |
| 276–283   | 7      | `if __name__ == "__main__"` entry point |
| 287–313   | —      | Challenge exercises (module-level docstring) |

### Key Functions

| Function              | Lines    | Purpose                                          |
|-----------------------|----------|--------------------------------------------------|
| `main()`              | 230–273  | Main `while` loop, routes menu choices           |
| `show_menu()`         | 125–133  | Prints menu options                              |
| `display_portfolio()` | 86–116   | Formats and prints portfolio table               |
| `add_coin()`          | 136–174  | Adds/updates a coin with input validation        |
| `remove_coin()`       | 177–196  | Removes a coin using `del`                       |
| `view_supported_coins()` | 199–207 | Lists all coins and prices                    |
| `check_price()`       | 210–221  | Looks up a single coin's price                  |
| `calculate_value()`   | 63–78    | Computes total value of a holding                |
| `format_currency()`   | 81–83    | Formats a float as `$X,XXX.XX`                  |

### Global Data Structures

```python
supported_coins  # list of ticker strings e.g. ["BTC", "ETH", ...]
coin_data        # dict: { "BTC": {"name": "Bitcoin", "price": 97250.00}, ... }
portfolio        # dict (local to main): { "BTC": 0.15, "ETH": 2.5, ... }
```

Simulated prices are hardcoded in `coin_data`. There is no live price feed unless added as a challenge.

---

## Conventions

### Code Style
- **Naming:** `snake_case` for functions and variables; `UPPERCASE` for module-level constants (`max_coins`, `is_running`)
- **Docstrings:** Every function has a PEP 257-compliant docstring. Lesson-focused functions include explicit "This teaches:" notes in the docstring
- **Comments:** Inline comments explain the educational concept, not just the mechanics
- **Formatting:** Section headers use `# ${'='*60}` banners for visual separation
- **f-strings:** Used throughout; alignment specifiers (`:<`, `:>`, `:^`) are used in `display_portfolio()`

### Output Style
- Emoji are used intentionally in user-facing output (`✅`, `❌`, `ℹ️`, `🚀`, `💪`) — preserve them
- Two-space indentation for all printed output (visual padding)
- Currency formatted via `format_currency()` — always use this helper, never raw f-string formatting elsewhere

### Error Handling
- `try/except ValueError` guards all `float(input(...))` calls
- Early `return` is used for validation failures rather than nested conditionals
- No bare `except` clauses

---

## What NOT to Change

- **The lesson structure** — the 7-lesson progression is the core educational scaffold; do not refactor it away
- **Inline educational comments** — comments like `# .upper() converts to uppercase` are intentional teaching content, not clutter
- **The challenge section** (lines 287–313) — this module-level docstring is a deliberate learning resource
- **Emoji in output** — they are intentional and part of the UX for the target learner
- **Zero-dependency constraint** — do not add `import` statements for third-party packages unless a challenge specifically calls for it (e.g., Challenge 8 adds `requests`)

---

## Making Changes

### Adding a new supported coin
1. Add to `supported_coins` list (line 23)
2. Add a matching entry in `coin_data` dict (lines 41–49) with `"name"` and `"price"` keys

### Adding a new menu option
1. Add a `print()` line in `show_menu()` (lines 125–133)
2. Add a matching `elif choice == "N":` block in `main()` (lines 249–273)
3. Implement the handler as a new function following the existing docstring pattern

### Implementing challenge features
- Challenge 6 (random prices): `import random` at top; replace static prices with `random.uniform(low, high)` in `calculate_value()` or at startup
- Challenge 7 (file persistence): `import json`; call `json.dump()` on quit and `json.load()` on startup
- Challenge 8 (live API): `pip install requests`; replace `coin_data` prices via `requests.get()` against CoinGecko

---

## Git Workflow

- **Active development branch:** `claude/add-claude-documentation-4ZqI7`
- **Single prior commit:** `4254306` — "Add AlliTrade Portfolio Tracker — Python learning project"
- There are no CI/CD pipelines, no linting hooks, and no pre-commit checks

When committing:
```bash
git add portfolio_tracker.py CLAUDE.md
git commit -m "descriptive message"
git push -u origin claude/add-claude-documentation-4ZqI7
```

---

## Audience Context

This project was built for **Alicia**, a learner building Python skills through practical projects. The motivational message on quit (`"Keep building, Alicia. You've got this. 💪"`) is intentional — preserve it. When suggesting changes or additions, favor clarity and educational value over conciseness or cleverness.
