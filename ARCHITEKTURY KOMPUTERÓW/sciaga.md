-----------------------------------------------------------

Rejestry (ogolnego przeznaczenia) procesora x86-64:

64bit	32bit	16bit	8bit
			(starszy* i mlodszy bajt)
rax	eax	ax	ah al	accumulator
rbx	ebx	bx	bh bl	base
rcx	ecx	cx	ch cl	counter
rdx	edx	dx	dh dl	data

			(tylko mlodsze 8 bitow)
rdi	edi	di	dil	destination index
rsi	esi	si	sil	source index
rsp	esp	sp	spl	stack pointer (wskaznik-wierzcholek stosu)
rbp	ebp	bp	bpl	base pointer (ramka stosu)


r8	r8d	r8w	r8b
...	...	...	...
r15	r15d	r15w	r15b

b - byte, 8 bitow
w - word, 16 bitow
d - double word, 32 bity
bez sufiksu - quadruple word - 64 bity

Uwagi do architektury x86-64:

64-bitowe stale liczbowe mozna przekazywac bezposrednio w kodzie rozkazu (immediate addressing)
jedna z instrukcji mov (np. movabs). Stale, bedace argumentami innych rozkazow 64-bitowych
(np. logicznych i arytmetycznych) kodowane sa jako liczby 32-bitowe i nastepnie rozszerzane do
64 bitow z uwzglednieniem znaku.

W przypadku instrukcji wykorzystujacych dwa rejestry 8-bitowe,
rejestrow ah, bh, ch, dh nie mozna uzywac w kombinacji z rejestrami
dil, sil, spl, bpl, r8b - r15b.

Operacje na rejestrze 32-bitowym zeruja starsze 32 bity odpowiadajacego mu rejestru 64 bitowego.
Operacje 16- i 8-bitowe nie modyfikuja starszej czesci.

-----------------------------------------------------------

Alokacja pamieci (dane) oraz sufiksy "rozmiaru" rozkazow:

.byte	b	8 bitow
.word	w	16 bitow
.long	l	32 bity
.quad	q	64 bity

Ciagi tekstowe:

"zwykle", bez znaku konczacego:
.ascii

terminowane znakiem pustym (NULL) - jak w jezyku C:
.asciz
.string

-----------------------------------------------------------

Kompilacja:

as plik.s -o plik.o

Linkowanie:

- przy braku wywolan funkcji z bibliotek jezyka C (golwna etykieta _start):

ld plik.o -o plik_wykonywalny

- przy wykorzystaniu funkcji bibliotecznych jezyka C (glowna etykieta main):

gcc plik.o -o plik_wykonywalny

- w przypadku kounikatu:

relocation R_X86_64_32S against `.data' can not be used when making a PIE object; recompile with -fPIE

dodac przelacznik no-pie:

ld/gcc plik.o -o plik_wykonywalny -no-pie

-----------------------------------------------------------