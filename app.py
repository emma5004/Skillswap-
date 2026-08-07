from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'skillswap_secret_key_123'

# Create database and tables
def init_db():
    conn = sqlite3.connect('skillswap.db')
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    # Skills table
    c.execute('''CREATE TABLE IF NOT EXISTS skills
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  skill_name TEXT NOT NULL,
                  category TEXT NOT NULL,
                  location TEXT NOT NULL,
                  description TEXT NOT NULL,
                  user_email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/find-skills')
def find_skills():
    return render_template('find-skills.html')

@app.route('/teach-skill', methods=['GET', 'POST'])
def teach_skill():
    if request.method == 'POST':
        skill_name = request.form['skill_name']
        category = request.form['category']
        location = request.form['location']
        description = request.form['description']
        user_email = "guest@skillswap.com" # We'll connect this to real login next

        conn = sqlite3.connect('skillswap.db')
        c = conn.cursor()
        c.execute("INSERT INTO skills (skill_name, category, location, description, user_email) VALUES (?,?,?,?,?)",
                  (skill_name, category, location, description, user_email))
        conn.commit()
        conn.close()
        flash('Skill posted successfully!')
        return redirect(url_for('browse'))

    return render_template('teach-skill.html')

@app.route('/browse')
def browse():
    conn = sqlite3.connect('skillswap.db')
    c = conn.cursor()
    c.execute("SELECT * FROM skills ORDER BY id DESC")
    skills = c.fetchall()
    conn.close()
    return render_template('browse.html', skills=skills)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('skillswap.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            flash(f'Welcome back, {user[1]}!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password!')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            conn = sqlite3.connect('skillswap.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (name, email, password) VALUES (?,?,?)",
                      (name, email, password))
            conn.commit()
            conn.close()
            flash('Account created successfully! Please login.')
            return redirect(url_for('login'))
        except:
            flash('Email already exists!')
    return render_template('signup.html')
