# STM32F429I - Bare Metal - System Zegarowy (RCC)

## 🕐 Reset and Clock Control (RCC)

### Dlaczego System Zegarowy Jest Ważny?

```
Wszystkie peryferia w STM32 potrzebują zegara do działania!

Bez włączonego zegara:
- Rejestry są "zamrożone"
- Peryferia nie reagują
- Nie możesz ich skonfigurować

ZŁOTA ZASADA:
Zawsze najpierw włącz zegar, potem konfiguruj peryferyjne!
```

## 📋 Struktura RCC - Podstawy

### Definicje Adresów

```c
/**
 * @brief  Adresy bazowe RCC
 */
#define RCC_BASE              0x40023800UL

/**
 * @brief  Kompletna struktura RCC
 */
typedef struct {
    __IO uint32_t CR;            // 0x00: Clock control register
    __IO uint32_t PLLCFGR;       // 0x04: PLL configuration register
    __IO uint32_t CFGR;          // 0x08: Clock configuration register
    __IO uint32_t CIR;           // 0x0C: Clock interrupt register
    __IO uint32_t AHB1RSTR;      // 0x10: AHB1 peripheral reset register
    __IO uint32_t AHB2RSTR;      // 0x14: AHB2 peripheral reset register
    __IO uint32_t AHB3RSTR;      // 0x18: AHB3 peripheral reset register
    uint32_t      RESERVED0;     // 0x1C: Reserved
    __IO uint32_t APB1RSTR;      // 0x20: APB1 peripheral reset register
    __IO uint32_t APB2RSTR;      // 0x24: APB2 peripheral reset register
    uint32_t      RESERVED1[2];  // 0x28-0x2C: Reserved
    __IO uint32_t AHB1ENR;       // 0x30: AHB1 peripheral clock enable register
    __IO uint32_t AHB2ENR;       // 0x34: AHB2 peripheral clock enable register
    __IO uint32_t AHB3ENR;       // 0x38: AHB3 peripheral clock enable register
    uint32_t      RESERVED2;     // 0x3C: Reserved
    __IO uint32_t APB1ENR;       // 0x40: APB1 peripheral clock enable register
    __IO uint32_t APB2ENR;       // 0x44: APB2 peripheral clock enable register
    uint32_t      RESERVED3[2];  // 0x48-0x4C: Reserved
    __IO uint32_t AHB1LPENR;     // 0x50: AHB1 low power mode clock enable
    __IO uint32_t AHB2LPENR;     // 0x54: AHB2 low power mode clock enable
    __IO uint32_t AHB3LPENR;     // 0x58: AHB3 low power mode clock enable
    uint32_t      RESERVED4;     // 0x5C: Reserved
    __IO uint32_t APB1LPENR;     // 0x60: APB1 low power mode clock enable
    __IO uint32_t APB2LPENR;     // 0x64: APB2 low power mode clock enable
    uint32_t      RESERVED5[2];  // 0x68-0x6C: Reserved
    __IO uint32_t BDCR;          // 0x70: Backup domain control register
    __IO uint32_t CSR;           // 0x74: Clock control & status register
    uint32_t      RESERVED6[2];  // 0x78-0x7C: Reserved
    __IO uint32_t SSCGR;         // 0x80: Spread spectrum clock generation
    __IO uint32_t PLLI2SCFGR;    // 0x84: PLLI2S configuration register
    __IO uint32_t PLLSAICFGR;    // 0x88: PLLSAI configuration register
    __IO uint32_t DCKCFGR;       // 0x8C: Dedicated clocks configuration register
} RCC_TypeDef;

#define RCC  ((RCC_TypeDef *) RCC_BASE)
```

## 🌳 Drzewo Zegarów STM32F429

### Schemat Przepływu Zegarów

```
Źródła zegarów:
┌──────────────┐
│ HSI (16 MHz) │  Internal RC oscillator (domyślny po resecie)
└──────┬───────┘
       │
┌──────▼───────┐
│ HSE (8-25 MHz)│  External crystal/oscillator
└──────┬───────┘
       │
       ├────────┐
       │        ▼
       │  ┌─────────┐      ┌──────────────┐
       │  │   PLL   │─────▶│ SYSCLK       │ System Clock (max 180 MHz)
       │  └─────────┘      └──────┬───────┘
       │                          │
       │                    ┌─────┼─────┬─────────┐
       │                    │     │     │         │
       │                    ▼     ▼     ▼         ▼
       │              ┌────────┐ ┌────┐ ┌────┐  ┌────┐
       │              │ AHB    │ │APB1│ │APB2│  │RTC │
       │              │(Cortex)│ │    │ │    │  │    │
       │              └───┬────┘ └─┬──┘ └─┬──┘  └────┘
       │                  │        │      │
       │              ┌───▼────────▼──────▼───┐
       │              │  Peryferia            │
       │              │  GPIO, UART, SPI...   │
       │              └───────────────────────┘
       │
       └──────────────▶ Bezpośrednio do niektórych peryferiów
```

### Magistrale i Prescalery

```
SYSCLK (max 180 MHz)
  │
  ├── AHB Prescaler (/1, /2, /4, /8, /16, ..., /512)
  │   │
  │   └─▶ AHB Clock (max 180 MHz)
  │       ├─▶ Cortex-M4 (CPU)
  │       ├─▶ DMA
  │       ├─▶ GPIO
  │       └─▶ Pamięć Flash (controller)
  │
  ├── APB1 Prescaler (/1, /2, /4, /8, /16)
  │   │
  │   └─▶ APB1 Clock (max 45 MHz)
  │       ├─▶ UART2, UART3, UART4, UART5
  │       ├─▶ I2C1, I2C2, I2C3
  │       ├─▶ SPI2, SPI3
  │       └─▶ TIM2, TIM3, TIM4, TIM5, TIM6, TIM7, TIM12, TIM13, TIM14
  │
  └── APB2 Prescaler (/1, /2, /4, /8, /16)
      │
      └─▶ APB2 Clock (max 90 MHz)
          ├─▶ UART1, UART6
          ├─▶ SPI1, SPI4, SPI5, SPI6
          ├─▶ ADC1, ADC2, ADC3
          └─▶ TIM1, TIM8, TIM9, TIM10, TIM11
```

## 🔧 Włączanie Zegarów Peryferiów

### Rejestr AHB1ENR - AHB1 Peripheral Clock Enable

```
RCC_AHB1ENR - AHB1 peripheral clock enable register
Offset: 0x30
Reset value: 0x00100000

Bit 0:  GPIOAEN  - GPIOA clock enable
Bit 1:  GPIOBEN  - GPIOB clock enable
Bit 2:  GPIOCEN  - GPIOC clock enable
Bit 3:  GPIODEN  - GPIOD clock enable
Bit 4:  GPIOEEN  - GPIOE clock enable
Bit 5:  GPIOFEN  - GPIOF clock enable
Bit 6:  GPIOGEN  - GPIOG clock enable
Bit 7:  GPIOHEN  - GPIOH clock enable
Bit 8:  GPIOIEN  - GPIOI clock enable
Bit 9:  GPIOJEN  - GPIOJ clock enable
Bit 10: GPIOKEN  - GPIOK clock enable
...
Bit 12: CRCEN    - CRC clock enable
...
Bit 21: DMA1EN   - DMA1 clock enable
Bit 22: DMA2EN   - DMA2 clock enable
Bit 23: DMA2DEN  - DMA2D clock enable
```

### Przykłady Włączania Zegarów

```c
/**
 * @brief  Włączanie zegarów GPIO - krok po kroku
 */
void Enable_GPIO_Clocks_StepByStep(void)
{
    // KROK 1: Sprawdź aktualny stan rejestru
    uint32_t current = RCC->AHB1ENR;
    // Po resecie: 0x00100000
    
    // KROK 2: Włącz zegar GPIOA (bit 0)
    RCC->AHB1ENR |= (1 << 0);  // Ustaw bit 0
    // Teraz bit 0 = 1, GPIOA ma zegar
    
    // KROK 3: Włącz zegar GPIOB (bit 1)
    RCC->AHB1ENR |= (1 << 1);  // Ustaw bit 1
    
    // KROK 4: Włącz kilka portów naraz
    RCC->AHB1ENR |= (1 << 2) | (1 << 3) | (1 << 4);
    // GPIOC, GPIOD, GPIOE
    
    // ALTERNATYWNIE: Wszystko w jednej linii
    RCC->AHB1ENR |= (1 << 0)   // GPIOA
                  | (1 << 1)   // GPIOB
                  | (1 << 2)   // GPIOC
                  | (1 << 3)   // GPIOD
                  | (1 << 4);  // GPIOE
}

/**
 * @brief  Makra dla czytelności
 */
#define RCC_AHB1ENR_GPIOAEN   (1 << 0)
#define RCC_AHB1ENR_GPIOBEN   (1 << 1)
#define RCC_AHB1ENR_GPIOCEN   (1 << 2)
#define RCC_AHB1ENR_GPIODEN   (1 << 3)
#define RCC_AHB1ENR_GPIOEEN   (1 << 4)
#define RCC_AHB1ENR_DMA1EN    (1 << 21)
#define RCC_AHB1ENR_DMA2EN    (1 << 22)

void Enable_Clocks_With_Macros(void)
{
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN 
                  | RCC_AHB1ENR_GPIOBEN
                  | RCC_AHB1ENR_DMA1EN;
}

/**
 * @brief  Sprawdzenie czy zegar jest włączony
 */
uint8_t Is_GPIO_Clock_Enabled(uint8_t gpio_port)
{
    // gpio_port: 0=GPIOA, 1=GPIOB, etc.
    if (RCC->AHB1ENR & (1 << gpio_port)) {
        return 1;  // Zegar włączony
    } else {
        return 0;  // Zegar wyłączony
    }
}
```

### Rejestr APB1ENR - APB1 Peripheral Clock Enable

```
RCC_APB1ENR - APB1 peripheral clock enable register
Offset: 0x40
Reset value: 0x00000000

Bit 0:  TIM2EN   - TIM2 clock enable
Bit 1:  TIM3EN   - TIM3 clock enable
Bit 2:  TIM4EN   - TIM4 clock enable
Bit 3:  TIM5EN   - TIM5 clock enable
...
Bit 11: WWDGEN   - Window watchdog clock enable
...
Bit 14: SPI2EN   - SPI2 clock enable
Bit 15: SPI3EN   - SPI3 clock enable
...
Bit 17: USART2EN - USART2 clock enable
Bit 18: USART3EN - USART3 clock enable
...
Bit 21: I2C1EN   - I2C1 clock enable
Bit 22: I2C2EN   - I2C2 clock enable
Bit 23: I2C3EN   - I2C3 clock enable
...
Bit 28: PWREN    - Power interface clock enable
```

### Przykłady APB1

```c
/**
 * @brief  Włączanie zegarów APB1
 */
#define RCC_APB1ENR_TIM2EN    (1 << 0)
#define RCC_APB1ENR_TIM3EN    (1 << 1)
#define RCC_APB1ENR_USART2EN  (1 << 17)
#define RCC_APB1ENR_I2C1EN    (1 << 21)
#define RCC_APB1ENR_SPI2EN    (1 << 14)

void Enable_APB1_Peripherals(void)
{
    // Włącz USART2
    RCC->APB1ENR |= RCC_APB1ENR_USART2EN;
    
    // Włącz I2C1
    RCC->APB1ENR |= RCC_APB1ENR_I2C1EN;
    
    // Włącz TIM2
    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;
}
```

### Rejestr APB2ENR - APB2 Peripheral Clock Enable

```
RCC_APB2ENR - APB2 peripheral clock enable register
Offset: 0x44
Reset value: 0x00000000

Bit 0:  TIM1EN   - TIM1 clock enable
Bit 1:  TIM8EN   - TIM8 clock enable
Bit 4:  USART1EN - USART1 clock enable
Bit 5:  USART6EN - USART6 clock enable
...
Bit 8:  ADC1EN   - ADC1 clock enable
Bit 9:  ADC2EN   - ADC2 clock enable
Bit 10: ADC3EN   - ADC3 clock enable
...
Bit 12: SPI1EN   - SPI1 clock enable
Bit 13: SPI4EN   - SPI4 clock enable
Bit 14: SYSCFGEN - SYSCFG clock enable
...
```

### Przykłady APB2

```c
/**
 * @brief  Włączanie zegarów APB2
 */
#define RCC_APB2ENR_USART1EN  (1 << 4)
#define RCC_APB2ENR_SPI1EN    (1 << 12)
#define RCC_APB2ENR_ADC1EN    (1 << 8)
#define RCC_APB2ENR_SYSCFGEN  (1 << 14)

void Enable_APB2_Peripherals(void)
{
    // Włącz USART1 (szybszy UART na APB2)
    RCC->APB2ENR |= RCC_APB2ENR_USART1EN;
    
    // Włącz SPI1
    RCC->APB2ENR |= RCC_APB2ENR_SPI1EN;
    
    // Włącz SYSCFG (potrzebny dla EXTI)
    RCC->APB2ENR |= RCC_APB2ENR_SYSCFGEN;
}
```

## ⚡ Źródła Zegarów

### Rejestr CR - Clock Control Register

```
RCC_CR - Clock control register
Offset: 0x00
Reset value: 0x00000083

Bit 0:  HSION     - Internal high-speed clock enable
Bit 1:  HSIRDY    - Internal high-speed clock ready flag
Bit 16: HSEON     - External high-speed clock enable
Bit 17: HSERDY    - External high-speed clock ready flag
Bit 18: HSEBYP    - External high-speed clock bypass
Bit 19: CSSON     - Clock security system enable
Bit 24: PLLON     - Main PLL enable
Bit 25: PLLRDY    - Main PLL clock ready flag
Bit 26: PLLI2SON  - PLLI2S enable
Bit 27: PLLI2SRDY - PLLI2S clock ready flag
```

### HSI - Internal RC Oscillator

```c
/**
 * @brief  HSI (High Speed Internal) - 16 MHz RC oscillator
 * 
 * Cechy:
 * - Dostępny od razu po resecie
 * - Mniejsza dokładność niż HSE (±1%)
 * - Niskie zużycie energii
 * - Nie wymaga zewnętrznych komponentów
 */

void Enable_HSI(void)
{
    // KROK 1: Włącz HSI
    RCC->CR |= (1 << 0);  // HSION = 1
    
    // KROK 2: Czekaj aż będzie gotowy
    while ((RCC->CR & (1 << 1)) == 0) {
        // Czekaj na HSIRDY = 1
    }
    
    // Teraz HSI jest gotowy do użycia
}

/**
 * @brief  HSI jest domyślnie włączony po resecie
 */
void Check_HSI_Status(void)
{
    if (RCC->CR & (1 << 0)) {
        // HSI jest włączony
    }
    
    if (RCC->CR & (1 << 1)) {
        // HSI jest gotowy (stabilny)
    }
}
```

### HSE - External Crystal Oscillator

```c
/**
 * @brief  HSE (High Speed External) - External crystal
 * 
 * Dla STM32F429I-Discovery:
 * - Kryształ 8 MHz
 * - Wysoka dokładność (±50 ppm)
 * - Potrzebny dla USB, Ethernet
 * 
 * Schemat sprzętowy:
 * 
 *     OSC_IN  -----[Crystal 8MHz]-----  OSC_OUT
 *                       |
 *                     [Caps]
 *                       |
 *                      GND
 */

void Enable_HSE(void)
{
    // KROK 1: Włącz HSE
    RCC->CR |= (1 << 16);  // HSEON = 1
    
    // KROK 2: Czekaj aż będzie gotowy (może trwać do 100ms)
    uint32_t timeout = 100000;
    while (((RCC->CR & (1 << 17)) == 0) && (timeout > 0)) {
        timeout--;
    }
    
    if (timeout == 0) {
        // ERROR: HSE nie startuje!
        // Sprawdź sprzęt (crystal, caps)
        Error_Handler();
    }
    
    // HSE jest gotowy
}

/**
 * @brief  HSE Bypass mode
 * 
 * Jeśli zamiast kryształu masz zewnętrzny oscylator:
 */
void Enable_HSE_Bypass(void)
{
    // Najpierw wyłącz HSE
    RCC->CR &= ~(1 << 16);
    
    // Włącz bypass
    RCC->CR |= (1 << 18);  // HSEBYP = 1
    
    // Teraz włącz HSE
    RCC->CR |= (1 << 16);  // HSEON = 1
    
    // Czekaj na gotowość
    while ((RCC->CR & (1 << 17)) == 0);
}
```

## 🚀 PLL - Phase Locked Loop

### Dlaczego PLL?

```
Problem:
- HSI = 16 MHz
- HSE = 8 MHz (na Discovery board)
- Chcemy SYSCLK = 180 MHz!

Rozwiązanie:
- PLL mnoży częstotliwość źródła
- Można osiągnąć 180 MHz z 8 MHz HSE
```

### Konfiguracja PLL - Rejestr PLLCFGR

```
RCC_PLLCFGR - PLL configuration register
Offset: 0x04
Reset value: 0x24003010

Formuła PLL:
f(VCO) = f(PLL_input) × (PLLN / PLLM)
f(PLL_output) = f(VCO) / PLLP

Bity:
0-5:   PLLM   - Division factor for PLL input (2-63)
6-14:  PLLN   - Multiplication factor (50-432)
16-17: PLLP   - Division factor for main clock (2, 4, 6, 8)
22:    PLLSRC - PLL source (0=HSI, 1=HSE)
24-27: PLLQ   - Division factor for USB, SDIO (2-15)

Ograniczenia:
- f(PLL_input) = 1-2 MHz (zalecane 2 MHz)
- f(VCO) = 100-432 MHz
- f(PLL_output) max = 180 MHz
```

### Obliczenia PLL dla 180 MHz

```c
/**
 * @brief  Konfiguracja PLL: HSE 8 MHz -> SYSCLK 180 MHz
 * 
 * Cel: SYSCLK = 180 MHz
 * Źródło: HSE = 8 MHz
 * 
 * KROK 1: Oblicz PLLM (dzielnik wejścia)
 * Cel: f(PLL_input) = 2 MHz (zalecane)
 * PLLM = HSE / 2 MHz = 8 MHz / 2 MHz = 4
 * 
 * KROK 2: Oblicz PLLN (mnożnik)
 * f(VCO) = f(PLL_input) × PLLN
 * Chcemy f(VCO) = 360 MHz (aby po /2 dać 180 MHz)
 * PLLN = f(VCO) / f(PLL_input) = 360 MHz / 2 MHz = 180
 * 
 * KROK 3: Oblicz PLLP (dzielnik wyjścia)
 * f(SYSCLK) = f(VCO) / PLLP
 * PLLP = f(VCO) / f(SYSCLK) = 360 MHz / 180 MHz = 2
 * 
 * KROK 4: Oblicz PLLQ (dla USB)
 * f(USB) = 48 MHz (wymagane)
 * PLLQ = f(VCO) / f(USB) = 360 MHz / 48 MHz = 7.5 ≈ 8
 * (Nie można idealnie, USB będzie 360/8 = 45 MHz - nie użyjesz USB)
 * Lepiej: VCO=336, PLLN=168, PLLP=2 dla 168MHz, PLLQ=7 dla 48MHz USB
 * 
 * PODSUMOWANIE dla 180 MHz bez USB:
 * PLLM = 4
 * PLLN = 180
 * PLLP = 2 (kod: 00)
 * PLLQ = 8
 * PLLSRC = 1 (HSE)
 */

void Configure_PLL_180MHz(void)
{
    // KROK 1: Wyłącz PLL przed konfiguracją
    RCC->CR &= ~(1 << 24);  // PLLON = 0
    
    // Czekaj aż PLL się wyłączy
    while (RCC->CR & (1 << 25));  // Czekaj aż PLLRDY = 0
    
    // KROK 2: Konfiguruj PLLCFGR
    uint32_t pllcfgr = 0;
    
    // PLLM = 4 (bits 0-5)
    pllcfgr |= (4 << 0);
    
    // PLLN = 180 (bits 6-14)
    pllcfgr |= (180 << 6);
    
    // PLLP = 2 -> kod 00 (bits 16-17)
    pllcfgr |= (0 << 16);  // 00 = /2
    
    // PLLSRC = HSE (bit 22)
    pllcfgr |= (1 << 22);
    
    // PLLQ = 8 (bits 24-27)
    pllcfgr |= (8 << 24);
    
    RCC->PLLCFGR = pllcfgr;
    
    // KROK 3: Włącz PLL
    RCC->CR |= (1 << 24);  // PLLON = 1
    
    // KROK 4: Czekaj aż PLL się ustabilizuje
    while ((RCC->CR & (1 << 25)) == 0);  // Czekaj na PLLRDY = 1
    
    // PLL gotowy!
}

/**
 * @brief  Alternatywna konfiguracja - 168 MHz z USB 48 MHz
 */
void Configure_PLL_168MHz_WithUSB(void)
{
    // VCO = 336 MHz
    // SYSCLK = 168 MHz
    // USB = 48 MHz
    
    RCC->CR &= ~(1 << 24);  // Wyłącz PLL
    while (RCC->CR & (1 << 25));
    
    uint32_t pllcfgr = 0;
    pllcfgr |= (4 << 0);    // PLLM = 4   (8 MHz / 4 = 2 MHz)
    pllcfgr |= (168 << 6);  // PLLN = 168 (2 MHz × 168 = 336 MHz)
    pllcfgr |= (0 << 16);   // PLLP = 2   (336 MHz / 2 = 168 MHz)
    pllcfgr |= (1 << 22);   // PLLSRC = HSE
    pllcfgr |= (7 << 24);   // PLLQ = 7   (336 MHz / 7 = 48 MHz) ✓
    
    RCC->PLLCFGR = pllcfgr;
    
    RCC->CR |= (1 << 24);   // Włącz PLL
    while ((RCC->CR & (1 << 25)) == 0);
}
```

## ⚙️ Przełączanie Źródła Zegarów

### Rejestr CFGR - Clock Configuration Register

```
RCC_CFGR - Clock configuration register
Offset: 0x08
Reset value: 0x00000000

Bity 0-1: SW[1:0] - System clock switch
  00: HSI selected
  01: HSE selected
  10: PLL selected
  11: Reserved

Bity 2-3: SWS[1:0] - System clock switch status (read-only)
  00: HSI used
  01: HSE used
  10: PLL used
  11: Reserved

Bity 4-7: HPRE[3:0] - AHB prescaler
Bity 10-12: PPRE1[2:0] - APB1 prescaler
Bity 13-15: PPRE2[2:0] - APB2 prescaler
```

### Przełączanie na PLL

```c
/**
 * @brief  Przełączanie SYSCLK z HSI na PLL
 * 
 * WAŻNE: Flash wait states muszą być ustawione PRZED przełączeniem!
 */
void Switch_To_PLL(void)
{
    // KROK 1: Ustaw Flash wait states dla 180 MHz
    // (omówione w następnej sekcji)
    Configure_Flash_WaitStates(5);  // 5 wait states @ 180 MHz
    
    // KROK 2: Przełącz SYSCLK na PLL
    // Wyczyść bity SW[1:0]
    RCC->CFGR &= ~(0x3 << 0);
    
    // Ustaw SW = 10 (PLL)
    RCC->CFGR |= (0x2 << 0);
    
    // KROK 3: Czekaj aż przełączy
    while ((RCC->CFGR & (0x3 << 2)) != (0x2 << 2)) {
        // Czekaj aż SWS = 10 (PLL używany)
    }
    
    // Teraz SYSCLK = PLL = 180 MHz!
}

/**
 * @brief  Sprawdzenie aktualnego źródła SYSCLK
 */
uint8_t Get_System_Clock_Source(void)
{
    uint32_t sws = (RCC->CFGR >> 2) & 0x3;
    
    switch (sws) {
        case 0: return 0;  // HSI
        case 1: return 1;  // HSE
        case 2: return 2;  // PLL
        default: return 0xFF;  // Error
    }
}
```

## 🔄 Prescalery Magistral

### AHB Prescaler

```
HPRE[3:0] - AHB prescaler (bits 4-7 w CFGR)

0xxx: SYSCLK not divided (AHB = SYSCLK)
1000: SYSCLK / 2
1001: SYSCLK / 4
1010: SYSCLK / 8
1011: SYSCLK / 16
1100: SYSCLK / 64
1101: SYSCLK / 128
1110: SYSCLK / 256
1111: SYSCLK / 512
```

### APB1 i APB2 Prescalers

```
PPRE1[2:0] - APB1 prescaler (bits 10-12)
PPRE2[2:0] - APB2 prescaler (bits 13-15)

0xx: AHB not divided (APBx = AHB)
100: AHB / 2
101: AHB / 4
110: AHB / 8
111: AHB / 16

OGRANICZENIA:
- APB1 max = 45 MHz
- APB2 max = 90 MHz
```

### Konfiguracja Prescalerów

```c
/**
 * @brief  Typowa konfiguracja dla 180 MHz
 * 
 * SYSCLK = 180 MHz
 * AHB = 180 MHz (bez dzielenia)
 * APB1 = 45 MHz (dziel przez 4)
 * APB2 = 90 MHz (dziel przez 2)
 */
void Configure_Bus_Prescalers(void)
{
    uint32_t cfgr = RCC->CFGR;
    
    // Wyczyść bity prescalera
    cfgr &= ~((0xF << 4) | (0x7 << 10) | (0x7 << 13));
    
    // AHB = SYSCLK (0xxx = no division)
    cfgr |= (0x0 << 4);
    
    // APB1 = AHB / 4 (101)
    // 180 MHz / 4 = 45 MHz ✓
    cfgr |= (0x5 << 10);
    
    // APB2 = AHB / 2 (100)
    // 180 MHz / 2 = 90 MHz ✓
    cfgr |= (0x4 << 13);
    
    RCC->CFGR = cfgr;
}

/**
 * @brief  UWAGA: Timery mają specjalny clock multiplier
 * 
 * Jeśli APBx prescaler != 1, to timery mają 2× clock:
 * 
 * APB1 = 45 MHz, ale TIM2-TIM7 clock = 90 MHz!
 * APB2 = 90 MHz, ale TIM1, TIM8 clock = 180 MHz!
 */
```

## ⚡ Flash Wait States

### Dlaczego Potrzebne?

```
Problem:
- Flash memory jest wolniejsza niż CPU
- Przy 180 MHz CPU, Flash nie nadąża
- Potrzebne wait states (cykle oczekiwania)

Bez wait states @ 180 MHz:
- CPU czyta niepoprawne dane
- Program crashuje
```

### Rejestr FLASH_ACR

```c
/**
 * @brief  Flash Access Control Register
 * 
 * Adres: 0x40023C00
 */
#define FLASH_BASE  0x40023C00UL
#define FLASH_ACR   (*(volatile uint32_t *)(FLASH_BASE + 0x00))

/**
 * @brief  Tabela wait states dla STM32F429 @ 3.3V
 * 
 * SYSCLK          Wait States
 * 0-30 MHz        0
 * 30-60 MHz       1
 * 60-90 MHz       2
 * 90-120 MHz      3
 * 120-150 MHz     4
 * 150-180 MHz     5
 */

void Configure_Flash_WaitStates(uint8_t latency)
{
    // KROK 1: Włącz instruction cache
    FLASH_ACR |= (1 << 9);  // ICEN
    
    // KROK 2: Włącz data cache
    FLASH_ACR |= (1 << 10);  // DCEN
    
    // KROK 3: Włącz prefetch
    FLASH_ACR |= (1 << 8);   // PRFTEN
    
    // KROK 4: Ustaw latency
    FLASH_ACR &= ~(0xF << 0);  // Wyczyść bity 0-3
    FLASH_ACR |= (latency << 0);
    
    // KROK 5: Sprawdź czy ustawione
    while ((FLASH_ACR & 0xF) != latency);
}
```

## 🎯 Kompletna Inicjalizacja 180 MHz

```c
/**
 * @brief  Kompletna konfiguracja systemu zegarowego
 * 
 * HSE 8 MHz -> PLL -> SYSCLK 180 MHz
 * AHB = 180 MHz
 * APB1 = 45 MHz
 * APB2 = 90 MHz
 */
void SystemClock_Config_180MHz(void)
{
    // KROK 1: Włącz Over-Drive mode (wymagane dla 180 MHz!)
    // (omówione w osobnej notatce)
    Enable_OverDrive_Mode();
    
    // KROK 2: Włącz HSE
    RCC->CR |= (1 << 16);  // HSEON
    while ((RCC->CR & (1 << 17)) == 0);  // Czekaj na HSERDY
    
    // KROK 3: Konfiguruj Flash (PRZED przełączeniem!)
    Configure_Flash_WaitStates(5);  // 5 WS dla 180 MHz
    
    // KROK 4: Konfiguruj prescalery magistral
    uint32_t cfgr = RCC->CFGR;
    cfgr &= ~((0xF << 4) | (0x7 << 10) | (0x7 << 13));
    cfgr |= (0x0 << 4);   // AHB = /1
    cfgr |= (0x5 << 10);  // APB1 = /4
    cfgr |= (0x4 << 13);  // APB2 = /2
    RCC->CFGR = cfgr;
    
    // KROK 5: Konfiguruj PLL
    RCC->CR &= ~(1 << 24);  // Wyłącz PLL
    while (RCC->CR & (1 << 25));  // Czekaj
    
    uint32_t pllcfgr = 0;
    pllcfgr |= (4 << 0);     // PLLM = 4
    pllcfgr |= (180 << 6);   // PLLN = 180
    pllcfgr |= (0 << 16);    // PLLP = 2
    pllcfgr |= (1 << 22);    // PLLSRC = HSE
    pllcfgr |= (8 << 24);    // PLLQ = 8
    RCC->PLLCFGR = pllcfgr;
    
    RCC->CR |= (1 << 24);    // Włącz PLL
    while ((RCC->CR & (1 << 25)) == 0);  // Czekaj na PLLRDY
    
    // KROK 6: Przełącz SYSCLK na PLL
    RCC->CFGR &= ~(0x3 << 0);
    RCC->CFGR |= (0x2 << 0);  // SW = PLL
    while ((RCC->CFGR & (0x3 << 2)) != (0x2 << 2));  // Czekaj na SWS = PLL
    
    // GOTOWE! System działa na 180 MHz
}

/**
 * @brief  Prostsza wersja - 84 MHz (bez Over-Drive)
 */
void SystemClock_Config_84MHz(void)
{
    // Włącz HSE
    RCC->CR |= (1 << 16);
    while ((RCC->CR & (1 << 17)) == 0);
    
    // Flash: 2 WS dla 84 MHz
    Configure_Flash_WaitStates(2);
    
    // Prescalery
    uint32_t cfgr = RCC->CFGR;
    cfgr &= ~((0xF << 4) | (0x7 << 10) | (0x7 << 13));
    cfgr |= (0x0 << 4);   // AHB = /1
    cfgr |= (0x4 << 10);  // APB1 = /2 (42 MHz)
    cfgr |= (0x0 << 13);  // APB2 = /1 (84 MHz)
    RCC->CFGR = cfgr;
    
    // PLL: 8 MHz / 4 × 168 / 2 = 84 MHz
    RCC->CR &= ~(1 << 24);
    while (RCC->CR & (1 << 25));
    
    uint32_t pllcfgr = 0;
    pllcfgr |= (4 << 0);     // PLLM = 4
    pllcfgr |= (168 << 6);   // PLLN = 168
    pllcfgr |= (0 << 16);    // PLLP = 2
    pllcfgr |= (1 << 22);    // PLLSRC = HSE
    pllcfgr |= (7 << 24);    // PLLQ = 7 (48 MHz dla USB)
    RCC->PLLCFGR = pllcfgr;
    
    RCC->CR |= (1 << 24);
    while ((RCC->CR & (1 << 25)) == 0);
    
    // Przełącz
    RCC->CFGR &= ~(0x3 << 0);
    RCC->CFGR |= (0x2 << 0);
    while ((RCC->CFGR & (0x3 << 2)) != (0x2 << 2));
}
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_podstawy|Bare Metal - Podstawy]]
- [[stm32f429i_bare_metal_gpio|Bare Metal - GPIO]]
- [[stm32f429i_bare_metal_overdrive|Bare Metal - Over-Drive Mode]]
- [[stm32f429i_system_zegarowy|System zegarowy z HAL - porównanie]]

## 📝 Podsumowanie

### Kolejność Inicjalizacji Zegara
1. Włącz HSE i czekaj na HSERDY
2. Konfiguruj Flash wait states
3. Konfiguruj prescalery magistral
4. Konfiguruj i włącz PLL
5. Przełącz SYSCLK na PLL

### Kluczowe Rejestry
- **RCC_CR** - Włączanie źródeł (HSI, HSE, PLL)
- **RCC_PLLCFGR** - Konfiguracja PLL
- **RCC_CFGR** - Wybór źródła SYSCLK, prescalery
- **RCC_AHB1ENR** - Zegary peryferiów AHB1 (GPIO, DMA)
- **RCC_APB1ENR** - Zegary peryferiów APB1
- **RCC_APB2ENR** - Zegary peryferiów APB2
- **FLASH_ACR** - Wait states dla Flash

### Wzory PLL
```
f(VCO) = f(PLL_input) × (PLLN / PLLM)
f(SYSCLK) = f(VCO) / PLLP
f(USB) = f(VCO) / PLLQ
```

---

*Następna notatka: [[stm32f429i_bare_metal_startup|Bare Metal - Startup Code i Vector Table]]*
