from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
from boto import mturk
from heapq import heappush, heappop

import boto3
import csv

AWS_ACCESS_KEY_ID = "AKIAJ4QIR3P6VESAPY4A"
AWS_SECRET_ACCESS_KEY = "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"

HOST = 'mechanicalturk.amazonaws.com'

connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID, 
	aws_secret_access_key=AWS_SECRET_ACCESS_KEY,host=HOST)

url = "https://powerful-inlet-12898.herokuapp.com/"
title = 'Arrange Adjectives on a Scale'
description = 'Arrange nodes representing adjectives on a scale according to relative intensity'
frame_height = 500
amount = .35

with open('mturk_responses.csv','w') as f:
	writer = csv.writer(f)
	writer.writerow(['WorkerId','Approve? (A/R)','Feedback?','Grant Bonus? (amount,reason)','attribute','answers'])
	for hit in connection.get_all_hits():

		if 'Arrange Adjectives' in hit.Title:
			assignments = connection.get_assignments(hit.HITId)
			for ass in assignments:
				li = []
				print ass.WorkerId

				#approve_assignment(ass.AssignmentId,feedback="")
				#reject_assignment(ass.AssignmentId,feedback="")
				#grant_bonus(ass.WorkerId,ass.AssignmentId,get_price_as_price(0.5),reason='')



				for ans in ass.answers:
					for a in ans[1:]:
						heappush(li,(int(a.fields[0]),a.qid.split('%')[0] +" : "+ a.fields[0]))

				writer.writerow([ass.WorkerId,"","","",ans[0].fields[0]] + [heappop(li)[1] for i in range(len(li))])


'''
with open('final_stims.csv','rb') as f:
	reader = csv.reader(f)
	
	for row in reader:
		attr = row[1].split('_')[0] + '_' + row[1].split('_')[1]
		questionform = mturk.question.ExternalQuestion(url + '?attr=' + attr,frame_height)


		create_hit_result = connection.create_hit(
			title = title,
			description = description,
			question = questionform,
			max_assignments = 3,
			keywords = "adjective,language,english,slider,task,repeat,linguistics,word",
			reward = mturk.price.Price(amount= amount),
		)
'''
