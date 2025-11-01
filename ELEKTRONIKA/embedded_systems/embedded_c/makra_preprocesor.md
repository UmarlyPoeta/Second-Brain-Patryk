# Makra preprocesora w Embedded C

## Wprowadzenie

Preprocesor C to potężne narzędzie w programowaniu systemów wbudowanych. Pozwala na definiowanie stałych, makr funkcyjnych i warunkowej kompilacji - wszystko bez narzutu runtime!

## Dyrektywy preprocesora

### #define - podstawowe stałe
```c
#define LED_PIN 5
#define MAX_BUFFER_SIZE 256
#define TIMEOUT_MS 1000
#define PI 3.14159f

// Użycie
uint8_t buffer[MAX_BUFFER_SIZE];
delay_ms(TIMEOUT_MS);
```

### #define - makra funkcyjne
```c
// Proste makra
#define SET_BIT(reg, bit)    ((reg) |= (1U << (bit)))
#define CLEAR_BIT(reg, bit)  ((reg) &= ~(1U << (bit)))
#define TOGGLE_BIT(reg, bit) ((reg) ^= (1U << (bit)))
#define READ_BIT(reg, bit)   (((reg) >> (bit)) & 1U)

// Użycie
SET_BIT(GPIOA->ODR, 5);      // LED ON
CLEAR_BIT(GPIOA->ODR, 5);    // LED OFF
TOGGLE_BIT(GPIOA->ODR, 5);   // LED Toggle
```

### Makra z parametrami
```c
// Makro maksimum/minimum
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

// Ograniczenie wartości
#define CLAMP(value, min, max) \
    (((value) < (min)) ? (min) : (((value) > (max)) ? (max) : (value)))

// Użycie
uint16_t result = MAX(sensor1, sensor2);
pwm_value = CLAMP(input, 0, 255);
```

## Kompilacja warunkowa

### #ifdef / #ifndef
```c
#define DEBUG

#ifdef DEBUG
    #define DEBUG_PRINT(msg) uart_send_string(msg)
#else
    #define DEBUG_PRINT(msg)  // Pusty w release
#endif

// W kodzie
DEBUG_PRINT("Sensor initialized\n");
```

### #if defined
```c
#if defined(STM32F4)
    #define SYSTEM_CLOCK 168000000
#elif defined(STM32F1)
    #define SYSTEM_CLOCK 72000000
#else
    #error "Nieznany mikrokontroler!"
#endif
```

### #pragma once
```c
// Zamiast include guards
#pragma once

// Lub tradycyjnie:
#ifndef MY_HEADER_H
#define MY_HEADER_H

// Zawartość pliku .h

#endif
```

## Makra dla rejestrów

### Definiowanie rejestrów
```c
// Base addresses
#define PERIPH_BASE     0x40000000UL
#define AHB1PERIPH_BASE (PERIPH_BASE + 0x00020000UL)
#define GPIOA_BASE      (AHB1PERIPH_BASE + 0x0000UL)

// Register access
#define GPIOA_MODER   (*(volatile uint32_t*)(GPIOA_BASE + 0x00))
#define GPIOA_ODR     (*(volatile uint32_t*)(GPIOA_BASE + 0x14))

// Bit definitions
#define GPIO_PIN_0  (1 << 0)
#define GPIO_PIN_5  (1 << 5)
#define GPIO_PIN_13 (1 << 13)
```

### Makra konfiguracyjne
```c
#define GPIO_MODE_MASK(pin)  (3UL << ((pin) * 2))
#define GPIO_MODE_INPUT(pin) (0UL << ((pin) * 2))
#define GPIO_MODE_OUTPUT(pin) (1UL << ((pin) * 2))

// Użycie
GPIOA_MODER &= ~GPIO_MODE_MASK(5);
GPIOA_MODER |= GPIO_MODE_OUTPUT(5);
```

## Makra pomocnicze

### Konwersje jednostek
```c
#define MS_TO_TICKS(ms)  ((ms) * (SYSTEM_CLOCK / 1000))
#define US_TO_CYCLES(us) ((us) * (SYSTEM_CLOCK / 1000000))
#define KHZ_TO_HZ(khz)   ((khz) * 1000)
#define MHZ_TO_HZ(mhz)   ((mhz) * 1000000)

// Konwersja ADC
#define ADC_TO_MV(adc)   (((adc) * 3300) / 4095)
#define MV_TO_ADC(mv)    (((mv) * 4095) / 3300)
```

### Operacje matematyczne
```c
#define ABS(x)           (((x) < 0) ? -(x) : (x))
#define SQUARE(x)        ((x) * (x))
#define IS_POWER_OF_2(x) (((x) != 0) && (((x) & ((x) - 1)) == 0))

// Zaokrąglanie
#define ROUND_UP(n, align)   (((n) + (align) - 1) & ~((align) - 1))
#define ROUND_DOWN(n, align) ((n) & ~((align) - 1))
```

## Debugging makra

### Assert
```c
#ifdef DEBUG
    #define ASSERT(expr) \
        do { \
            if(!(expr)) { \
                debug_assert_failed(__FILE__, __LINE__); \
                while(1); \
            } \
        } while(0)
#else
    #define ASSERT(expr) ((void)0)
#endif

// Użycie
ASSERT(value < MAX_VALUE);
ASSERT(ptr != NULL);
```

### Debug print
```c
#ifdef DEBUG
    #define LOG(fmt, ...) printf("[%s:%d] " fmt "\n", __FILE__, __LINE__, ##__VA_ARGS__)
#else
    #define LOG(fmt, ...) ((void)0)
#endif

// Użycie
LOG("Temperature: %d", temp);
```

## Bezpieczeństwo makr

### Problem z makrami
```c
// ❌ ZŁE makro
#define SQUARE(x) x * x

int result = SQUARE(2 + 3);  // 2 + 3 * 2 + 3 = 11, nie 25!

// ✅ DOBRE makro - z nawiasami
#define SQUARE(x) ((x) * (x))

int result = SQUARE(2 + 3);  // (2 + 3) * (2 + 3) = 25
```

### Efekty uboczne
```c
// ❌ Niebezpieczne z efektami ubocznymi
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int x = 5;
int result = MAX(x++, 10);  // x++ wykonane 2 razy!

// ✅ Bezpieczniejsze (C99+)
static inline int max(int a, int b) {
    return (a > b) ? a : b;
}
```

## Stringifikacja i konkatenacja

### Operator #
```c
#define TO_STRING(x) #x

const char *pin_name = TO_STRING(GPIO_PIN_5);  // "GPIO_PIN_5"
```

### Operator ##
```c
#define CONCAT(a, b) a##b

uint32_t CONCAT(value_, 1) = 100;  // value_1 = 100
CONCAT(GPIOA, _ODR) = 0x20;        // GPIOA_ODR = 0x20
```

### Praktyczne przykłady
```c
#define GPIO_PIN_DEF(port, pin) \
    GPIO##port##_ODR |= (1 << pin)

GPIO_PIN_DEF(A, 5);  // GPIOA_ODR |= (1 << 5)
```

## Multi-line makra

### Do-while trick
```c
// ✅ Bezpieczne makro wieloliniowe
#define SWAP(a, b) \
    do { \
        typeof(a) temp = (a); \
        (a) = (b); \
        (b) = temp; \
    } while(0)

// Działa poprawnie nawet w if bez nawiasów
if(condition)
    SWAP(x, y);
else
    // ...
```

## Przydatne wzorce

### Konfiguracja GPIO
```c
#define GPIO_CONFIG_OUTPUT(port, pin) \
    do { \
        port->MODER &= ~(3UL << ((pin) * 2)); \
        port->MODER |= (1UL << ((pin) * 2)); \
    } while(0)

GPIO_CONFIG_OUTPUT(GPIOA, 5);
```

### Delay z optimizacją
```c
#define NOP() __asm__ volatile("nop")

#define DELAY_US(us) \
    do { \
        for(volatile uint32_t i = 0; i < (us) * (SYSTEM_CLOCK / 1000000 / 4); i++) { \
            NOP(); \
        } \
    } while(0)
```

## Powiązane tematy
- [[typy_danych_embedded_c|Typy danych]]
- [[operatory_bitowe|Operatory bitowe]]
- [[dobre_praktyki_embedded_c|Dobre praktyki]]
