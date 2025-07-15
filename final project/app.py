from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'cs50-is-love-3000'  # Used to securely sign session cookies

# 📌 SQLite DB Configuration
basedir = os.path.abspath(os.path.dirname(__file__))

# Ensure 'instance' folder exists
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance/daulatbox.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 🔗 DB Init
db = SQLAlchemy(app)

# 📄 Suggestion Model
class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 🔐 User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# 🏠 Home Route
@app.route("/")
def index():
    return render_template("index.html", username=session.get('username'), is_admin=session.get('is_admin', False))

# 📩 Suggestion Submission
@app.route("/submit-suggestion", methods=["POST"])
def submit_suggestion():
    name = request.form['name']
    email = request.form.get('email')
    message = request.form['message']

    suggestion = Suggestion(name=name, email=email, message=message)
    db.session.add(suggestion)
    db.session.commit()

    return render_template("thank_you.html")

# 🌐 Static Pages
@app.route("/daulatbook")
def encyclopedia():
    return render_template("daulatbook.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/marketplace")
def marketplace():
    try:
        if not session.get("username"):
            flash("Login required to access the Marketplace.", "warning")
            return redirect(url_for("login"))
        return render_template("marketplace.html")
    except Exception as e:
        return f"Error: {e}"

@app.route("/contact")
def contact():
    return render_template("contact.html")


# 🔑 Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            return redirect(url_for('index'))
        else:
            return " Invalid credentials"

    return render_template("login.html")

# 📝 Registration Route
@app.route("/register", methods=["POST"])
def register():
    try:
        username = request.form['username']
        email = request.form.get('email')
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "⚠️ Username already exists. Please login instead."

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()

        session['username'] = username
        session['is_admin'] = False
        return redirect(url_for('index'))

    except Exception as e:
        return f"❌ Error during registration: {str(e)}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

# 🏁 Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
