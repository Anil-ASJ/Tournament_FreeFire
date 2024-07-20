from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random, secure string

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html', admin_logged_in=session.get('admin_logged_in', False))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO registrations (name, email, phone)
            VALUES (?, ?, ?)
        ''', (name, email, phone))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/registrations')
def registrations():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registrations')
    registrations = cursor.fetchall()
    conn.close()
    
    return render_template('registrations.html', registrations=registrations)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Replace this with your actual credentials check
        if username == 'Anil' and password == 'Anil5698':
            session['admin_logged_in'] = True
            return redirect(url_for('registrations'))
        else:
            return render_template('admin_login.html', error='Invalid username or password')
    
    return render_template('admin_login.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
