
Working with IBM Db2 service 

Step 1 : install Python SDK 

```
pip install ibm-db
```

> add the connection details from IBM DB2 as show under Service credentials of Portal

> Download SSL Certificate form setting pages of IBM DB2



Stpe 2 : Run flask app in debug mode 

```
flask --debug run
```

OR 

```
 export FLASK_ENV=development
 flask run

```

Open the application

```
http://127.0.0.1:5000/



