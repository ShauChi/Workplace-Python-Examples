#Print out the user's bio statment based upon userName with appsecret_proof
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
#print(people)

for person in people:
    try:
        users.index(person['userName'])
        uri = "https://graph.workplace.com/%s?fields=about&access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (person['id'], TOKEN, appsecret_proof, t)
        r = requests.get(uri, headers=headers)
        answer = r.json()
        try:
            bio = '"'+answer['about']+'"'
        except:
            bio = '""'
        print "%s, %s" % (person['userName'],bio)
    except ValueError:
        x = 0
        #print(person['userName'])
