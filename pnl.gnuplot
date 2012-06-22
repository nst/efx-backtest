set terminal png

set title "EUR_USD and PnL, spread 1.8 pips"

set format x "%Y%m%d_%H%M%S"

set xdata time
set timefmt "%Y%m%d_%H%M%S"

set grid

set output "pnl.png"

set format x ""

set lmargin 9
set rmargin 2

set multiplot
set size 1.0, 0.7
set origin 0, 0.3
set bmargin 0

plot "pnl.txt" using 1:2 notitle with lines

#set xlabel "Columbia infAP"
#set ylabel "IICT infAP"
#set nokey
#set xtics 2
#set title "Semi-log scaling"
#set yrange [75:105]
#set ytics (105, 100, 95, 90, 85, 80)
#set xrange [50:253]
#set lmargin 9
#set rmargin 2
#set grid
#set logscale y
#set title "Mean of 5 most similar transactions (percent)"
#plot "plot.txt" with lines
#set output "fx.png"
#set title "Mean of 5 most similar transactions (percent)"
#plot "fx_found.txt" using 1:2 with lines
#plot "fx_found.txt" with lines


unset label 1
unset label 2
unset title
set bmargin
set format x
set size 1.0, 0.3
set origin 0.0, 0.0
set tmargin 0

#set xtics ("6/03" 66, "7/03" 87, "8/03" 109, "9/03" 130, "10/03" 151, "11/03" 174, "12/03" 193, "1/04" 215, "2/04" 235)

#set autoscale y

plot 'pnl.txt' using 1:3 notitle with impulses lt 3
unset multiplot
