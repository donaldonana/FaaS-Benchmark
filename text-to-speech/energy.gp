set terminal png size 400,350
set output 'energy_plot.png'

set boxwidth 0.7    
set style fill solid

set title "Mean Energy by Schema"
set xlabel "Variants"
set ylabel "Mean Energy (j)"

set style data histograms
set style histogram cluster gap 1
set datafile separator '\t'


set grid ytics mytics  # draw lines for each ytics and mytics
set mytics 2           # set the spacing for the mytics
set grid  


unset key 
set yrange [0:*]  # <-- ensures y-axis starts at 0

plot 'energy_data.dat' using 2:xtic(1) title 'Mean Energy'
