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

@app.route('/post')
def index():
	Id, name, age, gender, race = request.args['id'], request.args['name'], request.args['age'], request.args['gender'], request.args['race']
	cnx = make_connection()
	cursor = cnx.cursor()
	table = request.args.get('table')
	query = f'''insert into {table} values (\"{Id}\",\"{name}\",\"{age}\",\"{gender}\",\"{race}\")'''
	cursor.execute(query)
	cnx.commit()
	cursor.close()
	get_by_name(name)



app.run(port=8080)
#app.run(host="localhost", port=8000, debug=True)

