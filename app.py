from flask import Flask, render_template

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()
