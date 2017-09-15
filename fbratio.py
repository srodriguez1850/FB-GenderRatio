#!/usr/bin/env python

"""
fbratio.py
Python script to determine the binary gender ratio of a Facebook event 
using calls to the Genderize.io API.
usage: ratio.py [-h] [-hc] [-i token eventid] [-g] [-n]

optional arguments:
  -h, --help        show this help message and exit
  -hc               runs the hardcoded token and event in the header of
                    ratio.py
  -i token eventid  runs the inline arguments [token] [eventid]
  -g                prints the names of all guests
  -n                no API call to Genderize.io (if you only want to see event
                    information/guest list)
"""

import urllib3
import facebook
import requests
import json
import argparse

# Hardcoded information to use with -hc flag
# # # # # EDIT VALUES TO USE -hc FLAG # # # # #
HC_ACCESS_TOKEN=''
HC_EVENT_ID=''
# # # # # EDIT VALUES TO USE -hc FLAG # # # # #

males = 0
females = 0
nullg = 0

mprob = 0
fprob = 0
prob = 0

gapi_error = None

def get_ratio(token, eventid, args):
	"""
	get_ratio uses the token and eventid to call on Facebook's Graph API,
	retrieves the names of all guests, and calls on the Genderize.io API
	multiple times to determine the gender of each guest.

	Note:
		Genderize.io takes a maximum of 1000 requests per day per IP.

	Args:
		token (str): The User Access Token generated from Facebook
		eventid (str): The n digit identifier for a Facebook Event
		(can be retrieved via the URL)
		args (parser.arguments): The arguments passed via the command line

	Returns:
		Nothing
	"""

	a_fn = []
	i_fn = []

	attn = []
	intd = []
	allg = []

	graph = facebook.GraphAPI(access_token=token, version='2.10')
	
	event = graph.request('/'+eventid+'/')
	print ''
	print 'Event Name: ' + event['name']
	print 'Start Time: ' + event['start_time']

	event = graph.request('/'+eventid+'/attending?limit=10000')
	for g in event['data']:
		a_fn.append(g['name'])

	event = graph.request('/'+eventid+'/interested?limit=10000')
	for g in event['data']:
		i_fn.append(g['name'])

	print ''
	if args.g:
		print 'Attending (' + str(len(a_fn)) + ')'
		print '---------'
		for g in a_fn:
			print g

		print ''

		print 'Interested (' + str(len(i_fn)) + ')'
		print '----------'
		for g in i_fn:
			print g
		print ''

	for g in a_fn:
		attn.append(g.split(' ', 1)[0])

	for g in i_fn:
		intd.append(g.split(' ', 1)[0])

	allg = attn + intd
	allg_c = len(allg)

	if args.n:
		return

	count = allg_c
	while count != 0:
		if count > 9:
			nt = []
			for i in xrange(10):
				nt.append(allg.pop())
			count -= 10
			parse_genders(get_genders(nt))

		else:
			nt = []
			for i in xrange(count):
				nt.append(allg.pop())
			count -= count
			parse_genders(get_genders(nt))

	global mprob, fprob, prob
	mprob = mprob/males if males > 0 else 0
	fprob = fprob/females if females > 0 else 0
	prob = prob/allg_c if males > 0 and females > 0 else 0

	if gapi_error != None:
		print '**Genderize.io API Error: ' + str(gapi_error)
		print ''

	print 'Total Guests: ' + str(allg_c)
	print 'Males: ' + str(males)
	print 'Females: ' + str(females)
	print 'Uncertain (by name): ' + str(nullg)

	print ''
	print 'Male Reliability : ' + str(mprob)
	print 'Female Reliability : ' + str(fprob)
	print 'Total Reliability : ' + str(prob)

	print ''
	print 'M/F Ratio: ' + str(males/females) if females > 0 else 0
	print 'F/M Ratio: ' + str(females/males) if males > 0 else 0

def get_genders(names):
	"""
	get_genders takes an array of first names and makes calls to the Genderize.io API
	to determine if the name is male or female.

	Note:
		A single API call can have up to 10 names. The amount of API calls are optimized
		by get_ratio.

	Args:
		names(str[]): Array of first names to be gendered

	Returns:
		Dictionary[Gender, Probability of Gender, API Name Count]
	"""

	url = ''
	cnt = 0
	if not isinstance(names,list):
		names = [names,]
	
	for name in names:
		if url == '':
			url = 'name[0]=' + name
		else:
			cnt += 1
			url = url + '&name[' + str(cnt) + ']=' + name
		

	req = requests.get('https://api.genderize.io?' + url)
	results = json.loads(req.text)
	
	if 'error' in results:
		global gapi_error
		gapi_error = results['error']
		return None
	
	retrn = []
	for result in results:
		if result['gender'] is not None:
			retrn.append((result['gender'], result['probability'], result['count']))
		else:
			retrn.append((u'None',u'0.0',0.0))
	return retrn

def parse_genders(results):
	"""
	parse_genders modifies global counts and probabilities for final statistics.

	Args:
		results(dict): Dictionary of results of a single API call

	Returns:
		Nothing, but global counts and probabilites are modified
	"""
	if results == None:
		return

	global males, females, nullg, mprob, fprob, prob
	for r in results:
		if r[0] == 'male':
			males += 1
			mprob += float(r[1])
		elif r[0] == 'female':
			females += 1
			fprob += float(r[1])
		else:
			nullg += 1
		prob += float(r[1])


if __name__ == '__main__':
	"""
	Program entry point (__main__)
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument('-hc', help='runs the hardcoded token and event in the header of ratio.py', action='store_true')
	parser.add_argument('-i', help='runs the inline arguments [token] [eventid]', action='store', nargs=2, type=str, dest='creds', metavar=('token', 'eventid'))
	parser.add_argument('-g', help='prints the names of all guests', action='store_true')
	parser.add_argument('-n', help='no API call to Genderize.io (if you only want to see event information/guest list)', action='store_true')
	args = parser.parse_args()

	iflag = False
	if args.creds != None:
		if args.creds[0] != None and args.creds[1] != None:
			iflag = True

	if args.hc and iflag:
		print 'Option conflict; cannot run hardcoded and inline simultaneously'
	elif args.hc:
		print '\tRunning hardcoded values'
		print 'Hardcoded User Access Token: ' + str(HC_ACCESS_TOKEN)
		print 'Hardcoded Event ID: ' + str(HC_EVENT_ID)
		get_ratio(HC_ACCESS_TOKEN, HC_EVENT_ID, args)
	elif iflag:
		print '\tRunning command line arguments'
		get_ratio(args.creds[0], args.creds[1], args)
	else:
		token = str(raw_input('User Access Token: '))
		eventid = str(raw_input('Facebook Event ID: '))
		get_ratio(token, eventid, args)