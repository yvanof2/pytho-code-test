from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Hardcoded secret key (vulnerability)
app.secret_key = "SuperSecretHardcodedKey123!"

## Insecure database connection (vulnerable to SQL Injection)
def get_user_info(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

@app.route("/")
def home():
    return "Welcome to Bido's demo!"

@app.route("/user")
def user():
    username = request.args.get("username", "")
    # No input validation => SQL Injection
    user_info = get_user_info(username)
    return jsonify(user_info)

# Debug mode enabled in production (vulnerability)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
