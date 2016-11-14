## GNUPLOT command file
set terminal png truecolor medium size 800,800 crop
set style data lines
set title 'Threshold Plot for Embrace Event'
set xlabel 'Detection Score'
set grid
set size ratio 0.85
plot [0.101000:0.996000]  \
  'x.det.Embrace_Event.dat.1' using 1:4 title 'PMiss' with lines lt 2, \
  'x.det.Embrace_Event.dat.1' using 1:5 title 'RFA' with lines lt 3, \
  'x.det.Embrace_Event.dat.1' using 1:6 title 'DCR' with lines lt 4, \
  'x.det.Embrace_Event.dat.2' using 1:2 title 'Min DCR 0.076, scr 0.343' with points lt 6