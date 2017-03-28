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

hit = connection.get_hit('3PKJ68EHDNFY265JBRQOXMEN1NCHJ9')

assignments = connection.get_assignments('30QQTY5GMK3ANXA1AH8QDBY440E7UT')

#connection.approve_rejected_assignment(assignments[0].AssignmentId,'changed to approved')

for ass in assignments:
    print ass.WorkerId
    for ans in ass.answers[0]:

        print ans.qid.split('%')[0] + ' '+ ans.fields[0]
    if hasattr(ass,'RejectionTime'):
        print ass.RejectionTime