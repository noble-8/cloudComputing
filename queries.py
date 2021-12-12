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
		#print(query)
		cursor.execute(query)
		cnx.commit()
	cursor.close()
	return


def parseIncl(inclusions, exclusions):
	
	#cnx = make_connection()
	#cursor = cnx.cursor()	

	basequery = '''SELECT cp.pat_id FROM cpop_patients cp, cpop_pat_info cpi, cpop_alcohol_lookup cal, cpop_race cr WHERE cp.pat_id = cpi.pat_id AND cp.race_id = cr.race_id AND cpi.alcohol_id = cal.alcohol_id'''
	exclbaseq = ''+basequery
	aliases = {
    	"age" : "cp.age",
    	"gender" : "cp.gender",
    	"race" : "cr.race",
    	"cigarettes" : "cpi.cigarettes",
    	"alcohol" : "cal.answer",
    	"asthma" : "cpi.asthma",
    	"diabetes" : "cpi.diabetes",
    	"allergic rhinitis": "cpi.allergic_rhinitis",
    	"aspirin sensitivity" : "cpi.aspirin_sensitivity",
		"depression": "cpi.depression"
	}
	if inclusions:
		for field in aliases.keys():
			inclusions = inclusions.replace(field, aliases[field])
		basequery = (basequery+' AND '+inclusions).replace(';', ' AND ')
	
	if exclusions:
		for field in aliases.keys():
			exclusions = exclusions.replace(field, aliases[field])
		exclbaseq = (exclbaseq+' AND '+exclusions).replace(';', 'AND')
		
	#cursor.execute(basequery)
	#for result in cursor:
	#	print(result)
	#cursor.close()
	return basequery + ' AND cp.pat_id NOT IN (' + exclbaseq+' )' if exclusions else basequery

print(parseIncl('age>20;race="Asian"', 'cigarettes<10'))
