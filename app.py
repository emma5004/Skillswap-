from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# HOMEPAGE
@app.route('/')
def home():
    return render_template('home.html')

# BROWSE SKILLS PAGE
@app.route('/browse')
def browse():
    return render_template('browse.html')

# TEACH A SKILL PAGE  
@app.route('/teach')
def teach():
    return render_template('teach.html')

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # We will add real login later
        return redirect(url_for('home'))
    return render_template('login.html')

# SIGNUP PAGE
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # We will add real signup later
        return redirect(url_for('home'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
