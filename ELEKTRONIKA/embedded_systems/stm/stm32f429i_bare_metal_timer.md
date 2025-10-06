# STM32F429I - Bare Metal - Timery TIM2-TIM5

## ⏱️ Timery STM32F429 - Przegląd

### Rodzaje Timerów

```
STM32F429 ma różne typy timerów:

Advanced-control timers (TIM1, TIM8):
- 16-bit up/down counter
- PWM complementary outputs
- Dead-time generation
- Break input
- Encoder interface

General-purpose timers (TIM2-TIM5):
- TIM2, TIM5: 32-bit counter  ← NAJCZĘŚCIEJ UŻYWANE
- TIM3, TIM4: 16-bit counter
- 4 kanały PWM każdy
- Input capture
- Output compare
- Encoder interface

Basic timers (TIM6, TIM7):
- 16-bit up counter
- Bez kanałów PWM
- Głównie dla DAC trigger, timebase
```

## 📋 Rejestry Timera (TIM2-TIM5)

### Adresy Bazowe

```c
/**
 * @brief  Timer Base Addresses
 */
#define TIM2_BASE  0x40000000UL  // APB1
#define TIM3_BASE  0x40000400UL  // APB1
#define TIM4_BASE  0x40000800UL  // APB1
#define TIM5_BASE  0x40000C00UL  // APB1

/**
 * @brief  Struktura Timera (uproszczona)
 */
typedef struct {
    volatile uint32_t CR1;    // 0x00: Control register 1
    volatile uint32_t CR2;    // 0x04: Control register 2
    volatile uint32_t SMCR;   // 0x08: Slave mode control register
    volatile uint32_t DIER;   // 0x0C: DMA/Interrupt enable register
    volatile uint32_t SR;     // 0x10: Status register
    volatile uint32_t EGR;    // 0x14: Event generation register
    volatile uint32_t CCMR1;  // 0x18: Capture/Compare mode register 1
    volatile uint32_t CCMR2;  // 0x1C: Capture/Compare mode register 2
    volatile uint32_t CCER;   // 0x20: Capture/Compare enable register
    volatile uint32_t CNT;    // 0x24: Counter
    volatile uint32_t PSC;    // 0x28: Prescaler
    volatile uint32_t ARR;    // 0x2C: Auto-reload register
    uint32_t RESERVED1;
    volatile uint32_t CCR1;   // 0x34: Capture/Compare register 1
    volatile uint32_t CCR2;   // 0x38: Capture/Compare register 2
    volatile uint32_t CCR3;   // 0x3C: Capture/Compare register 3
    volatile uint32_t CCR4;   // 0x40: Capture/Compare register 4
    uint32_t RESERVED2;
    volatile uint32_t DCR;    // 0x48: DMA control register
    volatile uint32_t DMAR;   // 0x4C: DMA address for full transfer
} TIM_TypeDef;

#define TIM2  ((TIM_TypeDef*)TIM2_BASE)
#define TIM3  ((TIM_TypeDef*)TIM3_BASE)
#define TIM4  ((TIM_TypeDef*)TIM4_BASE)
#define TIM5  ((TIM_TypeDef*)TIM5_BASE)
```

### Rejestr CR1 - Control Register 1

```
TIMx_CR1 - Control Register 1
Offset: 0x00
Reset value: 0x0000

Bit 0:  CEN    - Counter enable
Bit 1:  UDIS   - Update disable
Bit 2:  URS    - Update request source
Bit 3:  OPM    - One-pulse mode
Bit 4:  DIR    - Direction (0=up, 1=down)
Bit 5-6: CMS   - Center-aligned mode selection
Bit 7:  ARPE   - Auto-reload preload enable
Bit 8-9: CKD   - Clock division
```

### Rejestr PSC - Prescaler

```
TIMx_PSC - Prescaler Register
Offset: 0x28
Reset value: 0x0000

Bits 15:0 - PSC[15:0]: Prescaler value

Frequency = Timer_Clock / (PSC + 1)

Przykład:
Timer clock = 90 MHz
PSC = 8999
Frequency = 90,000,000 / (8999 + 1) = 10,000 Hz = 10 kHz
```

### Rejestr ARR - Auto-Reload Register

```
TIMx_ARR - Auto-Reload Register
Offset: 0x2C
Reset value: 0xFFFFFFFF (dla TIM2, TIM5)
Reset value: 0x0000FFFF (dla TIM3, TIM4)

Counter overflow gdy CNT == ARR

Period = (ARR + 1) / Frequency

Przykład:
Frequency = 10 kHz
ARR = 9999
Period = 10000 / 10000 = 1 Hz (1 sekunda)
```

### Rejestr CNT - Counter

```
TIMx_CNT - Counter Register
Offset: 0x24
Reset value: 0x00000000

Bieżąca wartość licznika.
- Inkrementowana przy każdym tick (up-counting)
- Dekrementowana (down-counting)
- Resetowana do 0 gdy osiągnie ARR
```

## 🎯 Podstawowa Konfiguracja Timera

### Obliczanie PSC i ARR

```c
/**
 * @brief  Wzory dla timera
 * 
 * Timer_Clock = APB_Clock × Multiplier
 * 
 * Dla APB1 (TIM2-TIM5):
 * - Jeśli APB1 prescaler = 1: Timer_Clock = APB1_Clock
 * - Jeśli APB1 prescaler > 1: Timer_Clock = APB1_Clock × 2
 * 
 * Przykład:
 * SYSCLK = 180 MHz
 * APB1 = SYSCLK / 4 = 45 MHz
 * Timer_Clock = 45 MHz × 2 = 90 MHz (bo prescaler > 1)
 * 
 * Update_Frequency = Timer_Clock / ((PSC + 1) × (ARR + 1))
 * 
 * Dla 1 Hz (1 sekunda):
 * 90,000,000 = (PSC + 1) × (ARR + 1) × 1
 * 
 * Możliwe kombinacje:
 * PSC = 8999, ARR = 9999  -> 90M / (9000 × 10000) = 1 Hz ✓
 * PSC = 89,   ARR = 999999 -> 90M / (90 × 1000000) = 1 Hz ✓
 */

/**
 * @brief  Oblicz PSC i ARR dla żądanej częstotliwości
 */
void Calculate_Timer_Values(uint32_t timer_clock, 
                            uint32_t desired_freq,
                            uint32_t *psc, 
                            uint32_t *arr)
{
    // Cel: Update_Freq = timer_clock / ((PSC+1) * (ARR+1))
    
    // Oblicz łączny dzielnik
    uint32_t total_div = timer_clock / desired_freq;
    
    // Rozdziel na PSC i ARR
    // Próbuj znaleźć najbardziej zbalansowane wartości
    
    // Prosty sposób: PSC mały, ARR duży
    *psc = 0;
    *arr = total_div - 1;
    
    // Jeśli ARR > 65535 dla 16-bit timera, zwiększ PSC
    if (*arr > 65535 && total_div > 65536) {
        *psc = (total_div / 65536);
        *arr = (total_div / (*psc + 1)) - 1;
    }
}

/**
 * @brief  Przykłady obliczeń
 */
void Timer_Calculation_Examples(void)
{
    // Timer clock = 90 MHz
    
    // Dla 1 kHz (1ms)
    uint32_t psc1, arr1;
    Calculate_Timer_Values(90000000, 1000, &psc1, &arr1);
    // psc = 0, arr = 89999 lub
    // psc = 89, arr = 999
    
    // Dla 1 Hz (1s)
    uint32_t psc2, arr2;
    Calculate_Timer_Values(90000000, 1, &psc2, &arr2);
    // psc = 8999, arr = 9999
    
    // Dla 10 kHz (100us)
    uint32_t psc3, arr3;
    Calculate_Timer_Values(90000000, 10000, &psc3, &arr3);
    // psc = 0, arr = 8999 lub
    // psc = 8, arr = 999
}
```

### Inicjalizacja Podstawowego Timera

```c
/**
 * @brief  TIM2 init - 1 Hz timebase (1 sekunda)
 * 
 * KROK PO KROKU:
 */
void TIM2_Init_1Hz(void)
{
    // KROK 1: Włącz zegar TIM2 (APB1)
    RCC->APB1ENR |= (1 << 0);  // TIM2EN
    
    // KROK 2: Wyłącz timer na czas konfiguracji
    TIM2->CR1 &= ~(1 << 0);  // CEN = 0
    
    // KROK 3: Ustaw prescaler
    // Timer clock = 90 MHz
    // PSC = 8999 -> 90MHz / 9000 = 10 kHz
    TIM2->PSC = 9000 - 1;
    
    // KROK 4: Ustaw auto-reload
    // ARR = 9999 -> 10kHz / 10000 = 1 Hz
    TIM2->ARR = 10000 - 1;
    
    // KROK 5: Ustaw direction (opcjonalnie)
    TIM2->CR1 &= ~(1 << 4);  // DIR = 0 (up-counting)
    
    // KROK 6: Włącz auto-reload preload
    TIM2->CR1 |= (1 << 7);   // ARPE = 1
    
    // KROK 7: Generate update event (załaduj PSC i ARR)
    TIM2->EGR |= (1 << 0);   // UG = 1
    
    // KROK 8: Wyczyść update flag
    TIM2->SR &= ~(1 << 0);   // UIF = 0
    
    // KROK 9: Włącz przerwanie update (opcjonalnie)
    TIM2->DIER |= (1 << 0);  // UIE = 1
    
    // KROK 10: Włącz przerwanie w NVIC
    NVIC_SetPriority(TIM2_IRQn, 5);
    NVIC_EnableIRQ(TIM2_IRQn);
    
    // KROK 11: Start timer
    TIM2->CR1 |= (1 << 0);   // CEN = 1
}

/**
 * @brief  TIM2 Interrupt Handler
 */
volatile uint32_t seconds_counter = 0;

void TIM2_IRQHandler(void)
{
    // Sprawdź update interrupt flag
    if (TIM2->SR & (1 << 0)) {
        // UIF = 1, overflow wystąpił
        
        seconds_counter++;
        
        // Toggle LED co sekundę
        GPIOA->ODR ^= (1 << 5);
        
        // WAŻNE: Wyczyść flagę!
        TIM2->SR &= ~(1 << 0);  // UIF = 0
    }
}
```

## 🔄 PWM - Pulse Width Modulation

### Tryb PWM w Timerze

```
PWM to szybkie przełączanie pinu HIGH/LOW z określonym duty cycle.

Frequency = Update_Frequency = Timer_Clock / ((PSC+1) × (ARR+1))
Duty_Cycle = (CCRx / ARR) × 100%

Przykład:
ARR = 999
CCR1 = 250  -> Duty = 250/999 = 25%
CCR1 = 500  -> Duty = 500/999 = 50%
CCR1 = 750  -> Duty = 750/999 = 75%
```

### Rejestr CCMR - Capture/Compare Mode Register

```
TIMx_CCMR1 - Capture/Compare Mode Register 1 (kanały 1-2)
TIMx_CCMR2 - Capture/Compare Mode Register 2 (kanały 3-4)

Dla kanału 1 (bity 0-7 w CCMR1):
Bit 0-1: CC1S   - Capture/Compare selection
         00 = Output
Bit 2:   OC1FE  - Output compare fast enable
Bit 3:   OC1PE  - Output compare preload enable
Bit 4-6: OC1M   - Output compare mode
         110 = PWM mode 1
         111 = PWM mode 2
Bit 7:   OC1CE  - Output compare clear enable
```

### Rejestr CCER - Capture/Compare Enable Register

```
TIMx_CCER - Capture/Compare Enable Register

Bit 0:  CC1E  - Capture/Compare 1 output enable
Bit 1:  CC1P  - Capture/Compare 1 output polarity
Bit 4:  CC2E  - Capture/Compare 2 output enable
Bit 5:  CC2P  - Capture/Compare 2 output polarity
Bit 8:  CC3E  - Capture/Compare 3 output enable
Bit 9:  CC3P  - Capture/Compare 3 output polarity
Bit 12: CC4E  - Capture/Compare 4 output enable
Bit 13: CC4P  - Capture/Compare 4 output polarity
```

### Konfiguracja PWM - Szczegółowo

```c
/**
 * @brief  TIM3 Channel 1 PWM @ 1 kHz, PA6
 * 
 * KROK PO KROKU:
 */
void TIM3_PWM_Init(void)
{
    // KROK 1: Włącz zegary
    RCC->AHB1ENR |= (1 << 0);   // GPIOA
    RCC->APB1ENR |= (1 << 1);   // TIM3
    
    // KROK 2: Konfiguruj pin PA6 jako AF (TIM3_CH1)
    // PA6 = AF2 (TIM3)
    GPIOA->MODER &= ~(0x3 << 12);
    GPIOA->MODER |= (0x2 << 12);   // Alternate function
    
    GPIOA->AFR[0] &= ~(0xF << 24);
    GPIOA->AFR[0] |= (0x2 << 24);  // AF2
    
    GPIOA->OSPEEDR |= (0x2 << 12); // High speed
    
    // KROK 3: Konfiguruj timer dla 1 kHz PWM
    // Timer clock = 90 MHz (APB1 × 2)
    // Dla 1 kHz: 90MHz / ((89+1) × (999+1)) = 1000 Hz
    
    TIM3->PSC = 90 - 1;    // 90 MHz / 90 = 1 MHz
    TIM3->ARR = 1000 - 1;  // 1 MHz / 1000 = 1 kHz
    
    // KROK 4: Konfiguruj kanał 1 jako PWM mode 1
    // CCMR1 dla kanału 1-2
    
    // CC1S = 00 (output)
    TIM3->CCMR1 &= ~(0x3 << 0);
    
    // OC1M = 110 (PWM mode 1)
    TIM3->CCMR1 &= ~(0x7 << 4);
    TIM3->CCMR1 |= (0x6 << 4);
    
    // OC1PE = 1 (preload enable)
    TIM3->CCMR1 |= (1 << 3);
    
    // KROK 5: Włącz output
    TIM3->CCER |= (1 << 0);  // CC1E = 1
    
    // Polarity (opcjonalnie)
    // TIM3->CCER &= ~(1 << 1);  // CC1P = 0 (active high)
    
    // KROK 6: Ustaw duty cycle (50% na start)
    TIM3->CCR1 = 500;  // 50% z 1000
    
    // KROK 7: Włącz auto-reload preload
    TIM3->CR1 |= (1 << 7);
    
    // KROK 8: Generate update event
    TIM3->EGR |= (1 << 0);
    
    // KROK 9: Start timer
    TIM3->CR1 |= (1 << 0);
}

/**
 * @brief  Ustawienie duty cycle
 */
void PWM_SetDutyCycle(uint16_t duty_percent)
{
    // duty_percent: 0-100
    uint32_t ccr_value = (TIM3->ARR + 1) * duty_percent / 100;
    TIM3->CCR1 = ccr_value;
}

/**
 * @brief  Przykłady użycia PWM
 */
void PWM_Examples(void)
{
    PWM_SetDutyCycle(0);    // 0% - LED OFF
    PWM_SetDutyCycle(25);   // 25% - ciemno
    PWM_SetDutyCycle(50);   // 50% - średnia jasność
    PWM_SetDutyCycle(75);   // 75% - jasno
    PWM_SetDutyCycle(100);  // 100% - max
}

/**
 * @brief  Płynne przygasanie/rozświetlanie
 */
void PWM_Fade(void)
{
    // Fade in
    for (int duty = 0; duty <= 100; duty++) {
        PWM_SetDutyCycle(duty);
        delay_ms(10);
    }
    
    // Fade out
    for (int duty = 100; duty >= 0; duty--) {
        PWM_SetDutyCycle(duty);
        delay_ms(10);
    }
}
```

## 📏 Input Capture - Pomiar Częstotliwości i Szerokości Impulsu

### Konfiguracja Input Capture

```c
/**
 * @brief  TIM4 Channel 1 Input Capture @ PB6
 * 
 * Cel: Zmierz częstotliwość sygnału wejściowego
 */

volatile uint32_t capture_value1 = 0;
volatile uint32_t capture_value2 = 0;
volatile uint8_t capture_done = 0;

void TIM4_InputCapture_Init(void)
{
    // Włącz zegary
    RCC->AHB1ENR |= (1 << 1);   // GPIOB
    RCC->APB1ENR |= (1 << 2);   // TIM4
    
    // Konfiguruj PB6 jako AF (TIM4_CH1 = AF2)
    GPIOB->MODER &= ~(0x3 << 12);
    GPIOB->MODER |= (0x2 << 12);
    GPIOB->AFR[0] &= ~(0xF << 24);
    GPIOB->AFR[0] |= (0x2 << 24);
    
    // Konfiguruj timer
    TIM4->PSC = 90 - 1;      // 90 MHz / 90 = 1 MHz (1us resolution)
    TIM4->ARR = 0xFFFF;      // Max dla 16-bit
    
    // Konfiguruj kanał 1 jako input capture
    // CC1S = 01 (IC1 mapped to TI1)
    TIM4->CCMR1 &= ~(0x3 << 0);
    TIM4->CCMR1 |= (0x1 << 0);
    
    // IC1F = 0000 (no filter)
    TIM4->CCMR1 &= ~(0xF << 4);
    
    // IC1PSC = 00 (no prescaler)
    TIM4->CCMR1 &= ~(0x3 << 2);
    
    // CC1P = 0 (rising edge)
    TIM4->CCER &= ~(1 << 1);
    
    // Włącz capture
    TIM4->CCER |= (1 << 0);  // CC1E = 1
    
    // Włącz przerwanie capture
    TIM4->DIER |= (1 << 1);  // CC1IE = 1
    
    NVIC_SetPriority(TIM4_IRQn, 4);
    NVIC_EnableIRQ(TIM4_IRQn);
    
    // Start timer
    TIM4->CR1 |= (1 << 0);
}

/**
 * @brief  TIM4 Interrupt Handler
 */
void TIM4_IRQHandler(void)
{
    if (TIM4->SR & (1 << 1)) {  // CC1IF
        if (!capture_done) {
            // Pierwszy pomiar
            capture_value1 = TIM4->CCR1;
            capture_done = 1;
        } else {
            // Drugi pomiar
            capture_value2 = TIM4->CCR1;
            
            // Oblicz różnicę (okres)
            uint32_t period;
            if (capture_value2 > capture_value1) {
                period = capture_value2 - capture_value1;
            } else {
                // Overflow
                period = (0xFFFF - capture_value1) + capture_value2;
            }
            
            // Frequency = 1MHz / period
            // np. period = 1000 -> freq = 1kHz
            
            capture_done = 0;  // Reset dla kolejnego pomiaru
        }
        
        // Wyczyść flagę
        TIM4->SR &= ~(1 << 1);
    }
}
```

### Pomiar Szerokości Impulsu (Pulse Width)

```c
/**
 * @brief  Pomiar szerokości impulsu HIGH
 * 
 * Używa dwóch kanałów:
 * - CH1: Rising edge
 * - CH2: Falling edge
 */

volatile uint32_t pulse_start = 0;
volatile uint32_t pulse_width = 0;

void TIM4_PulseWidth_Init(void)
{
    // Podobna inicjalizacja jak Input Capture
    
    // CH1: Rising edge
    TIM4->CCMR1 &= ~(0x3 << 0);
    TIM4->CCMR1 |= (0x1 << 0);   // IC1 = TI1
    TIM4->CCER &= ~(1 << 1);     // Rising
    TIM4->CCER |= (1 << 0);      // Enable
    
    // CH2: Falling edge (na tym samym pinie TI1)
    TIM4->CCMR1 &= ~(0x3 << 8);
    TIM4->CCMR1 |= (0x2 << 8);   // IC2 = TI1
    TIM4->CCER |= (1 << 5);      // Falling
    TIM4->CCER |= (1 << 4);      // Enable
    
    // Interrupts
    TIM4->DIER |= (1 << 1) | (1 << 2);  // CC1IE, CC2IE
    
    NVIC_EnableIRQ(TIM4_IRQn);
    TIM4->CR1 |= (1 << 0);
}

void TIM4_IRQHandler_PulseWidth(void)
{
    if (TIM4->SR & (1 << 1)) {  // CC1IF - Rising
        pulse_start = TIM4->CCR1;
        TIM4->SR &= ~(1 << 1);
    }
    
    if (TIM4->SR & (1 << 2)) {  // CC2IF - Falling
        uint32_t pulse_end = TIM4->CCR2;
        
        if (pulse_end > pulse_start) {
            pulse_width = pulse_end - pulse_start;
        } else {
            pulse_width = (0xFFFF - pulse_start) + pulse_end;
        }
        
        // pulse_width w mikrosekundach (jeśli timer @ 1MHz)
        
        TIM4->SR &= ~(1 << 2);
    }
}
```

## 🎯 Encoder Interface

### Konfiguracja Encoder Mode

```c
/**
 * @brief  TIM3 Encoder Interface
 * 
 * Enkoder: 2 sygnały (A i B) o przesuniętej fazie
 * Służy do pomiaru pozycji i kierunku obrotu
 * 
 * Piny: PA6 = TI1 (A), PA7 = TI2 (B)
 */

void TIM3_Encoder_Init(void)
{
    // Włącz zegary
    RCC->AHB1ENR |= (1 << 0);
    RCC->APB1ENR |= (1 << 1);
    
    // Konfiguruj piny PA6, PA7 jako AF2
    GPIOA->MODER &= ~((0x3 << 12) | (0x3 << 14));
    GPIOA->MODER |= ((0x2 << 12) | (0x2 << 14));
    GPIOA->AFR[0] &= ~((0xF << 24) | (0xF << 28));
    GPIOA->AFR[0] |= ((0x2 << 24) | (0x2 << 28));
    
    // Konfiguruj encoder mode
    // SMS = 011 (Encoder mode 3 - count on both edges)
    TIM3->SMCR &= ~(0x7 << 0);
    TIM3->SMCR |= (0x3 << 0);
    
    // Konfiguruj input channels
    // TI1, TI2 as inputs
    TIM3->CCMR1 &= ~((0x3 << 0) | (0x3 << 8));
    TIM3->CCMR1 |= ((0x1 << 0) | (0x1 << 8));
    
    // Polarity
    TIM3->CCER &= ~((1 << 1) | (1 << 5));
    
    // Enable channels
    TIM3->CCER |= (1 << 0) | (1 << 4);
    
    // Set ARR (max count)
    TIM3->ARR = 0xFFFF;
    
    // Start from 0
    TIM3->CNT = 0;
    
    // Enable timer
    TIM3->CR1 |= (1 << 0);
}

/**
 * @brief  Odczyt pozycji enkodera
 */
int32_t Encoder_Get_Position(void)
{
    return (int32_t)TIM3->CNT;
}

/**
 * @brief  Reset pozycji
 */
void Encoder_Reset(void)
{
    TIM3->CNT = 0;
}
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_nvic|Bare Metal - NVIC i przerwania]]
- [[stm32f429i_bare_metal_gpio|Bare Metal - GPIO dla AF]]
- [[stm32f429i_bare_metal_pwm_serwo|Bare Metal - Sterowanie Serwomechanizmem]]
- [[stm32f429i_timery|Timery z HAL - porównanie]]

## 📝 Podsumowanie

### Kluczowe Rejestry Timera
- **PSC** - Prescaler (dzielnik zegara)
- **ARR** - Auto-reload (okres)
- **CNT** - Counter (bieżąca wartość)
- **CCRx** - Capture/Compare (dla PWM, IC)
- **CR1** - Control (enable, direction)
- **CCMR1/2** - Mode configuration (PWM, IC)
- **CCER** - Channel enable
- **DIER** - Interrupt enable

### Wzory
```
Update_Freq = Timer_Clock / ((PSC+1) × (ARR+1))
PWM_Duty = (CCRx / ARR) × 100%
```

### Tryby Pracy
- **Timebase** - Podstawowy licznik z przerwaniem
- **PWM** - Generowanie sygnału PWM
- **Input Capture** - Pomiar częstotliwości/szerokości
- **Output Compare** - Generowanie impulsów
- **Encoder** - Interfejs enkodera

---

*Następna notatka: [[stm32f429i_bare_metal_spi|Bare Metal - SPI Komunikacja]]*
