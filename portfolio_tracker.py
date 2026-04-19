# “””
AlliTrade Portfolio Tracker

A beginner Python project and interactive tutorial.
Tracks your crypto portfolio with LIVE prices via CoinGecko API.

Challenges completed in this file:

- Challenge 6: Random price simulation (replaced by live API)
- Challenge 7: JSON file persistence (save/load portfolio)
- Challenge 8: Live CoinGecko API with your own API key

Keep building, Alicia. You’ve got this. 💪
“””

# =============================================================================

# LESSON 1: VARIABLES & DATA TYPES

# Variables store information. Python has several types:

# str (text), int (whole number), float (decimal), bool (True/False)

# =============================================================================

import requests  # Challenge 8: for live API calls
import json      # Challenge 7: for saving/loading portfolio
import os        # for reading environment variables securely

app_name: str = “AlliTrade Portfolio Tracker”
version: str = “2.0”
max_coins: int = 20
is_running: bool = True

# === YOUR API KEY ===

# Option A (recommended — keeps key out of code):

# In your terminal, run: export COINGECKO_API_KEY=“your_key_here”

# Then run: python portfolio_tracker.py

# 

# Option B (quick testing — less secure):

# Replace the empty string below with your actual key.

# Get a free Demo key at: https://www.coingecko.com/en/api

# 

COINGECKO_API_KEY: str = os.environ.get(“COINGECKO_API_KEY”, “”)

# File where your portfolio is saved between sessions (Challenge 7)

PORTFOLIO_FILE: str = “allitrade_portfolio.json”

# =============================================================================

# LESSON 2: LISTS

# Lists hold multiple items in order. You can add, remove, and loop through them.

# =============================================================================

supported_coins: list = [
“BTC”, “ETH”, “XRP”, “SUI”, “LINK”,
“SOL”, “ADA”, “DOGE”, “TAO”, “FET”
]

# =============================================================================

# LESSON 3: DICTIONARIES

# Dictionaries store key-value pairs. Think of them like a real dictionary:

# you look up a word (key) to find its definition (value).

# =============================================================================

# Hardcoded fallback prices — used if the API is unavailable

coin_data: dict = {
“BTC”:  {“name”: “Bitcoin”,       “price”: 97250.00},
“ETH”:  {“name”: “Ethereum”,      “price”: 3380.00},
“XRP”:  {“name”: “XRP”,           “price”: 2.15},
“SUI”:  {“name”: “Sui”,           “price”: 3.85},
“LINK”: {“name”: “Chainlink”,     “price”: 18.40},
“SOL”:  {“name”: “Solana”,        “price”: 185.00},
“ADA”:  {“name”: “Cardano”,       “price”: 0.72},
“DOGE”: {“name”: “Dogecoin”,      “price”: 0.18},
“TAO”:  {“name”: “Bittensor”,     “price”: 420.00},
“FET”:  {“name”: “Fetch.ai”,      “price”: 1.65},
}

# Maps CoinGecko API IDs to our ticker symbols

COINGECKO_ID_MAP: dict = {
“BTC”:  “bitcoin”,
“ETH”:  “ethereum”,
“XRP”:  “ripple”,
“SUI”:  “sui”,
“LINK”: “chainlink”,
“SOL”:  “solana”,
“ADA”:  “cardano”,
“DOGE”: “dogecoin”,
“TAO”:  “bittensor”,
“FET”:  “fetch-ai”,
}

# =============================================================================

# LESSON 4: FUNCTIONS, DOCSTRINGS, RETURN VALUES

# Functions are reusable blocks of code. def defines them.

# Docstrings (triple quotes) explain what the function does.

# return sends a value back to whoever called the function.

# =============================================================================

def calculate_value(ticker: str, amount: float) -> float:
“””
Calculates the total USD value of a coin holding.

```
This teaches: function parameters, return values, dictionary lookup.

Args:
    ticker: The coin symbol e.g. "BTC"
    amount: How many coins you own e.g. 0.5

Returns:
    Total value in USD as a float
"""
price = coin_data[ticker]["price"]  # dictionary lookup
return price * amount               # multiplication, then return
```

def format_currency(amount: float) -> str:
“””
Formats a float as a USD currency string.

```
This teaches: f-strings with format specifiers.

Args:
    amount: A dollar amount e.g. 12345.678

Returns:
    Formatted string e.g. "$12,345.68"
"""
return f"${amount:,.2f}"  # :,.2f = commas + 2 decimal places
```

def display_portfolio(portfolio: dict) -> None:
“””
Prints a formatted table of the current portfolio.

```
This teaches: f-string alignment, looping over dictionaries,
calling other functions, running totals.

Args:
    portfolio: Dict of { "BTC": 0.5, "ETH": 2.0, ... }
"""
if not portfolio:
    print("\n  ℹ️  Your portfolio is empty. Add some coins!\n")
    return

print("\n" + "=" * 58)
print(f"  {'COIN':<8} {'AMOUNT':>12} {'PRICE':>14} {'VALUE':>14}")
print("=" * 58)

total_value: float = 0.0

for ticker, amount in portfolio.items():
    price = coin_data[ticker]["price"]
    value = calculate_value(ticker, amount)
    total_value += value

    # :<, :>, :^ = left, right, center alignment in f-strings
    print(
        f"  {ticker:<8} "
        f"{amount:>12.4f} "
        f"{format_currency(price):>14} "
        f"{format_currency(value):>14}"
    )

print("=" * 58)
print(f"  {'TOTAL VALUE':>36} {format_currency(total_value):>14}")
print("=" * 58 + "\n")
```

# =============================================================================

# LESSON 8 (CHALLENGE): LIVE API WITH YOUR OWN KEY

# This function fetches real-time prices from CoinGecko.

# It teaches: HTTP requests, API keys, error handling, graceful fallback.

# =============================================================================

def fetch_live_prices() -> bool:
“””
Fetches live USD prices from CoinGecko and updates coin_data in place.

```
This teaches:
- Making HTTP GET requests with the requests library
- Passing API keys in request headers (secure pattern)
- Reading and parsing JSON API responses
- Handling multiple failure modes gracefully
- Fallback strategy when external services are unavailable

Returns:
    True if prices were updated successfully, False if fallback was used.
"""
ids_param = ",".join(COINGECKO_ID_MAP.values())

# Build request headers — API key goes here, not in the URL
headers = {"accept": "application/json"}
if COINGECKO_API_KEY:
    # Free Demo key header (get yours at coingecko.com/en/api)
    headers["x-cg-demo-api-key"] = COINGECKO_API_KEY
    # If you upgrade to a Pro key, use this instead:
    # headers["x-cg-pro-api-key"] = COINGECKO_API_KEY

url = (
    "https://api.coingecko.com/api/v3/simple/price"
    f"?ids={ids_param}&vs_currencies=usd"
)

try:
    print("  ℹ️  Fetching live prices from CoinGecko...")
    response = requests.get(url, headers=headers, timeout=8)

    # Handle specific HTTP error codes before raising
    if response.status_code == 429:
        print("  ❌ Rate limit reached (30 calls/min on free tier).")
        print("  ℹ️  Using cached prices. Try again in a minute.\n")
        return False

    if response.status_code == 401:
        print("  ❌ API key invalid or missing.")
        print("  ℹ️  Check your COINGECKO_API_KEY and try again.\n")
        return False

    response.raise_for_status()  # raises for any other 4xx/5xx errors
    data = response.json()       # parse JSON response into a dict

    # Update coin_data prices from API response
    updated_count = 0
    for ticker, cg_id in COINGECKO_ID_MAP.items():
        if cg_id in data and "usd" in data[cg_id]:
            coin_data[ticker]["price"] = data[cg_id]["usd"]
            updated_count += 1

    print(f"  ✅ Live prices loaded for {updated_count} coins!\n")
    return True

except requests.exceptions.ConnectionError:
    print("  ❌ No internet connection.")
    print("  ℹ️  Using cached prices.\n")
except requests.exceptions.Timeout:
    print("  ❌ CoinGecko request timed out (8s).")
    print("  ℹ️  Using cached prices.\n")
except requests.exceptions.RequestException as e:
    print(f"  ❌ Network error: {e}")
    print("  ℹ️  Using cached prices.\n")
except Exception as e:
    print(f"  ❌ Unexpected error: {e}")
    print("  ℹ️  Using cached prices.\n")

return False
```

# =============================================================================

# LESSON 7 (CHALLENGE): FILE PERSISTENCE WITH JSON

# Saves your portfolio to a file so it survives between sessions.

# This teaches: file I/O, json module, try/except for file errors.

# =============================================================================

def save_portfolio(portfolio: dict) -> None:
“””
Saves the portfolio to a JSON file.

```
This teaches: writing files, json.dump(), error handling for file I/O.

Args:
    portfolio: The current portfolio dict to save.
"""
try:
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)
    print(f"  ✅ Portfolio saved to {PORTFOLIO_FILE}\n")
except IOError as e:
    print(f"  ❌ Could not save portfolio: {e}\n")
```

def load_portfolio() -> dict:
“””
Loads the portfolio from a JSON file if it exists.

```
This teaches: reading files, json.load(), handling missing files.

Returns:
    A portfolio dict if the file exists, otherwise an empty dict.
"""
if not os.path.exists(PORTFOLIO_FILE):
    return {}  # No saved file yet — start fresh

try:
    with open(PORTFOLIO_FILE, "r") as f:
        portfolio = json.load(f)
    # Filter out any coins no longer in supported_coins
    portfolio = {k: v for k, v in portfolio.items() if k in coin_data}
    if portfolio:
        print(f"  ✅ Portfolio loaded from {PORTFOLIO_FILE}\n")
    return portfolio
except (IOError, json.JSONDecodeError) as e:
    print(f"  ❌ Could not load saved portfolio: {e}\n")
    return {}
```

# =============================================================================

# LESSON 5: USER INPUT, LOOPS, ERROR HANDLING

# input() reads text from the user. Loops repeat code. try/except

# catches errors so the program doesn’t crash unexpectedly.

# =============================================================================

def show_menu() -> None:
“””
Prints the main menu options.

```
This teaches: printing structured output, keeping UI logic separate.
"""
print("  What would you like to do?")
print("  1. View portfolio")
print("  2. Add / update a coin")
print("  3. Remove a coin")
print("  4. View all supported coins & live prices")
print("  5. Check a single coin's price")
print("  6. Refresh live prices")
print("  7. Save portfolio")
print("  8. Quit\n")
```

def add_coin(portfolio: dict) -> None:
“””
Prompts the user to add or update a coin in the portfolio.

```
This teaches: input validation, .upper() for normalization,
early return for invalid input, updating a dictionary.

Args:
    portfolio: The current portfolio dict (modified in place).
"""
print("\n  Supported coins:", ", ".join(supported_coins))
ticker = input("  Enter coin ticker (e.g. BTC): ").strip().upper()
# .upper() converts to uppercase so "btc" and "BTC" both work

if ticker not in coin_data:
    print(f"  ❌ '{ticker}' is not supported yet.\n")
    return  # early return stops the function here

try:
    amount = float(input(f"  Enter amount of {ticker} you own: ").strip())
except ValueError:
    # ValueError is raised when float() can't convert the input
    print("  ❌ Invalid amount. Please enter a number (e.g. 0.5).\n")
    return

if amount <= 0:
    print("  ❌ Amount must be greater than zero.\n")
    return

if len(portfolio) >= max_coins and ticker not in portfolio:
    print(f"  ❌ Portfolio limit reached ({max_coins} coins max).\n")
    return

portfolio[ticker] = amount  # add or update the dictionary entry
value = calculate_value(ticker, amount)
print(f"  ✅ Added {amount} {ticker} ({format_currency(value)})\n")
```

def remove_coin(portfolio: dict) -> None:
“””
Removes a coin from the portfolio.

```
This teaches: del statement, membership check with 'in'.

Args:
    portfolio: The current portfolio dict (modified in place).
"""
if not portfolio:
    print("  ℹ️  Nothing to remove — portfolio is empty.\n")
    return

ticker = input("  Enter coin ticker to remove: ").strip().upper()

if ticker not in portfolio:
    print(f"  ❌ '{ticker}' is not in your portfolio.\n")
    return

del portfolio[ticker]  # del removes a key-value pair from a dict
print(f"  ✅ Removed {ticker} from your portfolio.\n")
```

def view_supported_coins() -> None:
“””
Lists all supported coins with their current prices.

```
This teaches: looping over a dict with .items(), formatted output.
"""
print("\n  Supported Coins & Current Prices")
print("  " + "-" * 38)
for ticker, info in coin_data.items():
    # info is a dict: {"name": "Bitcoin", "price": 97250.0}
    print(
        f"  {ticker:<6} {info['name']:<18} {format_currency(info['price']):>12}"
    )
print()
```

def check_price() -> None:
“””
Looks up the current price of a single coin.

```
This teaches: dictionary lookup with error handling.
"""
ticker = input("  Enter coin ticker to check: ").strip().upper()

if ticker not in coin_data:
    print(f"  ❌ '{ticker}' is not in our supported coins list.\n")
    return

info = coin_data[ticker]
print(f"  ✅ {info['name']} ({ticker}): {format_currency(info['price'])}\n")
```

# =============================================================================

# LESSON 6: PUTTING IT ALL TOGETHER — THE MAIN PROGRAM LOOP

# The main() function ties everything together.

# A while loop keeps the menu running until the user chooses to quit.

# =============================================================================

def main() -> None:
“””
The main program loop.

```
This teaches: while loops, if/elif/else branching,
calling functions, keeping state across iterations.
"""
print("\n" + "=" * 58)
print(f"  🚀 {app_name} v{version}")
print("=" * 58 + "\n")

# Challenge 8: Try to load live prices at startup
fetch_live_prices()

# Challenge 7: Load saved portfolio from file (if it exists)
portfolio = load_portfolio()

while is_running:  # loop runs until we break out of it
    show_menu()
    choice = input("  Enter your choice (1-8): ").strip()
    print()  # blank line for breathing room

    if choice == "1":
        display_portfolio(portfolio)

    elif choice == "2":
        add_coin(portfolio)

    elif choice == "3":
        remove_coin(portfolio)

    elif choice == "4":
        view_supported_coins()

    elif choice == "5":
        check_price()

    elif choice == "6":
        # Refresh live prices on demand
        fetch_live_prices()

    elif choice == "7":
        # Manually save the portfolio to file
        save_portfolio(portfolio)

    elif choice == "8":
        # Auto-save on quit
        if portfolio:
            save_portfolio(portfolio)
        print("  Keep building, Alicia. You've got this. 💪\n")
        break  # break exits the while loop

    else:
        print("  ❌ Invalid choice. Please enter a number from 1 to 8.\n")
```

# =============================================================================

# LESSON 7: THE if **name** == “**main**” PATTERN

# This block only runs when you execute the file directly:

# python portfolio_tracker.py

# It does NOT run when the file is imported as a module.

# This is a Python best practice for all runnable scripts.

# =============================================================================

if **name** == “**main**”:
main()

# =============================================================================

# CHALLENGE EXERCISES

# =============================================================================

“””
You’ve already completed Challenges 6, 7, and 8 in this file!
Here are more ideas to keep growing:

Challenge 1 — DONE (basic structure)
Challenge 2 — DONE (add/remove coins)
Challenge 3 — DONE (display table)
Challenge 4 — DONE (input validation)
Challenge 5 — DONE (multiple menu options)
Challenge 6 — DONE (live prices via API, replacing random simulation)
Challenge 7 — DONE (JSON file persistence — save/load portfolio)
Challenge 8 — DONE (CoinGecko API with your own API key)

Challenge 9: PORTFOLIO HISTORY

- Every time prices are refreshed, append a timestamp + total value to a list
- At quit, save this history to a separate JSON file
- Add a “View history” menu option that prints a simple price chart using ASCII

Challenge 10: PROFIT/LOSS TRACKING

- When adding a coin, also ask: “What did you pay per coin?” (your cost basis)
- Store this in a separate dict: { “BTC”: 85000.00 }
- In display_portfolio(), add a P/L column showing gain or loss per holding
- Color-code it: green (profit) vs red (loss) using ANSI escape codes

Challenge 11: PRICE ALERTS

- Let the user set a target price for any coin: “Alert me when BTC hits $100k”
- Store alerts in a dict: { “BTC”: {“above”: 100000, “below”: None} }
- After each price refresh, check all alerts and print a notification

Challenge 12: EXPORT TO CSV

- Add a menu option to export the current portfolio to a .csv file
- Use Python’s built-in csv module
- Columns: Ticker, Name, Amount, Price, Value, % of Portfolio

Getting your free CoinGecko API key:

1. Go to https://www.coingecko.com/en/api
1. Sign up for a free account
1. Copy your Demo API key
1. In terminal: export COINGECKO_API_KEY=“your_key_here”
1. Run: python portfolio_tracker.py
   “””