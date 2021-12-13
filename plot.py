import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import pymysql
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

#d = {"sell": [
#           {
#               "Rate": 0.001425,
#               "Quantity": 537.27713514
#           },
#           {
#               "Rate": 0.00142853,
#               "Quantity": 6.59174681
#           }
#]}
#
#df = pd.DataFrame(d['sell'])
#print (df)
#
#plt.plot(df)
#plt.savefig("figure.png")

endpoint = 'wed8.c34yxqfbf9wx.us-east-2.rds.amazonaws.com'
port = '3306'
dbuser = 'admin'
password = 'rootroot'
database = 'rds'

def make_connection():
    return pymysql.connect(
            host=endpoint,
            user=dbuser,
            port=int(port),
            passwd=password,
            db=database)


def plotNormal():
	cnx = make_connection()
	cursor = cnx.cursor()
	myobj = {"study_id": 3}
	#print(json.dumps(myobj))
	url = 'http://loadbalancermkii-139261831.us-east-2.elb.amazonaws.com:8080/list'
	x = requests.post(url, data = json.dumps(myobj),headers = {"Content-Type":"application/json"})
	#print(x.json())
	pat_ids = x.json()
	pat_ids = ','.join(map(str, pat_ids))
	query = f'''SELECT
(
Need_to_blow_your_nose
+Nasal_Blockage
+Sneezing
+Runny_Nose
+Cough
+Post_nasal_discharge
+Thick_nasal_discharge
+Ear_fullness
+Dizziness
+Ear_pain
+Facial_pain_pressure
+Decreased_Sense_of_Smell_Taste
+Difficulty_falling_asleep
+Wake_up_at_night
+Lack_of_a_good_nights_sleep
+Wake_up_tired
+Fatigue
+Reduced_Productivity
+Reduced_Concentration
+Frustrated_restless_irritable
+Sad
+Embarassed
) as snot22_score
FROM
cpop_survey_responses
where
pat_id in ({pat_ids})'''

#	print(query)	

	cursor.execute(query)
	scores = []
	for result in cursor:
		scores.append(result[0])

	
	cursor.close()

	mu = np.mean(scores)
	sigma = np.std(scores)
	print(mu, sigma)
	# define the normal distribution and PDF
	dist = stats.norm(loc=mu, scale=sigma)
	x = np.linspace(dist.ppf(.001), dist.ppf(.999))
	y = dist.pdf(x)

	# calculate PPFs
	#ppfs = {}
	doc_val = 65
	perc = stats.percentileofscore(scores, doc_val, kind='weak')/100
	p = dist.ppf(perc)


# plot results
	fig, ax = plt.subplots(figsize=(11, 4))
	ax.plot(x, y, color='k')
# for i, ppf in enumerate(ppfs):
#     ax.axvline(ppfs[ppf], color=f'C{i}', label=f'{ppf:.0f}th: {ppfs[ppf]:.1f}')
	ax.axvline(p, color=f'C0', label=f'{perc*100:.0f}th percentile: {doc_val:.1f}')
	ax.axvline(mu, color=f'C2', label=f'mean: {mu:.1f}')
	ax.legend()
	plt.xlabel('SNOT-22 Scores', fontsize = 15)
	plt.show()
	plt.savefig('normal.png')
# print(mu, sigma)

plotNormal()
