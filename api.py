import requests
import json


class FlipkartAPI:
	def __init__(self, token):
		self.token = token
		self.session = self.get_session()
    
	def get_session(self):
		session = requests.Session()
		session.headers.update({
			'Authorization': 'Bearer %s' % self.token,
			'Content-type': 'application/json',
		})
		return session
    
	def search_orders(self):
		url = "https://api.flipkart.net/sellers/orders/search"
		filter = {"filter": {"states": ["PACKED","APPROVED","READY_TO_DISPATCH","CANCELLED"],},}
		response = self.session.post(url, data=json.dumps(filter))
		response_json = response.json()
		orders = []
		orders.append(response_json)
		while response_json.get('hasMore') == True:
			response = self.session.get('https://api.flipkart.net/sellers{0}'.format(response_json['nextPageUrl']))
			response_json = response.json()
			orders.append(response_json)
		else:
			print "All Orders Fetched"
		return orders
        
        
	def get_listing(self, skuid):
		url = "https://api.flipkart.net/sellers/skus/%s/listings" % skuid
		return self.session.get(url)
	
# TO-DO post_listing
	def post_listing(self, skuid, attributes):
		url = "https://api.flipkart.net/sellers/skus/%s/listings" % skuid
		return self.session.post(url, attribute=attributes)
	
	def get_order_by_orderItemId(self, orderItemId):
		url = "https://api.flipkart.net/sellers/orders/%s" % orderItemId
		return self.session.get(url)
	
	def shipment(self, orderItemIds):
		url = "https://api.flipkart.net/sellers/orders/shipments"
		payload = {'orderItemIds':','.join(orderItemIds)}
		return self.session.get(url, params=payload)

# TO-DO returns	
	def returns(self, source=None, modifiedAfter=None, createdAfter=None):
		url = "http://api.flipkart.net/returns"
		payload = {'source':'',
				   'modifiedAfter':'',
				   'createdAfter':'',}
		return self.session.get(url, params=payload)
		
	
