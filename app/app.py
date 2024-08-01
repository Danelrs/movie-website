from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecret'  # Asegúrate de usar una clave secreta segura

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rolonlol135",
    database="db_movies"
)

def loguser(username):
    resp = make_response(redirect(url_for('index')))  # Redirige a 'loggedin'
    maxAge = 60 * 60
    resp.set_cookie('token', '123', max_age=maxAge, path='/', secure=False, httponly=True)
    return resp

def logged_in():
    return request.cookies.get('token')

def valid_login(username, password):
    cursor = db_connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE BINARY username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    if user and check_password_hash(user['password'], password):
        return True
    return False


def register_user(email, username, password):
    cursor = db_connection.cursor()
    acc = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
    user_data = (email, username, generate_password_hash(password, method='pbkdf2:sha256'))
    cursor.execute(acc, user_data)
    db_connection.commit()
    cursor.close()
    return True

@app.route('/prueba', methods=['GET', 'POST'])
def prueba():
    return render_template('prueba.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    request.cookies.get('token')
    return render_template('index.html', session_user=session.get('username'))

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
            flash('Invalid username/password' , 'error')
    return render_template('login.html')

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        if register_user(request.form['email'], request.form['username'], request.form['password']):
            flash('Registration successful!' , 'success') 
            return redirect(url_for('login'))
        else:
            flash('Could not create user' , 'error')
    return render_template('register.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    resp = make_response(redirect(url_for('index')))
    return resp

if __name__ == '__main__':
    app.run(debug=True)
