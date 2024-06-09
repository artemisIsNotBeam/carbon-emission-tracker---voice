from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
connection = sqlite3.connect("database.db", check_same_thread=False)
c = connection.cursor()
postdb = False


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "123456789"
postdb = False
db = SQLAlchemy(app)
# this is code for saving user's data
def createTable():
  query = '''
 			CREATE TABLE IF NOT EXISTS scores(
	 		id INTEGER PRIMARY KEY AUTOINCREMENT,
			userId INTEGER,
	 		score INTEGER,
			)'''
  c.execute(query)

  def add_score(userId, score):
    query = "INSERT INTO scores (userId, score) VALUES (?, ?)"
    c.execute(query, (userId, score))
    connection.commit()

  def get_scores():
    query = "SELECT * FROM scores"
    c.execute(query)
    return c.fetchall()

# this is code for logging in and registering
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), unique=False, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.username
  
@app.route('/login', methods=["POST", "GET"])
def login():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    print(user)
    if user and (password == user.password):
      session["username"] = username
      return redirect('/')
    else:
      return render_template("login.html",
                             message="password or/and username is wrong")
  else:
    return render_template("login.html")
  
@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "GET":
    return render_template("register.html")
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("confirm-password")

    if password != password2:
      return render_template("register.html",
                             message="passwords are not the same")

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    session["username"] = username
    return redirect('/')

@app.route('/logout', methods=["GET"])
def logout():
  if "username" in session:
    session.pop("username")
    return redirect('/')
  

@app.route("/")
def index():
    db.create_all()
    print(session)
    return render_template("index.html")

@app.route("/log", methods=["POST","GET"])
def log():
    if request.method =="GET":
      return render_template("form.html")
    else:
      eTime = int(request.form.get("eTime"))
      eLights = int(request.form.get("eLights"))
      vTime= int(request.form.get("vTime"))
      foods = float(request.form.get("foods"))
      score = (eTime *.06) + (eLights * .05) + (vTime * 6) + foods
      return redirect(f"/results/{score}")

@app.route("/results/<score>")
def results(score):
    return render_template("results.html", score=score)

if __name__ == '__main__':  
   app.run(debug = True)