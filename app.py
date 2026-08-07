from flask import Flask, render_template, request, redirect

app = Flask(__name__)


# HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect('/dashboard')

    return render_template('login.html')


# SIGN UP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect('/dashboard')

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
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
