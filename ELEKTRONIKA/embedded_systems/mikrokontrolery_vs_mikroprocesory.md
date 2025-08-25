# Mikrokontrolery vs Mikroprocesory

## Różnice podstawowe

### Mikrokontroler (MCU - Microcontroller Unit)
- **Definicja**: Kompletny system komputerowy na jednym chipie
- **Komponenty**: CPU + RAM + Flash + Peryferyjne w jednym układzie
- **Przykłady**: ATmega328P (Arduino), PIC, STM32, ESP32
- **Zastosowania**: Systemy wbudowane, IoT, automatyka

### Mikroprocesor (MPU - Microprocessor Unit)  
- **Definicja**: Tylko jednostka centralna (CPU)
- **Komponenty**: Wymaga zewnętrznej pamięci i peryferii
- **Przykłady**: Intel x86, ARM Cortex-A (Raspberry Pi)
- **Zastosowania**: Komputery, serwery, zaawansowane systemy embedded

## Porównanie charakterystyk

| Cecha | Mikrokontroler | Mikroprocesor |
|-------|----------------|---------------|
| **Złożoność** | Niska-średnia | Wysoka |
| **Koszt** | Niski ($1-20) | Wysoki ($50-500+) |
| **Pobór mocy** | Bardzo niski (μW-mW) | Wysoki (W) |
| **Szybkość** | 1MHz-200MHz | 500MHz-5GHz+ |
| **Pamięć RAM** | KB-MB | MB-GB |
| **System operacyjny** | Bare metal/RTOS | Linux/Windows |
| **Czas uruchomienia** | Milisekundy | Sekundy |

## Architektura mikrokontrolerów

### Architektura Harvard vs von Neumann

#### Architektura Harvard (typowa dla MCU)
```
CPU ←→ Instruction Memory (Flash)
 ↕
Data Memory (RAM)
```
- **Zalety**: Równoczesny dostęp do instrukcji i danych
- **Przykłady**: AVR (Arduino), PIC, ARM Cortex-M

#### Architektura von Neumann (typowa dla MPU)
```
CPU ←→ Unified Memory (instrukcje + dane)
```
- **Zalety**: Elastyczność podziału pamięci
- **Przykłady**: Intel x86, ARM Cortex-A

### Blokowy schemat mikrokontrolera
```
┌─────────────────────────────────────┐
│              CPU CORE                │
├─────────────────────────────────────┤
│    Flash Memory    │   RAM Memory    │
├─────────────────────────────────────┤
│  Timer/Counter  │  UART  │   SPI    │
├─────────────────────────────────────┤
│      I2C        │  ADC   │   PWM    │
├─────────────────────────────────────┤
│             GPIO PORTS              │
└─────────────────────────────────────┘
```

## Popularne rodziny mikrokontrolerów

### AVR (Atmel/Microchip)
- **Architektura**: 8-bit RISC Harvard
- **Przykłady**: ATmega328P (Arduino Uno), ATtiny85
- **Cechy**: 
  - Proste programowanie w C/C++
  - Duża społeczność (Arduino)
  - Niski koszt

```c
// Przykład kodu AVR (bare metal)
#include <avr/io.h>
#include <util/delay.h>

int main() {
    DDRB |= (1 << PB5);  // Pin 13 jako wyjście
    
    while(1) {
        PORTB |= (1 << PB5);   // Włącz LED
        _delay_ms(1000);
        PORTB &= ~(1 << PB5);  // Wyłącz LED
        _delay_ms(1000);
    }
    return 0;
}
```

### ARM Cortex-M (ST, NXP, Nordic)
- **Architektura**: 32-bit RISC Harvard
- **Modele**: Cortex-M0, M0+, M3, M4, M7
- **Cechy**:
  - Wysoka wydajność
  - Zaawansowane peryferyjne
  - RTOS support

```c
// Przykład STM32 HAL
#include "stm32f4xx_hal.h"

int main() {
    HAL_Init();
    SystemClock_Config();
    
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    while(1) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        HAL_Delay(1000);
    }
}
```

### PIC (Microchip)
- **Architektura**: 8-bit, 16-bit, 32-bit
- **Cechy**:
  - Bardzo niski pobór mocy
  - MPLAB X IDE
  - XC kompilatory

### ESP32 (Espressif)
- **Architektura**: Dual-core Xtensa LX6
- **Cechy**:
  - WiFi + Bluetooth wbudowane
  - FreeRTOS
  - Arduino IDE support

```c
// ESP32 WiFi przykład
#include "WiFi.h"

const char* ssid = "your_network";
const char* password = "your_password";

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("WiFi connected!");
}
```

## Rejestry i porty

### Rejestry mikrokontrolerów
```c
// Przykład rejestrów AVR
DDRB  = 0xFF;    // Data Direction Register - wszystkie piny wyjścia
PORTB = 0xAA;    // Port Register - wartość na pinach
PINB;            // Pin Register - odczyt stanu pinów

// Manipulacja pojedynczych bitów
PORTB |= (1 << PB5);   // Ustaw bit 5
PORTB &= ~(1 << PB5);  // Wyczyść bit 5
PORTB ^= (1 << PB5);   // Przełącz bit 5
```

### Memory-mapped I/O
```c
// ARM Cortex-M - dostęp do rejestrów przez wskaźniki
#define GPIOA_BASE    0x40020000
#define GPIOA_MODER   *((volatile uint32_t*)(GPIOA_BASE + 0x00))
#define GPIOA_ODR     *((volatile uint32_t*)(GPIOA_BASE + 0x14))

// Konfiguracja pin 5 jako wyjście
GPIOA_MODER |= (1 << 10);  // Bit 10 dla pin 5 mode
GPIOA_ODR |= (1 << 5);     // Ustaw pin 5
```

## Układy peryferyjne mikrokontrolerów

### Timer/Counter
- **Funkcje**: Pomiar czasu, PWM, zliczanie zdarzeń
- **Tryby**: Normal, CTC (Clear Timer on Compare), Fast PWM

```c
// AVR Timer dla PWM
void setup_pwm() {
    DDRB |= (1 << PB3);        // Pin OC2A jako wyjście
    TCCR2A |= (1 << WGM21) | (1 << WGM20); // Fast PWM mode
    TCCR2A |= (1 << COM2A1);   // Clear OC2A on compare
    TCCR2B |= (1 << CS22);     // Prescaler 64
    OCR2A = 128;               // 50% duty cycle
}
```

### ADC (Analog-to-Digital Converter)
```c
// Inicjalizacja ADC
void adc_init() {
    ADMUX |= (1 << REFS0);     // AVcc reference
    ADCSRA |= (1 << ADEN);     // Enable ADC
    ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Prescaler 128
}

uint16_t adc_read(uint8_t channel) {
    ADMUX = (ADMUX & 0xF0) | (channel & 0x0F); // Select channel
    ADCSRA |= (1 << ADSC);     // Start conversion
    while(ADCSRA & (1 << ADSC)); // Wait for completion
    return ADC;
}
```

### Watchdog Timer
```c
#include <avr/wdt.h>

void setup() {
    wdt_enable(WDTO_2S);  // 2 sekundy timeout
}

void loop() {
    // Główny kod programu
    wdt_reset();  // Reset watchdog timer
    delay(1000);
}
```

## Bootloader i programowanie

### Bootloader w mikrokontrolerach
- **Funkcja**: Kod uruchamiany przy starcie, ładuje główny program
- **Lokalizacja**: Specjalny obszar flash memory
- **Arduino bootloader**: Optiboot (~512B)

### Metody programowania

#### ISP (In-System Programming)
```bash
# avrdude - programowanie przez ISP
avrdude -c usbasp -p atmega328p -U flash:w:program.hex:i
```

#### JTAG Debugging
```bash
# OpenOCD dla ARM
openocd -f interface/stlink-v2.cfg -f target/stm32f4x.cfg
```

#### Bootloader programming
```cpp
// Arduino-style bootloader update
// Komunikacja przez UART/USB
```

## Zarządzanie energią w mikrokontrolerach

### Sleep modes AVR
```c
#include <avr/sleep.h>
#include <avr/power.h>

void enter_sleep() {
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    power_adc_disable();
    power_spi_disable();
    power_timer0_disable();
    sleep_enable();
    sleep_cpu();
    sleep_disable();  // Wykonane po przebudzeniu
}
```

### Power management ARM Cortex-M
```c
// STM32 Low Power modes
HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_STOPENTRY_WFI);
```

## System przerwań

### Interrupt Vector Table
```c
// AVR interrupt example
#include <avr/interrupt.h>

ISR(TIMER1_OVF_vect) {
    // Timer1 overflow interrupt
    PORTB ^= (1 << PB5);  // Toggle LED
}

void setup_timer_interrupt() {
    TCCR1B |= (1 << CS12);  // Prescaler 256
    TIMSK1 |= (1 << TOIE1); // Enable overflow interrupt
    sei();                  // Enable global interrupts
}
```

### ARM NVIC (Nested Vectored Interrupt Controller)
```c
// STM32 interrupt example
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if(GPIO_Pin == GPIO_PIN_0) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
}
```

## Real-Time Operating Systems (RTOS)

### FreeRTOS na mikrokontrolerach
```c
#include "FreeRTOS.h"
#include "task.h"

void led_task(void *pvParameters) {
    while(1) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}

int main() {
    xTaskCreate(led_task, "LED", 128, NULL, 1, NULL);
    vTaskStartScheduler();
    return 0;
}
```

## Narzędzia rozwojowe

### IDE i kompilatory
- **Arduino IDE**: Prostota, duża społeczność
- **PlatformIO**: Profesjonalne środowisko, multi-platform
- **STM32CubeIDE**: Oficjalne IDE dla STM32
- **MPLAB X**: Microchip PIC development

### Debugowanie
- **Serial debugging**: Printf przez UART
- **JTAG/SWD**: Hardware debugging
- **Logic analyzer**: Analiza sygnałów cyfrowych
- **Oscilloscope**: Analiza sygnałów analogowych

## Powiązane tematy
- [[arduino_podstawy|Arduino - Podstawy]]
- [[raspberry_pi|Raspberry Pi]]
- [[io_cyfrowe_analogowe|Wejścia/Wyjścia Cyfrowe i Analogowe]]
- [[protokoly_komunikacyjne|Protokoły Komunikacyjne]]
- [[embedded_programming|Programowanie Embedded]]
- [[memory_management|Zarządzanie Pamięcią w Embedded]]