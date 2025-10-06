# STM32F429I - Bare Metal - GPIO Kompletny Przewodnik

## 📋 Rejestry GPIO - Szczegółowy Opis

### Struktura Kompletna GPIO

```c
/**
 * @brief  Kompletna struktura GPIO z wszystkimi rejestrami
 * 
 * Baza dla GPIOA: 0x40020000
 * Baza dla GPIOB: 0x40020400
 * Baza dla GPIOC: 0x40020800
 * itd. (offset +0x400 dla każdego portu)
 */
typedef struct {
    __IO uint32_t MODER;      // 0x00: Mode register
    __IO uint32_t OTYPER;     // 0x04: Output type register
    __IO uint32_t OSPEEDR;    // 0x08: Output speed register
    __IO uint32_t PUPDR;      // 0x0C: Pull-up/pull-down register
    __IO uint32_t IDR;        // 0x10: Input data register
    __IO uint32_t ODR;        // 0x14: Output data register
    __IO uint32_t BSRR;       // 0x18: Bit set/reset register
    __IO uint32_t LCKR;       // 0x1C: Configuration lock register
    __IO uint32_t AFR[2];     // 0x20: Alternate function low/high register
} GPIO_TypeDef;

// Definicje wskaźników
#define GPIOA  ((GPIO_TypeDef *) 0x40020000UL)
#define GPIOB  ((GPIO_TypeDef *) 0x40020400UL)
#define GPIOC  ((GPIO_TypeDef *) 0x40020800UL)
#define GPIOD  ((GPIO_TypeDef *) 0x40020C00UL)
#define GPIOE  ((GPIO_TypeDef *) 0x40021000UL)
#define GPIOF  ((GPIO_TypeDef *) 0x40021400UL)
#define GPIOG  ((GPIO_TypeDef *) 0x40021800UL)
#define GPIOH  ((GPIO_TypeDef *) 0x40021C00UL)
#define GPIOI  ((GPIO_TypeDef *) 0x40022000UL)
#define GPIOJ  ((GPIO_TypeDef *) 0x40022400UL)
#define GPIOK  ((GPIO_TypeDef *) 0x40022800UL)
```

## 🔧 Rejestr 1: MODER (Mode Register)

### Opis Rejestru

```
GPIOx_MODER - Port mode register
Offset: 0x00
Reset value: 0xA8000000 (GPIOA), 0x00000280 (GPIOB), 0x00000000 (inne)

Bit layout (każdy pin ma 2 bity):
31 30 | 29 28 | ... | 3 2 | 1 0
[P15 ] [P14 ]  ...  [P1] [P0]

Wartości dla każdego pinu:
00: Input mode (reset state)
01: General purpose output mode
10: Alternate function mode
11: Analog mode
```

### Przykład Konfiguracji

```c
/**
 * @brief  Krok po kroku: Konfiguracja PA5 jako output
 */
void Configure_PA5_Output_StepByStep(void)
{
    // Pin 5 używa bitów 10-11 w MODER
    // Pozycja = pin_number * 2
    
    // KROK 1: Zrozumienie początkowej wartości
    uint32_t current_moder = GPIOA->MODER;
    // current_moder = 0xA8000000
    // W binarnym: 1010 1000 0000 0000 0000 0000 0000 0000
    
    // KROK 2: Przygotowanie maski dla bitów 10-11
    uint32_t mask = 0x3 << 10;  // 0x3 = 0b11
    // mask = 0000 0000 0000 0000 0000 1100 0000 0000 = 0x00000C00
    
    // KROK 3: Wyczyść bity 10-11
    GPIOA->MODER &= ~mask;
    // To samo co: GPIOA->MODER = GPIOA->MODER & (~mask)
    // ~mask = 1111 1111 1111 1111 1111 0011 1111 1111
    // Wynik: Bity 10-11 są teraz 00
    
    // KROK 4: Ustaw wartość 01 (output) w bitach 10-11
    uint32_t value = 0x1 << 10;  // 0x1 = 0b01
    // value = 0000 0000 0000 0000 0000 0100 0000 0000 = 0x00000400
    GPIOA->MODER |= value;
    // Wynik: Bity 10-11 = 01 = Output mode
}

/**
 * @brief  Konfiguracja wielu pinów jednocześnie
 */
void Configure_Multiple_Pins(void)
{
    // Konfiguruj PA5, PA6, PA7 jako output
    // PA5: bity 10-11 = 01
    // PA6: bity 12-13 = 01
    // PA7: bity 14-15 = 01
    
    // SPOSÓB 1: Po kolei (mniej efektywny)
    GPIOA->MODER &= ~(0x3 << 10);
    GPIOA->MODER |= (0x1 << 10);
    GPIOA->MODER &= ~(0x3 << 12);
    GPIOA->MODER |= (0x1 << 12);
    GPIOA->MODER &= ~(0x3 << 14);
    GPIOA->MODER |= (0x1 << 14);
    
    // SPOSÓB 2: Wszystko razem (lepszy)
    uint32_t clear_mask = (0x3 << 10) | (0x3 << 12) | (0x3 << 14);
    uint32_t set_value = (0x1 << 10) | (0x1 << 12) | (0x1 << 14);
    
    GPIOA->MODER &= ~clear_mask;  // Wyczyść wszystkie
    GPIOA->MODER |= set_value;    // Ustaw wszystkie
    
    // SPOSÓB 3: Atomic (najlepszy)
    GPIOA->MODER = (GPIOA->MODER & ~clear_mask) | set_value;
}

/**
 * @brief  Wszystkie tryby pinów
 */
void Configure_All_Modes(void)
{
    // Input mode - PA0
    GPIOA->MODER &= ~(0x3 << 0);  // 00
    
    // Output mode - PA1
    GPIOA->MODER &= ~(0x3 << 2);
    GPIOA->MODER |= (0x1 << 2);   // 01
    
    // Alternate function - PA2
    GPIOA->MODER &= ~(0x3 << 4);
    GPIOA->MODER |= (0x2 << 4);   // 10
    
    // Analog mode - PA3
    GPIOA->MODER &= ~(0x3 << 6);
    GPIOA->MODER |= (0x3 << 6);   // 11
}
```

## 🔧 Rejestr 2: OTYPER (Output Type Register)

### Opis Rejestru

```
GPIOx_OTYPER - Port output type register
Offset: 0x04
Reset value: 0x00000000

Bit layout (każdy pin ma 1 bit):
31..16: Reserved
15 14 13 ... 2 1 0
[P15][P14][P13]...[P2][P1][P0]

Wartości:
0: Output push-pull (domyślnie)
1: Output open-drain
```

### Wyjaśnienie Push-Pull vs Open-Drain

```
PUSH-PULL:
  VDD ----[PMOS]----+---- Pin
                    |
  GND ----[NMOS]----+

  - Może "pchać" (push) do VDD
  - Może "ciągnąć" (pull) do GND
  - Silny stan HIGH i LOW
  - Dla większości zastosowań

OPEN-DRAIN:
  VDD
   |
  [External Pull-up]
   |
  Pin ----[NMOS]---- GND

  - Tylko "ciągnie" do GND
  - Wymaga zewnętrznego rezystora pull-up
  - Używane dla I2C, 1-Wire
  - Pozwala na wired-AND (kilka urządzeń na jednej linii)
```

### Przykład Konfiguracji

```c
/**
 * @brief  Konfiguracja output type
 */
void Configure_Output_Type(void)
{
    // PA5 jako push-pull (domyślnie)
    GPIOA->OTYPER &= ~(1 << 5);  // Bit 5 = 0
    
    // PA6 jako open-drain
    GPIOA->OTYPER |= (1 << 6);   // Bit 6 = 1
}

/**
 * @brief  Przykład: I2C wymaga open-drain
 */
void Configure_I2C_Pins_OpenDrain(void)
{
    // I2C1: PB8 = SCL, PB9 = SDA
    
    // Krok 1: Ustaw jako alternate function
    GPIOB->MODER &= ~((0x3 << 16) | (0x3 << 18));
    GPIOB->MODER |= ((0x2 << 16) | (0x2 << 18));
    
    // Krok 2: Ustaw jako open-drain (WYMAGANE dla I2C!)
    GPIOB->OTYPER |= (1 << 8) | (1 << 9);
    
    // Krok 3: Ustaw alternate function (AF4 dla I2C1)
    // (omówione później w AFR)
}
```

## 🔧 Rejestr 3: OSPEEDR (Output Speed Register)

### Opis Rejestru

```
GPIOx_OSPEEDR - Port output speed register
Offset: 0x08
Reset value: 0x00000000 (0x000000C0 dla GPIOA)

Bit layout (każdy pin ma 2 bity):
31 30 | 29 28 | ... | 3 2 | 1 0
[P15 ] [P14 ]  ...  [P1] [P0]

Wartości:
00: Low speed (2 MHz)
01: Medium speed (25 MHz)
10: High speed (50 MHz)
11: Very high speed (100 MHz)
```

### Kiedy Jaką Prędkość?

```c
/**
 * @brief  Wybór prędkości pinu
 * 
 * ZASADY:
 * - Wyższa prędkość = większe zużycie prądu + EMI
 * - Używaj najniższej prędkości która działa
 * 
 * ZASTOSOWANIA:
 * Low (2 MHz):     LED, przyciski, wolne sygnały
 * Medium (25 MHz): UART do 115200, I2C Fast Mode
 * High (50 MHz):   SPI do 10 MHz, UART szybki
 * Very High:       Wysokie częstotliwości, Ethernet, LCD
 */

void Configure_Speed_Examples(void)
{
    // LED (PA5) - Low speed wystarczy
    GPIOA->OSPEEDR &= ~(0x3 << 10);
    GPIOA->OSPEEDR |= (0x0 << 10);  // 00 = Low
    
    // UART TX (PA9) - Medium speed dla 115200 baud
    GPIOA->OSPEEDR &= ~(0x3 << 18);
    GPIOA->OSPEEDR |= (0x1 << 18);  // 01 = Medium
    
    // SPI CLK (PA5) - High speed dla 10 MHz SPI
    GPIOA->OSPEEDR &= ~(0x3 << 10);
    GPIOA->OSPEEDR |= (0x2 << 10);  // 10 = High
    
    // Ethernet (PG13) - Very high speed
    GPIOG->OSPEEDR &= ~(0x3 << 26);
    GPIOG->OSPEEDR |= (0x3 << 26);  // 11 = Very High
}
```

## 🔧 Rejestr 4: PUPDR (Pull-Up/Pull-Down Register)

### Opis Rejestru

```
GPIOx_PUPDR - Port pull-up/pull-down register
Offset: 0x0C
Reset value: 0x64000000 (GPIOA), 0x00000100 (GPIOB), 0x00000000 (inne)

Bit layout (każdy pin ma 2 bity):
31 30 | 29 28 | ... | 3 2 | 1 0
[P15 ] [P14 ]  ...  [P1] [P0]

Wartości:
00: No pull-up, no pull-down
01: Pull-up
10: Pull-down
11: Reserved
```

### Wyjaśnienie Pull-Up/Pull-Down

```
NO PULL-UP/DOWN:
  Pin ------ (floating)
  - Nieokreślony stan gdy nic nie podłączone
  - Używaj dla outputów lub gdy external pull jest

PULL-UP:
  VDD
   |
  [~40kΩ internal resistor]
   |
  Pin
  - Domyślnie HIGH gdy nic nie podłączone
  - Używaj dla przycisków podłączonych do GND

PULL-DOWN:
  Pin
   |
  [~40kΩ internal resistor]
   |
  GND
  - Domyślnie LOW gdy nic nie podłączone
  - Używaj dla przycisków podłączonych do VDD
```

### Przykłady Konfiguracji

```c
/**
 * @brief  Konfiguracja pull-up/pull-down
 */
void Configure_PullUpDown(void)
{
    // PA0: Przycisk podłączony do GND -> Pull-up
    GPIOA->PUPDR &= ~(0x3 << 0);
    GPIOA->PUPDR |= (0x1 << 0);   // 01 = Pull-up
    // Teraz: przycisk nieprzciśnięty = HIGH, przyciśnięty = LOW
    
    // PA1: Przycisk podłączony do VDD -> Pull-down
    GPIOA->PUPDR &= ~(0x3 << 2);
    GPIOA->PUPDR |= (0x2 << 2);   // 10 = Pull-down
    // Teraz: przycisk nieprzciśnięty = LOW, przyciśnięty = HIGH
    
    // PA5: LED (output) -> No pull
    GPIOA->PUPDR &= ~(0x3 << 10); // 00 = No pull
}

/**
 * @brief  Czytanie przycisku z pull-up
 */
uint8_t Read_Button_PullUp(void)
{
    // Przycisk na PA0 z pull-up
    // Nieprzciśnięty = HIGH (1)
    // Przyciśnięty = LOW (0)
    
    if ((GPIOA->IDR & (1 << 0)) == 0) {
        return 1;  // Przycisk przyciśnięty
    } else {
        return 0;  // Przycisk nie przyciśnięty
    }
}
```

## 🔧 Rejestr 5: IDR (Input Data Register)

### Opis Rejestru

```
GPIOx_IDR - Port input data register
Offset: 0x10
Reset value: 0x00000000
Access: Read only

Bit layout:
31..16: Reserved
15 14 13 ... 2 1 0
[P15][P14][P13]...[P2][P1][P0]

Każdy bit:
0: Pin is LOW
1: Pin is HIGH
```

### Przykłady Czytania

```c
/**
 * @brief  Czytanie pojedynczego pinu
 */
uint8_t Read_Pin(GPIO_TypeDef *GPIOx, uint8_t pin)
{
    if (GPIOx->IDR & (1 << pin)) {
        return 1;  // HIGH
    } else {
        return 0;  // LOW
    }
}

/**
 * @brief  Czytanie całego portu
 */
uint16_t Read_Port(GPIO_TypeDef *GPIOx)
{
    return (uint16_t)(GPIOx->IDR & 0xFFFF);
}

/**
 * @brief  Czytanie kilku pinów jednocześnie
 */
void Read_Multiple_Pins(void)
{
    // Przeczytaj PA0, PA1, PA2 jako 3-bitową wartość
    uint32_t pins_state = GPIOA->IDR & 0x07;  // 0x07 = 0b111 (maske dla bitów 0-2)
    
    // pins_state może być 0-7 (0b000 do 0b111)
    switch (pins_state) {
        case 0b000: /* Wszystkie LOW */ break;
        case 0b001: /* PA0=HIGH */ break;
        case 0b111: /* Wszystkie HIGH */ break;
        // itd.
    }
}

/**
 * @brief  Debouncing sprzętowy - czytaj kilka razy
 */
uint8_t Read_Button_Debounced(void)
{
    uint8_t sample1 = (GPIOA->IDR & (1 << 0)) ? 1 : 0;
    
    // Delay ~1ms (prosty sposób)
    for (volatile uint32_t i = 0; i < 2000; i++);
    
    uint8_t sample2 = (GPIOA->IDR & (1 << 0)) ? 1 : 0;
    
    // Tylko jeśli oba odczyty są takie same
    if (sample1 == sample2) {
        return sample1;
    }
    
    return 0;  // Niestabilne
}
```

## 🔧 Rejestr 6: ODR (Output Data Register)

### Opis Rejestru

```
GPIOx_ODR - Port output data register
Offset: 0x14
Reset value: 0x00000000
Access: Read/Write

Bit layout:
31..16: Reserved
15 14 13 ... 2 1 0
[P15][P14][P13]...[P2][P1][P0]

Każdy bit:
0: Output LOW
1: Output HIGH
```

### Przykłady Zapisu

```c
/**
 * @brief  Ustawianie pojedynczego pinu
 */
void Write_Pin(GPIO_TypeDef *GPIOx, uint8_t pin, uint8_t state)
{
    if (state) {
        GPIOx->ODR |= (1 << pin);   // Set HIGH
    } else {
        GPIOx->ODR &= ~(1 << pin);  // Set LOW
    }
}

/**
 * @brief  Toggle pin
 */
void Toggle_Pin(GPIO_TypeDef *GPIOx, uint8_t pin)
{
    GPIOx->ODR ^= (1 << pin);  // XOR = toggle
}

/**
 * @brief  UWAGA: Problem z ODR - Read-Modify-Write
 * 
 * PROBLEM:
 * Jeśli przerwanie wystąpi między odczytem a zapisem,
 * możemy stracić zmiany!
 */
void Unsafe_Toggle_Example(void)
{
    // NIEBEZPIECZNE w środowisku z przerwaniami:
    GPIOA->ODR ^= (1 << 5);
    
    // Co się dzieje:
    // 1. Odczyt ODR
    // 2. <PRZERWANIE może zmienić ODR>
    // 3. Modyfikacja odczytanej wartości
    // 4. Zapis z powrotem <- nadpisuje zmiany z przerwania!
}

/**
 * @brief  Bezpieczne rozwiązanie: Użyj BSRR!
 */
void Safe_Toggle_Example(void)
{
    // Użyj BSRR - atomic operation
    if (GPIOA->ODR & (1 << 5)) {
        GPIOA->BSRR = (1 << (5 + 16));  // Reset
    } else {
        GPIOA->BSRR = (1 << 5);         // Set
    }
}
```

## 🔧 Rejestr 7: BSRR (Bit Set/Reset Register)

### Opis Rejestru

```
GPIOx_BSRR - Port bit set/reset register
Offset: 0x18
Reset value: 0x00000000
Access: Write only

Bit layout:
31 30 29 ... 17 16 | 15 14 13 ... 1 0
[BR15][BR14]...[BR0]|[BS15][BS14]...[BS0]

Bity 0-15 (BS - Bit Set):
Zapis 1: Ustaw odpowiedni pin w ODR
Zapis 0: Brak efektu

Bity 16-31 (BR - Bit Reset):
Zapis 1: Wyzeruj odpowiedni pin w ODR
Zapis 0: Brak efektu

WAŻNE: Operacja atomowa - nie może być przerwana!
```

### Dlaczego BSRR jest Lepszy?

```c
/**
 * @brief  Porównanie ODR vs BSRR
 */

// SPOSÓB 1: ODR (Read-Modify-Write - NIEBEZPIECZNY)
void Set_Pin_ODR(void)
{
    GPIOA->ODR |= (1 << 5);
    // Problem: 3 operacje (read, modify, write)
    // Przerwanie może wystąpić między nimi
}

// SPOSÓB 2: BSRR (Atomic - BEZPIECZNY)
void Set_Pin_BSRR(void)
{
    GPIOA->BSRR = (1 << 5);
    // Zaleta: 1 operacja write
    // Nie można przerwać
    // Hardware gwarantuje atomowość
}
```

### Przykłady Użycia BSRR

```c
/**
 * @brief  Podstawowe operacje z BSRR
 */
void BSRR_Examples(void)
{
    // Ustaw pin 5 (BS5)
    GPIOA->BSRR = (1 << 5);
    // To samo co: GPIOA->BSRR = 0x00000020;
    
    // Zresetuj pin 5 (BR5)
    GPIOA->BSRR = (1 << (5 + 16));
    // To samo co: GPIOA->BSRR = 0x00200000;
    
    // Jednocześnie: Ustaw pin 3, Zresetuj pin 7
    GPIOA->BSRR = (1 << 3) | (1 << (7 + 16));
    // To samo co: GPIOA->BSRR = 0x00800008;
    
    // Ustaw kilka pinów naraz
    GPIOA->BSRR = (1 << 0) | (1 << 1) | (1 << 2);
    // Piny 0, 1, 2 = HIGH
    
    // Zresetuj kilka pinów naraz
    GPIOA->BSRR = (1 << 16) | (1 << 17) | (1 << 18);
    // Piny 0, 1, 2 = LOW
}

/**
 * @brief  Toggle używając BSRR (bezpieczny sposób)
 */
void Toggle_Pin_BSRR(GPIO_TypeDef *GPIOx, uint8_t pin)
{
    // Odczytaj aktualny stan
    if (GPIOx->ODR & (1 << pin)) {
        // Pin jest HIGH -> reset
        GPIOx->BSRR = (1 << (pin + 16));
    } else {
        // Pin jest LOW -> set
        GPIOx->BSRR = (1 << pin);
    }
}

/**
 * @brief  Szybkie miganie LED - wykorzystanie BSRR
 */
void Fast_Blink_BSRR(void)
{
    for (int i = 0; i < 1000000; i++) {
        GPIOA->BSRR = (1 << 5);          // Set
        GPIOA->BSRR = (1 << (5 + 16));   // Reset
    }
    // Maksymalna możliwa częstotliwość togglea!
}
```

## 🔧 Rejestr 8: AFR (Alternate Function Register)

### Opis Rejestru

```
GPIOx_AFR[0] - Alternate function low register (piny 0-7)
Offset: 0x20
GPIOx_AFR[1] - Alternate function high register (piny 8-15)
Offset: 0x24
Reset value: 0x00000000

Każdy pin ma 4 bity (16 możliwych funkcji AF0-AF15):

AFR[0] - Piny 0-7:
31..28  27..24  23..20  19..16  15..12  11..8   7..4    3..0
[AFR7 ] [AFR6 ] [AFR5 ] [AFR4 ] [AFR3 ] [AFR2 ] [AFR1 ] [AFR0 ]

AFR[1] - Piny 8-15:
31..28  27..24  23..20  19..16  15..12  11..8   7..4    3..0
[AFR15] [AFR14] [AFR13] [AFR12] [AFR11] [AFR10] [AFR9 ] [AFR8 ]
```

### Tabela Alternate Functions dla STM32F429

```
Przykładowe AF dla wybranych pinów:

PA9:
  AF0: (default)
  AF1: TIM1_CH2
  AF7: USART1_TX  <-- Często używane
  AF8: I2C3_SMBA

PA10:
  AF1: TIM1_CH3
  AF7: USART1_RX  <-- Często używane
  AF10: OTG_FS_ID

PB6:
  AF4: I2C1_SCL   <-- Często używane
  AF7: USART1_TX
  AF9: CAN2_TX

PB7:
  AF4: I2C1_SDA   <-- Często używane
  AF7: USART1_RX

Pełną tabelę znajdziesz w "Datasheet Table 9"
```

### Przykłady Konfiguracji AF

```c
/**
 * @brief  Konfiguracja USART1 TX (PA9) - krok po kroku
 */
void Configure_USART1_TX_Detailed(void)
{
    // USART1 TX jest na PA9, używa AF7
    
    // KROK 1: Ustaw pin 9 w tryb Alternate Function
    GPIOA->MODER &= ~(0x3 << 18);  // Wyczyść bity 18-19 (pin 9)
    GPIOA->MODER |= (0x2 << 18);   // Ustaw 10 = AF mode
    
    // KROK 2: Wybierz AF7 dla pinu 9
    // Pin 9 -> AFR[1] (bo pin > 7)
    // Pozycja w AFR[1] = (9-8) * 4 = 4
    // Czyli bity 4-7 w AFR[1]
    
    GPIOA->AFR[1] &= ~(0xF << 4);  // Wyczyść bity 4-7
    GPIOA->AFR[1] |= (0x7 << 4);   // Ustaw AF7
    
    // KROK 3: Opcjonalne - ustaw prędkość
    GPIOA->OSPEEDR &= ~(0x3 << 18);
    GPIOA->OSPEEDR |= (0x2 << 18);  // High speed
    
    // KROK 4: Opcjonalne - pull-up
    GPIOA->PUPDR &= ~(0x3 << 18);
    GPIOA->PUPDR |= (0x1 << 18);  // Pull-up
}

/**
 * @brief  Konfiguracja I2C1 (PB6=SCL, PB7=SDA)
 */
void Configure_I2C1_Pins(void)
{
    // I2C1: PB6=SCL (AF4), PB7=SDA (AF4)
    
    // Tryb Alternate Function dla PB6 i PB7
    GPIOB->MODER &= ~((0x3 << 12) | (0x3 << 14));
    GPIOB->MODER |= ((0x2 << 12) | (0x2 << 14));
    
    // Open-drain (WYMAGANE dla I2C!)
    GPIOB->OTYPER |= (1 << 6) | (1 << 7);
    
    // Prędkość
    GPIOB->OSPEEDR &= ~((0x3 << 12) | (0x3 << 14));
    GPIOB->OSPEEDR |= ((0x3 << 12) | (0x3 << 14));  // Very high
    
    // Pull-up (często zewnętrzny, ale można internal)
    GPIOB->PUPDR &= ~((0x3 << 12) | (0x3 << 14));
    GPIOB->PUPDR |= ((0x1 << 12) | (0x1 << 14));
    
    // AF4 dla obu pinów
    // PB6 i PB7 -> AFR[0] (bo piny < 8)
    GPIOB->AFR[0] &= ~((0xF << 24) | (0xF << 28));  // PB6=bits 24-27, PB7=bits 28-31
    GPIOB->AFR[0] |= ((0x4 << 24) | (0x4 << 28));   // AF4
}

/**
 * @brief  Makra pomocnicze
 */
#define GPIO_AF0_RTC_50Hz      ((uint8_t)0x00)
#define GPIO_AF1_TIM1          ((uint8_t)0x01)
#define GPIO_AF2_TIM3          ((uint8_t)0x02)
#define GPIO_AF4_I2C1          ((uint8_t)0x04)
#define GPIO_AF7_USART1        ((uint8_t)0x07)
#define GPIO_AF12_OTG_HS_FS    ((uint8_t)0x0C)

void Set_Alternate_Function(GPIO_TypeDef *GPIOx, uint8_t pin, uint8_t af)
{
    if (pin < 8) {
        GPIOx->AFR[0] &= ~(0xF << (pin * 4));
        GPIOx->AFR[0] |= (af << (pin * 4));
    } else {
        GPIOx->AFR[1] &= ~(0xF << ((pin - 8) * 4));
        GPIOx->AFR[1] |= (af << ((pin - 8) * 4));
    }
}
```

## 🎯 Kompletny Przykład: Inicjalizacja GPIO

```c
/**
 * @brief  Kompletna funkcja inicjalizacji GPIO
 * 
 * Przykład: Konfiguracja PA5 jako output, push-pull, high speed, no pull
 */
void GPIO_Init_Complete_Example(void)
{
    // KROK 1: Włącz zegar dla GPIOA
    // (omówione w notatce o RCC)
    RCC->AHB1ENR |= (1 << 0);  // GPIOAEN
    
    // KROK 2: Skonfiguruj tryb = Output
    GPIOA->MODER &= ~(0x3 << 10);  // Wyczyść MODER5
    GPIOA->MODER |= (0x1 << 10);   // Output mode
    
    // KROK 3: Typ output = Push-Pull
    GPIOA->OTYPER &= ~(1 << 5);    // Push-pull
    
    // KROK 4: Prędkość = High
    GPIOA->OSPEEDR &= ~(0x3 << 10);
    GPIOA->OSPEEDR |= (0x2 << 10); // High speed
    
    // KROK 5: Pull-up/down = None
    GPIOA->PUPDR &= ~(0x3 << 10);  // No pull
    
    // KROK 6: Stan początkowy = LOW
    GPIOA->BSRR = (1 << (5 + 16)); // Reset pin 5
    
    // GOTOWE! Pin PA5 jest skonfigurowany
}

/**
 * @brief  Uniwersalna funkcja init GPIO
 */
typedef struct {
    GPIO_TypeDef *port;
    uint8_t pin;
    uint8_t mode;        // 0=Input, 1=Output, 2=AF, 3=Analog
    uint8_t otype;       // 0=PP, 1=OD
    uint8_t speed;       // 0=Low, 1=Med, 2=High, 3=VeryHigh
    uint8_t pull;        // 0=None, 1=PU, 2=PD
    uint8_t af;          // 0-15 (tylko dla AF mode)
} GPIO_Config_t;

void GPIO_Init(GPIO_Config_t *config)
{
    uint32_t pos = config->pin * 2;
    
    // Mode
    config->port->MODER &= ~(0x3 << pos);
    config->port->MODER |= (config->mode << pos);
    
    // Output type
    if (config->mode == 1 || config->mode == 2) {  // Output lub AF
        if (config->otype) {
            config->port->OTYPER |= (1 << config->pin);
        } else {
            config->port->OTYPER &= ~(1 << config->pin);
        }
    }
    
    // Speed
    config->port->OSPEEDR &= ~(0x3 << pos);
    config->port->OSPEEDR |= (config->speed << pos);
    
    // Pull
    config->port->PUPDR &= ~(0x3 << pos);
    config->port->PUPDR |= (config->pull << pos);
    
    // Alternate function
    if (config->mode == 2) {  // AF mode
        if (config->pin < 8) {
            config->port->AFR[0] &= ~(0xF << (config->pin * 4));
            config->port->AFR[0] |= (config->af << (config->pin * 4));
        } else {
            config->port->AFR[1] &= ~(0xF << ((config->pin - 8) * 4));
            config->port->AFR[1] |= (config->af << ((config->pin - 8) * 4));
        }
    }
}

/**
 * @brief  Użycie uniwersalnej funkcji
 */
void Example_Universal_Init(void)
{
    // Włącz zegary
    RCC->AHB1ENR |= (1 << 0) | (1 << 1);  // GPIOA, GPIOB
    
    // LED na PA5
    GPIO_Config_t led = {
        .port = GPIOA,
        .pin = 5,
        .mode = 1,        // Output
        .otype = 0,       // Push-pull
        .speed = 0,       // Low speed
        .pull = 0,        // No pull
        .af = 0           // Unused
    };
    GPIO_Init(&led);
    
    // USART1 TX na PA9
    GPIO_Config_t usart_tx = {
        .port = GPIOA,
        .pin = 9,
        .mode = 2,        // AF
        .otype = 0,       // Push-pull
        .speed = 2,       // High speed
        .pull = 1,        // Pull-up
        .af = 7           // AF7 = USART1
    };
    GPIO_Init(&usart_tx);
}
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_podstawy|Bare Metal - Podstawy]]
- [[stm32f429i_bare_metal_clock|Bare Metal - System zegarowy (RCC)]]
- [[stm32f429i_bare_metal_exti|Bare Metal - Przerwania zewnętrzne (EXTI)]]
- [[stm32f429i_gpio|GPIO z HAL - porównanie]]

## 📝 Podsumowanie

### Kluczowe Rejestry GPIO
1. **MODER** - Tryb pinu (Input/Output/AF/Analog)
2. **OTYPER** - Typ output (Push-Pull/Open-Drain)
3. **OSPEEDR** - Prędkość output
4. **PUPDR** - Pull-up/Pull-down
5. **IDR** - Odczyt stanu pinu
6. **ODR** - Ustawienie stanu pinu (read-modify-write)
7. **BSRR** - Atomic set/reset (najlepszy do output)
8. **AFR** - Wybór alternate function

### Best Practices
- Używaj **BSRR** zamiast ODR dla atomic operations
- Zawsze włącz zegar przed konfiguracją GPIO
- Dla I2C używaj Open-Drain
- Wybierz najniższą prędkość która wystarcza
- Używaj pull-up/down dla inputów floating

---

*Następna notatka: [[stm32f429i_bare_metal_clock|Bare Metal - System Zegarowy RCC]]*
