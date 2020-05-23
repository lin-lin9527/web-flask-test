from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1) 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.sqlite'
app.config['SECRET_KEY']='your key'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)



class database(db.Model):
    __tablename__ = "web_data"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(80),unique=True,nullable=False)
    idcard = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
    bool_ = db.Column(db.Boolean,default=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    def __init__(self,username,email,idcard,password):
        self.username=username
        self.email=email
        self.idcard=idcard
        self.password=password

        
    def __repr__(self):
        return "username:%s,email:%s,idcard:%s,bool_:%s,insert_time:%s" %(self.username,self.email,self.idcard,self.bool_,self.insert_time)
    

if __name__ == '__main__':
    manager.run()