# Wskaźniki i adresowanie pamięci w Embedded C

## Wprowadzenie

Wskaźniki to fundament programowania Embedded C. Umożliwiają bezpośredni dostęp do pamięci, rejestrów sprzętowych i efektywne zarządzanie danymi w systemach o ograniczonych zasobach.

## Podstawy wskaźników

### Deklaracja i podstawowe użycie
```c
uint32_t value = 100;
uint32_t *ptr;        // Wskaźnik do uint32_t

ptr = &value;         // ptr wskazuje na value
*ptr = 200;           // Modyfikacja value przez wskaźnik
// value jest teraz = 200
```

### Wskaźniki a adresy
```c
uint32_t data = 0x12345678;
uint32_t *ptr = &data;

printf("Adres zmiennej: %p\n", (void*)&data);
printf("Wartość ptr: %p\n", (void*)ptr);
printf("Wartość *ptr: 0x%08X\n", *ptr);

// Przykładowe wyjście (adresy będą różne):
// Adres zmiennej: 0x20000100
// Wartość ptr: 0x20000100
// Wartość *ptr: 0x12345678
```

## Wskaźniki do rejestrów sprzętowych

### Pojedynczy rejestr
```c
// Definicja rejestru jako wskaźnik do volatile uint32_t
#define GPIOA_ODR  (*(volatile uint32_t*)0x40020014)

// Użycie
GPIOA_ODR = 0x00000020;  // Ustaw wartość rejestru
GPIOA_ODR |= (1 << 5);   // Ustaw bit 5
```

### Dlaczego volatile?
```c
volatile uint32_t *status_reg = (volatile uint32_t*)0x40001000;

// BEZ volatile:
while(*status_reg == 0);  // Kompilator może zoptymalizować do while(1)!

// Z volatile:
while(*status_reg == 0);  // Kompilator zawsze czyta z pamięci
```

### Wskaźnik do struktury rejestrów
```c
typedef struct {
    volatile uint32_t MODER;    // Offset 0x00
    volatile uint32_t OTYPER;   // Offset 0x04
    volatile uint32_t OSPEEDR;  // Offset 0x08
    volatile uint32_t PUPDR;    // Offset 0x0C
    volatile uint32_t IDR;      // Offset 0x10
    volatile uint32_t ODR;      // Offset 0x14
} GPIO_TypeDef;

// Wskaźnik do struktury GPIO
#define GPIOA  ((GPIO_TypeDef*)0x40020000)
#define GPIOB  ((GPIO_TypeDef*)0x40020400)

// Użycie - bardzo czytelne!
GPIOA->ODR = 0x0020;
GPIOB->MODER |= (1 << 10);
```

## Arytmetyka wskaźników

### Podstawowa arytmetyka
```c
uint32_t array[5] = {10, 20, 30, 40, 50};
uint32_t *ptr = array;

*ptr = 100;        // array[0] = 100
ptr++;             // Wskaźnik przesuwa się o sizeof(uint32_t) = 4 bajty
*ptr = 200;        // array[1] = 200
ptr += 2;          // Przesuń o 2 elementy
*ptr = 300;        // array[3] = 300
```

### Dostęp do tablicy przez wskaźnik
```c
uint8_t buffer[10];
uint8_t *ptr = buffer;

// Te zapisy są równoważne:
buffer[3] = 0xFF;
*(buffer + 3) = 0xFF;
*(ptr + 3) = 0xFF;
ptr[3] = 0xFF;
```

### Różnica wskaźników
```c
uint32_t array[10];
uint32_t *start = &array[2];
uint32_t *end = &array[7];

ptrdiff_t diff = end - start;  // diff = 5 (elementów, nie bajtów!)
```

## Wskaźniki w funkcjach

### Przekazywanie przez wskaźnik (modyfikacja)
```c
void increment(uint32_t *value) {
    (*value)++;
}

int main(void) {
    uint32_t counter = 10;
    increment(&counter);
    // counter jest teraz 11
}
```

### Wskaźniki do tablic
```c
void process_array(uint8_t *data, uint16_t length) {
    for(uint16_t i = 0; i < length; i++) {
        data[i] = data[i] * 2;
    }
}

// Lub z arytmetyką wskaźników
void process_array_v2(uint8_t *data, uint16_t length) {
    uint8_t *end = data + length;
    while(data < end) {
        *data = (*data) * 2;
        data++;
    }
}
```

### Zwracanie wskaźników
```c
// ❌ NIEBEZPIECZNE - zwraca wskaźnik do zmiennej lokalnej!
uint32_t* bad_function(void) {
    uint32_t local = 100;
    return &local;  // local zniknie po return!
}

// ✅ DOBRE - zwraca wskaźnik do statycznej zmiennej
uint32_t* good_function(void) {
    static uint32_t persistent = 100;
    return &persistent;
}

// ✅ DOBRE - zwraca wskaźnik przekazany jako parametr
uint8_t* find_value(uint8_t *array, uint16_t length, uint8_t value) {
    for(uint16_t i = 0; i < length; i++) {
        if(array[i] == value) {
            return &array[i];
        }
    }
    return NULL;  // Nie znaleziono
}
```

## Wskaźniki const i volatile

### Różne kombinacje const
```c
// Wskaźnik do stałych danych
const uint8_t *ptr1;
ptr1 = &data;    // OK
*ptr1 = 5;       // BŁĄD - dane są const
ptr1 = &other;   // OK - wskaźnik nie jest const

// Stały wskaźnik
uint8_t * const ptr2 = &data;
*ptr2 = 5;       // OK - dane nie są const
ptr2 = &other;   // BŁĄD - wskaźnik jest const

// Stały wskaźnik do stałych danych
const uint8_t * const ptr3 = &data;
*ptr3 = 5;       // BŁĄD - dane są const
ptr3 = &other;   // BŁĄD - wskaźnik jest const
```

### Volatile z const
```c
// Rejestr tylko do odczytu (np. ID chip)
const volatile uint32_t *chip_id = (const volatile uint32_t*)0x1FFF7A10;
uint32_t id = *chip_id;  // Odczyt OK
*chip_id = 123;          // BŁĄD - const

// Rejestr do zapisu (kompilator nie może optymalizować)
volatile uint32_t *output_reg = (volatile uint32_t*)0x40020014;
*output_reg = 0x100;
*output_reg = 0x200;  // Oba zapisy wykonane, mimo że brak odczytu między nimi
```

## Wskaźniki funkcji

### Podstawy
```c
// Deklaracja typu wskaźnika funkcji
typedef void (*callback_t)(void);

// Funkcje
void function_a(void) {
    uart_send_string("A\n");
}

void function_b(void) {
    uart_send_string("B\n");
}

// Użycie
callback_t callback = function_a;
callback();  // Wywołuje function_a

callback = function_b;
callback();  // Wywołuje function_b
```

### Callback w przerwaniach
```c
typedef void (*irq_callback_t)(void);

static irq_callback_t uart_rx_callback = NULL;

void uart_register_callback(irq_callback_t callback) {
    uart_rx_callback = callback;
}

void UART_IRQHandler(void) {
    if(USART1->SR & USART_SR_RXNE) {
        uint8_t data = USART1->DR;
        
        // Wywołaj callback jeśli zarejestrowany
        if(uart_rx_callback != NULL) {
            uart_rx_callback();
        }
    }
}

// Rejestracja callback
void my_rx_handler(void) {
    // Obsługa odebranych danych
}

int main(void) {
    uart_init();
    uart_register_callback(my_rx_handler);
    // ...
}
```

### Tablica wskaźników funkcji (state machine)
```c
typedef enum {
    STATE_IDLE,
    STATE_RUNNING,
    STATE_ERROR,
    STATE_MAX
} state_t;

typedef void (*state_handler_t)(void);

void idle_handler(void) {
    // Obsługa stanu IDLE
}

void running_handler(void) {
    // Obsługa stanu RUNNING
}

void error_handler(void) {
    // Obsługa stanu ERROR
}

// Tablica wskaźników funkcji
const state_handler_t state_handlers[STATE_MAX] = {
    idle_handler,
    running_handler,
    error_handler
};

void state_machine_update(state_t current_state) {
    if(current_state < STATE_MAX) {
        state_handlers[current_state]();
    }
}
```

## Mapowanie pamięci

### Regiony pamięci
```c
// Adresy charakterystyczne dla ARM Cortex-M

// Flash (Code)
#define FLASH_BASE     0x08000000

// SRAM
#define SRAM_BASE      0x20000000

// Peripheral
#define PERIPH_BASE    0x40000000

// Cortex-M System
#define SYSTEM_BASE    0xE0000000
```

### Dostęp do różnych regionów
```c
// Stałe w Flash
const uint32_t lookup_table[256] = { /* ... */ };
const uint32_t *flash_ptr = lookup_table;  // Wskazuje na Flash

// Dane w RAM
uint32_t ram_data[100];
uint32_t *ram_ptr = ram_data;  // Wskazuje na RAM

// Rejestr peryferii
volatile uint32_t *periph_ptr = (volatile uint32_t*)0x40020000;
```

### Linkowanie zmiennych do określonych adresów
```c
// Użycie atrybutu GCC
__attribute__((section(".my_section")))
uint32_t special_data[100];

// Lub bezpośrednie umieszczenie pod adresem
uint32_t *fixed_buffer = (uint32_t*)0x20001000;

// W linker script:
// .my_section 0x20002000 :
// {
//     *(.my_section)
// } > RAM
```

## DMA i wskaźniki

### Konfiguracja transferu DMA
```c
typedef struct {
    volatile uint32_t CR;     // Control Register
    volatile uint32_t NDTR;   // Number of Data Register
    volatile uint32_t PAR;    // Peripheral Address Register
    volatile uint32_t MAR;    // Memory Address Register
} DMA_Channel_TypeDef;

#define DMA1_Channel1 ((DMA_Channel_TypeDef*)0x40020008)

uint8_t buffer[100];

void dma_setup(void) {
    // Adres peryferii (np. USART data register)
    DMA1_Channel1->PAR = (uint32_t)&USART1->DR;
    
    // Adres pamięci
    DMA1_Channel1->MAR = (uint32_t)buffer;
    
    // Liczba danych do transferu
    DMA1_Channel1->NDTR = 100;
    
    // Konfiguracja i start
    DMA1_Channel1->CR |= DMA_CR_EN;
}
```

## Wskaźniki a struktury

### Dostęp do członków struktury
```c
typedef struct {
    uint16_t x;
    uint16_t y;
    uint16_t z;
} point_t;

point_t point = {10, 20, 30};
point_t *ptr = &point;

// Dwa sposoby dostępu:
(*ptr).x = 100;  // Wymaga nawiasów
ptr->x = 100;    // Preferowane - operator ->
```

### Iteracja po tablicy struktur
```c
typedef struct {
    uint8_t id;
    uint16_t value;
} sensor_t;

sensor_t sensors[10];

void update_sensors(void) {
    sensor_t *ptr = sensors;
    for(uint8_t i = 0; i < 10; i++) {
        ptr->value = read_sensor(ptr->id);
        ptr++;
    }
}
```

## Wskaźniki wielopoziomowe

### Wskaźnik do wskaźnika
```c
uint32_t value = 100;
uint32_t *ptr1 = &value;
uint32_t **ptr2 = &ptr1;

**ptr2 = 200;  // Modyfikuje value
// value == 200
```

### Tablica wskaźników
```c
const char *messages[] = {
    "Init OK",
    "Error",
    "Warning",
    "Ready"
};

void print_message(uint8_t index) {
    if(index < 4) {
        uart_send_string(messages[index]);
    }
}
```

## Alignment i padding

### Wyrównanie danych
```c
// ARM Cortex-M wymaga wyrównania dla szybkiego dostępu
uint32_t aligned_data __attribute__((aligned(4)));

// Sprawdzenie wyrównania
if(((uint32_t)ptr & 0x03) == 0) {
    // ptr jest wyrównany do 4 bajtów
}
```

### Padding w strukturach
```c
struct {
    uint8_t  a;    // 1 bajt
    // 3 bajty padding
    uint32_t b;    // 4 bajty (wymaga wyrównania)
    uint8_t  c;    // 1 bajt
    // 3 bajty padding
} data;  // Razem 12 bajtów zamiast 6!

// Pakowanie (ostrożnie - może być wolniejsze!)
struct __attribute__((packed)) {
    uint8_t  a;    // 1 bajt
    uint32_t b;    // 4 bajty
    uint8_t  c;    // 1 bajt
} packed_data;  // Tylko 6 bajtów
```

## Bezpieczeństwo wskaźników

### Sprawdzanie NULL
```c
void safe_function(uint8_t *data) {
    if(data == NULL) {
        return;  // Ochrona przed NULL pointer
    }
    
    *data = 0xFF;  // Bezpieczne użycie
}
```

### Sprawdzanie zakresu
```c
bool is_valid_ram_address(void *ptr) {
    uint32_t addr = (uint32_t)ptr;
    return (addr >= SRAM_BASE) && 
           (addr < (SRAM_BASE + SRAM_SIZE));
}
```

### Wskaźniki restrict (C99)
```c
// Kompilator wie, że src i dst nie nakładają się
void copy_buffer(uint8_t * restrict dst, 
                 const uint8_t * restrict src, 
                 size_t len) {
    for(size_t i = 0; i < len; i++) {
        dst[i] = src[i];
    }
}
```

## Przykład kompleksowy - Ring Buffer

```c
typedef struct {
    uint8_t *buffer;      // Wskaźnik do bufora
    uint16_t size;        // Rozmiar bufora
    volatile uint16_t head;  // Indeks zapisu
    volatile uint16_t tail;  // Indeks odczytu
} ring_buffer_t;

void ring_buffer_init(ring_buffer_t *rb, uint8_t *buffer, uint16_t size) {
    rb->buffer = buffer;
    rb->size = size;
    rb->head = 0;
    rb->tail = 0;
}

bool ring_buffer_put(ring_buffer_t *rb, uint8_t data) {
    uint16_t next_head = (rb->head + 1) % rb->size;
    
    if(next_head == rb->tail) {
        return false;  // Bufor pełny
    }
    
    *(rb->buffer + rb->head) = data;  // Lub rb->buffer[rb->head]
    rb->head = next_head;
    return true;
}

bool ring_buffer_get(ring_buffer_t *rb, uint8_t *data) {
    if(rb->head == rb->tail) {
        return false;  // Bufor pusty
    }
    
    *data = *(rb->buffer + rb->tail);
    rb->tail = (rb->tail + 1) % rb->size;
    return true;
}

// Użycie
uint8_t uart_buffer[256];
ring_buffer_t uart_rb;

int main(void) {
    ring_buffer_init(&uart_rb, uart_buffer, sizeof(uart_buffer));
    
    // W przerwaniu UART RX
    uint8_t received;
    if(uart_read(&received)) {
        ring_buffer_put(&uart_rb, received);
    }
    
    // W main loop
    uint8_t data;
    if(ring_buffer_get(&uart_rb, &data)) {
        process_byte(data);
    }
}
```

## Dobre praktyki

1. **Zawsze inicjalizuj** wskaźniki (NULL lub prawidłowy adres)
2. **Sprawdzaj NULL** przed dereferencją
3. **Używaj const** gdzie to możliwe
4. **Używaj volatile** dla rejestrów i współdzielonych danych
5. **Unikaj wskaźników wielopoziomowych** (trudne w utrzymaniu)
6. **Dokumentuj właściciela** pamięci (kto zwalnia)
7. **Używaj typedef** dla wskaźników funkcji

## Powiązane tematy
- [[typy_danych_embedded_c|Typy danych w Embedded C]]
- [[volatile_keyword|Słowo kluczowe volatile]]
- [[memory_mapped_io|Memory-Mapped I/O]]
- [[stack_vs_heap_embedded|Stack vs Heap]]
