# Operatory bitowe w Embedded C

## Wprowadzenie

Operatory bitowe to fundament programowania systemów wbudowanych. Umożliwiają bezpośrednią manipulację bitami w rejestrach sprzętowych, co jest kluczowe dla konfiguracji peryferiów mikrokontrolera.

## Podstawowe operatory bitowe

### AND (&) - iloczyn bitowy
```c
// Maskowanie - wyzerowanie bitów
uint8_t value = 0b11011010;
value = value & 0b00001111;  // Zostają tylko dolne 4 bity
// Wynik: 0b00001010

// Sprawdzenie pojedynczego bitu
uint8_t flags = 0b10100101;
if (flags & 0b00000100) {  // Czy bit 2 jest ustawiony?
    // Bit ustawiony
}

// Czyszczenie bitu
uint32_t reg = 0xFFFFFFFF;
reg &= ~(1 << 5);  // Wyczyść bit 5
// reg = 0xFFFFFFDF
```

### OR (|) - suma bitowa
```c
// Ustawianie bitów
uint8_t value = 0b00000000;
value = value | 0b00001111;  // Ustaw dolne 4 bity
// Wynik: 0b00001111

// Ustawienie pojedynczego bitu
uint32_t reg = 0x00000000;
reg |= (1 << 5);  // Ustaw bit 5
// reg = 0x00000020

// Ustawienie wielu bitów
reg |= (1 << 3) | (1 << 7) | (1 << 15);
```

### XOR (^) - różnica symetryczna
```c
// Przełączanie (toggle) bitów
uint8_t value = 0b10101010;
value = value ^ 0b11111111;  // Odwróć wszystkie bity
// Wynik: 0b01010101

// Toggle pojedynczego bitu
uint32_t reg = 0x00000020;
reg ^= (1 << 5);  // Toggle bit 5
// reg = 0x00000000

reg ^= (1 << 5);  // Toggle bit 5 ponownie
// reg = 0x00000020
```

### NOT (~) - negacja bitowa
```c
// Odwrócenie wszystkich bitów
uint8_t value = 0b10101010;
value = ~value;
// Wynik: 0b01010101

// Utworzenie maski
uint32_t mask = ~(1 << 5);  // Wszystkie bity = 1 oprócz bit 5
// mask = 0xFFFFFFDF

// Czyszczenie bitów
uint32_t reg = 0xFFFFFFFF;
reg &= ~(0b1111 << 4);  // Wyczyść bity 4-7
```

### Przesunięcia w lewo (<<)
```c
// Mnożenie przez potęgi 2
uint16_t value = 5;
value = value << 2;  // 5 * 4 = 20

// Tworzenie maski bitu
#define BIT0  (1 << 0)  // 0x0001
#define BIT5  (1 << 5)  // 0x0020
#define BIT15 (1 << 15) // 0x8000

// Ustawienie wartości w określonych bitach
uint32_t reg = 0;
reg |= (0b101 << 4);  // Ustaw bity 4-6 na 101
// reg = 0x00000050
```

### Przesunięcia w prawo (>>)
```c
// Dzielenie przez potęgi 2
uint16_t value = 20;
value = value >> 2;  // 20 / 4 = 5

// Ekstrakcja bitów
uint32_t reg = 0x12345678;
uint8_t high_byte = (reg >> 24) & 0xFF;  // 0x12

// Signed vs unsigned
int8_t signed_val = -8;  // 0b11111000
signed_val = signed_val >> 2;  // Arithmetic shift: 0b11111110 (-2)

uint8_t unsigned_val = 0b11111000;
unsigned_val = unsigned_val >> 2;  // Logical shift: 0b00111110 (62)
```

## Typowe wzorce w programowaniu embedded

### Ustawianie bitu
```c
// Makro dla czytelności
#define SET_BIT(reg, bit)   ((reg) |= (1U << (bit)))

// Użycie
uint32_t GPIOA_ODR = 0;
SET_BIT(GPIOA_ODR, 5);  // Ustaw bit 5
```

### Czyszczenie bitu
```c
#define CLEAR_BIT(reg, bit) ((reg) &= ~(1U << (bit)))

// Użycie
uint32_t GPIOA_ODR = 0xFFFFFFFF;
CLEAR_BIT(GPIOA_ODR, 5);  // Wyczyść bit 5
```

### Przełączanie bitu
```c
#define TOGGLE_BIT(reg, bit) ((reg) ^= (1U << (bit)))

// Użycie - miganie LED
while(1) {
    TOGGLE_BIT(GPIOA_ODR, 5);
    delay_ms(500);
}
```

### Sprawdzenie bitu
```c
#define READ_BIT(reg, bit)  (((reg) >> (bit)) & 1U)

// Użycie
if (READ_BIT(GPIOC_IDR, 13)) {
    // Przycisk wciśnięty (bit 13 = 1)
}
```

### Modyfikacja pola bitowego
```c
// Modyfikacja wielu bitów na raz
#define MODIFY_REG(reg, clear_mask, set_mask) \
    ((reg) = ((reg) & ~(clear_mask)) | (set_mask))

// Przykład: Konfiguracja GPIO MODE (2 bity na pin)
// Chcemy ustawić pin 5 jako output (01)
uint32_t GPIOA_MODER = 0;
MODIFY_REG(GPIOA_MODER, 
           0b11 << (5*2),      // Wyczyść bity 10-11
           0b01 << (5*2));     // Ustaw na 01 (output)
```

## Praktyczne przykłady z GPIO

### Konfiguracja pojedynczego pinu
```c
#include <stdint.h>

#define GPIOA_MODER   (*(volatile uint32_t*)0x40020000)
#define GPIOA_ODR     (*(volatile uint32_t*)0x40020014)

#define LED_PIN 5

void led_init(void) {
    // Konfiguruj pin 5 jako output (tryb 01)
    GPIOA_MODER &= ~(3 << (LED_PIN * 2));  // Wyczyść 2 bity
    GPIOA_MODER |= (1 << (LED_PIN * 2));   // Ustaw na 01
}

void led_on(void) {
    GPIOA_ODR |= (1 << LED_PIN);  // Ustaw bit
}

void led_off(void) {
    GPIOA_ODR &= ~(1 << LED_PIN);  // Wyczyść bit
}

void led_toggle(void) {
    GPIOA_ODR ^= (1 << LED_PIN);  // Toggle bit
}
```

### Konfiguracja wielu pinów
```c
// Definicje pinów
#define LED1_PIN  5
#define LED2_PIN  6
#define LED3_PIN  7

#define LED_MASK  ((1 << LED1_PIN) | (1 << LED2_PIN) | (1 << LED3_PIN))

void all_leds_on(void) {
    GPIOA_ODR |= LED_MASK;
}

void all_leds_off(void) {
    GPIOA_ODR &= ~LED_MASK;
}

void set_led_pattern(uint8_t pattern) {
    // Wyczyść wszystkie LED
    GPIOA_ODR &= ~LED_MASK;
    
    // Ustaw nowy wzór
    if (pattern & 0x01) GPIOA_ODR |= (1 << LED1_PIN);
    if (pattern & 0x02) GPIOA_ODR |= (1 << LED2_PIN);
    if (pattern & 0x04) GPIOA_ODR |= (1 << LED3_PIN);
}
```

## Operacje na rejestrach konfiguracyjnych

### Konfiguracja zegara systemowego
```c
#define RCC_CR        (*(volatile uint32_t*)0x40023800)
#define RCC_PLLCFGR   (*(volatile uint32_t*)0x40023804)

// Włącz HSE (High Speed External oscillator)
#define RCC_CR_HSEON  (1 << 16)
#define RCC_CR_HSERDY (1 << 17)

void enable_hse(void) {
    // Włącz HSE
    RCC_CR |= RCC_CR_HSEON;
    
    // Czekaj aż będzie gotowy
    while(!(RCC_CR & RCC_CR_HSERDY));
}

// Konfiguracja PLL
void configure_pll(void) {
    // PLL_M = 8, PLL_N = 336, PLL_P = 2, PLL_Q = 7
    RCC_PLLCFGR = (8 << 0)      // PLLM
                | (336 << 6)    // PLLN  
                | (0 << 16)     // PLLP (0 = /2)
                | (1 << 22)     // PLLSRC (HSE)
                | (7 << 24);    // PLLQ
}
```

### Konfiguracja UART
```c
#define USART1_CR1  (*(volatile uint32_t*)0x40011000)
#define USART1_BRR  (*(volatile uint32_t*)0x40011008)

// Bity kontrolne
#define USART_CR1_UE    (1 << 13)  // USART Enable
#define USART_CR1_TE    (1 << 3)   // Transmitter Enable
#define USART_CR1_RE    (1 << 2)   // Receiver Enable

void uart_init(void) {
    // Ustaw baudrate (przykład)
    USART1_BRR = 0x0683;  // 9600 baud @ 16MHz
    
    // Włącz UART, TX i RX
    USART1_CR1 |= USART_CR1_UE | USART_CR1_TE | USART_CR1_RE;
}
```

## Flagi i statusy

### Pojedyncze flagi
```c
typedef enum {
    FLAG_READY    = (1 << 0),  // 0x01
    FLAG_BUSY     = (1 << 1),  // 0x02
    FLAG_ERROR    = (1 << 2),  // 0x04
    FLAG_COMPLETE = (1 << 3)   // 0x08
} system_flags_t;

uint8_t status = 0;

// Ustawianie flag
status |= FLAG_READY;
status |= FLAG_COMPLETE;

// Sprawdzanie flag
if (status & FLAG_ERROR) {
    // Obsługa błędu
}

// Czyszczenie flag
status &= ~FLAG_ERROR;

// Sprawdzenie wielu flag naraz
if ((status & (FLAG_READY | FLAG_COMPLETE)) == (FLAG_READY | FLAG_COMPLETE)) {
    // Obie flagi ustawione
}
```

### Rejestry statusu
```c
#define USART_SR  (*(volatile uint32_t*)0x4001100C)

// Definicje bitów statusu
#define USART_SR_TXE   (1 << 7)   // TX Empty
#define USART_SR_RXNE  (1 << 5)   // RX Not Empty
#define USART_SR_TC    (1 << 6)   // Transmission Complete

void uart_send_byte(uint8_t byte) {
    // Czekaj aż TX buffer pusty
    while(!(USART_SR & USART_SR_TXE));
    
    USART_DR = byte;
    
    // Czekaj na zakończenie transmisji
    while(!(USART_SR & USART_SR_TC));
}

uint8_t uart_receive_byte(void) {
    // Czekaj na dane
    while(!(USART_SR & USART_SR_RXNE));
    
    return USART_DR;
}
```

## Ekstrakcja i wstawianie danych

### Ekstrakcja bajtów ze słowa
```c
uint32_t word = 0x12345678;

uint8_t byte0 = (word >> 0)  & 0xFF;  // 0x78
uint8_t byte1 = (word >> 8)  & 0xFF;  // 0x56
uint8_t byte2 = (word >> 16) & 0xFF;  // 0x34
uint8_t byte3 = (word >> 24) & 0xFF;  // 0x12
```

### Składanie słowa z bajtów
```c
uint8_t b0 = 0x78, b1 = 0x56, b2 = 0x34, b3 = 0x12;

uint32_t word = ((uint32_t)b3 << 24) |
                ((uint32_t)b2 << 16) |
                ((uint32_t)b1 << 8)  |
                ((uint32_t)b0 << 0);
// word = 0x12345678
```

### Ekstrakcja pól bitowych
```c
// Rejestr 32-bitowy z różnymi polami:
// [31:16] - Reserved
// [15:8]  - Data
// [7:4]   - Config
// [3:0]   - Status

uint32_t reg = 0x0000AB52;

uint8_t status = (reg >> 0) & 0x0F;   // 0x2
uint8_t config = (reg >> 4) & 0x0F;   // 0x5
uint8_t data   = (reg >> 8) & 0xFF;   // 0xAB
```

### Ustawienie pól bitowych
```c
uint32_t reg = 0;

// Ustaw Status (bity 0-3) na 0xA
reg &= ~(0x0F << 0);   // Wyczyść pole
reg |= (0x0A << 0);    // Ustaw nową wartość

// Ustaw Data (bity 8-15) na 0x5C
reg &= ~(0xFF << 8);
reg |= (0x5C << 8);

// reg = 0x00005C0A
```

## Optymalizacja operacji bitowych

### Sprawdzanie potęgi 2
```c
// Sprawdź czy liczba jest potęgą 2
bool is_power_of_2(uint32_t n) {
    return (n != 0) && ((n & (n - 1)) == 0);
}

// Przykłady:
// 8:   0b1000 & 0b0111 = 0b0000 ✓
// 7:   0b0111 & 0b0110 = 0b0110 ✗
// 16:  0b10000 & 0b01111 = 0b00000 ✓
```

### Liczenie ustawionych bitów
```c
// Algorytm Brian Kernighan
uint8_t count_set_bits(uint32_t n) {
    uint8_t count = 0;
    while(n) {
        n &= (n - 1);  // Usuń najmniej znaczący ustawiony bit
        count++;
    }
    return count;
}

// Przykład: n = 0b10110 (22)
// Iteracja 1: 0b10110 & 0b10101 = 0b10100, count=1
// Iteracja 2: 0b10100 & 0b10011 = 0b10000, count=2
// Iteracja 3: 0b10000 & 0b01111 = 0b00000, count=3
```

### Odwrócenie bitów
```c
uint32_t reverse_bits(uint32_t n) {
    uint32_t result = 0;
    for(int i = 0; i < 32; i++) {
        result <<= 1;
        result |= (n & 1);
        n >>= 1;
    }
    return result;
}
```

### Zamiana bajtów (endianness)
```c
uint32_t swap_bytes(uint32_t n) {
    return ((n >> 24) & 0x000000FF) |
           ((n >> 8)  & 0x0000FF00) |
           ((n << 8)  & 0x00FF0000) |
           ((n << 24) & 0xFF000000);
}

// 0x12345678 -> 0x78563412
```

## Pułapki i błędy

### Priorytet operatorów
```c
// ❌ ZŁE - & ma niższy priorytet niż ==
if (flags & FLAG_READY == 1) {  
    // To zostanie zinterpretowane jako:
    // if (flags & (FLAG_READY == 1))
}

// ✅ DOBRE - użyj nawiasów
if ((flags & FLAG_READY) != 0) {
    // Prawidłowe sprawdzenie
}
```

### Przesunięcia signed vs unsigned
```c
// Niebezpieczne z signed
int8_t val = -1;  // 0xFF
val >> 1;  // Może być 0xFF (arithmetic shift) lub 0x7F (logical)

// Bezpieczne z unsigned
uint8_t val = 0xFF;
val >> 1;  // Zawsze 0x7F (logical shift)
```

### Przesunięcia >= szerokości typu
```c
uint8_t val = 0xFF;
val << 8;  // Undefined behavior! Przesunięcie >= 8 bitów

// Bezpieczniej:
uint16_t result = ((uint16_t)val) << 8;
```

## Przykład kompleksowy - Sterownik LED RGB

```c
#include <stdint.h>

#define LED_PORT (*(volatile uint32_t*)0x40020014)

// Definicje pinów
#define LED_R_PIN  0
#define LED_G_PIN  1
#define LED_B_PIN  2

// Kolory
#define COLOR_OFF     0b000
#define COLOR_RED     0b001
#define COLOR_GREEN   0b010
#define COLOR_BLUE    0b100
#define COLOR_YELLOW  (COLOR_RED | COLOR_GREEN)
#define COLOR_CYAN    (COLOR_GREEN | COLOR_BLUE)
#define COLOR_MAGENTA (COLOR_RED | COLOR_BLUE)
#define COLOR_WHITE   (COLOR_RED | COLOR_GREEN | COLOR_BLUE)

void set_rgb_color(uint8_t color) {
    // Wyczyść wszystkie LED
    LED_PORT &= ~(0b111 << LED_R_PIN);
    
    // Ustaw nowy kolor
    LED_PORT |= (color << LED_R_PIN);
}

void rgb_demo(void) {
    const uint8_t colors[] = {
        COLOR_RED, COLOR_GREEN, COLOR_BLUE,
        COLOR_YELLOW, COLOR_CYAN, COLOR_MAGENTA,
        COLOR_WHITE, COLOR_OFF
    };
    
    for(uint8_t i = 0; i < 8; i++) {
        set_rgb_color(colors[i]);
        delay_ms(500);
    }
}
```

## Dobre praktyki

1. **Używaj nawiasów** w makrach
2. **Używaj typów unsigned** dla operacji bitowych
3. **Definiuj stałe** zamiast liczb magicznych
4. **Dokumentuj** znaczenie bitów
5. **Sprawdzaj zakresy** przy przesunięciach
6. **Używaj 1U** zamiast 1 dla przesunięć (unsigned)

## Powiązane tematy
- [[typy_danych_embedded_c|Typy danych w Embedded C]]
- [[operacje_rejestry|Operacje na rejestrach]]
- [[konfiguracja_gpio_c|Konfiguracja GPIO w C]]
