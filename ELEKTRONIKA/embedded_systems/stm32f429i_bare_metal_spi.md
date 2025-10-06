# STM32F429I - Bare Metal - SPI Komunikacja

## 📡 SPI - Serial Peripheral Interface

### Czym Jest SPI?

```
SPI to synchroniczna, pełno-dupleksowa komunikacja szeregowa.

Linie sygnałowe:
- MOSI (Master Out Slave In) - dane z mastera do slave
- MISO (Master In Slave Out) - dane ze slave do mastera
- SCK  (Serial Clock)        - zegar generowany przez master
- NSS  (Slave Select)        - wybór slave (aktywny niski)

Cechy:
- Szybka (do 45 MHz na STM32F429)
- Pełny duplex (TX i RX jednocześnie)
- Master-Slave architektura
- Wiele trybów clock (CPOL, CPHA)
- 8 lub 16 bit transfer
```

### Topologia SPI

```
Single Slave:
┌────────┐                      ┌────────┐
│ Master │ ─MOSI─────────MOSI─> │ Slave  │
│        │ <─MISO─────────MISO─ │        │
│        │ ─SCK──────────── SCK> │        │
│        │ ─NSS──────────── NSS> │        │
└────────┘                      └────────┘

Multiple Slaves:
┌────────┐                      ┌────────┐
│        │ ─MOSI─────┬─────MOSI>│ Slave1 │
│ Master │ <─MISO────┼─────MISO<│        │
│        │ ─SCK──────┼──────SCK>│        │
│        │ ─NSS1─────┴──────NSS>└────────┘
│        │                      ┌────────┐
│        │ ──────────┬─────MOSI>│ Slave2 │
│        │           ├─────MISO<│        │
│        │           ├──────SCK>│        │
│        │ ─NSS2─────┴──────NSS>└────────┘
└────────┘
```

## 📋 Rejestry SPI

### Adresy Bazowe

```c
/**
 * @brief  SPI Base Addresses
 */
#define SPI1_BASE  0x40013000UL  // APB2 (max 45 MHz)
#define SPI2_BASE  0x40003800UL  // APB1 (max 22.5 MHz)
#define SPI3_BASE  0x40003C00UL  // APB1
#define SPI4_BASE  0x40013400UL  // APB2
#define SPI5_BASE  0x40015000UL  // APB2
#define SPI6_BASE  0x40015400UL  // APB2

/**
 * @brief  Struktura SPI
 */
typedef struct {
    volatile uint32_t CR1;      // 0x00: Control register 1
    volatile uint32_t CR2;      // 0x04: Control register 2
    volatile uint32_t SR;       // 0x08: Status register
    volatile uint32_t DR;       // 0x0C: Data register
    volatile uint32_t CRCPR;    // 0x10: CRC polynomial register
    volatile uint32_t RXCRCR;   // 0x14: RX CRC register
    volatile uint32_t TXCRCR;   // 0x18: TX CRC register
    volatile uint32_t I2SCFGR;  // 0x1C: I2S configuration register
    volatile uint32_t I2SPR;    // 0x20: I2S prescaler register
} SPI_TypeDef;

#define SPI1  ((SPI_TypeDef*)SPI1_BASE)
#define SPI2  ((SPI_TypeDef*)SPI2_BASE)
#define SPI3  ((SPI_TypeDef*)SPI3_BASE)
```

### Rejestr CR1 - Control Register 1

```
SPI_CR1 - Control Register 1
Offset: 0x00
Reset value: 0x0000

Bit 0:    CPHA    - Clock phase
Bit 1:    CPOL    - Clock polarity
Bit 2:    MSTR    - Master selection (1=Master, 0=Slave)
Bit 3:    BR[0]   - Baud rate control bits
Bit 4:    BR[1]
Bit 5:    BR[2]
Bit 6:    SPE     - SPI enable
Bit 7:    LSBFIRST- Frame format (0=MSB first, 1=LSB first)
Bit 8:    SSI     - Internal slave select
Bit 9:    SSM     - Software slave management
Bit 10:   RXONLY  - Receive only mode
Bit 11:   DFF     - Data frame format (0=8-bit, 1=16-bit)
Bit 12:   CRCNEXT - CRC transfer next
Bit 13:   CRCEN   - Hardware CRC enable
Bit 14:   BIDIOE  - Output enable in bidirectional mode
Bit 15:   BIDIMODE- Bidirectional data mode enable
```

### Rejestr CR2 - Control Register 2

```
SPI_CR2 - Control Register 2
Offset: 0x04
Reset value: 0x0000

Bit 0:    RXDMAEN  - RX buffer DMA enable
Bit 1:    TXDMAEN  - TX buffer DMA enable
Bit 2:    SSOE     - SS output enable
Bit 4:    FRF      - Frame format (0=SPI, 1=TI)
Bit 5:    ERRIE    - Error interrupt enable
Bit 6:    RXNEIE   - RX buffer not empty interrupt enable
Bit 7:    TXEIE    - TX buffer empty interrupt enable
```

### Rejestr SR - Status Register

```
SPI_SR - Status Register
Offset: 0x08
Reset value: 0x0002

Bit 0:    RXNE    - Receive buffer not empty
Bit 1:    TXE     - Transmit buffer empty
Bit 2:    CHSIDE  - Channel side (I2S)
Bit 3:    UDR     - Underrun flag (I2S)
Bit 4:    CRCERR  - CRC error flag
Bit 5:    MODF    - Mode fault
Bit 6:    OVR     - Overrun flag
Bit 7:    BSY     - Busy flag
Bit 8:    FRE     - Frame error (I2S)
```

### Rejestr DR - Data Register

```
SPI_DR - Data Register
Offset: 0x0C
Reset value: 0x0000

Bits 15:0 - DR[15:0]: Data register
- Zapis: dane do wysłania
- Odczyt: odebrane dane
```

## ⚙️ Tryby Clock - CPOL i CPHA

### Wyjaśnienie CPOL i CPHA

```
CPOL (Clock Polarity):
- CPOL = 0: Clock idle LOW  (domyślnie niski)
- CPOL = 1: Clock idle HIGH (domyślnie wysoki)

CPHA (Clock Phase):
- CPHA = 0: Próbkowanie na PIERWSZEJ krawędzi clock
- CPHA = 1: Próbkowanie na DRUGIEJ krawędzi clock

4 tryby SPI:
Mode 0: CPOL=0, CPHA=0 (najczęstszy)
Mode 1: CPOL=0, CPHA=1
Mode 2: CPOL=1, CPHA=0
Mode 3: CPOL=1, CPHA=1

Timing Mode 0 (CPOL=0, CPHA=0):
SCK  : _┌─┐_┌─┐_┌─┐_┌─┐_┌─┐_┌─┐_┌─┐_┌─┐_
MOSI : ──<D7>─<D6>─<D5>─<D4>─<D3>─<D2>─<D1>─<D0>─
MISO : ──<D7>─<D6>─<D5>─<D4>─<D3>─<D2>─<D1>─<D0>─
        ^ Sample points (rising edge)
```

### Konfiguracja Trybu Clock

```c
/**
 * @brief  Ustawienie trybu SPI (CPOL, CPHA)
 */
void SPI_SetClockMode(uint8_t mode)
{
    switch (mode) {
        case 0:  // CPOL=0, CPHA=0
            SPI1->CR1 &= ~(1 << 1);  // CPOL = 0
            SPI1->CR1 &= ~(1 << 0);  // CPHA = 0
            break;
        case 1:  // CPOL=0, CPHA=1
            SPI1->CR1 &= ~(1 << 1);  // CPOL = 0
            SPI1->CR1 |= (1 << 0);   // CPHA = 1
            break;
        case 2:  // CPOL=1, CPHA=0
            SPI1->CR1 |= (1 << 1);   // CPOL = 1
            SPI1->CR1 &= ~(1 << 0);  // CPHA = 0
            break;
        case 3:  // CPOL=1, CPHA=1
            SPI1->CR1 |= (1 << 1);   // CPOL = 1
            SPI1->CR1 |= (1 << 0);   // CPHA = 1
            break;
    }
}
```

## 🔧 Baud Rate - Obliczanie Prędkości

### Bity BR[2:0] - Prescaler

```
BR[2:0] określa prescaler dla clock:

000: fPCLK/2    (najmniejszy dzielnik, najszybszy)
001: fPCLK/4
010: fPCLK/8
011: fPCLK/16
100: fPCLK/32
101: fPCLK/64
110: fPCLK/128
111: fPCLK/256  (największy dzielnik, najwolniejszy)

SPI_Clock = APB_Clock / Prescaler

Przykład dla SPI1 @ APB2 90 MHz:
BR=000: 90 MHz / 2 = 45 MHz
BR=001: 90 MHz / 4 = 22.5 MHz
BR=010: 90 MHz / 8 = 11.25 MHz
BR=011: 90 MHz / 16 = 5.625 MHz
...
```

### Ustawienie Baud Rate

```c
/**
 * @brief  Oblicz BR bits dla żądanej częstotliwości
 */
uint8_t Calculate_SPI_BR(uint32_t apb_clock, uint32_t desired_freq)
{
    uint32_t prescalers[] = {2, 4, 8, 16, 32, 64, 128, 256};
    
    for (uint8_t br = 0; br < 8; br++) {
        uint32_t spi_freq = apb_clock / prescalers[br];
        if (spi_freq <= desired_freq) {
            return br;
        }
    }
    
    return 7;  // Najwolniejszy (fPCLK/256)
}

/**
 * @brief  Ustawienie baud rate
 */
void SPI_SetBaudRate(uint8_t br_bits)
{
    // br_bits: 0-7
    SPI1->CR1 &= ~(0x7 << 3);     // Wyczyść BR[2:0]
    SPI1->CR1 |= (br_bits << 3);  // Ustaw nowy BR
}

/**
 * @brief  Przykłady
 */
void SPI_BaudRate_Examples(void)
{
    // APB2 = 90 MHz, chcemy SPI @ 10 MHz
    uint8_t br = Calculate_SPI_BR(90000000, 10000000);
    // br = 3 (90MHz/16 = 5.625 MHz, najbliższe <= 10 MHz)
    
    SPI_SetBaudRate(br);
}
```

## 🎯 Konfiguracja SPI Master - Krok Po Kroku

### Kompletna Inicjalizacja SPI1

```c
/**
 * @brief  SPI1 Master Init
 * 
 * Piny: PA5 = SCK, PA6 = MISO, PA7 = MOSI
 * Mode: Mode 0 (CPOL=0, CPHA=0)
 * Baudrate: ~ 11.25 MHz @ APB2 90MHz
 * NSS: Software (GPIO kontrolowany ręcznie)
 * 
 * KROK PO KROKU:
 */

void SPI1_Master_Init(void)
{
    // KROK 1: Włącz zegary
    RCC->AHB1ENR |= (1 << 0);   // GPIOA
    RCC->APB2ENR |= (1 << 12);  // SPI1
    
    // KROK 2: Konfiguruj piny GPIO
    // PA5 = SCK  (AF5)
    // PA6 = MISO (AF5)
    // PA7 = MOSI (AF5)
    
    // Tryb Alternate Function
    GPIOA->MODER &= ~((0x3 << 10) | (0x3 << 12) | (0x3 << 14));
    GPIOA->MODER |= ((0x2 << 10) | (0x2 << 12) | (0x2 << 14));
    
    // AF5 dla SPI1
    GPIOA->AFR[0] &= ~((0xF << 20) | (0xF << 24) | (0xF << 28));
    GPIOA->AFR[0] |= ((0x5 << 20) | (0x5 << 24) | (0x5 << 28));
    
    // Prędkość Very High
    GPIOA->OSPEEDR |= ((0x3 << 10) | (0x3 << 12) | (0x3 << 14));
    
    // KROK 3: Wyłącz SPI na czas konfiguracji
    SPI1->CR1 &= ~(1 << 6);  // SPE = 0
    
    // KROK 4: Konfiguruj SPI jako Master
    SPI1->CR1 |= (1 << 2);   // MSTR = 1 (Master mode)
    
    // KROK 5: Ustaw clock mode (Mode 0)
    SPI1->CR1 &= ~(1 << 1);  // CPOL = 0
    SPI1->CR1 &= ~(1 << 0);  // CPHA = 0
    
    // KROK 6: Ustaw baud rate (fPCLK/8 = 90MHz/8 = 11.25 MHz)
    SPI1->CR1 &= ~(0x7 << 3);
    SPI1->CR1 |= (0x2 << 3);  // BR = 010 (/8)
    
    // KROK 7: Ustaw data frame (8-bit)
    SPI1->CR1 &= ~(1 << 11);  // DFF = 0 (8-bit)
    
    // KROK 8: Ustaw MSB first
    SPI1->CR1 &= ~(1 << 7);   // LSBFIRST = 0 (MSB first)
    
    // KROK 9: Software Slave Management
    SPI1->CR1 |= (1 << 9);    // SSM = 1
    SPI1->CR1 |= (1 << 8);    // SSI = 1
    
    // KROK 10: Full duplex mode
    SPI1->CR1 &= ~(1 << 10);  // RXONLY = 0
    SPI1->CR1 &= ~(1 << 15);  // BIDIMODE = 0
    
    // KROK 11: Włącz SPI
    SPI1->CR1 |= (1 << 6);    // SPE = 1
}

/**
 * @brief  NSS pin jako GPIO output
 */
void SPI_NSS_Init(void)
{
    // PA4 jako NSS (software controlled)
    GPIOA->MODER &= ~(0x3 << 8);
    GPIOA->MODER |= (0x1 << 8);    // Output
    
    GPIOA->OTYPER &= ~(1 << 4);    // Push-pull
    GPIOA->OSPEEDR |= (0x3 << 8);  // Very high
    
    // NSS idle HIGH (slave not selected)
    GPIOA->BSRR = (1 << 4);
}

#define NSS_LOW()   GPIOA->BSRR = (1 << 20)  // PA4 = 0
#define NSS_HIGH()  GPIOA->BSRR = (1 << 4)   // PA4 = 1
```

## 📤📥 Transmisja i Odbiór Danych

### Transmisja/Odbiór Pojedynczego Bajtu

```c
/**
 * @brief  Wyślij i odbierz bajt (full duplex)
 * 
 * W SPI, transmisja i odbiór zawsze występują jednocześnie!
 */
uint8_t SPI_TransmitReceive(uint8_t data)
{
    // KROK 1: Czekaj aż TXE = 1 (TX buffer empty)
    while (!(SPI1->SR & (1 << 1)));
    
    // KROK 2: Wyślij dane
    *(volatile uint8_t*)&SPI1->DR = data;
    
    // KROK 3: Czekaj aż RXNE = 1 (RX buffer not empty)
    while (!(SPI1->SR & (1 << 0)));
    
    // KROK 4: Odczytaj odebrane dane
    return *(volatile uint8_t*)&SPI1->DR;
}

/**
 * @brief  Wyślij bajt (ignoruj RX)
 */
void SPI_Transmit(uint8_t data)
{
    while (!(SPI1->SR & (1 << 1)));  // Wait TXE
    *(volatile uint8_t*)&SPI1->DR = data;
    
    while (!(SPI1->SR & (1 << 0)));  // Wait RXNE
    volatile uint8_t dummy = *(volatile uint8_t*)&SPI1->DR;  // Odczytaj aby wyczyścić
    (void)dummy;
}

/**
 * @brief  Odbierz bajt (wyślij dummy)
 */
uint8_t SPI_Receive(void)
{
    return SPI_TransmitReceive(0xFF);  // Wyślij dummy byte
}

/**
 * @brief  Czekaj aż SPI nie jest busy
 */
void SPI_WaitNotBusy(void)
{
    while (SPI1->SR & (1 << 7));  // Wait BSY = 0
}
```

### Transmisja Wielu Bajtów

```c
/**
 * @brief  Wyślij bufor danych
 */
void SPI_TransmitBuffer(uint8_t *data, uint16_t size)
{
    for (uint16_t i = 0; i < size; i++) {
        SPI_Transmit(data[i]);
    }
    SPI_WaitNotBusy();
}

/**
 * @brief  Odbierz bufor danych
 */
void SPI_ReceiveBuffer(uint8_t *buffer, uint16_t size)
{
    for (uint16_t i = 0; i < size; i++) {
        buffer[i] = SPI_Receive();
    }
}

/**
 * @brief  Full duplex transmit/receive
 */
void SPI_TransmitReceiveBuffer(uint8_t *tx_data, uint8_t *rx_data, uint16_t size)
{
    for (uint16_t i = 0; i < size; i++) {
        rx_data[i] = SPI_TransmitReceive(tx_data[i]);
    }
}
```

## 💾 Przykład: W25Q Flash Memory

### Komunikacja z pamięcią Flash

```c
/**
 * @brief  W25Q Flash Commands
 */
#define W25Q_CMD_WRITE_ENABLE    0x06
#define W25Q_CMD_WRITE_DISABLE   0x04
#define W25Q_CMD_READ_STATUS1    0x05
#define W25Q_CMD_READ_STATUS2    0x35
#define W25Q_CMD_READ_DATA       0x03
#define W25Q_CMD_PAGE_PROGRAM    0x02
#define W25Q_CMD_SECTOR_ERASE    0x20
#define W25Q_CMD_CHIP_ERASE      0xC7
#define W25Q_CMD_READ_ID         0x9F

/**
 * @brief  Odczyt ID pamięci Flash
 */
void W25Q_ReadID(uint8_t *manufacturer, uint8_t *memory_type, uint8_t *capacity)
{
    NSS_LOW();
    
    SPI_Transmit(W25Q_CMD_READ_ID);
    *manufacturer = SPI_Receive();
    *memory_type = SPI_Receive();
    *capacity = SPI_Receive();
    
    NSS_HIGH();
}

/**
 * @brief  Odczyt status register
 */
uint8_t W25Q_ReadStatus(void)
{
    NSS_LOW();
    
    SPI_Transmit(W25Q_CMD_READ_STATUS1);
    uint8_t status = SPI_Receive();
    
    NSS_HIGH();
    return status;
}

/**
 * @brief  Write Enable
 */
void W25Q_WriteEnable(void)
{
    NSS_LOW();
    SPI_Transmit(W25Q_CMD_WRITE_ENABLE);
    NSS_HIGH();
}

/**
 * @brief  Czekaj aż busy
 */
void W25Q_WaitBusy(void)
{
    uint8_t status;
    do {
        status = W25Q_ReadStatus();
    } while (status & 0x01);  // Bit 0 = BUSY
}

/**
 * @brief  Odczyt danych z pamięci
 */
void W25Q_ReadData(uint32_t address, uint8_t *buffer, uint16_t size)
{
    NSS_LOW();
    
    SPI_Transmit(W25Q_CMD_READ_DATA);
    SPI_Transmit((address >> 16) & 0xFF);  // A23-A16
    SPI_Transmit((address >> 8) & 0xFF);   // A15-A8
    SPI_Transmit(address & 0xFF);          // A7-A0
    
    SPI_ReceiveBuffer(buffer, size);
    
    NSS_HIGH();
}

/**
 * @brief  Zapis strony (max 256 bajtów)
 */
void W25Q_PageProgram(uint32_t address, uint8_t *data, uint16_t size)
{
    // Max 256 bajtów
    if (size > 256) size = 256;
    
    W25Q_WriteEnable();
    
    NSS_LOW();
    
    SPI_Transmit(W25Q_CMD_PAGE_PROGRAM);
    SPI_Transmit((address >> 16) & 0xFF);
    SPI_Transmit((address >> 8) & 0xFF);
    SPI_Transmit(address & 0xFF);
    
    SPI_TransmitBuffer(data, size);
    
    NSS_HIGH();
    
    W25Q_WaitBusy();
}

/**
 * @brief  Kasowanie sektora (4KB)
 */
void W25Q_SectorErase(uint32_t address)
{
    W25Q_WriteEnable();
    
    NSS_LOW();
    
    SPI_Transmit(W25Q_CMD_SECTOR_ERASE);
    SPI_Transmit((address >> 16) & 0xFF);
    SPI_Transmit((address >> 8) & 0xFF);
    SPI_Transmit(address & 0xFF);
    
    NSS_HIGH();
    
    W25Q_WaitBusy();
}

/**
 * @brief  Kompletny przykład użycia
 */
void W25Q_Example(void)
{
    uint8_t man, type, cap;
    
    // Inicjalizacja
    SPI1_Master_Init();
    SPI_NSS_Init();
    
    // Odczyt ID
    W25Q_ReadID(&man, &type, &cap);
    printf("Manufacturer: 0x%02X\r\n", man);
    printf("Memory Type: 0x%02X\r\n", type);
    printf("Capacity: 0x%02X\r\n", cap);
    
    // Kasowanie sektora 0
    W25Q_SectorErase(0x000000);
    
    // Zapis danych
    uint8_t write_data[] = "Hello STM32!";
    W25Q_PageProgram(0x000000, write_data, sizeof(write_data));
    
    // Odczyt danych
    uint8_t read_data[100];
    W25Q_ReadData(0x000000, read_data, sizeof(read_data));
    
    printf("Read: %s\r\n", read_data);
}
```

## 🔄 SPI z Przerwaniami

### Konfiguracja Przerwań

```c
/**
 * @brief  SPI1 init z przerwaniami
 */
volatile uint8_t *tx_buffer;
volatile uint8_t *rx_buffer;
volatile uint16_t tx_size, rx_size;
volatile uint16_t tx_count, rx_count;
volatile uint8_t spi_busy = 0;

void SPI1_Init_IT(void)
{
    SPI1_Master_Init();
    
    // Włącz przerwania
    SPI1->CR2 |= (1 << 7);  // TXEIE
    SPI1->CR2 |= (1 << 6);  // RXNEIE
    
    NVIC_SetPriority(SPI1_IRQn, 3);
    NVIC_EnableIRQ(SPI1_IRQn);
}

/**
 * @brief  Rozpocznij transfer (non-blocking)
 */
void SPI_TransferIT(uint8_t *tx, uint8_t *rx, uint16_t size)
{
    tx_buffer = tx;
    rx_buffer = rx;
    tx_size = size;
    rx_size = size;
    tx_count = 0;
    rx_count = 0;
    spi_busy = 1;
    
    // Przerwanie TXE wystartuje transfer
}

/**
 * @brief  SPI1 Interrupt Handler
 */
void SPI1_IRQHandler(void)
{
    // TX
    if ((SPI1->SR & (1 << 1)) && (SPI1->CR2 & (1 << 7))) {  // TXE && TXEIE
        if (tx_count < tx_size) {
            *(volatile uint8_t*)&SPI1->DR = tx_buffer[tx_count++];
        } else {
            SPI1->CR2 &= ~(1 << 7);  // Wyłącz TXEIE
        }
    }
    
    // RX
    if ((SPI1->SR & (1 << 0)) && (SPI1->CR2 & (1 << 6))) {  // RXNE && RXNEIE
        if (rx_count < rx_size) {
            rx_buffer[rx_count++] = *(volatile uint8_t*)&SPI1->DR;
            
            if (rx_count >= rx_size) {
                SPI1->CR2 &= ~(1 << 6);  // Wyłącz RXNEIE
                spi_busy = 0;
                // Transfer complete callback
            }
        }
    }
}
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_gpio|Bare Metal - GPIO dla AF]]
- [[stm32f429i_bare_metal_dma_spi|Bare Metal - DMA z SPI]]
- [[stm32f429i_bare_metal_nvic|Bare Metal - NVIC i przerwania]]
- [[stm32f429i_spi|SPI z HAL - porównanie]]

## 📝 Podsumowanie

### Kluczowe Rejestry SPI
- **CR1** - Control (MSTR, SPE, BR, CPOL, CPHA, DFF)
- **CR2** - Interrupts, DMA
- **SR** - Status (TXE, RXNE, BSY)
- **DR** - Data register (TX/RX)

### Tryby Clock
- **Mode 0**: CPOL=0, CPHA=0 (najczęstszy)
- **Mode 1**: CPOL=0, CPHA=1
- **Mode 2**: CPOL=1, CPHA=0
- **Mode 3**: CPOL=1, CPHA=1

### Baud Rate
```
SPI_Clock = APB_Clock / (2^(BR+1))
BR=0: /2, BR=1: /4, ..., BR=7: /256
```

### Kolejność Inicjalizacji Master
1. Włącz zegary (GPIO + SPI)
2. Konfiguruj piny (AF mode)
3. Wyłącz SPI (SPE=0)
4. Ustaw Master mode (MSTR=1)
5. Ustaw CPOL, CPHA
6. Ustaw baud rate (BR)
7. Ustaw data frame (DFF)
8. Ustaw SSM=1, SSI=1
9. Włącz SPI (SPE=1)

### Transfer Danych
```c
while (!(SPI->SR & (1<<1)));  // Wait TXE
SPI->DR = data;               // Send
while (!(SPI->SR & (1<<0)));  // Wait RXNE
data = SPI->DR;               // Receive
```

---

*Następna notatka: [[stm32f429i_bare_metal_i2c|Bare Metal - I2C Komunikacja]]*
