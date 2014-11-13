#
# user network degree. G(683240, 1187518). 98529 (0.1442) nodes with in-deg > avg deg (3.5), 62105 (0.0909) with >2*avg.deg (Thu Nov 13 00:47:24 2014)
#

set title "User Network Degree. G(683240, 1187518)"
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
set output 'inDeg.user_network.png'
plot 	"inDeg.user_network.tab" using 1:2 title "" with linespoints pt 6
