import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Initialize Flask app
app = Flask(__name__)

# Register custom filter for formatting currency
app.jinja_env.filters["usd"] = usd

# Configure session to use the filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to SQLite database
db = SQL("sqlite:///finance.db")

# Create 'users' table: stores user accounts
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        cash NUMERIC DEFAULT 10000.00
    )
""")

# Create 'history' table: logs all buy/sell transactions
db.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        price NUMERIC NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")

# Prevent browser from caching responses


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Homepage: show portfolio of user's current stock holdings


@app.route("/")
@login_required
def index():
    # Get user's current cash balance
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Get total shares for each stock symbol the user owns
    holdings = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM history
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, session["user_id"])

    # Calculate real-time value of each holding
    total_portfolio_value = user_cash
    for holding in holdings:
        quote_result = lookup(holding["symbol"])
        holding["name"] = quote_result["name"]
        holding["price"] = quote_result["price"]
        holding["total_value"] = holding["total_shares"] * quote_result["price"]
        total_portfolio_value += holding["total_value"]

    return render_template("index.html", user_cash=user_cash, holdings=holdings, total_portfolio_value=total_portfolio_value)

# Log in user


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        # Validate username/password fields
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for user
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember user in session
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

# Register a new user


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Validate input fields
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # Hash the password
        hashed_password = generate_password_hash(request.form.get("password"))

        # Insert new user into database
        try:
            result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                                request.form.get("username"), hashed_password)
        except ValueError:
            return apology("username already exists", 400)

        # Log in the new user
        session["user_id"] = result
        return redirect("/")
    else:
        return render_template("register.html")

# Get stock quote


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        # Validate input
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)

        # Look up stock symbol
        quote_result = lookup(request.form.get("symbol"))
        if not quote_result:
            return apology("stock symbol not found", 400)

        return render_template("quoted.html", quote=quote_result)
    else:
        return render_template("quote.html")

# Buy stocks


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # Validate form inputs
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)
        if not request.form.get("shares"):
            return apology("must provide number of shares", 400)

        # Ensure shares is a positive integer
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("number of shares must be a positive integer", 400)

        # Look up stock
        quote_result = lookup(request.form.get("symbol"))
        if not quote_result:
            return apology("stock symbol not found", 400)

        total_cost = shares * quote_result["price"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Check if user can afford the purchase
        if total_cost > user_cash:
            return apology("insufficient funds", 400)

        # Complete purchase
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])
        db.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], quote_result["symbol"], shares, quote_result["price"])

        return redirect("/")
    else:
        return render_template("buy.html")

# Sell stocks


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        # Validate form inputs
        if not request.form.get("symbol"):
            return apology("must provide stock symbol", 400)
        if not request.form.get("shares"):
            return apology("must provide number of shares", 400)

        # Ensure shares is a positive integer
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("number of shares must be a positive integer", 400)

        quote_result = lookup(request.form.get("symbol"))
        if not quote_result:
            return apology("stock symbol not found", 400)

        # Check if user owns enough shares
        user_holdings = db.execute("""
            SELECT SUM(shares) as total_shares
            FROM history
            WHERE user_id = ? AND symbol = ?
            GROUP BY symbol
        """, session["user_id"], quote_result["symbol"])

        if not user_holdings or user_holdings[0]["total_shares"] < shares:
            return apology("insufficient shares to sell", 400)

        # Record the sale as a negative transaction
        total_sale_value = shares * quote_result["price"]
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   total_sale_value, session["user_id"])
        db.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], quote_result["symbol"], -shares, quote_result["price"])

        return redirect("/")
    else:
        # Populate dropdown with stocks the user currently owns
        symbols = db.execute("""
            SELECT symbol
            FROM history
            WHERE user_id = ?
            GROUP BY symbol
            HAVING SUM(shares) > 0
        """, session["user_id"])
        return render_template("sell.html", holdings=symbols)

# Show user's full transaction history


@app.route("/history")
@login_required
def history():
    transactions = db.execute("""
        SELECT symbol, shares, price, timestamp
        FROM history
        WHERE user_id = ?
    """, session["user_id"])

    # Add company name for display (optional)
    for transaction in transactions:
        quote_result = lookup(transaction["symbol"])
        transaction["name"] = quote_result["name"]

    return render_template("history.html", transactions=transactions)

# Log out current user


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")