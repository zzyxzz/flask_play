from app import Organisation, Town, County, Tier, SubTier
from app import db
import csv

# create sqlite db

db.create_all()

# add records

with open('./content/data.csv', 'r') as data:
	reader = csv.reader(data)
	count = 1
	for row in reader:
		if not row[0]:
			continue
		org_name = row[0].rstrip()
		town_name = row[1].rstrip()
		county_name = 'NA'
		tier_names = row[2].rstrip().split('\n')
		sub_tier_names = row[3].rstrip().split('\n')
		tiers = zip(tier_names, sub_tier_names)

		org = Organisation(org_name)
		db.session.add(org)

		# check whether whether town exists in towns table
		town = Town.query.filter_by(name = town_name).first()
		if not town:
			# if not, create Town object
			town = Town(town_name)
			# check whether county exists in counties table
			county = County.query.filter_by(name = county_name).first()
			if not county:
				# if not, create County object
				county = County(county_name)
				# add county to seesion
				db.session.add(county)
			# link town and county
			county.towns.append(town)
			# add town to session
			db.session.add(town)
		# link town and organisation
		town.organisations.append(org)

		for tier_name, sub_tier_name in tiers:
			# check whether sub_tier exists in subtiers table
			sub_tier = SubTier.query.filter_by(name = sub_tier_name).first()
			if not sub_tier:
				# if not, create SubTier object 
				sub_tier = SubTier(sub_tier_name)
				tier = Tier.query.filter_by(name = tier_name).first()
				if not tier:
					# if not, create Tier object
					tier = Tier(tier_name)
					# add tier to session
					db.session.add(tier)
				# link tier and sub_tier
				tier.sub_tiers.append(sub_tier)
				# add sub_tier to session
				db.session.add(sub_tier)
			# link sub_tier and organisation
			sub_tier.organisations.append(org)
			org.sub_tiers.append(sub_tier)

		if count%10 == 0:
			# db.session.flush()
			break
		count += 1
	db.session.commit()

	companies = Organisation.query.all()
	for com in companies:
		print "Com: {} Town: {} County: {} Tier: {} SubTier: {} \n".format(
			com.name, com.town, com.town.county, [s.tier for s in com.sub_tiers], com.sub_tiers)



		

