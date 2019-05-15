#Reactivate a user if they have been deactivated based upon their userName
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
        uri = "https://www.workplace.com/scim/v1/Users/%s" % person['id']
        r = requests.get(uri, headers=headers)
        state = r.json()
        if state['active'] == False:
            state['active'] = True
            r = requests.put(uri, data=json.dumps(state), headers=headers)
            print(r.json())
        else:
            print "User %s was already active" % person['userName']
    except ValueError:
        x = 0
