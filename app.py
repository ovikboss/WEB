from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

login = "Ovik"
password = "qwerty12"

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

@app.route('/main')
def hello(name = None):
  if name != None:
    return render_template('main.html', name=name)
  else:
     return render_template('main.html', name = "нет")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form["username"]
        passw = request.form["password"]
        if name == login and password == passw:
          return hello(name)
        else:
          return hello()
    return render_template('start.html')

  
if __name__ == '__main__':
  app.run(debug=True, port=5000)