import requests

class Authentication:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.url = "https://api.flipkart.net/oauth-service/oauth/token"
    
    def get_access_token(self):
        data = {'grant_type':'client_credentials','scope':'Seller_Api'}
        return requests.get(self.url, params = data, auth = (self.app_id, self.app_secret))
