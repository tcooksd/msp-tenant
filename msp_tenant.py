#!/usr/bin/python

import requests
import json
token = "5a671567-31c5-442d-8d93-633de4074707"
url1 = "https://10.0.0.8/api/"

#NOTE:
# Current requests are handled through vars assigned globably. 
class Morpheus:
    headers={
        'Authorization': 'Bearer %s ' % token,
        'Content-Type': 'application/json'
    }
    def __init__(
        self, baseurl, api_location, data):
        self.baseurl = baseurl
        self.api_location = api_location
        self.data = data

    def getreq(self):
        response=requests.get(
            url= url1 + self.api_location,
            headers = self.headers,
            verify = False
            )
        json_payload = ('{content}'.format(
                content=response.content))
        return json.loads(json_payload)


    def putreq(self):
        response=requests.post(
            url= url1 + self.api_location,
            headers = self.headers,
            data = self.data,
            verify = False
            )
        json_payload = ('{content}'.format(
                content=response.content))
        return json.loads(json_payload)




#loop through tenants and return a list of tenant names.
def check_tenant():
    tenantn = []
    morph = Morpheus( url1, "accounts", "" )
    for i in morph.getreq()['accounts']:
         tenantn.append(i['name'])
    return tenantn

#takes:
# 1 arg: tenant name.
#returns:
# dict of tenant metadata.
def tenantinfo(tenantn):
    morph = Morpheus( url1, "accounts", "" )
    if tenantn in check_tenant():
        for i in morph.getreq()['accounts']:
            if i['name'] == tenantn:
                return i
#takes:
# 3 args:
#group_name = name of the group:
#location = geo location
#api_location = api endpoint
def create_group(group_name, api_location, location="west"):
    data01 = """ {
        "group": {
            "name": "%s",
            "description": "My description",
            "location": "%s"
            }
        } """ % ( group_name, location )
    morph = Morpheus( url1, api_location, data01 )
    morph.putreq()


def create_user(username, email, firstn, lastn, passwd, api_location):
    data01 = """ {
        "user": {
            "username": "%s",
            "email": "%s",
            "firstname": "%s",
            "lastname": "%s",
            "password": "%s",
            "role":
                {"id": "4"}
            }
        } """ % ( username, email, firstn, lastn, passwd )
    morph = Morpheus( url1, api_location, data01 )
    morph.putreq()

def create_cloud(username, code, description, location,
    groupid, account_id, api_location):
    data01 = """ {
        "zone": {
            "name": "%s",
            "code": "%s",
            "description": "%s",
            "location": "%s",
            "groupId": "%s",
            "accountId": "%s"
            }
        } """ % ( username, code, description, location, groupid, account_id )
    morph = Morpheus( url1, api_location, data01 )
    morph.putreq()

def create_tenant(tenant_name, api_location="accounts"):
    #Validate if tenant exists.
    if  tenantinfo(tenant_name):
        print "Tenant Exists:"
        print tenantinfo(tenant_name)
    else:
        data01 = """ {
                    "account": {
                        "name": "%s",
                        "description": "My description",
                        "subdomain": "%s",
                        "role":
                            {"id": "5"}
                            }
                            } """ % ( tenant_name, tenant_name )
        morph = Morpheus( url1, api_location, data01 )
        morph.putreq()

        create_group("demo_group", "accounts/%s/groups"
            % tenantinfo(tenant_name)['id'])

        # Find the group id to use when creating a cloud.
        # The only value that matters to the class instance is url1 .
        morph = Morpheus( url1, "accounts/sdf/groups", "data")
        id1 = tenantinfo(tenant_name)['id']
        morph.api_location = "accounts/%s/groups" % id1

        for i in morph.getreq()['groups']:
            if i['name'] == "demo_group":
                group_id = i['id']


        create_user("tcooktest1", "tcook@gmail.com", "Tim", "Cook", "00pha7Bu!",
            "accounts/%s/users" % tenantinfo(tenant_name)['id'])

        create_cloud("name", "demo_cloud", "description", "location",
            "%s" % group_id, "%s" % tenantinfo(tenant_name)['id'], "zones")



create_tenant("tcooktest1112")

#print check_tenant("test")
