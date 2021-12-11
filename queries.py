import json
import pymysql
import random
import re

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


def parseIncl():
    aliases = {'age':'cp.age','race':'cr.race'}
    sample = '''age>20;race="Asian"'''

    basequery = '''SELECT
                cp.pat_id
                FROM
                cpop_patients cp
                ,cpop_pat_info cpi
                ,cpop_alcohol_lookup cal
                ,cpop_race cr
                WHERE
                cp.pat_id = cpi.pat_id
                AND cp.race_id = cr.race_id
                AND cpi.alcohol_id = cal.alcohol_id
                '''

    for cond in sample.split(';'):
        cond_pred = re.split(
        query = '''SELECT 
                cp.pat_id
                FROM
                cpop_patients cp
                ,cpop_pat_info cpi
                ,cpop_alcohol_lookup cal
                ,cpop_race cr
                WHERE
                cp.pat_id = cpi.pat_id
                AND cp.race_id = cr.race_id
                AND cpi.alcohol_id = cal.alcohol_id
                AND {aliases['cond_pred'} {cond_op} {cond_val}
                '''

parseIncl()


