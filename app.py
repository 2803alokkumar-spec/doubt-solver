from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 🔥 My problems list (multiple store karega)
my_problems = []

# 🔥 Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Problems table
    c.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    return render_template('index.html')

# 📤 Share page
@app.route('/share')
def share():
    return render_template('problemsharepage.html')

# 💾 Save problem
@app.route('/submit', methods=['POST'])
def submit():
    problem = request.form['problem']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO problems (question) VALUES (?)", (problem,))
    last_id = c.lastrowid

    conn.commit()
    conn.close()

    # 🔥 list me add karo (replace nahi hoga ab)
    my_problems.append(last_id)

    return redirect('/my')

# 👀 View all problems
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

# ⭐ My problems (multiple show karega)
@app.route('/my')
def my():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    all_data = []

    for pid in my_problems:
        c.execute("SELECT * FROM problems WHERE id=?", (pid,))
        problem = c.fetchone()

        if problem:
            c.execute("SELECT answer FROM answers WHERE problem_id=?", (pid,))
            answers = c.fetchall()
            all_data.append((problem, answers))

    conn.close()

    return render_template('my.html', data=all_data)

# 💬 Add answer
@app.route('/answer/<int:pid>', methods=['POST'])
def answer(pid):
    ans = request.form['answer']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO answers (problem_id, answer) VALUES (?, ?)", (pid, ans))

    conn.commit()
    conn.close()

    return redirect('/view')

# 🚀 Run
app.run(host='0.0.0.0', port=5000, debug=True)