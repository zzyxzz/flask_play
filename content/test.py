import csv

"""
test on the csv file to get right format which has no carriage return and zip
the Tier with corresponding sub Tier. 
"""
with open('data.csv', 'r') as data:
	reader = csv.reader(data)
	count = 1
	for line in reader:
		if line[0]:
			print '=========================='
			print line[0].rstrip() 
			print line[1].rstrip() 
			tiers =  line[2].rstrip().split('\n')
			subs  = line[3].rstrip().split('\n')
			tiers = zip(tiers,subs)
			print tiers
			print '==========================\n'
		if count % 20 == 0:
			break
		count += 1
