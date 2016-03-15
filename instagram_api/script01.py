# -----------------------------------------------
# EDIT INFO BELOW
# -----------------------------------------------

# FILL IN YOUR COMPANIES EXACT NAMES

brands = ['Groceries Apparel', 'James Perse', 'Acne Studios', 'APC', 'Death To Tennis', 
	'Elizabeth Suzann', 'Orley', 'Wool & Prince']

# FIND YOUR INSTAGRAM ACCOUNT INFO (CLIENT_ID, etc)
# https://www.instagram.com/developer/

# RUN get_access_token.py
# ENTER ACCT INFO TO GET YOUR ACCESS TOKEN
# ENTER YOUR ACCESS BELOW AS A STRING

ACCESS_TOKEN = ''

# -----------------------------------------------
# -----------------------------------------------

# ----------- SCRIPT BELOW SHOULD JUST RUN -----------
import requests
import numpy as np
import pandas as pd

baseUrl = 'https://api.instagram.com/v1/'

# ---------- Get array of brand IDs
allIds = []
allBrandDict = []

for brand in brands:
	r = requests.get(baseUrl + 'users/search?access_token=' + ACCESS_TOKEN + '&q=' + brand)
	brandData = r.json()
	allIds.append(brandData['data'][0]['id'])
	brand = {}
	brand['name'] = brandData['data'][0]['username']
	brand['id'] = brandData['data'][0]['id']
	#brand[brandData['data'][0]['username']] = brandData['data'][0]['id'] 
	
	# number of followers
	numberFollowersReq = requests.get(baseUrl + 'users/' + brandData['data'][0]['id'] + '?access_token=' + ACCESS_TOKEN)
	numberFollowers = numberFollowersReq.json()
	brand['followers'] = numberFollowers['data']['counts']['followed_by']

	# picture stuff
	recentMediaReq = requests.get(baseUrl + 'users/' + brandData['data'][0]['id'] + '/media/recent?access_token=' + ACCESS_TOKEN)
	recentMedia = recentMediaReq.json()

	numberPhotos = 0
	totalLikes = 0
	totalComments = 0
	indivPhotoData = []
	photoNumber = 0
	for r in recentMedia['data']:
		totalComments += r['comments']['count']
		totalLikes += r['likes']['count']
		tempPhotoData = {}
		tempPhotoData['number'] = photoNumber + 1
		tempPhotoData['likes'] = r['likes']['count']
		tempPhotoData['comments'] = r['likes']['count']
		indivPhotoData.append(tempPhotoData)

	brand['totalLikes'] = totalLikes
	brand['totalComments'] = totalComments
	brand['avgLikes'] = totalLikes/len(indivPhotoData)
	brand['avgComments'] = totalComments/len(indivPhotoData)
	# print 'number of photos analyzed: ' + str(len(indivPhotoData)): THIS EQUALS 20
	#brand['indPhotoData'] = indivPhotoData

	allBrandDict.append(brand)

print allIds
print allBrandDict

# Export to csv
df = pd.DataFrame(allBrandDict)
print df

# Rearrange columns
cols = list(df)
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('name')))
# use ix to reorder
df = df.ix[:, cols]
print df

# Ouput to a csv
df.to_csv('insta_data.csv')
