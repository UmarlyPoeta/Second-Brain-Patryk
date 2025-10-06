# STM32F429I - Bare Metal - UART Komunikacja Szeregowa

## 📡 USART/UART - Universal (Synchronous) Asynchronous Receiver Transmitter

### Różnica USART vs UART

```
UART - Asynchronous only
- TX, RX
- Nie ma clock line
- Dane synchronizowane przez start/stop bity

USART - Synchronous + Asynchronous  
- TX, RX, CK (clock)
- Może pracować synchronicznie (z clock)
- Może pracować asynchronicznie (jak UART)

STM32F429 ma:
- USART1, USART2, USART3, USART6 (pełny USART)
- UART4, UART5, UART7, UART8 (tylko async)
```

## 📋 Rejestry USART

### Adresy Bazowe

```c
/**
 * @brief  USART Base Addresses
 */
#define USART1_BASE  0x40011000UL  // APB2
#define USART2_BASE  0x40004400UL  // APB1
#define USART3_BASE  0x40004800UL  // APB1
#define UART4_BASE   0x40004C00UL  // APB1
#define UART5_BASE   0x40005000UL  // APB1
#define USART6_BASE  0x40011400UL  // APB2

/**
 * @brief  Struktura USART
 */
typedef struct {
    volatile uint32_t SR;    // 0x00: Status register
    volatile uint32_t DR;    // 0x04: Data register
    volatile uint32_t BRR;   // 0x08: Baud rate register
    volatile uint32_t CR1;   // 0x0C: Control register 1
    volatile uint32_t CR2;   // 0x10: Control register 2
    volatile uint32_t CR3;   // 0x14: Control register 3
    volatile uint32_t GTPR;  // 0x18: Guard time and prescaler register
} USART_TypeDef;

#define USART1  ((USART_TypeDef*)USART1_BASE)
#define USART2  ((USART_TypeDef*)USART2_BASE)
#define USART3  ((USART_TypeDef*)USART3_BASE)
```

### Rejestr SR - Status Register

```
USART_SR - Status Register
Offset: 0x00
Reset value: 0x00C00000

Bit 0:  PE    - Parity error
Bit 1:  FE    - Framing error
Bit 2:  NF    - Noise detected flag
Bit 3:  ORE   - Overrun error
Bit 4:  IDLE  - IDLE line detected
Bit 5:  RXNE  - Read data register not empty (data received)
Bit 6:  TC    - Transmission complete
Bit 7:  TXE   - Transmit data register empty (ready to send)
Bit 8:  LBD   - LIN break detection flag
Bit 9:  CTS   - CTS flag
```

### Rejestr DR - Data Register

```
USART_DR - Data Register
Offset: 0x04
Reset value: 0x00000000

Bits 8:0 - DR[8:0]: Data value
- Odczyt: Zwraca odebrany bajt
- Zapis: Wysyła bajt
```

### Rejestr BRR - Baud Rate Register

```
USART_BRR - Baud Rate Register  
Offset: 0x08
Reset value: 0x0000

Bits 15:4 - DIV_Mantissa[11:0]: Mantissa baud rate
Bits 3:0  - DIV_Fraction[3:0]:  Fraction baud rate

USARTDIV = f_CK / (8 × (2 - OVER8) × baud_rate)

Dla OVER8=0 (oversampling 16):
USARTDIV = f_CK / (16 × baud_rate)
```

### Rejestr CR1 - Control Register 1

```
USART_CR1 - Control Register 1
Offset: 0x0C
Reset value: 0x0000

Bit 0:  SBK   - Send break
Bit 1:  RWU   - Receiver wakeup
Bit 2:  RE    - Receiver enable
Bit 3:  TE    - Transmitter enable
Bit 4:  IDLEIE - IDLE interrupt enable
Bit 5:  RXNEIE - RXNE interrupt enable
Bit 6:  TCIE   - Transmission complete interrupt enable
Bit 7:  TXEIE  - TXE interrupt enable
Bit 8:  PEIE   - PE interrupt enable
Bit 9:  PS     - Parity selection (0=even, 1=odd)
Bit 10: PCE    - Parity control enable
Bit 11: WAKE   - Wakeup method
Bit 12: M      - Word length (0=8 bits, 1=9 bits)
Bit 13: UE     - USART enable
Bit 15: OVER8  - Oversampling mode (0=16, 1=8)
```

## ⚙️ Konfiguracja UART - Krok Po Kroku

### Obliczanie Baud Rate

```c
/**
 * @brief  Obliczanie BRR dla baud rate
 * 
 * Przykład: USART2 @ APB1 = 45 MHz, baud = 115200
 * 
 * KROK 1: Oblicz USARTDIV
 * USARTDIV = 45,000,000 / (16 × 115,200) = 24.4140625
 * 
 * KROK 2: Rozbij na mantissa i fraction
 * Mantissa = int(24.4140625) = 24 = 0x18
 * Fraction = frac(24.4140625) × 16 = 0.4140625 × 16 = 6.625 ≈ 7
 * 
 * KROK 3: Zbuduj BRR
 * BRR = (Mantissa << 4) | Fraction
 * BRR = (0x18 << 4) | 0x7 = 0x187
 */

uint32_t Calculate_BRR(uint32_t f_ck, uint32_t baud_rate)
{
    // USARTDIV = f_CK / (16 × baud_rate)
    // Multiply by 16 to keep precision
    uint32_t usartdiv_x16 = (f_ck * 16) / (16 * baud_rate);
    
    uint32_t mantissa = usartdiv_x16 / 16;
    uint32_t fraction = usartdiv_x16 % 16;
    
    return (mantissa << 4) | fraction;
}

/**
 * @brief  Przykłady BRR dla typowych baudów
 */
void BRR_Examples(void)
{
    // APB1 = 45 MHz
    uint32_t apb1_freq = 45000000;
    
    uint32_t brr_9600   = Calculate_BRR(apb1_freq, 9600);    // 0x1D4C
    uint32_t brr_115200 = Calculate_BRR(apb1_freq, 115200);  // 0x0187
    uint32_t brr_921600 = Calculate_BRR(apb1_freq, 921600);  // 0x0031
}
```

### Kompletna Inicjalizacja USART2

```c
/**
 * @brief  USART2 init - 115200 8N1 @ APB1 45MHz
 * 
 * Piny: PA2 = TX, PA3 = RX
 * Format: 8 data bits, No parity, 1 stop bit
 * 
 * KROK PO KROKU:
 */

void USART2_Init(void)
{
    // KROK 1: Włącz zegary
    RCC->AHB1ENR |= (1 << 0);   // GPIOA
    RCC->APB1ENR |= (1 << 17);  // USART2
    
    // KROK 2: Konfiguruj piny PA2 (TX), PA3 (RX)
    // PA2, PA3 = Alternate Function AF7
    
    // Tryb AF
    GPIOA->MODER &= ~((0x3 << 4) | (0x3 << 6));
    GPIOA->MODER |= ((0x2 << 4) | (0x2 << 6));
    
    // AF7 dla USART2
    GPIOA->AFR[0] &= ~((0xF << 8) | (0xF << 12));
    GPIOA->AFR[0] |= ((0x7 << 8) | (0x7 << 12));
    
    // Prędkość High
    GPIOA->OSPEEDR |= ((0x2 << 4) | (0x2 << 6));
    
    // Pull-up dla RX (opcjonalnie)
    GPIOA->PUPDR &= ~((0x3 << 4) | (0x3 << 6));
    GPIOA->PUPDR |= (0x1 << 6);  // PA3 pull-up
    
    // KROK 3: Wyłącz USART na czas konfiguracji
    USART2->CR1 &= ~(1 << 13);  // UE = 0
    
    // KROK 4: Ustaw baud rate (115200 @ 45 MHz)
    USART2->BRR = Calculate_BRR(45000000, 115200);
    
    // KROK 5: Ustaw format: 8N1
    // M = 0 (8 bits)
    // PCE = 0 (no parity)
    // CR2: STOP = 00 (1 stop bit)
    USART2->CR1 &= ~(1 << 12);  // M = 0 (8 bits)
    USART2->CR1 &= ~(1 << 10);  // PCE = 0 (no parity)
    USART2->CR2 &= ~(0x3 << 12); // STOP = 00 (1 stop bit)
    
    // KROK 6: Włącz TX i RX
    USART2->CR1 |= (1 << 3);    // TE = 1 (Transmitter enable)
    USART2->CR1 |= (1 << 2);    // RE = 1 (Receiver enable)
    
    // KROK 7: Włącz USART
    USART2->CR1 |= (1 << 13);   // UE = 1
}
```

## 📤 Wysyłanie Danych

### Transmisja Pojedynczego Bajtu

```c
/**
 * @brief  Wyślij jeden bajt - polling
 */
void USART2_SendByte(uint8_t data)
{
    // KROK 1: Czekaj aż TXE = 1 (transmit buffer empty)
    while (!(USART2->SR & (1 << 7)));
    
    // KROK 2: Zapisz dane do DR
    USART2->DR = data;
    
    // KROK 3: Opcjonalnie - czekaj na TC (transmission complete)
    // while (!(USART2->SR & (1 << 6)));
}

/**
 * @brief  Wyślij string
 */
void USART2_SendString(const char *str)
{
    while (*str) {
        USART2_SendByte(*str++);
    }
}

/**
 * @brief  Przykład użycia
 */
void Test_USART_TX(void)
{
    USART2_SendString("Hello STM32!\r\n");
    USART2_SendByte('A');
    USART2_SendByte('\n');
}
```

### Printf przez UART

```c
/**
 * @brief  Przekierowanie printf do UART
 * 
 * Implementacja _write() dla newlib
 */

#include <sys/stat.h>

int _write(int file, char *ptr, int len)
{
    int i;
    for (i = 0; i < len; i++) {
        USART2_SendByte(*ptr++);
    }
    return len;
}

/**
 * @brief  Teraz możesz używać printf!
 */
#include <stdio.h>

void Test_Printf(void)
{
    printf("Hello from STM32!\r\n");
    printf("Counter: %d\r\n", 42);
    printf("Hex: 0x%08X\r\n", 0xDEADBEEF);
}
```

## 📥 Odbieranie Danych

### Odbiór Pojedynczego Bajtu - Polling

```c
/**
 * @brief  Odbierz jeden bajt - polling
 */
uint8_t USART2_ReceiveByte(void)
{
    // KROK 1: Czekaj aż RXNE = 1 (data received)
    while (!(USART2->SR & (1 << 5)));
    
    // KROK 2: Odczytaj dane z DR
    return (uint8_t)(USART2->DR & 0xFF);
}

/**
 * @brief  Echo - odbierz i odeślij
 */
void USART_Echo_Test(void)
{
    while (1) {
        uint8_t received = USART2_ReceiveByte();
        USART2_SendByte(received);  // Echo back
    }
}
```

### Odbiór z Przerwaniem - Najlepszy Sposób

```c
/**
 * @brief  Circular buffer dla odbioru
 */
#define RX_BUFFER_SIZE  128

volatile uint8_t rx_buffer[RX_BUFFER_SIZE];
volatile uint16_t rx_write_pos = 0;
volatile uint16_t rx_read_pos = 0;

/**
 * @brief  Inicjalizacja USART2 z przerwaniem RX
 */
void USART2_Init_With_Interrupt(void)
{
    // Podstawowa inicjalizacja (jak poprzednio)
    USART2_Init();
    
    // KROK DODATKOWY: Włącz przerwanie RXNE
    USART2->CR1 |= (1 << 5);  // RXNEIE = 1
    
    // Włącz przerwanie w NVIC
    NVIC_SetPriority(USART2_IRQn, 3);
    NVIC_EnableIRQ(USART2_IRQn);
}

/**
 * @brief  USART2 Interrupt Handler
 */
void USART2_IRQHandler(void)
{
    // Sprawdź RXNE (data received)
    if (USART2->SR & (1 << 5)) {
        // Odczytaj dane (automatycznie czyści RXNE)
        uint8_t data = USART2->DR & 0xFF;
        
        // Zapisz do circular buffer
        rx_buffer[rx_write_pos] = data;
        rx_write_pos = (rx_write_pos + 1) % RX_BUFFER_SIZE;
        
        // Check overflow
        if (rx_write_pos == rx_read_pos) {
            // Buffer overflow! Starsza data zostanie nadpisana
        }
    }
    
    // Sprawdź inne flagi (ORE, FE, etc.)
    if (USART2->SR & (1 << 3)) {
        // Overrun error
        volatile uint32_t dummy = USART2->DR;  // Clear ORE
        (void)dummy;
    }
}

/**
 * @brief  Sprawdź czy są dane w buforze
 */
uint8_t USART2_Available(void)
{
    return (rx_write_pos != rx_read_pos);
}

/**
 * @brief  Odczytaj bajt z bufora
 */
uint8_t USART2_Read(void)
{
    if (!USART2_Available()) {
        return 0;  // Brak danych
    }
    
    uint8_t data = rx_buffer[rx_read_pos];
    rx_read_pos = (rx_read_pos + 1) % RX_BUFFER_SIZE;
    return data;
}

/**
 * @brief  Przykład - odbierz linię tekstu
 */
void Read_Line_Example(void)
{
    char line[100];
    uint8_t pos = 0;
    
    while (1) {
        if (USART2_Available()) {
            char c = USART2_Read();
            
            if (c == '\r' || c == '\n') {
                line[pos] = '\0';
                printf("Received: %s\r\n", line);
                pos = 0;
            } else if (pos < 99) {
                line[pos++] = c;
            }
        }
    }
}
```

## 🔄 Transmisja z Przerwaniem TXE

```c
/**
 * @brief  TX buffer
 */
#define TX_BUFFER_SIZE  128

volatile uint8_t tx_buffer[TX_BUFFER_SIZE];
volatile uint16_t tx_write_pos = 0;
volatile uint16_t tx_read_pos = 0;
volatile uint8_t tx_busy = 0;

/**
 * @brief  Inicjalizacja z TX interrupt
 */
void USART2_Init_TX_Interrupt(void)
{
    USART2_Init();
    
    // Przerwanie TXE będzie włączane tylko gdy są dane do wysłania
    USART2->CR1 &= ~(1 << 7);  // TXEIE = 0 (wyłączone na start)
    
    NVIC_SetPriority(USART2_IRQn, 3);
    NVIC_EnableIRQ(USART2_IRQn);
}

/**
 * @brief  Wyślij bajt (non-blocking!)
 */
void USART2_SendByte_IT(uint8_t data)
{
    // Zapisz do bufora
    tx_buffer[tx_write_pos] = data;
    tx_write_pos = (tx_write_pos + 1) % TX_BUFFER_SIZE;
    
    // Włącz przerwanie TXE
    USART2->CR1 |= (1 << 7);  // TXEIE = 1
}

/**
 * @brief  Handler z TX
 */
void USART2_IRQHandler_With_TX(void)
{
    // RX
    if (USART2->SR & (1 << 5)) {  // RXNE
        uint8_t data = USART2->DR;
        rx_buffer[rx_write_pos] = data;
        rx_write_pos = (rx_write_pos + 1) % RX_BUFFER_SIZE;
    }
    
    // TX
    if (USART2->SR & (1 << 7)) {  // TXE
        if (tx_read_pos != tx_write_pos) {
            // Są dane do wysłania
            USART2->DR = tx_buffer[tx_read_pos];
            tx_read_pos = (tx_read_pos + 1) % TX_BUFFER_SIZE;
        } else {
            // Brak danych - wyłącz przerwanie TXE
            USART2->CR1 &= ~(1 << 7);  // TXEIE = 0
        }
    }
}
```

## 🎯 Kompletny Przykład: Command Parser

```c
/**
 * @brief  Prosty parser komend
 * 
 * Komendy:
 * - "LED ON\r\n"  -> włącz LED
 * - "LED OFF\r\n" -> wyłącz LED
 * - "STATUS\r\n"  -> status LED
 */

#define CMD_BUFFER_SIZE  32

char cmd_buffer[CMD_BUFFER_SIZE];
uint8_t cmd_pos = 0;

void Process_Command(char *cmd)
{
    if (strcmp(cmd, "LED ON") == 0) {
        GPIOA->BSRR = (1 << 5);  // LED ON
        printf("LED turned ON\r\n");
    }
    else if (strcmp(cmd, "LED OFF") == 0) {
        GPIOA->BSRR = (1 << 21);  // LED OFF
        printf("LED turned OFF\r\n");
    }
    else if (strcmp(cmd, "STATUS") == 0) {
        uint8_t led_state = (GPIOA->ODR & (1 << 5)) ? 1 : 0;
        printf("LED is %s\r\n", led_state ? "ON" : "OFF");
    }
    else {
        printf("Unknown command: %s\r\n", cmd);
    }
}

void Command_Parser_Loop(void)
{
    while (1) {
        if (USART2_Available()) {
            char c = USART2_Read();
            
            // Echo
            USART2_SendByte(c);
            
            if (c == '\r' || c == '\n') {
                if (cmd_pos > 0) {
                    cmd_buffer[cmd_pos] = '\0';
                    Process_Command(cmd_buffer);
                    cmd_pos = 0;
                }
                printf("> ");  // Prompt
            }
            else if (cmd_pos < CMD_BUFFER_SIZE - 1) {
                cmd_buffer[cmd_pos++] = c;
            }
        }
    }
}
```

## 🐛 Obsługa Błędów

### Typy Błędów

```c
/**
 * @brief  Sprawdzanie i obsługa błędów
 */
void USART_Check_Errors(void)
{
    uint32_t sr = USART2->SR;
    
    // Parity Error
    if (sr & (1 << 0)) {
        // PE flag
        volatile uint32_t dummy = USART2->DR;  // Read DR to clear
        (void)dummy;
    }
    
    // Framing Error
    if (sr & (1 << 1)) {
        // FE - nieprawidłowy stop bit
        volatile uint32_t dummy = USART2->DR;
        (void)dummy;
    }
    
    // Noise Error
    if (sr & (1 << 2)) {
        // NF - szum na linii
        volatile uint32_t dummy = USART2->DR;
        (void)dummy;
    }
    
    // Overrun Error
    if (sr & (1 << 3)) {
        // ORE - nowe dane nadpisały nieodczytane
        volatile uint32_t dummy = USART2->DR;
        (void)dummy;
        // To się zdarza gdy nie czytasz danych wystarczająco szybko!
    }
}

/**
 * @brief  Handler z obsługą błędów
 */
void USART2_IRQHandler_With_ErrorHandling(void)
{
    uint32_t sr = USART2->SR;
    
    // Check errors first
    if (sr & 0x0F) {  // PE, FE, NF, ORE
        USART_Check_Errors();
        return;
    }
    
    // Normal RX
    if (sr & (1 << 5)) {
        uint8_t data = USART2->DR;
        // Process data...
    }
}
```

## 🔧 Konfiguracje Specjalne

### Różne Formaty Danych

```c
/**
 * @brief  9-bit data mode
 */
void USART_9bit_Config(void)
{
    USART2->CR1 |= (1 << 12);  // M = 1 (9 bits)
    
    // Transmit 9-bit
    uint16_t data_9bit = 0x1FF;  // 9 bits
    while (!(USART2->SR & (1 << 7)));
    USART2->DR = data_9bit;
    
    // Receive 9-bit
    while (!(USART2->SR & (1 << 5)));
    uint16_t received_9bit = USART2->DR & 0x1FF;
}

/**
 * @brief  Parity enable
 */
void USART_Parity_Config(void)
{
    USART2->CR1 |= (1 << 10);  // PCE = 1 (parity enable)
    USART2->CR1 |= (1 << 9);   // PS = 1 (odd parity)
    // lub
    USART2->CR1 &= ~(1 << 9);  // PS = 0 (even parity)
}

/**
 * @brief  2 stop bits
 */
void USART_2StopBits_Config(void)
{
    USART2->CR2 &= ~(0x3 << 12);
    USART2->CR2 |= (0x2 << 12);  // STOP = 10 (2 stop bits)
}

/**
 * @brief  Half-duplex mode (1 wire)
 */
void USART_HalfDuplex_Config(void)
{
    USART2->CR3 |= (1 << 3);  // HDSEL = 1
}
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_nvic|Bare Metal - NVIC i przerwania]]
- [[stm32f429i_bare_metal_gpio|Bare Metal - GPIO dla AF]]
- [[stm32f429i_bare_metal_dma_uart|Bare Metal - DMA z UART]]
- [[stm32f429i_uart|UART z HAL - porównanie]]

## 📝 Podsumowanie

### Kluczowe Rejestry USART
- **SR** - Status (TXE, RXNE, TC, błędy)
- **DR** - Data register (send/receive)
- **BRR** - Baud rate
- **CR1** - Control (UE, TE, RE, interrupts, format)
- **CR2** - Stop bits
- **CR3** - Hardware flow control, Half-duplex

### Kolejność Inicjalizacji
1. Włącz zegary (GPIO + USART)
2. Konfiguruj piny (AF mode)
3. Wyłącz USART (UE=0)
4. Ustaw baud rate (BRR)
5. Ustaw format (CR1, CR2)
6. Włącz TX/RX (TE, RE)
7. Opcjonalnie - włącz przerwania
8. Włącz USART (UE=1)

### Transmisja Polling
```c
while (!(USART->SR & (1<<7)));  // Wait TXE
USART->DR = data;
```

### Odbiór Interrupt (zalecany)
```c
void USARTx_IRQHandler(void) {
    if (USART->SR & (1<<5)) {  // RXNE
        uint8_t data = USART->DR;
        // Process...
    }
}
```

---

*Następna notatka: [[stm32f429i_bare_metal_timer|Bare Metal - Timery i PWM]]*
