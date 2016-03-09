# -----------------------------------------------
# EDIT INFO BELOW
# -----------------------------------------------

# RUN THIS IN YOUR TERMINAL
# sudo pip install python-instagram

# FILL IN YOUR COMPANIES EXACT NAMES

brands = ['Groceries Apparel', 'James Perse', 'Acne Studios', 'APC', 'Death To Tennis', 
	'Elizabeth Suzann', 'Orley', 'Wool & Prince']

# FIND IN INSTAGRAM ACCOUNT INFO
# https://www.instagram.com/developer/

CLIENT_ID = 'a2bcad5de7ab400eb16b7cc8d2ff0d24'
CLIENT_SECRET = '4a0b191e4c8a4c71be5bfa60328f4e3c'

# RUN get_access_token.py
# ENTER access token BELOW

ACCESS_TOKEN = '225686819.a2bcad5.ebe2686bcb5c48aa95097c521e307f84'

# -----------------------------------------------
# -----------------------------------------------

# ----------- SCRIPT BELOW SHOULD RUN -----------
import requests

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

# ---------- Get data for each brand

# number of followers
#numberFollowers = 'users/' + ID + '?access_token=' + ACCESS_TOKEN
