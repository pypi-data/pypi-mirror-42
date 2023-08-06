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
                               'micros1client',
                               'micros1client'))
#    sys.path.insert(0, apppath)

sys.path.insert(0, apppath)

#print(sys.path)

from tokenleaderclient.configs.config_handler import Configs    
from  tokenleaderclient.client.client import Client 
from micros1client.client   import MSClient

auth_config = Configs()
tlclient = Client(auth_config)
c = MSClient(tlclient)

parser = argparse.ArgumentParser(add_help=False)


subparser = parser.add_subparsers()

ep3_parser = subparser.add_parser('ep3', help="call the ep3 api route from microservice micros1")

try:                    
    options = parser.parse_args()  
except:
    #print usage help when no argument is provided
    parser.print_help(sys.stderr)    
    sys.exit(1)

def main():
    if len(sys.argv)==1:
        # display help message when no args are passed.
        parser.print_help()
        sys.exit(1)   
   
    #print(sys.argv)
    
    if  sys.argv[1] == 'ep3':
        print(c.ep3())     
                    
     
    
if __name__ == '__main__':
    main()
    
'''
/mnt/c/mydev/microservice-tsp-billing/tokenleader$ ./tokenadmin.sh  -h    to get help
'''
    
    
