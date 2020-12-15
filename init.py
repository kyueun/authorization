from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'

invalid_str = 'invalid URL'
url_str = '{domain}/{subdomain}'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register():
    return


@app.route('/login')
def login():
    return


@app.route('/user')
def user():
    return


if __name__ == '__main__':
    app.run(debug=False)