from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, PasswordField,BooleanField 
from wtforms.fields.html5 import EmailField
from wtforms import ValidationError
from wtforms.validators import DataRequired
#from modle import database
#from passlib.hash import pbkdf2_sha256

class FormRegister(Form):

    username = StringField('使用者名稱',validators=[
        validators.DataRequired(),
        validators.Length(2, 30)
    ])
    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(1, 50),
        validators.Email()
    ])
    idcard = StringField('身分證字號',validators=[
        validators.DataRequired(),
        validators.Length(10,20)
    ])
    password = PasswordField('密碼', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='PASSWORD NEED MATCH')
    ])
    password2 = PasswordField('請再輸入一次密碼', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Register New Account')


'''def validate_email():
    email =  database.query.filter_by(email=database.email).first()
    if email is True:
        raise ValidationError('Email already register by somebody')

def validate_username():
    username = database.query.filter_by(username=database.username).first()
    if username is True:
        raise  ValidationError('UserName already register by somebody')
        
def vaildate_idcard():
    idcard = database.query.filter_by(idcard=database.idcard).first()
    if idcard is True:
        raise ValidationError('idcard already register by somebody')
    
'''
   
'''    from database_table import db,database


    if request.method == 'POST':

        first = request.form["first_pass"]
        new = request.form["new_pass"]
        print(first,new)
        passw = database.query.filter_by(password=first).first()
        #print(passw)
        if passw == None:
            return "password Not Found"
        passw.password = new
        db.session.add(passw)
        db.session.commit()
        #print(new)
        return "success"
    else:
        return render_template('update.html')'''