import requests

class Authentication:
    def __init__(self, application_id, application_secret, sandbox = False):

        '''

        Initialize all the parametres.
        application_id and application_secret as provided by flipkart. Read the Flipkart APi for how to get your application_id and application_secret.

        '''

        self.application_id = application_id
        self.application_secret = application_secret
        self.sandbox = sandbox
        if self.sandbox == True:
        	self.url = "https://sandbox-api.flipkart.net/oauth-service/oauth/token"
        else:
            self.url = "https://api.flipkart.net/oauth-service/oauth/token"
    
    def get_access_token(self):

        '''
        Send a GET REQUEST to fetch an access token.
        '''

        data = {'grant_type':'client_credentials','scope':'Seller_Api'}
        return requests.get(self.url, params = data, auth = (self.application_id, self.application_secret))
