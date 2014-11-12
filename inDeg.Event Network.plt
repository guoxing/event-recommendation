#
# Event Network Degree. G(15897435, 30279252). 1478048 (0.0930) nodes with in-deg > avg deg (3.8), 502722 (0.0316) with >2*avg.deg (Wed Nov 12 13:35:10 2014)
# 

set title "Network Degree G(15897435, 30279252)"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Degree"
set ylabel "Count"
set tics scale 2
set terminal png size 1000,800
set output 'inDeg.Event Network.png'
plot 	"inDeg.Event Network.tab" using 1:2 title "" with linespoints pt 6
