#Create email-less users from a CSV file
#This script requires the access token to be placed in a file named accessToken
#The script also requires a list Workplace user names in a file named userNames.csv
#The format of users.csv is to have 1 user name per line with no empty lines
import requests, json, ast

#Get the access token from a file named accessToken
f = open("accessToken", "r")
TOKEN = f.read()
TOKEN = TOKEN.rstrip("\r\n")
f.close()
#Generate the Authentication header
AUTH = "Bearer %s" % TOKEN
headers = {'Authorization': AUTH, 'Content-Type': 'application/json'}

#Get the list of userNames
with open("users.csv", "r") as f:
    first = f.readline()
    first = first.rstrip("\r\n")
    fields = first.split(',')
    users = []
    for line in f:
        line = line.rstrip("\r\n")
        values = line.split(',')
        user = {}
        for i in range(len(fields)):
            user[fields[i]] = values[i]
        users.append(user)

scimUser = "https://www.workplace.com/scim/v1/Users/"

#for emailless users, we must leave userName blank and the unique employee ID is mapped to externalId
state = {}
for user in users:
    if user['"external id"'] != "" or (user['"first name"'] == "" and user['"last name"'] == ""):
        state['externalId'] = user['"external id"']
        state['active'] = True
        state['schemas'] = ['urn:scim:schemas:core:1.0','urn:scim:schemas:extension:facebook:auth_method:1.0']
        state['urn:scim:schemas:extension:facebook:auth_method:1.0'] = {}
        state['urn:scim:schemas:extension:facebook:auth_method:1.0']['auth_method'] = 'password'
        state['name'] = {}
        if user['"first name"'] != "":
            state['name']['givenName'] = user['"first name"']
        if user['"last name"'] != "":
            state['name']['familyName'] = user['"last name"']
        state['name']['formatted'] = user['"first name"'] + " " + user['"last name"']
        if user['"job title"'] != "":
            state['title'] = user['"job title"']
        if user['"phone number"'] != "":
            state['phoneNumbers'] = {}
            state['phoneNumbers']['type'] = 'work'
            state['phoneNumbers']['primary'] = True
            state['phoneNumbers']['value'] = user['"phone number"']
        if user['location'] != "":
            state['addresses'] = {}
            state['addresses']['primary'] = True
            state['addresses']['type'] = 'work'
            state['addresses']['locality'] = user['location']
        if user['locale'] != "":
            state['locale'] = user['locale']
        if user['timezone'] != "":
            state['timezone'] = user['timezone']
        if user['department'] != "" or user['organization'] != "" or user['division'] != "" or user['"cost center"'] != "":
            state['schemas'].append('urn:scim:schemas:extension:enterprise:1.0')
            state['urn:scim:schemas:extension:enterprise:1.0'] = {}
            if user['department'] != "":
                state['urn:scim:schemas:extension:enterprise:1.0']['department'] = user['department']
            if user['organization'] != "":
                state['urn:scim:schemas:extension:enterprise:1.0']['organization'] = user['organization']
            if user['division'] != "":
                state['urn:scim:schemas:extension:enterprise:1.0']['division'] = user['division']
            if user['"cost center"'] != "":
                state['urn:scim:schemas:extension:enterprise:1.0']['costCenter'] = user['"cost center"']
        if user['"start date"'] != "":
            state['schemas'].append('urn:scim:schemas:extension:facebook:starttermdates:1.0')
            state['urn:scim:schemas:extension:facebook:starttermdates:1.0'] = {}
            state['urn:scim:schemas:extension:facebook:starttermdates:1.0']['startDate'] = user['"start date"']
        r = requests.post(scimUser, data=json.dumps(state), headers=headers)
        print(r.text)
