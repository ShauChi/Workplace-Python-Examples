#Print out the user's bio statment based upon userName with appsecret_proof
#Use this version if Require App Secret Proof has been enabled
#This script requires the access token to be placed in a file named accessToken
#This script requires the app secret to be placed in a file named appSecret
#The script also requires a list Workplace user names in a file named userNames.csv
#The format of userNames.csv is the people export from Workplace
import requests, json, hmac, hashlib, time, ast

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
with open("userNames.csv", "r") as f:
    f.readline()
    users = []
    for line in f:
        mylist = line.split(',')
        users.append(mylist[1])
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

xlink = {}
for person in people:
    try:
        xlink[person['userName']] = person['id']
    except:
        x = 0

for user in users:
    try:
        #Insert 18 second delay between calls to avoid API call failure due to throttling
        #time.sleep(18)
        #Get the app secret time and generate the app secret proof
        t = str(int(time.time()))
        blurb = TOKEN+'|'+t
        blurb = bytes(blurb)
        appsecret_proof = hmac.new(APPSECRET, blurb, hashlib.sha256)
        appsecret_proof = appsecret_proof.hexdigest()
        uri = "https://graph.workplace.com/%s?fields=about&access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (xlink[user], TOKEN, appsecret_proof, t)
        r = requests.get(uri, headers=headers)
        blob = r.json()
        try:
            bio = '"'+blob['about']+'"'
        except:
            bio = '""'
        print "%s, %s" % (user,bio)
        usage = r.headers['x-app-usage']
        usage = ast.literal_eval(usage)
        if usage['call_count'] > 90:
            time.sleep(60)
    except:
        x = 0
