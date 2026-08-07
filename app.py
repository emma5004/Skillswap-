from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'skillswap_secret_123'

users = [] # Temporary storage
skills = [] # Temporary storage

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/browse')
def browse():
    return render_template('browse.html', skills=skills)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users.append({'email': request.form['email'], 'password': request.form['password']})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['email']
        return redirect(url_for('teach'))
    return render_template('login.html')

@app.route('/teach', methods=['GET', 'POST'])
def teach():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        skill_name = request.form['skill_name']
        category = request.form['category']
        price = int(request.form['price'])
        description = request.form['description']
        teacher = session['user']

        # Block prices below minimum
        mins = {'high': 5000, 'medium': 3000, 'low': 1500}
        if price < mins[category]:
            return f"Error: Minimum price for this category is ₦{mins[category]}"

        skills.append({
            'skill_name': skill_name,
            'category': category,
            'price': price,
            'description': description,
            'teacher': teacher
        })
        
        return redirect(url_for('browse'))
    
    return render_template('teach.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
