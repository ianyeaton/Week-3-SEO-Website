from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import secrets


app = Flask(__name__)
proxided = FlaskBehindProxy(app)
sec_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = str(sec_key)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"


@app.route("/")
def opening_page():
  return render_template('start.html')


@app.route("/home")
def home():
  return render_template('home.html', subtitle='Home Page', text='Welcome to the home page!')


@app.route("/done")
def done():
  return render_template('home.html', subtitle='Thank you for registering!', text='Submission recorded in the database!')


@app.route("/register", methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('done'))
  return render_template('register.html', title='Register Here!', form=form)


if __name__=='__main__':
    app.run(debug=True, host="0.0.0.0")
