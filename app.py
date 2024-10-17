from flask import Flask
from flask import render_template, redirect, session, url_for
from flask import request
from db import *


app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False

app.secret_key = 'wefefwefw3fewf'


@app.route('/main',  methods=['GET', 'POST'])
def hello():
  if session:
    if request.method == "POST":
       conname = request.form.get("addusername")
       phonenum = request.form.get("addphonenum")
       con = f"Имя: {conname}  \n  Номер: {phonenum} \n"
       update(session["username"],con)
       return  redirect(request.url)
    else:
      return render_template('main.html', name=dictlist(select(session["username"])))
  else:
      return render_template('main.html', name="нет")

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        name = request.form.get("username")
        passw = request.form.get("password")
        if checklog(name):  
          if checkpass(name,passw):
            session["username"] = name
            session["password"] = passw
            return redirect(url_for('hello'))
          else:
             return render_template("auth.html", massage = "Неправильный логин или пароль")
        else:
          return render_template("auth.html", massage = "Неправильный логин или пароль")
    return render_template('auth.html')

@app.route('/reg',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form["username"]
        passw = request.form["password"]
        num = request.form["phonenum"]
        if checklog(name):
            return render_template("reg.html", massage = "Такой логин уже есть")
        else:
            insert(name, passw, num)
            session["username"] = name
            session["password"] = passw
            return redirect(url_for('hello'))
    return render_template("reg.html")

@app.route('/exit/')
def signout():
        session.clear()
        return redirect(url_for('auth'))


  
if __name__ == '__main__':
  app.run(debug=True, port=5000)