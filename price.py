#!/usr/bin/python

class Price:
    
    def __init__(self, timestamp, open, low, high, close):
        self.timestamp = timestamp;
        self.open = open
        self.low = low
        self.high = high
        self.close = close
    
    def __str__(self):
        return "<Price> %s - %s %s %s" % (self.timestamp.strftime("%Y-%m-%d"), self.open, self.low, self.high, self.close)
    
    def contains_price(self, value):
        return value <= self.high and value >= self.high
    