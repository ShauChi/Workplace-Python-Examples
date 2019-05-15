#Print out the user's bio statment based upon userName
#This script requires the access token to be placed in a file named accessToken
#The script also requires a list Workplace user names in a file named userNames
#The format of userNames is to have 1 user name per line with no empty lines
import requests, json

#Get the access token from a file named accessToken
f = open("accessToken", "r")
TOKEN = f.read()
TOKEN = TOKEN.rstrip("\r\n")
f.close()
#Generate the Authentication header
AUTH = "Bearer %s" % TOKEN
headers = {'Authorization': AUTH, 'Content-Type': 'application/json'}

#Get the list of userNames
with open("userNames", "r") as f:
    users = []
    for line in f:
        users.append(line.rstrip("\r\n"))
#print(users)

getUsers = "https://www.workplace.com/scim/v1/Users/"
r = requests.get(getUsers, headers=headers)
answer = r.json()
people = answer['Resources']
#print(people)

for person in people:
    try:
        users.index(person['userName'])
        uri = "https://graph.workplace.com/%s?fields=about" % person['id']
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
