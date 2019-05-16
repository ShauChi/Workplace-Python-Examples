#Demonstrates how to follow pagination to scroll through all group results with appsecret_proof
#Use this version if Require App Secret Proof has been enabled
#This script requires the access token to be placed in a file named accessToken
#This script requires the app secret to be placed in a file named appSecret
#Adjust the value of lim to see how return results are grouped
import requests, json, hmac, hashlib, time

lim = 4

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

getGroups = "https://graph.workplace.com/community/groups?limit=%s&access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (lim, TOKEN, appsecret_proof, t)
r = requests.get(getGroups, headers=headers)
response = r.json()
groups = response['data']
print(groups)
paging = response['paging']
next = True
while next:
    try:
        url = paging['next']
        url = url+"&appsecret_proof=%s&appsecret_time=%s" % (appsecret_proof, t)
        r = requests.get(url, headers=headers)
        answer = r.json()
#        print(url)
        print(answer['data'])
        paging = answer['paging']
    except KeyError:
        next = False
