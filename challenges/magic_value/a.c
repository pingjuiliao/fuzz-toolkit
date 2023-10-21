#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char** argv) {
  char buf[20];
  int r = read(0, buf, 20);
  if (r == 0) {
    exit(-1);
  }
  if (strncmp(buf, "ABCD", 4) == 0) {
    __builtin_trap();
  }

  return 0;
}
