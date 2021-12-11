import json
from flask import Flask
from flask import request
from flask import send_file
import pymysql
endpoint = 'wed8.c34yxqfbf9wx.us-east-2.rds.amazonaws.com'
port = '3306'
dbuser = 'admin'
password = 'rootroot'
database = 'rds'

#query = """insert into cpop_users values (5, 'Shreyes', 23, 'M', 'Asian')"""
#query = """select * from cpop_users"""

def make_connection():
    return pymysql.connect(
        host=endpoint,
        user=dbuser,
        port=int(port),
        passwd=password,
        db=database)


app = Flask(__name__)

table = 'cpop_users'
@app.route('/')
def home():
	return send_file("figure.png", mimetype='image/gif')

@app.route('/list')
def list():
	cnx = make_connection()
	cursor = cnx.cursor()
	print(table)
	query = f'select * from {table}'
	cursor.execute(query)
	results_list = []
	for result in cursor:
		results_list.append(result)
		print(results_list)
	cursor.close()
	return json.dumps(results_list)

@app.route('/get/<name>')
def get_by_name(name):
	cnx = make_connection()
	cursor = cnx.cursor()
	query = f'''select * from {table} where name=\"{name}\"'''
	cursor.execute(query)
	results_list = []
	for result in cursor:
		results_list.append(result)
		print(results_list)
	cursor.close()
	return json.dumps(results_list)

@app.route('/signup', methods= ['POST'])
def index():
	#Id, name, age, gender, race = request.args['id'], request.args['name'], request.args['age'], request.args['gender'], request.args['race']
	body = request.get_json( )
	email, password, name, age, gender, race , doc_id , start_date , end_date = body['email'],body['password'],body['name'],body['age'],body['gender'],body['race'],body['doctor'] ,body['start_date'],body['end_date']
	cnx = make_connection()
	cursor = cnx.cursor();
	#INSERT INTO cpop_patients VALUES (0,1,'2020-12-10 12:12:12','4712-12-12 00:00:00', 'Abhishek Verule', 25,'M', 1, 'abc@xyz.com');
	query = f'''INSERT INTO cpop_patients VALUES (0,1,"{start_date}",'{end_date}', '{name}',{age} ,'{gender}',{race} , '{email}');''';
	try:
		cursor.execute(query)
		cnx.commit()
		cursor.close()
		return "{msg:entered successfully}"
	except  Exception as e: 
		print(e);
		return "check syntax"
	


app.run(host="0.0.0.0",port=8080)
#app.run(host="localhost", port=8000, debug=True)

