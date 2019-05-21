#Reactivate a user if they have been deactivated based upon their userName with appsecret_proof
#Use this version if Require App Secret Proof has been enabled
#This script requires the access token to be placed in a file named accessToken
#This script requires the app secret to be placed in a file named appSecret
#The script also requires a list Workplace user names in a file named userNames
#The format of userNames is to have 1 user name per line with no empty lines
import requests, json, hmac, hashlib, time

#Get the access token from a file named accessToken
f = open("accessToken", "r")
TOKEN = f.read()
TOKEN = TOKEN.rstrip("\r\n")
f.close()
#Get the app secret from a file named appSecret
f = open("appSecret", "r")
APPSECRET = f.read()
APPSECRET= APPSECRET.rstrip("\r\n")
f.close()
#Generate the content header
headers = {'Content-Type': 'application/json'}
#Get the app secret time and generate the app secret proof
t = str(int(time.time()))
blurb = TOKEN+'|'+t
blurb = bytes(blurb)
appsecret_proof = hmac.new(APPSECRET, blurb, hashlib.sha256)
appsecret_proof = appsecret_proof.hexdigest()

#Get the list of userNames
with open("userNames", "r") as f:
    users = []
    for line in f:
        users.append(line.rstrip("\r\n"))
#print(users)

getUsers = "https://www.workplace.com/scim/v1/Users?access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (TOKEN, appsecret_proof, t)
r = requests.get(getUsers, headers=headers)
answer = r.json()
people = answer['Resources']
try:
    itemsPerPage = answer['itemsPerPage']
    total = answer['totalResults']
    startIndex = answer['startIndex']
    startIndex += itemsPerPage
    while startIndex < total:
        startIndex += itemsPerPage
        getUsers = "https://www.workplace.com/scim/v1/Users?count=%s&startIndex=%s&access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (itemsPerPage, startIndex, TOKEN, appsecret_proof, t)
        r = requests.get(getUsers, headers=headers)
        answer = r.json()
        try:
            people = people + answer['Resources']
        except:
            x = 0
except:
    x = 0

link = {}
for person in people:
    try:
        xlink[person['userName']] = person['id']
    except:
        x = 0

for user in users:
    try:
        uri = "https://www.workplace.com/scim/v1/Users/%s?access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (xlink[user], TOKEN, appsecret_proof, t)
        r = requests.get(uri, headers=headers)
        state = r.json()
        if state['active'] == False:
            state['active'] = True
            r = requests.put(uri, data=json.dumps(state), headers=headers)
            print(r.json())
        else:
            print "User %s was already active" % user
    except ValueError:
        x = 0
