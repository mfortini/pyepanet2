all: _epanet2.so

epanet2_wrap.c: epanet2.i
	swig -python epanet2.i

_epanet2.so: epanet2_wrap.c
	gcc -O2 -c epanet2_wrap.c -fPIC -I /usr/include/python2.7
	ld -shared epanet2_wrap.o -o _epanet2.so /usr/local/lib/libepanet2.a


clean:
	rm -f _epanet2.so
	rm -f epanet2_wrap.c
	rm -f epanet2.py
