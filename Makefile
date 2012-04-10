all: _pyepanet2.so

pyepanet2_wrap.c: pyepanet2.i
	swig -python pyepanet2.i

_pyepanet2.so: pyepanet2_wrap.c
	gcc  -c pyepanet2_wrap.c -fPIC -I /usr/include/python2.7
	ld -shared pyepanet2_wrap.o -o _pyepanet2.so /usr/local/lib/libepanet2


