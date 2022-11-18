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

  
@app.route("/dash")
def dashboard():
    api_key = '361169dd3dae4d6a9395b7a1afd291a9'
    
    RAPID_API = NewsApiClient(api_key=api_key)

    top_headlines = RAPID_API.get_top_headlines(sources = "bbc-news")
    all_articles = RAPID_API.get_everything(sources = "bbc-news")

    t_articles = top_headlines['articles']
    a_articles = all_articles['articles']

    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range (len(t_articles)):
      main_article = t_articles[i]
      news.append(main_article['title'])
      desc.append(main_article['description'])
      img.append(main_article['urlToImage'])
      p_date.append(main_article['publishedAt'])
      url.append(main_article['url'])

      contents = zip( news,desc,img,p_date,url)

    news_all = []
    desc_all = []
    img_all = []
    p_date_all = []   
    url_all = []

    for j in range(len(a_articles)): 
        main_all_articles = a_articles[j]   

        news_all.append(main_all_articles['title'])
        desc_all.append(main_all_articles['description'])
        img_all.append(main_all_articles['urlToImage'])
        p_date_all.append(main_all_articles['publishedAt'])
        url_all.append(main_article['url'])
        
        all = zip( news_all,desc_all,img_all,p_date_all,url_all)

    return render_template('dashboard.html',contents=contents,all = all)


  


if __name__ == '__main__':
   app.run(debug = True)
