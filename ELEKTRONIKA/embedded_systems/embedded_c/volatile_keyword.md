# Słowo kluczowe volatile w Embedded C

## Wprowadzenie

`volatile` to jedno z najważniejszych słów kluczowych w programowaniu systemów wbudowanych. Informuje kompilator, że wartość zmiennej może zmienić się w sposób nieprzewidywalny dla analizatora kodu (np. przez przerwanie, DMA, lub rejestr sprzętowy).

## Czym jest volatile?

### Definicja
`volatile` mówi kompilatorowi: **"NIE optymalizuj dostępu do tej zmiennej, zawsze czytaj/pisz do pamięci"**

### Problem bez volatile
```c
// BEZ volatile
uint32_t status_register;

// Kompilator może zoptymalizować:
while(status_register == 0) {
    // Pętla nieskończona!
}

// Do:
if(status_register == 0) {
    while(1) {  // Kompilator "wie" że status nie zmieni się
        // ...
    }
}
```

### Rozwiązanie z volatile
```c
volatile uint32_t status_register;

// Kompilator MUSI czytać status_register w każdej iteracji
while(status_register == 0) {
    // Pętla zakończy się gdy status zmieni wartość
}
```

## Kiedy używać volatile?

### 1. Rejestry sprzętowe
```c
// ZAWSZE używaj volatile dla rejestrów!
#define GPIO_ODR  (*(volatile uint32_t*)0x40020014)
#define UART_SR   (*(volatile uint32_t*)0x4001100C)
#define ADC_DR    (*(volatile uint32_t*)0x4001204C)

// Odczyt rejestru statusu
while(!(UART_SR & UART_SR_TXE)) {
    // Czekaj na opróżnienie bufora TX
}

// Bez volatile kompilator mógłby odczytać UART_SR tylko raz!
```

### 2. Zmienne modyfikowane w przerwaniach
```c
volatile uint32_t tick_count = 0;
volatile bool data_ready = false;

// Przerwanie SysTick
void SysTick_Handler(void) {
    tick_count++;  // Modyfikacja w przerwaniu
}

// Główna pętla
void delay_ms(uint32_t ms) {
    volatile uint32_t start = tick_count;
    while((tick_count - start) < ms) {
        // volatile zapewnia że tick_count jest czytane w każdej iteracji
    }
}

// Przerwanie UART
void UART_IRQHandler(void) {
    if(USART1->SR & USART_SR_RXNE) {
        received_data = USART1->DR;
        data_ready = true;  // Sygnał dla main
    }
}

int main(void) {
    while(1) {
        if(data_ready) {  // volatile - zawsze sprawdza pamięć
            process_data();
            data_ready = false;
        }
    }
}
```

### 3. Zmienne współdzielone z DMA
```c
volatile uint8_t dma_buffer[256];

void setup_dma(void) {
    // DMA będzie zapisywać do tego bufora
    DMA1_Channel1->MAR = (uint32_t)dma_buffer;
    DMA1_Channel1->NDTR = 256;
    DMA1_Channel1->CR |= DMA_CR_EN;
}

void process_dma_data(void) {
    // volatile zapewnia odczyt aktualnych danych zapisanych przez DMA
    for(uint16_t i = 0; i < 256; i++) {
        uart_send(dma_buffer[i]);
    }
}
```

### 4. Memory-mapped I/O
```c
// Urządzenia zewnętrzne mapowane w pamięci
volatile uint8_t *external_device = (volatile uint8_t*)0x60000000;

// Odczyt/zapis musi być wykonany za każdym razem
uint8_t value = *external_device;
*external_device = 0xFF;
```

## Volatile z różnymi typami

### Pojedyncza zmienna
```c
volatile uint32_t counter;
volatile bool flag;
volatile int16_t temperature;
```

### Wskaźniki volatile

#### Wskaźnik do volatile danych
```c
volatile uint32_t *ptr;  
// *ptr jest volatile, sam wskaźnik nie

volatile uint32_t data = 100;
ptr = &data;
*ptr = 200;  // Zapis volatile
```

#### Volatile wskaźnik
```c
uint32_t * volatile ptr;
// Sam wskaźnik jest volatile, dane nie

// Rzadko używane w embedded
```

#### Volatile wskaźnik do volatile danych
```c
volatile uint32_t * volatile ptr;
// Zarówno wskaźnik jak i dane są volatile

// Bardzo rzadko potrzebne
```

### Przykłady praktyczne
```c
// Rejestr sprzętowy - wskaźnik do volatile
#define GPIO_ODR  (*(volatile uint32_t*)0x40020014)

// Struktura rejestrów
typedef struct {
    volatile uint32_t CR;
    volatile uint32_t SR;
    volatile uint32_t DR;
} USART_TypeDef;

volatile USART_TypeDef *uart = (volatile USART_TypeDef*)0x40011000;
```

### Tablice volatile
```c
volatile uint8_t rx_buffer[256];  // Cała tablica volatile
volatile uint32_t adc_samples[100];

// Każdy element jest traktowany jako volatile
for(uint16_t i = 0; i < 256; i++) {
    process(rx_buffer[i]);  // Każdy odczyt z pamięci
}
```

### Struktury z volatile
```c
typedef struct {
    volatile uint32_t status;
    volatile uint32_t control;
    volatile uint32_t data;
} peripheral_t;

peripheral_t *device = (peripheral_t*)0x40000000;

// Dostęp do pól
device->control = 0x01;
uint32_t stat = device->status;
```

## Volatile a optymalizacja kompilatora

### Przykład 1: Czytanie rejestru
```c
volatile uint32_t *reg = (volatile uint32_t*)0x40020014;

// Kod:
uint32_t a = *reg;
uint32_t b = *reg;

// BEZ volatile kompilator mógłby zoptymalizować do:
uint32_t a = *reg;
uint32_t b = a;  // Nie czyta ponownie!

// Z volatile - zawsze dwa odczyty z pamięci
```

### Przykład 2: Zapisywanie rejestru
```c
volatile uint32_t *reg = (volatile uint32_t*)0x40020014;

// Kod:
*reg = 0x01;
*reg = 0x02;

// BEZ volatile kompilator mógłby usunąć pierwszy zapis:
*reg = 0x02;  // Tylko ostatni zapis

// Z volatile - oba zapisy wykonane
// (Ważne np. dla sekwencji konfiguracyjnych)
```

### Przykład 3: Pętla oczekująca
```c
volatile uint32_t *status = (volatile uint32_t*)0x40001000;

// Kod:
while(*status & 0x01) {
    // Czekaj
}

// BEZ volatile:
if(*status & 0x01) {
    while(1);  // Nieskończona pętla!
}

// Z volatile - sprawdza status w każdej iteracji
```

## Volatile nie gwarantuje atomowości!

### Problem z wielobajtowymi operacjami
```c
volatile uint32_t counter = 0;

// W przerwaniu
void IRQ_Handler(void) {
    counter++;  // Na ARM Cortex-M: OK (atomowe)
}

// Na 8-bitowym AVR może być rozbite na:
// LOAD high_byte
// LOAD low_byte
// INCREMENT
// STORE low_byte
// STORE high_byte
// ^ PRZERWANIE może wystąpić w środku!
```

### Rozwiązania dla atomowości

#### 1. Wyłączenie przerwań
```c
void safe_increment(void) {
    __disable_irq();
    counter++;
    __enable_irq();
}
```

#### 2. Operacje atomowe (CMSIS)
```c
#include "cmsis_gcc.h"

volatile uint32_t counter = 0;

void increment(void) {
    __disable_irq();
    counter++;
    __enable_irq();
}

// Lub użyj atomic operations (Cortex-M3+)
uint32_t old_value;
do {
    old_value = counter;
} while(!__LDREXW(&counter) == old_value || 
        !__STREXW(old_value + 1, &counter));
```

#### 3. Typy atomowe (C11)
```c
#include <stdatomic.h>

atomic_uint_fast32_t counter = 0;

// W przerwaniu
void IRQ_Handler(void) {
    atomic_fetch_add(&counter, 1);  // Atomowe
}
```

## Volatile w różnych scenariuszach

### Polling rejestru statusu
```c
#define USART_SR  (*(volatile uint32_t*)0x4001100C)
#define USART_DR  (*(volatile uint32_t*)0x40011004)

void uart_send_byte(uint8_t byte) {
    // Czekaj aż TX buffer pusty
    while(!(USART_SR & (1 << 7)));
    
    // Wyślij dane
    USART_DR = byte;
}
```

### Komunikacja między przerwaniem a main
```c
volatile uint8_t rx_buffer[256];
volatile uint16_t rx_head = 0;
volatile uint16_t rx_tail = 0;

void UART_IRQHandler(void) {
    if(USART1->SR & USART_SR_RXNE) {
        rx_buffer[rx_head] = USART1->DR;
        rx_head = (rx_head + 1) % 256;
    }
}

int main(void) {
    while(1) {
        if(rx_head != rx_tail) {
            uint8_t data = rx_buffer[rx_tail];
            rx_tail = (rx_tail + 1) % 256;
            process_byte(data);
        }
    }
}
```

### Timeout z volatile
```c
volatile uint32_t systick_ms = 0;

void SysTick_Handler(void) {
    systick_ms++;
}

bool wait_for_flag(volatile uint32_t *flag, uint32_t timeout_ms) {
    volatile uint32_t start = systick_ms;
    
    while(*flag == 0) {
        if((systick_ms - start) > timeout_ms) {
            return false;  // Timeout
        }
    }
    return true;  // Sukces
}
```

## Częste błędy

### Błąd 1: Brak volatile dla flag przerwań
```c
// ❌ ŹLE
bool data_ready = false;

void IRQ_Handler(void) {
    data_ready = true;
}

int main(void) {
    while(!data_ready);  // Może być zoptymalizowane do while(1)
}

// ✅ DOBRZE
volatile bool data_ready = false;
```

### Błąd 2: Brak volatile dla rejestrów
```c
// ❌ ŹLE
#define GPIO_IDR  (*(uint32_t*)0x40020010)

// Kompilator może cache'ować wartość

// ✅ DOBRZE
#define GPIO_IDR  (*(volatile uint32_t*)0x40020010)
```

### Błąd 3: Przekazywanie volatile jako nie-volatile
```c
volatile uint32_t data;

// ❌ Warning: discards volatile qualifier
void process(uint32_t *ptr) {
    *ptr = 100;
}

process(&data);

// ✅ Akceptuj volatile
void process(volatile uint32_t *ptr) {
    *ptr = 100;
}
```

### Błąd 4: Mylenie volatile z synchronizacją
```c
// ❌ volatile NIE ZAPEWNIA atomowości!
volatile uint32_t shared_counter = 0;

void thread1(void) {
    shared_counter++;  // NIE jest atomowe na wszystkich platformach!
}

void thread2(void) {
    shared_counter++;
}

// ✅ Użyj proper synchronizacji
void thread1(void) {
    __disable_irq();
    shared_counter++;
    __enable_irq();
}
```

## Volatile vs const

### Kombinacja volatile const
```c
// Volatile const - można czytać, nie można pisać
// Typowo dla rejestrów tylko do odczytu

const volatile uint32_t *chip_id = 
    (const volatile uint32_t*)0x1FFF7A10;

uint32_t id = *chip_id;  // OK - odczyt
*chip_id = 0;            // BŁĄD kompilacji - const
```

### Przykłady rejestrów
```c
typedef struct {
    volatile uint32_t CR;           // Read/Write
    const volatile uint32_t SR;     // Read-only
    volatile uint32_t DR;           // Read/Write
} PERIPHERAL_TypeDef;
```

## Optymalizacja z volatile

### Redukcja dostępów volatile
```c
// ❌ Nieefektywne - wiele dostępów volatile
volatile uint32_t *reg = (volatile uint32_t*)0x40020000;

for(int i = 0; i < 100; i++) {
    if(*reg & FLAG_READY) {  // Odczyt volatile
        *reg |= FLAG_PROCESS;  // Odczyt + zapis volatile
    }
}

// ✅ Lepiej - cache'uj gdy to bezpieczne
uint32_t cached_value = *reg;  // Jeden odczyt

for(int i = 0; i < 100; i++) {
    if(cached_value & FLAG_READY) {
        // Przetwarzanie
    }
}

*reg = updated_value;  // Jeden zapis
```

### Kiedy można cache'ować?
- Gdy wartość nie zmieni się w trakcie użycia
- Gdy nie ma przerwań modyfikujących wartość
- Gdy kontrolujesz wszystkie punkty zapisu

## Przykład kompleksowy

```c
#include <stdint.h>
#include <stdbool.h>

// Definicje rejestrów
typedef struct {
    volatile uint32_t CR1;
    volatile uint32_t CR2;
    const volatile uint32_t SR;
    volatile uint32_t DR;
    volatile uint32_t BRR;
} USART_TypeDef;

#define USART1 ((USART_TypeDef*)0x40011000)

// Flagi volatile
volatile bool tx_complete = false;
volatile uint8_t rx_buffer[256];
volatile uint16_t rx_count = 0;

// Przerwanie TX Complete
void USART1_IRQHandler(void) {
    // Sprawdź volatile rejestr
    if(USART1->SR & (1 << 6)) {
        tx_complete = true;  // Ustaw volatile flagę
    }
    
    // Odbieranie
    if(USART1->SR & (1 << 5)) {
        rx_buffer[rx_count] = USART1->DR;
        rx_count++;
    }
}

// Funkcja wysyłająca
void uart_send_blocking(uint8_t data) {
    // Czekaj na volatile rejestr
    while(!(USART1->SR & (1 << 7)));
    
    // Wyślij do volatile rejestru
    USART1->DR = data;
}

// Funkcja z timeout
bool uart_send_timeout(uint8_t data, uint32_t timeout_ms) {
    extern volatile uint32_t systick_count;
    volatile uint32_t start = systick_count;
    
    // Czekaj na volatile rejestr z timeout
    while(!(USART1->SR & (1 << 7))) {
        if((systick_count - start) > timeout_ms) {
            return false;
        }
    }
    
    USART1->DR = data;
    return true;
}

int main(void) {
    // Inicjalizacja UART
    USART1->BRR = 0x0683;
    USART1->CR1 = (1 << 13) | (1 << 3) | (1 << 2);
    
    while(1) {
        // Sprawdź volatile flagę
        if(rx_count > 0) {
            // Pobierz z volatile bufora
            uint8_t byte = rx_buffer[0];
            
            // Przesuń dane (chronione przed przerwaniem)
            __disable_irq();
            for(uint16_t i = 0; i < rx_count - 1; i++) {
                rx_buffer[i] = rx_buffer[i + 1];
            }
            rx_count--;
            __enable_irq();
            
            // Przetwórz
            process_byte(byte);
        }
    }
}
```

## Podsumowanie

### Używaj volatile dla:
- ✅ Rejestrów sprzętowych
- ✅ Zmiennych modyfikowanych w przerwaniach
- ✅ Zmiennych współdzielonych z DMA
- ✅ Memory-mapped I/O
- ✅ Zmiennych współdzielonych między wątkami (z dodatkową synchronizacją!)

### NIE używaj volatile dla:
- ❌ Normalnych zmiennych lokalnych
- ❌ Parametrów funkcji (chyba że wskaźnik do volatile)
- ❌ Zamiast proper synchronizacji

### Pamiętaj:
- volatile mówi kompilatorowi "nie optymalizuj"
- volatile NIE zapewnia atomowości
- volatile NIE zapewnia synchronizacji pamięci
- volatile jest niezbędne w embedded, ale nie rozwiązuje wszystkich problemów

## Powiązane tematy
- [[typy_danych_embedded_c|Typy danych w Embedded C]]
- [[wskazniki_adresowanie|Wskaźniki i adresowanie pamięci]]
- [[przerwania_c|Przerwania w języku C]]
- [[memory_mapped_io|Memory-Mapped I/O]]
