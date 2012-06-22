#!/usr/bin/python

class Account:
    
    def __init__(self):
        self.orders = []
        self.win_count = 0
        self.lose_count = 0
        
    def add_order(self, o):
        self.orders.append(o)
    
    def execute_orders_with_price_change(self, p):
        
        for o in self.orders:

            if o.status == "closed":
                continue
            
            elif o.status is None:
                if o.price >= p.low and o.price <= p.high:
                    o.open(p.timestamp)
            
            elif o.status == "opened":
                
                if p.contains_price(o.stop_loss):
                    o.close(p.timestamp, o.stop_loss)
                    self.lose_count += 1
                elif p.contains_price(o.take_profit):
                    o.close(p.timestamp, o.take_profit)
                    self.win_count += 1
                
                elif o.buy_or_sell == "BUY":
                    if p.low <= o.stop_loss:
                        o.close(p.timestamp, o.stop_loss)
                        self.lose_count += 1
                    elif p.high >= o.take_profit:
                        o.close(p.timestamp, o.take_profit)
                        self.win_count += 1
                
                elif o.buy_or_sell == "SELL":
                    if p.high >= o.stop_loss:
                        o.close(p.timestamp, o.stop_loss)
                        self.lose_count += 1
                    elif p.low <= o.take_profit:
                        o.close(p.timestamp, o.take_profit)
                        self.win_count += 1
    
    def exposure(self):
        opened_orders = filter(lambda o:o.status == "opened", self.orders)
        return sum(map(lambda o:o.amount, opened_orders))

    def pnl_realized(self):
        n = 0.0
        for o in filter(lambda o:o.status == "closed", self.orders):
            n += o.pnl()
        return n
	
    def pnl_unrealized_with_price(self, price):
        n = 0.0

        for o in self.opened_orders():
            if o.buy_or_sell == "BUY":
                n += o.price - price.close
            elif o.buy_or_sell == "SELL":
                n += price.close - o.price
            else:
                print "--", o.buy_or_sell
                raise Exception

        return n * 10000
   
    def trades_count(self):
        return len(filter(lambda o:o.status != None, self.orders))
    
    def opened_orders(self):
        return filter(lambda o:o.status == "opened", self.orders)
    
    def closed_orders(self):
        return filter(lambda o:o.status == "closed", self.orders)
    
    def opened_or_closed_orders(self):
        return filter(lambda o:o.status == "opened" or o.status == "closed", self.orders)
    
    def latest_closed_order(self):
    	l = self.closed_orders()
    	return l[-1] if len(l) > 0 else None
    
    
    
