#!./venv/bin/python

# -*- coding: utf-8 -*-

import os
import sys
import argparse


possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir))
                                                

# 
# if os.path.exists(os.path.join(possible_topdir,
#                                'app1',
#                                '__init__.py')):
apppath = (os.path.join(possible_topdir,
                               'tokenleaderclient',
                               'tokenleaderclient'))
#    sys.path.insert(0, apppath)

sys.path.insert(0, apppath)

#print(sys.path)
from tokenleaderclient.configs.config_handler import Configs
from tokenleaderclient.client.client  import Client
auth_config = Configs()
c = Client(auth_config)

parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument( '--authuser', action = "store", dest = "authuser", required = False,)
parent_parser.add_argument('--authpwd', action = "store", dest = "authpwd", required = False)


subparser = parent_parser.add_subparsers()

token_parser = subparser.add_parser('gettoken', parents=[parent_parser], help="Get a token from the tokenleader server ,"
                                    " configure {} and generate the auth file using tlconfig command before"
                                    "getting a token".format(auth_config.config_file))

token_parser = subparser.add_parser('verify', help='verify  a token' )
token_parser.add_argument('-t', '--token', 
                  action = "store", dest = "token",
                  required = True,
                  help = "verify and retrieve users role and work context from the token "
                        " ensure you have obtained the public key from the tokenleader server"
                        "and put it in tl_public_key section of {}".format(auth_config.config_file)
                  )

list_parser = subparser.add_parser('list', help='listuser' )
list_parser.add_argument('entity', choices=['org', 'ou', 'dept', 'wfc', 'role', 'user' ])
list_parser.add_argument('-n', '--name', 
                  action = "store", dest = "name",
                  required = False,
                  help = "Name of the entitiy , type 'all' as name while listing ",
                  )


try:                    
    options = parent_parser.parse_args()  
except:
    #print usage help when no argument is provided
    parent_parser.print_help(sys.stderr)    
    sys.exit(1)

def main():     
  
    if len(sys.argv)==1:
        # display help message when no args are passed.
        parent_parser.print_help()
        sys.exit(1)   
   
    #print(sys.argv)
    if options.authuser and options.authpwd:        
        auth_config = Configs(tlusr=options.authuser, tlpwd=options.authpwd)
        c = Client(auth_config)
        print("initializing client  using the user name and password supplied from CLI")
    
    if  sys.argv[1] == 'gettoken':
        print(c.get_token())
        
    if  sys.argv[1] == 'verify':
        print(c.verify_token(options.token))
    
    if  sys.argv[1] == 'list':
        if options.name:
            print(c.list_user_byname(options.name))
        else:
            print(c.list_users())
                
     
    
if __name__ == '__main__':
    main()
    
'''
/mnt/c/mydev/microservice-tsp-billing/tokenleader$ ./tokenadmin.sh  -h    to get help
'''
    
    
