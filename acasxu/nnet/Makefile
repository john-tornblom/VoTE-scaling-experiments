
all: libnnet.so

libnnet.so: nnet.cpp nnet.h
	gcc -fPIC -shared -o libnnet.so nnet.cpp

clean:
	rm libnnet.so
