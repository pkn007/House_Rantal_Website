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


@app.route('/')
def index():
    return render_template('home.html') 


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
    return render_template('User_login.html',msg = msg)

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
            return redirect(url_for('owner',msg = accounts[1]))
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
            return redirect('owner',msg = ownername)
    return render_template('owner_register.html',msg = msg)
        
        
@app.route('/house_register',methods = ['GET','POST'])
def house_register():
    msg = ''  
    ok = request.args.get('id')
    if ok:
        id = ok
    # if request.method == 'POST':
    if request.method == "POST":
        size = request.form['size']
        size = request.form['size']
        size = request.form['size']
        size = request.form['size']
        
    return render_template('house.html',msg = msg)
        
@app.route('/owner')
def owner():
    msg = []
    name = request.args.get('msg')
    account = None
    if id:
        cur.execute(f"SELECT * FROM land_lord where username = '{name}'")
        account = cur.fetchone()
    return render_template('owner_page.html',name = account[1],id = account[0])
        
    
if __name__ == '__main__':
    app.run(debug = True)       




# eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InByaXRhbWd1cmF2OTUyNzJAZ21haWwuY29tIiwiZ29vZ2xlQW5hbHl0aWNzSWQiOiIxNjc2Mjc3ODc2LjE2OTkyNTA4NTgiLCJtaXhwYW5lbElkIjoiJGRldmljZToxOGJhMzNlNWViMzFmOTUtMDc5ZWE2YmVkNjNmNzMtMjYwMzExNTEtMTQ0MDAwLTE4YmEzM2U1ZWIzMWY5NSIsIm1peHBhbmVsUHJvamVjdElkIjoiNGJmYjI0MTRhYjk3M2M3NDFiNmYwNjdiZjA2ZDU1NzUiLCJvcmciOiJwZXMgdW5pdmVyc2l0eSIsInB1YiI6Im5lbzRqLmNvbSIsInJlZyI6InByaXRhbSBndXJhdiIsInN1YiI6Im5lbzRqLWRlc2t0b3AiLCJleHAiOjE3MzA4NzMzMDgsInZlciI6IioiLCJpc3MiOiJuZW80ai5jb20iLCJuYmYiOjE2OTkyNTA5MDgsImlhdCI6MTY5OTI1MDkwOCwianRpIjoiNm1LdVZVRjEyIn0.rzldcTBEQJ7NjoT3WPGoBkE_HyiMHp3QzB8zXgwRjhSTDOyoaLLLkAYB8SZqvFiaQv3UdsyWbE7v6lGQZoEd9nV7EV5hlU1WjRhr3QhL7Io3hZeQjWeRblOisH4vKQW7_FxI2whQNcqOZj7aS9uJvbjX871vQEdmKXjsFge47-XusqrFyp8R96uqBGc0hALuJvffHKQPfWAstesO640BcCj8YlApjmsTA1eg6N5e4ZWWo7rM2mL__IRt9ejSTQ6EwhKXqQQiEdqF63x4US1n3Y2udt2h0okESWjd57HZBG9iWNJq8LsjLD73xNaO7b_Useyh4eRfp-20KapQ5mb2SQ

    


# 118000878027911