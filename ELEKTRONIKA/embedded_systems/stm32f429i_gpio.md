# STM32F429I - GPIO i Konfiguracja Pinów

## 📌 General Purpose Input/Output (GPIO)

### Wprowadzenie
STM32F429I posiada do 168 pinów GPIO (w zależności od obudowy) zorganizowanych w porty oznaczone literami od A do K. Każdy pin GPIO może być konfigurowany niezależnie w różnych trybach pracy.

## 🔌 Porty GPIO

### Dostępne porty
- **GPIOA - GPIOK**: 11 portów
- **Liczba pinów**: 16 pinów na port (GPIO_PIN_0 do GPIO_PIN_15)
- **Zegar**: Wszystkie porty GPIO podłączone do magistrali AHB1

```c
// Włączanie zegarów portów GPIO
__HAL_RCC_GPIOA_CLK_ENABLE();
__HAL_RCC_GPIOB_CLK_ENABLE();
__HAL_RCC_GPIOC_CLK_ENABLE();
// ... itd.
```

## ⚙️ Tryby pracy GPIO

### 1. Input Mode (Wejście)
```c
/**
 * @brief  Konfiguracja pinu jako wejście cyfrowe
 */
void GPIO_Input_Config(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;  // lub GPIO_PULLDOWN, GPIO_NOPULL
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

/**
 * @brief  Odczyt stanu pinu
 */
void Read_GPIO_Pin(void)
{
    GPIO_PinState pin_state = HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0);
    
    if (pin_state == GPIO_PIN_SET) {
        // Pin w stanie wysokim (3.3V)
    } else {
        // Pin w stanie niskim (0V)
    }
}
```

### 2. Output Mode (Wyjście)

#### Push-Pull Output
```c
/**
 * @brief  Wyjście typu Push-Pull
 */
void GPIO_Output_PushPull(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;  // Push-Pull
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // Sterowanie pinem
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);   // HIGH
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET); // LOW
    
    // Toggle pin
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
}
```

#### Open-Drain Output
```c
/**
 * @brief  Wyjście typu Open-Drain
 */
void GPIO_Output_OpenDrain(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOB_CLK_ENABLE();
    
    GPIO_InitStruct.Pin = GPIO_PIN_8 | GPIO_PIN_9;  // I2C SCL, SDA
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;     // Open-Drain
    GPIO_InitStruct.Pull = GPIO_PULLUP;             // Wymagany pull-up
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
}
```

### 3. Alternate Function Mode (Funkcje alternatywne)

```c
/**
 * @brief  Konfiguracja pinów dla USART1
 */
void GPIO_USART1_Config(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // PA9 - USART1_TX, PA10 - USART1_RX
    GPIO_InitStruct.Pin = GPIO_PIN_9 | GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART1;  // Funkcja alternatywna 7
    
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

/**
 * @brief  Konfiguracja pinów dla SPI1
 */
void GPIO_SPI1_Config(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // PA5 - SCK, PA6 - MISO, PA7 - MOSI
    GPIO_InitStruct.Pin = GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF5_SPI1;
    
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}
```

### Tabela funkcji alternatywnych (wybrane)
| AF Number | Funkcja |
|-----------|---------|
| AF0 | SYSTEM (EVENTOUT, MCO) |
| AF1 | TIM1/TIM2 |
| AF2 | TIM3/TIM4/TIM5 |
| AF3 | TIM8/TIM9/TIM10/TIM11 |
| AF4 | I2C1/I2C2/I2C3 |
| AF5 | SPI1/SPI2/SPI4/SPI5/SPI6 |
| AF6 | SPI3/SAI1 |
| AF7 | USART1/USART2/USART3 |
| AF8 | UART4/UART5/USART6 |
| AF9 | CAN1/CAN2/TIM12/TIM13/TIM14 |
| AF10 | USB_OTG_FS/USB_OTG_HS |
| AF11 | ETH |
| AF12 | FMC/SDIO/OTG_HS_FS |
| AF13 | DCMI |
| AF14 | LCD-TFT |
| AF15 | EVENTOUT |

### 4. Analog Mode (Tryb analogowy)

```c
/**
 * @brief  Konfiguracja pinu jako wejście analogowe dla ADC
 */
void GPIO_Analog_Config(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // PA0 - ADC1_IN0
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}
```

### 5. Interrupt Mode (Przerwania)

```c
/**
 * @brief  Konfiguracja pinu z przerwaniem
 */
void GPIO_Interrupt_Config(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOC_CLK_ENABLE();
    
    // PC13 - przycisk USER (zbocze opadające)
    GPIO_InitStruct.Pin = GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;  // Przerwanie na zbocze opadające
    // Dostępne opcje:
    // GPIO_MODE_IT_RISING        - zbocze narastające
    // GPIO_MODE_IT_FALLING       - zbocze opadające  
    // GPIO_MODE_IT_RISING_FALLING - oba zbocza
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
    
    // Konfiguracja NVIC
    HAL_NVIC_SetPriority(EXTI15_10_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);
}

/**
 * @brief  Handler przerwania EXTI dla pinów 10-15
 */
void EXTI15_10_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13);
}

/**
 * @brief  Callback przerwania GPIO
 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_13) {
        // Obsługa przycisku
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);  //Toggluj LED
    }
}
```

## ⚡ Prędkość GPIO

### Dostępne prędkości
```c
GPIO_SPEED_FREQ_LOW         // Niska (2 MHz)
GPIO_SPEED_FREQ_MEDIUM      // Średnia (25 MHz)
GPIO_SPEED_FREQ_HIGH        // Wysoka (50 MHz)
GPIO_SPEED_FREQ_VERY_HIGH   // Bardzo wysoka (100 MHz)
```

### Wybór prędkości
- **LOW**: Sygnały wolnozmienne, przyciski, LED
- **MEDIUM**: Standardowe peryferyjne
- **HIGH**: SPI, I2C przy wyższych prędkościach
- **VERY_HIGH**: Wysokie częstotliwości, Ethernet, LCD-TFT

## 🔧 Pull-up/Pull-down

```c
// Opcje pull-up/pull-down
GPIO_NOPULL     // Brak rezystora podciągającego
GPIO_PULLUP     // Rezystor pull-up (~40kΩ)
GPIO_PULLDOWN   // Rezystor pull-down (~40kΩ)
```

### Przykłady zastosowania
- **PULLUP**: Przyciski (aktywne LOW), linie I2C, SPI CS
- **PULLDOWN**: Rzadko używany
- **NOPULL**: Sygnały z zewnętrznymi rezystorami

## 💡 Praktyczne przykłady

### LED blink (miganie LED)
```c
/**
 * @brief  Prosta aplikacja migania LED
 */
int main(void)
{
    HAL_Init();
    SystemClock_Config();
    
    // Konfiguracja LED na PA5
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    while (1) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        HAL_Delay(500);  // 500 ms
    }
}
```

### Obsługa przycisku z debouncing
```c
/**
 * @brief  Odczyt przycisku z programowym debouncing
 */
typedef struct {
    GPIO_TypeDef* port;
    uint16_t pin;
    uint32_t last_press_time;
    uint16_t debounce_delay;
} Button_t;

uint8_t Button_IsPressed(Button_t* button)
{
    uint32_t current_time = HAL_GetTick();
    
    if (HAL_GPIO_ReadPin(button->port, button->pin) == GPIO_PIN_RESET) {
        if ((current_time - button->last_press_time) > button->debounce_delay) {
            button->last_press_time = current_time;
            return 1;  // Przycisk wciśnięty
        }
    }
    
    return 0;  // Przycisk nie wciśnięty lub debounce
}

// Użycie
Button_t user_button = {
    .port = GPIOC,
    .pin = GPIO_PIN_13,
    .debounce_delay = 50  // 50 ms debounce
};

void main_loop(void)
{
    if (Button_IsPressed(&user_button)) {
        // Akcja po wciśnięciu przycisku
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
}
```

### Sterowanie RGB LED
```c
/**
 * @brief  Sterowanie RGB LED
 */
typedef struct {
    GPIO_TypeDef* port;
    uint16_t red_pin;
    uint16_t green_pin;
    uint16_t blue_pin;
} RGB_LED_t;

void RGB_LED_Init(RGB_LED_t* led)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    // Zakładamy że wszystkie piny są na tym samym porcie
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    GPIO_InitStruct.Pin = led->red_pin | led->green_pin | led->blue_pin;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    
    HAL_GPIO_Init(led->port, &GPIO_InitStruct);
}

void RGB_LED_SetColor(RGB_LED_t* led, uint8_t red, uint8_t green, uint8_t blue)
{
    HAL_GPIO_WritePin(led->port, led->red_pin, red ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(led->port, led->green_pin, green ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(led->port, led->blue_pin, blue ? GPIO_PIN_SET : GPIO_PIN_RESET);
}

// Przykład użycia
RGB_LED_t rgb_led = {
    .port = GPIOA,
    .red_pin = GPIO_PIN_0,
    .green_pin = GPIO_PIN_1,
    .blue_pin = GPIO_PIN_2
};

RGB_LED_SetColor(&rgb_led, 1, 0, 0);  // Czerwony
RGB_LED_SetColor(&rgb_led, 0, 1, 0);  // Zielony
RGB_LED_SetColor(&rgb_led, 0, 0, 1);  // Niebieski
```

### Szybkie operacje bitowe (Direct Register Access)
```c
/**
 * @brief  Szybkie ustawienie/reset pinu (bez HAL)
 */
// Szybkie ustawienie pinu (atomic)
GPIOA->BSRR = GPIO_PIN_5;  // Set PA5

// Szybki reset pinu (atomic)
GPIOA->BSRR = (uint32_t)GPIO_PIN_5 << 16;  // Reset PA5

// Odczyt całego portu
uint16_t port_value = GPIOA->IDR;

// Zapis do całego portu
GPIOA->ODR = 0x00FF;

// Toggle pinu (szybka implementacja)
GPIOA->ODR ^= GPIO_PIN_5;
```

## 📋 Linie EXTI (External Interrupt)

### Mapowanie EXTI
Każdy numer pinu (0-15) może być podłączony tylko do jednego portu jednocześnie:
- EXTI0: może być PA0, PB0, PC0, itd. (tylko jeden)
- EXTI1: może być PA1, PB1, PC1, itd. (tylko jeden)
- ...
- EXTI15: może być PA15, PB15, PC15, itd. (tylko jeden)

### IRQ handlery EXTI
```c
EXTI0_IRQHandler      // EXTI Line 0
EXTI1_IRQHandler      // EXTI Line 1
EXTI2_IRQHandler      // EXTI Line 2
EXTI3_IRQHandler      // EXTI Line 3
EXTI4_IRQHandler      // EXTI Line 4
EXTI9_5_IRQHandler    // EXTI Lines 5-9
EXTI15_10_IRQHandler  // EXTI Lines 10-15
```

## 🔒 GPIO Locking

### Blokowanie konfiguracji GPIO
```c
/**
 * @brief  Zablokowanie konfiguracji pinu (do resetu)
 */
void GPIO_Lock_Config(void)
{
    // Po zablokowaniu konfiguracja nie może być zmieniona
    // do resetu mikrokontrolera
    HAL_GPIO_LockPin(GPIOA, GPIO_PIN_5);
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_przerwania|STM32F429I - Przerwania i NVIC]]
- [[stm32f429i_timery|STM32F429I - Timery]]
- [[stm32f429i_pwm|STM32F429I - PWM]]
- [[io_cyfrowe_analogowe|Wejścia/Wyjścia cyfrowe i analogowe]]

## 📝 Best Practices

### Zalecenia
1. **Zawsze włączaj zegar portu** przed konfiguracją GPIO
2. **Używaj odpowiedniej prędkości** - wyższa = większy pobór prądu
3. **Pull-up dla przycisków** - aktywne LOW z pull-up
4. **Debouncing** - zawsze dla przycisków (sprzętowy lub programowy)
5. **Open-drain dla I2C** - wymagane dla magistrali I2C
6. **Atomic operations** - używaj BSRR dla szybkich operacji

### Typowe błędy
1. Brak włączenia zegara portu
2. Niewłaściwa funkcja alternatywna
3. Brak debouncing dla przycisków
4. Zbyt wysoka prędkość dla wolnych sygnałów

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
