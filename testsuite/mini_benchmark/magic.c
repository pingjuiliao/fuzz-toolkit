#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv) {
  int r = 0;
  char  *s = NULL;
  char buf[0x100];
  
  memset(buf, 0, sizeof(buf));
  s = fgets(buf, sizeof(buf), stdin);
  if (s == NULL) {
     fprintf(stderr, "fgets() error");
     exit(-1);
  }
  if (strcmp(s, "ABCD") == 0) {
    __builtin_trap();
  }
  return 0;
}
