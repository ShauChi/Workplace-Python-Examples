#Demonstrates pagination of users through the SCIM API appsecret_proof
#Use this version if Require App Secret Proof has been enabled
#This script requires the access token to be placed in a file named accessToken
#This script requires the app secret to be placed in a file named appSecret
#unlike the Graph API, SCIM uses count and startIndex
import requests, json, hmac, hashlib, time

count = 2
startIndex = 1

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

getUsers = "https://www.workplace.com/scim/v1/Users?count=%s&access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (count, TOKEN, appsecret_proof, t)
r = requests.get(getUsers, headers=headers)
answer = r.json()
total = answer['totalResults']
people = answer['Resources']
for person in people:
    print(person['userName'])
while startIndex < total:
    startIndex += count
    getUsers = "https://www.workplace.com/scim/v1/Users?count=%s&startIndex=%s&access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (count, startIndex, TOKEN, appsecret_proof, t)
    r = requests.get(getUsers, headers=headers)
    answer = r.json()
    people = answer['Resources']
    for person in people:
        print(person['userName'])
