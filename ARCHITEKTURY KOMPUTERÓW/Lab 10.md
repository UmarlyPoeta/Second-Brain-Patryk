.section .note.GNU-stack, "", @progbits
.globl	main

# Liczba sumowanych par (+ i -) elementow.

.equ	N , 1000
.equ	NF, N * 6

.data

nfop:		.quad	NF
ndiv:		.double 0.000000001
timetab:	.double	0.0, 0.0, 0.0
cw:		.word		0
str1:		.string	" PI_ref =\t%1.20Lf\n PI_com =\t%1.20Lf\n delta  =\t%1.20Lf\n"
str2:		.string	"USER CPU TIME = %lf s\nGFLOPS = %2.2lf\n"

.text

main:

sub	$8 , %rsp

# Rozpocznij pomiar czasu.

call	init_time

mov	$N , %rcx

finit

# 1) Ustaw odpowiednia precyzje obliczen oraz sposob zaokraglania.
# p: 0 - single, 2 - double, 3 - extended

fstcw	cw(%rip)
andw	$0xf0ff , cw(%rip)
orw	$0x0p00 , cw(%rip)
fldcw	cw(%rip)


# Obliczanie wartosci PI:
#
# +(1/1) - (1/3) + (1/5) - (1/7) + (1/9) + ... => PI/4
#

# 2) Nadaj rejestrom FPU wartosci poczatkowe.

fld1
fadd	%st(0) , %st(0)
fldz
fld1

# st(2) - stala = 2
# st(1) - suma = 0
# st(0) - mianownik = 1

for:

# 3a) Oblicz pierwszy element (dodatni).

fld1
fdiv	%st(1) , %st(0)		# st(0) = st(0)/st(1) = 1/m
faddp	%st(2)			# st(1) = suma + 1/m
fadd	%st(2) , %st(0)		# st(0) = m + 2

# 3b) Analogicznie oblicz drugi element (i odejmij go od sumy).

# ...

dec	%rcx
jnz	for

# 4) Wynik *=4

fxch	%st(1)
fadd	%st(0) , %st(0)
fadd	%st(0) , %st(0)

# Roznica miedzy wartoscia obliczona w %st(0) a "dokladna" PI.

fldpi
fsub	%st(1) , %st(0)
fabs

# Wrzuc wszystko na stos CPU.

sub	$16 , %rsp
fstpt	(%rsp)

sub	$16 , %rsp
fstpt	(%rsp)

fldpi
sub	$16 , %rsp
fstpt	(%rsp)

# Zakoncz pomiar czasu.

lea	timetab(%rip) , %rdi
call	read_time

# Wydrukuj obliczone wartosci, zmierzony czas i wydajnosc obliczen.

lea	str1(%rip) , %rdi
xor	%eax , %eax
call	printf

lea	str2(%rip) , %rdi
movsd	timetab+8(%rip) , %xmm0

mov	nfop(%rip) , %rax
cvtsi2sd	%rax , %xmm1
divsd	%xmm0 , %xmm1
movsd	ndiv(%rip) , %xmm2
mulsd	%xmm2 , %xmm1

mov	$2 , %eax
call	printf

add	$56 , %rsp
ret