#################################################################
#
# Laboratorium 2 - sterowanie przebiegiem programu:
# - petla "for" (rozne sposoby).

.globl _start

# Definicje stalych, uzywanych w programie (opcjonalnie).

.equ	sys_write,	1
.equ	sys_exit,	60
.equ	stdout,	1
.equ	n,		5
.equ	strlen, 	new_line + 1 - str


#################################################################
#
# Alokacja pamieci - zmienne statyczne, z nadana wartoscia poczatkowa.

.data

counter:	.byte	0
str:		.ascii	"iteracja nr: x"
new_line:	.byte	0x0A

#################################################################
#
# Program glowny.

.text

_start:

# Zadanie 1. Petla for: sposob "naiwny" - analiza i ew.Â optymalizacja.

# 1. Inicjuj licznik petli wartoscia poczatkowa:

# ...

petla_for:

# 2. Sprawdz warunek wyjscia z petli:

# ...

# 3a. Jesli warunek spelniony - wyjdz z petli:

# ...

# 3b. Jesli nie - wykonaj kod objety petla:

# wydrukuj ciag tekstowy "str" w petli "n" razy.

# Korekcja ASCII - zmodyfikuj "x" w ciagu "str" tak,
# aby w jego miejscu drukowana byla wartosc licznika iteracji "counter"

# ...

# Wywolaj System Call nr 1 (sys_write) - powtorz "n" razy.

mov	$sys_write , %eax
mov	$stdout , %edi
mov	$str , %esi
mov	$strlen , %edx
syscall

