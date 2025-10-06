# STM32F429I - Bare Metal - ADC Konwerter Analogowo-Cyfrowy

## 🔬 ADC - Analog-to-Digital Converter

### Czym Jest ADC?

```
ADC konwertuje napięcie analogowe na wartość cyfrową.

STM32F429 ma 3 ADC:
- ADC1, ADC2, ADC3
- 12-bit resolution (0-4095)
- Do 24 kanałów (16 external + 3 internal)
- Sampling time konfigurowalny
- Multiple modes (single, continuous, scan, etc.)
- DMA support
- Max conversion rate: 2.4 MSPS

Zakres napięć:
- VREF- to VREF+ (typowo 0V to 3.3V)
- Digital value = (Vin / VREF+) × 4095

Przykład:
Vin = 1.65V, VREF+ = 3.3V
Digital = (1.65 / 3.3) × 4095 = 2047.5 ≈ 2048
```

### Kanały ADC

```
External channels:
- ADC1_IN0 - ADC1_IN15  (PA0-PA7, PB0-PB1, PC0-PC5)
- ADC2_IN0 - ADC2_IN15
- ADC3_IN0 - ADC3_IN15

Internal channels (wspólne dla wszystkich ADC):
- ADC_IN16: Temperature sensor
- ADC_IN17: VREFINT (internal reference 1.21V)
- ADC_IN18: VBAT/4 (battery voltage)

Przykładowe mapowanie pinów:
PA0 = ADC123_IN0
PA1 = ADC123_IN1
...
PF3 = ADC3_IN9
```

## 📋 Rejestry ADC

### Adresy Bazowe

```c
/**
 * @brief  ADC Base Addresses
 */
#define ADC1_BASE  0x40012000UL  // APB2
#define ADC2_BASE  0x40012100UL  // APB2
#define ADC3_BASE  0x40012200UL  // APB2
#define ADC_COMMON_BASE  0x40012300UL  // Common registers

/**
 * @brief  Struktura ADC
 */
typedef struct {
    volatile uint32_t SR;     // 0x00: Status register
    volatile uint32_t CR1;    // 0x04: Control register 1
    volatile uint32_t CR2;    // 0x08: Control register 2
    volatile uint32_t SMPR1;  // 0x0C: Sample time register 1
    volatile uint32_t SMPR2;  // 0x10: Sample time register 2
    volatile uint32_t JOFR1;  // 0x14: Injected channel data offset register 1
    volatile uint32_t JOFR2;  // 0x18: Injected channel data offset register 2
    volatile uint32_t JOFR3;  // 0x1C: Injected channel data offset register 3
    volatile uint32_t JOFR4;  // 0x20: Injected channel data offset register 4
    volatile uint32_t HTR;    // 0x24: Watchdog high threshold register
    volatile uint32_t LTR;    // 0x28: Watchdog low threshold register
    volatile uint32_t SQR1;   // 0x2C: Regular sequence register 1
    volatile uint32_t SQR2;   // 0x30: Regular sequence register 2
    volatile uint32_t SQR3;   // 0x34: Regular sequence register 3
    volatile uint32_t JSQR;   // 0x38: Injected sequence register
    volatile uint32_t JDR1;   // 0x3C: Injected data register 1
    volatile uint32_t JDR2;   // 0x40: Injected data register 2
    volatile uint32_t JDR3;   // 0x44: Injected data register 3
    volatile uint32_t JDR4;   // 0x48: Injected data register 4
    volatile uint32_t DR;     // 0x4C: Regular data register
} ADC_TypeDef;

/**
 * @brief  ADC Common registers
 */
typedef struct {
    volatile uint32_t CSR;   // 0x00: Common status register
    volatile uint32_t CCR;   // 0x04: Common control register
    volatile uint32_t CDR;   // 0x08: Common regular data register (multi-ADC)
} ADC_Common_TypeDef;

#define ADC1  ((ADC_TypeDef*)ADC1_BASE)
#define ADC2  ((ADC_TypeDef*)ADC2_BASE)
#define ADC3  ((ADC_TypeDef*)ADC3_BASE)
#define ADC_COMMON  ((ADC_Common_TypeDef*)ADC_COMMON_BASE)
```

### Rejestr CR1 - Control Register 1

```
ADC_CR1 - Control Register 1
Offset: 0x04
Reset value: 0x00000000

Bits 0-4:  AWDCH[4:0]  - Analog watchdog channel select
Bit 5:     EOCIE       - Interrupt enable for EOC
Bit 6:     AWDIE       - Analog watchdog interrupt enable
Bit 7:     JEOCIE      - Interrupt enable for injected channels
Bit 8:     SCAN        - Scan mode
Bit 9:     AWDSGL      - Enable watchdog on a single channel
Bit 10:    JAUTO       - Automatic injected group conversion
Bit 11:    DISCEN      - Discontinuous mode on regular channels
Bit 12:    JDISCEN     - Discontinuous mode on injected channels
Bits 13-15: DISCNUM[2:0] - Discontinuous mode channel count
Bit 22:    JAWDEN      - Analog watchdog enable on injected channels
Bit 23:    AWDEN       - Analog watchdog enable on regular channels
Bits 24-25: RES[1:0]   - Resolution
                         00: 12-bit
                         01: 10-bit
                         10: 8-bit
                         11: 6-bit
Bit 26:    OVRIE       - Overrun interrupt enable
```

### Rejestr CR2 - Control Register 2

```
ADC_CR2 - Control Register 2
Offset: 0x08
Reset value: 0x00000000

Bit 0:     ADON        - ADC ON/OFF
Bit 1:     CONT        - Continuous conversion
Bit 8:     DMA         - Direct memory access mode
Bit 9:     DDS         - DMA disable selection
Bit 10:    EOCS        - End of conversion selection
Bit 11:    ALIGN       - Data alignment (0=right, 1=left)
Bits 16-19: JEXTSEL[3:0] - External event select for injected
Bits 20-21: JEXTEN[1:0]  - External trigger enable for injected
Bit 22:    JSWSTART    - Start conversion of injected channels
Bits 24-27: EXTSEL[3:0]  - External event select for regular
Bits 28-29: EXTEN[1:0]   - External trigger enable for regular
                           00: Trigger detection disabled
                           01: Rising edge
                           10: Falling edge
                           11: Both edges
Bit 30:    SWSTART     - Start conversion of regular channels
```

### Rejestr SR - Status Register

```
ADC_SR - Status Register
Offset: 0x00
Reset value: 0x00000000

Bit 0:  AWD   - Analog watchdog flag
Bit 1:  EOC   - Regular channel end of conversion
Bit 2:  JEOC  - Injected channel end of conversion
Bit 3:  JSTRT - Injected channel start flag
Bit 4:  STRT  - Regular channel start flag
Bit 5:  OVR   - Overrun
```

### Rejestr SMPR1/SMPR2 - Sample Time Registers

```
SMPR1 - Sample time dla kanałów 10-18
SMPR2 - Sample time dla kanałów 0-9

Każdy kanał ma 3 bity dla sample time:
000: 3 cycles
001: 15 cycles
010: 28 cycles
011: 56 cycles
100: 84 cycles
101: 112 cycles
110: 144 cycles
111: 480 cycles

Przykład dla kanału 0 (bity 0-2 w SMPR2):
SMPR2 = 0x4;  // 100 = 84 cycles

Total conversion time = Sample time + 12 cycles
Dla 84 cycles: Total = 84 + 12 = 96 cycles
```

### Rejestr SQR1/SQR2/SQR3 - Sequence Registers

```
SQR1 - Sequence 13-16 + length
SQR2 - Sequence 7-12
SQR3 - Sequence 1-6

SQR1:
Bits 0-4:   SQ13[4:0]
Bits 5-9:   SQ14[4:0]
Bits 10-14: SQ15[4:0]
Bits 15-19: SQ16[4:0]
Bits 20-23: L[3:0] - Sequence length (0-15, czyli 1-16 konwersji)

Przykład:
L = 0:  1 konwersja (tylko SQ1)
L = 3:  4 konwersje (SQ1, SQ2, SQ3, SQ4)
L = 15: 16 konwersji (SQ1-SQ16)
```

## 🔧 Konfiguracja ADC - Single Channel

### Podstawowa Inicjalizacja ADC1

```c
/**
 * @brief  ADC1 init - single channel @ PA0 (ADC1_IN0)
 * 
 * Mode: Single conversion
 * Resolution: 12-bit
 * Sample time: 84 cycles
 * 
 * KROK PO KROKU:
 */

void ADC1_Init_SingleChannel(void)
{
    // KROK 1: Włącz zegary
    RCC->AHB1ENR |= (1 << 0);   // GPIOA
    RCC->APB2ENR |= (1 << 8);   // ADC1
    
    // KROK 2: Konfiguruj pin PA0 jako analog
    GPIOA->MODER |= (0x3 << 0);  // Analog mode (11)
    
    // KROK 3: Ustaw prescaler dla ADC clock
    // ADC clock = APB2 / prescaler
    // APB2 = 90 MHz, chcemy max 36 MHz dla ADC
    // Prescaler = 4 -> 90 MHz / 4 = 22.5 MHz
    ADC_COMMON->CCR &= ~(0x3 << 16);
    ADC_COMMON->CCR |= (0x1 << 16);  // ADCPRE = 01 (/4)
    
    // KROK 4: Włącz ADC
    ADC1->CR2 |= (1 << 0);  // ADON = 1
    
    // Delay dla stabilizacji
    for (volatile int i = 0; i < 1000; i++);
    
    // KROK 5: Ustaw resolution (12-bit)
    ADC1->CR1 &= ~(0x3 << 24);  // RES = 00 (12-bit)
    
    // KROK 6: Disable continuous mode
    ADC1->CR2 &= ~(1 << 1);  // CONT = 0 (single conversion)
    
    // KROK 7: Ustaw sample time dla kanału 0
    // 84 cycles = 100 w SMPR2 dla kanału 0 (bity 0-2)
    ADC1->SMPR2 &= ~(0x7 << 0);
    ADC1->SMPR2 |= (0x4 << 0);  // 100 = 84 cycles
    
    // KROK 8: Ustaw sequence (1 kanał = kanał 0)
    // SQR1: L = 0 (1 konwersja)
    ADC1->SQR1 &= ~(0xF << 20);  // L = 0000
    
    // SQR3: SQ1 = 0 (kanał 0)
    ADC1->SQR3 &= ~(0x1F << 0);
    ADC1->SQR3 |= (0 << 0);  // Kanał 0
    
    // KROK 9: Data alignment (right)
    ADC1->CR2 &= ~(1 << 11);  // ALIGN = 0 (right aligned)
}

/**
 * @brief  Odczyt ADC - single conversion
 */
uint16_t ADC_Read(void)
{
    // KROK 1: Start conversion
    ADC1->CR2 |= (1 << 30);  // SWSTART = 1
    
    // KROK 2: Czekaj na EOC
    while (!(ADC1->SR & (1 << 1)));
    
    // KROK 3: Odczytaj dane (automatycznie czyści EOC)
    return ADC1->DR & 0xFFF;  // 12-bit mask
}

/**
 * @brief  Konwersja do napięcia
 */
float ADC_ToVoltage(uint16_t adc_value)
{
    // VREF+ = 3.3V
    return (adc_value * 3.3f) / 4095.0f;
}

/**
 * @brief  Przykład użycia
 */
void ADC_Example(void)
{
    ADC1_Init_SingleChannel();
    
    while (1) {
        uint16_t value = ADC_Read();
        float voltage = ADC_ToVoltage(value);
        
        printf("ADC: %d, Voltage: %.3fV\r\n", value, voltage);
        delay_ms(500);
    }
}
```

## 🔄 Continuous Mode

### Konfiguracja Trybu Ciągłego

```c
/**
 * @brief  ADC1 Continuous mode
 * 
 * W trybie ciągłym, ADC automatycznie startuje kolejną konwersję
 * po zakończeniu poprzedniej.
 */

void ADC1_Init_Continuous(void)
{
    // Podstawowa inicjalizacja (jak wcześniej)
    ADC1_Init_SingleChannel();
    
    // DODATKOWO: Włącz continuous mode
    ADC1->CR2 |= (1 << 1);  // CONT = 1
    
    // Start pierwszej konwersji
    ADC1->CR2 |= (1 << 30);  // SWSTART
}

/**
 * @brief  Odczyt w trybie ciągłym
 */
uint16_t ADC_Read_Continuous(void)
{
    // Czekaj na EOC
    while (!(ADC1->SR & (1 << 1)));
    
    // Odczytaj dane
    return ADC1->DR & 0xFFF;
    
    // Nowa konwersja startuje automatycznie!
}
```

## 📊 Scan Mode - Multiple Channels

### Skanowanie Wielu Kanałów

```c
/**
 * @brief  ADC1 Scan mode - 4 kanały
 * 
 * Kanały: ADC1_IN0 (PA0), IN1 (PA1), IN2 (PA2), IN3 (PA3)
 * Mode: Scan + Continuous
 */

#define ADC_NUM_CHANNELS  4

volatile uint16_t adc_values[ADC_NUM_CHANNELS];
volatile uint8_t adc_conversion_complete = 0;

void ADC1_Init_ScanMode(void)
{
    // KROK 1: Włącz zegary i konfiguruj piny
    RCC->AHB1ENR |= (1 << 0);
    RCC->APB2ENR |= (1 << 8);
    
    // PA0-PA3 jako analog
    GPIOA->MODER |= (0x3 << 0) | (0x3 << 2) | (0x3 << 4) | (0x3 << 6);
    
    // KROK 2: Prescaler ADC
    ADC_COMMON->CCR &= ~(0x3 << 16);
    ADC_COMMON->CCR |= (0x1 << 16);  // /4
    
    // KROK 3: Włącz ADC
    ADC1->CR2 |= (1 << 0);
    for (volatile int i = 0; i < 1000; i++);
    
    // KROK 4: Włącz SCAN mode
    ADC1->CR1 |= (1 << 8);  // SCAN = 1
    
    // KROK 5: Continuous mode
    ADC1->CR2 |= (1 << 1);  // CONT = 1
    
    // KROK 6: Sample time dla kanałów 0-3
    ADC1->SMPR2 &= ~(0x7 << 0);
    ADC1->SMPR2 |= (0x4 << 0);   // CH0: 84 cycles
    ADC1->SMPR2 &= ~(0x7 << 3);
    ADC1->SMPR2 |= (0x4 << 3);   // CH1: 84 cycles
    ADC1->SMPR2 &= ~(0x7 << 6);
    ADC1->SMPR2 |= (0x4 << 6);   // CH2: 84 cycles
    ADC1->SMPR2 &= ~(0x7 << 9);
    ADC1->SMPR2 |= (0x4 << 9);   // CH3: 84 cycles
    
    // KROK 7: Sequence length = 4
    ADC1->SQR1 &= ~(0xF << 20);
    ADC1->SQR1 |= (3 << 20);  // L = 3 (4 konwersje)
    
    // KROK 8: Sequence channels
    // SQ1 = CH0, SQ2 = CH1, SQ3 = CH2, SQ4 = CH3
    ADC1->SQR3 &= ~(0x1F << 0);
    ADC1->SQR3 |= (0 << 0);   // SQ1 = CH0
    ADC1->SQR3 &= ~(0x1F << 5);
    ADC1->SQR3 |= (1 << 5);   // SQ2 = CH1
    ADC1->SQR3 &= ~(0x1F << 10);
    ADC1->SQR3 |= (2 << 10);  // SQ3 = CH2
    ADC1->SQR3 &= ~(0x1F << 15);
    ADC1->SQR3 |= (3 << 15);  // SQ4 = CH3
    
    // KROK 9: DMA mode
    ADC1->CR2 |= (1 << 8);   // DMA = 1
    ADC1->CR2 |= (1 << 9);   // DDS = 1 (DMA continuous)
    
    // KROK 10: Enable DMA dla ADC
    // (konfiguracja DMA w osobnej notatce)
    
    // KROK 11: Start conversion
    ADC1->CR2 |= (1 << 30);  // SWSTART
}

/**
 * @brief  Odczyt w scan mode (bez DMA)
 */
void ADC_Read_ScanMode(void)
{
    for (uint8_t i = 0; i < ADC_NUM_CHANNELS; i++) {
        // Czekaj na EOC
        while (!(ADC1->SR & (1 << 1)));
        
        // Odczytaj dane
        adc_values[i] = ADC1->DR & 0xFFF;
    }
    
    adc_conversion_complete = 1;
}
```

## 🌡️ Internal Temperature Sensor

### Pomiar Temperatury

```c
/**
 * @brief  ADC Temperature Sensor
 * 
 * Temperature sensor jest na kanale 16 (ADC_IN16)
 * Wymaga włączenia w ADC_CCR
 */

void ADC_TempSensor_Init(void)
{
    // Podstawowa init
    RCC->APB2ENR |= (1 << 8);
    ADC_COMMON->CCR |= (0x1 << 16);  // Prescaler /4
    
    // Włącz temperature sensor
    ADC_COMMON->CCR |= (1 << 23);  // TSVREFE = 1
    
    // Włącz ADC
    ADC1->CR2 |= (1 << 0);
    for (volatile int i = 0; i < 1000; i++);
    
    // Sample time dla kanału 16 (min 10us wymagane)
    // Przy 22.5 MHz ADC clock, 10us = 225 cycles
    // Używamy 480 cycles dla pewności
    ADC1->SMPR1 &= ~(0x7 << 18);  // Kanał 16: bity 18-20
    ADC1->SMPR1 |= (0x7 << 18);   // 111 = 480 cycles
    
    // Sequence: 1 kanał = kanał 16
    ADC1->SQR1 &= ~(0xF << 20);  // L = 0
    ADC1->SQR3 &= ~(0x1F << 0);
    ADC1->SQR3 |= (16 << 0);     // SQ1 = CH16
}

/**
 * @brief  Odczyt temperatury
 * 
 * Formuła z Reference Manual:
 * Temperature (°C) = ((V25 - Vsense) / Avg_Slope) + 25
 * 
 * Dla STM32F429:
 * V25 = 0.76V (typowo)
 * Avg_Slope = 2.5 mV/°C
 */
float ADC_ReadTemperature(void)
{
    // Start conversion
    ADC1->CR2 |= (1 << 30);
    
    // Czekaj na EOC
    while (!(ADC1->SR & (1 << 1)));
    
    // Odczytaj ADC
    uint16_t adc_value = ADC1->DR & 0xFFF;
    
    // Konwertuj na napięcie
    float vsense = (adc_value * 3.3f) / 4095.0f;
    
    // Oblicz temperaturę
    const float V25 = 0.76f;           // V
    const float Avg_Slope = 0.0025f;   // V/°C
    
    float temperature = ((V25 - vsense) / Avg_Slope) + 25.0f;
    
    return temperature;
}

/**
 * @brief  Przykład użycia
 */
void TempSensor_Example(void)
{
    ADC_TempSensor_Init();
    
    while (1) {
        float temp = ADC_ReadTemperature();
        printf("Temperature: %.1f°C\r\n", temp);
        delay_ms(1000);
    }
}
```

## ⚡ ADC z Przerwaniem

### Konfiguracja Przerwań EOC

```c
/**
 * @brief  ADC1 z przerwaniem End-of-Conversion
 */

volatile uint16_t adc_result;
volatile uint8_t adc_ready = 0;

void ADC1_Init_Interrupt(void)
{
    ADC1_Init_SingleChannel();
    
    // Włącz przerwanie EOC
    ADC1->CR1 |= (1 << 5);  // EOCIE = 1
    
    // NVIC
    NVIC_SetPriority(ADC_IRQn, 5);
    NVIC_EnableIRQ(ADC_IRQn);
}

/**
 * @brief  Start konwersji (non-blocking)
 */
void ADC_StartConversion(void)
{
    adc_ready = 0;
    ADC1->CR2 |= (1 << 30);  // SWSTART
}

/**
 * @brief  ADC Interrupt Handler
 */
void ADC_IRQHandler(void)
{
    if (ADC1->SR & (1 << 1)) {  // EOC
        adc_result = ADC1->DR & 0xFFF;
        adc_ready = 1;
        
        // EOC cleared automatycznie przez odczyt DR
    }
}

/**
 * @brief  Użycie z przerwaniem
 */
void ADC_Interrupt_Example(void)
{
    ADC1_Init_Interrupt();
    
    while (1) {
        ADC_StartConversion();
        
        // Czekaj na wynik
        while (!adc_ready);
        
        float voltage = ADC_ToVoltage(adc_result);
        printf("Voltage: %.3fV\r\n", voltage);
        
        delay_ms(500);
    }
}
```

## 🎯 Analog Watchdog

### Monitorowanie Zakresu Napięcia

```c
/**
 * @brief  Analog Watchdog - alarm gdy napięcie poza zakresem
 */

#define ADC_LOW_THRESHOLD   1000  // ~0.8V
#define ADC_HIGH_THRESHOLD  3000  // ~2.4V

void ADC_Watchdog_Init(void)
{
    ADC1_Init_SingleChannel();
    
    // Ustaw threshold
    ADC1->LTR = ADC_LOW_THRESHOLD;
    ADC1->HTR = ADC_HIGH_THRESHOLD;
    
    // Enable watchdog na kanale 0
    ADC1->CR1 |= (1 << 23);  // AWDEN = 1
    ADC1->CR1 |= (1 << 9);   // AWDSGL = 1 (single channel)
    ADC1->CR1 &= ~(0x1F << 0);
    ADC1->CR1 |= (0 << 0);   // AWDCH = 0 (kanał 0)
    
    // Enable watchdog interrupt
    ADC1->CR1 |= (1 << 6);   // AWDIE = 1
    
    NVIC_EnableIRQ(ADC_IRQn);
}

/**
 * @brief  ADC Handler z Watchdog
 */
void ADC_IRQHandler_Watchdog(void)
{
    if (ADC1->SR & (1 << 0)) {  // AWD flag
        // Napięcie poza zakresem!
        uint16_t value = ADC1->DR;
        
        if (value < ADC_LOW_THRESHOLD) {
            printf("ALARM: Voltage too LOW!\r\n");
        } else if (value > ADC_HIGH_THRESHOLD) {
            printf("ALARM: Voltage too HIGH!\r\n");
        }
        
        // Wyczyść flagę
        ADC1->SR &= ~(1 << 0);
    }
}
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_gpio|Bare Metal - GPIO dla Analog mode]]
- [[stm32f429i_bare_metal_dma|Bare Metal - DMA z ADC]]
- [[stm32f429i_bare_metal_timer|Bare Metal - Timer trigger dla ADC]]
- [[stm32f429i_adc|ADC z HAL - porównanie]]

## 📝 Podsumowanie

### Kluczowe Rejestry ADC
- **CR1** - Control (SCAN, RES, interrupts, watchdog)
- **CR2** - Control (ADON, CONT, DMA, SWSTART)
- **SR** - Status (EOC, AWD, OVR)
- **DR** - Data register (12-bit result)
- **SMPR1/SMPR2** - Sample time (3-480 cycles)
- **SQR1/SQR2/SQR3** - Sequence (16 channels max)
- **CCR** - Common (prescaler, TSVREFE)

### Conversion Time
```
Total = Sample_Time + 12 cycles
Dla 84 cycles sample: Total = 84 + 12 = 96 cycles
Przy 22.5 MHz ADC clock: Time = 96 / 22.5MHz = 4.27 μs
```

### Tryby Pracy
- **Single** - Jedna konwersja, potem stop
- **Continuous** - Automatyczne powtarzanie
- **Scan** - Sekwencja wielu kanałów
- **Discontinuous** - Przerwy między konwersjami

### Kolejność Inicjalizacji
1. Włącz zegary (GPIO + ADC)
2. Konfiguruj pin jako analog
3. Ustaw prescaler ADC
4. Włącz ADC (ADON=1, delay)
5. Ustaw resolution
6. Ustaw sample time
7. Ustaw sequence
8. Start conversion (SWSTART)

### Konwersja na Napięcie
```c
Voltage = (ADC_Value * VREF+) / 4095
// Dla VREF+ = 3.3V:
Voltage = (ADC_Value * 3.3) / 4095
```

---

*Następna notatka: [[stm32f429i_bare_metal_dma|Bare Metal - DMA Transfer Danych]]*
