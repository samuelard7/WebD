from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class RegisterForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=5, max=15) , DataRequired()])
    passw = PasswordField(label='Password', validators= [Length(min=6), DataRequired()]) 
    cpassw = PasswordField(label='Confirm Password', validators=[EqualTo('passw'), DataRequired()])
    email_address =StringField(label='Email', validators=[Email()])
    submit = SubmitField(label='Submit')
    
class Recovery(FlaskForm):

    email_add =StringField(label='Email', validators=[Email()])
    otp = PasswordField(label='OTP',validators=[Length(max=6)])
    submit = SubmitField(label='Submit')

      
    


    