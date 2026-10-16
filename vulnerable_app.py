# Sample app to audit (intentionally insecure, for learning)
import sqlite3, os
from flask import Flask, request

app = Flask(__name__)
app.secret_key = "admin123"            # hardcoded secret

def db():
    return sqlite3.connect("users.db")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # SQL query user input se directly bani hai
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = db().execute(query).fetchone()
    return "Welcome!" if user else "Invalid"

@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    return f"<h1>Hello {name}</h1>"    # user input seedha HTML me

@app.route("/ping")
def ping():
    host = request.args.get("host", "")
    return os.popen(f"ping -c 1 {host}").read()   # command seedha chal rahi hai

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")           # debug on, sabke liye open
