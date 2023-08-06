import requests
import json
import jwt



class Client():   
     
    def __init__(self , auth_config):
        '''
        auth_config is  tokenleaderclient.configs.config_handler.Configs object
        initialized by the user of the client
        ''' 
        self.tl_username = auth_config.tl_user
        auth_config.decrypt_password()
        self.tl_password = auth_config.tl_password  
        self.tl_url = auth_config.tl_url    
        self.ssl_verify = auth_config.ssl_verify     
        self.tokenleader_public_key = auth_config.tl_public_key 
        

    def get_token(self):
        api_route = '/token/gettoken'
        service_endpoint = self.tl_url + api_route
        headers={'content-type':'application/json'}
        self.data=json.dumps(dict(username=self.tl_username, password=self.tl_password))
        try:
            r = requests.post(service_endpoint, self.data, headers=headers, verify=self.ssl_verify)
            r_dict = json.loads(r.content.decode())
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}
        #print(r_dict)
        return r_dict 
              
    
    def verify_token_from_tl(self,token,):
        api_route = '/token/verify_token'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}  
        try:  
            r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
            r_dict = json.loads(r.content.decode())  
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)} 
    #     print(r.content)
    #     print(type(r.content))
        
        return r_dict
    
        
    def verify_token(self, token): 
        #print(self.tokenleader_public_key)  
        payload = self._decrypt_n_verify_token(token, self.tokenleader_public_key)    
        if payload == "Signature expired. Please log in again." :
            status = "Signature expired"
            message = "Signature expired. Please log in and get a fresh token and send it for reverify."
        elif payload == "Invalid token. Please log in again.":
            status = "Invalid token"
            message = "Invalid token. obtain a valid token and send it for verifiaction"
        elif payload == "did you configured the correct public key in the client_config file":
            status = " Invalid public key , can not decrypt  token"
            message = status
        elif not isinstance(payload, dict):
            status = "could not verify token"
            message = status
            
        else:
            status = "Verification Successful"
            message = "Token has been successfully decrypted"   
            
        responseObject = {
                            'status': status,
                            'message': message,
                            'payload': payload}
#         print(responseObject)      
        return responseObject
    
    
    def _decrypt_n_verify_token(self, auth_token, pub_key):
        try:
            payload = jwt.decode(
                auth_token,
                pub_key,
                algorithm=['RS512']
            )
            
            return payload
    #         
        except jwt.ExpiredSignatureError:
                return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
                return 'Invalid token. Please log in again.'
        except ValueError as e:
               return 'did you configured the correct public key in the client_config file'
        except Exception as e:
            return "could not decrypt the token for error {}".format(e)

            
    def list_users(self):
        token = self.get_token().get('auth_token')
        api_route = '/list/users'
        service_endpoint = self.tl_url + api_route
        headers={'X-Auth-Token': token}  
        try:  
            r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
            r_dict = json.loads(r.content.decode())   
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}    #     
        
#         print(r_dict)  # for displaying from the cli  print in cli parser
        return r_dict
        
    

