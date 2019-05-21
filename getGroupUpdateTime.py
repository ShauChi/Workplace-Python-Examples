#This script gets the last update time for every group when the App Secret is required
#This script requires the access token to be placed in a file named accessToken
#This script requires the app secret to be placed in a file named appSecret
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

headers = {'Content-Type': 'application/json'}

getGroups = "https://graph.workplace.com/community/groups?access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (TOKEN, appsecret_proof, t)

r = requests.get(getGroups, headers=headers)
response = r.json()
groups = response['data']
for group in groups:
    getUpdateTime = "https://graph.workplace.com/%s?fields=name,updated_time&access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (group['id'], TOKEN, appsecret_proof, t)
    r = requests.get(getUpdateTime, headers=headers)
    response = r.json()
    print(response)
