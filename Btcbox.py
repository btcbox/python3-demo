#!/usr/bin/python
# -**- coding:utf8 -**-

import time
import configparser
import requests
import locale
import json
import hashlib
import hmac

class Btcbox():

    def __init__(self):

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.base = config.get("DEEP", 'base')
        self.symbol = config.get("DEEP", 'coin')

        self.sec = config.get("DEEP", 'sec')
        self.key = config.get("DEEP", 'key')

        self.symobl_coin = self.symbol.upper() + "/JPY"

        print(self.symobl_coin)
        
    def nonce(self):
        return str(int(time.time()*1000))

    def signature(self, param_dic):
        msg = ''
        for index,(k, v) in enumerate(param_dic.items()) :
            msg += str(k) + "=" + str(v)
            if index < len(list(param_dic.keys())) - 1:
                msg += '&'

        s = bytes(msg,'utf8')
        api_secret_md5 =hashlib.md5(self.sec.encode()).hexdigest()
        secret = bytes(api_secret_md5,'utf8')
        return hmac.new(secret, s, digestmod=hashlib.sha256).hexdigest()
    
    def base_dic_sig(self):

        return {'key' : self.key, 'nonce':self.nonce()}
        

    # 1.1. Ticker Public
    def ticker(self):
        
        url = self.base + '/api/v1/ticker/?coin=' + self.symbol
        r = requests.get(url).json()
        self.price = (r["buy"] + r["sell"])/2
        print('ticker\nurl: %s\nresult: %s \nprice: %d \n---------------' %(url ,  json.dumps(r),self.price))
        
    # 1.2 Depth Public
    def deep(self):
        
        url = self.base + '/api/v1/depth/?coin=' + self.symbol
        r = requests.get(url).json()
        print("deep\nurl: %s \ndeep:%s \n---------------" % (url, json.dumps(r)))

    # 1.3 Orders Public
    def orders(self):
        url = self.base + '/api/v1/orders?coin=' + self.symbol
        r = requests.get(url).json()
        print("orders\nurl: %s \nresult: %s\n---------------" % (url, json.dumps(r)))

    # 1.4 balance
    def balance(self):

        url = self.base + '/api/v1/balance'
        param = self.base_dic_sig()
        param["signature"] = self.signature(param)
        r = requests.post(url, param).json()
        print('1.4 balance \nurl: %s \nresult:%s \n---------------' %(url,json.dumps(r)))
    
    # 1.5 Wallet
    def wallet(self):

        url = self.base + '/api/v1/wallet?coin=' + self.symbol
        param = self.base_dic_sig()
        param["signature"] = self.signature(param)
        r = requests.post(url, param).json()
        print("1.5 Wallet url: %s \nresult: %s \n---------------"  % (url, r))

    # 1.6 trade_list
    def trade_list(self):

        url = self.base + '/api/v1/trade_list'
        param = self.base_dic_sig()
        param["signature"] = self.signature(param)
        r = requests.post(url, param).json()
        
        print('1.6 trade_list \nurl: %s \nresult:%s \n---------------' %(url,json.dumps(r)))
            

     # 1.7. Trade_view
    def trade_view(self,order_id):

        url = self.base + '/api/v1/trade_view'
        param = self.base_dic_sig()

        param["id"] = order_id
        param["signature"] = self.signature(param)
        r = requests.post(url, param).json()

        print("1.7 Trade_view \nurl: %s \nresult: %s \n---------------" % (url,r))
       
    # 1.8. Trade_cancel
    def trade_cancel(self, order_id):

        url = self.base + '/api/v1/trade_cancel'
        param = self.base_dic_sig()

        param["id"] = order_id
        param["signature"] = self.signature(param)
        r = requests.post(url, param).json()
        print("1.8 trade_cancel \nurl: %s \nresult: %s \n---------------" % (url,r))

    # 1.9. Trade_add
    def trade_add(self,direction,amount,price):

        url = self.base + '/api/v1/trade_add'
        param = self.base_dic_sig()

        param["amount"] = amount
        param["coin"] = self.symbol
        param["type"] = direction
        param["price"] = price
        param["signature"] = self.signature(param)
        r = requests.post(url, param).json()
        print("1.9 trade_add \nurl: %s \nresult: %s \n---------------" %(url,r))

    

if __name__ == "__main__":

    box = Btcbox()
    
    try:

        # 1.1. Ticker
        box.ticker()
        # 1.2. Depth
        box.deep()
        # 1.3 orders
        box.orders()
        # 1.4 balance
        box.balance()
        # 1.5 wallet
        box.wallet()
        # 1.6 trade_list
        box.trade_list()
        
        # 1.7 trade_view
        box.trade_view('889554')
        # 1.8 trade_cancel
        box.trade_cancel('889554')

        # 1.9 Trade_add
        box.trade_add('buy', 0.001,box.price)

    except Exception as e:
        print("error：" + str(e))