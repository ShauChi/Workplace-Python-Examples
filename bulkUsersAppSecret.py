#Get all users with appsecret_proof
#Use this version if Require App Secret Proof has been enabled
#This script requires the access token to be placed in a file named accessToken
#This script requires the app secret to be placed in a file named appSecret
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

print("inactive people")
for person in people:
    #Get the app secret time and generate the app secret proof
    t = str(int(time.time()))
    blurb = TOKEN+'|'+t
    blurb = bytes(blurb)
    appsecret_proof = hmac.new(APPSECRET, blurb, hashlib.sha256)
    appsecret_proof = appsecret_proof.hexdigest()
    member = "https://graph.workplace.com/%s/feed?access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (person['id'], TOKEN, appsecret_proof, t)
    r = requests.get(member, headers=headers)
    answer = r.json()
    if answer['data'] == []:
        print("%s, %s") % (person['userName'], person['id'])
    usage = r.headers['x-app-usage']
    usage = ast.literal_eval(usage)
    if usage['call_count'] > 90:
        time.sleep(60)
