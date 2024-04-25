from flask import Flask, render_template, redirect, url_for,current_app, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from forms import RegisterForm
import psycopg2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://quiztriviadb:password@localhost/user'
app.config['SECRET_KEY']='6871ff06b5fb8f0fdd73300f'
db = SQLAlchemy(app)

app.app_context().push()


def db_conn():
    conn = psycopg2.connect(dbname = "user", 
                        user = "richard_quant", 
                        host= 'localhost',
                        password = "$*CO8I3m",
                        port = 5432)

   
    return conn

         
# class Entries(db.Model):
#     __tablename__='owned_user'
#     id = db.Column(db.Integer(),primary_key=True)
#     category = db.Column(db.String(length=20),nullable=False)
#     type = db.Column(db.String(length=20),nullable=False)
#     difficulty = db.Column(db.String(length=10),nullable=False)
#     result = db.Column(db.String(length=10))
#     userrelate = db.Column(db.Integer(),db.ForeignKey('user.id'))
class userinfo(db.Model):
   
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=30),nullable=False,unique=True)
    password = db.Column(db.String(length=20),nullable=False)
    email_address = db.Column(db.String(length=50),nullable=False)
    # entry = db.relationship('Entries',backref='owned_user',lazy=True)
  
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

@app.route('/LoginPage')
def login_page():
    return render_template('Login.html')

@app.route('/Contact')
def contact_page():
    return render_template('Contact.html')

@app.route('/LoginPage',methods=['GET','POST'])
def search_data():
    usernamefield = request.form['user_name']
    password_field = request.form['pass_word']
    conn = db_conn()
    cur=conn.cursor()
    cur.execute('''select * from userinfo''')
    data = cur.fetchall()
    for i in range(len(data)):
        user_name = data[i][1]
        pass_word = data[i][2]
        if user_name == usernamefield and password_field == pass_word:
            return render_template('Success_HomePage.html',name=usernamefield)
        flash(f'User Not Registered',category="danger")
    return render_template('Login.html')
@app.route('/Register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS userinfo 
            (id SERIAL PRIMARY KEY,
            username varchar(50),
            password varchar(50),
            email_address varchar(50));
            ''')
    if form.validate_on_submit():
        cur.execute(
            '''INSERT INTO userinfo(username,password,email_address) VALUES(%s,%s,%s)''',(form.username.data,form.passw.data,form.email_address.data))
        if request.method == 'POST':
            name = request.form.get('username')
            conn.commit()
            cur.close()
            conn.close()
            return render_template('Success_HomePage.html',name=name)
        return redirect(url_for('home_page',message="Failed"))
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



