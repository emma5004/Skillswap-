from flask import Flask, render_template

app = Flask(__name__)


# HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')


# LOGIN PAGE
@app.route('/login')
def login():
    return render_template('login.html')


# SIGN UP PAGE
@app.route('/signup')
def signup():
    return render_template('signup.html')


# DASHBOARD
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# BROWSE SKILLS
@app.route('/browse')
def browse():
    return render_template('browse.html')


# ADD SKILL
@app.route('/add-skill')
def add_skill():
    return render_template('teach_skill.html')


# LOGOUT
@app.route('/logout')
def logout():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
