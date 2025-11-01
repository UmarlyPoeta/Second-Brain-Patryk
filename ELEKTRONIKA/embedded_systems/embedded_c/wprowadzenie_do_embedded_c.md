# Wprowadzenie do Embedded C

## Czym jest Embedded C?

Embedded C to podzbiór języka C wykorzystywany do programowania systemów wbudowanych - małych komputerów zintegrowanych z urządzeniami elektronicznymi. Jest to język programowania niskopoziomowego, który daje programiście bezpośredni dostęp do sprzętu.

## Historia

- **1972** - Dennis Ritchie tworzy język C w Bell Labs
- **Lata 80** - C staje się popularny w systemach wbudowanych
- **Dzisiaj** - Embedded C dominuje w programowaniu mikrokontrolerów

## Dlaczego Embedded C?

### Zalety
- ✅ **Wydajność** - kod bliski maszynowemu, minimalny narzut
- ✅ **Kontrola** - bezpośredni dostęp do rejestrów sprzętowych
- ✅ **Przenośność** - dostępne kompilatory dla większości architektur
- ✅ **Dojrzałość** - ogromna baza wiedzy i bibliotek
- ✅ **Rozmiar** - małe footprint kodu
- ✅ **Przewidywalność** - deterministyczne zachowanie

### Wady
- ❌ Brak wysokopoziomowych abstrakcji
- ❌ Wymaga dobrej znajomości sprzętu
- ❌ Łatwo popełnić błędy związane z pamięcią
- ❌ Brak automatycznego zarządzania zasobami

## Podstawowe cechy Embedded C

### 1. Deterministyczne wykonanie
```c
// Kod musi wykonywać się w przewidywalnym czasie
void handle_critical_task(void) {
    // Ta funkcja MUSI zakończyć się w < 10 µs
    GPIO_PORT->ODR ^= (1 << LED_PIN);  // Toggle LED
}
```

### 2. Ograniczone zasoby
```c
// Typowy mikrokontroler: 64KB Flash, 20KB RAM
#define MAX_BUFFER_SIZE 256  // Nie 256000!

static uint8_t buffer[MAX_BUFFER_SIZE];  // Oszczędne użycie RAM
```

### 3. Bezpośredni dostęp do sprzętu
```c
// Dostęp do rejestrów sprzętowych
#define GPIO_BASE 0x40020000
#define GPIOA_MODER (*(volatile uint32_t*)(GPIO_BASE + 0x00))

// Ustawienie pinu jako wyjście
GPIOA_MODER |= (1 << 0);
```

### 4. Programowanie sterowane przerwaniami
```c
void USART1_IRQHandler(void) {
    if (USART1->SR & USART_SR_RXNE) {
        char received = USART1->DR;
        process_data(received);
    }
}
```

## Typowa struktura projektu Embedded C

```
projekt/
├── src/
│   ├── main.c          # Główny plik programu
│   ├── gpio.c          # Obsługa GPIO
│   ├── uart.c          # Komunikacja UART
│   └── timer.c         # Obsługa timerów
├── inc/
│   ├── main.h
│   ├── gpio.h
│   ├── uart.h
│   └── timer.h
├── startup/
│   └── startup.c       # Kod startowy
├── linker/
│   └── memory.ld       # Skrypt linkera
└── Makefile
```

## Pierwszy program - "Blink LED"

```c
#include <stdint.h>

// Definicje adresów (przykład dla STM32)
#define RCC_AHB1ENR   (*(volatile uint32_t*)0x40023830)
#define GPIOA_MODER   (*(volatile uint32_t*)0x40020000)
#define GPIOA_ODR     (*(volatile uint32_t*)0x40020014)

#define LED_PIN 5

void delay(volatile uint32_t count) {
    while(count--);
}

int main(void) {
    // Włącz taktowanie GPIOA
    RCC_AHB1ENR |= (1 << 0);
    
    // Skonfiguruj pin jako wyjście
    GPIOA_MODER &= ~(3 << (LED_PIN * 2));  // Wyczyść bity
    GPIOA_MODER |= (1 << (LED_PIN * 2));   // Ustaw jako output
    
    while(1) {
        GPIOA_ODR ^= (1 << LED_PIN);  // Przełącz LED
        delay(500000);                 // Opóźnienie
    }
    
    return 0;  // Nigdy nie osiągniemy tego punktu
}
```

## Różnice od standardowego C

| Aspekt | Standardowy C | Embedded C |
|--------|--------------|------------|
| Dynamiczna alokacja | malloc/free często używane | Rzadko lub wcale |
| Biblioteka standardowa | Pełna libc | Ograniczona lub brak |
| Funkcja main() | Może zwrócić wartość | Zazwyczaj nieskończona pętla |
| Floating point | Standardowe | Często unikane (wolne) |
| Rekurencja | Akceptowalna | Unikana (stack overflow) |

## Kompilacja kodu Embedded C

```bash
# Kompilacja dla ARM Cortex-M4
arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -O2 \
    -Wall -Wextra \
    -c main.c -o main.o

# Linkowanie
arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb \
    -T linker_script.ld \
    main.o startup.o -o firmware.elf

# Konwersja do formatu hex/bin
arm-none-eabi-objcopy -O ihex firmware.elf firmware.hex
arm-none-eabi-objcopy -O binary firmware.elf firmware.bin
```

## Narzędzia programisty Embedded C

### Kompilatory
- **GCC ARM** - arm-none-eabi-gcc (darmowy)
- **Keil MDK** - armcc (komercyjny)
- **IAR** - iccarm (komercyjny)
- **AVR-GCC** - dla mikrokontrolerów AVR

### IDE
- STM32CubeIDE
- Keil µVision
- IAR Embedded Workbench
- Eclipse + plugins
- Visual Studio Code + extensions

### Debuggery
- GDB (GNU Debugger)
- OpenOCD
- SEGGER J-Link
- ST-Link

## Co dalej?

Po opanowaniu podstaw, kolejne kroki to:
1. [[typy_danych_embedded_c|Typy danych w Embedded C]]
2. [[operatory_bitowe|Operacje bitowe]]
3. [[wskazniki_adresowanie|Wskaźniki i adresowanie pamięci]]

## Ćwiczenia

1. **Podstawowe**: Napisz program migający LED-em z różnymi częstotliwościami
2. **Średnie**: Stwórz sekwencję świecenia wielu LED-ów
3. **Zaawansowane**: Zaimplementuj efekt "Knight Rider" z 8 LED-ami

## Przydatne linki
- [[roznice_c_embedded_c|Różnice między C a Embedded C]]
- [[embedded_programming|Programowanie Embedded]]
- [[embedded_systems_index|Systemy wbudowane - indeks]]
