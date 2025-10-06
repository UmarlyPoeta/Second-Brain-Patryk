# STM32F429I - I2C i Magistrala Dwuprzewodowa

## 🔗 Inter-Integrated Circuit (I2C)

### Wprowadzenie
I2C to szeroko stosowana, dwuprzewodowa magistrala szeregowa do komunikacji między układami. STM32F429I posiada 3 interfejsy I2C obsługujące tryby Standard (100 kHz), Fast (400 kHz) i Fast Plus (1 MHz).

### Dostępne interfejsy I2C

| Interface | Magistrala | Max prędkość | Piny domyślne (SCL/SDA) |
|-----------|-----------|--------------|-------------------------|
| I2C1 | APB1 | 1 MHz | PB6/PB7, PB8/PB9 |
| I2C2 | APB1 | 1 MHz | PB10/PB11, PF0/PF1 |
| I2C3 | APB1 | 1 MHz | PA8/PC9, PH7/PH8 |

### Architektura I2C

```
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│   Master     │        │   Slave 1    │        │   Slave 2    │
│              │        │   (0x50)     │        │   (0x68)     │
│   SCL  ├─────┼────────┼──────────────┼────────┼──────────────┤
│   SDA  ├─────┼────────┼──────────────┼────────┼──────────────┤
│              │        │              │        │              │
└──────────────┘        └──────────────┘        └──────────────┘
     VDD                     VDD                     VDD
      │                       │                       │
      └──────┬────────────────┴───────────────────────┘
          4.7kΩ  (Pull-up resistors)
```

## 🔧 Konfiguracja I2C Master

### Podstawowa konfiguracja (100 kHz)

```c
/**
 * @brief  Konfiguracja I2C1 (100 kHz)
 */
I2C_HandleTypeDef hi2c1;

void I2C1_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    // Włącz zegary
    __HAL_RCC_I2C1_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    
    // GPIO Configuration: PB8=SCL, PB9=SDA
    GPIO_InitStruct.Pin = GPIO_PIN_8 | GPIO_PIN_9;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;  // Open-drain!
    GPIO_InitStruct.Pull = GPIO_PULLUP;      // Pull-up
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF4_I2C1;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    
    // I2C Configuration
    hi2c1.Instance = I2C1;
    hi2c1.Init.ClockSpeed = 100000;              // 100 kHz
    hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;      // Dla Standard mode
    hi2c1.Init.OwnAddress1 = 0;                  // Własny adres (master nie używa)
    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
    hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
    hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
    
    if (HAL_I2C_Init(&hi2c1) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Konfiguracja Fast Mode (400 kHz)
 */
void I2C1_FastMode_Init(void)
{
    // Podobna konfiguracja, tylko zmienić:
    hi2c1.Init.ClockSpeed = 400000;              // 400 kHz
    hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_16_9;   // Dla Fast mode
    
    HAL_I2C_Init(&hi2c1);
}
```

## 📤 Transmisja i odbiór danych

### Podstawowe operacje

```c
/**
 * @brief  Sprawdź czy urządzenie I2C jest dostępne
 */
uint8_t I2C_DeviceReady(uint8_t device_addr)
{
    // Timeout 100ms, 1 próba
    if (HAL_I2C_IsDeviceReady(&hi2c1, device_addr << 1, 1, 100) == HAL_OK) {
        return 1;  // Urządzenie odpowiada
    }
    return 0;  // Brak odpowiedzi
}

/**
 * @brief  Zapis jednego bajtu do rejestru
 */
HAL_StatusTypeDef I2C_WriteRegister(uint8_t device_addr, uint8_t reg_addr, uint8_t data)
{
    uint8_t buffer[2];
    buffer[0] = reg_addr;
    buffer[1] = data;
    
    return HAL_I2C_Master_Transmit(&hi2c1, device_addr << 1, buffer, 2, 100);
}

/**
 * @brief  Odczyt jednego bajtu z rejestru
 */
HAL_StatusTypeDef I2C_ReadRegister(uint8_t device_addr, uint8_t reg_addr, uint8_t *data)
{
    HAL_StatusTypeDef status;
    
    // Wyślij adres rejestru
    status = HAL_I2C_Master_Transmit(&hi2c1, device_addr << 1, &reg_addr, 1, 100);
    if (status != HAL_OK) return status;
    
    // Odbierz dane
    return HAL_I2C_Master_Receive(&hi2c1, device_addr << 1, data, 1, 100);
}

/**
 * @brief  Odczyt wielu bajtów z rejestru
 */
HAL_StatusTypeDef I2C_ReadRegisters(uint8_t device_addr, uint8_t reg_addr, 
                                    uint8_t *data, uint16_t size)
{
    HAL_StatusTypeDef status;
    
    // Wyślij adres rejestru
    status = HAL_I2C_Master_Transmit(&hi2c1, device_addr << 1, &reg_addr, 1, 100);
    if (status != HAL_OK) return status;
    
    // Odbierz dane
    return HAL_I2C_Master_Receive(&hi2c1, device_addr << 1, data, size, 100);
}

/**
 * @brief  Użycie HAL_I2C_Mem funkcji (łatwiejsze)
 */
HAL_StatusTypeDef I2C_WriteRegister_Mem(uint8_t device_addr, uint8_t reg_addr, uint8_t data)
{
    return HAL_I2C_Mem_Write(&hi2c1, device_addr << 1, reg_addr, 
                            I2C_MEMADD_SIZE_8BIT, &data, 1, 100);
}

HAL_StatusTypeDef I2C_ReadRegister_Mem(uint8_t device_addr, uint8_t reg_addr, uint8_t *data)
{
    return HAL_I2C_Mem_Read(&hi2c1, device_addr << 1, reg_addr, 
                           I2C_MEMADD_SIZE_8BIT, data, 1, 100);
}
```

## 🌡️ Sensor BME280 (temperatura, wilgotność, ciśnienie)

### Obsługa BME280

```c
/**
 * @brief  BME280 definitions
 */
#define BME280_ADDR         0x76  // lub 0x77
#define BME280_REG_ID       0xD0
#define BME280_REG_CTRL_HUM 0xF2
#define BME280_REG_CTRL_MEAS 0xF4
#define BME280_REG_CONFIG   0xF5
#define BME280_REG_PRESS    0xF7
#define BME280_REG_TEMP     0xFA
#define BME280_REG_HUM      0xFD

/**
 * @brief  Sprawdź ID BME280
 */
uint8_t BME280_CheckID(void)
{
    uint8_t id;
    I2C_ReadRegister_Mem(BME280_ADDR, BME280_REG_ID, &id);
    return (id == 0x60);  // BME280 chip ID
}

/**
 * @brief  Inicjalizacja BME280
 */
void BME280_Init(void)
{
    // Konfiguracja humidity oversampling ×1
    I2C_WriteRegister_Mem(BME280_ADDR, BME280_REG_CTRL_HUM, 0x01);
    
    // Konfiguracja temp/pressure oversampling ×1, normal mode
    I2C_WriteRegister_Mem(BME280_ADDR, BME280_REG_CTRL_MEAS, 0x27);
    
    // Konfiguracja: standby 1000ms, filter off
    I2C_WriteRegister_Mem(BME280_ADDR, BME280_REG_CONFIG, 0xA0);
    
    HAL_Delay(100);
}

/**
 * @brief  Odczyt temperatury (uproszczony)
 */
float BME280_ReadTemperature(void)
{
    uint8_t data[3];
    int32_t adc_T;
    
    // Odczyt surowych danych temperatury
    I2C_ReadRegisters(BME280_ADDR, BME280_REG_TEMP, data, 3);
    
    adc_T = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4);
    
    // Uproszczone przeliczenie (bez kalibracji)
    float temp = ((float)adc_T / 16384.0f) - 1024.0f;
    
    return temp / 5.0f;  // Przybliżona temperatura
}
```

## 🧭 MPU6050 (IMU - akcelerometr + żyroskop)

### Obsługa MPU6050

```c
/**
 * @brief  MPU6050 definitions
 */
#define MPU6050_ADDR        0x68
#define MPU6050_REG_WHO_AM_I 0x75
#define MPU6050_REG_PWR_MGMT_1 0x6B
#define MPU6050_REG_ACCEL_XOUT_H 0x3B
#define MPU6050_REG_GYRO_XOUT_H  0x43

typedef struct {
    int16_t accel_x;
    int16_t accel_y;
    int16_t accel_z;
    int16_t gyro_x;
    int16_t gyro_y;
    int16_t gyro_z;
    int16_t temp;
} MPU6050_Data_t;

/**
 * @brief  Inicjalizacja MPU6050
 */
void MPU6050_Init(void)
{
    uint8_t check;
    
    // Sprawdź WHO_AM_I
    I2C_ReadRegister_Mem(MPU6050_ADDR, MPU6050_REG_WHO_AM_I, &check);
    
    if (check == 0x68) {
        // Wybudzenie z sleep mode
        I2C_WriteRegister_Mem(MPU6050_ADDR, MPU6050_REG_PWR_MGMT_1, 0x00);
        HAL_Delay(100);
        
        // Konfiguracja sample rate divider
        I2C_WriteRegister_Mem(MPU6050_ADDR, 0x19, 0x07);
        
        // Konfiguracja DLPF
        I2C_WriteRegister_Mem(MPU6050_ADDR, 0x1A, 0x00);
        
        // Konfiguracja zakresu akcelerometru ±2g
        I2C_WriteRegister_Mem(MPU6050_ADDR, 0x1C, 0x00);
        
        // Konfiguracja zakresu żyroskopu ±250°/s
        I2C_WriteRegister_Mem(MPU6050_ADDR, 0x1B, 0x00);
    }
}

/**
 * @brief  Odczyt wszystkich danych
 */
void MPU6050_ReadAll(MPU6050_Data_t *data)
{
    uint8_t buffer[14];
    
    // Odczyt 14 bajtów (accel + temp + gyro)
    I2C_ReadRegisters(MPU6050_ADDR, MPU6050_REG_ACCEL_XOUT_H, buffer, 14);
    
    // Parsowanie danych (big-endian)
    data->accel_x = (buffer[0] << 8) | buffer[1];
    data->accel_y = (buffer[2] << 8) | buffer[3];
    data->accel_z = (buffer[4] << 8) | buffer[5];
    data->temp = (buffer[6] << 8) | buffer[7];
    data->gyro_x = (buffer[8] << 8) | buffer[9];
    data->gyro_y = (buffer[10] << 8) | buffer[11];
    data->gyro_z = (buffer[12] << 8) | buffer[13];
}

/**
 * @brief  Konwersja do jednostek fizycznych
 */
void MPU6050_GetAccel_g(MPU6050_Data_t *data, float *ax, float *ay, float *az)
{
    // Dla zakresu ±2g: 16384 LSB/g
    *ax = data->accel_x / 16384.0f;
    *ay = data->accel_y / 16384.0f;
    *az = data->accel_z / 16384.0f;
}

void MPU6050_GetGyro_dps(MPU6050_Data_t *data, float *gx, float *gy, float *gz)
{
    // Dla zakresu ±250°/s: 131 LSB/(°/s)
    *gx = data->gyro_x / 131.0f;
    *gy = data->gyro_y / 131.0f;
    *gz = data->gyro_z / 131.0f;
}
```

## 🖥️ OLED Display (SSD1306)

### Obsługa OLED SSD1306 (128x64)

```c
/**
 * @brief  SSD1306 definitions
 */
#define SSD1306_ADDR    0x3C
#define SSD1306_WIDTH   128
#define SSD1306_HEIGHT  64

/**
 * @brief  Wysłanie komendy do OLED
 */
void SSD1306_WriteCommand(uint8_t cmd)
{
    uint8_t data[2] = {0x00, cmd};  // 0x00 = command mode
    HAL_I2C_Master_Transmit(&hi2c1, SSD1306_ADDR << 1, data, 2, 100);
}

/**
 * @brief  Inicjalizacja OLED
 */
void SSD1306_Init(void)
{
    HAL_Delay(100);
    
    SSD1306_WriteCommand(0xAE);  // Display OFF
    SSD1306_WriteCommand(0x20);  // Set Memory Addressing Mode
    SSD1306_WriteCommand(0x00);  // Horizontal Addressing Mode
    SSD1306_WriteCommand(0xB0);  // Set Page Start Address
    SSD1306_WriteCommand(0xC8);  // Set COM Output Scan Direction
    SSD1306_WriteCommand(0x00);  // Set low column address
    SSD1306_WriteCommand(0x10);  // Set high column address
    SSD1306_WriteCommand(0x40);  // Set start line address
    SSD1306_WriteCommand(0x81);  // Set contrast control
    SSD1306_WriteCommand(0xFF);  // Max contrast
    SSD1306_WriteCommand(0xA1);  // Set segment re-map
    SSD1306_WriteCommand(0xA6);  // Set normal display
    SSD1306_WriteCommand(0xA8);  // Set multiplex ratio
    SSD1306_WriteCommand(0x3F);  // 1/64 duty
    SSD1306_WriteCommand(0xD3);  // Set display offset
    SSD1306_WriteCommand(0x00);  // No offset
    SSD1306_WriteCommand(0xD5);  // Set display clock divide ratio
    SSD1306_WriteCommand(0x80);  // Default
    SSD1306_WriteCommand(0xD9);  // Set pre-charge period
    SSD1306_WriteCommand(0xF1);
    SSD1306_WriteCommand(0xDA);  // Set COM pins
    SSD1306_WriteCommand(0x12);
    SSD1306_WriteCommand(0xDB);  // Set VCOMH
    SSD1306_WriteCommand(0x20);
    SSD1306_WriteCommand(0x8D);  // Enable charge pump
    SSD1306_WriteCommand(0x14);
    SSD1306_WriteCommand(0xAF);  // Display ON
    
    HAL_Delay(100);
}

/**
 * @brief  Wyślij bufor do OLED
 */
void SSD1306_UpdateScreen(uint8_t *buffer)
{
    // Bufor = 128 * 64 / 8 = 1024 bajty
    uint8_t cmd_data[2] = {0x40, 0};  // 0x40 = data mode
    
    for (uint8_t i = 0; i < 8; i++) {  // 8 stron (pages)
        SSD1306_WriteCommand(0xB0 + i);  // Ustaw stronę
        SSD1306_WriteCommand(0x00);      // Kolumna low nibble
        SSD1306_WriteCommand(0x10);      // Kolumna high nibble
        
        // Wyślij 128 bajtów dla tej strony
        cmd_data[0] = 0x40;  // Data mode
        HAL_I2C_Master_Transmit(&hi2c1, SSD1306_ADDR << 1, cmd_data, 1, 100);
        HAL_I2C_Master_Transmit(&hi2c1, SSD1306_ADDR << 1, 
                               &buffer[i * 128], 128, 100);
    }
}
```

## 🔍 I2C Scanner

### Skanowanie magistrali I2C

```c
/**
 * @brief  Znajdź wszystkie urządzenia na magistrali I2C
 */
void I2C_Scanner(void)
{
    printf("I2C Scanner\r\n");
    printf("Scanning...\r\n");
    
    uint8_t devices_found = 0;
    
    for (uint8_t addr = 1; addr < 128; addr++) {
        if (HAL_I2C_IsDeviceReady(&hi2c1, addr << 1, 1, 10) == HAL_OK) {
            printf("Device found at 0x%02X\r\n", addr);
            devices_found++;
        }
    }
    
    printf("Scan complete. Found %d device(s)\r\n", devices_found);
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_dma|STM32F429I - DMA]]
- [[stm32f429i_gpio|STM32F429I - GPIO]]
- [[protokoly_komunikacyjne|Protokoły komunikacyjne]]
- [[sensory_i_aktuatory|Sensory i aktuatory]]

## 📝 Wzory i obliczenia

### I2C Clock calculation
```
I2C_Clock = APB1_Clock / (2 × (CCR + 1))

Dla Standard Mode (100 kHz):
CCR = (APB1_Clock / (2 × 100000)) - 1

Dla Fast Mode (400 kHz):
CCR = (APB1_Clock / (2 × 400000)) - 1
```

### Adresowanie I2C
```
7-bit address: 0x00 - 0x7F
W ramce I2C: (Address << 1) | R/W_bit

Przykład:
Address = 0x68
Write: 0xD0 (0x68 << 1 | 0)
Read:  0xD1 (0x68 << 1 | 1)
```

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
