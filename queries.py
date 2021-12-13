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

	basequery = '''SELECT cp.pat_id FROM cpop_patients cp, cpop_pat_info cpi, cpop_alcohol_lookup cal, cpop_race cr, cpop_survey_responses csr WHERE cp.pat_id = cpi.pat_id AND cp.race_id = cr.race_id AND cpi.alcohol_id = cal.alcohol_id AND cp.pat_id = csr.pat_id'''
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
		exclusions = exclusions+';cp.doc_id=0'
		for field in aliases.keys():
			exclusions = exclusions.replace(field, aliases[field])
		exclbaseq = (exclbaseq+' AND '+exclusions).replace(';', 'AND')
		
	#cursor.execute(basequery)
	#for result in cursor:
	#	print(result)
	#cursor.close()
	return basequery + ' AND cp.pat_id NOT IN (' + exclbaseq+' )' if exclusions else basequery

#print(parseIncl('age>20;race="Asian"', 'cigarettes<10'))
string = '''insert into cpop_survey_responses values(0, 1, 2, "2021-04-09 12:12:12", "Pre_op", 4, 0, 2, 0, 2, 0, 5, 2, 1, 1, 2, 3, 5, 0, 1, 1, 4, 0, 2, 4, 0, 4)
insert into cpop_survey_responses values(0, 1, 2, "2021-04-11 12:12:12", "Post_op", 5, 5, 4, 4, 2, 0, 3, 0, 4, 1, 4, 5, 3, 5, 0, 5, 2, 0, 2, 4, 3, 0)
insert into cpop_survey_responses values(0, 1, 2, "2021-07-09 12:12:12", "3_months", 5, 5, 3, 2, 3, 3, 0, 0, 4, 0, 5, 2, 0, 3, 1, 0, 1, 1, 0, 1, 1, 1)
insert into cpop_survey_responses values(0, 1, 2, "2021-10-07 12:12:12", "6_months", 3, 2, 5, 2, 5, 0, 4, 5, 2, 4, 2, 4, 4, 4, 5, 0, 1, 4, 1, 1, 2, 4)
insert into cpop_survey_responses values(0, 2, 3, "2020-12-31 12:12:12", "Pre_op", 4, 3, 0, 4, 3, 3, 1, 5, 4, 0, 4, 2, 2, 5, 2, 1, 2, 5, 1, 3, 3, 0)
insert into cpop_survey_responses values(0, 2, 3, "2021-01-02 12:12:12", "Post_op", 2, 0, 2, 1, 1, 5, 2, 1, 0, 3, 0, 0, 2, 0, 1, 4, 0, 5, 1, 4, 1, 4)
insert into cpop_survey_responses values(0, 2, 3, "2021-04-01 12:12:12", "3_months", 5, 4, 4, 3, 5, 1, 1, 1, 4, 1, 2, 0, 1, 3, 0, 5, 2, 2, 4, 2, 4, 1)
insert into cpop_survey_responses values(0, 2, 3, "2021-06-30 12:12:12", "6_months", 1, 5, 3, 1, 0, 2, 0, 0, 5, 0, 4, 0, 2, 5, 0, 1, 4, 4, 1, 3, 0, 0)
insert into cpop_survey_responses values(0, 3, 2, "2021-01-31 12:12:12", "Pre_op", 3, 0, 4, 5, 5, 5, 4, 3, 0, 0, 3, 0, 2, 4, 1, 2, 3, 2, 3, 5, 4, 5)
insert into cpop_survey_responses values(0, 3, 2, "2021-02-02 12:12:12", "Post_op", 2, 0, 2, 5, 4, 2, 3, 2, 5, 3, 4, 3, 1, 5, 2, 1, 4, 5, 2, 4, 0, 0)
insert into cpop_survey_responses values(0, 3, 2, "2021-05-02 12:12:12", "3_months", 5, 3, 0, 3, 2, 4, 3, 4, 2, 3, 5, 1, 2, 0, 3, 2, 1, 3, 5, 4, 4, 0)
insert into cpop_survey_responses values(0, 3, 2, "2021-07-31 12:12:12", "6_months", 0, 0, 0, 3, 2, 3, 1, 1, 5, 0, 4, 2, 1, 0, 0, 0, 3, 0, 4, 2, 4, 1)
insert into cpop_survey_responses values(0, 4, 2, "2021-01-31 12:12:12", "Pre_op", 0, 4, 2, 3, 0, 0, 2, 4, 4, 5, 1, 4, 5, 2, 2, 1, 4, 1, 3, 5, 0, 3)
insert into cpop_survey_responses values(0, 4, 2, "2021-02-02 12:12:12", "Post_op", 3, 1, 0, 4, 0, 1, 5, 5, 3, 3, 0, 1, 4, 0, 2, 4, 0, 5, 3, 4, 4, 3)
insert into cpop_survey_responses values(0, 4, 2, "2021-05-02 12:12:12", "3_months", 3, 3, 5, 4, 3, 2, 4, 5, 5, 3, 0, 1, 3, 3, 3, 0, 1, 5, 0, 2, 2, 2)
insert into cpop_survey_responses values(0, 4, 2, "2021-07-31 12:12:12", "6_months", 2, 5, 2, 2, 5, 4, 1, 5, 1, 4, 3, 4, 1, 0, 5, 4, 4, 1, 4, 3, 0, 2)
insert into cpop_survey_responses values(0, 8, 2, "2021-02-28 12:12:12", "Pre_op", 5, 1, 0, 1, 2, 3, 0, 1, 0, 4, 3, 4, 1, 4, 0, 5, 2, 5, 3, 0, 5, 3)
insert into cpop_survey_responses values(0, 8, 2, "2021-03-02 12:12:12", "Post_op", 3, 3, 1, 3, 5, 5, 5, 2, 2, 3, 1, 2, 3, 4, 0, 5, 0, 2, 4, 2, 1, 4)
insert into cpop_survey_responses values(0, 8, 2, "2021-05-30 12:12:12", "3_months", 5, 1, 1, 4, 2, 2, 0, 4, 0, 4, 1, 4, 4, 1, 4, 2, 5, 2, 3, 5, 3, 0)
insert into cpop_survey_responses values(0, 8, 2, "2021-08-28 12:12:12", "6_months", 2, 5, 5, 5, 0, 0, 1, 3, 4, 1, 4, 0, 5, 0, 2, 1, 2, 0, 1, 4, 5, 3)
insert into cpop_survey_responses values(0, 12, 1, "2021-02-28 12:12:12", "Pre_op", 3, 0, 2, 5, 1, 2, 3, 5, 2, 0, 2, 4, 3, 4, 4, 2, 5, 2, 4, 0, 4, 1)
insert into cpop_survey_responses values(0, 12, 1, "2021-03-02 12:12:12", "Post_op", 4, 4, 4, 5, 3, 1, 3, 1, 2, 4, 4, 4, 3, 4, 2, 0, 3, 1, 0, 4, 4, 0)
insert into cpop_survey_responses values(0, 12, 1, "2021-05-30 12:12:12", "3_months", 3, 0, 2, 4, 3, 2, 4, 1, 2, 1, 5, 2, 0, 2, 3, 5, 0, 1, 3, 4, 5, 2)
insert into cpop_survey_responses values(0, 12, 1, "2021-08-28 12:12:12", "6_months", 4, 3, 1, 0, 0, 3, 0, 0, 2, 4, 4, 2, 0, 1, 0, 4, 3, 2, 4, 1, 4, 2)
insert into cpop_survey_responses values(0, 14, 3, "2021-03-31 12:12:12", "Pre_op", 0, 1, 0, 0, 4, 0, 0, 4, 3, 5, 5, 3, 0, 4, 5, 2, 3, 4, 4, 5, 1, 3)
insert into cpop_survey_responses values(0, 14, 3, "2021-04-02 12:12:12", "Post_op", 4, 1, 5, 2, 5, 5, 0, 4, 2, 3, 4, 2, 5, 2, 4, 0, 2, 1, 3, 4, 3, 1)
insert into cpop_survey_responses values(0, 14, 3, "2021-06-30 12:12:12", "3_months", 1, 0, 0, 5, 2, 1, 5, 5, 3, 0, 2, 3, 4, 4, 0, 1, 3, 3, 2, 0, 2, 0)
insert into cpop_survey_responses values(0, 14, 3, "2021-09-28 12:12:12", "6_months", 4, 4, 2, 2, 1, 3, 3, 2, 1, 0, 1, 4, 0, 4, 0, 3, 5, 1, 3, 2, 3, 5)
insert into cpop_survey_responses values(0, 15, 2, "2021-04-30 12:12:12", "Pre_op", 5, 5, 0, 3, 1, 2, 1, 2, 1, 4, 4, 1, 3, 3, 5, 2, 4, 4, 3, 1, 5, 1)
insert into cpop_survey_responses values(0, 15, 2, "2021-05-02 12:12:12", "Post_op", 4, 2, 4, 2, 1, 0, 1, 3, 3, 4, 1, 2, 2, 5, 5, 5, 4, 2, 3, 4, 0, 2)
insert into cpop_survey_responses values(0, 15, 2, "2021-07-30 12:12:12", "3_months", 5, 2, 1, 4, 5, 0, 4, 3, 1, 5, 5, 1, 0, 4, 0, 5, 5, 1, 4, 4, 1, 5)
insert into cpop_survey_responses values(0, 15, 2, "2021-10-28 12:12:12", "6_months", 0, 3, 4, 0, 0, 3, 4, 3, 5, 5, 3, 1, 0, 2, 3, 4, 0, 5, 5, 0, 0, 4)
insert into cpop_survey_responses values(0, 18, 1, "2021-05-04 12:12:12", "Pre_op", 1, 5, 4, 5, 0, 3, 1, 0, 4, 3, 2, 3, 3, 1, 2, 2, 2, 2, 5, 1, 3, 4)
insert into cpop_survey_responses values(0, 18, 1, "2021-05-06 12:12:12", "Post_op", 2, 1, 3, 3, 1, 3, 1, 2, 4, 2, 5, 2, 0, 1, 1, 1, 0, 1, 0, 3, 0, 1)
insert into cpop_survey_responses values(0, 18, 1, "2021-08-03 12:12:12", "3_months", 4, 2, 3, 1, 1, 5, 4, 4, 3, 3, 2, 3, 2, 4, 4, 4, 3, 4, 5, 0, 2, 4)
insert into cpop_survey_responses values(0, 18, 1, "2021-11-01 12:12:12", "6_months", 3, 5, 4, 5, 4, 4, 1, 1, 0, 3, 4, 5, 1, 5, 4, 1, 2, 4, 0, 0, 1, 3)
insert into cpop_survey_responses values(0, 20, 0, "2021-06-04 12:12:12", "Pre_op", 1, 5, 3, 5, 3, 0, 3, 0, 4, 2, 2, 5, 1, 3, 0, 2, 0, 2, 4, 3, 1, 2)
insert into cpop_survey_responses values(0, 20, 0, "2021-06-06 12:12:12", "Post_op", 1, 0, 4, 4, 4, 1, 1, 0, 3, 5, 2, 4, 1, 4, 1, 4, 0, 1, 5, 2, 2, 0)
insert into cpop_survey_responses values(0, 20, 0, "2021-09-03 12:12:12", "3_months", 0, 5, 3, 2, 1, 2, 4, 4, 1, 1, 2, 1, 4, 2, 2, 4, 5, 5, 4, 3, 1, 2)
insert into cpop_survey_responses values(0, 20, 0, "2021-12-02 12:12:12", "6_months", 3, 1, 4, 0, 5, 2, 4, 5, 0, 3, 0, 5, 2, 1, 1, 3, 4, 0, 0, 4, 4, 5)
insert into cpop_survey_responses values(0, 21, 1, "2021-06-04 12:12:12", "Pre_op", 4, 3, 1, 5, 0, 5, 0, 2, 0, 0, 3, 0, 3, 3, 1, 2, 2, 4, 4, 1, 3, 2)
insert into cpop_survey_responses values(0, 21, 1, "2021-06-06 12:12:12", "Post_op", 3, 4, 4, 5, 3, 2, 3, 5, 5, 4, 0, 2, 4, 1, 1, 3, 1, 2, 1, 1, 5, 0)
insert into cpop_survey_responses values(0, 21, 1, "2021-09-03 12:12:12", "3_months", 3, 3, 5, 1, 2, 3, 2, 5, 1, 2, 5, 0, 0, 4, 3, 5, 1, 5, 5, 4, 5, 2)
insert into cpop_survey_responses values(0, 21, 1, "2021-12-02 12:12:12", "6_months", 0, 0, 1, 4, 1, 0, 4, 5, 4, 0, 3, 4, 3, 4, 1, 3, 0, 3, 3, 2, 3, 0)
insert into cpop_survey_responses values(0, 22, 3, "2021-06-04 12:12:12", "Pre_op", 0, 0, 5, 2, 3, 4, 3, 4, 2, 1, 0, 4, 3, 1, 2, 5, 0, 3, 0, 5, 3, 4)
insert into cpop_survey_responses values(0, 22, 3, "2021-06-06 12:12:12", "Post_op", 4, 0, 4, 0, 5, 3, 3, 4, 4, 2, 0, 0, 3, 1, 4, 4, 2, 5, 0, 1, 0, 3)
insert into cpop_survey_responses values(0, 22, 3, "2021-09-03 12:12:12", "3_months", 2, 4, 2, 0, 0, 2, 5, 0, 3, 2, 4, 1, 1, 1, 5, 4, 1, 0, 4, 0, 4, 2)
insert into cpop_survey_responses values(0, 22, 3, "2021-12-02 12:12:12", "6_months", 1, 1, 5, 2, 4, 0, 0, 0, 4, 5, 2, 0, 3, 2, 4, 0, 4, 3, 3, 2, 2, 2)
insert into cpop_survey_responses values(0, 23, 0, "2021-06-04 12:12:12", "Pre_op", 5, 5, 4, 0, 2, 4, 4, 1, 1, 0, 1, 2, 5, 4, 3, 3, 2, 1, 5, 5, 3, 4)
insert into cpop_survey_responses values(0, 23, 0, "2021-06-06 12:12:12", "Post_op", 1, 0, 5, 2, 0, 5, 2, 5, 0, 0, 5, 2, 2, 5, 4, 4, 1, 2, 1, 4, 3, 1)
insert into cpop_survey_responses values(0, 23, 0, "2021-09-03 12:12:12", "3_months", 5, 3, 3, 5, 0, 5, 1, 2, 5, 1, 0, 2, 4, 3, 1, 1, 0, 0, 1, 3, 4, 1)
insert into cpop_survey_responses values(0, 23, 0, "2021-12-02 12:12:12", "6_months", 5, 2, 2, 5, 3, 3, 3, 0, 0, 3, 4, 4, 0, 4, 1, 1, 5, 2, 2, 0, 1, 3)
insert into cpop_survey_responses values(0, 24, 2, "2021-06-04 12:12:12", "Pre_op", 1, 4, 1, 4, 2, 3, 3, 0, 3, 1, 4, 4, 3, 5, 4, 4, 1, 0, 3, 4, 5, 0)
insert into cpop_survey_responses values(0, 24, 2, "2021-06-06 12:12:12", "Post_op", 2, 5, 5, 4, 3, 2, 1, 5, 1, 4, 1, 5, 1, 2, 2, 5, 1, 0, 5, 3, 3, 3)
insert into cpop_survey_responses values(0, 24, 2, "2021-09-03 12:12:12", "3_months", 3, 1, 2, 2, 1, 3, 3, 4, 3, 0, 1, 2, 3, 2, 3, 1, 3, 5, 2, 0, 5, 1)
insert into cpop_survey_responses values(0, 24, 2, "2021-12-02 12:12:12", "6_months", 0, 1, 1, 0, 0, 2, 3, 4, 4, 2, 2, 3, 4, 1, 4, 0, 1, 3, 3, 1, 1, 4)'''
cnx = make_connection()
cursor = cnx.cursor()
for line in string.splitlines():
	cursor.execute(line)
	cnx.commit()
cursor.close()	
