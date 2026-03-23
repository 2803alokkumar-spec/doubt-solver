from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 🔥 Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Problems table (username ke saath)
    c.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            question TEXT
        )
    ''')

    # Answers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER,
            answer TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# 🏠 Home
@app.route('/')
def home():
    return render_template('index.html')  # yahan login ya username form hona chahiye

# 📤 Share problem page
@app.route('/share')
def share():
    return render_template('problemsharepage.html')  # form me "username" aur "problem" field

# 💾 Save problem
@app.route('/submit', methods=['POST'])
def submit():
    problem = request.form['problem']
    username = request.form['username']  # user ka naam form se le rahe hai

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO problems (username, question) VALUES (?, ?)", (username, problem))
    conn.commit()
    conn.close()

    return redirect(f'/my?username={username}')  # apne problems page pe redirect

# 👀 View all problems (public view)
@app.route('/view')
def view():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM problems")
    problems = c.fetchall()

    all_data = []
    for p in problems:
        c.execute("SELECT answer FROM answers WHERE problem_id=?", (p[0],))
        answers = c.fetchall()
        all_data.append((p, answers))

    conn.close()
    return render_template('viewproblempage.html', data=all_data)

# ⭐ My problems (user-specific)
@app.route('/my')
def my():
    username = request.args.get('username')  # current logged-in user

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM problems WHERE username=?", (username,))
    problems = c.fetchall()

    all_data = []
    for p in problems:
        c.execute("SELECT answer FROM answers WHERE problem_id=?", (p[0],))
        answers = c.fetchall()
        all_data.append((p, answers))

    conn.close()
    return render_template('my.html', data=all_data, username=username)

# 💬 Add answer to a problem
@app.route('/answer/<int:pid>', methods=['POST'])
def answer(pid):
    ans = request.form['answer']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO answers (problem_id, answer) VALUES (?, ?)", (pid, ans))

    conn.commit()
    conn.close()

    return redirect('/view')

# 🚀 Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)