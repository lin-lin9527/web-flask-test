from modle import db
from modle import app
from modle import database
from flask_mail import Message,Mail
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import secure_filename
from flask import render_template, jsonify, request,url_for,make_response
import os,cv2,time,json,csv
from fpdf import FPDF
from werkzeug.security import generate_password_hash,check_password_hash
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app.config.update(
    #  gmail的設置
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PROT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='youaks87@gmail.com',
    MAIL_PASSWORD='youaks1557link'
)
#  gmail記得開權限
mail = Mail(app)

#表單資料填寫-----------------------------------------------------------
@app.route('/api/register', methods=['GET', 'POST'])
def register():
    from form import FormRegister
    form =FormRegister()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        idcard = form.idcard.data
        password = form.password.data
        
        hashed_pswd = generate_password_hash(password)
        user = database(
            username = username,
            email = email,
            idcard = idcard,
            password = hashed_pswd
        )
        if user != True:
            db.session.add(user)
            db.session.commit()
            return "success"
        else:
            return "error"
    return render_template('test.html', form=form)

#使用者資料查詢--------------------------------------------------------
@app.route('/api/admin',methods=['GET','POST'])
def users():
    if request.method == 'GET':
       users = database.query.all()
       return jsonify(["id :{0} username:{1} email:{2} idcard:{3} password:{4}".format(user.id ,user.username, user.email,user.idcard,user.password) for user in users])
    if request.method =='POST':
           return "post"

#資料刪除--------------------------------------------------------------
@app.route('/api/user/delete/<int:id>')
def userdelete(id):
    task_to_delete = database.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return"data already delete"

#上傳圖片-----------------------------------------------------------------
@app.route('/api/upload',methods=['GET','POST'])
def upload():
    if request.method =='POST':
        f = request.files['file']
        if not(f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "please use 'png', 'jpg', 'JPG', 'PNG', 'bmp'"})
        user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)  # 當前文件所在路徑
        upload_path = os.path.join(basepath, 'static/photo', secure_filename(f.filename))  # 注意：没有的文件夹一定要先創建，不然會提示没有該路徑
        f.save(upload_path)
        # 使用Opencv轉換一下圖片格式和名稱
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/photo', 'test.jpg'), img)
        return render_template('upload_ok.html',userinput=user_input,val1=time.time())
    return render_template('picture.html')

#帳號登入-----------------------------------------------------------
@app.route('/')
def web():
    return render_template("form.html")
@app.route('/api' ,methods=["POST"])
def count():
    username = request.form["username"]
    password = request.form["password"]
    name = database.query.filter_by(username=username).first() 
    if name == None:
        return jsonify({"username":username+" Not Found"}),400
    elif not pbkdf2_sha256.verify(password, name.password):
        return "密碼錯誤"
    
    '''pas = database.query.filter_by(password=password).first()
    if pas == None:
        return "密碼錯誤"'''
    return "welcome to my web, {}".format(username)

#修改密碼--------------------------------------------------------------
@app.route('/api/update',methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        username = request.form["username"]
        first = request.form["first_pass"]
        new = request.form["new_pass"]
        first_password = pbkdf2_sha256.hash(first)
        new_password = pbkdf2_sha256.hash(new)
        name = database.query.filter_by(username = username).first()
        if name == None:
            return jsonify({"username":username+" Not Found"}),400
        elif  pbkdf2_sha256.verify(first_password, name.password):
            return "error01"
        elif  pbkdf2_sha256.verify(new_password, name.password):
            return "error02"
        name.password = new_password
        db.session.add(name)
        db.session.commit()
        return "success"
    else:
        return render_template('update.html')

#假刪除(隱藏資訊)----------------------------------------------------------
@app.route('/api/user/<string:username>/delete')
def hide(username):
    task_to_delete =  database.query.filter_by(username=username).first()
    #db.session.delete(task_to_delete)
    task_to_delete.bool_=True
    db.session.add(task_to_delete)
    db.session.commit()
    return"data already hide"

#資料復原-------------------------------------------------------------------
@app.route('/api/user/<string:username>/reset')
def reset(username):
    task_to_reset = database.query.filter_by(username=username).first()
    task_to_reset.bool_=False
    db.session.add(task_to_reset)
    db.session.commit()
    return "data already reset"

#單獨資料查詢----------------------------------------------------------------    
@app.route('/api/user/<string:username>',methods=['GET'])
def user(username):
   #user = database.query.filter_by(id=id).first()
   hide = database.query.filter_by(username=username).first()
   if hide == None:
       return "not found this user"
   if hide.bool_==True:
       return "this user’s data already hide"
   else:
       data = hide.__dict__
       data.pop("_sa_instance_state")
       return jsonify(data),200 
   
# mail寄件-------------------------------------------------------------------
@app.route("/api/message",methods=["GET","POST"])
def index():
       if request.method=="POST":
              title = request.form["title"]
              sender = request.form["email1"]
              recipients = [request.form["email2"]]
              rec = list(recipients)             
              body = request.form["comment"]
              msg = Message(title,
                            sender=sender,
                            recipients=rec)
              msg.body = body
              mail.send(msg)
              return "success"
       return render_template("email.html")

#csv下載----------------------------------------------------------------------
@app.route('/api/download/csv')
def csvdownload():
    with open ('output.csv','w',newline='', encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['id','username','email','身分證字號','帳號狀態','創建時間'])
        user = database.query.all()
        for item in user:
            writer.writerow([item.id,item.username,item.email,item.idcard,item.bool_,item.insert_time])
    return "已經成功下載"

#json下載---------------------------------------------------------------------
@app.route('/api/download/json')
def jsondownload(): 
    csvfile = open('output.csv','r', encoding='utf-8')
    jsonfile = open('output.json','w', encoding='utf-8')
    reader = csv.DictReader(csvfile)
    for row in reader:
        json.dump(row,jsonfile,ensure_ascii=False)
        jsonfile.write('\n')
    return "已經成功下載"


'''
import numpy as np
@app.route('/api/download/pdf')
def pdfdownload():
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=12)
    test = database.query.all()
    for item in test:
        pdf.cell(200,10,txt=item.username, ln=1,align="C")
        pdf.output("output.pdf")
'''     



if __name__ == '__main__':
    app.run(debug=True)
