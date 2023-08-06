import requests
import json
import jwt

# from tokenleaderclient.client.client import Client as tlClient
from micros1client.configs.config_handler import Configs as MSConfig

# must_have_keys_in_yml_for_ms1c = {
#                                   'url_type',
#                                   'ssl_enabled',
#                                   'ssl_verify'                            
#                                  }   

service_name = 'micros1'
conf_file='/etc/tokenleader/client_configs.yml'

must_have_keys_in_yml = {}   

conf = MSConfig(service_name, conf_file=conf_file, must_have_keys_in_yml= must_have_keys_in_yml)

micros1_yml = conf.yml.get(service_name)
#print(yml)


# TC = tlClient()

class MSClient():   
    '''
    First initialize an instance of tokenleader client and  pass it to MSCclient 
    as its parameter
    '''
    
    def __init__(self, tlClient ):       
        
        self.tlClient = tlClient
        self.url_type = micros1_yml.get('url_type')
        self.ssl_enabled = micros1_yml.get('ssl_verify')
        self.ssl_verify = micros1_yml.get('ssl_verify')
        self.url_to_connect = self.get_url_to_connect()
        

    def get_url_to_connect(self):
        url_to_connect = None
        catalogue = self.tlClient.get_token()['service_catalog']
        #print(catalogue)
        if catalogue.get(service_name):
            #print(catalogue.get(service_name))
            url_to_connect = catalogue[service_name][self.url_type]
        else:
            msg = ("{} is not found in the service catalogue, ask the administrator"
                   " to register it in tokenleader".format(service_name))
            print(msg)
        return url_to_connect
    
    
    def ep3(self):
        token = self.tlClient.get_token().get('auth_token')
        api_route = '/ep3'
        service_endpoint = self.url_to_connect + api_route
        headers={'X-Auth-Token': token}  
        try:  
            r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
            r_dict = json.loads(r.content.decode())   
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}    #     
        
#         print(r_dict)  # for displaying from the cli  print in cli parser
        return r_dict
              
    
    
    

