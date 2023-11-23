from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField, PasswordField
from wtforms.validators import DataRequired, email, Length,EqualTo


class ContactForm(FlaskForm):
    fullname=StringField("Fullname",validators=[DataRequired(message="enter your fullname")])
    confirm_name=StringField("Confirm Name",validators=[DataRequired(message="haba!"),EqualTo('fullname',message="do you mean your names are different?")])
    email=StringField("email", validators=[email()])
    message=TextAreaField("message", validators=[Length(10,20)])
    btn=SubmitField("Send Message")

class SignupForm(FlaskForm):
    fullname = StringField("Fullname",validators=[DataRequired(message="hello, full name required")])
    email = StringField("Your Email",validators=[email()])
    password=PasswordField("Password",validators=[DataRequired()])
    confirm_password=PasswordField("Confirm Password",validators=[EqualTo("password",message="Must match password")])
    
    btn = SubmitField("Sign Up!")




class PostForm(FlaskForm):
    title=StringField("Post Title", validators=[DataRequired()])
    author=StringField("Author", validators=[DataRequired()])
    content=TextAreaField("Your Post", validators=[DataRequired()])
    btn=SubmitField("Submit")


class ContactUs(FlaskForm):
    fullname=StringField("Fullname",validators=[DataRequired()])
    phone=StringField("Phone", validators=[DataRequired()])
    email=StringField("email", validators=[email()])
    message=TextAreaField("message", validators=[Length(10,20)])
    btn=SubmitField("Send Message")


