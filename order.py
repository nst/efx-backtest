#!/usr/bin/python

import datetime

DEBUG = False

SPREAD = 1.8

class Order:
    
    def __init__(self, BUY_OR_SELL, amount, price, stop_loss_pips, take_profit_pips):
        if BUY_OR_SELL not in ("BUY", "SELL"):
            raise AttributeError

        if not amount > 0:
            raise AttributeError

        if not price > 0:
            raise AttributeError
        
        sl_tp_modifier = 1 if BUY_OR_SELL == "BUY" else -1
        
        self.buy_or_sell = BUY_OR_SELL
        self.amount = amount
        self.price = price
        self.stop_loss = price - (stop_loss_pips / 10000.0) * sl_tp_modifier
        self.take_profit = price + (take_profit_pips / 10000.0) * sl_tp_modifier
        self.status = None # None, "opened", "closed"
        self.pips = 0.0
        self.timestamp_open = None
        self.timestamp_close = None
    
    def __str__(self):
        s = "<Order> [%s - %s] (%s) %s %s %s (SL:%s TP:%s)" % (self.timestamp_open, self.timestamp_close, self.status, self.buy_or_sell, self.amount, self.price, self.stop_loss, self.take_profit)
        if self.status == "closed":
            s +=  "\t %s" % self.pnl()
        return s
    
    def open(self, timestamp):
        self.status = "opened"
        self.pips = SPREAD * -1
        self.timestamp_open = timestamp + datetime.timedelta(microseconds=1)
        
        if DEBUG:
            print "\t\t\t  OPEN", self
    
    def close(self, timestamp, close_price_value):
        self.status = "closed"
        
        self.timestamp_close = timestamp # in fact it will be shorter be we miss st / tp prices
        
        if self.buy_or_sell == "BUY":
            if close_price_value >= self.take_profit:
                self.pips += (self.take_profit - self.price) * 10000
            elif close_price_value <= self.stop_loss:
                self.pips -= (self.price - self.stop_loss) * 10000
            else:
                raise Exception

        elif self.buy_or_sell == "SELL":
            if close_price_value <= self.take_profit:
                self.pips += (self.price - self.take_profit) * 10000
            elif close_price_value >= self.stop_loss:
                self.pips -= (self.stop_loss - self.price) * 10000
            else:
                raise Exception
        
        else:
            raise Exception

        if DEBUG:
            print "\t\t\t CLOSE", self
        
    def pnl(self):
        return self.pips * (self.amount / 10000)
    