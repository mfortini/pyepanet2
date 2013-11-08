all: _pyepanet2_swig.so

pyepanet2_swig_wrap.c: pyepanet2_swig.i
	swig -python pyepanet2_swig.i

_pyepanet2_swig.so: pyepanet2_swig_wrap.c
	gcc  -c pyepanet2_swig_wrap.c -fPIC -I /usr/include/python2.7
	ld -shared pyepanet2_swig_wrap.o -o _pyepanet2_swig.so /usr/local/lib/libepanet2


clean:
	rm -f _pyepanet2.so
	rm -f pyepanet2_swig_wrap.c
