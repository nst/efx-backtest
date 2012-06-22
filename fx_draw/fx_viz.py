#!/usr/bin/python

import datetime
import sys
from datetime import date
import Image,ImageDraw
import math

class Price:
    
    def __init__(self, timestamp, open, low, high, close):
        self.timestamp = timestamp;
        self.open = open
        self.low = low
        self.high = high
        self.close = close
    
    def __str__(self):
        return "<Price> %s - %f %f %f %f" % (self.timestamp.strftime("%Y-%m-%d"), self.open, self.low, self.high, self.close)
    
    def var_delta(self, p0):
    
        if not p0:
            return 0.0
        
        return 1.0 - self.open / p0.open

    def var_volatility(self, p0):
        if not p0:
            return 0.0

        return self.high - self.low

    def var_min_pips(self, p0, pips):
        if not p0:
            return 0.0
        
        var = self.open - p0.open
        if abs(var) > (pips / 1000.0):
            return var
        else:
            return 0.0
        
    def color_since(self, p0):
        var = self.var_delta(p0) * 2
        #var = self.var_volatility(p0)
        #var = self.var_min_pips(p0, 4)

        var_norm = abs(var)

        intensity = int(var_norm * 50000)
        
        if intensity > 255:
            intensity = 255
            
        color = ("white")
        
        if var > 0.0:
            color = (0,intensity,0)
        else:
            color = (intensity,0,0)
    
        return color

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

path = "EURCHF_hour.csv"
prices = []

f = open(path)

for line in f.xreadlines():
    p = price_from_line(line)
    if p:
        prices.append(p)

#print len(prices)

#datetime.date(2010, 6, 16)

current_week_number = None

weeks = []

for p in prices:    
    week_number = p.timestamp.isocalendar()[1]
    
    if len(weeks) == 0 or week_number != current_week_number:
        weeks.append([])
        current_week_number = week_number
    
    weeks[-1].append(p)

nb_weeks = len(weeks)

print "-- nb_weeks:", len(weeks)

# draw

img = Image.new("RGB", (24 * 5 - 1, nb_weeks), "black")
draw = ImageDraw.Draw(img)

p0 = None

#var_min = 100
#var_max = -100

#vars_per_weekdayhour = []
#for i in range(24 * 5 - 1):
#    vars_per_weekdayhour.append([])

for i in range(len(weeks)):
    prices = weeks[i]

    for p in prices:
        color = p.color_since(p0)
    
        #var = p.var_volatility(p0)  
        
        p0 = p

        day_index = p.timestamp.weekday()
        week_number = p.timestamp.isocalendar()[1]
        year = p.timestamp.year
        # print year, week_number, day_index
        
        #print vars_per_weekday[day_index]
        
        x = day_index * 24 + p.timestamp.hour

        #vars_per_weekdayhour[x].append(var)
        
        draw.point((x,i), fill=color)

img.save("eur_chf_weekly.png", "PNG")

#for i in range(len(vars_per_weekdayhour)):
#    vars = vars_per_weekdayhour[i]
#    
#    if len(vars) == 0:
#        print "-- error, len(vars) == 0"
#        continue
#    print "%d \t %d \t %.5f" % (i / 24, i % 24, 1000 * sum(vars) / len(vars))


#print var_min * 10000
#print var_max * 10000
