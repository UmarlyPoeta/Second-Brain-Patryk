# STM32F429I - Bare Metal - Podstawy i Architektura Rejestrów

## 🔧 Programowanie Bare Metal

### Czym jest Bare Metal?
Bare metal to programowanie mikrokontrolera bezpośrednio na poziomie rejestrów sprzętowych, bez użycia bibliotek HAL czy LL. Daje to:
- **Pełną kontrolę** nad każdym bitem
- **Minimalne zużycie pamięci** - brak nadmiarowego kodu bibliotek
- **Maksymalną wydajność** - brak warstw abstrakcji
- **Głębokie zrozumienie** działania sprzętu

### Dlaczego warto uczyć się bare metal?
1. **Zrozumienie hardware** - widzisz dokładnie co dzieje się w układzie
2. **Debugging** - łatwiej znaleźć problemy gdy znasz rejestry
3. **Optymalizacja** - możesz napisać kod bardziej efektywny niż HAL
4. **Uniwersalność** - umiejętności przenoszą się na inne mikrokontrolery

## 📋 Struktura Pamięci STM32F429I

### Mapa Pamięci (Memory Map)

```
0x0000 0000 ┌──────────────────┐
            │  FLASH (2 MB)    │  Program + Dane stałe
0x0800 0000 ├──────────────────┤
            │                  │
0x1FFF 0000 ├──────────────────┤
            │  System Memory   │  Bootloader
0x1FFF 7FFF ├──────────────────┤
            │                  │
0x2000 0000 ├──────────────────┤
            │  SRAM (256 KB)   │  Zmienne, stack, heap
0x2003 FFFF ├──────────────────┤
            │                  │
0x4000 0000 ├──────────────────┤
            │  Peripherals     │  Rejestry peryferiów
0x5FFF FFFF ├──────────────────┤
            │                  │
0xE000 0000 ├──────────────────┤
            │  Cortex-M4       │  Rejestry procesora
0xFFFF FFFF └──────────────────┘
```

### Adresy Bazowe Peryferiów

```c
/**
 * @brief  Podstawowe adresy bazowe
 */
#define PERIPH_BASE           0x40000000UL  // Baza peryferiów
#define APB1PERIPH_BASE       PERIPH_BASE
#define APB2PERIPH_BASE       (PERIPH_BASE + 0x00010000UL)
#define AHB1PERIPH_BASE       (PERIPH_BASE + 0x00020000UL)
#define AHB2PERIPH_BASE       (PERIPH_BASE + 0x10000000UL)

// Przykłady adresów peryferiów
#define GPIOA_BASE            (AHB1PERIPH_BASE + 0x0000UL)
#define GPIOB_BASE            (AHB1PERIPH_BASE + 0x0400UL)
#define RCC_BASE              (AHB1PERIPH_BASE + 0x3800UL)
#define USART1_BASE           (APB2PERIPH_BASE + 0x1000UL)
#define TIM2_BASE             (APB1PERIPH_BASE + 0x0000UL)
```

## 🗂️ Rejestry - Podstawy

### Co to jest Rejestr?
Rejestr to specjalna lokacja pamięci o określonym adresie, która kontroluje funkcje peryferyjnego. Każdy bit w rejestrze ma konkretne znaczenie.

### Przykład: Rejestr GPIO MODER

```
GPIO Port Mode Register (GPIOx_MODER)
Offset: 0x00
Reset value: 0xA8000000 (dla GPIOA)

31  30  29  28  27  26  25  24  23  22  21  20  19  18  17  16
[MODER15 ][MODER14 ][MODER13 ][MODER12 ][MODER11 ][MODER10 ][MODER9][MODER8]

15  14  13  12  11  10  9   8   7   6   5   4   3   2   1   0
[MODER7 ][MODER6 ][MODER5 ][MODER4 ][MODER3 ][MODER2 ][MODER1][MODER0]

MODERy[1:0]: Tryb dla pinu y
  00: Input
  01: Output
  10: Alternate function
  11: Analog
```

### Dostęp do Rejestrów - Podstawy

```c
/**
 * @brief  Definicje typów dla rejestrów
 */
typedef unsigned int uint32_t;
typedef unsigned short uint16_t;
typedef unsigned char uint8_t;

/**
 * @brief  Volatile - WAŻNE!
 * 
 * Słowo kluczowe 'volatile' informuje kompilator że wartość
 * może się zmienić z zewnątrz (hardware) i nie może być
 * optymalizowana.
 */
#define __IO volatile

/**
 * @brief  Struktura GPIO (uproszczona)
 */
typedef struct {
    __IO uint32_t MODER;    // Mode register               Offset: 0x00
    __IO uint32_t OTYPER;   // Output type register        Offset: 0x04
    __IO uint32_t OSPEEDR;  // Output speed register       Offset: 0x08
    __IO uint32_t PUPDR;    // Pull-up/pull-down register  Offset: 0x0C
    __IO uint32_t IDR;      // Input data register         Offset: 0x10
    __IO uint32_t ODR;      // Output data register        Offset: 0x14
    __IO uint32_t BSRR;     // Bit set/reset register      Offset: 0x18
    __IO uint32_t LCKR;     // Configuration lock register Offset: 0x1C
    __IO uint32_t AFR[2];   // Alternate function registers Offset: 0x20-0x24
} GPIO_TypeDef;

/**
 * @brief  Wskaźnik do struktury GPIO
 */
#define GPIOA  ((GPIO_TypeDef *) GPIOA_BASE)
#define GPIOB  ((GPIO_TypeDef *) GPIOB_BASE)
#define GPIOC  ((GPIO_TypeDef *) GPIOC_BASE)
```

## 🔨 Operacje Bitowe - Podstawy

### Podstawowe Operacje

```c
/**
 * @brief  Operacje bitowe używane w bare metal
 */

// 1. Ustawienie bitu (Set bit)
// Użycie: Włącz funkcję
register |= (1 << bit_position);
// Przykład: Włącz pin 5
GPIOA->BSRR = (1 << 5);

// 2. Wyczyszczenie bitu (Clear bit)
// Użycie: Wyłącz funkcję
register &= ~(1 << bit_position);
// Przykład: Wyczyść bit 3
GPIOA->MODER &= ~(1 << 3);

// 3. Toggle bit (Przełącz bit)
// Użycie: Zmień stan bitu
register ^= (1 << bit_position);
// Przykład: Toggle pin 5
GPIOA->ODR ^= (1 << 5);

// 4. Test bitu (Sprawdź bit)
// Użycie: Czy bit jest ustawiony?
if (register & (1 << bit_position)) {
    // Bit jest ustawiony
}

// 5. Ustawienie wielu bitów (Set multiple bits)
// Użycie: Ustaw bity 2, 3, 5
register |= ((1 << 2) | (1 << 3) | (1 << 5));

// 6. Maskowanie (Masking)
// Użycie: Ustaw bity według maski
register = (register & ~mask) | (value & mask);
```

### Praktyczne Przykłady

```c
/**
 * @brief  Przykład 1: Ustawienie trybu output dla pinu 5
 * 
 * MODER5[1:0] = 01 (Output mode)
 * Bity 10-11 w rejestrze MODER
 */
void Set_PA5_Output_Manual(void)
{
    // Krok 1: Wyczyść bity MODER5 (bity 10-11)
    GPIOA->MODER &= ~(0x3 << 10);  // 0x3 = 0b11, wyczyść oba bity
    
    // Krok 2: Ustaw MODER5 = 01 (output)
    GPIOA->MODER |= (0x1 << 10);   // 0x1 = 0b01, ustaw bit 10
}

/**
 * @brief  Przykład 2: Czytanie stanu pinu
 */
uint8_t Read_PA0(void)
{
    // Sprawdź bit 0 w IDR
    if (GPIOA->IDR & (1 << 0)) {
        return 1;  // Pin HIGH
    } else {
        return 0;  // Pin LOW
    }
}

/**
 * @brief  Przykład 3: Atomic set/reset przez BSRR
 * 
 * BSRR jest specjalnym rejestrem:
 * Bity 0-15: Set (BS) - ustawienie odpowiedniego pinu
 * Bity 16-31: Reset (BR) - reset odpowiedniego pinu
 */
void Atomic_GPIO_Operations(void)
{
    // Ustaw pin 5 (bit 5)
    GPIOA->BSRR = (1 << 5);
    
    // Reset pin 5 (bit 21 = 16 + 5)
    GPIOA->BSRR = (1 << 21);
    
    // Jednocześnie: Ustaw pin 3, reset pin 7
    GPIOA->BSRR = (1 << 3) | (1 << (16 + 7));
}
```

## 📖 Czytanie Reference Manual

### Jak Znaleźć Informacje?

```
1. Otwórz "RM0090 Reference Manual" dla STM32F429

2. Znajdź rozdział dla peryferyjnego (np. "GPIO")

3. Szukaj sekcji "Register description"

4. Dla każdego rejestru znajdziesz:
   - Offset (przesunięcie od adresu bazowego)
   - Reset value (wartość po resecie)
   - Opis każdego bitu
   - Prawa dostępu (R/W, RO, WO)

Przykład dla GPIOA_MODER:
Address offset: 0x00
Reset value: 0xA8000000
Bits 31:0 MODER[15:0]: Port x configuration bits
```

### Przykład Dekodowania z RM

```c
/**
 * @brief  Przykład z Reference Manual
 * 
 * GPIO port output speed register (GPIOx_OSPEEDR)
 * 
 * Address offset: 0x08
 * Reset value: 0x00000000 (0x000000C0 dla port A)
 * 
 * Bits 2y+1:2y OSPEEDRy[1:0]: Port x configuration bits (y = 0..15)
 * 00: Low speed
 * 01: Medium speed
 * 10: High speed
 * 11: Very high speed
 */

void Set_PA5_HighSpeed(void)
{
    // Pin 5 -> bity 10-11 w OSPEEDR
    // Ustaw na 10 (High speed)
    
    GPIOA->OSPEEDR &= ~(0x3 << 10);  // Wyczyść
    GPIOA->OSPEEDR |= (0x2 << 10);   // Ustaw 10
}
```

## 🎯 Pierwszy Program Bare Metal

### Minimalny LED Blink

```c
/**
 * @brief  Kompletny przykład LED blink bez HAL
 * 
 * Cel: Miganie LED na pinie PA5
 * 
 * Kroki:
 * 1. Włącz zegar dla GPIOA
 * 2. Skonfiguruj PA5 jako output
 * 3. Toggle PA5 w pętli
 */

// Definicje adresów
#define RCC_BASE              0x40023800UL
#define GPIOA_BASE            0x40020000UL

// Struktury
typedef struct {
    __IO uint32_t CR;
    __IO uint32_t PLLCFGR;
    __IO uint32_t CFGR;
    __IO uint32_t CIR;
    __IO uint32_t AHB1RSTR;
    __IO uint32_t AHB2RSTR;
    __IO uint32_t AHB3RSTR;
    uint32_t RESERVED0;
    __IO uint32_t APB1RSTR;
    __IO uint32_t APB2RSTR;
    uint32_t RESERVED1[2];
    __IO uint32_t AHB1ENR;     // Offset 0x30
    __IO uint32_t AHB2ENR;
    __IO uint32_t AHB3ENR;
    uint32_t RESERVED2;
    __IO uint32_t APB1ENR;
    __IO uint32_t APB2ENR;
    // ... inne rejestry
} RCC_TypeDef;

#define RCC    ((RCC_TypeDef *) RCC_BASE)
#define GPIOA  ((GPIO_TypeDef *) GPIOA_BASE)

/**
 * @brief  Prosta funkcja delay (bardzo niedokładna!)
 */
void delay_ms(uint32_t ms)
{
    // Przy 16 MHz HSI (domyślny zegar), ~2000 iteracji ≈ 1ms
    for (uint32_t i = 0; i < ms * 2000; i++) {
        __asm("nop");  // No operation
    }
}

/**
 * @brief  Główna funkcja
 */
int main(void)
{
    // Krok 1: Włącz zegar dla GPIOA
    // Bit 0 w RCC_AHB1ENR włącza GPIOA
    RCC->AHB1ENR |= (1 << 0);
    
    // Krok 2: Skonfiguruj PA5 jako output
    // MODER5[1:0] = 01
    GPIOA->MODER &= ~(0x3 << 10);  // Wyczyść bity 10-11
    GPIOA->MODER |= (0x1 << 10);   // Ustaw bit 10
    
    // Krok 3: Ustaw prędkość (opcjonalne)
    GPIOA->OSPEEDR &= ~(0x3 << 10);
    GPIOA->OSPEEDR |= (0x2 << 10);  // High speed
    
    // Krok 4: Główna pętla
    while (1) {
        // Toggle pin 5
        GPIOA->ODR ^= (1 << 5);
        
        // Lub użyj BSRR (lepiej):
        // GPIOA->BSRR = (1 << 5);    // Set
        // delay_ms(500);
        // GPIOA->BSRR = (1 << 21);   // Reset
        
        delay_ms(500);
    }
    
    return 0;
}
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_gpio|Bare Metal - GPIO szczegółowo]]
- [[stm32f429i_bare_metal_clock|Bare Metal - System zegarowy]]
- [[stm32f429i_bare_metal_startup|Bare Metal - Startup i inicjalizacja]]
- [[stm32f429i_wprowadzenie|STM32F429I - Wprowadzenie]]

## 📝 Kluczowe Pojęcia

### Memory-Mapped I/O
Peryferia są dostępne przez adresy pamięci. Zapis/odczyt z adresu = operacja na sprzęcie.

### Volatile
```c
volatile uint32_t *reg = (uint32_t *)0x40020014;
```
Bez `volatile` kompilator może "zoptymalizować" kod i nie wykonać operacji!

### Atomic Operations
BSRR pozwala atomowo (bez możliwości przerwania) ustawić/zresetować pin - bezpieczne dla przerwań.

### Struktura Danych
Używamy struktur C do reprezentacji bloków rejestrów - łatwiejszy dostęp niż bezpośrednie adresy.

---

*Następna notatka: [[stm32f429i_bare_metal_gpio|Bare Metal GPIO - Kompletny Przewodnik]]*
