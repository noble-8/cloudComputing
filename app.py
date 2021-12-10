import pymysql
import logging
import traceback 
from os import environ
endpoint = 'wed8.c34yxqfbf9wx.us-east-2.rds.amazonaws.com'
port = '3306'
dbuser = 'admin'
password = 'rootroot'
database = 'rds'

#query = """insert into cpop_users values(0,"Bhadft", 23, "M", "Asian");"""
query = """select * from cpop_users"""

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def make_connection():
    return pymysql.connect(
        host=endpoint,
        user=dbuser,
        port=int(port),
        passwd=password,
        db=database)


def log_err(errmsg):
    logger.error(errmsg)
    return {"body": errmsg, "headers": {}, "statusCode": 400,
            "isBase64Encoded": "false"}


logger.info("start complete.")


def lambda_handler(event, context):

    try:
        cnx = make_connection()
        cursor = cnx.cursor()

        try:
            cursor.execute(query)
        except:
            return log_err("ERROR: Cannot execute cursor.\n{}".format(traceback.format_exc()))
        try:
            results_list = []
            for result in cursor:
                results_list.append(result)
                print(results_list)
            cursor.close()

        except:
            return log_err("ERROR: Cannot retrieve query data.\n{}".format(traceback.format_exc()))

        return {
               "body": str(results_list), 
               "headers": {}, "statusCode": 200,
               "isBase64Encoded": "false"
                }

    except:
        return log_err("ERROR: Cannot connect to database from handler.\n{}".format(traceback.format_exc()))

    finally:
        try:
            cnx.close()
        except:
            pass


lambda_handler('', '')


