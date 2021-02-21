#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ========================================================
# import設定
# ========================================================
import requests, time, json, random, string
import hmac, hashlib, base64

# ========================================================
# EndPoint Format
# ========================================================
# https://{base-url}/{api-path}?{query-string}
# Required HTTPS, JSON, and Auth
# Content-Type: application/json
# ========================================================
# TestNet(Cashew) : test-api.blockchain.line.me
# MainNEt(Daphne) : api.blockchain.line.me
# ========================================================

class API:

	# コンストラクタ
	def __init__(self, api_key, secret_key, is_distribution):
		if is_distribution == True:
			self.url = 'https://api.blockchain.line.me'
		else:
			self.url = 'https://test-api.blockchain.line.me'

		self.api_key = api_key
		self.secret_key = secret_key
		self.headers = { 'service-api-key': self.api_key }

		API.refresh_request(self)

	# nonceとtimestampを更新
	def refresh_request(self, is_json = False):
		self.nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
		self.timestamp = str(int(round(time.time() * 1000)))
		self.headers['nonce'] = self.nonce
		self.headers['timestamp'] = self.timestamp

		if is_json == True:
			self.headers['Content-Type'] = 'application/json'
		else:
			if 'Content-Type' in self.headers:
				del self.headers['Content-Type']

	# signature算出
	def get_signature(self, method, path, params = [], body = ''):
		print(method + ': ' + path)
		signStr = self.nonce + str(self.timestamp) + method + path

		isFirst = True
		for key, value in params:
			if isFirst:
				signStr += '?'
			else:
				signStr += '&'

			signStr += key + '=' + str(value)
			isFirst = False

		signStr += str(body)

		hashStr = hmac.new(bytes(self.secret_key, 'UTF-8'), bytes(signStr, 'UTF-8'), hashlib.sha512).hexdigest()
		print('signStr = ' + signStr)
		print('hashStr = ' + hashStr)
		print('signature  = ' + str(base64.b64encode(hashStr.encode())))
		self.headers['signature'] = base64.b64encode(hashStr.encode())

	# サーバ時刻取得
	def GET_v1_time(self):
		path = '/v1/time'
		return requests.get(self.url + path, headers=self.headers).json()

	# サービス情報取得
	def GET_v1_services(self, service_id):
		path = '/v1/services/' + service_id
		API.refresh_request(self)
		API.get_signature(self, 'GET', path)
		return requests.get(self.url + path, headers=self.headers).json()

	# サービストークンの一覧を取得
	# サービストークンはサービスごとに最大100件まで作成可能
	def GET_v1_service_tokens(self):
		path = '/v1/service-tokens'
		API.refresh_request(self)
		API.get_signature(self, 'GET', path)
		return requests.get(self.url + path, headers=self.headers).json()

	# サービストークンの情報を取得
	# 指定されたcontractに属しているサービストークン情報を取得
	def GET_v1_service_tokens_by_contract_id(self, contract_id):
		path = '/v1/service-tokens/' + contract_id
		API.refresh_request(self)
		API.get_signature(self, 'GET', path)
		return requests.get(self.url + path, headers=self.headers).json()

	# サービストークンの情報を更新
	# 指定されたcontractに該当するサービストークン情報を更新
	def PUT_v1_service_tokens_update(self, contract_id, name, meta, ownerAddress, ownerSecret):
		path = '/v1/service-tokens/' + contract_id
		API.refresh_request(self, is_json=True)

		request_body = sorted({
			'name': name,
			'meta': meta,
			'ownerAddress': ownerAddress,
			'ownerSecret': ownerSecret
		})
		API.get_signature(self, 'PUT', path, body=request_body)
		return requests.put(self.url + path, headers=self.headers, json=str(request_body)).json()

	# サービストークンを鋳造
	# 指定されたサービストークンを新しく鋳造して希望ウォレットに発行
	def POST_v1_service_tokens_mint(self, contract_id, ownerAddress, ownerSecret, toAddress, amount):
		path = '/v1/service-tokens/' + contract_id + '/mint'
		API.refresh_request(self, is_json=True)

		request_body = sorted({
			'ownerAddress': ownerAddress,
			'ownerSecret': ownerSecret,
			'toAddress': toAddress,
			'amount': amount
		})
		API.get_signature(self, 'POST', path, body=request_body)
		return requests.post(self.url + path, headers=self.headers, json=str(request_body)).json()

	# UserWalletでサービストークンを焼却
	def POST_v1_service_tokens_burn(self, contract_id, ownerAddress, ownerSecret, fromAddress, amount):
		path = '/v1/service-tokens/' + contract_id + '/burn-from'
		API.refresh_request(self, is_json=True)

		request_body = sorted({
			'ownerAddress': ownerAddress,
			'ownerSecret': ownerSecret,
			'fromAddress': fromAddress,
			'amount': amount
		})
		API.get_signature(self, 'POST', path, body=request_body)
		return requests.post(self.url + path, headers=self.headers, json=str(request_body)).json()

	# サービストークンの保有者一覧を取得
	def GET_v1_service_tokens_holders(self, contract_id):
		path = '/v1/service-tokens/' + contract_id + '/holders'
		API.refresh_request(self)

		query_params = sorted({
			'limit': 10,
			'orderBy': 'desc',
			'page': 1
		}.items())
		API.get_signature(self, 'POST', path, params=query_params)
		return requests.post(self.url + path, headers=self.headers).json()
