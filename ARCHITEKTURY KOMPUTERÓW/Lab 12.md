# [[Instrukcja + wytlumaczenie]]

```

#include <stdio.h>
#include <math.h>
#include "eval_time.h"

//Rozmiar glownych macierzy
#define SIZE 2000

//Rozmiar bloku alg. blokowego
#define nb 4

static double a[SIZE*SIZE];
static double b[SIZE*SIZE];
static double c[SIZE*SIZE];
static double d[SIZE*SIZE];

void dgemm_naive(int,double*,double*,double*);
void dgemm_blocked(int,double*,double*,double*);

void block(int,int,int,int,double*,double*,double*);

//-------------------------------------------------------------------------------

int main(void)
{

unsigned int i,j,n;
unsigned long f;
double time_tabl[3];

n=SIZE;

//Liczba operacji zmiennoprzecinkowych:
f=2*(unsigned long)n*(unsigned long)n*(unsigned long)n;

//-------------------------------------------------------------------------------
// INIT - wypelnienie tablic a i b wartosciami poczatkowymi, 

for (i=0;i<n;++i)
    for (j=0;j<n;++j)
    {
	a[j+i*n]=(double)(i+j*n);
	b[j+i*n]=(double)(j+i*n);
    }

// tablice c i d zostaw wyzerowane.

//-------------------------------------------------------------------------------

init_time();
dgemm_blocked(n,a,b,c);
read_time(time_tabl);

printf("blocked     = %lf s\n",time_tabl[1]);
printf("GFLOPS      = %lf\n\n",(double)f/time_tabl[1]*1.0e-9);

//-------------------------------------------------------------------------------

init_time();
dgemm_naive(n,a,b,d);
read_time(time_tabl);

printf("naive       = %lf s\n",time_tabl[1]);
printf("GFLOPS      = %lf\n\n",(double)f/time_tabl[1]*1.0e-9);

//-------------------------------------------------------------------------------
// TEST poprawnosci mnozenia - sprawdzenie czy oba algorytmy daly ten sam wynik.

for (i=0;i<SIZE*SIZE;++i) 
    if (fabs(c[i]-d[i])>1.0e-9) {printf("Error!\n"); goto rtrn;}

rtrn:
return(0);
}

//-------------------------------------------------------------------------------

void dgemm_naive(int n, double* A, double* B, double* C)
{
register int i,j,k;
register double cij;

for(i=0;i<n;++i)
    for(j=0;j<n;++j)
    {
	cij=C[i+j*n]; 			// cij = C[i][j]
	for(k=0;k<n;++k)
	    cij+=A[i+k*n]*B[k+j*n]; 	// cij += A[i][k]*B[k][j]
	C[i+j*n]=cij; 			// C[i][j] = cij
    }
}

//-------------------------------------------------------------------------------

void dgemm_blocked(int n, double* A, double* B, double* C)
{
register int bi,bj,bk;

for(bi=0;bi<n;bi+=nb)
    for(bj=0;bj<n;bj+=nb)
	for(bk=0;bk<n;bk+=nb)
	    block(n,bi,bj,bk,A,B,C);
}

void block(int n, int bi, int bj, int bk, double *A, double *B, double *C)
{

register int i,j,k;
register double cij;

for(i=bi;i<bi+nb;++i)
    for(j=bj;j<bj+nb;++j)
    {
	cij=C[i+j*n];
	for(k=bk;k<bk+nb;++k)
	    cij+=A[i+k*n]*B[k+j*n];
	C[i+j*n]=cij;
    }
}

//-------------------------------------------------------------------------------
```