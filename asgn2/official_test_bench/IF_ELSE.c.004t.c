#include <stdio.h>
int main ()
{
  int D1732;
  int D1736;
  int i;
  int j;
  int sum;

  j = 1;
  sum = 0;
  i = 0;
  j = 1;
  goto D1728;
  D1727:
  {

    D1732 = j % 10;
    if (D1732 == 0) goto D1733; else goto D1734;
    D1733:
    printf ("%d", j);
    goto D1735;
    D1734:
    sum = sum + i;
  }
  D1735:
  i = i + 1;
  j = i * 2;
  D1728:
  if (i <= 99) goto D1727; else goto D1729;
  D1729:
  printf ("%d", sum);
  D1736 = 0;
  return D1736;
}


