# Flipkart-Python
Flipkart Seller Api - python

Example:

from auth import Authentication <br>
from api import FlipkartAPI

auth = Authentication(app_id, app_secret) <br>
token_str = auth.get_access_token().json() <br>
token = token_str['access_token']

flipkart = FlipkartAPI(token) <br>
sku_listing = flipkart.get_listing(sku_id)
