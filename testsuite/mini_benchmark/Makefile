.PHONY=clean

all: hello.exe magic.exe
%.exe: %.c
	$(CC) $(CFLAGS) -o $@ $<
clean:
	rm $(wildcard *.exe)
