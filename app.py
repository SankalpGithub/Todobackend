from flask import Flask
from FlaskApp.routes import auth


app = Flask(__name__)

@app.route('/register', methods = ['POST'])
def home():
    return auth.register()

if __name__ == '__main__':
    app.run(debug=True)