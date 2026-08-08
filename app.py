from flask import Flask, render_template, request, redirect, session, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "skill_swap_secret_key"

# Folder for profile pictures
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed image types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


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
# PROFILE
# =========================
@app.route('/profile')
def profile():

    name = session.get('name', 'Skill Swapper')

    return render_template(
        'profile.html',
        name=name
    )

# =========================
# EDIT PROFILE
# =========================
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():

    if request.method == 'POST':

        session['name'] = request.form.get('name', '')
        session['email'] = request.form.get('email', '')
        session['about'] = request.form.get('about', '')

        return redirect('/profile')

    return render_template('edit_profile.html')
# =========================
# UPLOAD PROFILE PICTURE
# =========================
@app.route('/upload-profile-picture', methods=['POST'])
def upload_profile_picture():

    if 'profile_picture' not in request.files:
        return redirect('/profile')

    file = request.files['profile_picture']

    if file.filename == '':
        return redirect('/profile')

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        # Give the file a simple user-specific name
        filename = "profile_" + filename

        file.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

        session['profile_picture'] = filename

    return redirect('/profile')


# =========================
# SERVE UPLOADED PICTURES
# =========================
@app.route('/uploads/<filename>')
def uploaded_file(filename):

    from flask import send_from_directory

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename
    )


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
