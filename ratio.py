#!/usr/bin/env python

import urllib3, facebook, requests, json

PRINT_FULL_NAMES = True

s_token='EAACEdEose0cBADStXyAZC6MfP4wu8fn8SAZAUpGoHpuCPVlSoNwi1VW9UH0uww7H5QKS8F1rRCINN8W18dPeP6fZCrOVRwCYWl0eZB4WTTmwI5Lc8ZBe7LQ6P9Vi7EGXp0HXnRWKApxqAXcw6BhZAVXhY6EMVcr6azAJEqPdUCqZAVrh3G5DEwweGtV2lgoAJ8ZD'
event_id='424735347920363'

males = 0
females = 0
nullg = 0
prob = 0

def get_partners():

	a_fn = []
	i_fn = []

	attn = []
	intd = []
	allg = []

	graph = facebook.GraphAPI(access_token=s_token, version='2.10')
	
	event = graph.request('/'+event_id+'/attending?limit=10000')
	for g in event['data']:
		a_fn.append(g['name'])

	event = graph.request('/'+event_id+'/interested?limit=10000')
	for g in event['data']:
		i_fn.append(g['name'])

	if PRINT_FULL_NAMES:
		print 'Attending'
		print '---------'
		print 'Num. Guests: ' + str(len(a_fn))
		for g in a_fn:
			print g

		print ''

		print 'Interested'
		print '----------'
		print 'Num. Guests: ' + str(len(i_fn))
		for g in i_fn:
			print g

	for g in a_fn:
		attn.append(g.split(' ', 1)[0])
	#print attn

	for g in i_fn:
		intd.append(g.split(' ', 1)[0])
	#print intd

	allg = attn + intd
	allg_c = len(allg)

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

	global prob
	prob /= allg_c

	print ''
	print 'Leads: ' + str(males)
	print 'Follows: ' + str(females)
	print 'Uncertain (by name): ' + str(nullg)
	print 'Result Reliability : ' + str(prob)

def get_genders(names):
#Max 10 names at once
	url = ""
	cnt = 0
	if not isinstance(names,list):
		names = [names,]
	
	for name in names:
		if url == "":
			url = "name[0]=" + name
		else:
			cnt += 1
			url = url + "&name[" + str(cnt) + "]=" + name
		

	req = requests.get("https://api.genderize.io?" + url)
	results = json.loads(req.text)
	
	retrn = []
	for result in results:
		if result["gender"] is not None:
			retrn.append((result["gender"], result["probability"], result["count"]))
		else:
			retrn.append((u'None',u'0.0',0.0))
	return retrn

def parse_genders(results):
	global males, females, nullg, prob
	for r in results:
		if r[0] == 'male':
			males += 1
		elif r[0] == 'female':
			females += 1
		else:
			nullg += 1
		prob += float(r[1])


if __name__ == '__main__':
	get_partners()