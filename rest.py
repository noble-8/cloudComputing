import json
import hashlib
from flask import Flask
from flask import request
from flask import send_file
import pymysql
from datetime import datetime 
from datetime import timedelta

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

table = 'cpop_auth'
@app.route('/')
def home():
    return "hello world" 

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

@app.route('/signupPatient', methods= ['POST'])
def index():
    #Id, name, age, gender, race = request.args['id'], request.args['name'], request.args['age'], request.args['gender'], request.args['race']
    body = request.get_json( )
    email, password, name, age, gender, race , doc_id , start_date , end_date = body['email'],body['password'],body['name'],body['age'],body['gender'],body['race'],body['doctor'] ,body['start_date'],body['end_date']
    try:
        cnx = make_connection()
        cursor = cnx.cursor();
        #INSERT INTO cpop_auth VALUES ("uname","password",role_id,"token");
        token = hashlib.sha1('{password}'.encode('utf-8')).hexdigest()
        #hashlib.md5(b'{password}').hexdigest();
        query = f''' INSERT INTO cpop_auth VALUES ("{email}","{password}",2,"{token}")''';
        cursor.execute(query)
        cursor = cnx.cursor();
        #INSERT INTO cpop_patients VALUES (0,1,'2020-12-10 12:12:12','4712-12-12 00:00:00', 'Abhishek Verule', 25,'M', 1, 'abc@xyz.com');
        query = f'''INSERT INTO cpop_patients VALUES (0,1,"{start_date}",'{end_date}', '{name}',{age} ,'{gender}',{race} , '{email}');''';
        cursor.execute(query)
        query = f'''select pat_id from cpop_patients where email="{email}"'''
        cursor.execute(query)
        results_list = []
        for result in cursor:
            results_list.append(result)
        cursor.close()
        cnx.commit()
        cursor.close()
        return json.dumps(results_list)
    except  Exception as e: 
        print(e);
        return "check syntax"
    
@app.route('/signupDoctor', methods= ['POST'])
def signupDoc():
    #Id, name, age, gender, race = request.args['id'], request.args['name'], request.args['age'], request.args['gender'], request.args['race']
    body = request.get_json( )
    email, password, name = body['email'],body['password'],body['name']
    try:
        cnx = make_connection()
        cursor = cnx.cursor();
        #INSERT INTO cpop_auth VALUES ("uname","password",role_id,"token");
        token = hashlib.sha1('{password}'.encode('utf-8')).hexdigest()
        #hashlib.md5(b'{password}').hexdigest();
        query = f''' INSERT INTO cpop_auth VALUES ("{email}","{password}",1,"{token}")''';
        cursor.execute(query)
        cursor = cnx.cursor();
        #insert into cpop_doctors (doc_id,name, email) values (2,"hannibal",'hbgKcKK@hospital.com');
        query = f'''INSERT INTO cpop_doctors VALUES (0,'{name}','{email}');''';
        cursor.execute(query)
        query = f'''select doc_id from cpop_doctors where email="{email}"'''
        cursor.execute(query)
        results_list = []
        for result in cursor:
            results_list.append(result)
        cursor.close()
        cnx.commit()
        cursor.close()
        return json.dumps(results_list)
    except  Exception as e: 
        print(e);
        return "check syntax"

@app.route('/patInfo', methods= ['POST'])
def patInfo():
    #Id, name, age, gender, race = request.args['id'], request.args['name'], request.args['age'], request.args['gender'], request.args['race']
    body = request.get_json( )
    pat_id , education , cigarettes , alcohol_id , asthma , diabetes, allergic_rhinitis , aspirin_sensitivity , depression= body['pat_id'],body['education'],body['cigarettes'],body['alcohol_id'],body['asthma'],body['diabetes'],body['allergic_rhinitis'],body['aspirin_sensitivity'],body['depression']

    try:
        cnx = make_connection()
        cursor = cnx.cursor();
        #insert into cpop_pat_info values(1, "Bachelor's Degree", 4, 2, 1, 0, 1, 0, 1);
        query = f''' INSERT INTO cpop_pat_info VALUES ({pat_id}, "{education}",{cigarettes},{alcohol_id},{asthma},{diabetes},{allergic_rhinitis},{aspirin_sensitivity},{depression})''';
        print(query)
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        return "{msg:entered successfully}"
    except  Exception as e: 
        print(e);
        return "check syntax"

@app.route('/postSurvey', methods= ['POST'])
def postSurvey():
    #Id, name, age, gender, race = request.args['id'], request.args['name'], request.args['age'], request.args['gender'], request.args['race']
    body = request.get_json( )
    response_id , pat_id , study_id , response_date , response_code , Need_to_blow_your_nose , Nasal_Blockage , Sneezing , Runny_Nose , Cough , Post_nasal_discharge , Thick_nasal_discharge , Ear_fullness , Dizziness , Ear_pain , Facial_pain_pressure , Decreased_Sense_of_Smell_Taste , Difficulty_falling_asleep , Wake_up_at_night , Lack_of_a_good_nights_sleep , Wake_up_tired , Fatigue , Reduced_Productivity , Reduced_Concentration , Frustrated_restless_irritable , Sad , Embarassed  = body['response_id'],body['pat_id'],body['study_id'],body['response_date'],body['response_code'],body['Need_to_blow_your_nose'],body['Nasal_Blockage'],body['Sneezing'],body['Runny_Nose'],body['Cough'],body['Post_nasal_discharge'],body['Thick_nasal_discharge'],body['Ear_fullness'],body['Dizziness'],body['Ear_pain'],body['Facial_pain_pressure'],body['Decreased_Sense_of_Smell_Taste'],body['Difficulty_falling_asleep'],body['Wake_up_at_night'],body['Lack_of_a_good_nights_sleep'],body['Wake_up_tired'],body['Fatigue'],body['Reduced_Productivity'],body['Reduced_Concentration'],body['Frustrated_restless_irritable'],body['Sad'],body['Embarassed']
    try:
        cnx = make_connection()
        cursor = cnx.cursor();
        query = f''' INSERT INTO cpop_survey_responses VALUES ({response_id},{pat_id},{study_id},"{response_date}","{response_code}",{Need_to_blow_your_nose},{Nasal_Blockage},{Sneezing},{Runny_Nose},{Cough},{Post_nasal_discharge},{Thick_nasal_discharge},{Ear_fullness},{Dizziness},{Ear_pain},{Facial_pain_pressure},{Decreased_Sense_of_Smell_Taste},{Difficulty_falling_asleep},{Wake_up_at_night},{Lack_of_a_good_nights_sleep},{Wake_up_tired},{Fatigue},{Reduced_Productivity},{Reduced_Concentration},{Frustrated_restless_irritable},{Sad},{Embarassed} )''';
        print(query)
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        return "{msg:entered successfully}"
    except  Exception as e: 
        print(e);
        return "check syntax"



@app.route('/createStudy', methods= ['POST'])
def createStudy():
        #Id, name, age, gender, race = request.args['id'], request.args['name'], request.args['age'], request.args['gender'], request.args['race']
        body = request.get_json()
        study_id , doc_id , study_name , inclusion , exclusion = body['study_id'],body['doc_id'],body['study_name'],body['inclusion'],body['exclusion']
        try:
                cnx = make_connection()
                cursor = cnx.cursor();
                #insert into cpop_pat_info values(1, "Bachelor's Degree", 4, 2, 1, 0, 1, 0, 1);
                query = f''' INSERT INTO cpop_studies VALUES ({study_id}, {doc_id},\"{study_name}\",\"{inclusion}\",\"{exclusion}\")''';
                print(query)
                cursor.execute(query)
                cnx.commit()
                cursor.close()
                return "{msg:entered successfully}"
        except  Exception as e:
                return e

@app.route('/createOperation', methods= ['POST'])
def createOperation():
        body = request.get_json()
        doc_id , pat_id , operation_date = body['doc_id'],body['pat_id'],body['operation_date']
        op = datetime.strptime(operation_date, '%Y-%m-%d %H:%M:%S')
        pre_op = op + timedelta(days=-1)
        post_op = op + timedelta(days=1)
        op_3= op + timedelta(days=90)
        op_6= op + timedelta(days=180)
        print(pre_op)
        print(post_op)
        print(op_3)
        print(op_6)
        try:
                cnx = make_connection()
                cursor = cnx.cursor();
                query = f''' INSERT INTO cpop_operations VALUES (0,{doc_id},{pat_id},{operation_date})''';
                print(query)
                cursor.execute(query)
                query = f'''select operation_id from cpop_doctors where doc_id="{doc_id}" and pat_id={pat_id} and operation_date={operation_date}'''
                        cursor.execute(query)
                        results_list = []
                        for result in cursor:
                            results_list.append(result)
                cnx.commit()
                cursor.close()
                return results_list 
        except  Exception as e:
                return e




def genemails():
    cnx = make_connection()
    cursor = cnx.cursor()
    def random_char(char_num):
        return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))
    for i in range(2):
        email = random_char(7)+"@hospital.com"
        password_length = random.randint(6,12)
        password = secrets.token_urlsafe(password_length)
        roleid = 1
        token = hashlib.sha1(password.encode('utf-8')).hexdigest()
        print(password, token)
        query = f'''INSERT INTO cpop_auth VALUES ("{email}","{password}","{roleid}","{token}");''';
        cursor.execute(query)
        cnx.commit()
    cursor.close()
    return


app.run(host="0.0.0.0",port=8080)
#app.run(host="localhost", port=8000, debug=True)

