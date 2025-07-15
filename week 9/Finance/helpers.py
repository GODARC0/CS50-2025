import requests
from flask import redirect, render_template, session
from functools import wraps

# Show an apology message with a meme image


def apology(message, code=400):
    """Render message as an apology to user using memegen."""

    def escape(s):
        """
        Escape special characters for URL formatting (memegen requirement).
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    # Render apology.html with meme text
    return render_template("apology.html", top=code, bottom=escape(message)), code


# Login required decorator to protect routes
def login_required(f):
    """
    Ensure user is logged in before accessing certain routes.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# Fetch real-time stock quote data
def lookup(symbol):
    """Look up stock quote for a given symbol using CS50’s API."""
    url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for HTTP problems

        quote_data = response.json()

        return {
            "name": quote_data["companyName"],
            "price": quote_data["latestPrice"],
            "symbol": symbol.upper()
        }

    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")

    return None  # Return None if lookup fails


# Format value as USD currency
def usd(value):
    """Format a numeric value as USD (e.g., 1234.5 -> $1,234.50)."""
    return f"${value:,.2f}"