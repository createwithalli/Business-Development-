# CLAUDE.md — AI Assistant Guide for Business-Development-

## Project Overview

**AlliTrade Portfolio Tracker** is a single-file Python educational project. It serves two purposes simultaneously:

1. A **functional CLI application** — an interactive crypto portfolio tracker
2. A **structured Python tutorial** — 7 inline lessons teaching core Python fundamentals

The project is intentionally minimal: no dependencies beyond Python standard library (plus `requests` for Challenge 8). The goal is accessibility for a beginner learner.

---

## Repository Structure

```
Business-Development-/
├── CLAUDE.md                  # This file
└── portfolio_tracker.py       # The entire application (479 lines)
```

There are no subdirectories, configuration files, or additional source files. This is a deliberate design choice to keep the project approachable.

---

## Running the Application

```bash
python portfolio_tracker.py
```

No virtual environment required. The script uses Python's standard library plus `requests` for live API calls (Challenge 8). Python 3 is assumed (f-strings, type hints in docstrings).

**Optional:** Set up live CoinGecko prices:
```bash
export COINGECKO_API_KEY="your_demo_key_here"
python portfolio_tracker.py
```

---

## Codebase Structure (`portfolio_tracker.py`)

The file is organized into 7 clearly marked lesson sections, each preceded by a `# ===...===` banner:

| Lines     | Lesson | Concept Taught                        |
|-----------|--------|---------------------------------------|
| 15–29     | 1      | Variables & data types                |
| 44–51     | 2      | Lists                                 |
| 54–85     | 3      | Dictionaries                          |
| 88–161    | 4      | Functions, docstrings, return values  |
| 164–241   | 5      | Loops, HTTP requests, error handling  |
| 244–289   | 6      | File I/O, JSON persistence           |
| 292–467   | 7      | Main program loop (everything together) |
| 469–524   | —      | Challenge exercises (module-level docstring) |

### Key Functions

| Function              | Lines    | Purpose                                          |
|-----------------------|----------|--------------------------------------------------|
| `main()`              | 413–467  | Main `while` loop, routes menu choices           |
| `show_menu()`         | 297–311  | Prints menu options                              |
| `display_portfolio()` | 126–161  | Formats and prints portfolio table               |
| `add_coin()`          | 314–350  | Adds/updates a coin with input validation        |
| `remove_coin()`       | 352–372  | Removes a coin using `del`                       |
| `view_supported_coins()` | 375–388 | Lists all coins and prices                    |
| `check_price()`       | 391–404  | Looks up a single coin's price                  |
| `fetch_live_prices()` | 170–240  | Fetches live USD prices from CoinGecko API       |
| `save_portfolio()`    | 249–263  | Saves portfolio to JSON file                     |
| `load_portfolio()`    | 266–288  | Loads portfolio from JSON file                   |
| `calculate_value()`   | 94–108   | Computes total value of a holding                |
| `format_currency()`   | 111–123  | Formats a float as `$X,XXX.XX`                  |

### Global Data Structures

```python
supported_coins       # list of ticker strings e.g. ["BTC", "ETH", ...]
coin_data             # dict: { "BTC": {"name": "Bitcoin", "price": 97250.00}, ... }
COINGECKO_ID_MAP      # dict: maps tickers to CoinGecko API IDs
COINGECKO_API_KEY     # str: read from environment variable
PORTFOLIO_FILE        # str: path to JSON persistence file
portfolio             # dict (local to main): { "BTC": 0.15, "ETH": 2.5, ... }
```

---

## Conventions

### Code Style
- **Naming:** `snake_case` for functions and variables; `UPPERCASE` for module-level constants (`max_coins`, `is_running`)
- **Docstrings:** Every function has a PEP 257-compliant docstring. Lesson-focused functions include explicit "This teaches:" notes in the docstring
- **Comments:** Inline comments explain the educational concept, not just the mechanics
- **Formatting:** Section headers use `# ${'='*60}` banners for visual separation
- **f-strings:** Used throughout; alignment specifiers (`:<`, `:>`, `:^`) are used in `display_portfolio()`
- **Type hints:** Used in function signatures (e.g., `def add_coin(portfolio: dict) -> None:`)

### Output Style
- Two-space indentation for all printed output (visual padding)
- Currency formatted via `format_currency()` — always use this helper, never raw f-string formatting elsewhere
- Structured table output in `display_portfolio()` with ASCII borders

### Error Handling
- `try/except ValueError` guards all `float(input(...))` calls
- Early `return` is used for validation failures rather than nested conditionals
- Multiple exception handlers for API calls: `ConnectionError`, `Timeout`, `RequestException`
- Graceful fallback to hardcoded prices when API is unavailable

---

## What NOT to Change

- **The lesson structure** — the 7-lesson progression is the core educational scaffold; do not refactor it away
- **Inline educational comments** — comments like `# .upper() converts to uppercase` are intentional teaching content, not clutter
- **The challenge section** (lines 482–524) — this module-level docstring is a deliberate learning resource
- **Zero-dependency constraint (for core)** — standard library only for the base app; `requests` is part of Challenge 8
- **Hardcoded fallback prices** — kept in `coin_data` so the app works even without an API key

---

## Making Changes

### Adding a new supported coin
1. Add to `supported_coins` list (line 48–51)
2. Add matching entries in:
   - `coin_data` dict (lines 60–71) with `"name"` and `"price"` keys
   - `COINGECKO_ID_MAP` dict (lines 74–85) with CoinGecko ID

### Adding a new menu option
1. Add a `print()` line in `show_menu()` (lines 297–311)
2. Add a matching `elif choice == "N":` block in `main()` (lines 435–466)
3. Implement the handler as a new function following the existing docstring pattern

### Implementing challenge features
- **Challenge 9 (Portfolio History):** Track timestamp + total value on each price refresh; save to separate JSON file
- **Challenge 10 (Profit/Loss Tracking):** Store cost basis per coin; add P/L column in display with ANSI color codes
- **Challenge 11 (Price Alerts):** Store target prices; check alerts after each refresh; print notifications
- **Challenge 12 (CSV Export):** Add menu option to export portfolio to `.csv` using Python's `csv` module

---

## API Integration (Challenge 8)

The app includes **live price fetching from CoinGecko**:

- **Endpoint:** `https://api.coingecko.com/api/v3/simple/price`
- **Authentication:** Free Demo key via header `x-cg-demo-api-key`
- **Setup:** `export COINGECKO_API_KEY="your_key"` before running
- **Fallback:** If API fails (rate limit, timeout, no internet), app uses hardcoded `coin_data` prices
- **Rate Limit:** 30 calls/minute on free tier; handled gracefully in `fetch_live_prices()`

---

## Git Workflow

- **Active development:** Check current branch with `git branch`
- **Committing changes:**
```bash
git add portfolio_tracker.py CLAUDE.md
git commit -m "descriptive message"
git push origin <branch-name>
```
- **No CI/CD pipelines** — manual testing only

---

## Audience Context

This project was built for **Alicia**, a learner building Python skills through practical projects. The motivational message on quit (`"Keep building, Alicia. You've got this."`) is intentional. All teaching content assumes Python 3 basics but no prior crypto or finance knowledge.

---

## File Persistence

Portfolio data is saved to **`allitrade_portfolio.json`** in the current directory:

```json
{
  "BTC": 0.15,
  "ETH": 2.5,
  "SOL": 10.0
}
```

On startup, `load_portfolio()` restores this data. On quit, if the portfolio is non-empty, it auto-saves. Users can also manually save via menu option 7.

---

## Next Steps for Enhancement

See the Challenge Exercises section (lines 482–524 in `portfolio_tracker.py`) for 12 progressive enhancements, including:
- Portfolio history with ASCII charts
- Profit/loss tracking with color-coded output
- Price alerts and notifications
- CSV export functionality
