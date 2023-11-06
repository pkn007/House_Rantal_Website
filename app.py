from flask import Flask, render_template,redirect,url_for, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector

app = Flask(__name__)


db=mysql.connector.connect(
   host="127.0.0.1",
   port="3306",
   user="root",
   passwd="Pritam@95272",
   database="house_rental_system"
)

cur = db.cursor()

cur.execute("SELECT * FROM tenant")

@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/user_login', methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur.execute('SELECT * FROM tenant WHERE username = %s AND password = %s',(username,password))
        account = cur.fetchone()
        if account:
            msg = 'Logged In Successfully'
            
        else:
            msg = 'Incorrect username/password'
    return render_template('login.html',msg = msg)

@app.route('/user_register',methods = ['GET','POST'])
def register():
    msg = ''
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        print(request)
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        number = request.form['number']
        employment_status = request.form['employment']
        marital_status = request.form['marital']
        age = request.form['age']
        str = f"SELECT * FROM tenant WHERE username = '{(username)}'"
        print(str)
        cur.execute(str)
        account = cur.fetchone()
        print(account)
        if account:
            msg = "Account Already Exists"
        elif int(age) < 19 or int(age) > 100:
            msg = "Enter Correct Age"
        else:
            cur.execute('INSERT INTO tenant (username, password, age, contact_info, employment_info,tanant_name,marital_status) VALUES (%s,%s,%s,%s,%s,%s,%s)',(username,password,int(age),number,employment_status,name,marital_status))
            db.commit()
            msg = "User Registered"
    return render_template('user_register.html',msg = msg)  

@app.route('/owner_login',methods = ['POST','GET'])
def owner_login():
    msg = ''
    if request.method == 'POST' and 'ownername' in  request.form and 'password' in request.form:
        ownername = request.form['ownername']
        password = request.form['password']
        cur.execute("SELECT * FROM land_lord WHERE username = %s and password = %s",(ownername,password))
        accounts = cur.fetchone()
        if accounts:
            msg = "Land_Lord Logged In"
        else:
            msg = "Enter Correct Username or Password"
    return render_template('owner_login.html',msg = msg)

@app.route('/owner_register',methods = ['GET','POST'])
def owner_register():
    msg = ""
    if request.method == 'POST':
        ownername = request.form['ownername']
        password = request.form['password']
        name = request.form['name']
        contact = request.form['contact']
        cur.execute(f"SELECT * FROM land_lord WHERE username = '{ownername}'")
        account = cur.fetchone()
        if account:
            msg = "The Account Already Exists"
        else:
            cur.execute("insert into land_lord (username,password,name,contact_info) values (%s,%s,%s,%s)",(ownername,password,name,contact))
            db.commit()
            msg = "Land_Lord Register"
    return render_template('owner_register.html',msg = msg)
        
        
@app.route('/owner/house_register',methods = ['GET','POST'])
def house_register():
    msg = ''
    if request.method == 'POST':
        rent = request.form("rent")
        
    
if __name__ == '__main__':
    app.run(debug = True)       


    

