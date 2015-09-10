/* { dg-do compile } */
/* { dg-options "-save-temps -O2" } */

int
foo (int a, int b)
{
  int i = 0;
  int x, y;
  for (; i < (1UL << 20); ++i)
    {
      x = 0x12345678;
      y = 0xDEADBEEF;
      a += (a * x) + (b * y);
    }
  return a;
}

/* { dg-final { scan-assembler "movk\\tw4, 0x1234, lsl 16\\n\\tmul\\tw1, w1, w2\\n\\tmov\\tw2, 1048576\\n\.L2:\\n"  } } */
/* { dg-final { cleanup-saved-temps } } */
