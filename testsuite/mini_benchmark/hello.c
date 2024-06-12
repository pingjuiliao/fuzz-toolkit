#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void bug(void) {
  int* addr = (int *) 0xdeadbeef;
  *addr = 1337;
}


int main(int argc, char** argv) {
  int r = 0;
  char *s = NULL;
  char buf[0x100];

  memset(buf, 0, sizeof(buf));
  s = fgets(buf, sizeof(buf), stdin);
  if (s == NULL) {
    fprintf(stderr, "fgets() error");
    exit(-1);    
  }

  if (s[0] == 'h' && s[1] == 'e' && s[2] == 'l' &&
      s[3] == 'l' && s[4] == 'o') {
    bug();
  }

  return 0;
}
