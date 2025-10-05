# STM32F429I - ADC i Pomiary Analogowe

## 📊 Analog-to-Digital Converter (ADC)

### Charakterystyka ADC w STM32F429I

STM32F429I posiada 3 niezależne przetworniki ADC:

| Parametr | Wartość |
|----------|---------|
| Liczba ADC | 3 (ADC1, ADC2, ADC3) |
| Rozdzielczość | 12-bit (do 4096 poziomów) |
| Tryby rozdzielczości | 12, 10, 8, 6 bitów |
| Częstotliwość próbkowania | Do 2.4 MSPS |
| Kanały na ADC | Do 16 zewnętrznych + 3 wewnętrzne |
| Napięcie referencyjne | VREF+ (typowo 3.3V) |
| Zakres napięć | 0V - VREF+ |
| DMA | Wsparcie transferu przez DMA |

### Kanały ADC

**Zewnętrzne (GPIO)**:
- ADC1/2/3: IN0-IN15 (wspólne dla wszystkich ADC)

**Wewnętrzne**:
- **IN16**: Sensor temperatury (tylko ADC1)
- **IN17**: VREFINT - napięcie referencyjne wewnętrzne
- **IN18**: VBAT - napięcie baterii (przez dzielnik /2)

## 🔧 Konfiguracja ADC

### Podstawowa konfiguracja jednokana łowa

```c
/**
 * @brief  Konfiguracja ADC1 kanał 0 (PA0)
 */
ADC_HandleTypeDef hadc1;

void ADC1_Init(void)
{
    ADC_ChannelConfTypeDef sConfig = {0};
    
    __HAL_RCC_ADC1_CLK_ENABLE();
    
    // Konfiguracja ADC
    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;  // APB2/4
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = DISABLE;  // Single channel
    hadc1.Init.ContinuousConvMode = DISABLE;  // Single conversion
    hadc1.Init.DiscontinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 1;
    hadc1.Init.DMAContinuousRequests = DISABLE;
    hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
    
    if (HAL_ADC_Init(&hadc1) != HAL_OK) {
        Error_Handler();
    }
    
    // Konfiguracja kanału
    sConfig.Channel = ADC_CHANNEL_0;  // PA0
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_3CYCLES;
    
    if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Konfiguracja GPIO dla ADC
 */
void ADC1_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // PA0 jako analog
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}
```

### Odczyt pojedynczej wartości (Polling)

```c
/**
 * @brief  Odczyt wartości ADC (blocking)
 */
uint16_t ADC_Read(void)
{
    uint16_t adc_value = 0;
    
    // Start konwersji
    HAL_ADC_Start(&hadc1);
    
    // Czekaj na zakończenie (timeout 100ms)
    if (HAL_ADC_PollForConversion(&hadc1, 100) == HAL_OK) {
        adc_value = HAL_ADC_GetValue(&hadc1);
    }
    
    // Stop ADC
    HAL_ADC_Stop(&hadc1);
    
    return adc_value;
}

/**
 * @brief  Konwersja wartości ADC na napięcie
 */
float ADC_ToVoltage(uint16_t adc_value)
{
    // VREF = 3.3V, 12-bit ADC (0-4095)
    return (adc_value * 3.3f) / 4095.0f;
}

/**
 * @brief  Przykład użycia
 */
void ADC_Example(void)
{
    ADC1_GPIO_Init();
    ADC1_Init();
    
    while (1) {
        uint16_t raw = ADC_Read();
        float voltage = ADC_ToVoltage(raw);
        
        printf("ADC: %u, Voltage: %.3f V\r\n", raw, voltage);
        HAL_Delay(500);
    }
}
```

## 📡 ADC z przerwaniami

### Konfiguracja w trybie przerwań

```c
/**
 * @brief  ADC z przerwaniem
 */
volatile uint16_t adc_value = 0;
volatile uint8_t adc_conversion_done = 0;

void ADC1_Interrupt_Init(void)
{
    ADC1_Init();
    
    // Włącz przerwanie ADC
    HAL_NVIC_SetPriority(ADC_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(ADC_IRQn);
}

/**
 * @brief  Start konwersji z przerwaniem
 */
void ADC_Start_IT(void)
{
    adc_conversion_done = 0;
    HAL_ADC_Start_IT(&hadc1);
}

/**
 * @brief  Handler przerwania ADC
 */
void ADC_IRQHandler(void)
{
    HAL_ADC_IRQHandler(&hadc1);
}

/**
 * @brief  Callback po zakończeniu konwersji
 */
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{
    if (hadc->Instance == ADC1) {
        adc_value = HAL_ADC_GetValue(hadc);
        adc_conversion_done = 1;
    }
}

/**
 * @brief  Użycie w main
 */
void main_loop(void)
{
    while (1) {
        ADC_Start_IT();
        
        // Czekaj na zakończenie
        while (!adc_conversion_done);
        
        float voltage = ADC_ToVoltage(adc_value);
        printf("Voltage: %.3f V\r\n", voltage);
        
        HAL_Delay(500);
    }
}
```

## 🔄 Continuous Mode z DMA

### Konfiguracja ADC + DMA

```c
/**
 * @brief  ADC w trybie ciągłym z DMA
 */
#define ADC_BUFFER_SIZE 100

uint16_t adc_buffer[ADC_BUFFER_SIZE];
DMA_HandleTypeDef hdma_adc1;

void ADC1_DMA_Init(void)
{
    ADC_ChannelConfTypeDef sConfig = {0};
    
    __HAL_RCC_ADC1_CLK_ENABLE();
    __HAL_RCC_DMA2_CLK_ENABLE();
    
    // Konfiguracja DMA
    hdma_adc1.Instance = DMA2_Stream0;
    hdma_adc1.Init.Channel = DMA_CHANNEL_0;
    hdma_adc1.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_adc1.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_adc1.Init.MemInc = DMA_MINC_ENABLE;
    hdma_adc1.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;  // 16-bit
    hdma_adc1.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
    hdma_adc1.Init.Mode = DMA_CIRCULAR;
    hdma_adc1.Init.Priority = DMA_PRIORITY_HIGH;
    
    HAL_DMA_Init(&hdma_adc1);
    
    __HAL_LINKDMA(&hadc1, DMA_Handle, hdma_adc1);
    
    // Konfiguracja ADC
    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = DISABLE;
    hadc1.Init.ContinuousConvMode = ENABLE;  // Tryb ciągły!
    hadc1.Init.DMAContinuousRequests = ENABLE;  // Ciągłe żądania DMA
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 1;
    hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
    
    HAL_ADC_Init(&hadc1);
    
    // Konfiguracja kanału
    sConfig.Channel = ADC_CHANNEL_0;
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_480CYCLES;  // Wolniejsze próbkowanie
    
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // Start ADC z DMA
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buffer, ADC_BUFFER_SIZE);
}

/**
 * @brief  Callback po zakończeniu transferu DMA
 */
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{
    // Bufor pełny - można przetwarzać dane
    if (hadc->Instance == ADC1) {
        // Oblicz średnią
        uint32_t sum = 0;
        for (int i = 0; i < ADC_BUFFER_SIZE; i++) {
            sum += adc_buffer[i];
        }
        uint16_t average = sum / ADC_BUFFER_SIZE;
        
        printf("Average ADC: %u\r\n", average);
    }
}
```

## 📈 Multi-channel ADC (Scan Mode)

### Odczyt wielu kanałów

```c
/**
 * @brief  ADC z wieloma kanałami (scan mode)
 */
#define NUM_CHANNELS 4

uint16_t adc_values[NUM_CHANNELS];

void ADC1_MultiChannel_Init(void)
{
    ADC_ChannelConfTypeDef sConfig = {0};
    
    __HAL_RCC_ADC1_CLK_ENABLE();
    
    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = ENABLE;  // Scan mode!
    hadc1.Init.ContinuousConvMode = ENABLE;
    hadc1.Init.DMAContinuousRequests = ENABLE;
    hadc1.Init.NbrOfConversion = NUM_CHANNELS;  // 4 kanały
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    
    HAL_ADC_Init(&hadc1);
    
    // Kanał 0 (PA0)
    sConfig.Channel = ADC_CHANNEL_0;
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_84CYCLES;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // Kanał 1 (PA1)
    sConfig.Channel = ADC_CHANNEL_1;
    sConfig.Rank = 2;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // Kanał 2 (PA2)
    sConfig.Channel = ADC_CHANNEL_2;
    sConfig.Rank = 3;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // Kanał 3 (PA3)
    sConfig.Channel = ADC_CHANNEL_3;
    sConfig.Rank = 4;
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // Start z DMA
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_values, NUM_CHANNELS);
}

/**
 * @brief  Odczyt wartości z poszczególnych kanałów
 */
void Read_MultiChannel_Values(void)
{
    printf("CH0: %u, CH1: %u, CH2: %u, CH3: %u\r\n",
           adc_values[0], adc_values[1], adc_values[2], adc_values[3]);
}
```

## 🌡️ Wewnętrzny sensor temperatury

### Pomiar temperatury MCU

```c
/**
 * @brief  Konfiguracja ADC dla sensora temperatury
 */
void ADC_TempSensor_Init(void)
{
    ADC_ChannelConfTypeDef sConfig = {0};
    
    __HAL_RCC_ADC1_CLK_ENABLE();
    
    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = DISABLE;
    hadc1.Init.ContinuousConvMode = DISABLE;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 1;
    
    HAL_ADC_Init(&hadc1);
    
    // Włącz sensor temperatury
    sConfig.Channel = ADC_CHANNEL_TEMPSENSOR;
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_480CYCLES;  // Długi czas dla temperatury
    
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
}

/**
 * @brief  Odczyt temperatury w °C
 * @note   Wzór z datasheetu STM32F429
 */
float ADC_ReadTemperature(void)
{
    uint16_t adc_value;
    float voltage;
    float temperature;
    
    // Odczyt ADC
    HAL_ADC_Start(&hadc1);
    HAL_ADC_PollForConversion(&hadc1, 100);
    adc_value = HAL_ADC_GetValue(&hadc1);
    HAL_ADC_Stop(&hadc1);
    
    // Konwersja na napięcie
    voltage = (adc_value * 3.3f) / 4095.0f;
    
    // Wzór z dokumentacji (typowy)
    // V25 = 0.76V (napięcie przy 25°C)
    // Avg_Slope = 2.5 mV/°C
    temperature = ((voltage - 0.76f) / 0.0025f) + 25.0f;
    
    return temperature;
}
```

## 🔋 Pomiar napięcia baterii (VBAT)

```c
/**
 * @brief  Pomiar VBAT
 */
float ADC_ReadVBAT(void)
{
    ADC_ChannelConfTypeDef sConfig = {0};
    uint16_t adc_value;
    
    // Konfiguracja kanału VBAT
    sConfig.Channel = ADC_CHANNEL_VBAT;
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_480CYCLES;
    
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // Odczyt
    HAL_ADC_Start(&hadc1);
    HAL_ADC_PollForConversion(&hadc1, 100);
    adc_value = HAL_ADC_GetValue(&hadc1);
    HAL_ADC_Stop(&hadc1);
    
    // VBAT jest dzielone przez 2 przed ADC
    float voltage = ((adc_value * 3.3f) / 4095.0f) * 2.0f;
    
    return voltage;
}
```

## 📐 Kalibracja i filtrowanie

### Software oversampling

```c
/**
 * @brief  Oversampling dla zwiększenia rozdzielczości
 */
uint16_t ADC_Oversample(uint8_t num_samples)
{
    uint32_t sum = 0;
    
    for (uint8_t i = 0; i < num_samples; i++) {
        sum += ADC_Read();
    }
    
    return (uint16_t)(sum / num_samples);
}
```

### Filtr dolnoprzepustowy (moving average)

```c
/**
 * @brief  Filtr uśredniający
 */
#define FILTER_SIZE 10

uint16_t ADC_MovingAverage(uint16_t new_value)
{
    static uint16_t buffer[FILTER_SIZE] = {0};
    static uint8_t index = 0;
    static uint32_t sum = 0;
    
    // Usuń starą wartość z sumy
    sum -= buffer[index];
    
    // Dodaj nową wartość
    buffer[index] = new_value;
    sum += new_value;
    
    // Następny index (circular buffer)
    index = (index + 1) % FILTER_SIZE;
    
    return (uint16_t)(sum / FILTER_SIZE);
}
```

### Exponential Moving Average (EMA)

```c
/**
 * @brief  Filtr EMA
 */
float ADC_EMA_Filter(float new_value, float alpha)
{
    static float filtered_value = 0;
    static uint8_t first_run = 1;
    
    if (first_run) {
        filtered_value = new_value;
        first_run = 0;
    } else {
        // y[n] = α * x[n] + (1 - α) * y[n-1]
        filtered_value = alpha * new_value + (1.0f - alpha) * filtered_value;
    }
    
    return filtered_value;
}

// Użycie: alpha = 0.1 dla wolnego filtra, 0.9 dla szybkiego
float filtered = ADC_EMA_Filter(ADC_ToVoltage(raw_value), 0.2f);
```

## 🔗 Powiązane tematy

- [[stm32f429i_dma|STM32F429I - DMA]]
- [[stm32f429i_dac|STM32F429I - DAC]]
- [[stm32f429i_gpio|STM32F429I - GPIO]]
- [[io_cyfrowe_analogowe|Wejścia/Wyjścia cyfrowe i analogowe]]

## 📝 Wzory i obliczenia

### Częstotliwość próbkowania
```
ADC_Clock = APB2_Clock / Prescaler
Conversion_Time = Sampling_Time + 12_cycles
Sample_Rate = ADC_Clock / Conversion_Time

Przykład:
APB2 = 90 MHz, Prescaler = 4
ADC_Clock = 22.5 MHz
Sampling_Time = 3 cycles
Conversion_Time = 3 + 12 = 15 cycles
Max_Sample_Rate = 22.5MHz / 15 = 1.5 MSPS
```

### Rozdzielczość
```
12-bit: 4096 poziomów (0-4095)
10-bit: 1024 poziomy (0-1023)
8-bit:  256 poziomów (0-255)
6-bit:  64 poziomy (0-63)

LSB (12-bit, 3.3V) = 3.3V / 4096 ≈ 0.806 mV
```

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
