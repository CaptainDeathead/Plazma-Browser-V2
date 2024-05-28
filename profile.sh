python3 -m cProfile -o main.pstats main.py
unset GTK_PATH
gprof2dot -f pstats main.pstats | dot -Tpng -o output.png && eog output.png