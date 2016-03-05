import requests
import json

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
    
    def getAccessToken(self):

        '''
        Send a GET REQUEST to fetch an access token.
        '''

        data = {'grant_type':'client_credentials','scope':'Seller_Api'}
        return requests.get(self.url, params = data, auth = (self.application_id, self.application_secret))




class FlipkartAPI:
	def __init__(self, token, sandbox=False):

		'''Initialize the FlipkartAPI Class with token we got from Authentication class.		
		'''

		self.token = token
		self.session = self.getSession()
		self.sandbox = sandbox


	

	def getSession(self):

		''' Create a session to GET or POST long data sequences. 
		'''
		
		session = requests.Session()
		session.headers.update({
			'Authorization': 'Bearer %s' % self.token,
			'Content-type': 'application/json',
		})
		return session




	
	def searchOrders(self, order_states_list, from_date=None):

		'''
		Method search_orders fetch all the orders which are not completed. We have to pass the status of Orders as a list of strings.
		Status: ["APPROVED", "CANCELLED", "READY_TO_DISPATCH", "PACKED"]. Returns a list of orders with each order of <dict> type.
		'''

		if self.sandbox == True:
			url = "https://api.flipkart.net/sellers/v2/orders/search"
			next_url = 'https://sandbox-api.flipkart.net/sellers/v2{0}'
		else:
			url = "https://api.flipkart.net/sellers/v2/orders/search"
			next_url = 'https://api.flipkart.net/sellers/v2{0}'


		if from_date == None:
			payload = {"filter": {
						"states":order_states_list,
					},
					"pagination": {
						"pageSize":20
					}
				  }
		else:
			payload = {"filter": {
						"states":order_states_list,
						"orderDate": {
							"fromDate": from_date,
						}
					},
					"pagination": {
						"pageSize":20
					}
				  }
		response = self.session.post(url, data = json.dumps(payload))
		orders = []
		resp_json = response.json()

		for each in resp_json['orderItems']:
			orders.append(each)

		while resp_json['hasMore'] == True:
			new_url = ''
			new_url = next_url.format(resp_json['nextPageUrl'])
			response = self.session.get(new_url)
			resp_json = response.json()
			for each in resp_json['orderItems']:
				orders.append(each)

		return orders



		
	def getListingByListingId(self, listing_id):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/skus/listings/%s" % listing_id
		else:
			url = "https://api.flipkart.net/sellers/skus/listings/%s" % listing_id
		return self.session.get(url)




	
	def getListingBySkuId(self, sku_id):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/skus/%s/listings" % skuid
		else:
			url = "https://api.flipkart.net/sellers/skus/%s/listings" % skuid
		return self.session.get(url)




	
	def postListing(self, listing_id_list, stock_list, selling_price_list, mrp_list=None, status_list=None, national_ship_charge_list=None, zonal_ship_charge_list=None, local_ship_charge_list=None, sla_list=None):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/skus/listings/bulk"
		else:
			url = "https://api.flipkart.net/sellers/skus/listings/bulk"

		payload = {"listings":[]}

		""" Check for optional list. If one is empty then only update stock and selling_price"""

		if mrp_list == None:
			for listing_id, stock, selling_price in zip(listing_id_list, stock_list, selling_price_list):
				payload['listings'].append({"listingId": listing_id,
											"attributeValues": {
												"selling_price": selling_price,
												"stock_count": stock
											}
										})
		else:
			for listing_id, selling_price, stock, mrp, status, nsc, zsc, lsc, sla in zip(listing_id_list, selling_price_list, stock_list, mrp_list, status_list, national_ship_charge_list, zonal_ship_charge_list, local_ship_charge_list, sla_list):
				payload['listings'].append({"listingId": listing_id,
											"attributeValues": {
												"mrp": mrp,
												"selling_price": selling_price,
												"listing_status": status,
												"fulfilled_by": "seller",
												"national_shipping_charge": nsc,
												"zonal_shipping_charge": zsc,
												"local_shipping_charge": lsc,
												"procurement_sla": sla,
												"stock_count": stock
											}
										})
		return self.session.post(url, data=json.dumps(payload))
	



	def getOrderByOrderItemId(self, order_item_id):

		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/v2/orders/%s" % order_item_id
		else:
			url = "https://api.flipkart.net/sellers/v2/orders/%s" % order_item_id
		return self.session.get(url)




	
	def getShipment(self, order_item_id_list):
		if self.sandbox == True:
			url = "https://api.flipkart.net/sellers/v2/orders/shipments"
		else:
			url = "https://api.flipkart.net/sellers/v2/orders/shipments"
		payload = {'orderItemIds':','.join(order_item_id_list)}
		return self.session.get(url, params=payload)





	def getReturns(self, return_source, createdAfter=None):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/v2/returns"
			next_url = 'https://sandbox-api.flipkart.net/sellers/v2{0}'
		else:
			url = "https://api.flipkart.net/sellers/v2/returns"
			next_url = "https://api.flipkart.net/sellers/v2{0}"

		payload = {'source':return_source,
					'createdAfter':createdAfter}
		response = self.session.get(url, params=payload)
		orders = []
		resp_json = response.json()

		for each in resp_json['returnItems']:
			orders.append(each)

		# print resp_json, type(resp_json)

		# while resp_json['hasMore'] == True:
		# 	print resp_json['hasMore']
		# 	print resp_json['nextUrl']
		# 	new_url = ''
		# 	new_url = next_url.format(resp_json['nextUrl'])
		# 	response = self.session.get(new_url)
		# 	resp_json = response.content
		# 	print resp_json
			# for each in resp_json['returnItems']:
			# 	orders.append(each)

		return orders

	
	def fetchLabels(self, order_item_id_list):

		'''
		This method fetch shipping labels for those orderItemIds which have been packed.
		'''

		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/v2/orders/labels"
		else:
			url = "https://api.flipkart.net/sellers/v2/orders/labels"
		headers = {'Content-type': 'application/octet-stream'}
		payload = {'orderItemIds':','.join(order_item_id_list)}
		return self.session.get(url, params=payload, headers=headers, stream=True)




	
	def getOrderByOrderItemIds(self, order_item_id_list):

		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/v2/orders/"
		else:
			url = "https://api.flipkart.net/sellers/v2/orders/"

		payload = {'orderItemIds':','.join(order_item_id_list)}
		return self.session.get(url, params=payload)




	
	def getInvoice(self, order_item_id_list):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/v2/orders/invoices"
		else:
			url = "https://api.flipkart.net/sellers/v2/orders/invoices"

		payload = {'orderItemIds':','.join(order_item_id_list)}
		return self.session.get(url, params=payload)





	def cancelOrders(self, order_item_id_list, reason_list=None):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/v2/orders/cancel"
		else:
			url = "https://api.flipkart.net/sellers/v2/orders/cancel"

		payload = []
		for order_item_id, reason in zip(order_item_id_list, reason_list):
			payload.append({'orderItemId':orderItemId,
					'reason':reason})
		return self.session.post(url, data = json.dumps(payload))



	def bulkDispatchOrders(self, order_item_id_list, quantity_list):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/dispatch"
		else:
			url = "https://api.flipkart.net/sellers/orders/dispatch"

		payload = {"orderItems": []}
		for oid, qty in zip(order_item_id_list, quantity_list):
			payload['orderItems'].append({"orderItemId": oid, "quantity": qty})

		return self.session.post(url, data =json.dumps(payload))




	
	def bulkPackOrders(self, order_item_id_list, invoice_date_list, tax_rate_list):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/v2/orders/labels"
		else:
			url = "https://api.flipkart.net/sellers/v2/orders/labels"

		payload = {"orderItems":[]}

		for order_item_id, invoice_date, tax_rate in zip(order_item_id_list, invoice_date_list, tax_rate_list):
			payload["orderItems"].append({"orderItemId":order_item_id,
										  "taxRate":tax_rate,
										  "serialNumbers":[],
										  "invoiceDate":invoice_date,
										  "subItems":[]})

		return self.session.post(url, data=json.dumps(payload))



	def fetchManifest(self):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/v2/orders/manifest"
		else:
			url = "https://api.flipkart.net/sellers/v2/orders/manifest"

		return self.session.get(url)