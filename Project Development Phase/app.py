from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape
from newsapi import NewsApiClient

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ylx10738;PWD=YuqgHrF3ar3j4hsD",'','')

app = Flask(__name__)



@app.route('/')
def home():
  return render_template('index.html')



@app.route('/addUser')
def new_student():
  return render_template('add_student.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['name']
    address = request.form['address']
    city = request.form['city']
    pin = request.form['pin']

    sql = "SELECT * FROM students WHERE name =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      # return render_template('dashboard.html', msg="You are already a member, please login using your details")
      return redirect('/dash')
    else:
      insert_sql = "INSERT INTO students VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, address)
      ibm_db.bind_param(prep_stmt, 3, city)
      ibm_db.bind_param(prep_stmt, 4, pin)
      ibm_db.execute(prep_stmt)
    
    return render_template('login.html', msg="User Data saved successfuly..")

@app.route('/list')
def list():
  students = []
  sql = "SELECT * FROM Students"
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_both(stmt)
  while dictionary != False:
    # print ("The Name is : ",  dictionary)
    students.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)

  if students:
    return render_template("list.html", students = students)

@app.route('/delete/<name>')
def delete(name):
  sql = f"SELECT * FROM Students WHERE name='{escape(name)}'"
  print(sql)
  stmt = ibm_db.exec_immediate(conn, sql)
  student = ibm_db.fetch_row(stmt)
  print ("The Name is : ",  student)
  if student:
    sql = f"DELETE FROM Students WHERE name='{escape(name)}'"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)

    students = []
    sql = "SELECT * FROM Students"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
      students.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
    if students:
      return render_template("list.html", students = students, msg="Delete successfully")

  



  
  # # while student != False:
  # #   print ("The Name is : ",  student)

  # print(student)
    # return "success..."

if __name__ == '__main__':
   app.run(debug = True)

# @app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
# def edit(id):
    
#     post = BlogPost.query.get_or_404(id)

#     if request.method == 'POST':
#         post.title = request.form['title']
#         post.author = request.form['author']
#         post.content = request.form['content']
#         db.session.commit()
#         return redirect('/posts')
#     else:
#         return render_template('edit.html', post=post)
