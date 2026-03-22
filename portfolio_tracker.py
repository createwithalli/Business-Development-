# ============================================================
# 📘 LESSON 1: VARIABLES & DATA TYPES
# ============================================================
# Variables store information. Python figures out the type automatically.

app_name = "AlliTrade Portfolio Tracker"  # This is a STRING (text)
version = 1.0                              # This is a FLOAT (decimal number)
max_coins = 20                             # This is an INTEGER (whole number)
is_running = True                          # This is a BOOLEAN (True or False)

# Print sends text to the screen. f"..." lets you insert variables with {curly braces}
print(f"\n{'='*50}")
print(f"  {app_name} v{version}")
print(f"{'='*50}\n")


# ============================================================
# 📘 LESSON 2: LISTS
# ============================================================
# Lists hold multiple items in order. They use square brackets [].
# You can add, remove, and loop through them.

supported_coins = ["BTC", "ETH", "BASE", "LINK", "XRP", "SOL", "GLTO"]

# Access items by index (position). Indexing starts at 0!
print(f"First coin: {supported_coins[0]}")   # BTC
print(f"Last coin: {supported_coins[-1]}")    # GLTO (negative = from the end)

# Check how many items: len()
print(f"We support {len(supported_coins)} coins\n")


# ============================================================
# 📘 LESSON 3: DICTIONARIES
# ============================================================
# Dictionaries store key:value pairs. Like a real dictionary:
# the word is the KEY, the definition is the VALUE.
# They use curly braces {}.

# Each coin has a name and a simulated price
coin_data = {
    "BTC":  {"name": "Bitcoin",    "price": 97250.00},
    "ETH":  {"name": "Ethereum",   "price": 3420.50},
    "BASE": {"name": "Base",       "price": 12.75},
    "LINK": {"name": "Chainlink",  "price": 18.90},
    "XRP":  {"name": "XRP",        "price": 2.35},
    "SOL":  {"name": "Solana",     "price": 195.60},
    "GLTO": {"name": "GlobalLotto","price": 0.05},
}

# Access a value by its key
btc_price = coin_data["BTC"]["price"]
print(f"Bitcoin price: ${btc_price:,.2f}")
# The :,.2f means: comma separators, 2 decimal places, float format


# ============================================================
# 📘 LESSON 4: FUNCTIONS
# ============================================================
# Functions are reusable blocks of code. Define with 'def'.
# They can take PARAMETERS (inputs) and RETURN values (outputs).

def calculate_value(symbol, quantity):
    """Calculate the total value of a coin holding.

    Parameters:
        symbol (str): The coin ticker, like "BTC"
        quantity (float): How many coins you hold

    Returns:
        float: The total dollar value
    """
    # Look up the price from our coin_data dictionary
    if symbol in coin_data:
        price = coin_data[symbol]["price"]
        return price * quantity
    else:
        return 0.0  # Return 0 if coin not found


def format_currency(amount):
    """Format a number as USD currency string."""
    return f"${amount:,.2f}"


def display_portfolio(portfolio):
    """Print a nicely formatted portfolio table.

    This function shows you:
    - FOR loops (iterating through data)
    - String formatting (alignment with :<, :>, :^)
    - Calling other functions from within a function
    """
    if not portfolio:
        print("  Your portfolio is empty! Add some coins.\n")
        return

    total_value = 0.0

    # Print table header
    print(f"  {'Coin':<8} {'Name':<14} {'Qty':>10} {'Price':>12} {'Value':>14}")
    print(f"  {'-'*8} {'-'*14} {'-'*10} {'-'*12} {'-'*14}")

    # FOR LOOP: do something for EACH item in the portfolio
    for symbol, quantity in portfolio.items():
        name = coin_data[symbol]["name"]
        price = coin_data[symbol]["price"]
        value = calculate_value(symbol, quantity)
        total_value += value  # += means "add to the current value"

        print(f"  {symbol:<8} {name:<14} {quantity:>10.4f} {format_currency(price):>12} {format_currency(value):>14}")

    print(f"  {'-'*60}")
    print(f"  {'TOTAL':>46} {format_currency(total_value):>14}\n")

    return total_value


# ============================================================
# 📘 LESSON 5: USER INPUT & THE MAIN LOOP
# ============================================================
# input() pauses and waits for the user to type something.
# A while loop keeps running until a condition becomes False.

def show_menu():
    """Display the main menu options."""
    print("  What would you like to do?")
    print("  [1] View Portfolio")
    print("  [2] Add a Coin")
    print("  [3] Remove a Coin")
    print("  [4] View Supported Coins")
    print("  [5] Check a Coin's Price")
    print("  [Q] Quit\n")


def add_coin(portfolio):
    """Add a coin to the portfolio.

    This teaches:
    - User input
    - Input validation (checking if input is valid)
    - Error handling with try/except
    - The .upper() string method
    """
    print("\n  --- Add a Coin ---")
    symbol = input("  Enter coin symbol (e.g. BTC): ").upper()  # .upper() converts to uppercase

    # CONDITIONAL: check IF the symbol is valid
    if symbol not in coin_data:
        print(f"  ❌ '{symbol}' is not supported. Use option [4] to see available coins.\n")
        return portfolio  # Exit the function early

    if symbol in portfolio:
        print(f"  ℹ️  You already have {symbol}. Current quantity: {portfolio[symbol]}")

    # TRY/EXCEPT: handle errors gracefully (e.g., user types "abc" instead of a number)
    try:
        quantity = float(input("  Enter quantity: "))
        if quantity <= 0:
            print("  ❌ Quantity must be greater than 0.\n")
            return portfolio
    except ValueError:
        print("  ❌ That's not a valid number. Try again.\n")
        return portfolio

    # Add to portfolio (or update existing quantity)
    if symbol in portfolio:
        portfolio[symbol] += quantity  # Add to existing
        print(f"  ✅ Updated {symbol} → total quantity: {portfolio[symbol]:.4f}\n")
    else:
        portfolio[symbol] = quantity   # New entry
        print(f"  ✅ Added {quantity:.4f} {symbol} to your portfolio!\n")

    return portfolio


def remove_coin(portfolio):
    """Remove a coin from the portfolio.

    This teaches the 'del' keyword for removing dictionary entries.
    """
    print("\n  --- Remove a Coin ---")

    if not portfolio:
        print("  Your portfolio is empty — nothing to remove.\n")
        return portfolio

    symbol = input("  Enter coin symbol to remove: ").upper()

    if symbol in portfolio:
        del portfolio[symbol]  # 'del' deletes an item from a dictionary
        print(f"  ✅ Removed {symbol} from your portfolio.\n")
    else:
        print(f"  ❌ {symbol} is not in your portfolio.\n")

    return portfolio


def view_supported_coins():
    """Show all supported coins and their prices.

    This teaches: looping through a dictionary with .items()
    """
    print("\n  --- Supported Coins ---")
    for symbol, data in coin_data.items():
        print(f"  {symbol:<6} {data['name']:<14} {format_currency(data['price']):>12}")
    print()


def check_price():
    """Look up a single coin's price.

    This teaches: dictionary lookups and conditional logic.
    """
    symbol = input("\n  Enter coin symbol: ").upper()

    if symbol in coin_data:
        data = coin_data[symbol]
        print(f"\n  {data['name']} ({symbol}): {format_currency(data['price'])}\n")
    else:
        print(f"  ❌ '{symbol}' not found.\n")


# ============================================================
# 📘 LESSON 6: PUTTING IT ALL TOGETHER — THE MAIN PROGRAM
# ============================================================
# This is where everything connects. The 'main()' function
# runs a WHILE LOOP that keeps the app going until you quit.

def main():
    """The main program loop."""

    # Start with a sample portfolio (you can change these!)
    portfolio = {
        "BTC": 0.15,
        "ETH": 2.5,
        "GLTO": 10000.0,
    }

    print("  Welcome! Here's your starting portfolio:\n")
    display_portfolio(portfolio)

    # WHILE LOOP: keeps running as long as is_running is True
    running = True
    while running:
        show_menu()
        choice = input("  Your choice: ").strip()  # .strip() removes extra spaces

        if choice == "1":
            print("\n  --- Your Portfolio ---")
            display_portfolio(portfolio)

        elif choice == "2":
            portfolio = add_coin(portfolio)

        elif choice == "3":
            portfolio = remove_coin(portfolio)

        elif choice == "4":
            view_supported_coins()

        elif choice == "5":
            check_price()

        elif choice.upper() == "Q":
            print("\n  Final portfolio summary:")
            display_portfolio(portfolio)
            print(f"  Thanks for using {app_name}! 🚀")
            print("  Keep building, Alicia. You've got this. 💪\n")
            running = False  # This stops the while loop

        else:
            print("  ❌ Invalid choice. Please enter 1-5 or Q.\n")


# ============================================================
# 📘 LESSON 7: THE ENTRY POINT
# ============================================================
# This special 'if' statement means: "only run main() if this
# file is being run directly (not imported by another file)."
# It's a Python convention you'll see everywhere.

if __name__ == "__main__":
    main()


"""
🎯 CHALLENGES — Try these after you run the program!
=====================================================

EASY:
  1. Add a new coin to the coin_data dictionary (pick your favorite)
  2. Change the starting portfolio amounts
  3. Change the app_name to something custom

MEDIUM:
  4. Add a menu option [6] that shows your best-performing holding
  5. Add a "total cost" field so you can track profit/loss
  6. Make the coin prices change randomly each time you view them
     (Hint: import random, then use random.uniform(low, high))

HARD:
  7. Save the portfolio to a file so it persists between runs
     (Hint: look up Python's 'json' module — json.dump / json.load)
  8. Connect to a REAL API to get live prices
     (Hint: pip install requests, then use requests.get()
      with the CoinGecko API — you've already worked with this!)
  9. Add a "price alert" feature that notifies you when a coin
     hits a target price

Each challenge builds on what you learned in the lessons above.
Start with the easy ones and work your way up! 🚀
"""
