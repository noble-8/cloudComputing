import json
import pymysql
import random

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



def genquery():
	cnx = make_connection()
	cursor = cnx.cursor()
	def random_char(char_num):
		return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))

	query = '''select pat_id from cpop_patients'''
	cursor.execute(query)
	results_list = []
	for result in cursor:
		results_list.append(result[0])
	
	for patId in results_list:
		degree = random.choice(["\"High School\"", "\"Bachelor\'s Degree\"", "\"Master\'s Degree\"", "\"PhD\""])
		query = f'''insert into cpop_pat_info values ({patId}, {degree}, {random.randint(0, 30)}, {random.choice([1,2,3])}, {random.choice([0,1])}, {random.choice([0,1])},{random.choice([0,1])},{random.choice([0,1])},{random.choice([0,1])})''' 
		print(query)
		cursor.execute(query)
		cnx.commit()
	cursor.close()
	return


genquery()
