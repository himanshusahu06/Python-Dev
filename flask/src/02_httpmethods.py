from flask import Flask, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return 'Method used %s' % request.method


@app.route('/admin')
def hello_admin():
    return 'This is Admin User'


@app.route('/guest/<username>')
def hello_guest(username):
    return 'Hello %s' % username


@app.route('/bacon', methods=['GET', 'POST'])
def bacon():
    if request.method == 'GET':
        return 'GET method'
    if request.method == 'POST':
        # request.args <- query parameters
        return 'POST method %s' % request.args


@app.route('/user/<username>')
def hello_user(username):
    if username == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', username = username))


if __name__ == "__main__":
    app.run(debug=True)
 