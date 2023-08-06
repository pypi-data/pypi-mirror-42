import unittest
# from flask import Flask
from flask_testing import TestCase
import json
from  tokenleaderclient import flaskapp
# from tokenleaderclient.rbac import enforcer
from tokenleaderclient.tests.test_acl import enforcer, role_acl_map_file
from tokenleaderclient.tests.test_acl import sample_token,admin_token 
from tokenleaderclient.tests.test_acl import sample_token_role_as_list_nonexisting
from tokenleaderclient.tests.test_acl import sample_token_role_as_list_valid_role
from tokenleaderclient.tests.test_acl import enforcer_user_input  

app = flaskapp.create_app()

sample_token_multi_role = {"message":"Token has been successfully decrypted",
                          "payload":{"exp":1548487022,
                                     "iat":1548483422,
                                     "sub":{"email":"user_with_multi_role@itc.in",
                                            "id":1,
                                            "roles": ["role1", "role2"],
                                            "username":"user_with_multi_role",
                                            "wfc": {
                                                    "department": "dept1",
                                                    "id": 1,
                                                    "name": "wfc1",
                                                    "org": "org1",
                                                    "orgunit": "ou1"
                                                  }
                                            }
                                     },
                          "status":"Verification Successful"}


sample_token_user1_role_mismatched = {"message":"Token has been successfully decrypted",
                          "payload":{"exp":1548487022,
                                     "iat":1548483422,
                                     "sub":{"email":"admin@itc.in",
                                            "id":1,
                                            "roles": ["role_mismatched"],
                                            "username":"user1",
                                            "wfc": {
                                                    "department": "dept1",
                                                    "id": 1,
                                                    "name": "wfc1",
                                                    "org": "org1",
                                                    "orgunit": "ou1"
                                                  }
                                            }
                                     },
                          "status":"Verification Successful"}


sample_token_user1_rule_mismatched = {"message":"Token has been successfully decrypted",
                          "payload":{"exp":1548487022,
                                     "iat":1548483422,
                                     "sub":{"email":"user1@itc.in",
                                            "id":1,
                                            "roles": ["role1",],
                                            "username":"user1",
                                            "wfc": {
                                                    "department": "dept1",
                                                    "id": 1,
                                                    "name": "wfc1",
                                                    "org": "org1",
                                                    "orgunit": "ou1"
                                                  }
                                            }
                                     },
                          "status":"Verification Successful"}


@enforcer.enforce_access_rule_with_token('service1:first_api:rulename1', 
                                           role_acl_map_file, admin_token)
def acl_enforcer_func_for_test_with_admin_token(wfc=None):
    msg = ("enforcer decorator working ok with admin")  
    return msg
 


@enforcer_user_input.enforce_access_rule_with_token('service1:first_api:rulename1', 
                                           role_acl_map_file, admin_token)
def acl_enforcer_func_for_test_with_admin_token_user_input(wfc=None):
    msg = ("enforcer decorator working ok with admin")  
    return msg
 


@enforcer.enforce_access_rule_with_token('service1:first_api:rulename1', 
                                           role_acl_map_file, sample_token)
def acl_enforcer_func_for_test(wfc=None):
    msg = ("enforcer decorator working ok with wfc org = {},"
            "orgunit={}, dept={}".format(wfc.org, wfc.orgunit, wfc.department))
  
    return msg
 
 
 
@enforcer_user_input.enforce_access_rule_with_token('service1:first_api:rulename1', 
                                           role_acl_map_file, sample_token)
def acl_enforcer_func_for_test_user_input(wfc=None):
    msg = ("enforcer decorator working ok with wfc org = {},"
            "orgunit={}, dept={}".format(wfc.org, wfc.orgunit, wfc.department))
  
    return msg
 
 
@enforcer.enforce_access_rule_with_token('service1:third_api:rulename3', 
                                           role_acl_map_file, sample_token_multi_role)
def acl_enforcer_func_for_test_multirole(wfc=None):
#     return "enforcer decorator working ok with multi role and wfc {}".WFC.org
    return "enforcer decorator working ok with multi role"



@enforcer.enforce_access_rule_with_token('service1:first_api:rulename1', role_acl_map_file, 
                                           sample_token_user1_role_mismatched)
def acl_enforcer_role_mismatched():
    return "falied due to role mismatched"


@enforcer.enforce_access_rule_with_token('rule_mismatched', role_acl_map_file, 
                                           sample_token_user1_rule_mismatched)
def acl_enforcer_permission_mismatched():
    return "failed due to permission rule mismatched"

txt = "enforcer decorator working ok with wfc org = org1,orgunit=ou1, dept=dept1" 


class TestAclEnforcer(TestCase):
    def create_app(self):       
        return app              
    
    
    def acl_enforcer_func_for_test_with_admin_token(self):
        msg = acl_enforcer_func_for_test_with_admin_token()
        self.assertTrue(msg == "enforcer decorator working ok with admin")
        
    def acl_enforcer_func_for_test_with_admin_token_user_input(self):
        msg = acl_enforcer_func_for_test_with_admin_token_user_input()
        self.assertTrue(msg == "enforcer decorator working ok with admin")
        
    def test_acl_enforcer_func(self):
        msg = acl_enforcer_func_for_test() 
        self.assertTrue(msg == txt)
        
    def test_acl_enforcer_func_user_input(self):
        msg = acl_enforcer_func_for_test_user_input() 
        self.assertTrue(msg == txt)
    
    def test_acl_enforcer_func_multirole(self):
        msg = acl_enforcer_func_for_test()
        self.assertTrue(msg == txt)
          
    def test_acl_enforcer_role_mismatched(self):        
        msg = acl_enforcer_role_mismatched()
        #print(msg)
        self.assertFalse(msg == "falied due to role mismatched")
    
    def test_acl_enforcer_permission_mismatched(self):        
        msg = acl_enforcer_permission_mismatched()
        #print(msg)
        self.assertFalse(msg =="failed due to permission rule mismatched")
        


# role_acl_map_file='tokenleaderclient/tests/testdata/role_to_acl_map.yml'
# 
# 
# admin_token = {"message":"Token has been successfully decrypted",
#                           "payload":{"exp":1548487022,
#                                      "iat":1548483422,
#                                      "sub":{"email":"admin@itc.in",
#                                             "id":1,
#                                             "roles": ["admin"],
#                                             "username":"admin",
#                                             "wfc": {
#                                                     "department": "dept1",
#                                                     "id": 1,
#                                                     "name": "wfc1",
#                                                     "org": "org1",
#                                                     "orgunit": "ou1"
#                                                   }
#                                             }
#                                      },
#                           "status":"Verification Successful"}
# 
# sample_token = {"message":"Token has been successfully decrypted",
#                           "payload":{"exp":1548487022,
#                                      "iat":1548483422,
#                                      "sub":{"email":"user1@itc.in",
#                                             "id":1,
#                                             "roles": ["role1"],
#                                             "username":"user1",
#                                             "wfc": {
#                                                     "department": "dept1",
#                                                     "id": 1,
#                                                     "name": "wfc1",
#                                                     "org": "org1",
#                                                     "orgunit": "ou1"
#                                                   }
#                                             }
#                                      },
#                           "status":"Verification Successful"}
