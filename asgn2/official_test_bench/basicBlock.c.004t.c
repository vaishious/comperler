#include <stdio.h>
int main ()
{
  int D1730;
  int D1731;
  int D1732;
  int D1733;
  int D1734;
  int a;
  int b;
  int c;
  int d;
  int eval;

  a = 0;
  b = 10;
  c = 20;
  d = 40;
  D1730 = b / a;
  D1731 = D1730 + a;
  D1732 = d * 2;
  eval = D1731 + D1732;
  D1733 = c * d;
  eval = D1733 + eval;
  printf ("%d", eval);
  D1734 = 0;
  return D1734;
}


