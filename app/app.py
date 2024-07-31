from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for
from flask import make_response, flash
from flask import session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecret'



def loguser():
    resp = make_response(redirect(url_for('index')))
    maxAge = 60 * 60 
    resp.set_cookie('token', '123', max_age=maxAge, path='/login')
    return resp

def isLogged():
    return request.cookies.get('token')



@app.route('/', methods=['GET' , 'POST'])
def index():
    
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        resp = loguser()
        print('Cookies set:', resp.headers.getlist('Set-Cookie'))
        return resp
    else:
        flash('Invalid username/password')
    if isLogged():
        print('Already logged in. Redirecting...')
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=['POST','GET'])
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)