#This script demonstrates getting the /seen edge from posts when the App Secret is required
#This script requires the access token to be placed in a file named accessToken
#This script requires the app secret to be placed in a file named appSecret
import requests, json, hmac, hashlib, time

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
lim = 5000

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
            getSeen = "https://graph.workplace.com/%s/seen?limit=%d&access_token=%s&appsecret_proof=%s&appsecret_time=%s" % (blob['id'], lim, TOKEN, appsecret_proof, t)
            r = requests.get(getSeen, headers=headers)
            response = r.json()
            if response['data'] != []:
#                print(getSeen)
                print("Post %s, %s was seen by\n%s" % (blob['id'], blob['message'], response['data']))
                paging = response['paging']
                next = True
                while next:
                    try:
                        url = paging['next']
                        url = url+"&appsecret_proof=%s&appsecret_time=%s" % (appsecret_proof, t)
                        r = requests.get(url, headers=headers)
                        answer = r.json()
#                        print(url)
                        print("Post %s, %s was seen by\n%s" % (blob['id'], blob['message'], response['data']))
                        paging = answer['paging']
                    except KeyError:
                        next = False
