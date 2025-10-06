# STM32F429I - UART i Komunikacja Szeregowa

## 📡 UART/USART

### Wprowadzenie
STM32F429I posiada 4x USART i 4x UART umożliwiające asynchroniczną komunikację szeregową. USART dodatkowo obsługuje tryb synchroniczny i smartcard.

### Dostępne interfejsy

| Interfejs | Magistrala | Max prędkość | Funkcje dodatkowe |
|-----------|-----------|--------------|-------------------|
| USART1 | APB2 | 11.25 Mbps | Synchronous, SmartCard, IrDA |
| USART2 | APB1 | 5.625 Mbps | Synchronous, SmartCard, IrDA |
| USART3 | APB1 | 5.625 Mbps | Synchronous, SmartCard, IrDA |
| UART4 | APB1 | 5.625 Mbps | Asynchronous only |
| UART5 | APB1 | 5.625 Mbps | Asynchronous only |
| USART6 | APB2 | 11.25 Mbps | Synchronous, SmartCard, IrDA |
| UART7 | APB1 | 5.625 Mbps | Asynchronous only |
| UART8 | APB1 | 5.625 Mbps | Asynchronous only |

### Piny USART1
- **TX**: PA9, PB6
- **RX**: PA10, PB7
- **CK**: PA8 (tylko USART - clock)
- **CTS**: PA11 (flow control)
- **RTS**: PA12 (flow control)

## 🔧 Podstawowa konfiguracja UART

### UART polling mode

```c
/**
 * @brief  Konfiguracja USART1: 115200 8N1
 */
UART_HandleTypeDef huart1;

void USART1_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    // Włącz zegary
    __HAL_RCC_USART1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // GPIO Configuration: PA9=TX, PA10=RX
    GPIO_InitStruct.Pin = GPIO_PIN_9 | GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART1;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // UART Configuration
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart1.Init.OverSampling = UART_OVERSAMPLING_16;
    
    if (HAL_UART_Init(&huart1) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Wysłanie danych (blocking)
 */
void UART_Transmit_String(const char *str)
{
    HAL_UART_Transmit(&huart1, (uint8_t*)str, strlen(str), HAL_MAX_DELAY);
}

/**
 * @brief  Odbiór danych (blocking)
 */
void UART_Receive_Data(uint8_t *buffer, uint16_t size)
{
    HAL_UART_Receive(&huart1, buffer, size, 1000);  // Timeout 1s
}
```

## 📨 Printf przez UART

### Przekierowanie printf do UART

```c
/**
 * @brief  Implementacja _write dla printf
 */
#ifdef __GNUC__
int _write(int file, char *ptr, int len)
{
    HAL_UART_Transmit(&huart1, (uint8_t*)ptr, len, HAL_MAX_DELAY);
    return len;
}
#endif

/**
 * @brief  Dla kompilatorów ARM/Keil
 */
#ifdef __CC_ARM
int fputc(int ch, FILE *f)
{
    HAL_UART_Transmit(&huart1, (uint8_t*)&ch, 1, HAL_MAX_DELAY);
    return ch;
}
#endif

/**
 * @brief  Użycie printf
 */
void UART_Printf_Example(void)
{
    printf("STM32F429I UART Test\r\n");
    printf("Temperature: %.2f°C\r\n", 25.67);
    printf("Counter: %d\r\n", 12345);
}
```

## 🔔 UART z przerwaniami

### Receive interrupt

```c
/**
 * @brief  UART RX z przerwaniem
 */
uint8_t rx_byte;
volatile uint8_t rx_complete = 0;

void USART1_Interrupt_Init(void)
{
    USART1_Init();
    
    // Włącz przerwanie UART
    HAL_NVIC_SetPriority(USART1_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(USART1_IRQn);
    
    // Start odbioru
    HAL_UART_Receive_IT(&huart1, &rx_byte, 1);
}

/**
 * @brief  Handler przerwania USART1
 */
void USART1_IRQHandler(void)
{
    HAL_UART_IRQHandler(&huart1);
}

/**
 * @brief  Callback odbioru
 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1) {
        rx_complete = 1;
        
        // Echo odebranego bajtu
        HAL_UART_Transmit(huart, &rx_byte, 1, 10);
        
        // Odbierz następny bajt
        HAL_UART_Receive_IT(huart, &rx_byte, 1);
    }
}
```

## 🔄 UART z DMA

### Konfiguracja TX i RX przez DMA

```c
/**
 * @brief  UART z DMA (TX i RX)
 */
#define UART_RX_BUFFER_SIZE 256

uint8_t uart_rx_buffer[UART_RX_BUFFER_SIZE];
uint8_t uart_tx_buffer[256];
DMA_HandleTypeDef hdma_usart1_tx;
DMA_HandleTypeDef hdma_usart1_rx;

void USART1_DMA_Init(void)
{
    __HAL_RCC_DMA2_CLK_ENABLE();
    
    // DMA TX (Stream 7, Channel 4)
    hdma_usart1_tx.Instance = DMA2_Stream7;
    hdma_usart1_tx.Init.Channel = DMA_CHANNEL_4;
    hdma_usart1_tx.Init.Direction = DMA_MEMORY_TO_PERIPH;
    hdma_usart1_tx.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_usart1_tx.Init.MemInc = DMA_MINC_ENABLE;
    hdma_usart1_tx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
    hdma_usart1_tx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
    hdma_usart1_tx.Init.Mode = DMA_NORMAL;
    hdma_usart1_tx.Init.Priority = DMA_PRIORITY_LOW;
    
    HAL_DMA_Init(&hdma_usart1_tx);
    __HAL_LINKDMA(&huart1, hdmatx, hdma_usart1_tx);
    
    // DMA RX (Stream 2, Channel 4)
    hdma_usart1_rx.Instance = DMA2_Stream2;
    hdma_usart1_rx.Init.Channel = DMA_CHANNEL_4;
    hdma_usart1_rx.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_usart1_rx.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_usart1_rx.Init.MemInc = DMA_MINC_ENABLE;
    hdma_usart1_rx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
    hdma_usart1_rx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
    hdma_usart1_rx.Init.Mode = DMA_CIRCULAR;  // Circular dla RX
    hdma_usart1_rx.Init.Priority = DMA_PRIORITY_HIGH;
    
    HAL_DMA_Init(&hdma_usart1_rx);
    __HAL_LINKDMA(&huart1, hdmarx, hdma_usart1_rx);
    
    // Interrupt priorities
    HAL_NVIC_SetPriority(DMA2_Stream7_IRQn, 6, 0);
    HAL_NVIC_EnableIRQ(DMA2_Stream7_IRQn);
    
    HAL_NVIC_SetPriority(DMA2_Stream2_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(DMA2_Stream2_IRQn);
    
    // UART Init
    USART1_Init();
    
    // Start RX DMA
    HAL_UART_Receive_DMA(&huart1, uart_rx_buffer, UART_RX_BUFFER_SIZE);
}

/**
 * @brief  DMA Interrupt handlers
 */
void DMA2_Stream7_IRQHandler(void)
{
    HAL_DMA_IRQHandler(&hdma_usart1_tx);
}

void DMA2_Stream2_IRQHandler(void)
{
    HAL_DMA_IRQHandler(&hdma_usart1_rx);
}

/**
 * @brief  Wysłanie przez DMA
 */
void UART_DMA_Transmit(const char *data, uint16_t size)
{
    HAL_UART_Transmit_DMA(&huart1, (uint8_t*)data, size);
}
```

## 📝 Ring Buffer dla UART RX

### Implementacja ring buffera

```c
/**
 * @brief  Ring buffer structure
 */
typedef struct {
    uint8_t *buffer;
    uint16_t size;
    uint16_t head;
    uint16_t tail;
} RingBuffer_t;

/**
 * @brief  Inicjalizacja ring buffera
 */
void RingBuffer_Init(RingBuffer_t *rb, uint8_t *buffer, uint16_t size)
{
    rb->buffer = buffer;
    rb->size = size;
    rb->head = 0;
    rb->tail = 0;
}

/**
 * @brief  Dostępne dane w buforze
 */
uint16_t RingBuffer_Available(RingBuffer_t *rb)
{
    if (rb->head >= rb->tail) {
        return rb->head - rb->tail;
    } else {
        return rb->size - rb->tail + rb->head;
    }
}

/**
 * @brief  Odczyt bajtu z bufora
 */
uint8_t RingBuffer_Read(RingBuffer_t *rb)
{
    uint8_t data = rb->buffer[rb->tail];
    rb->tail = (rb->tail + 1) % rb->size;
    return data;
}

/**
 * @brief  UART RX z ring bufferem
 */
RingBuffer_t uart_ring_buffer;
uint8_t uart_rb_storage[512];

void UART_RingBuffer_Init(void)
{
    RingBuffer_Init(&uart_ring_buffer, uart_rb_storage, 512);
    
    // Start UART RX z DMA
    HAL_UART_Receive_DMA(&huart1, uart_rb_storage, 512);
}

/**
 * @brief  Aktualizacja head w IDLE callback
 */
void UART_IDLE_Callback(void)
{
    // Oblicz aktualną pozycję DMA
    uint16_t dma_pos = 512 - __HAL_DMA_GET_COUNTER(&hdma_usart1_rx);
    uart_ring_buffer.head = dma_pos;
}
```

## 🔐 Protokoły komunikacyjne

### Prosty protokół pakietowy

```c
/**
 * @brief  Struktura pakietu
 */
typedef struct __attribute__((packed)) {
    uint8_t start;      // 0xAA
    uint8_t cmd;        // Komenda
    uint8_t length;     // Długość danych
    uint8_t data[64];   // Dane
    uint8_t checksum;   // XOR checksum
} Packet_t;

/**
 * @brief  Oblicz checksum
 */
uint8_t Calculate_Checksum(Packet_t *packet)
{
    uint8_t checksum = 0;
    uint8_t *ptr = (uint8_t*)packet;
    
    for (int i = 0; i < sizeof(Packet_t) - 1; i++) {
        checksum ^= ptr[i];
    }
    
    return checksum;
}

/**
 * @brief  Wyślij pakiet
 */
void UART_Send_Packet(uint8_t cmd, uint8_t *data, uint8_t length)
{
    Packet_t packet;
    
    packet.start = 0xAA;
    packet.cmd = cmd;
    packet.length = length;
    memcpy(packet.data, data, length);
    packet.checksum = Calculate_Checksum(&packet);
    
    HAL_UART_Transmit(&huart1, (uint8_t*)&packet, 
                     3 + length + 1, HAL_MAX_DELAY);
}

/**
 * @brief  Odbierz i zweryfikuj pakiet
 */
uint8_t UART_Receive_Packet(Packet_t *packet)
{
    // Odbierz pakiet
    HAL_UART_Receive(&huart1, (uint8_t*)packet, sizeof(Packet_t), 1000);
    
    // Sprawdź start byte
    if (packet->start != 0xAA) {
        return 0;  // Błędny pakiet
    }
    
    // Sprawdź checksum
    uint8_t calc_checksum = Calculate_Checksum(packet);
    if (calc_checksum != packet->checksum) {
        return 0;  // Błędny checksum
    }
    
    return 1;  // Pakiet OK
}
```

## 💬 AT Commands Handler

### Obsługa komend AT

```c
/**
 * @brief  AT Command parser
 */
#define CMD_BUFFER_SIZE 128

char cmd_buffer[CMD_BUFFER_SIZE];
uint8_t cmd_index = 0;

void UART_AT_Command_Handler(uint8_t byte)
{
    // Dodaj znak do bufora
    if (byte == '\r' || byte == '\n') {
        if (cmd_index > 0) {
            cmd_buffer[cmd_index] = '\0';
            
            // Przetwórz komendę
            if (strcmp(cmd_buffer, "AT") == 0) {
                UART_Transmit_String("OK\r\n");
            }
            else if (strncmp(cmd_buffer, "AT+VER", 6) == 0) {
                UART_Transmit_String("Version 1.0\r\n");
            }
            else if (strncmp(cmd_buffer, "AT+TEMP", 7) == 0) {
                float temp = Read_Temperature();
                printf("TEMP:%.2f\r\n", temp);
            }
            else {
                UART_Transmit_String("ERROR\r\n");
            }
            
            cmd_index = 0;
        }
    }
    else if (cmd_index < CMD_BUFFER_SIZE - 1) {
        cmd_buffer[cmd_index++] = byte;
    }
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_dma|STM32F429I - DMA]]
- [[stm32f429i_gpio|STM32F429I - GPIO]]
- [[stm32f429i_przerwania|STM32F429I - Przerwania]]
- [[protokoly_komunikacyjne|Protokoły komunikacyjne]]

## 📝 Wzory i obliczenia

### Baudrate calculation
```
Baudrate = f_CK / (8 × (2 - OVER8) × USARTDIV)

Dla OVER8=0 (oversampling 16):
USARTDIV = f_CK / (16 × Baudrate)

Przykład: 115200 baud @ 90 MHz (APB1)
USARTDIV = 90,000,000 / (16 × 115200) = 48.828

Błąd baudrate:
Error % = |(Actual - Desired) / Desired| × 100%
```

### Popularne baudrate
- 9600, 19200, 38400, 57600, 115200
- 230400, 460800, 921600, 1000000, 2000000

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
