from flask import Flask, render_template, redirect, session, url_for, request, jsonify
from db import *
from db import new_user

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.secret_key = 'wefefwefw3fewf'

@app.route('/main', methods=['GET', 'POST'])
def hello():
    if "username" in session:
        if request.method == "POST":
            conname = request.form["addusername"]
            phonenum = request.form["addphonenum"]
            comment = request.form["addcomment"]
            new_conntact(Name= conname, Phone_number= phonenum, Coment = comment, ID=session["ID"])
            return redirect(request.url)
        else:
            return render_template('main.html', name = session["username"], phonenumber = session["phonenum"], contact = select_contacts(session["ID"]))
    return render_template('main.html', name=None)

@app.route('/', methods=['GET', 'POST'])
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if session:
       return redirect(url_for('hello'))
    else:
        if request.method == 'POST':
            name = request.form.get("username")
            passw = request.form.get("password")
            if check_pass_log(name, passw):
                session["username"] = name
                session["password"] = passw
                session["phonenum"],session["ID"] = select_num(name)
                return redirect(url_for('hello'))
            return render_template("auth.html", massage="Неправильный логин или пароль")
        return render_template('auth.html')


@app.route('/reg', methods=['GET', 'POST'])
def register():
    if  session:
       return redirect(url_for('hello'))

    else:
        if request.method == 'POST':
            name = request.form["username"]
            passw = request.form["password"]
            num = request.form["phonenum"]
            full_name = request.form["fullname"]
            if check_log(name):
                return     render_template("reg.html", massage="Имя пользователя занято")
            else:
                session["phonenum"] = num
                session["username"] = name
                session["ID"] = new_user(Name= name, Full_name=full_name, Phone_number= num, Passw = passw)
                return redirect(url_for('hello'))
        return render_template("reg.html",massage = "test")




@app.route('/exit/')
def signout():
    session.clear()
    return redirect(url_for('auth'))

@app.route('/delete_contact/<int:ID>', methods=['POST'])
def delete_contact(ID):
    print(ID)
    with Session(engine) as sess:
            sess.query(Contact).filter(Contact.id == ID).delete()
            sess.commit()
            return redirect(url_for('hello'))
    

@app.route('/change_contact/<int:ID>', methods=['POST'])
def change_contact(ID):
    name = request.form["changename"]
    phone = request.form["changephone"]
    coment = request.form["changecoment"]
    with Session(engine) as sess:
        if name:
            sess.query(Contact).filter(Contact.id == int(ID)).update({"name":name})
        if phone:
            sess.query(Contact).filter(Contact.id == int(ID)).update({"phone_number":phone})
        if coment:
            sess.query(Contact).filter(Contact.id == int(ID)).update({"coment":coment})
        sess.commit()
        return redirect(url_for('hello'))

    

if __name__ == '__main__':
    app.run(host="192.168.1.117" ,debug=True,)
