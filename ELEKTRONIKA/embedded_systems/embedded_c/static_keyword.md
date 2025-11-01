# Słowo kluczowe static w Embedded C

## Wprowadzenie

`static` to wielofunkcyjne słowo kluczowe w C, które ma różne znaczenia w zależności od kontekstu. W programowaniu embedded jest kluczowe dla zarządzania pamięcią i organizacji kodu.

## Trzy znaczenia static

### 1. Static w zmiennych lokalnych
Zmienna zachowuje wartość między wywołaniami funkcji.

```c
uint32_t count_calls(void) {
    static uint32_t counter = 0;  // Inicjalizowana tylko raz
    counter++;
    return counter;
}

// Wywołania:
count_calls();  // Zwraca 1
count_calls();  // Zwraca 2
count_calls();  // Zwraca 3
```

### 2. Static w zmiennych globalnych
Ogranicza widoczność do jednego pliku (internal linkage).

```c
// W pliku sensor.c
static uint16_t sensor_reading = 0;  // Widoczne tylko w sensor.c

void update_sensor(void) {
    sensor_reading = adc_read();
}
```

### 3. Static w funkcjach
Funkcja widoczna tylko w jednym pliku.

```c
// W pliku driver.c
static void internal_init(void) {
    // Pomocnicza funkcja - nie eksportowana
}

void public_init(void) {
    internal_init();  // OK w tym samym pliku
}
```

## Static w zmiennych lokalnych

### Trwałość między wywołaniami
```c
void toggle_led(void) {
    static bool state = false;
    
    state = !state;
    
    if(state) {
        LED_ON();
    } else {
        LED_OFF();
    }
}

// Każde wywołanie przełącza LED
```

### Liczniki i filtry
```c
uint16_t moving_average(uint16_t new_value) {
    static uint32_t sum = 0;
    static uint16_t buffer[8] = {0};
    static uint8_t index = 0;
    
    // Usuń najstarszą wartość z sumy
    sum -= buffer[index];
    
    // Dodaj nową wartość
    buffer[index] = new_value;
    sum += new_value;
    
    // Przesuń indeks
    index = (index + 1) % 8;
    
    return sum / 8;
}
```

### State machines
```c
void state_machine(void) {
    static state_t current_state = STATE_INIT;
    
    switch(current_state) {
        case STATE_INIT:
            if(init_complete()) {
                current_state = STATE_RUNNING;
            }
            break;
            
        case STATE_RUNNING:
            if(error_detected()) {
                current_state = STATE_ERROR;
            }
            break;
            
        case STATE_ERROR:
            handle_error();
            current_state = STATE_INIT;
            break;
    }
}
```

## Static w zmiennych globalnych

### Enkapsulacja danych modułu
```c
// uart.c
static uint8_t tx_buffer[256];
static volatile uint16_t tx_head = 0;
static volatile uint16_t tx_tail = 0;

// Funkcje publiczne do dostępu
bool uart_send_byte(uint8_t byte) {
    uint16_t next_head = (tx_head + 1) % 256;
    if(next_head == tx_tail) {
        return false;  // Bufor pełny
    }
    
    tx_buffer[tx_head] = byte;
    tx_head = next_head;
    return true;
}
```

### Ukrywanie szczegółów implementacji
```c
// driver.c
static const uint32_t MAGIC_NUMBER = 0xDEADBEEF;
static volatile bool initialized = false;

void driver_init(void) {
    if(!initialized) {
        // Użycie MAGIC_NUMBER
        initialized = true;
    }
}

// MAGIC_NUMBER i initialized nie są widoczne z innych plików
```

## Static w funkcjach

### Funkcje pomocnicze
```c
// spi.c

// Funkcja publiczna (w .h)
void spi_transfer(uint8_t *data, uint16_t length);

// Funkcje prywatne (tylko w .c)
static void cs_low(void) {
    GPIO_RESET(SPI_CS_PIN);
}

static void cs_high(void) {
    GPIO_SET(SPI_CS_PIN);
}

static void spi_wait_ready(void) {
    while(!(SPI1->SR & SPI_SR_TXE));
}

// Implementacja publiczna używa prywatnych
void spi_transfer(uint8_t *data, uint16_t length) {
    cs_low();
    
    for(uint16_t i = 0; i < length; i++) {
        spi_wait_ready();
        SPI1->DR = data[i];
    }
    
    cs_high();
}
```

### Inline static functions
```c
// W pliku .c
static inline uint32_t read_register(volatile uint32_t *reg) {
    return *reg;
}

static inline void write_register(volatile uint32_t *reg, uint32_t value) {
    *reg = value;
}

// Kompilator może zinlinować te funkcje
void gpio_set_pin(uint8_t pin) {
    uint32_t reg = read_register(&GPIOA->ODR);
    reg |= (1 << pin);
    write_register(&GPIOA->ODR, reg);
}
```

## Static a pamięć

### Alokacja pamięci
```c
void function(void) {
    // Normalna zmienna lokalna - na stosie
    uint32_t local_var = 0;  
    
    // Static - w sekcji .data/.bss (nie na stosie!)
    static uint32_t static_var = 0;
}
```

### Inicjalizacja static
```c
// Static z inicjalizacją - w sekcji .data
static uint32_t initialized_var = 100;

// Static bez inicjalizacji - w sekcji .bss (zerowana)
static uint32_t uninitialized_var;

// const static - w sekcji .rodata (Flash)
static const uint32_t const_var = 200;
```

## Wzorce użycia w embedded

### Singleton pattern
```c
// device.c
typedef struct {
    bool initialized;
    uint32_t config;
    volatile uint32_t status;
} device_t;

static device_t device_instance;  // Jedna instancja

device_t* device_get_instance(void) {
    return &device_instance;
}

void device_init(void) {
    device_instance.initialized = true;
    device_instance.config = 0;
}
```

### Moduł z private state
```c
// pwm.c
static uint32_t current_duty_cycle = 0;
static uint32_t current_frequency = 1000;

static void update_hardware(void) {
    // Aktualizacja rejestrów sprzętowych
    TIM2->ARR = 1000000 / current_frequency;
    TIM2->CCR1 = (TIM2->ARR * current_duty_cycle) / 100;
}

void pwm_set_duty_cycle(uint8_t duty) {
    if(duty <= 100) {
        current_duty_cycle = duty;
        update_hardware();
    }
}

void pwm_set_frequency(uint32_t freq) {
    if(freq > 0 && freq <= 100000) {
        current_frequency = freq;
        update_hardware();
    }
}
```

### Bufory komunikacyjne
```c
// uart.c
#define BUFFER_SIZE 256

static uint8_t rx_buffer[BUFFER_SIZE];
static volatile uint16_t rx_head = 0;
static volatile uint16_t rx_tail = 0;

static uint8_t tx_buffer[BUFFER_SIZE];
static volatile uint16_t tx_head = 0;
static volatile uint16_t tx_tail = 0;

// Funkcje publiczne do zarządzania buforami
bool uart_rx_available(void) {
    return (rx_head != rx_tail);
}

uint8_t uart_read_byte(void) {
    uint8_t byte = rx_buffer[rx_tail];
    rx_tail = (rx_tail + 1) % BUFFER_SIZE;
    return byte;
}

void UART_IRQHandler(void) {
    if(USART1->SR & USART_SR_RXNE) {
        rx_buffer[rx_head] = USART1->DR;
        rx_head = (rx_head + 1) % BUFFER_SIZE;
    }
}
```

## Static vs extern

```c
// ===== config.c =====
// Widoczne tylko w config.c
static uint32_t internal_setting = 100;

// Widoczne globalnie (trzeba zadeklarować extern w .h)
uint32_t public_setting = 200;

// ===== config.h =====
extern uint32_t public_setting;
// Nie ma extern dla internal_setting - nie jest dostępne!

// ===== main.c =====
#include "config.h"

void test(void) {
    public_setting = 300;     // OK
    internal_setting = 150;   // BŁĄD - niewidoczne
}
```

## Static inline functions

### Małe, często wywoływane funkcje
```c
// W pliku .h (dla inline)
static inline void gpio_set(uint8_t pin) {
    GPIOA->BSRR = (1 << pin);
}

static inline void gpio_reset(uint8_t pin) {
    GPIOA->BSRR = (1 << (pin + 16));
}

static inline bool gpio_read(uint8_t pin) {
    return (GPIOA->IDR & (1 << pin)) != 0;
}

// Kompilator inline'uje te funkcje w miejscu wywołania
// Brak overhead wywołania funkcji
```

## Dobre praktyki

### 1. Ukrywaj implementację
```c
// ❌ ŹLE - wszystko globalne
uint8_t buffer[256];
uint16_t index;

// ✅ DOBRZE - szczegóły ukryte
static uint8_t buffer[256];
static uint16_t index;

// API publiczne
void buffer_add(uint8_t byte);
uint8_t buffer_get(void);
```

### 2. Redukuj coupling
```c
// Każdy moduł ma własny static state
// Komunikacja tylko przez publiczne funkcje

// sensor.c
static uint16_t sensor_value;

uint16_t sensor_read(void) {
    return sensor_value;
}

// display.c  
static uint16_t last_value;

void display_update(void) {
    uint16_t new_value = sensor_read();  // Przez API
    if(new_value != last_value) {
        // Aktualizuj display
        last_value = new_value;
    }
}
```

### 3. Zmienne static const dla lookup tables
```c
static const uint8_t crc_table[256] = {
    0x00, 0x07, 0x0E, 0x09, // ...
};

static uint8_t calculate_crc(const uint8_t *data, uint16_t len) {
    uint8_t crc = 0;
    for(uint16_t i = 0; i < len; i++) {
        crc = crc_table[crc ^ data[i]];
    }
    return crc;
}
```

## Rozmiar kodu - static functions

```c
// Funkcja używana w wielu miejscach
static void delay_us(uint32_t us) {
    for(volatile uint32_t i = 0; i < us * 10; i++);
}

// Kompilator może:
// 1. Zinlinować ją (duplikacja kodu, szybsze)
// 2. Stworzyć jedną kopię (mniejszy kod, call overhead)
// 3. Usunąć jeśli nieużywana (optymalizacja)

// Z static kompilator ma więcej informacji do optymalizacji
```

## Przykład kompleksowy - Moduł ADC

```c
// adc_driver.c

#define ADC_CHANNELS 4
#define SAMPLES_PER_CHANNEL 8

// Private state
static uint16_t adc_buffer[ADC_CHANNELS][SAMPLES_PER_CHANNEL];
static uint8_t current_sample = 0;
static volatile bool conversion_complete = false;

// Private functions
static void start_conversion(void) {
    ADC1->CR2 |= ADC_CR2_SWSTART;
}

static uint16_t get_average(uint8_t channel) {
    uint32_t sum = 0;
    for(uint8_t i = 0; i < SAMPLES_PER_CHANNEL; i++) {
        sum += adc_buffer[channel][i];
    }
    return sum / SAMPLES_PER_CHANNEL;
}

// Public API
void adc_init(void) {
    // Konfiguracja ADC
    RCC->APB2ENR |= RCC_APB2ENR_ADC1EN;
    ADC1->CR1 = ADC_CR1_SCAN;
    ADC1->CR2 = ADC_CR2_ADON | ADC_CR2_DMA;
    
    // Wyzeruj bufory
    for(uint8_t ch = 0; ch < ADC_CHANNELS; ch++) {
        for(uint8_t s = 0; s < SAMPLES_PER_CHANNEL; s++) {
            adc_buffer[ch][s] = 0;
        }
    }
}

uint16_t adc_read_channel(uint8_t channel) {
    if(channel < ADC_CHANNELS) {
        return get_average(channel);
    }
    return 0;
}

// Przerwanie ADC
void ADC_IRQHandler(void) {
    if(ADC1->SR & ADC_SR_EOC) {
        for(uint8_t ch = 0; ch < ADC_CHANNELS; ch++) {
            adc_buffer[ch][current_sample] = ADC1->DR;
        }
        
        current_sample = (current_sample + 1) % SAMPLES_PER_CHANNEL;
        conversion_complete = true;
    }
}
```

## Podsumowanie

### Używaj static dla:
- ✅ Zmiennych lokalnych zachowujących stan
- ✅ Zmiennych globalnych prywatnych dla modułu
- ✅ Funkcji pomocniczych (nie w API)
- ✅ Buforów wewnętrznych modułu
- ✅ State machine states
- ✅ Lookup tables w module

### Korzyści:
- 🔒 Enkapsulacja - ukrycie implementacji
- 🎯 Zmniejszenie coupling między modułami
- ⚡ Lepsze możliwości optymalizacji
- 📦 Unikanie konfliktów nazw
- 🐛 Łatwiejsze debugowanie (znany scope)

### Pamiętaj:
- Static zmienne lokalne NIE są na stosie
- Static zmienne są inicjalizowane tylko raz
- Static funkcje mogą być zinlinowane
- Static ogranicza widoczność do pliku

## Powiązane tematy
- [[const_keyword|Słowo kluczowe const]]
- [[volatile_keyword|Słowo kluczowe volatile]]
- [[optymalizacja_pamieci|Optymalizacja wykorzystania pamięci]]
- [[dobre_praktyki_embedded_c|Dobre praktyki w Embedded C]]
