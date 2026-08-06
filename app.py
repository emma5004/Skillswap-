from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/find-skills')
def find_skills():
    return render_template('find-skills.html')

@app.route('/teach')
def teach():
    return render_template('teach.html')

@app.route('/teach-skill')
def teach_skill():
    return render_template('teach-skill.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
