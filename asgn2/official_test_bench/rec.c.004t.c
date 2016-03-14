#include <stdio.h>
int g = 10;
void myfunc();

int main()
{
  myfunc();
}


void myfunc()
{
  int g0;
  int g1;
  const char * D2049;
  int g2;
  int g3;

  g0 = g;
  if (g0 == 0) goto D2046; else goto D2047;
  D2046:
  return;
  D2047:
  g1 = g;
  D2049 = (const char *) &"value of g is %d\n"[0];
  printf (D2049, g1);
  g2 = g;
  g3 = g2 - 1;
  g = g3;
  myfunc();
}


