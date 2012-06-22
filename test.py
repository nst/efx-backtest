import unittest

from strategy import *
from price import *
from order import *
from account import *

import datetime

t = datetime.datetime.now()

def to_date(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")

def pips_to_pnl(pips, amount, pips_precision=4):
    return (1.0 / pow(10, pips_precision)) * pips * amount

class Testpnl(unittest.TestCase):

    amount = 10000
    
    def setUp(self):
        pass
    
    def test_pnl(self):
        o = Order("BUY", self.amount, 1.2, 10, 10)
        self.assertTrue(o.status == None)
        
        o.open(t)
        self.assertEqual(o.status, 'opened')
        
        o.close(t, 1.2010) # 10 pips
        self.assertEqual(o.status, 'closed')
        
        actual = o.pnl()
        self.assertAlmostEqual(10 - SPREAD, actual)
        
        raw_pnl = pips_to_pnl(10, self.amount)
        spread_amount = pips_to_pnl(SPREAD, self.amount)
        net_pnl = raw_pnl - spread_amount
        self.assertAlmostEqual(actual, net_pnl)

    def test_buy_sl(self):
        o = Order("BUY", self.amount, 1.2, 15, 20)
        o.open(t)
        o.close(t, 1.0) # -15 pips
        actual = o.pnl()
        self.assertAlmostEqual(-15 - SPREAD, actual)

    def test_buy_tp(self):
        o = Order("BUY", self.amount, 1.2, 15, 20)
        o.open(t)
        o.close(t, 2.0) # +20 pips
        actual = o.pnl()
        self.assertAlmostEqual(+20 - SPREAD, actual)

    def test_sell_sl(self):
        o = Order("SELL", self.amount, 1.2, 15, 20)
        o.open(t)
        o.close(t, 2.0) # -15 pips
        actual = o.pnl()
        self.assertAlmostEqual(-15 - SPREAD, actual)

    def test_sell_tp(self):
        o = Order("SELL", self.amount, 1.2, 15, 20)
        o.open(t)
        o.close(t, 1.0) # +20 pips
        actual = o.pnl()
        self.assertAlmostEqual(20 - SPREAD, actual)

    def test_open_order_no_change(self):
        a = Account()

        ts = datetime.date(2011, 1, 29)
        p = Price(ts, 10, 8, 13, 10)

        o = Order("BUY", 10000, 7.5, 0.1, 0.1)
        a.add_order(o)

        a.execute_orders_with_price_change(p)

        self.assertEqual(o.status, None)

    def test_order_opening(self):
        a = Account()

        ts = datetime.date(2011, 1, 29)
        p = Price(ts, 10, 8, 13, 10)
        
        o = Order("BUY", 10000, 9, 0.1, 0.1)
        a.add_order(o)
        
        a.execute_orders_with_price_change(p)
        
        self.assertEqual(o.status, "opened")

    def test_order_close_loss(self):
        a = Account()

        ts = datetime.date(2011, 1, 29)
        p = Price(ts, 10, 8, 13, 10)
        
        o = Order("BUY", 10000, 9, 1, 1)
        o.open(t)
        a.add_order(o)

        a.execute_orders_with_price_change(p)

        self.assertEqual(o.status, "closed")
        
        self.assertTrue(o.pnl() < 0)

    def test_order_close_win(self):
        a = Account()

        ts = datetime.date(2011, 1, 29)
        p = Price(ts, 10, 8, 15, 10)

        o = Order("BUY", 10000, 9, 100000, 5000)
        o.open(t)
        a.add_order(o)

        a.execute_orders_with_price_change(p)

        self.assertEqual(o.status, "closed")

        self.assertTrue(o.pnl() > 0)

if __name__ == '__main__':
    unittest.main()
