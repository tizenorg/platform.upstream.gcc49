/* { dg-do compile } */
/* { dg-options "-save-temps -O2" } */

#define VALUE 0xc521974f

int
foo (int *p, int *q)
{
  p[0] = VALUE;
  q[0] = VALUE;
}

/* { dg-final { scan-assembler-times "mov\\tw2, 38735" 1 } } */
/* { dg-final { scan-assembler-times "movk\\tw2, 0xc521, lsl 16" 1 } } */
/* { dg-final { cleanup-saved-temps } } */
