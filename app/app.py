from flask import Flask, request, render_template, make_response, redirect, url_for
import requests

app = Flask(__name__)

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
    if isLogged():
        print('Already logged in. Redirecting...')
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=['POST','GET'])
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)