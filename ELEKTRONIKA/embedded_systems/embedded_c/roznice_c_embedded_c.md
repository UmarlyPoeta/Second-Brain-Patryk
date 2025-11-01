# Różnice między C a Embedded C

## Wprowadzenie

Chociaż Embedded C bazuje na standardzie ANSI C (C89/C90) lub C99, istnieje wiele istotnych różnic w sposobie pisania i używania kodu. Te różnice wynikają z ograniczeń sprzętowych i specyficznych wymagań systemów wbudowanych.

## Główne różnice

### 1. Środowisko wykonania

#### Standardowy C
```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    printf("Hello World!\n");
    return 0;  // Program kończy działanie
}
```

#### Embedded C
```c
#include <stdint.h>

// Brak argc/argv - nie ma systemu operacyjnego
int main(void) {
    // Inicjalizacja sprzętu
    init_hardware();
    
    // Nieskończona pętla - program nigdy się nie kończy
    while(1) {
        // Główna logika programu
        process_tasks();
    }
    
    // Ten kod nigdy się nie wykona
    return 0;
}
```

### 2. Biblioteka standardowa

#### Standardowy C - pełna biblioteka
```c
#include <stdio.h>   // I/O
#include <stdlib.h>  // malloc, free
#include <string.h>  // strcpy, strcmp
#include <math.h>    // sin, cos, sqrt

void example(void) {
    char *buffer = malloc(1024);
    strcpy(buffer, "Hello");
    printf("Result: %f\n", sqrt(16.0));
    free(buffer);
}
```

#### Embedded C - ograniczona biblioteka
```c
#include <stdint.h>  // Typy o stałej szerokości
#include <stdbool.h> // bool, true, false

// Często NIE MA stdio.h, stdlib.h!
// Trzeba implementować własne funkcje

void my_strcpy(char *dest, const char *src) {
    while((*dest++ = *src++));
}

// Własna implementacja printf - często bardzo ograniczona
void uart_printf(const char *str) {
    while(*str) {
        uart_send_char(*str++);
    }
}
```

### 3. Dynamiczna alokacja pamięci

#### Standardowy C
```c
// malloc/free szeroko używane
void process_data(size_t size) {
    int *data = malloc(size * sizeof(int));
    if (data == NULL) {
        fprintf(stderr, "Błąd alokacji!\n");
        return;
    }
    
    // Przetwarzanie...
    
    free(data);
}
```

#### Embedded C
```c
// Alokacja statyczna - unikanie malloc/free!
#define MAX_DATA_SIZE 100

static int data_buffer[MAX_DATA_SIZE];

void process_data(size_t size) {
    // Sprawdzenie rozmiaru w czasie kompilacji lub runtime
    if (size > MAX_DATA_SIZE) {
        // Obsługa błędu
        return;
    }
    
    // Używamy statycznego bufora
    // Brak potrzeby zwalniania pamięci
}
```

**Powody unikania malloc w embedded:**
- Fragmentacja pamięci
- Niedeterministyczny czas wykonania
- Możliwość wyczerpania pamięci
- Zwiększa rozmiar kodu (biblioteka malloc)

### 4. Typy danych

#### Standardowy C
```c
// Rozmiary typów zależne od platformy
int value;          // Może być 16, 32 lub 64 bity
long counter;       // Niejasny rozmiar
unsigned int flags; // ?
```

#### Embedded C
```c
#include <stdint.h>

// Typy o dokładnie określonej szerokości
uint8_t  byte_value;    // Dokładnie 8 bitów
uint16_t word_value;    // Dokładnie 16 bitów  
uint32_t dword_value;   // Dokładnie 32 bity
int16_t  signed_value;  // Dokładnie 16 bitów ze znakiem

// Krytyczne dla dostępu do rejestrów!
volatile uint32_t *GPIO_ODR = (volatile uint32_t*)0x40020014;
```

### 5. Operacje bitowe

#### Standardowy C - rzadko używane
```c
int flags = 0;
// Operacje na całych zmiennych
if (is_flag_set) {
    flags = 1;
}
```

#### Embedded C - intensywne użycie
```c
// Stałe manipulacje bitami
#define LED1_PIN  (1 << 0)  // Bit 0
#define LED2_PIN  (1 << 1)  // Bit 1
#define LED3_PIN  (1 << 5)  // Bit 5

// Ustawienie bitu
GPIOA->ODR |= LED1_PIN;

// Czyszczenie bitu
GPIOA->ODR &= ~LED2_PIN;

// Przełączenie bitu
GPIOA->ODR ^= LED3_PIN;

// Sprawdzenie bitu
if (GPIOA->IDR & LED1_PIN) {
    // Bit ustawiony
}
```

### 6. Volatile keyword

#### Standardowy C - rzadko używany
```c
int counter = 0;  // Normalny int
```

#### Embedded C - krytyczny!
```c
// volatile dla zmiennych modyfikowanych przez przerwania
volatile uint32_t tick_count = 0;

// volatile dla rejestrów sprzętowych
#define GPIOA_IDR (*(volatile uint32_t*)0x40020010)

// W przerwaniu
void SysTick_Handler(void) {
    tick_count++;  // Zmiana w przerwaniu
}

// W głównej pętli
void delay_ms(uint32_t ms) {
    volatile uint32_t start = tick_count;
    while((tick_count - start) < ms) {
        // volatile zapobiega optymalizacji
    }
}
```

### 7. Floating point

#### Standardowy C
```c
double calculate_average(double *values, int count) {
    double sum = 0.0;
    for(int i = 0; i < count; i++) {
        sum += values[i];
    }
    return sum / count;
}
```

#### Embedded C
```c
// Często unika się float/double - wolne na wielu MCU!
// Używa się arytmetyki stałoprzecinkowej

// Zamiast: float temperature = 25.5;
int16_t temperature_x10 = 255;  // 25.5°C * 10

// Konwersja ADC na napięcie bez float
// Zamiast: voltage = (adc_value / 4095.0) * 3.3
uint32_t voltage_mv = (adc_value * 3300) / 4095;  // W miliWoltach

// Jeśli FPU dostępne (ARM Cortex-M4F), można używać:
float sensor_value = 25.5f;  // Użyj 'f' dla float zamiast double
```

### 8. Inicjalizacja zmiennych

#### Standardowy C
```c
int main(void) {
    int value = 0;  // Inicjalizacja lokalna
    // ...
}
```

#### Embedded C
```c
// Zmienne globalne zerowane przez startup code
uint32_t global_counter;  // = 0 automatycznie

// Zmienne w .data inicjalizowane z Flash
const uint8_t lookup_table[] = {1, 2, 4, 8, 16};

// Zmienne lokalne - mogą być niezainicjalizowane!
void function(void) {
    uint32_t temp;  // NIEBEZPIECZNE - śmieci!
    temp = 0;       // Zawsze inicjalizuj!
}
```

### 9. Funkcja main() i startup

#### Standardowy C
```c
// System operacyjny wywołuje main()
int main(int argc, char *argv[]) {
    // Kod aplikacji
    return 0;  // Zwraca status do OS
}
```

#### Embedded C
```c
// Reset_Handler wywołuje main po inicjalizacji
void Reset_Handler(void) {
    // 1. Kopiowanie .data z Flash do RAM
    extern uint32_t _sdata, _edata, _sidata;
    uint32_t *src = &_sidata;
    uint32_t *dst = &_sdata;
    while(dst < &_edata) {
        *dst++ = *src++;
    }
    
    // 2. Zerowanie .bss
    extern uint32_t _sbss, _ebss;
    dst = &_sbss;
    while(dst < &_ebss) {
        *dst++ = 0;
    }
    
    // 3. Wywołanie main
    main();
    
    // 4. Jeśli main() zwróci (nie powinno!)
    while(1);
}

int main(void) {
    // Inicjalizacja sprzętu
    SystemInit();
    init_peripherals();
    
    // Nieskończona pętla
    while(1) {
        // Główna logika
    }
}
```

### 10. Obsługa błędów

#### Standardowy C
```c
#include <errno.h>
#include <stdio.h>

void handle_error(void) {
    if (errno == ENOMEM) {
        fprintf(stderr, "Out of memory!\n");
        exit(1);
    }
}
```

#### Embedded C
```c
// Brak errno, exit() nie ma sensu
// Własne mechanizmy obsługi błędów

typedef enum {
    ERR_OK = 0,
    ERR_INVALID_PARAM,
    ERR_TIMEOUT,
    ERR_BUSY
} error_code_t;

error_code_t init_sensor(void) {
    if (!check_sensor_present()) {
        return ERR_TIMEOUT;
    }
    return ERR_OK;
}

// Lub asercje (wyłączane w produkcji)
#ifdef DEBUG
    #define ASSERT(expr) \
        if(!(expr)) { \
            error_handler(__FILE__, __LINE__); \
        }
#else
    #define ASSERT(expr) ((void)0)
#endif
```

## Podsumowanie różnic

| Cecha | Standardowy C | Embedded C |
|-------|--------------|------------|
| main() zwraca | TAK | Rzadko (while(1)) |
| malloc/free | Często | Rzadko/Nigdy |
| printf/scanf | TAK | Często brak |
| Biblioteka standardowa | Pełna | Minimalna |
| float/double | Bez problemu | Ostrożnie |
| volatile | Rzadko | Często |
| Operacje bitowe | Rzadko | Bardzo często |
| Typy stdint.h | Opcjonalnie | Zawsze |
| Obsługa przerwań | Nie | Kluczowa |
| Rekurencja | OK | Unikana |

## Przykład kompleksowy

### Standardowy C - aplikacja desktopowa
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <filename>\n", argv[0]);
        return 1;
    }
    
    FILE *file = fopen(argv[1], "r");
    if (!file) {
        perror("Error opening file");
        return 1;
    }
    
    char *line = NULL;
    size_t len = 0;
    
    while(getline(&line, &len, file) != -1) {
        printf("%s", line);
    }
    
    free(line);
    fclose(file);
    return 0;
}
```

### Embedded C - firmware mikrokontrolera
```c
#include <stdint.h>
#include <stdbool.h>

#define LED_PIN    (1 << 5)
#define BUTTON_PIN (1 << 13)

volatile uint32_t systick_count = 0;

void SysTick_Handler(void) {
    systick_count++;
}

void delay_ms(uint32_t ms) {
    uint32_t start = systick_count;
    while((systick_count - start) < ms);
}

int main(void) {
    // Konfiguracja zegara systemowego
    SystemClock_Config();
    
    // Konfiguracja SysTick (1ms)
    SysTick_Config(SystemCoreClock / 1000);
    
    // Włącz zegar GPIO
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    
    // Konfiguruj LED jako output
    GPIOA->MODER &= ~(3 << (5*2));
    GPIOA->MODER |= (1 << (5*2));
    
    // Konfiguruj przycisk jako input
    GPIOC->MODER &= ~(3 << (13*2));
    GPIOC->PUPDR |= (2 << (13*2));  // Pull-down
    
    while(1) {
        // Sprawdź przycisk
        if (GPIOC->IDR & BUTTON_PIN) {
            GPIOA->ODR |= LED_PIN;   // LED ON
        } else {
            GPIOA->ODR &= ~LED_PIN;  // LED OFF
        }
        
        delay_ms(10);  // Debouncing
    }
}
```

## Powiązane tematy
- [[wprowadzenie_do_embedded_c|Wprowadzenie do Embedded C]]
- [[typy_danych_embedded_c|Typy danych w Embedded C]]
- [[volatile_keyword|Słowo kluczowe volatile]]

## Dalsza lektura
- [[operatory_bitowe|Operatory bitowe]]
- [[wskazniki_adresowanie|Wskaźniki i adresowanie pamięci]]
