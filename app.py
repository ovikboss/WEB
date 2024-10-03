from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

app.config['WTF_CSRF_ENABLED'] = False

@app.route('/main')
def hello(name = None):
  if name != None:
    return render_template('main.html', name=name)
  else:
     return "вы не авторизованы"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form["username"]
        return hello(name)
    return render_template('reg.html')

    



if __name__ == '__main__':
  app.run(debug=True, port=5000)