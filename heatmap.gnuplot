set terminal png
set output "heatmap.png"

set title "EUR/USD: PnL since 2001 following daily trend, SL/TP at X+200"

unset key
set tic scale 0

#set palette rgbformula -7,2,-7
#set palette color
set palette negative
set palette defined

#set ticslevel 0
#set cbtics scale 1000

#show palette gradient

set cbrange [-6000:6000]
#set cblabel "PnL"
#unset cbtics

set xrange [0:99.5]
set yrange [0:1118]

set view map

splot 'map.txt' matrix with image
