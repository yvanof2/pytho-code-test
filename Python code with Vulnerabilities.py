from flask import Flask, request, session, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = '123'  # 🔓 Hardcoded secret key

# 🔓 Insecure database setup (run once)
def init_db():
    conn = sqlite3.connect('insecure.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    c.execute("INSERT INTO users VALUES ('admin', 'adminpass')")  # 🔓 Plaintext password
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return '<h1>Welcome</h1><a href="/login">Login</a> | <a href="/search">Search</a>'

# 🔓 Login with broken authentication and insecure password check
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('insecure.db')
        c = conn.cursor()
        # 🔓 SQL Injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        result = c.fetchone()
        conn.close()
        if result:
            session['user'] = username  # 🔓 No session timeout or strong auth
            return 'Logged in!'
        return 'Invalid credentials'
    return '''
    <form method="POST">
        Username: <input name="username"><br>
        Password: <input name="password"><br>
        <input type="submit">
    </form>
    '''

# 🔓 Reflected XSS vulnerability
@app.route('/search')
def search():
    query = request.args.get('q', '')
    return render_template_string(f"<h2>Search results for: {query}</h2>")  # 🚨 No sanitization

# 🔓 Logout with no CSRF protection
@app.route('/logout')
def logout():
    session.pop('user', None)
    return 'Logged out.'

if __name__ == '__main__':
    app.run(debug=True)
