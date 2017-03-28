from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
from boto.mturk import layoutparam
from boto import mturk

AWS_ACCESS_KEY_ID = "AKIAJ4QIR3P6VESAPY4A"
AWS_SECRET_ACCESS_KEY = "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"
layout_id = "3RYJVOUNO72JC0JT8VHB04IHOBY8PI"

HOST = 'mechanicalturk.sandbox.amazonaws.com'

connection = MTurkConnection(aws_access_key_id=AWS_ACCESS_KEY_ID, 
	aws_secret_access_key=AWS_SECRET_ACCESS_KEY,host=HOST)

url = "https://powerful-inlet-12898.herokuapp.com/"
title = 'Image Evaluation'
description = 'check this out'
frame_height = 500
amount = .05

urls = ["https://upload.wikimedia.org/wikipedia/commons/f/ff/Solid_blue.svg", "https://commons.wikimedia.org/wiki/File:Red.svg", "https://commons.wikimedia.org/wiki/File:Solid_orange.svg", "https://commons.wikimedia.org/wiki/File:Solid_purple.svg"]

#params = [layoutparam.LayoutParameter('image_url',"https://images-na.ssl-images-amazon.com/images/G/01/webservices/mechanical-turk/logoAI3.gif")]
params = []

questionform = mturk.question.ExternalQuestion(url,frame_height)

for url in urls:
	create_hit_result = connection.create_hit(
		hit_layout = layout_id,
		title = title,
		description = description,
		#question = questionform,
		reward = mturk.price.Price(amount= amount),
		layout_params = layoutparam.LayoutParameters([layoutparam.LayoutParameter("image_url",url)])
	)

