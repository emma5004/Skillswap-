from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/find-skills')
def find_skills():
    return render_template('find-skills.html')

@app.route('/teach-skill')
def teach_skill():
    return render_template('teach-skill.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # For now we just print it. Later we will save to database
        print(f"Login attempt: {email}")
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        print(f"New signup: {name} - {email}")
        return redirect(url_for('home'))
    return render_template('signup.html')
