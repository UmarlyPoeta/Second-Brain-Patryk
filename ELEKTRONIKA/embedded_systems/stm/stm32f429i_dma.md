# STM32F429I - DMA i Transfer Danych

## 🚀 Direct Memory Access (DMA)

### Wprowadzenie
DMA (Direct Memory Access) umożliwia transfer danych między pamięcią a peryferyjnymi bez udziału CPU, znacząco zwiększając wydajność systemu i zmniejszając obciążenie procesora.

### DMA w STM32F429I

| Parametr | DMA1 | DMA2 |
|----------|------|------|
| Strumienie (Streams) | 8 (Stream 0-7) | 8 (Stream 0-7) |
| Kanały na stream | 8 (Channel 0-7) | 8 (Channel 0-7) |
| Magistrala | AHB1 | AHB1 |
| FIFO | 4 słowa (16 bajtów) | 4 słowa (16 bajtów) |
| Transfer sizes | Byte, Half-word, Word | Byte, Half-word, Word |

### Architektura DMA

```
┌─────────────────────────────────────────────┐
│              DMA Controller                 │
│                                             │
│  Stream 0 ──┐                               │
│  Stream 1 ──┤                               │
│  Stream 2 ──┤  Channel                      │
│  Stream 3 ──┼─ Selection ──▶ Arbitration ──▶ AHB
│  Stream 4 ──┤  (0-7)                        │
│  Stream 5 ──┤                               │
│  Stream 6 ──┤                               │
│  Stream 7 ──┘                               │
│                                             │
│  ┌──────────┐  ┌──────────┐                │
│  │  FIFO    │  │ Priority │                │
│  │  Buffer  │  │ Arbiter  │                │
│  └──────────┘  └──────────┘                │
└─────────────────────────────────────────────┘
```

## 🔧 Konfiguracja DMA

### Podstawowa konfiguracja Memory-to-Memory

```c
/**
 * @brief  Transfer danych pamięć-do-pamięci
 */
DMA_HandleTypeDef hdma_memtomem;

void DMA_MemToMem_Init(void)
{
    __HAL_RCC_DMA2_CLK_ENABLE();
    
    hdma_memtomem.Instance = DMA2_Stream0;
    hdma_memtomem.Init.Channel = DMA_CHANNEL_0;
    hdma_memtomem.Init.Direction = DMA_MEMORY_TO_MEMORY;
    hdma_memtomem.Init.PeriphInc = DMA_PINC_ENABLE;  // Source increment
    hdma_memtomem.Init.MemInc = DMA_MINC_ENABLE;     // Dest increment
    hdma_memtomem.Init.PeriphDataAlignment = DMA_PDATAALIGN_WORD;
    hdma_memtomem.Init.MemDataAlignment = DMA_MDATAALIGN_WORD;
    hdma_memtomem.Init.Mode = DMA_NORMAL;  // Single transfer
    hdma_memtomem.Init.Priority = DMA_PRIORITY_HIGH;
    hdma_memtomem.Init.FIFOMode = DMA_FIFOMODE_ENABLE;
    hdma_memtomem.Init.FIFOThreshold = DMA_FIFO_THRESHOLD_FULL;
    hdma_memtomem.Init.MemBurst = DMA_MBURST_SINGLE;
    hdma_memtomem.Init.PeriphBurst = DMA_PBURST_SINGLE;
    
    if (HAL_DMA_Init(&hdma_memtomem) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Wykonaj transfer danych
 */
void DMA_MemCopy(uint32_t *src, uint32_t *dest, uint32_t size)
{
    // Start transferu (blocking)
    HAL_DMA_Start(&hdma_memtomem, (uint32_t)src, (uint32_t)dest, size);
    
    // Czekaj na zakończenie
    HAL_DMA_PollForTransfer(&hdma_memtomem, HAL_DMA_FULL_TRANSFER, HAL_MAX_DELAY);
}

/**
 * @brief  Przykład użycia
 */
void DMA_MemCopy_Example(void)
{
    uint32_t source[100];
    uint32_t destination[100];
    
    // Wypełnij źródło danymi
    for (int i = 0; i < 100; i++) {
        source[i] = i;
    }
    
    // Kopiuj przez DMA
    DMA_MemToMem_Init();
    DMA_MemCopy(source, destination, 100);
    
    // Sprawdź wynik
    for (int i = 0; i < 100; i++) {
        if (destination[i] != source[i]) {
            printf("Error at index %d\r\n", i);
        }
    }
}
```

## 📡 DMA z UART

### UART RX z DMA (circular buffer)

```c
/**
 * @brief  UART receive z DMA w trybie circular
 */
#define RX_BUFFER_SIZE 256

uint8_t uart_rx_buffer[RX_BUFFER_SIZE];
DMA_HandleTypeDef hdma_usart1_rx;
UART_HandleTypeDef huart1;

void UART_DMA_Init(void)
{
    // Konfiguracja DMA dla UART1 RX
    __HAL_RCC_DMA2_CLK_ENABLE();
    
    hdma_usart1_rx.Instance = DMA2_Stream2;
    hdma_usart1_rx.Init.Channel = DMA_CHANNEL_4;
    hdma_usart1_rx.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_usart1_rx.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_usart1_rx.Init.MemInc = DMA_MINC_ENABLE;
    hdma_usart1_rx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
    hdma_usart1_rx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
    hdma_usart1_rx.Init.Mode = DMA_CIRCULAR;  // Circular mode!
    hdma_usart1_rx.Init.Priority = DMA_PRIORITY_HIGH;
    
    HAL_DMA_Init(&hdma_usart1_rx);
    
    __HAL_LINKDMA(&huart1, hdmarx, hdma_usart1_rx);
    
    // Konfiguracja UART (zakładamy że już zrobiona)
    // Start UART RX z DMA
    HAL_UART_Receive_DMA(&huart1, uart_rx_buffer, RX_BUFFER_SIZE);
}

/**
 * @brief  Odczyt danych z circular buffer
 */
uint16_t UART_DMA_GetDataLength(void)
{
    // Oblicz ile danych jest w buforze
    return RX_BUFFER_SIZE - __HAL_DMA_GET_COUNTER(&hdma_usart1_rx);
}

/**
 * @brief  Callback half transfer
 */
void HAL_UART_RxHalfCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1) {
        // Pierwsza połowa bufora pełna
        // Przetwórz dane z pierwszej połowy
        Process_Data(&uart_rx_buffer[0], RX_BUFFER_SIZE / 2);
    }
}

/**
 * @brief  Callback full transfer
 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1) {
        // Druga połowa bufora pełna
        // Przetwórz dane z drugiej połowy
        Process_Data(&uart_rx_buffer[RX_BUFFER_SIZE / 2], RX_BUFFER_SIZE / 2);
    }
}
```

### UART TX z DMA

```c
/**
 * @brief  Wysłanie danych przez UART z DMA
 */
void UART_DMA_Transmit(uint8_t *data, uint16_t size)
{
    HAL_UART_Transmit_DMA(&huart1, data, size);
}

/**
 * @brief  Callback zakończenia transmisji
 */
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1) {
        // Transmisja zakończona
        tx_complete_flag = 1;
    }
}
```

## 📊 DMA z ADC

### ADC + DMA (continuous sampling)

```c
/**
 * @brief  ADC z DMA w trybie ciągłym
 */
#define ADC_SAMPLES 1000

uint16_t adc_dma_buffer[ADC_SAMPLES];
DMA_HandleTypeDef hdma_adc1;
ADC_HandleTypeDef hadc1;

void ADC_DMA_Init(void)
{
    ADC_ChannelConfTypeDef sConfig = {0};
    
    // DMA Configuration
    __HAL_RCC_DMA2_CLK_ENABLE();
    
    hdma_adc1.Instance = DMA2_Stream0;
    hdma_adc1.Init.Channel = DMA_CHANNEL_0;
    hdma_adc1.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_adc1.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_adc1.Init.MemInc = DMA_MINC_ENABLE;
    hdma_adc1.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
    hdma_adc1.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
    hdma_adc1.Init.Mode = DMA_CIRCULAR;
    hdma_adc1.Init.Priority = DMA_PRIORITY_HIGH;
    
    HAL_DMA_Init(&hdma_adc1);
    
    __HAL_LINKDMA(&hadc1, DMA_Handle, hdma_adc1);
    
    // ADC Configuration
    __HAL_RCC_ADC1_CLK_ENABLE();
    
    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = DISABLE;
    hadc1.Init.ContinuousConvMode = ENABLE;  // Continuous!
    hadc1.Init.DMAContinuousRequests = ENABLE;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 1;
    
    HAL_ADC_Init(&hadc1);
    
    sConfig.Channel = ADC_CHANNEL_0;
    sConfig.Rank = 1;
    sConfig.SamplingTime = ADC_SAMPLETIME_84CYCLES;
    
    HAL_ADC_ConfigChannel(&hadc1, &sConfig);
    
    // Start ADC with DMA
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_dma_buffer, ADC_SAMPLES);
}

/**
 * @brief  Callback po zakończeniu konwersji
 */
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc)
{
    if (hadc->Instance == ADC1) {
        // Bufor pełny - przetwórz dane
        uint32_t sum = 0;
        for (int i = 0; i < ADC_SAMPLES; i++) {
            sum += adc_dma_buffer[i];
        }
        uint16_t average = sum / ADC_SAMPLES;
        
        printf("ADC Average: %u\r\n", average);
    }
}
```

## 🎵 DMA z DAC (waveform generation)

```c
/**
 * @brief  DAC z DMA dla generowania przebiegów
 */
extern const uint16_t sine_wave[256];  // Z poprzedniego przykładu
DMA_HandleTypeDef hdma_dac1;
DAC_HandleTypeDef hdac;

void DAC_DMA_Init(void)
{
    DAC_ChannelConfTypeDef sConfig = {0};
    
    // DMA Configuration
    __HAL_RCC_DMA1_CLK_ENABLE();
    
    hdma_dac1.Instance = DMA1_Stream5;
    hdma_dac1.Init.Channel = DMA_CHANNEL_7;
    hdma_dac1.Init.Direction = DMA_MEMORY_TO_PERIPH;
    hdma_dac1.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_dac1.Init.MemInc = DMA_MINC_ENABLE;
    hdma_dac1.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
    hdma_dac1.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
    hdma_dac1.Init.Mode = DMA_CIRCULAR;  // Continuous waveform
    hdma_dac1.Init.Priority = DMA_PRIORITY_HIGH;
    
    HAL_DMA_Init(&hdma_dac1);
    
    __HAL_LINKDMA(&hdac, DMA_Handle1, hdma_dac1);
    
    // DAC Configuration
    __HAL_RCC_DAC_CLK_ENABLE();
    
    hdac.Instance = DAC;
    HAL_DAC_Init(&hdac);
    
    sConfig.DAC_Trigger = DAC_TRIGGER_T6_TRGO;
    sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
    
    HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1);
    
    // Start DAC with DMA
    HAL_DAC_Start_DMA(&hdac, DAC_CHANNEL_1, 
                      (uint32_t*)sine_wave, 256, DAC_ALIGN_12B_R);
}
```

## 🔄 Double Buffering

### Ping-Pong buffer dla ciągłego przetwarzania

```c
/**
 * @brief  Double buffer dla UART RX
 */
#define BUFFER_SIZE 512

uint8_t rx_buffer_a[BUFFER_SIZE];
uint8_t rx_buffer_b[BUFFER_SIZE];
uint8_t *current_buffer = rx_buffer_a;
volatile uint8_t buffer_ready = 0;

void UART_DoubleBuffer_Init(void)
{
    // Konfiguracja DMA w trybie normal (nie circular)
    hdma_usart1_rx.Init.Mode = DMA_NORMAL;
    HAL_DMA_Init(&hdma_usart1_rx);
    
    // Start z pierwszym buforem
    HAL_UART_Receive_DMA(&huart1, rx_buffer_a, BUFFER_SIZE);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1) {
        buffer_ready = 1;
        
        // Przełącz buffer
        if (current_buffer == rx_buffer_a) {
            current_buffer = rx_buffer_b;
            HAL_UART_Receive_DMA(huart, rx_buffer_b, BUFFER_SIZE);
        } else {
            current_buffer = rx_buffer_a;
            HAL_UART_Receive_DMA(huart, rx_buffer_a, BUFFER_SIZE);
        }
    }
}

/**
 * @brief  Przetwarzanie w main loop
 */
void main_loop(void)
{
    while (1) {
        if (buffer_ready) {
            buffer_ready = 0;
            
            // Przetwórz wypełniony bufor (poprzedni)
            uint8_t *process_buffer = (current_buffer == rx_buffer_a) ? 
                                      rx_buffer_b : rx_buffer_a;
            
            Process_Data(process_buffer, BUFFER_SIZE);
        }
    }
}
```

## 🚦 Priorytety DMA

### Konfiguracja priorytetów

```c
/**
 * @brief  Przykład różnych priorytetów DMA
 */
void DMA_Priority_Example(void)
{
    // High priority dla krytycznych danych (ADC)
    hdma_adc1.Init.Priority = DMA_PRIORITY_VERY_HIGH;
    
    // Medium priority dla UART
    hdma_usart1_rx.Init.Priority = DMA_PRIORITY_MEDIUM;
    
    // Low priority dla memory-to-memory
    hdma_memtomem.Init.Priority = DMA_PRIORITY_LOW;
}
```

## 🎛️ FIFO Mode

### Konfiguracja FIFO

```c
/**
 * @brief  DMA z FIFO dla burst transfers
 */
void DMA_FIFO_Config(void)
{
    hdma_memtomem.Init.FIFOMode = DMA_FIFOMODE_ENABLE;
    hdma_memtomem.Init.FIFOThreshold = DMA_FIFO_THRESHOLD_FULL;
    hdma_memtomem.Init.MemBurst = DMA_MBURST_INC4;  // 4-beat burst
    hdma_memtomem.Init.PeriphBurst = DMA_PBURST_INC4;
    
    HAL_DMA_Init(&hdma_memtomem);
}
```

## 🔍 Mapowanie DMA Streams i Channels

### Tabela DMA1
| Peryferyjne | Stream | Channel |
|-------------|--------|---------|
| SPI3_RX | Stream 0 | Channel 0 |
| TIM4_CH1 | Stream 0 | Channel 2 |
| I2C1_RX | Stream 0 | Channel 1 |
| USART3_TX | Stream 3 | Channel 4 |
| SPI2_TX | Stream 4 | Channel 0 |
| DAC1 | Stream 5 | Channel 7 |
| TIM2_CH1 | Stream 5 | Channel 3 |

### Tabela DMA2
| Peryferyjne | Stream | Channel |
|-------------|--------|---------|
| ADC1 | Stream 0 | Channel 0 |
| SPI1_RX | Stream 0 | Channel 3 |
| USART1_RX | Stream 2 | Channel 4 |
| SDIO | Stream 3 | Channel 4 |
| SPI1_TX | Stream 3 | Channel 3 |
| USART1_TX | Stream 7 | Channel 4 |

## 🔗 Powiązane tematy

- [[stm32f429i_adc|STM32F429I - ADC]]
- [[stm32f429i_dac|STM32F429I - DAC]]
- [[stm32f429i_uart|STM32F429I - UART]]
- [[stm32f429i_spi|STM32F429I - SPI]]

## 📝 Best Practices

### Zalecenia
1. **Używaj DMA dla dużych transferów** (> 10 bajtów)
2. **Circular mode** dla ciągłego zbierania danych (ADC, UART RX)
3. **Normal mode** dla pojedynczych transferów
4. **Double buffering** dla przetwarzania w czasie rzeczywistym
5. **Cache coherency** - pamiętaj o DCacheClean/Invalidate
6. **Alignment** - dla optymalnej wydajności wyrównuj bufory do 32-bit

### Typowe błędy
1. Brak włączenia zegara DMA
2. Nieprawidłowy stream/channel dla peryferyjnego
3. Nie odznaczenie flag przerwań
4. Problemy z cache (DMA używa fizycznych adresów)
5. Bufory w nieprawidłowej lokalizacji pamięci

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
