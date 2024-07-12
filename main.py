from flask import Flask, render_template, redirect, url_for,current_app, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from forms import RegisterForm, Recovery, QueryForm
import smtplib
import random
import psycopg2

otp_gen = ""
user_recovery=""
nameProfile="User"
profile = f"Hello {nameProfile}"

user_cat = ""
user_noq = ""
user_diff = ""
print(user_cat)
print(user_noq)
print(user_diff)

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://quiztriviadb:password@localhost/user'
# app.config['SECRET_KEY']= '1vcv231xcvxcv23dfg12345jniomoim345'
my_email = "samuelrichard214@gmail.com"
password = "ebsv xtyp eeuc pufg"

recipients = ['rs7871@dseu.ac.in']
db = SQLAlchemy(app)

app.app_context().push()


   

def db_conn():
    conn = psycopg2.connect(dbname = "user", 
                        user = "quiztriviadb", 
                        host= 'localhost',
                        password = "password",
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
  
  
def otp_generate():
    l = ['0','1','2','3','4','5','6','7','8','9']
    otp = ""
    for i in range(6):
        otp = otp + random.choice(l)
    return otp


@app.route('/')
def home():
    return render_template('Base.html',name = nameProfile)
@app.route('/Front')
def front_page():
    
    return render_template('HomePage.html',name= nameProfile)



@app.route('/About')
def about_us():
    return render_template('About.html')


@app.route('/LoginPage')
def login_page():
    return render_template('Login.html')

@app.route('/Contact',methods=['GET','POST'])
def contact_page():
    form = QueryForm()
    profile=f'Hi {nameProfile}'
   
    usr_name = request.form.get('person_name')
    usr_email = request.form.get('person_email')
    usr_mobile = request.form.get('person_mobile')
    usr_message = request.form.get('person_message')
    conn = db_conn()
    cur=conn.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS userquery 
            (id SERIAL PRIMARY KEY,
            Name varchar(50) NOT NULL,
            Email varchar(50) NOT NULL,
            Mobile varchar(10) NOT NULL,
            Message varchar(300) NOT NULL);
                ''')
   
    if form.validate_on_submit():
        cur.execute(
            '''INSERT INTO userquery(Name,Email,Mobile,Message) VALUES(%s,%s,%s,%s)''',
            (form.person_name.data,form.person_email.data,form.person_mobile.data,form.person_message.data))
        if request.method == 'POST':
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(from_addr=f'{usr_email}', to_addrs=recipients,
                            msg=f"Subject:{usr_name} query\n\n {usr_message} \n\n\n Mob:{usr_mobile}")
            conn.commit()
            cur.close()
            conn.close()
            flash('Successfully Sended.', category='success')
            return render_template('HomePage.html',name=usr_name)
  
        
    return render_template('Contact.html',name=profile, form=form)


@app.route('/LoginPage',methods=['GET','POST'])
def search_data():
    global nameProfile
    usernamefield = request.form['user_name'] # type: ignore
    password_field = request.form['pass_word']
    conn = db_conn()
    cur=conn.cursor()
    cur.execute('''select * from userinfo''')
    data = cur.fetchall()
    for i in range(len(data)):
        user_name = data[i][1]
        pass_word = data[i][2]
        if user_name == usernamefield and password_field == pass_word:
            conn.commit()
            cur.close()
            conn.close()
            nameProfile = usernamefield
            flash(f'Success',category="success")
            return redirect(url_for('home'))
       
    flash('User Not Found Create new Account',category="danger")
    return redirect(url_for('home'))
    
@app.route('/Register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS userinfo 
            (id SERIAL PRIMARY KEY,
            username varchar(50) NOT NULL,
            password varchar(50) NOT NULL,
            email_address varchar(50) NOT NULL UNIQUE);
            ''')
    if form.validate_on_submit():
        cur.execute(
            '''INSERT INTO userinfo(username,password,email_address) VALUES(%s,%s,%s)''',
            (form.username.data,form.passw.data,form.email_address.data))
        if request.method == 'POST':
            name = request.form.get('username')
            conn.commit()
            cur.close()
            conn.close()
            flash('Successfully Created.', category='success')
            return render_template('HomePage.html',name=name)
        return redirect(url_for('home',message="Failed"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category="danger")
    return render_template('Register.html',form=form)


@app.route('/Recovery',methods=['GET','POST'])
def forgot_password():
    global user_recovery, otp_gen
    form = Recovery()
    conn = db_conn()
    cur = conn.cursor()
    email_entry = request.form.get('email_add')
    user_recovery = email_entry
    if form.validate_on_submit():
        cur.execute('''select email_address from userinfo''')
        if request.method == 'POST' or request.method == 'GET':
            data = cur.fetchall()
            for i in range(len(data)):
                if data[i][0]==email_entry:
                    otp = otp_generate() 
                    otp_gen = otp
                    cur.execute(f''' select username from userinfo where email_address like '%{email_entry}%' ''')
                    j = cur.fetchall()
                    conn.commit()
                    cur.close()
                    conn.close()
                    flash(f"Welcome {j[0][0]}", category="success")
                    with smtplib.SMTP("smtp.gmail.com") as connection:
                         connection.starttls()
                         connection.login(user=my_email, password=password)
                         connection.sendmail(from_addr=my_email, to_addrs=user_recovery, # type: ignore
                         msg=f"Subject: Account Recovery for Quiz Trivia\n\n {otp} is your one time password !!! Please do not share it with anyone. ")
                    return redirect(url_for('forgot_password_otp',email = email_entry,form=form))
                
            flash(f'No user with email {email_entry} found! please register your account.',category="danger")
            return redirect(url_for('register_page'))
               
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category="danger")
    return render_template('Forgot_password.html',form=form)              
            
@app.route('/PasswordRecovery',methods=['GET','POST'])
def forgot_password_otp():
    nome = user_recovery
    form = Recovery()
    conn = db_conn()
    cur = conn.cursor()
    print(otp_gen)
    otp_entered = request.form.get('otp')
    if form.validate_on_submit():
        cur.execute(f''' select username,password from userinfo where email_address like '%{nome}%' ''')
        data= cur.fetchall()
        print(data)
        if otp_gen == otp_entered:
            print('hola')
        else:
            print('otp mismatch')
            flash('Otp Mismatch! Try Again!', category="danger")
            
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category="danger")
            
    return render_template('Forgot_password_otp.html',email = nome,form=form)
        

   
@app.route('/Front',methods=['POST','GET'])
def game_play():
    global user_cat, user_diff,user_noq
    user_cat = request.form['category']
    user_diff= request.form['difficulty']
    user_noq = request.form['no_of_questions']
    user_category = user_cat
    no_of_question = user_noq
    difficulty_of_questions = user_diff
    print(user_cat)
    print(user_noq)
    print(user_diff)
    return render_template('game.html',uc = user_category, noq=no_of_question,doq=difficulty_of_questions,un = nameProfile)



@app.route('/templates/end.html')
def end():
    return render_template('end.html')


if __name__ == "__main__":
    app.run(debug=True)

    
    
