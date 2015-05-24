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
		org_name = row[0]
		town_name = row[1]
		county_name = 'NA'
		tier_name = row[2]
		sub_tier_name = row[3]

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
		town.organisation.append(org)

		# check whether sub_tier exists in subtiers table
		sub_tier = SubTier.query.filter_by(name = sub_tier_name).first()
		if not sub_tier:
			# if not, create SubTier object 
			sub_tier = SubTier(sub_tier_name)
			tier = Tier,query.filter_by(name = tier_name).first()
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

		if count%10 == 0:
			# db.session.flush()
			break
		count += 1
	db.session.commit()

	companies = Organisation.query.all()
	for com in companies:
		print "Com: {} Town: {} County: {} Tier: {} SubTier: {} \n".format(
			com.name, com.town, com.town.county, com.subtier.tier, com.subtier)



		

