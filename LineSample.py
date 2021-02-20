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

# ========================================================
# API設定
# ========================================================
line_server = 'https://test-api.blockchain.line.me'
line_api_key = ''
line_secret_key = ''

def get_nonce():
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

def get_signature(method, path, nonce, timestamp, params = {}):
	signStr = nonce + str(timestamp) + method + path

	isFirst = True
	for key, value in params.items():
		if isFirst:
			signStr += '?'
		else:
			signStr += '&'

		signStr += key + '=' + value
		isFirst = False

	hashStr = hmac.new(bytes(line_secret_key, 'UTF-8'), bytes(signStr, 'UTF-8'), hashlib.sha512).hexdigest()
	print('signStr = ' + signStr)
	print('hashStr = ' + hashStr)
	print('base64  = ' + str(base64.b64encode(hashStr.encode())))
	return base64.b64encode(hashStr.encode())

def GET_v1_service_tokens():
    path = '/v1/service-tokens'
    nonce = get_nonce()
    timestamp = int(round(time.time() * 1000))
    signature = get_signature('GET', path, nonce, timestamp, {})
    print('path = ' + path)
    print('nonce = ' + nonce)
    print('timestamp = ' + str(timestamp))

    headers = {
        'service-api-key': line_api_key,
        'nonce': nonce,
        'timestamp': str(timestamp),
        'signature': signature
    }

    res = requests.get(line_server + path, headers=headers)
    return res.json()

print(GET_v1_service_tokens())
