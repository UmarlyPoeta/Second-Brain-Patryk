# [[sciaga]]

#################################################################
#
# Laboratorium 1 - budowa najprostszego programu:
# wywolanie System Calls,
# wydrukowanie ciagu tekstowego w oknie terminala,
# tworzenie pliku wykonywalnego: kompilacja i linkowanie.

.globl _start

# "_start" to nazwa (etykieta - label) programu glownego,
# jest to adres pierwszej instrukcji programu.

# Definicje stalych, uzywanych w programie (opcjonalnie).

.equ	sys_write,	1
.equ	sys_exit,	60
.equ	stdout,	1
.equ	strlen, 	new_line + 1 - str

#################################################################
#
# Alokacja pamieci - zmienne statyczne, 8/16/32/64-bitowe,
# z nadana wartoscia poczatkowa.

.data

str:		.ascii	"Hello!"
new_line:	.byte	0x0A

#################################################################
#
# Program glowny.

.text

_start:

# Zadania:
# - 1 - zrobione - przekaz argumenty i wywolaj System Call nr 1 (sys_write).

mov	$sys_write , %eax
mov	$stdout , %edi
mov	$str , %esi
mov	$strlen , %edx
syscall

# - 2 - zakoncz poprawnie program,
# przekaz argumenty i wywolaj System Call nr 60 (sys_exit).

# ...
