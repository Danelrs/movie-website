from flask import Flask, request, render_template, make_response, redirect, url_for
import requests

app = Flask(__name__)

def loguser():
    resp = make_response(redirect(url_for('index')))
    maxAge = 60 * 60 
    resp.set_cookie('token', '123', max_age=maxAge)
    return resp

def isLogged():
    token = request.cookies.get('token')
    if token is None:
        return False
    return True

@app.route('/', methods=['GET' , 'POST'])
def index():
    if isLogged():
        return render_template('index.html')
    if request.method == 'POST':
        return loguser()
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)