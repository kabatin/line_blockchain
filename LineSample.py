#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ========================================================
# import設定
# ========================================================
import requests, time, json, random, string
import hmac, hashlib, base64
import LineBlockchainLib

# API定義
APIKey = ''
SecretKey = ''
IsDistribution = False

lbl = LineBlockchainLib.API(APIKey, SecretKey, IsDistribution)
print(lbl.GET_v1_time())
print('---------------------------------------')
print(lbl.GET_v1_services('ServiceId'))
print('---------------------------------------')
print(lbl.GET_v1_service_tokens())
print('---------------------------------------')
print(lbl.GET_v1_service_tokens_by_contract_id('ContractId'))
print('---------------------------------------')
print(lbl.PUT_v1_service_tokens_update('ContractId', 'Name', 'Meta', 'OwnerAddress', 'OwnerSecret'))
print('---------------------------------------')
print(lbl.POST_v1_service_tokens_mint('ContractId', 'OwnerAddress', 'OwnerSecret', 'ToAddress', 'Amount'))
print('---------------------------------------')
print(lbl.POST_v1_service_tokens_burn('ContractId', 'OwnerAddress', 'OwnerSecret', 'FromAddress', 'Amount'))
print('---------------------------------------')
print(lbl.GET_v1_service_tokens_holders('ContractId'))
print('---------------------------------------')
