
set xlabel "time[s]"
set ylabel "Throughput[Mbps]"
set key bel
plot  "tcp1.tr" u ($1):($2) t "TCP1" w lp, "tcp2.tr" u ($1):($2) t "TCP2" w lp

set term png
set output "TCPThroughput.png"
replot

pause -1