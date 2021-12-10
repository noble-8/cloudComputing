import json
from flask import Flask
from flask import request
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
	return 'hello world'


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
	doc_id, email, password, name, age, gender, race = body['doctor'],body['email'],body['password'],body['name'],body['age'],body['gender'],body['race']
	cnx = make_connection()
	cursor = cnx.cursor()	
	query = f'''insert into cpop_patients values (\"0\",\"{doc_id}\","{name}\",\"{age}\",\"{gender}\",\"{race}\")'''
	cursor.execute(query)
	cnx.commit()
	cursor.close()
	return "hello"
	


app.run(host="0.0.0.0",port=8080)
#app.run(host="localhost", port=8000, debug=True)

