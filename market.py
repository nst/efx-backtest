#!/usr/bin/env python

# input: price list
# action: send prices to strategies, gets orders
# output: chartable data and stats

from strategy import *
from price import *
import datetime
import sys

DEBUG = False
HEATMAP = False

# http://www.fxhistoricaldata.com/
def price_from_line(line):
    if line.startswith('<'):
        return None
	
    (currency, date_string, time_string, open_string, low_string, high_string, close_string) = line.split(',')

    dt = "%s %s" % (date_string, time_string)

    timestamp = datetime.datetime.strptime(dt, "%Y%m%d %H:%M:%S")
    
    open = float(open_string)
    low = float(low_string)
    high = float(high_string)
    close = float(close_string)
    
    return Price(timestamp, open, low, high, close)

def pretty_timestamp(ts):
    return ts.strftime("%Y%m%d_%H%M%S")

def run_simulation():
	path = "EURUSD_day.csv"
	
	pnl = 0.0
	equity = 0.0
	prices_count = 0
	max_exposure = 0
	current_price = None
	
	f = open('histories/' + path)
	
	strategies = []
	
	a = None
	
	for sl_tp_delta in range(200, 300):
		s = Strategy(sl_tp_delta)
		strategies.append(s)
	
	if HEATMAP:
		pass
	else:
		sltp = 78
		strategies = strategies[sltp:sltp+1]
	
	for line in f.xreadlines():
		p = price_from_line(line)
		if not p:
			continue
		prices_count += 1
		
		if DEBUG:
			print p
		
		for s in strategies:
		
			a = s.account
		
			a.execute_orders_with_price_change(p)
	
			o = s.order_for_price(p)
			if o:
				a.add_order(o)
				#print o
		
			max_exposure = max(a.exposure(), max_exposure)
			
			if HEATMAP:
				print a.pnl_realized() + a.pnl_unrealized_with_price(p), # heatmap
			else:
				print "%s\t%s\t%s" % (pretty_timestamp(p.timestamp), p.close, a.pnl_realized() + a.pnl_unrealized_with_price(p))
		
		if HEATMAP:
			print ""
	
	if not HEATMAP:
		a = strategies[0].account
		
		sys.stderr.write("number of prices : %d\n" % prices_count)
		sys.stderr.write("number of trades : %s (%d win, %d lose)\n" % (a.trades_count(), a.win_count, a.lose_count))
		sys.stderr.write("max_exposure     : %f\n" % max_exposure)
		sys.stderr.write("realized pnl     : %f\n" % a.pnl_realized())
		sys.stderr.write("unrealized pnl   : %f\n" % a.pnl_unrealized_with_price(p))

if __name__=='__main__':
    run_simulation()
