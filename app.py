from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# Secret key for keeping the user logged in
app.secret_key = "skill_swap_secret_key"


# HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')

        # Save the email in the session
        session['email'] = email

        return redirect('/dashboard')

    return render_template('login.html')


# SIGN UP
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')

        # Save the user's information
        session['name'] = name
        session['email'] = email

        return redirect('/dashboard')

    return render_template('signup.html')


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    name = session.get('name', 'Skill Swapper')

    return render_template(
        'dashboard.html',
        name=name
    )


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

    session.clear()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
