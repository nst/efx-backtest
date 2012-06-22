#!/usr/bin/python

from order import *
from account import *

class Strategy:
    
    def __init__(self, sl_tp_delta=200):
        self.account = Account()
        self.prices = []
        self.sl_tp_delta = sl_tp_delta
    
    def order_for_price(self, p):
        o = None
        
        if p == None:
            return None
        
        #sl_tp_delta = 200 # pips
        sl_tp = self.sl_tp_delta
        
        previous_price = self.prices[-1] if len(self.prices) > 0 else None
        if previous_price == None:
            o = Order("BUY", 10000, p.close, sl_tp, sl_tp) # first trade
            
        self.prices.append(p)
        
        if o:
            o.open(p.timestamp) # market order..
            return o

        if self.account.exposure() >= 10000:
            return None
        
        if p.close >= previous_price.close:
            o = Order("SELL", 10000, p.close, sl_tp, sl_tp)
        elif p.close <= previous_price.close:
            o = Order("BUY", 10000, p.close, sl_tp, sl_tp)
        else:
            raise Exception

        if o:
            o.open(p.timestamp) # market order..
            return o

        return None
