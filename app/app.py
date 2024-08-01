from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecret'  # Asegúrate de usar una clave secreta segura

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rolonlol135",
    database="db-movies"
)

def loguser(username):
    resp = make_response(redirect(url_for('index')))  # Redirige a 'loggedin'
    maxAge = 60 * 60
    resp.set_cookie('token', '123', max_age=maxAge, path='/', secure=False, httponly=True)
    return resp

def logged_in():
    return request.cookies.get('token')

def valid_login(username, password):
    try:
        cursor = db_connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE BINARY user = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        if user and check_password_hash(user['password'], password):
            return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return False

def register_user(email, username, password):
    try:
        cursor = db_connection.cursor()
        acc = "INSERT INTO users (email, user, password) VALUES (%s, %s, %s)"
        user_data = (email, username, generate_password_hash(password, method='pbkdf2:sha256'))
        cursor.execute(acc, user_data)
        db_connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db_connection.rollback()
        return False

@app.route('/prueba', methods=['GET', 'POST'])
def prueba():
    return render_template('prueba.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    #if 'username' in session:
       # return redirect(url_for('loggedin'))  # Redirige a 'loggedin'
    return render_template('index.html')

@app.route('/loggedin', methods=['GET', 'POST'])
def loggedin():
    return render_template('loggedin.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_login(username, password):
            session['username'] = username  # Guardar el usuario en la sesión
            return redirect(url_for('index'))  
        else:
            flash('Invalid username/password')
    return render_template('login.html')

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        if register_user(request.form['email'], request.form['username'], request.form['password']):
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Could not create user')
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
