from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# Secret key
app.secret_key = "skill_swap_secret_key"


# =========================
# HOME
# =========================
@app.route('/')
def home():
    return render_template('home.html')


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')

        session['email'] = email

        return redirect('/dashboard')

    return render_template('login.html')


# =========================
# SIGN UP
# =========================
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')

        session['name'] = name
        session['email'] = email

        return redirect('/dashboard')

    return render_template('signup.html')


# =========================
# DASHBOARD
# =========================
@app.route('/dashboard')
def dashboard():

    name = session.get('name', 'Skill Swapper')

    return render_template(
        'dashboard.html',
        name=name
    )


# =========================
# BROWSE SKILLS
# =========================
@app.route('/browse')
def browse():
    return render_template('browse.html')


# =========================
# ADD SKILL I CAN TEACH
# =========================
@app.route('/add-skill', methods=['GET', 'POST'])
def add_skill():

    if request.method == 'POST':

        skill = request.form.get('skill')
        category = request.form.get('category')
        level = request.form.get('level')
        description = request.form.get('description')

        session['skill'] = skill
        session['category'] = category
        session['level'] = level
        session['description'] = description

        return redirect('/dashboard')

    return render_template('teach_skill.html')


# =========================
# ADD SKILL I WANT TO LEARN
# =========================
@app.route('/learn-skill', methods=['GET', 'POST'])
def learn_skill():

    if request.method == 'POST':

        skill = request.form.get('skill')
        category = request.form.get('category')
        level = request.form.get('level')
        description = request.form.get('description')

        session['learning_skill'] = skill
        session['learning_category'] = category
        session['learning_level'] = level
        session['learning_description'] = description

        return redirect('/dashboard')

    return render_template('learn_skill.html')


# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# =========================
# START FLASK
# =========================
if __name__ == '__main__':
    app.run(debug=True)
