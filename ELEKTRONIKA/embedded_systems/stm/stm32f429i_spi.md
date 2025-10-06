# STM32F429I - SPI i Komunikacja Synchroniczna

## 🔄 Serial Peripheral Interface (SPI)

### Wprowadzenie
SPI to synchroniczny, full-duplex interfejs komunikacyjny typu master-slave. STM32F429I posiada 6 interfejsów SPI.

### Dostępne interfejsy SPI

| Interface | Magistrala | Max prędkość | NSS | Piny (domyślne) |
|-----------|-----------|--------------|-----|-----------------|
| SPI1 | APB2 | 45 Mbps | Hardware/Software | PA5-7, PA4 |
| SPI2 | APB1 | 22.5 Mbps | Hardware/Software | PB13-15, PB12 |
| SPI3 | APB1 | 22.5 Mbps | Hardware/Software | PC10-12, PA15 |
| SPI4 | APB2 | 45 Mbps | Hardware/Software | PE2, PE5-6, PE4 |
| SPI5 | APB2 | 45 Mbps | Hardware/Software | PF7-9, PF6 |
| SPI6 | APB2 | 45 Mbps | Hardware/Software | PG12-14, PG8 |

### Architektura SPI

```
       Master                          Slave
┌───────────────────┐          ┌───────────────────┐
│                   │          │                   │
│  MOSI  ├─────────┼──────────┤  MOSI             │
│  MISO  ├─────────┼──────────┤  MISO             │
│  SCK   ├─────────┼──────────┤  SCK              │
│  NSS   ├─────────┼──────────┤  NSS              │
│                   │          │                   │
└───────────────────┘          └───────────────────┘
```

## 🔧 Konfiguracja SPI Master

### Podstawowa konfiguracja

```c
/**
 * @brief  Konfiguracja SPI1 jako Master
 */
SPI_HandleTypeDef hspi1;

void SPI1_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    // Włącz zegary
    __HAL_RCC_SPI1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // GPIO Configuration
    // PA5 - SCK, PA6 - MISO, PA7 - MOSI
    GPIO_InitStruct.Pin = GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF5_SPI1;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // PA4 - NSS (software controlled)
    GPIO_InitStruct.Pin = GPIO_PIN_4;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // Deselect slave
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_4, GPIO_PIN_SET);
    
    // SPI Configuration
    hspi1.Instance = SPI1;
    hspi1.Init.Mode = SPI_MODE_MASTER;
    hspi1.Init.Direction = SPI_DIRECTION_2LINES;  // Full duplex
    hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
    hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;    // CPOL = 0
    hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;        // CPHA = 0
    hspi1.Init.NSS = SPI_NSS_SOFT;                // Software NSS
    hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_16;  // 90MHz/16 = 5.625MHz
    hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
    hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
    hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
    
    if (HAL_SPI_Init(&hspi1) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Makra CS (Chip Select)
 */
#define SPI1_CS_LOW()   HAL_GPIO_WritePin(GPIOA, GPIO_PIN_4, GPIO_PIN_RESET)
#define SPI1_CS_HIGH()  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_4, GPIO_PIN_SET)
```

## 📤 Transmisja i odbiór danych

### Polling mode

```c
/**
 * @brief  Wysłanie pojedynczego bajtu
 */
uint8_t SPI_TransmitReceive(uint8_t data)
{
    uint8_t received;
    
    HAL_SPI_TransmitReceive(&hspi1, &data, &received, 1, HAL_MAX_DELAY);
    
    return received;
}

/**
 * @brief  Wysłanie wielobajtowe
 */
void SPI_Transmit(uint8_t *data, uint16_t size)
{
    SPI1_CS_LOW();
    HAL_SPI_Transmit(&hspi1, data, size, HAL_MAX_DELAY);
    SPI1_CS_HIGH();
}

/**
 * @brief  Odbiór wielobajtowy
 */
void SPI_Receive(uint8_t *data, uint16_t size)
{
    SPI1_CS_LOW();
    HAL_SPI_Receive(&hspi1, data, size, HAL_MAX_DELAY);
    SPI1_CS_HIGH();
}

/**
 * @brief  Full-duplex transfer
 */
void SPI_TransferData(uint8_t *tx_data, uint8_t *rx_data, uint16_t size)
{
    SPI1_CS_LOW();
    HAL_SPI_TransmitReceive(&hspi1, tx_data, rx_data, size, HAL_MAX_DELAY);
    SPI1_CS_HIGH();
}
```

### DMA mode

```c
/**
 * @brief  SPI z DMA
 */
DMA_HandleTypeDef hdma_spi1_tx;
DMA_HandleTypeDef hdma_spi1_rx;

void SPI1_DMA_Init(void)
{
    __HAL_RCC_DMA2_CLK_ENABLE();
    
    // DMA TX (Stream 3, Channel 3)
    hdma_spi1_tx.Instance = DMA2_Stream3;
    hdma_spi1_tx.Init.Channel = DMA_CHANNEL_3;
    hdma_spi1_tx.Init.Direction = DMA_MEMORY_TO_PERIPH;
    hdma_spi1_tx.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_spi1_tx.Init.MemInc = DMA_MINC_ENABLE;
    hdma_spi1_tx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
    hdma_spi1_tx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
    hdma_spi1_tx.Init.Mode = DMA_NORMAL;
    hdma_spi1_tx.Init.Priority = DMA_PRIORITY_HIGH;
    
    HAL_DMA_Init(&hdma_spi1_tx);
    __HAL_LINKDMA(&hspi1, hdmatx, hdma_spi1_tx);
    
    // DMA RX (Stream 0, Channel 3)
    hdma_spi1_rx.Instance = DMA2_Stream0;
    hdma_spi1_rx.Init.Channel = DMA_CHANNEL_3;
    hdma_spi1_rx.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_spi1_rx.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_spi1_rx.Init.MemInc = DMA_MINC_ENABLE;
    hdma_spi1_rx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
    hdma_spi1_rx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
    hdma_spi1_rx.Init.Mode = DMA_NORMAL;
    hdma_spi1_rx.Init.Priority = DMA_PRIORITY_HIGH;
    
    HAL_DMA_Init(&hdma_spi1_rx);
    __HAL_LINKDMA(&hspi1, hdmarx, hdma_spi1_rx);
    
    // DMA interrupts
    HAL_NVIC_SetPriority(DMA2_Stream3_IRQn, 6, 0);
    HAL_NVIC_EnableIRQ(DMA2_Stream3_IRQn);
    
    HAL_NVIC_SetPriority(DMA2_Stream0_IRQn, 6, 0);
    HAL_NVIC_EnableIRQ(DMA2_Stream0_IRQn);
    
    SPI1_Init();
}

/**
 * @brief  Transfer z DMA
 */
void SPI_DMA_TransferData(uint8_t *tx_data, uint8_t *rx_data, uint16_t size)
{
    SPI1_CS_LOW();
    HAL_SPI_TransmitReceive_DMA(&hspi1, tx_data, rx_data, size);
}

/**
 * @brief  Callback zakończenia transferu
 */
void HAL_SPI_TxRxCpltCallback(SPI_HandleTypeDef *hspi)
{
    if (hspi->Instance == SPI1) {
        SPI1_CS_HIGH();
        // Transfer complete
    }
}
```

## 💾 Komunikacja z pamięcią Flash (W25Q)

### Obsługa W25Qxx Flash

```c
/**
 * @brief  Komendy W25Qxx
 */
#define W25Q_WRITE_ENABLE       0x06
#define W25Q_WRITE_DISABLE      0x04
#define W25Q_READ_STATUS        0x05
#define W25Q_READ_DATA          0x03
#define W25Q_PAGE_PROGRAM       0x02
#define W25Q_SECTOR_ERASE       0x20
#define W25Q_CHIP_ERASE         0xC7
#define W25Q_READ_ID            0x9F

/**
 * @brief  Odczyt ID pamięci
 */
void W25Q_ReadID(uint8_t *manufacturer, uint16_t *device_id)
{
    uint8_t cmd = W25Q_READ_ID;
    uint8_t data[3];
    
    SPI1_CS_LOW();
    HAL_SPI_Transmit(&hspi1, &cmd, 1, 100);
    HAL_SPI_Receive(&hspi1, data, 3, 100);
    SPI1_CS_HIGH();
    
    *manufacturer = data[0];
    *device_id = (data[1] << 8) | data[2];
}

/**
 * @brief  Write Enable
 */
void W25Q_WriteEnable(void)
{
    uint8_t cmd = W25Q_WRITE_ENABLE;
    
    SPI1_CS_LOW();
    HAL_SPI_Transmit(&hspi1, &cmd, 1, 100);
    SPI1_CS_HIGH();
}

/**
 * @brief  Odczyt Status Register
 */
uint8_t W25Q_ReadStatus(void)
{
    uint8_t cmd = W25Q_READ_STATUS;
    uint8_t status;
    
    SPI1_CS_LOW();
    HAL_SPI_Transmit(&hspi1, &cmd, 1, 100);
    HAL_SPI_Receive(&hspi1, &status, 1, 100);
    SPI1_CS_HIGH();
    
    return status;
}

/**
 * @brief  Czekaj aż pamięć będzie gotowa
 */
void W25Q_WaitBusy(void)
{
    while (W25Q_ReadStatus() & 0x01);  // Bit 0 = BUSY
}

/**
 * @brief  Odczyt danych
 */
void W25Q_ReadData(uint32_t address, uint8_t *buffer, uint32_t size)
{
    uint8_t cmd[4];
    
    cmd[0] = W25Q_READ_DATA;
    cmd[1] = (address >> 16) & 0xFF;
    cmd[2] = (address >> 8) & 0xFF;
    cmd[3] = address & 0xFF;
    
    SPI1_CS_LOW();
    HAL_SPI_Transmit(&hspi1, cmd, 4, 100);
    HAL_SPI_Receive(&hspi1, buffer, size, 1000);
    SPI1_CS_HIGH();
}

/**
 * @brief  Programowanie strony (256 bajtów max)
 */
void W25Q_PageProgram(uint32_t address, uint8_t *data, uint16_t size)
{
    uint8_t cmd[4];
    
    if (size > 256) size = 256;
    
    W25Q_WriteEnable();
    
    cmd[0] = W25Q_PAGE_PROGRAM;
    cmd[1] = (address >> 16) & 0xFF;
    cmd[2] = (address >> 8) & 0xFF;
    cmd[3] = address & 0xFF;
    
    SPI1_CS_LOW();
    HAL_SPI_Transmit(&hspi1, cmd, 4, 100);
    HAL_SPI_Transmit(&hspi1, data, size, 1000);
    SPI1_CS_HIGH();
    
    W25Q_WaitBusy();
}

/**
 * @brief  Kasowanie sektora (4KB)
 */
void W25Q_SectorErase(uint32_t address)
{
    uint8_t cmd[4];
    
    W25Q_WriteEnable();
    
    cmd[0] = W25Q_SECTOR_ERASE;
    cmd[1] = (address >> 16) & 0xFF;
    cmd[2] = (address >> 8) & 0xFF;
    cmd[3] = address & 0xFF;
    
    SPI1_CS_LOW();
    HAL_SPI_Transmit(&hspi1, cmd, 4, 100);
    SPI1_CS_HIGH();
    
    W25Q_WaitBusy();
}
```

## 🖥️ LCD TFT przez SPI (ILI9341)

### Inicjalizacja ILI9341

```c
/**
 * @brief  GPIO dla LCD control pins
 */
#define LCD_DC_PIN    GPIO_PIN_1  // Data/Command
#define LCD_RST_PIN   GPIO_PIN_2  // Reset
#define LCD_DC_PORT   GPIOB
#define LCD_RST_PORT  GPIOB

#define LCD_DC_LOW()   HAL_GPIO_WritePin(LCD_DC_PORT, LCD_DC_PIN, GPIO_PIN_RESET)
#define LCD_DC_HIGH()  HAL_GPIO_WritePin(LCD_DC_PORT, LCD_DC_PIN, GPIO_PIN_SET)
#define LCD_RST_LOW()  HAL_GPIO_WritePin(LCD_RST_PORT, LCD_RST_PIN, GPIO_PIN_RESET)
#define LCD_RST_HIGH() HAL_GPIO_WritePin(LCD_RST_PORT, LCD_RST_PIN, GPIO_PIN_SET)

/**
 * @brief  Wysłanie komendy do LCD
 */
void LCD_WriteCommand(uint8_t cmd)
{
    LCD_DC_LOW();
    SPI1_CS_LOW();
    HAL_SPI_Transmit(&hspi1, &cmd, 1, 10);
    SPI1_CS_HIGH();
}

/**
 * @brief  Wysłanie danych do LCD
 */
void LCD_WriteData(uint8_t data)
{
    LCD_DC_HIGH();
    SPI1_CS_LOW();
    HAL_SPI_Transmit(&hspi1, &data, 1, 10);
    SPI1_CS_HIGH();
}

/**
 * @brief  Inicjalizacja ILI9341
 */
void ILI9341_Init(void)
{
    // Reset
    LCD_RST_LOW();
    HAL_Delay(10);
    LCD_RST_HIGH();
    HAL_Delay(120);
    
    // Power Control A
    LCD_WriteCommand(0xCB);
    LCD_WriteData(0x39);
    LCD_WriteData(0x2C);
    LCD_WriteData(0x00);
    LCD_WriteData(0x34);
    LCD_WriteData(0x02);
    
    // Power Control B
    LCD_WriteCommand(0xCF);
    LCD_WriteData(0x00);
    LCD_WriteData(0xC1);
    LCD_WriteData(0x30);
    
    // Memory Access Control
    LCD_WriteCommand(0x36);
    LCD_WriteData(0x48);  // MY=0, MX=1, MV=0, ML=0, BGR=1
    
    // Pixel Format
    LCD_WriteCommand(0x3A);
    LCD_WriteData(0x55);  // 16-bit color
    
    // Sleep Out
    LCD_WriteCommand(0x11);
    HAL_Delay(120);
    
    // Display ON
    LCD_WriteCommand(0x29);
}
```

## 📡 SPI Slave Mode

### Konfiguracja jako Slave

```c
/**
 * @brief  SPI Slave configuration
 */
void SPI2_Slave_Init(void)
{
    hspi2.Instance = SPI2;
    hspi2.Init.Mode = SPI_MODE_SLAVE;
    hspi2.Init.Direction = SPI_DIRECTION_2LINES;
    hspi2.Init.DataSize = SPI_DATASIZE_8BIT;
    hspi2.Init.CLKPolarity = SPI_POLARITY_LOW;
    hspi2.Init.CLKPhase = SPI_PHASE_1EDGE;
    hspi2.Init.NSS = SPI_NSS_HARD_INPUT;  // Hardware NSS
    hspi2.Init.FirstBit = SPI_FIRSTBIT_MSB;
    
    HAL_SPI_Init(&hspi2);
    
    // Rozpocznij odbiórspi jako slave
    HAL_SPI_Receive_IT(&hspi2, rx_buffer, RX_SIZE);
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_dma|STM32F429I - DMA]]
- [[stm32f429i_gpio|STM32F429I - GPIO]]
- [[stm32f429i_lcd_tft|STM32F429I - LCD-TFT]]
- [[protokoly_komunikacyjne|Protokoły komunikacyjne]]

## 📝 Wzory i obliczenia

### Baudrate calculation
```
SPI_Clock = APB_Clock / Prescaler

Prescaler: 2, 4, 8, 16, 32, 64, 128, 256

Dla SPI1 (APB2 = 90 MHz):
Prescaler = 2  → 45 MHz
Prescaler = 4  → 22.5 MHz
Prescaler = 16 → 5.625 MHz
```

### Tryby SPI (CPOL/CPHA)
```
Mode 0: CPOL=0, CPHA=0 (najczęstszy)
Mode 1: CPOL=0, CPHA=1
Mode 2: CPOL=1, CPHA=0
Mode 3: CPOL=1, CPHA=1
```

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
