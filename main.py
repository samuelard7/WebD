from flask import Flask, render_template, redirect, url_for,current_app, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///user.db'
app.config['SECRET_KEY']='6871ff06b5fb8f0fdd73300f'
db = SQLAlchemy(app)

app.app_context().push()



class User(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=30),nullable=False,unique=True)
    password = db.Column(db.String(length=20),nullable=False)
    email_address = db.Column(db.String(length=50),nullable=False)
    entry = db.relationship('Entries',backref='owned_user',lazy=True)
        
class Entries(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    category = db.Column(db.String(length=20),nullable=False)
    type = db.Column(db.String(length=20),nullable=False)
    difficulty = db.Column(db.String(length=10),nullable=False)
    result = db.Column(db.String(length=10))
    userrelate = db.Column(db.Integer(),db.ForeignKey('user.id'))


@app.route('/')
@app.route('/Front')
def front_page():
    return render_template('HomePage.html')

@app.route('/Home')
def home_page():
    return render_template('Success_HomePage.html')

@app.route('/About')
def about_us():
    return render_template('About.html')

@app.route('/Login')
def login_page():
    return render_template('Login.html')

@app.route('/Contact')
def contact_page():
    return render_template('Contact.html')

@app.route('/Register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,
                            password=form.passw.data,
                            email_address=form.email_address.data,
                            ) # type: ignore
        db.session.add(user_to_create)
        db.session.commit()
        if request.method == 'POST':
            name = request.form.get('username')
            return render_template('Success_HomePage.html',name=name)
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category="danger")
    return render_template('Register.html',form=form)

@app.route('/Game')
def game_play():
    return render_template('game.html')



def __repr__(self):
    return f'Entries{self.name}'

if __name__ == "__main__":
    app.run(debug=True)