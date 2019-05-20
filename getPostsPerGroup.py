#This script demonstrates getting the posts through the group feed when the App Secret is required
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
    getFeed = "https://graph.workplace.com/%s/feed?access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (group['id'], TOKEN, appsecret_proof, t)
    r = requests.get(getFeed, headers=headers)
    response = r.json()
    if response['data'] != []:
        for blob in response['data']:
            getPost = "https://graph.workplace.com/%s?access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (blob['id'], TOKEN, appsecret_proof, t)
            r = requests.get(getPost, headers=headers)
            response = r.json()
            getPost = "https://graph.workplace.com/%s?access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (response['id'], TOKEN, appsecret_proof, t)
            r = requests.get(getPost, headers=headers)
            response = r.json()
            print(response)
