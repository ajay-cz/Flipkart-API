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
		filter = {"filter": {"states": ["APPROVED",],},}
		return self.session.post(url, data=json.dumps(filter))
		orderList = []
		resp_json = response.json()
		orderList.append(resp_json["orderItems"])
		while resp_json.get('hasMore') == True:
			response = self.session.get('https://api.flipkart.net/sellers{0}'.format(resp_json['nextPageUrl']))
			resp_json = response.json()
			orderList.append(resp_json["orderItems"])
		return orderList
	
	def get_listing(self, skuid):
		url = "https://api.flipkart.net/sellers/skus/%s/listings" % skuid
		return self.session.get(url)
	
	''' TO-DO post_listing '''
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
	
	''' TO_DO returns '''
	def returns(self):
		url = "http://api.flipkart.net/returns"
		payload = {'source':['customer_return','courier_return'],
				   'modifiedAfter':'2015-06-30',}
		return self.session.get(url, params=payload)
	
	''' TO-DO bulk_listing'''
	def bulk_listing(self, skuids):
		url = "https://api.flipkart.net/sellers/skus/listings/bulk"
		payload = {'listings':[]}
	
	def fetch_labels(self, orderItemIds):
		url = "https://api.flipkart.net/sellers/orders/labels"
		headers = {'Accept': 'application/octet-stream'}
		payload = {'orderItemId':','.join(orderItemIds)}
		return self.session.get(url, params=payload, headers=headers, stream=True)
	
	def get_orders_by_orderItemIds(self, orderItemIds):
		url = "https://api.flipkart.net/sellers/orders/"
		payload = {'orderItemIds':','.join(orderItemIds)}
		return self.session.get(url, params=payload)
	
	def label_request(self, labelRequestId):
		url = "https://api.flipkart.net/sellers/orders/labelRequest/%s" % labelRequestId
		return self.session.get(url)
	
	''' TO-DO cancel_orders '''
	def cancel_orders(self, orderItemId, reason=None):
		url = "https://api.flipkart.net/sellers/orders/cancel"
		payload = [{'orderItemId':orderItemId,
					'reason':reason},]
		return self.session.post(url, data = json.dumps(payload))
	
	''' TO-DO dispatch_orders '''
	def dispatch_orders(self, orderItemId, quantity):
		url = "https://api.flipkart.net/sellers/orders/dispatch"
		payload = {"orderItems": [{"orderItemId": orderItemId,
					"quantity": quantity},]}
		return self.session.post(url, data =json.dumps(payload))
	
	def pack_orders(self, orderItemId, invoiceDate, invoiceNumber, tax, subOrderItemId = None, subInvoiceDate = None, subTax = None):
		url = "https://api.flipkart.net/sellers/orders/labels"
		payload = [{"orderItemId": orderItemId,
					"serialNumbers": [],
					"invoiceDate": invoiceDate,
					"invoiceNumber": invoiceNumber,
					"tax": tax,
					"subItems": []
					}]
		return self.session.post(url, data=json.dumps(payload))