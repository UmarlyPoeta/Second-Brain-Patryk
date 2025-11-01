# Alokacja pamięci statycznej

## Wprowadzenie

Alokacja statyczna to preferowana metoda zarządzania pamięcią w systemach wbudowanych. Pamięć jest przydzielana w czasie kompilacji/linkowania, nie runtime.

## Zmienne globalne

```c
// Sekcja .data (inicjalizowane)
uint32_t global_counter = 0;
uint8_t config_data[16] = {1, 2, 3, 4};

// Sekcja .bss (zerowane)
uint8_t uninitialized_buffer[256];
```

## Zmienne static

```c
void function(void) {
    static uint32_t call_counter = 0;  // Inicjalizowane raz
    static uint8_t buffer[100];        // Zerowane raz
    
    call_counter++;
}
```

## Const dane w Flash

```c
const uint8_t lookup_table[256] = { /* dane */ };  // W Flash
const char *message = "Hello";  // String w Flash
```

## Memory layout

```
Flash (Code + const data)
├── .text (kod programu)
├── .rodata (const data)
└── .data init values

RAM
├── .data (zmienne inicjalizowane)
├── .bss (zmienne zerowane)
├── heap (jeśli używane)
└── stack (górny RAM)
```

## Zalety alokacji statycznej

1. **Deterministyczne** - znany rozmiar w compile-time
2. **Szybkie** - brak overhead malloc/free
3. **Bezpieczne** - brak fragmentacji
4. **Przewidywalne** - łatwe sprawdzenie użycia RAM

## Linker script

```ld
MEMORY
{
    FLASH (rx) : ORIGIN = 0x08000000, LENGTH = 64K
    RAM  (rwx) : ORIGIN = 0x20000000, LENGTH = 20K
}

SECTIONS
{
    .text : { *(.text*) } > FLASH
    .rodata : { *(.rodata*) } > FLASH
    .data : { *(.data*) } > RAM AT> FLASH
    .bss : { *(.bss*) } > RAM
}
```

## Powiązane tematy
- [[stack_vs_heap_embedded|Stack vs Heap]]
- [[const_keyword|Const keyword]]
- [[optymalizacja_pamieci|Optymalizacja pamięci]]
