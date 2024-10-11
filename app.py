from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from db import *


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
        if checklog(name):
          if checkpass(name,passw):
            return hello(dictlist(select(name)))
          else:
             return render_template("auth.html", massage = "Неправильный логин или пароль")
        else:
          return render_template("auth.html", massage = "Неправильный логин или пароль")
    return render_template('auth.html')

  
if __name__ == '__main__':
  app.run(debug=True, port=5000)