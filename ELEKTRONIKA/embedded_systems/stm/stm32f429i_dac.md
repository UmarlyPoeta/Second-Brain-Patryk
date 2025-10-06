# STM32F429I - DAC i Generowanie Sygnałów Analogowych

## 🎵 Digital-to-Analog Converter (DAC)

### Charakterystyka DAC w STM32F429I

| Parametr | Wartość |
|----------|---------|
| Liczba DAC | 2 kanały (DAC1, DAC2) |
| Rozdzielczość | 12-bit (0-4095) |
| Wyjście | PA4 (DAC_OUT1), PA5 (DAC_OUT2) |
| Napięcie wyjściowe | 0V - VREF+ (typowo 0-3.3V) |
| Czas ustalania | ~3 µs (przy 1 MΩ, 50 pF) |
| Tryby pracy | Normalne, DMA, Timer trigger |
| Buffer | Wbudowany wzmacniacz buforujący |

### Architektura DAC

```
┌─────────────────────────────────────────┐
│          DAC Module                     │
│  ┌──────────────┐    ┌───────────┐     │
│  │  12-bit DAC  │───▶│  Output   │───▶ PA4/PA5
│  │   Register   │    │  Buffer   │     │
│  └──────┬───────┘    └───────────┘     │
│         │                               │
│    ┌────▼────────────────┐             │
│    │  Trigger Sources:   │             │
│    │  - Software         │             │
│    │  - Timer (2/4/5/6/7/8) │         │
│    │  - External (EXTI9) │             │
│    └─────────────────────┘             │
└─────────────────────────────────────────┘
```

## 🔧 Podstawowa konfiguracja DAC

### DAC w trybie podstawowym (Software Trigger)

```c
/**
 * @brief  Konfiguracja DAC Channel 1 (PA4)
 */
DAC_HandleTypeDef hdac;

void DAC1_Init(void)
{
    DAC_ChannelConfTypeDef sConfig = {0};
    
    __HAL_RCC_DAC_CLK_ENABLE();
    
    // Konfiguracja DAC
    hdac.Instance = DAC;
    
    if (HAL_DAC_Init(&hdac) != HAL_OK) {
        Error_Handler();
    }
    
    // Konfiguracja kanału 1
    sConfig.DAC_Trigger = DAC_TRIGGER_NONE;  // Software trigger
    sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;  // Bufor włączony
    
    if (HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Konfiguracja GPIO dla DAC
 */
void DAC1_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // PA4 jako analog dla DAC_OUT1
    GPIO_InitStruct.Pin = GPIO_PIN_4;
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

/**
 * @brief  Ustawienie wartości DAC
 */
void DAC_SetValue(uint16_t value)
{
    // Wartość 0-4095 dla 12-bit DAC
    if (value > 4095) value = 4095;
    
    // Ustaw wartość i wystartuj DAC
    HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, value);
    HAL_DAC_Start(&hdac, DAC_CHANNEL_1);
}

/**
 * @brief  Ustawienie napięcia wyjściowego (0-3.3V)
 */
void DAC_SetVoltage(float voltage)
{
    // VREF = 3.3V
    if (voltage > 3.3f) voltage = 3.3f;
    if (voltage < 0.0f) voltage = 0.0f;
    
    // Oblicz wartość DAC
    uint16_t dac_value = (uint16_t)((voltage / 3.3f) * 4095.0f);
    
    DAC_SetValue(dac_value);
}
```

## 📊 Generowanie przebiegów

### Fala trójkątna

```c
/**
 * @brief  Generowanie fali trójkątnej
 */
void DAC_GenerateTriangle(void)
{
    static uint16_t value = 0;
    static int8_t direction = 1;
    
    // Ustaw wartość
    DAC_SetValue(value);
    
    // Zmiana wartości
    if (direction > 0) {
        value += 10;
        if (value >= 4095) {
            value = 4095;
            direction = -1;
        }
    } else {
        value -= 10;
        if (value == 0) {
            direction = 1;
        }
    }
}

/**
 * @brief  Wywołaj w timerze dla ciągłego przebiegu
 */
void TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM6) {
        DAC_GenerateTriangle();
    }
}
```

### Fala sinusoidalna (lookup table)

```c
/**
 * @brief  Tablica wartości sinusa (256 próbek)
 */
const uint16_t sine_wave[256] = {
    2048, 2098, 2148, 2198, 2248, 2298, 2348, 2398, 2447, 2496,
    2545, 2594, 2642, 2690, 2737, 2784, 2831, 2877, 2923, 2968,
    3013, 3057, 3100, 3143, 3185, 3226, 3267, 3307, 3346, 3385,
    3423, 3459, 3495, 3530, 3565, 3598, 3630, 3662, 3692, 3722,
    3750, 3777, 3804, 3829, 3853, 3876, 3898, 3919, 3939, 3958,
    3975, 3992, 4007, 4021, 4034, 4045, 4056, 4065, 4073, 4080,
    4086, 4090, 4093, 4095, 4095, 4095, 4093, 4090, 4086, 4080,
    4073, 4065, 4056, 4045, 4034, 4021, 4007, 3992, 3975, 3958,
    3939, 3919, 3898, 3876, 3853, 3829, 3804, 3777, 3750, 3722,
    3692, 3662, 3630, 3598, 3565, 3530, 3495, 3459, 3423, 3385,
    3346, 3307, 3267, 3226, 3185, 3143, 3100, 3057, 3013, 2968,
    2923, 2877, 2831, 2784, 2737, 2690, 2642, 2594, 2545, 2496,
    2447, 2398, 2348, 2298, 2248, 2198, 2148, 2098, 2048, 1998,
    1948, 1898, 1848, 1798, 1748, 1698, 1649, 1600, 1551, 1502,
    1454, 1406, 1359, 1312, 1265, 1219, 1173, 1128, 1083, 1039,
    996, 953, 911, 870, 829, 789, 750, 711, 673, 637,
    601, 566, 531, 498, 466, 434, 404, 374, 346, 319,
    292, 267, 243, 220, 198, 177, 157, 138, 121, 104,
    89, 75, 62, 51, 40, 31, 23, 16, 10, 6,
    3, 1, 1, 1, 3, 6, 10, 16, 23, 31,
    40, 51, 62, 75, 89, 104, 121, 138, 157, 177,
    198, 220, 243, 267, 292, 319, 346, 374, 404, 434,
    466, 498, 531, 566, 601, 637, 673, 711, 750, 789,
    829, 870, 911, 953, 996, 1039, 1083, 1128, 1173, 1219,
    1265, 1312, 1359, 1406, 1454, 1502, 1551, 1600, 1649, 1698,
    1748, 1798, 1848, 1898, 1948, 1998
};

/**
 * @brief  Generowanie fali sinusoidalnej
 */
void DAC_GenerateSine(void)
{
    static uint8_t index = 0;
    
    // Wyślij wartość z tabeli
    DAC_SetValue(sine_wave[index]);
    
    // Następna próbka
    index++;
    if (index >= 256) index = 0;
}
```

### Fala prostokątna

```c
/**
 * @brief  Generowanie fali prostokątnej
 */
void DAC_GenerateSquare(uint16_t low_value, uint16_t high_value)
{
    static uint8_t state = 0;
    
    if (state) {
        DAC_SetValue(high_value);
    } else {
        DAC_SetValue(low_value);
    }
    
    state = !state;
}
```

## ⏱️ DAC z Timer Trigger

### DAC wyzwalany przez timer

```c
/**
 * @brief  Konfiguracja DAC z Timer trigger
 */
void DAC_TIM6_Trigger_Init(uint32_t frequency_hz)
{
    DAC_ChannelConfTypeDef sConfig = {0};
    TIM_HandleTypeDef htim6;
    
    // Konfiguracja Timer 6
    __HAL_RCC_TIM6_CLK_ENABLE();
    
    // Timer clock = 90 MHz
    uint32_t period = (90000000 / frequency_hz) - 1;
    
    htim6.Instance = TIM6;
    htim6.Init.Prescaler = 0;
    htim6.Init.Period = period;
    htim6.Init.CounterMode = TIM_COUNTERMODE_UP;
    
    HAL_TIM_Base_Init(&htim6);
    
    // Master mode - TRGO trigger dla DAC
    TIM_MasterConfigTypeDef sMasterConfig = {0};
    sMasterConfig.MasterOutputTrigger = TIM_TRGO_UPDATE;
    sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
    HAL_TIMEx_MasterConfigSynchronization(&htim6, &sMasterConfig);
    
    // Konfiguracja DAC
    __HAL_RCC_DAC_CLK_ENABLE();
    
    hdac.Instance = DAC;
    HAL_DAC_Init(&hdac);
    
    sConfig.DAC_Trigger = DAC_TRIGGER_T6_TRGO;  // Timer 6 TRGO
    sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
    
    HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1);
    
    // Start timer i DAC
    HAL_TIM_Base_Start(&htim6);
    HAL_DAC_Start(&hdac, DAC_CHANNEL_1);
}
```

## 🔄 DAC z DMA (fala sinusoidalna)

### Continuous sine wave przez DMA

```c
/**
 * @brief  DAC + DMA + Timer dla ciągłej fali sinusoidalnej
 */
DMA_HandleTypeDef hdma_dac1;

void DAC_DMA_Sine_Init(uint32_t frequency_hz)
{
    DAC_ChannelConfTypeDef sConfig = {0};
    TIM_HandleTypeDef htim6;
    
    // Częstotliwość próbkowania = frequency * 256 (256 próbek na okres)
    uint32_t sample_rate = frequency_hz * 256;
    
    // Konfiguracja DMA
    __HAL_RCC_DMA1_CLK_ENABLE();
    
    hdma_dac1.Instance = DMA1_Stream5;
    hdma_dac1.Init.Channel = DMA_CHANNEL_7;
    hdma_dac1.Init.Direction = DMA_MEMORY_TO_PERIPH;
    hdma_dac1.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_dac1.Init.MemInc = DMA_MINC_ENABLE;
    hdma_dac1.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
    hdma_dac1.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
    hdma_dac1.Init.Mode = DMA_CIRCULAR;  // Circular mode!
    hdma_dac1.Init.Priority = DMA_PRIORITY_HIGH;
    
    HAL_DMA_Init(&hdma_dac1);
    
    __HAL_LINKDMA(&hdac, DMA_Handle1, hdma_dac1);
    
    // Konfiguracja Timer 6
    __HAL_RCC_TIM6_CLK_ENABLE();
    
    uint32_t period = (90000000 / sample_rate) - 1;
    
    htim6.Instance = TIM6;
    htim6.Init.Prescaler = 0;
    htim6.Init.Period = period;
    htim6.Init.CounterMode = TIM_COUNTERMODE_UP;
    
    HAL_TIM_Base_Init(&htim6);
    
    TIM_MasterConfigTypeDef sMasterConfig = {0};
    sMasterConfig.MasterOutputTrigger = TIM_TRGO_UPDATE;
    HAL_TIMEx_MasterConfigSynchronization(&htim6, &sMasterConfig);
    
    // Konfiguracja DAC
    __HAL_RCC_DAC_CLK_ENABLE();
    
    hdac.Instance = DAC;
    HAL_DAC_Init(&hdac);
    
    sConfig.DAC_Trigger = DAC_TRIGGER_T6_TRGO;
    sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
    
    HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1);
    
    // Start DAC z DMA
    HAL_DAC_Start_DMA(&hdac, DAC_CHANNEL_1, 
                      (uint32_t*)sine_wave, 256, DAC_ALIGN_12B_R);
    
    // Start timer
    HAL_TIM_Base_Start(&htim6);
}

/**
 * @brief  Przykład: generuj sinusoidę 1 kHz
 */
void Generate_1kHz_Sine(void)
{
    DAC1_GPIO_Init();
    DAC_DMA_Sine_Init(1000);  // 1 kHz
}
```

## 🎼 Generowanie dźwięku

### Proste tony muzyczne

```c
/**
 * @brief  Odtwórz ton o określonej częstotliwości
 */
void DAC_PlayTone(uint32_t frequency_hz, uint32_t duration_ms)
{
    // Konfiguruj DAC z DMA dla danej częstotliwości
    DAC_DMA_Sine_Init(frequency_hz);
    
    // Graj przez określony czas
    HAL_Delay(duration_ms);
    
    // Stop
    HAL_DAC_Stop_DMA(&hdac, DAC_CHANNEL_1);
}

/**
 * @brief  Odtwórz melodię
 */
typedef struct {
    uint32_t frequency;
    uint32_t duration;
} Note_t;

void DAC_PlayMelody(const Note_t* melody, uint8_t num_notes)
{
    for (uint8_t i = 0; i < num_notes; i++) {
        if (melody[i].frequency > 0) {
            DAC_PlayTone(melody[i].frequency, melody[i].duration);
        } else {
            // Pauza
            HAL_Delay(melody[i].duration);
        }
        
        HAL_Delay(50);  // Krótka przerwa między nutami
    }
}

// Przykładowa melodia
const Note_t mario_melody[] = {
    {659, 150}, {659, 150}, {0, 150}, {659, 150},
    {0, 150}, {523, 150}, {659, 150}, {0, 150},
    {784, 150}
};

void Play_Mario(void)
{
    DAC_PlayMelody(mario_melody, sizeof(mario_melody) / sizeof(Note_t));
}
```

## 📈 DAC jako VREF dla ADC

### Generowanie napięcia referencyjnego

```c
/**
 * @brief  DAC jako programowalne VREF
 */
void DAC_SetReference_mV(uint16_t millivolts)
{
    // Max 3300 mV
    if (millivolts > 3300) millivolts = 3300;
    
    float voltage = millivolts / 1000.0f;
    DAC_SetVoltage(voltage);
}

/**
 * @brief  Przykład: ustaw 2.5V jako referencję
 */
void Set_2V5_Reference(void)
{
    DAC1_GPIO_Init();
    DAC1_Init();
    DAC_SetReference_mV(2500);  // 2.5V
}
```

## 🔊 Dual DAC Mode

### Synchroniczne wyjścia (dual DAC)

```c
/**
 * @brief  Konfiguracja dwóch kanałów DAC
 */
void DAC_Dual_Init(void)
{
    DAC_ChannelConfTypeDef sConfig = {0};
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_DAC_CLK_ENABLE();
    
    // GPIO dla obu kanałów
    GPIO_InitStruct.Pin = GPIO_PIN_4 | GPIO_PIN_5;  // PA4, PA5
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // DAC Init
    hdac.Instance = DAC;
    HAL_DAC_Init(&hdac);
    
    // Channel 1
    sConfig.DAC_Trigger = DAC_TRIGGER_NONE;
    sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
    HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1);
    
    // Channel 2
    HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_2);
    
    // Start obu kanałów
    HAL_DAC_Start(&hdac, DAC_CHANNEL_1);
    HAL_DAC_Start(&hdac, DAC_CHANNEL_2);
}

/**
 * @brief  Ustaw wartości dla obu kanałów
 */
void DAC_Dual_SetValues(uint16_t ch1_value, uint16_t ch2_value)
{
    HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, ch1_value);
    HAL_DAC_SetValue(&hdac, DAC_CHANNEL_2, DAC_ALIGN_12B_R, ch2_value);
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_adc|STM32F429I - ADC]]
- [[stm32f429i_dma|STM32F429I - DMA]]
- [[stm32f429i_timery|STM32F429I - Timery]]
- [[io_cyfrowe_analogowe|Wejścia/Wyjścia cyfrowe i analogowe]]

## 📝 Wzory i obliczenia

### Obliczanie wartości DAC
```
DAC_Value = (Voltage / VREF) × 4095
Voltage = (DAC_Value / 4095) × VREF

Dla VREF = 3.3V:
LSB = 3.3V / 4096 ≈ 0.806 mV

Przykłady:
1.65V → (1.65 / 3.3) × 4095 = 2047.5 ≈ 2048
2.5V  → (2.5 / 3.3) × 4095 = 3102
```

### Częstotliwość próbkowania dla przebiegów
```
Sine_Frequency = Sample_Rate / Number_of_Samples

Dla 256 próbek:
1 kHz sine → Sample_Rate = 1000 × 256 = 256 kSPS
```

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
