# STM32F429I - Bare Metal - I2C Komunikacja

## 🔌 I2C - Inter-Integrated Circuit

### Czym Jest I2C?

```
I2C to synchroniczna, dwuprzewodowa komunikacja master-slave.

Linie sygnałowe:
- SCL (Serial Clock)  - zegar generowany przez master
- SDA (Serial Data)   - linia danych (bidirectional)

Cechy:
- 2 przewody (oszczędność pinów)
- Multi-master, multi-slave
- Każde urządzenie ma unique adres (7 lub 10 bit)
- Open-drain outputs (wymaga pull-up)
- Prędkości:
  * Standard mode: 100 kHz
  * Fast mode: 400 kHz
  * Fast mode Plus: 1 MHz

Topologia:
┌────────┐         Pull-up Resistors
│ Master │              │     │
│        │──SCL─────────┴─────┼──┐
│        │──SDA───────────────┴─┐│
└────────┘                      ││
┌────────┐                      ││
│ Slave1 │──SCL─────────────────┘│
│  0x50  │──SDA───────────────────┘
└────────┘
┌────────┐
│ Slave2 │──SCL──────────────────┐
│  0x51  │──SDA──────────────────┘
└────────┘
```

### Protokół I2C - Timing

```
START: SDA falling edge gdy SCL high
┌───┐     ┌───────────
SCL │     │
    └─────┘
    ┌───────┐
SDA │       └──────────
      ↑ START

STOP: SDA rising edge gdy SCL high
    ┌─────────┐
SCL │         │
────┘         └───
──────────┐   ┌───
SDA       └───┘
            ↑ STOP

Byte transfer (8 bits + ACK):
     ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐
SCL  │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
    ─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─
SDA <D7><D6><D5><D4><D3><D2><D1><D0><ACK>

ACK: SDA pulled LOW przez slave (0 = ACK, 1 = NACK)
```

## 📋 Rejestry I2C

### Adresy Bazowe

```c
/**
 * @brief  I2C Base Addresses
 */
#define I2C1_BASE  0x40005400UL  // APB1
#define I2C2_BASE  0x40005800UL  // APB1
#define I2C3_BASE  0x40005C00UL  // APB1

/**
 * @brief  Struktura I2C
 */
typedef struct {
    volatile uint32_t CR1;    // 0x00: Control register 1
    volatile uint32_t CR2;    // 0x04: Control register 2
    volatile uint32_t OAR1;   // 0x08: Own address register 1
    volatile uint32_t OAR2;   // 0x0C: Own address register 2
    volatile uint32_t DR;     // 0x10: Data register
    volatile uint32_t SR1;    // 0x14: Status register 1
    volatile uint32_t SR2;    // 0x18: Status register 2
    volatile uint32_t CCR;    // 0x1C: Clock control register
    volatile uint32_t TRISE;  // 0x20: TRISE register
    volatile uint32_t FLTR;   // 0x24: FLTR register
} I2C_TypeDef;

#define I2C1  ((I2C_TypeDef*)I2C1_BASE)
#define I2C2  ((I2C_TypeDef*)I2C2_BASE)
#define I2C3  ((I2C_TypeDef*)I2C3_BASE)
```

### Rejestr CR1 - Control Register 1

```
I2C_CR1 - Control Register 1
Offset: 0x00
Reset value: 0x0000

Bit 0:  PE      - Peripheral enable
Bit 1:  SMBUS   - SMBus mode
Bit 2:  RESERVED
Bit 3:  SMBTYPE - SMBus type
Bit 4:  ENARP   - ARP enable
Bit 5:  ENPEC   - PEC enable
Bit 6:  ENGC    - General call enable
Bit 7:  NOSTRETCH - Clock stretching disable
Bit 8:  START   - Start generation
Bit 9:  STOP    - Stop generation
Bit 10: ACK     - Acknowledge enable
Bit 11: POS     - Acknowledge/PEC Position
Bit 12: PEC     - Packet error checking
Bit 13: ALERT   - SMBus alert
Bit 15: SWRST   - Software reset
```

### Rejestr CR2 - Control Register 2

```
I2C_CR2 - Control Register 2
Offset: 0x04
Reset value: 0x0000

Bits 0-5:  FREQ[5:0]  - Peripheral clock frequency (MHz)
                        Dla APB1 45 MHz -> FREQ = 45
Bit 8:     ITERREN    - Error interrupt enable
Bit 9:     ITEVTEN    - Event interrupt enable
Bit 10:    ITBUFEN    - Buffer interrupt enable
Bit 11:    DMAEN      - DMA requests enable
Bit 12:    LAST       - DMA last transfer
```

### Rejestr SR1 - Status Register 1

```
I2C_SR1 - Status Register 1
Offset: 0x14
Reset value: 0x0000

Bit 0:  SB      - Start bit (Master mode)
Bit 1:  ADDR    - Address sent (master) / matched (slave)
Bit 2:  BTF     - Byte transfer finished
Bit 3:  ADD10   - 10-bit header sent (Master)
Bit 4:  STOPF   - Stop detection (Slave)
Bit 6:  RxNE    - Data register not empty (receivers)
Bit 7:  TxE     - Data register empty (transmitters)
Bit 8:  BERR    - Bus error
Bit 9:  ARLO    - Arbitration lost
Bit 10: AF      - Acknowledge failure
Bit 11: OVR     - Overrun/Underrun
Bit 12: PECERR  - PEC Error in reception
Bit 14: TIMEOUT - Timeout or Tlow error
Bit 15: SMBALERT- SMBus alert
```

### Rejestr SR2 - Status Register 2

```
I2C_SR2 - Status Register 2
Offset: 0x18
Reset value: 0x0000

Bit 0:  MSL     - Master/Slave
Bit 1:  BUSY    - Bus busy
Bit 2:  TRA     - Transmitter/Receiver
Bit 4:  GENCALL - General call address (Slave)
Bit 5:  SMBDEFAULT - SMBus device default address
Bit 6:  SMBHOST - SMBus host header
Bit 7:  DUALF   - Dual flag
Bits 8-15: PEC[7:0] - Packet error checking register
```

### Rejestr CCR - Clock Control Register

```
I2C_CCR - Clock Control Register
Offset: 0x1C
Reset value: 0x0000

Bits 0-11: CCR[11:0] - Clock control register
Bit 14:    DUTY      - Fast mode duty cycle
Bit 15:    F/S       - I2C master mode selection
                       0 = Standard mode (100kHz)
                       1 = Fast mode (400kHz)

Obliczenia:
Standard mode (100 kHz):
  T_high = CCR × T_PCLK1
  T_low = CCR × T_PCLK1
  CCR = PCLK1 / (2 × 100000)

Fast mode (400 kHz):
  DUTY = 0: T_high = CCR × T_PCLK1, T_low = 2 × CCR × T_PCLK1
  DUTY = 1: T_high = 9 × CCR × T_PCLK1, T_low = 16 × CCR × T_PCLK1
```

### Rejestr TRISE

```
I2C_TRISE - TRISE Register
Offset: 0x20
Reset value: 0x0002

Bits 0-5: TRISE[5:0] - Maximum rise time

Standard mode: TRISE = (T_rise_max / T_PCLK1) + 1
  T_rise_max = 1000 ns
  TRISE = (1000 / (1/PCLK1)) + 1

Fast mode: T_rise_max = 300 ns
  TRISE = (300 / (1/PCLK1)) + 1

Przykład dla PCLK1 = 45 MHz:
  T_PCLK1 = 1/45000000 = 22.2 ns
  Standard: TRISE = (1000 / 22.2) + 1 = 46
  Fast: TRISE = (300 / 22.2) + 1 = 14
```

## 🔧 Konfiguracja I2C - Krok Po Kroku

### Obliczanie CCR i TRISE

```c
/**
 * @brief  Oblicz CCR dla I2C
 */
uint16_t Calculate_I2C_CCR(uint32_t pclk1_freq, uint32_t i2c_freq, uint8_t fast_mode)
{
    if (fast_mode) {
        // Fast mode 400 kHz, duty = 0 (2:1)
        // CCR = PCLK1 / (3 × I2C_freq)
        return pclk1_freq / (3 * i2c_freq);
    } else {
        // Standard mode 100 kHz
        // CCR = PCLK1 / (2 × I2C_freq)
        return pclk1_freq / (2 * i2c_freq);
    }
}

/**
 * @brief  Oblicz TRISE
 */
uint8_t Calculate_I2C_TRISE(uint32_t pclk1_freq, uint8_t fast_mode)
{
    // T_PCLK1 w nanosekundach
    float t_pclk1_ns = 1000000000.0f / pclk1_freq;
    
    if (fast_mode) {
        // T_rise_max = 300 ns
        return (uint8_t)(300.0f / t_pclk1_ns) + 1;
    } else {
        // T_rise_max = 1000 ns
        return (uint8_t)(1000.0f / t_pclk1_ns) + 1;
    }
}

/**
 * @brief  Przykłady obliczeń
 */
void I2C_Calculation_Examples(void)
{
    // PCLK1 = 45 MHz
    uint32_t pclk1 = 45000000;
    
    // Standard mode 100 kHz
    uint16_t ccr_std = Calculate_I2C_CCR(pclk1, 100000, 0);
    // ccr_std = 45000000 / (2 × 100000) = 225
    
    uint8_t trise_std = Calculate_I2C_TRISE(pclk1, 0);
    // trise_std = (1000 / 22.2) + 1 = 46
    
    // Fast mode 400 kHz
    uint16_t ccr_fast = Calculate_I2C_CCR(pclk1, 400000, 1);
    // ccr_fast = 45000000 / (3 × 400000) = 37
    
    uint8_t trise_fast = Calculate_I2C_TRISE(pclk1, 1);
    // trise_fast = (300 / 22.2) + 1 = 14
}
```

### Inicjalizacja I2C1 Master

```c
/**
 * @brief  I2C1 Master Init @ 100 kHz
 * 
 * Piny: PB6 = SCL, PB7 = SDA
 * Mode: Standard (100 kHz)
 * PCLK1: 45 MHz
 * 
 * KROK PO KROKU:
 */

void I2C1_Master_Init(void)
{
    // KROK 1: Włącz zegary
    RCC->AHB1ENR |= (1 << 1);   // GPIOB
    RCC->APB1ENR |= (1 << 21);  // I2C1
    
    // KROK 2: Konfiguruj piny PB6 (SCL), PB7 (SDA)
    // AF4 dla I2C1
    
    // Tryb Alternate Function
    GPIOB->MODER &= ~((0x3 << 12) | (0x3 << 14));
    GPIOB->MODER |= ((0x2 << 12) | (0x2 << 14));
    
    // AF4
    GPIOB->AFR[0] &= ~((0xF << 24) | (0xF << 28));
    GPIOB->AFR[0] |= ((0x4 << 24) | (0x4 << 28));
    
    // Open-drain (WYMAGANE dla I2C!)
    GPIOB->OTYPER |= (1 << 6) | (1 << 7);
    
    // Speed Very High
    GPIOB->OSPEEDR |= ((0x3 << 12) | (0x3 << 14));
    
    // Pull-up (opcjonalnie - external pull-ups preferowane)
    GPIOB->PUPDR &= ~((0x3 << 12) | (0x3 << 14));
    GPIOB->PUPDR |= ((0x1 << 12) | (0x1 << 14));
    
    // KROK 3: Reset I2C
    I2C1->CR1 |= (1 << 15);   // SWRST = 1
    I2C1->CR1 &= ~(1 << 15);  // SWRST = 0
    
    // KROK 4: Wyłącz I2C na czas konfiguracji
    I2C1->CR1 &= ~(1 << 0);   // PE = 0
    
    // KROK 5: Ustaw FREQ w CR2 (45 MHz)
    I2C1->CR2 &= ~(0x3F << 0);
    I2C1->CR2 |= (45 << 0);   // FREQ = 45
    
    // KROK 6: Ustaw CCR dla 100 kHz
    I2C1->CCR &= ~(1 << 15);  // F/S = 0 (standard mode)
    
    uint16_t ccr = Calculate_I2C_CCR(45000000, 100000, 0);
    I2C1->CCR &= ~(0xFFF << 0);
    I2C1->CCR |= (ccr << 0);  // CCR = 225
    
    // KROK 7: Ustaw TRISE
    uint8_t trise = Calculate_I2C_TRISE(45000000, 0);
    I2C1->TRISE = trise;      // TRISE = 46
    
    // KROK 8: Włącz I2C
    I2C1->CR1 |= (1 << 0);    // PE = 1
}
```

## 📤 Transmisja Danych - Master

### Sekwencja Master Transmit

```
1. Generuj START
2. Wyślij adres slave + Write bit (0)
3. Czekaj na ACK
4. Wyślij dane
5. Czekaj na ACK
6. (Powtarzaj 4-5)
7. Generuj STOP
```

### Implementacja Master Transmit

```c
/**
 * @brief  Generuj START condition
 */
void I2C_Start(void)
{
    // KROK 1: Generuj START
    I2C1->CR1 |= (1 << 8);  // START = 1
    
    // KROK 2: Czekaj na SB = 1 (Start bit)
    while (!(I2C1->SR1 & (1 << 0)));
    
    // SB cleared automatycznie przez odczyt SR1
}

/**
 * @brief  Wyślij adres slave
 */
void I2C_SendAddress(uint8_t address, uint8_t rw)
{
    // KROK 1: Wyślij adres (7 bit) + R/W bit
    // address << 1 | rw (0=write, 1=read)
    I2C1->DR = (address << 1) | rw;
    
    // KROK 2: Czekaj na ADDR = 1
    while (!(I2C1->SR1 & (1 << 1)));
    
    // KROK 3: Wyczyść ADDR przez odczyt SR1 i SR2
    volatile uint32_t dummy = I2C1->SR1;
    dummy = I2C1->SR2;
    (void)dummy;
}

/**
 * @brief  Wyślij dane
 */
void I2C_WriteData(uint8_t data)
{
    // KROK 1: Czekaj na TxE = 1
    while (!(I2C1->SR1 & (1 << 7)));
    
    // KROK 2: Zapisz dane
    I2C1->DR = data;
    
    // KROK 3: Czekaj na BTF = 1 (byte transfer finished)
    while (!(I2C1->SR1 & (1 << 2)));
}

/**
 * @brief  Generuj STOP condition
 */
void I2C_Stop(void)
{
    I2C1->CR1 |= (1 << 9);  // STOP = 1
}

/**
 * @brief  Kompletny Master Write
 */
void I2C_Master_Write(uint8_t slave_addr, uint8_t *data, uint16_t size)
{
    // START
    I2C_Start();
    
    // Adres + Write
    I2C_SendAddress(slave_addr, 0);
    
    // Wyślij dane
    for (uint16_t i = 0; i < size; i++) {
        I2C_WriteData(data[i]);
    }
    
    // STOP
    I2C_Stop();
}
```

## 📥 Odbiór Danych - Master

### Sekwencja Master Receive

```
1. Generuj START
2. Wyślij adres slave + Read bit (1)
3. Czekaj na ACK
4. Włącz ACK (dla multi-byte)
5. Odbierz dane
6. Wyślij ACK (kontynuuj) lub NACK (koniec)
7. (Powtarzaj 5-6)
8. Generuj STOP
```

### Implementacja Master Receive

```c
/**
 * @brief  Odbierz jeden bajt
 */
uint8_t I2C_ReadData_ACK(void)
{
    // Włącz ACK
    I2C1->CR1 |= (1 << 10);  // ACK = 1
    
    // Czekaj na RxNE = 1
    while (!(I2C1->SR1 & (1 << 6)));
    
    return I2C1->DR;
}

/**
 * @brief  Odbierz ostatni bajt (NACK)
 */
uint8_t I2C_ReadData_NACK(void)
{
    // Wyłącz ACK
    I2C1->CR1 &= ~(1 << 10);  // ACK = 0
    
    // Czekaj na RxNE = 1
    while (!(I2C1->SR1 & (1 << 6)));
    
    return I2C1->DR;
}

/**
 * @brief  Master Read - single byte
 */
uint8_t I2C_Master_Read_Single(uint8_t slave_addr)
{
    uint8_t data;
    
    // START
    I2C_Start();
    
    // Adres + Read
    I2C_SendAddress(slave_addr, 1);
    
    // Disable ACK (single byte)
    I2C1->CR1 &= ~(1 << 10);
    
    // Czekaj na dane
    while (!(I2C1->SR1 & (1 << 6)));
    
    // Generate STOP przed odczytem
    I2C_Stop();
    
    // Odczytaj dane
    data = I2C1->DR;
    
    return data;
}

/**
 * @brief  Master Read - multiple bytes
 */
void I2C_Master_Read(uint8_t slave_addr, uint8_t *buffer, uint16_t size)
{
    // START
    I2C_Start();
    
    // Adres + Read
    I2C_SendAddress(slave_addr, 1);
    
    // Odbierz dane
    for (uint16_t i = 0; i < size; i++) {
        if (i == size - 1) {
            // Ostatni bajt - NACK i STOP
            buffer[i] = I2C_ReadData_NACK();
            I2C_Stop();
        } else {
            // Nie ostatni - ACK
            buffer[i] = I2C_ReadData_ACK();
        }
    }
}
```

## 🔧 Operacje z Rejestrem - Typowy Pattern

### Write Register

```c
/**
 * @brief  Zapis do rejestru slave device
 * 
 * Sekwencja:
 * START - ADDR(W) - REG_ADDR - DATA - STOP
 */
void I2C_Write_Register(uint8_t slave_addr, uint8_t reg_addr, uint8_t data)
{
    I2C_Start();
    I2C_SendAddress(slave_addr, 0);  // Write
    I2C_WriteData(reg_addr);         // Register address
    I2C_WriteData(data);             // Data
    I2C_Stop();
}

/**
 * @brief  Zapis wielu bajtów do rejestru
 */
void I2C_Write_Registers(uint8_t slave_addr, uint8_t reg_addr, uint8_t *data, uint16_t size)
{
    I2C_Start();
    I2C_SendAddress(slave_addr, 0);
    I2C_WriteData(reg_addr);
    
    for (uint16_t i = 0; i < size; i++) {
        I2C_WriteData(data[i]);
    }
    
    I2C_Stop();
}
```

### Read Register

```c
/**
 * @brief  Odczyt z rejestru slave device
 * 
 * Sekwencja:
 * START - ADDR(W) - REG_ADDR - REPEATED_START - ADDR(R) - DATA - STOP
 */
uint8_t I2C_Read_Register(uint8_t slave_addr, uint8_t reg_addr)
{
    uint8_t data;
    
    // KROK 1: Write register address
    I2C_Start();
    I2C_SendAddress(slave_addr, 0);  // Write
    I2C_WriteData(reg_addr);
    
    // KROK 2: Repeated START
    I2C_Start();
    
    // KROK 3: Read data
    I2C_SendAddress(slave_addr, 1);  // Read
    
    I2C1->CR1 &= ~(1 << 10);  // NACK
    while (!(I2C1->SR1 & (1 << 6)));
    
    I2C_Stop();
    data = I2C1->DR;
    
    return data;
}

/**
 * @brief  Odczyt wielu bajtów z rejestru
 */
void I2C_Read_Registers(uint8_t slave_addr, uint8_t reg_addr, uint8_t *buffer, uint16_t size)
{
    // Write register address
    I2C_Start();
    I2C_SendAddress(slave_addr, 0);
    I2C_WriteData(reg_addr);
    
    // Repeated START
    I2C_Start();
    
    // Read data
    I2C_SendAddress(slave_addr, 1);
    
    for (uint16_t i = 0; i < size; i++) {
        if (i == size - 1) {
            buffer[i] = I2C_ReadData_NACK();
            I2C_Stop();
        } else {
            buffer[i] = I2C_ReadData_ACK();
        }
    }
}
```

## 📟 Przykład: BME280 Sensor

### Komunikacja z BME280

```c
/**
 * @brief  BME280 I2C Address i Rejestry
 */
#define BME280_ADDR       0x76  // lub 0x77

#define BME280_REG_ID     0xD0
#define BME280_REG_RESET  0xE0
#define BME280_REG_CTRL_HUM  0xF2
#define BME280_REG_STATUS    0xF3
#define BME280_REG_CTRL_MEAS 0xF4
#define BME280_REG_CONFIG    0xF5
#define BME280_REG_PRESS_MSB 0xF7  // Pressure/Temp/Hum data start

/**
 * @brief  Odczyt ID BME280 (powinno być 0x60)
 */
uint8_t BME280_Read_ID(void)
{
    return I2C_Read_Register(BME280_ADDR, BME280_REG_ID);
}

/**
 * @brief  Reset BME280
 */
void BME280_Reset(void)
{
    I2C_Write_Register(BME280_ADDR, BME280_REG_RESET, 0xB6);
    delay_ms(10);  // Wait for reset
}

/**
 * @brief  Inicjalizacja BME280
 */
void BME280_Init(void)
{
    // Humidity oversampling ×1
    I2C_Write_Register(BME280_ADDR, BME280_REG_CTRL_HUM, 0x01);
    
    // Temp oversampling ×1, Pressure oversampling ×1, Normal mode
    I2C_Write_Register(BME280_ADDR, BME280_REG_CTRL_MEAS, 0x27);
    
    // Standby 0.5ms, filter off
    I2C_Write_Register(BME280_ADDR, BME280_REG_CONFIG, 0x00);
}

/**
 * @brief  Odczyt surowych danych (Press, Temp, Hum)
 */
void BME280_Read_Raw(int32_t *press, int32_t *temp, int32_t *hum)
{
    uint8_t data[8];
    
    // Odczytaj 8 bajtów od 0xF7
    I2C_Read_Registers(BME280_ADDR, BME280_REG_PRESS_MSB, data, 8);
    
    // Parse pressure (20-bit)
    *press = (int32_t)((data[0] << 12) | (data[1] << 4) | (data[2] >> 4));
    
    // Parse temperature (20-bit)
    *temp = (int32_t)((data[3] << 12) | (data[4] << 4) | (data[5] >> 4));
    
    // Parse humidity (16-bit)
    *hum = (int32_t)((data[6] << 8) | data[7]);
}

/**
 * @brief  Przykład użycia
 */
void BME280_Example(void)
{
    I2C1_Master_Init();
    
    uint8_t id = BME280_Read_ID();
    printf("BME280 ID: 0x%02X\r\n", id);
    
    if (id == 0x60) {
        BME280_Init();
        
        while (1) {
            int32_t press, temp, hum;
            BME280_Read_Raw(&press, &temp, &hum);
            
            // (Kompensacja danych wymaga calibration coefficients)
            printf("Raw: P=%d T=%d H=%d\r\n", press, temp, hum);
            
            delay_ms(1000);
        }
    }
}
```

## 🔍 I2C Scanner

### Skanowanie Urządzeń na Magistrali

```c
/**
 * @brief  I2C Scanner - znajdź wszystkie urządzenia
 */
void I2C_Scanner(void)
{
    printf("I2C Scanner:\r\n");
    printf("Scanning addresses 0x00-0x7F...\r\n\r\n");
    
    uint8_t found = 0;
    
    for (uint8_t addr = 0; addr < 128; addr++) {
        // START
        I2C1->CR1 |= (1 << 8);
        while (!(I2C1->SR1 & (1 << 0)));
        
        // Send address + Write
        I2C1->DR = (addr << 1);
        
        // Czekaj krótko na ADDR lub AF
        uint32_t timeout = 10000;
        while (timeout--) {
            uint32_t sr1 = I2C1->SR1;
            
            if (sr1 & (1 << 1)) {  // ADDR
                // Device found!
                printf("Found device at 0x%02X\r\n", addr);
                found++;
                
                // Clear ADDR
                volatile uint32_t dummy = I2C1->SR1;
                dummy = I2C1->SR2;
                (void)dummy;
                break;
            }
            
            if (sr1 & (1 << 10)) {  // AF (No ACK)
                // No device
                I2C1->SR1 &= ~(1 << 10);  // Clear AF
                break;
            }
        }
        
        // STOP
        I2C1->CR1 |= (1 << 9);
        delay_ms(1);
    }
    
    printf("\r\nScan complete. Found %d device(s).\r\n", found);
}
```

## 🐛 Obsługa Błędów

### Sprawdzanie i Czyszczenie Błędów

```c
/**
 * @brief  Sprawdź błędy I2C
 */
uint8_t I2C_Check_Errors(void)
{
    uint32_t sr1 = I2C1->SR1;
    
    if (sr1 & (1 << 10)) {  // AF - Acknowledge Failure
        I2C1->SR1 &= ~(1 << 10);
        return 1;  // NACK
    }
    
    if (sr1 & (1 << 9)) {   // ARLO - Arbitration Lost
        I2C1->SR1 &= ~(1 << 9);
        return 2;
    }
    
    if (sr1 & (1 << 8)) {   // BERR - Bus Error
        I2C1->SR1 &= ~(1 << 8);
        return 3;
    }
    
    if (sr1 & (1 << 11)) {  // OVR - Overrun
        I2C1->SR1 &= ~(1 << 11);
        return 4;
    }
    
    return 0;  // No error
}

/**
 * @brief  Recovery przy błędzie
 */
void I2C_Error_Recovery(void)
{
    // Software reset
    I2C1->CR1 |= (1 << 15);
    I2C1->CR1 &= ~(1 << 15);
    
    // Re-init
    I2C1_Master_Init();
}
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_gpio|Bare Metal - GPIO dla AF i Open-Drain]]
- [[stm32f429i_bare_metal_nvic|Bare Metal - NVIC i przerwania]]
- [[stm32f429i_bare_metal_dma_i2c|Bare Metal - DMA z I2C]]
- [[stm32f429i_i2c|I2C z HAL - porównanie]]

## 📝 Podsumowanie

### Kluczowe Rejestry I2C
- **CR1** - Control (PE, START, STOP, ACK)
- **CR2** - FREQ, interrupts, DMA
- **SR1** - Status (SB, ADDR, TxE, RxNE, BTF, AF)
- **SR2** - MSL, BUSY, TRA
- **DR** - Data register
- **CCR** - Clock control
- **TRISE** - Rise time

### Wzory
```
Standard mode (100 kHz):
  CCR = PCLK1 / (2 × 100000)
  TRISE = (1000ns / T_PCLK1) + 1

Fast mode (400 kHz):
  CCR = PCLK1 / (3 × 400000)
  TRISE = (300ns / T_PCLK1) + 1
```

### Master Write Sekwencja
```
START → ADDR(W) → DATA → ... → STOP
```

### Master Read Sekwencja
```
START → ADDR(W) → REG → Re-START → ADDR(R) → DATA → ... → NACK → STOP
```

### Wymagania Sprzętowe
- **Open-drain outputs** - obowiązkowe!
- **External pull-ups** - 4.7kΩ typowo
- **Fast rise/fall times** - krótkie przewody

---

*Następna notatka: [[stm32f429i_bare_metal_adc|Bare Metal - ADC Konwerter]]*
