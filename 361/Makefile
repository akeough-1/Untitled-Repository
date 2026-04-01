a.out: lib/libpoint.so rectangle.o
	gcc main.c rectangle.o -Isrc -Llib -libpoint -lm

rectangle.o:
	gcc -c src/rectangle.c -o rectangle.o

lib/libpoint.so:
	gcc -c -shared src/point.c -o lib/libpoint.so

clean:
	rm lib/libpoint.so *.o a.out