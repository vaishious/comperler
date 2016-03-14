#include <stdio.h>
int main ()
{
  const char * D2055;
  int i;
  int j;
  int k;
  int res;

  res = 0;
  i = 0;
  goto D2052;
  D2051:
  j = 0;
  goto D2049;
  D2048:
  k = 0;
  goto D2046;
  D2045:
  res = res + 1;
  k = k + 1;
  D2046:
  if (k <= 9) goto D2045; else goto D2047;
  D2047:
  j = j + 1;
  D2049:
  if (j <= 9) goto D2048; else goto D2050;
  D2050:
  i = i + 1;
  D2052:
  if (i <= 9) goto D2051; else goto D2053;
  D2053:
  D2055 = (const char *) &"res = %d\n"[0];
  printf (D2055, res);
}


