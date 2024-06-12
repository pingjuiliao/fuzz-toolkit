#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#define STDIN 0

void bug() {
  int* addr = (int *)0xdeadbeef;
  *addr = 1337;
}

int main(int argc, char** argv) {
  int r = 0;
  char buf[0x100];
  uint64_t* magic = (uint64_t*) buf;

  if ((r = read(STDIN, buf, 0x20)) == 0) {
    fprintf(stderr, "read() error");
    exit(-1);
  }

  if (*magic == 0x6867666564636261) {
    bug();
  }
  return 0;
}
