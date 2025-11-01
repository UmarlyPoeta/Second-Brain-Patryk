# Struktury i unie w Embedded C

## Wprowadzenie

Struktury i unie to kluczowe narzędzia do organizacji danych w systemach wbudowanych. Pozwalają grupować powiązane dane i efektywnie zarządzać pamięcią.

## Struktury (struct)

### Podstawowa definicja
```c
typedef struct {
    uint16_t temperature;  // Temperatura * 10
    uint16_t humidity;     // Wilgotność * 10
    uint32_t timestamp;    // Czas pomiaru
    uint8_t  status;       // Status sensora
} sensor_data_t;

sensor_data_t reading;
reading.temperature = 235;  // 23.5°C
reading.humidity = 655;     // 65.5%
```

### Struktury dla rejestrów
```c
typedef struct {
    volatile uint32_t CR1;    // Control Register 1
    volatile uint32_t CR2;    // Control Register 2
    volatile uint32_t SR;     // Status Register
    volatile uint32_t DR;     // Data Register
} USART_TypeDef;

#define USART1 ((USART_TypeDef*)0x40011000)

USART1->CR1 |= (1 << 13);  // Enable USART
```

## Unie (union)

### Dostęp do bajtów
```c
typedef union {
    uint32_t word;
    uint8_t bytes[4];
} word_bytes_t;

word_bytes_t data;
data.word = 0x12345678;
// data.bytes[0] = 0x78
// data.bytes[1] = 0x56
// data.bytes[2] = 0x34
// data.bytes[3] = 0x12
```

### Protokoły komunikacyjne
```c
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

## Packed structures

### Bez pakowania
```c
struct {
    uint8_t  a;    // 1 bajt + 3 padding
    uint32_t b;    // 4 bajty
    uint8_t  c;    // 1 bajt + 3 padding
} normal;  // 12 bajtów
```

### Z pakowaniem
```c
struct __attribute__((packed)) {
    uint8_t  a;    // 1 bajt
    uint32_t b;    // 4 bajty  
    uint8_t  c;    // 1 bajt
} packed;  // 6 bajtów
```

## Bitfieldy

### Efektywne pakowanie flag
```c
typedef struct {
    uint8_t flag1  : 1;  // 1 bit
    uint8_t flag2  : 1;  // 1 bit
    uint8_t value  : 4;  // 4 bity
    uint8_t unused : 2;  // 2 bity
} flags_t;  // Tylko 1 bajt

flags_t config;
config.flag1 = 1;
config.value = 0xA;
```

### Mapowanie rejestrów
```c
typedef struct {
    uint32_t MODE0  : 2;  // Bity 0-1
    uint32_t MODE1  : 2;  // Bity 2-3
    uint32_t MODE2  : 2;  // Bity 4-5
    // ...
} GPIO_MODER_bits_t;
```

## Wyrównanie i padding

### Kontrola wyrównania
```c
// Wyrównanie do 4 bajtów
typedef struct __attribute__((aligned(4))) {
    uint8_t data[100];
} aligned_buffer_t;

// Sprawdzenie
_Static_assert(sizeof(aligned_buffer_t) % 4 == 0, "Bad alignment");
```

## Przykłady praktyczne

### Konfiguracja pinu
```c
typedef struct {
    GPIO_TypeDef *port;
    uint8_t pin;
    uint8_t mode;
    uint8_t pull;
} gpio_config_t;

const gpio_config_t led_config = {
    .port = GPIOA,
    .pin = 5,
    .mode = GPIO_MODE_OUTPUT,
    .pull = GPIO_NOPULL
};
```

### Ring buffer
```c
typedef struct {
    uint8_t *buffer;
    uint16_t size;
    volatile uint16_t head;
    volatile uint16_t tail;
} ring_buffer_t;

ring_buffer_t uart_buffer;
```

## Powiązane tematy
- [[typy_danych_embedded_c|Typy danych]]
- [[wskazniki_adresowanie|Wskaźniki]]
- [[operacje_rejestry|Operacje na rejestrach]]
