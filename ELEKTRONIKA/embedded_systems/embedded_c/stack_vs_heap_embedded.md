# Stack vs Heap w systemach wbudowanych

## Wprowadzenie

W systemach wbudowanych zarządzanie pamięcią jest krytyczne. Zrozumienie różnicy między Stack a Heap pozwala unikać błędów i optymalizować wykorzystanie ograniczonych zasobów.

## Stack (Stos)

### Charakterystyka
- Automatyczne zarządzanie (LIFO - Last In First Out)
- Szybki dostęp
- Ograniczony rozmiar (np. 4-8KB)
- Zmienne lokalne funkcji

```c
void function(void) {
    uint32_t local_var;  // Na stosie
    uint8_t buffer[100]; // Na stosie
    
    // Po return() pamięć automatycznie zwalniana
}
```

### Przepełnienie stosu (Stack Overflow)
```c
// ❌ NIEBEZPIECZNE - duża tablica na stosie
void bad_function(void) {
    uint8_t big_buffer[4096];  // Może przepełnić stos!
}

// ✅ LEPIEJ - statyczna alokacja
static uint8_t big_buffer[4096];  // W .bss, nie na stosie
```

## Heap (Sterta)

### W embedded - zazwyczaj UNIKAMY
```c
// Standardowe C - malloc/free
uint8_t *buffer = malloc(256);  // ❌ Unikane w embedded
if(buffer != NULL) {
    // Użycie
    free(buffer);
}
```

### Problemy z Heap w embedded
1. **Fragmentacja pamięci**
2. **Niedeterministyczny czas**
3. **Brak gwarancji sukcesu**
4. **Trudne debugowanie**

## Statyczna alokacja - preferowana metoda

```c
// Definicja globalnie/static
static uint8_t static_buffer[256];  // W .bss

void process_data(void) {
    // Użycie bufora statycznego
    for(uint16_t i = 0; i < 256; i++) {
        static_buffer[i] = i;
    }
}
```

## Memory pools jako alternatywa

```c
#define POOL_SIZE 10
#define BUFFER_SIZE 64

typedef struct {
    uint8_t data[BUFFER_SIZE];
    bool used;
} buffer_t;

static buffer_t buffer_pool[POOL_SIZE];

buffer_t* allocate_buffer(void) {
    for(uint8_t i = 0; i < POOL_SIZE; i++) {
        if(!buffer_pool[i].used) {
            buffer_pool[i].used = true;
            return &buffer_pool[i];
        }
    }
    return NULL;  // Pool pełny
}

void free_buffer(buffer_t *buf) {
    if(buf != NULL) {
        buf->used = false;
    }
}
```

## Rozmiary pamięci

### Typowy mikrokontroler (STM32F103)
- Flash: 64KB-128KB
- RAM: 20KB
- Stack: 4KB
- .data + .bss: ~10KB
- Heap: Zazwyczaj ZERO

## Monitorowanie stosu

```c
// Wypełnienie stosu pattern
extern uint32_t _estack;
extern uint32_t _sstack;

void stack_fill_pattern(void) {
    uint32_t *p = &_sstack;
    while(p < &_estack) {
        *p++ = 0xDEADBEEF;
    }
}

uint32_t stack_usage(void) {
    uint32_t *p = &_sstack;
    uint32_t unused = 0;
    
    while(*p == 0xDEADBEEF && p < &_estack) {
        unused += 4;
        p++;
    }
    
    return ((uint32_t)&_estack - (uint32_t)&_sstack) - unused;
}
```

## Dobre praktyki

1. **Preferuj alokację statyczną**
2. **Unikaj dużych tablic lokalnych**
3. **Użyj memory pools gdy potrzebna elastyczność**
4. **Monitoruj użycie stosu**
5. **Unikaj malloc/free w produkcji**

## Powiązane tematy
- [[alokacja_statyczna|Alokacja pamięci statycznej]]
- [[optymalizacja_pamieci|Optymalizacja pamięci]]
- [[memory_mapped_io|Memory-Mapped I/O]]
