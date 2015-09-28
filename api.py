import requests
import json


class FlipkartAPI:
	def __init__(self, token, sandbox=False):

		'''Initialize the FlipkartAPI Class with token we got from Authentication class.		
		'''

		self.token = token
		self.session = self.get_session()
		self.sandbox = sandbox



	

	def get_session(self):

		''' Create a session to GET or POST long data sequences. 
		'''
		
		session = requests.Session()
		session.headers.update({
			'Authorization': 'Bearer %s' % self.token,
			'Content-type': 'application/json',
		})
		return session




	
	def search_orders(self, order_states):

		'''
		Method search_orders fetch all the orders which are not completed. We have to pass the status of Orders as a list of strings.
		Status: ["APPROVED", "CANCELLED", "READY_TO_DISPATCH", "PACKED"]
		'''

		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/search"
			url1 = 'https://sandbox-api.flipkart.net/sellers{0}'
		else:
			url = "https://api.flipkart.net/sellers/orders/search"
			url1 = 'https://api.flipkart.net/sellers{0}'
		filter = {"filter": {"states": order_states},}
		response = self.session.post(url, data=json.dumps(filter))
		resp_json = response.json()
		data_string = resp_json
		while resp_json.get('hasMore') == True:
			response = self.session.get(url1.format(resp_json['nextPageUrl']))
			resp_json = response.json()
			data_string.update(resp_json)
		return data_string




	
	def get_listing(self, skuid):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/skus/%s/listings" % skuid
		else:
			url = "https://api.flipkart.net/sellers/skus/%s/listings" % skuid
		return self.session.get(url)




	
	def post_listing(self, sku_id, listing_id, mrp, selling_price, status, nsc, zsc, lsc, sla, stock):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/skus/%s/listings" % sku_id
		else:
			url = "https://api.flipkart.net/sellers/skus/%s/listings" % sku_id
		payload = {"skuId": sku_id,
					"listingId": listing_id,
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
					}
		return self.session.post(url, data = json.dumps(payload))
	
	def get_order_by_orderItemId(self, orderItemId):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/%s" % orderItemId
		else:
			url = "https://api.flipkart.net/sellers/orders/%s" % orderItemId
		return self.session.get(url)




	
	def shipment(self, orderItemIds):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/shipments"
		else:
			url = "https://api.flipkart.net/sellers/orders/shipments"
		payload = {'orderItemIds':','.join(orderItemIds)}
		return self.session.get(url, params=payload)




	
	''' TO_DO returns '''
	def returns(self):
		if self.sandbox == True:
			url = "http://sandbox-api.flipkart.net/returns"
		else:
			url = "http://api.flipkart.net/returns"
		payload = {'source':['customer_return','courier_return'],
				   'modifiedAfter':'2015-06-30',}
		return self.session.get(url, params=payload)



	
	def bulk_listing(self,listing_ids, sku_ids, fsns, mrps, selling_prices, status, nscs, zscs, lscs, slas, stocks):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/skus/listings/bulk"
		else:
			url = "https://api.flipkart.net/sellers/skus/listings/bulk"
		payload = {'listings':[]}
		for lid, sku, fsn, mrp, sp, stts, nsc, zsc, lsc, sla, stck in zip(listing_ids, sku_ids, fsns, mrps, selling_prices, status, nscs, zscs, lscs, slas, stocks):
			payload['listings'].append({"listingId": lid,
										"skuId": sku,
										"fsn": fsn,
										"attributeValues": {
											"mrp": mrp,
											"selling_price": sp,
											"listing_status": stts,
											"fulfilled_by": "seller",
											"national_shipping_charge": nsc,
											"zonal_shipping_charge": zsc,
											"local_shipping_charge": lsc,
											"procurement_sla": sla,
											"stock_count": stck}
										})
		return self.session.post(url, data = json.dumps(payload))




	
	def fetch_labels(self, orderItemIds):

		'''
		This method fetch shipping labels for those orderItemIds which have been packed.
		'''

		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/labels"
		else:
			url = "https://api.flipkart.net/sellers/orders/labels"
		headers = {'Accept': 'application/octet-stream'}
		payload = {'orderItemId':','.join(orderItemIds)}
		return self.session.get(url, params=payload, headers=headers, stream=True)




	
	def get_orders_by_orderItemIds(self, orderItemIds):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/"
		else:
			url = "https://api.flipkart.net/sellers/orders/"
		payload = {'orderItemIds':','.join(orderItemIds)}
		return self.session.get(url, params=payload)




	
	def label_request(self, labelRequestId):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/labelRequest/%s" % labelRequestId
		else:
			url = "https://api.flipkart.net/sellers/orders/labelRequest/%s" % labelRequestId
		return self.session.get(url)






	def cancel_orders(self, order_item_id_list):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/cancel"
		else:
			url = "https://api.flipkart.net/sellers/orders/cancel"
		payload = []
		for order_item_id in order_item_id_list:
			payload.append({'orderItemId':order_item_id,
							 'reason':'Cancelled By Seller'})
		return self.session.post(url, data = json.dumps(payload))



	
	def dispatch_orders(self, orderItemId, quantity):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/dispatch"
		else:
			url = "https://api.flipkart.net/sellers/orders/dispatch"
		payload = {"orderItems": [{"orderItemId": orderItemId,
					"quantity": quantity},]}
		return self.session.post(url, data =json.dumps(payload))




	
	def pack_orders(self, order_item_id, invoice_date, invoice_number, tax, sub_order_item_id = None, sub_invoice_date = None, sub_tax = None):
		if self.sandbox == True:
			url = "https://sandbox-api.flipkart.net/sellers/orders/labels"
		else:
			url = "https://api.flipkart.net/sellers/orders/labels"

		payload = [{"orderItemId": order_item_id,
					"serialNumbers": [],
					"invoiceDate": invoice_date,
					"invoiceNumber": invoice_number,
					"tax": tax,
					"subItems": []
					}]
		return self.session.post(url, data=json.dumps(payload))