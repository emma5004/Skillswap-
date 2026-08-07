from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/add-skill')
def add_skill():
    return render_template('teach_skill.html')  # <-- this connects to your file

if __name__ == '__main__':
    app.run(debug=True)
