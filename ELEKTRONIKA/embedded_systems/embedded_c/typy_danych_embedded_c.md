# Typy danych w Embedded C

## Wprowadzenie

W programowaniu systemów wbudowanych precyzja typów danych jest krytyczna. Musimy dokładnie wiedzieć, ile pamięci zajmuje każda zmienna i jak będzie reprezentowana w pamięci mikrokontrolera.

## Problemy z tradycyjnymi typami C

### Niejednoznaczne rozmiary
```c
// NIE UŻYWAJ w embedded! Rozmiary zależą od platformy
int value;        // 16 bitów na AVR, 32 bity na ARM
long counter;     // 32 lub 64 bity
short data;       // Zwykle 16 bitów, ale nie gwarantowane
```

**Problem:** Ten sam kod może zachowywać się inaczej na różnych mikrokontrolerach!

## Typy stdint.h - standard w Embedded C

```c
#include <stdint.h>

// Typy bez znaku (unsigned)
uint8_t  byte_value;     // 8 bitów (0 do 255)
uint16_t word_value;     // 16 bitów (0 do 65535)
uint32_t dword_value;    // 32 bity (0 do 4294967295)
uint64_t qword_value;    // 64 bity

// Typy ze znakiem (signed)
int8_t   signed_byte;    // 8 bitów (-128 do 127)
int16_t  signed_word;    // 16 bitów (-32768 do 32767)
int32_t  signed_dword;   // 32 bity
int64_t  signed_qword;   // 64 bity
```

### Przykłady użycia

```c
// Rejestr sprzętowy - zawsze 32 bity
volatile uint32_t *GPIO_ODR = (volatile uint32_t*)0x40020014;

// Wartość z ADC - 12 bitów, używamy uint16_t
uint16_t adc_value;

// Flagi - uint8_t wystarczy
uint8_t system_flags;

// Licznik milisekund - może być duży
uint32_t milliseconds;

// Dane z sensora temperatury
int16_t temperature_celsius;  // -40 do +125°C
```

## Typy bool

```c
#include <stdbool.h>

bool is_ready;          // true lub false
bool sensor_active;
bool error_occurred;

// Przed C99, ręcznie:
typedef enum {
    FALSE = 0,
    TRUE = 1
} bool_t;
```

## Typy dla rejestrów sprzętowych

### Pointer do rejestru
```c
// Pojedynczy rejestr 32-bitowy
#define GPIOA_ODR  (*(volatile uint32_t*)0x40020014)

// Użycie
GPIOA_ODR = 0x0020;  // Ustaw wartość rejestru
```

### Struktura dla peryferii
```c
typedef struct {
    volatile uint32_t MODER;    // Offset 0x00
    volatile uint32_t OTYPER;   // Offset 0x04
    volatile uint32_t OSPEEDR;  // Offset 0x08
    volatile uint32_t PUPDR;    // Offset 0x0C
    volatile uint32_t IDR;      // Offset 0x10
    volatile uint32_t ODR;      // Offset 0x14
    volatile uint32_t BSRR;     // Offset 0x18
    volatile uint32_t LCKR;     // Offset 0x1C
    volatile uint32_t AFR[2];   // Offset 0x20-0x24
} GPIO_TypeDef;

#define GPIOA ((GPIO_TypeDef*)0x40020000)

// Użycie - czytelniejsze!
GPIOA->ODR = 0x0020;
GPIOA->MODER |= (1 << 10);
```

## Typy wyliczeniowe (enum)

### Zamiast #define dla stanów
```c
// ❌ Mniej czytelne
#define STATE_IDLE     0
#define STATE_RUNNING  1
#define STATE_ERROR    2

uint8_t current_state = STATE_IDLE;

// ✅ Lepsze - enum
typedef enum {
    STATE_IDLE = 0,
    STATE_RUNNING,
    STATE_ERROR
} system_state_t;

system_state_t current_state = STATE_IDLE;

// Kompilator może wykryć błędy!
switch(current_state) {
    case STATE_IDLE:
        // ...
        break;
    case STATE_RUNNING:
        // ...
        break;
    case STATE_ERROR:
        // ...
        break;
    // Warning jeśli brakuje case!
}
```

### Rozmiar enum
```c
// Kontrola rozmiaru enum
typedef enum __attribute__((packed)) {
    CMD_READ = 0,
    CMD_WRITE,
    CMD_ERASE
} command_t;  // Zajmie tylko 1 bajt zamiast 4

// Lub z określonym typem bazowym (C23/GCC extension)
typedef enum : uint8_t {
    ERR_OK = 0,
    ERR_TIMEOUT,
    ERR_BUSY
} error_t;
```

## Struktury i unie

### Struktury dla danych
```c
// Dane z sensora
typedef struct {
    uint16_t temperature;  // W dziesiątych °C
    uint16_t humidity;     // W dziesiątych %
    uint32_t timestamp;    // Czas odczytu
    uint8_t  status;       // Flagi statusu
} sensor_data_t;

sensor_data_t current_reading;
current_reading.temperature = 235;  // 23.5°C
```

### Pakowanie struktur
```c
// Bez pakowania - wyrównanie do 4 bajtów
typedef struct {
    uint8_t  byte1;   // 1 bajt + 3 bajty padding
    uint32_t dword;   // 4 bajty
    uint8_t  byte2;   // 1 bajt + 3 bajty padding
} unpacked_t;  // Zajmuje 12 bajtów!

// Z pakowaniem - oszczędność pamięci
typedef struct __attribute__((packed)) {
    uint8_t  byte1;   // 1 bajt
    uint32_t dword;   // 4 bajty
    uint8_t  byte2;   // 1 bajt
} packed_t;  // Zajmuje tylko 6 bajtów

// UWAGA: Dostęp może być wolniejszy!
```

### Unie dla interpretacji danych
```c
// Konwersja między bajtami a słowem
typedef union {
    uint32_t word;
    uint8_t  bytes[4];
} word_bytes_t;

word_bytes_t data;
data.word = 0x12345678;
// data.bytes[0] = 0x78
// data.bytes[1] = 0x56
// data.bytes[2] = 0x34
// data.bytes[3] = 0x12

// Użyteczne dla protokołów komunikacyjnych
typedef union {
    struct {
        uint8_t command;
        uint8_t length;
        uint8_t data[8];
        uint8_t checksum;
    } fields;
    uint8_t raw[11];
} protocol_frame_t;

protocol_frame_t frame;
frame.fields.command = 0x01;
// Wyślij frame.raw przez UART
```

## Bitfieldy w strukturach

```c
// Efektywne pakowanie flag
typedef struct {
    uint32_t pin0  : 1;  // 1 bit
    uint32_t pin1  : 1;  // 1 bit
    uint32_t pin2  : 1;  // 1 bit
    uint32_t pin3  : 1;  // 1 bit
    uint32_t reserved : 28;  // Reszta
} gpio_bits_t;

// Użycie do dostępu do rejestrów
typedef struct {
    uint32_t MODE0  : 2;   // Bity 0-1
    uint32_t MODE1  : 2;   // Bity 2-3
    uint32_t MODE2  : 2;   // Bity 4-5
    uint32_t MODE3  : 2;   // Bity 6-7
    // ... reszta pinów
} MODER_bits_t;

#define GPIOA_MODER_BITS ((MODER_bits_t*)0x40020000)

// Dostęp
GPIOA_MODER_BITS->MODE5 = 0b01;  // Output mode
```

**UWAGA:** Kolejność bitów w bitfieldach zależy od kompilatora!

## Typy dla oszczędności pamięci

### Zmienne o zmniejszonej precyzji
```c
// Zamiast float (4 bajty)
int16_t temperature_x10;  // 2 bajty, precyzja 0.1°C
temperature_x10 = 235;    // 23.5°C

// Konwersja
float temp_float = temperature_x10 / 10.0f;

// Napięcie w mV zamiast V
uint16_t voltage_mv;  // 0-65535 mV (0-65.535V)
```

### Tablice o zmniejszonym rozmiarze
```c
// ❌ Marnowanie pamięci
uint32_t small_values[100];  // 400 bajtów

// ✅ Lepiej jeśli wartości < 256
uint8_t small_values[100];   // 100 bajtów
```

## Volatile - typ kwalifikator

```c
// Dla zmiennych modyfikowanych poza kontrolą programu
volatile uint32_t systick_counter;  // Modyfikowane w przerwaniu

// Dla rejestrów sprzętowych
volatile uint32_t *ADC_DR = (volatile uint32_t*)0x4001204C;

// Dla flag między przerwaniem a main
volatile bool data_ready = false;

void UART_IRQHandler(void) {
    if (uart_data_received()) {
        data_ready = true;
    }
}

int main(void) {
    while(1) {
        if (data_ready) {  // volatile zapobiega optymalizacji
            process_data();
            data_ready = false;
        }
    }
}
```

## Const - typ kwalifikator

```c
// Dane w Flash zamiast RAM
const uint8_t sine_table[256] = {
    128, 131, 134, 137, // ...
};

// Wskaźniki const
const uint8_t *ptr;        // Wskaźnik do const danych
uint8_t * const ptr;       // Const wskaźnik
const uint8_t * const ptr; // Const wskaźnik do const danych

// Parametry funkcji
void process(const uint8_t *data, uint16_t length) {
    // data nie może być modyfikowane
    for(uint16_t i = 0; i < length; i++) {
        uart_send(data[i]);
    }
}
```

## Typy dla optymalizacji

### Register variables
```c
void fast_loop(void) {
    register uint32_t i;  // Sugestia dla kompilatora
    for(i = 0; i < 1000; i++) {
        // Szybki dostęp
    }
}
```

### Inline functions
```c
// Zamiast makr - bezpieczniejsze
static inline uint32_t read_register(volatile uint32_t *reg) {
    return *reg;
}

static inline void write_register(volatile uint32_t *reg, uint32_t value) {
    *reg = value;
}
```

## Rozmiary typów - podsumowanie

```c
sizeof(uint8_t)   // 1 bajt
sizeof(uint16_t)  // 2 bajty
sizeof(uint32_t)  // 4 bajty
sizeof(uint64_t)  // 8 bajtów

sizeof(bool)      // 1 bajt (z stdbool.h)

sizeof(float)     // 4 bajty
sizeof(double)    // 8 bajtów (często unikane!)

// Wskaźniki - zależą od architektury
sizeof(void*)     // 4 bajty na ARM Cortex-M (32-bit)
                  // 2 bajty na AVR (16-bit)
```

## Przykład praktyczny - konfiguracja GPIO

```c
#include <stdint.h>
#include <stdbool.h>

// Definicja struktury GPIO
typedef struct {
    volatile uint32_t MODER;
    volatile uint32_t OTYPER;
    volatile uint32_t OSPEEDR;
    volatile uint32_t PUPDR;
    volatile uint32_t IDR;
    volatile uint32_t ODR;
    volatile uint32_t BSRR;
    volatile uint32_t LCKR;
    volatile uint32_t AFR[2];
} GPIO_TypeDef;

#define GPIOA ((GPIO_TypeDef*)0x40020000)

// Enum dla trybu pinu
typedef enum {
    GPIO_MODE_INPUT  = 0,
    GPIO_MODE_OUTPUT = 1,
    GPIO_MODE_AF     = 2,
    GPIO_MODE_ANALOG = 3
} gpio_mode_t;

// Funkcja konfiguracji
void gpio_config_pin(GPIO_TypeDef *port, uint8_t pin, gpio_mode_t mode) {
    // Wyczyść bity
    port->MODER &= ~(3U << (pin * 2));
    // Ustaw nowy tryb
    port->MODER |= (mode << (pin * 2));
}

// Użycie
int main(void) {
    gpio_config_pin(GPIOA, 5, GPIO_MODE_OUTPUT);
    
    while(1) {
        GPIOA->ODR ^= (1 << 5);  // Toggle LED
    }
}
```

## Dobre praktyki

1. **Zawsze używaj stdint.h** dla dokładnych rozmiarów
2. **Używaj typedef** dla czytelności
3. **Dokumentuj zakres** wartości w komentarzach
4. **Unikaj double** jeśli nie ma FPU
5. **Pakuj struktury** tylko gdy konieczne
6. **Używaj const** dla danych tylko do odczytu
7. **Używaj volatile** dla rejestrów i danych współdzielonych

## Powiązane tematy
- [[volatile_keyword|Słowo kluczowe volatile]]
- [[const_keyword|Słowo kluczowe const]]
- [[operacje_rejestry|Operacje na rejestrach]]
- [[optymalizacja_pamieci|Optymalizacja wykorzystania pamięci]]
