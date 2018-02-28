from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is home page'

@app.route('/profile/<username>')
def profile(username):
    return '<h2>Hi %s</h2>' % username

@app.route('/post/<int:post_id>')
def post(post_id):
    return '<h2>Post ID: %s</h2>' % post_id

if __name__ == "__main__":
    app.run(debug=True)
 