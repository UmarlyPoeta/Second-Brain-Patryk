# STM32F429I - Bare Metal - Startup Code i Inicjalizacja

## 🚀 Co Się Dzieje Po Włączeniu Zasilania?

### Sekwencja Startu Mikrokontrolera

```
1. Zasilanie włączone
   ↓
2. Hardware reset
   ↓
3. Cortex-M4 czyta Vector Table z adresu 0x00000000
   ↓
4. Ładuje Stack Pointer (SP) z pierwszego wpisu
   ↓
5. Ładuje Program Counter (PC) z drugiego wpisu (Reset_Handler)
   ↓
6. Rozpoczyna wykonywanie Reset_Handler
   ↓
7. Reset_Handler kopiuje .data z Flash do RAM
   ↓
8. Reset_Handler zeruje .bss w RAM
   ↓
9. Reset_Handler wywołuje SystemInit()
   ↓
10. Reset_Handler wywołuje main()
   ↓
11. Program użytkownika działa
```

## 📋 Vector Table - Tablica Wektorów Przerwań

### Czym Jest Vector Table?

```
Vector Table to tablica adresów funkcji obsługi przerwań.
Znajduje się na początku pamięci Flash (adres 0x08000000).

Po resecie, mikrokontroler:
1. Czyta adres z pozycji 0 -> Stack Pointer
2. Czyta adres z pozycji 4 -> Reset_Handler
3. Skacze do Reset_Handler

Struktura Vector Table:
Offset  | Nazwa              | Opis
--------|--------------------|---------------------------------
0x0000  | Stack Pointer      | Początkowy SP (top of stack)
0x0004  | Reset              | Adres Reset_Handler
0x0008  | NMI                | Non-Maskable Interrupt
0x000C  | HardFault          | Hard Fault handler
0x0010  | MemManage          | Memory Management Fault
0x0014  | BusFault           | Bus Fault
0x0018  | UsageFault         | Usage Fault
...     | ...                | ...
0x0058  | SysTick            | System Tick Timer
0x005C  | WWDG               | Window Watchdog
0x0060  | PVD                | PVD through EXTI
0x0064  | TAMP_STAMP         | Tamper and TimeStamp
...     | ...                | ... (łącznie 91 przerwań)
```

### Definiowanie Vector Table w C

```c
/**
 * @brief  Stack size definition
 */
#define STACK_SIZE  0x400  // 1KB stack

/**
 * @brief  Stack allocation (w sekcji .stack)
 */
__attribute__((section(".stack")))
uint8_t stack[STACK_SIZE];

/**
 * @brief  Deklaracje handlerów
 */
void Reset_Handler(void);
void NMI_Handler(void) __attribute__((weak, alias("Default_Handler")));
void HardFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void MemManage_Handler(void) __attribute__((weak, alias("Default_Handler")));
void BusFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void UsageFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SVC_Handler(void) __attribute__((weak, alias("Default_Handler")));
void DebugMon_Handler(void) __attribute__((weak, alias("Default_Handler")));
void PendSV_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SysTick_Handler(void) __attribute__((weak, alias("Default_Handler")));

// External interrupts
void WWDG_IRQHandler(void) __attribute__((weak, alias("Default_Handler")));
void PVD_IRQHandler(void) __attribute__((weak, alias("Default_Handler")));
void TAMP_STAMP_IRQHandler(void) __attribute__((weak, alias("Default_Handler")));
void USART1_IRQHandler(void) __attribute__((weak, alias("Default_Handler")));
// ... więcej przerwań

/**
 * @brief  Default handler - infinite loop
 */
void Default_Handler(void)
{
    while (1) {
        // Trap - przerwanie którego nie obsługujemy
    }
}

/**
 * @brief  Vector table definition
 * 
 * __attribute__((section(".isr_vector"))) - umieść w specjalnej sekcji
 * która będzie na początku Flash
 */
__attribute__((section(".isr_vector")))
void (* const vector_table[])(void) = {
    // Cortex-M4 System Exceptions
    (void (*)(void))((uint32_t)stack + STACK_SIZE),  // Initial Stack Pointer
    Reset_Handler,              // Reset Handler
    NMI_Handler,                // NMI Handler
    HardFault_Handler,          // Hard Fault Handler
    MemManage_Handler,          // MPU Fault Handler
    BusFault_Handler,           // Bus Fault Handler
    UsageFault_Handler,         // Usage Fault Handler
    0,                          // Reserved
    0,                          // Reserved
    0,                          // Reserved
    0,                          // Reserved
    SVC_Handler,                // SVCall Handler
    DebugMon_Handler,           // Debug Monitor Handler
    0,                          // Reserved
    PendSV_Handler,             // PendSV Handler
    SysTick_Handler,            // SysTick Handler
    
    // External Interrupts
    WWDG_IRQHandler,            // Window WatchDog
    PVD_IRQHandler,             // PVD through EXTI Line detection
    TAMP_STAMP_IRQHandler,      // Tamper and TimeStamps
    // ... dodaj wszystkie 91 przerwań
};
```

## 🔧 Reset_Handler - Serce Startu

### Co Robi Reset_Handler?

```c
/**
 * @brief  Reset Handler - pierwsza wykonywana funkcja
 * 
 * Zadania:
 * 1. Kopiuj .data z Flash do RAM
 * 2. Wyzeruj .bss w RAM
 * 3. Wywołaj SystemInit() (opcjonalnie)
 * 4. Wywołaj main()
 */

// Symbole definiowane w linker script
extern uint32_t _sdata;     // Start adres .data w RAM
extern uint32_t _edata;     // End adres .data w RAM
extern uint32_t _sidata;    // Start adres .data w Flash (load address)
extern uint32_t _sbss;      // Start adres .bss
extern uint32_t _ebss;      // End adres .bss

void Reset_Handler(void)
{
    uint32_t *src, *dest;
    
    // KROK 1: Kopiuj .data z Flash do RAM
    // .data zawiera zmienne globalne z wartościami początkowymi
    // np: int x = 42; <- to musi być skopiowane z Flash
    
    src = &_sidata;   // Źródło w Flash
    dest = &_sdata;   // Cel w RAM
    
    while (dest < &_edata) {
        *dest++ = *src++;
    }
    
    // KROK 2: Wyzeruj .bss
    // .bss zawiera zmienne globalne bez wartości początkowych
    // np: int y; <- to musi być wyzerowane
    
    dest = &_sbss;
    while (dest < &_ebss) {
        *dest++ = 0;
    }
    
    // KROK 3: Opcjonalnie - SystemInit()
    // Inicjalizacja zegara, FPU, cache, etc.
    #ifdef USE_SYSTEM_INIT
    SystemInit();
    #endif
    
    // KROK 4: Wywołaj main()
    main();
    
    // Jeśli main() kiedykolwiek zwróci (nie powinien!)
    while (1);
}
```

### Szczegółowe Wyjaśnienie .data i .bss

```c
/**
 * @brief  Przykłady zmiennych w różnych sekcjach
 */

// SEKCJA .data - zmienne z wartością początkową
int initialized_var = 42;           // w .data (Flash -> RAM)
const char message[] = "Hello";     // w .rodata (Flash, read-only)
static int static_var = 100;        // w .data

// SEKCJA .bss - zmienne bez wartości początkowej (zerowane)
int uninitialized_var;              // w .bss (wyzerowane)
static int static_uninit;           // w .bss
int array[100];                     // w .bss (400 bajtów wyzerowane)

// SEKCJA .rodata - stałe (const)
const int constant = 123;           // w .rodata (Flash)
const char *const string = "Text";  // w .rodata

/**
 * @brief  Dlaczego rozróżniamy .data i .bss?
 * 
 * OSZCZĘDNOŚĆ PAMIĘCI FLASH:
 * 
 * int array[1000] = {0};  <- .data, wymaga 4000 bajtów w Flash!
 * int array[1000];        <- .bss, wymaga 0 bajtów w Flash! (tylko zerowanie w RAM)
 * 
 * Dlatego .bss oszczędza miejsce w Flash.
 */
```

## 📜 Linker Script - Definiowanie Layoutu Pamięci

### Podstawowy Linker Script

```ld
/**
 * @brief  STM32F429ZI Linker Script
 * 
 * Plik: STM32F429ZI_FLASH.ld
 */

/* Punkty wejścia */
ENTRY(Reset_Handler)

/* Definicja pamięci */
MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 2048K
    RAM (rwx)   : ORIGIN = 0x20000000, LENGTH = 192K
    CCMRAM (rw) : ORIGIN = 0x10000000, LENGTH = 64K
}

/* Definicja sekcji */
SECTIONS
{
    /* Vector table na początku Flash */
    .isr_vector : {
        . = ALIGN(4);
        KEEP(*(.isr_vector))   /* Vector table */
        . = ALIGN(4);
    } > FLASH
    
    /* Kod programu */
    .text : {
        . = ALIGN(4);
        *(.text)               /* Kod funkcji */
        *(.text*)
        *(.rodata)             /* Stałe (const) */
        *(.rodata*)
        . = ALIGN(4);
        _etext = .;            /* End of code */
    } > FLASH
    
    /* Dane z wartościami początkowymi */
    .data : {
        . = ALIGN(4);
        _sdata = .;            /* Start of .data w RAM */
        *(.data)
        *(.data*)
        . = ALIGN(4);
        _edata = .;            /* End of .data w RAM */
    } > RAM AT > FLASH
    
    /* Load address .data w Flash */
    _sidata = LOADADDR(.data);
    
    /* Dane bez wartości (zerowane) */
    .bss : {
        . = ALIGN(4);
        _sbss = .;             /* Start of .bss */
        *(.bss)
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        _ebss = .;             /* End of .bss */
    } > RAM
    
    /* Stack */
    .stack : {
        . = ALIGN(8);
        . = . + 0x400;         /* 1KB stack */
        _estack = .;
    } > RAM
    
    /* Heap (opcjonalny) */
    .heap : {
        . = ALIGN(4);
        _sheap = .;
        . = . + 0x200;         /* 512B heap */
        _eheap = .;
    } > RAM
}
```

### Wyjaśnienie Linker Script

```
MEMORY:
- Definiuje dostępne obszary pamięci
- FLASH: 2MB @ 0x08000000 (rx = read, execute)
- RAM: 192KB @ 0x20000000 (rwx = read, write, execute)

SECTIONS:
.isr_vector -> początek FLASH (0x08000000)
  - Vector Table musi być na początku!

.text -> FLASH po .isr_vector
  - Kod programu
  - Stałe (const)

.data -> RAM, ale load address w FLASH
  - Zmienne z wartościami początkowymi
  - Muszą być skopiowane z Flash do RAM przez Reset_Handler
  - "AT > FLASH" oznacza "ładuj z Flash"

.bss -> RAM
  - Zmienne bez wartości
  - Zerowane przez Reset_Handler
  
.stack -> RAM
  - Stack dla programu
  - Rośnie w dół

.heap -> RAM (opcjonalny)
  - Dla malloc(), free()
```

## 🎯 Kompletny Minimalny Projekt Bare Metal

### Struktura Plików

```
projekt/
├── startup.c          # Vector table, Reset_Handler
├── main.c             # Kod aplikacji
├── system.c           # SystemInit(), clock config
├── STM32F429.ld       # Linker script
└── Makefile           # Kompilacja
```

### startup.c

```c
/**
 * @file   startup.c
 * @brief  Startup code dla STM32F429
 */

#include <stdint.h>

// Stack definition
#define STACK_SIZE  0x400
__attribute__((section(".stack")))
uint8_t stack[STACK_SIZE];

// Symbole z linker script
extern uint32_t _sdata, _edata, _sidata;
extern uint32_t _sbss, _ebss;

// Funkcje zewnętrzne
extern int main(void);
extern void SystemInit(void);

// Deklaracje handlerów
void Reset_Handler(void);
void Default_Handler(void);

// Weak aliases
void NMI_Handler(void) __attribute__((weak, alias("Default_Handler")));
void HardFault_Handler(void) __attribute__((weak, alias("Default_Handler")));
void SysTick_Handler(void) __attribute__((weak, alias("Default_Handler")));
void USART1_IRQHandler(void) __attribute__((weak, alias("Default_Handler")));
// ... więcej

// Vector table
__attribute__((section(".isr_vector")))
void (* const vector_table[])(void) = {
    (void (*)(void))((uint32_t)stack + STACK_SIZE),
    Reset_Handler,
    NMI_Handler,
    HardFault_Handler,
    // ... pełna tablica (91 wektorów)
};

// Reset Handler implementation
void Reset_Handler(void)
{
    uint32_t *src = &_sidata;
    uint32_t *dest = &_sdata;
    
    // Copy .data
    while (dest < &_edata) {
        *dest++ = *src++;
    }
    
    // Zero .bss
    dest = &_sbss;
    while (dest < &_ebss) {
        *dest++ = 0;
    }
    
    // System init
    SystemInit();
    
    // Call main
    main();
    
    // Trap
    while (1);
}

// Default handler
void Default_Handler(void)
{
    while (1);
}
```

### main.c

```c
/**
 * @file   main.c
 * @brief  Główny program - LED blink bare metal
 */

#include <stdint.h>

// Definicje z poprzednich notatek
#define RCC_BASE    0x40023800UL
#define GPIOA_BASE  0x40020000UL

typedef struct {
    volatile uint32_t MODER;
    volatile uint32_t OTYPER;
    volatile uint32_t OSPEEDR;
    volatile uint32_t PUPDR;
    volatile uint32_t IDR;
    volatile uint32_t ODR;
    volatile uint32_t BSRR;
    volatile uint32_t LCKR;
    volatile uint32_t AFR[2];
} GPIO_TypeDef;

typedef struct {
    volatile uint32_t CR;
    volatile uint32_t PLLCFGR;
    volatile uint32_t CFGR;
    // ... reszta rejestrów
    volatile uint32_t AHB1ENR;
    // ...
} RCC_TypeDef;

#define RCC   ((RCC_TypeDef*)RCC_BASE)
#define GPIOA ((GPIO_TypeDef*)GPIOA_BASE)

void delay_ms(uint32_t ms)
{
    for (uint32_t i = 0; i < ms * 2000; i++) {
        __asm("nop");
    }
}

int main(void)
{
    // Włącz zegar GPIOA
    RCC->AHB1ENR |= (1 << 0);
    
    // PA5 jako output
    GPIOA->MODER &= ~(0x3 << 10);
    GPIOA->MODER |= (0x1 << 10);
    
    // Główna pętla
    while (1) {
        GPIOA->ODR ^= (1 << 5);  // Toggle PA5
        delay_ms(500);
    }
    
    return 0;
}
```

### system.c

```c
/**
 * @file   system.c
 * @brief  System initialization
 */

#include <stdint.h>

#define RCC_BASE    0x40023800UL
#define FLASH_BASE  0x40023C00UL

typedef struct {
    volatile uint32_t CR;
    volatile uint32_t PLLCFGR;
    volatile uint32_t CFGR;
    // ...
} RCC_TypeDef;

#define RCC   ((RCC_TypeDef*)RCC_BASE)
#define FLASH_ACR  (*(volatile uint32_t*)(FLASH_BASE))

void SystemInit(void)
{
    // KROK 1: Włącz FPU (Cortex-M4F)
    // CPACR - Coprocessor Access Control Register
    #define SCB_CPACR  (*(volatile uint32_t*)0xE000ED88UL)
    SCB_CPACR |= (0xF << 20);  // CP10, CP11 Full Access
    
    // KROK 2: Reset RCC do wartości domyślnych
    RCC->CR |= (1 << 0);       // HSION = 1
    RCC->CFGR = 0x00000000;    // Reset CFGR
    RCC->CR &= 0xFEF6FFFFUL;   // Reset HSEON, CSSON, PLLON
    RCC->PLLCFGR = 0x24003010; // Reset value
    
    // KROK 3: Disable all interrupts
    RCC->CIR = 0x00000000;
    
    // KROK 4: Konfiguracja zegara (opcjonalnie)
    // Można pozostać na HSI 16 MHz lub skonfigurować PLL
    // (kod z poprzedniej notatki)
    
    // KROK 5: Włącz instruction & data cache
    FLASH_ACR |= (1 << 9);  // ICEN
    FLASH_ACR |= (1 << 10); // DCEN
    FLASH_ACR |= (1 << 8);  // PRFTEN
}
```

### Makefile

```makefile
# Kompilator i narzędzia
CC = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy
SIZE = arm-none-eabi-size

# Flagi kompilatora
CFLAGS  = -mcpu=cortex-m4
CFLAGS += -mthumb
CFLAGS += -mfloat-abi=hard
CFLAGS += -mfpu=fpv4-sp-d16
CFLAGS += -O2
CFLAGS += -g
CFLAGS += -Wall
CFLAGS += -ffunction-sections
CFLAGS += -fdata-sections

# Flagi linkera
LDFLAGS  = -T STM32F429.ld
LDFLAGS += -Wl,--gc-sections
LDFLAGS += -Wl,-Map=output.map
LDFLAGS += --specs=nosys.specs

# Pliki źródłowe
SRCS = startup.c main.c system.c

# Pliki obiektowe
OBJS = $(SRCS:.c=.o)

# Target
TARGET = firmware

all: $(TARGET).elf $(TARGET).bin

$(TARGET).elf: $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) $^ -o $@
	$(SIZE) $@

$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o *.elf *.bin *.map

flash: $(TARGET).bin
	st-flash write $(TARGET).bin 0x8000000

.PHONY: all clean flash
```

### Kompilacja i Wgrywanie

```bash
# Kompilacja
make

# Wgranie do mikrokontrolera
make flash

# Lub ręcznie przez st-link
st-flash write firmware.bin 0x8000000

# Lub przez OpenOCD
openocd -f interface/stlink-v2.cfg -f target/stm32f4x.cfg \
        -c "program firmware.elf verify reset exit"
```

## 🐛 Debug Startup Problems

### Typowe Błędy

```c
/**
 * @brief  Problem 1: Stack overflow
 * 
 * Objaw: Hard fault, nieoczekiwane resety
 * Przyczyna: Stack za mały
 * Rozwiązanie: Zwiększ STACK_SIZE
 */

// Zbyt mały stack
#define STACK_SIZE  0x100  // 256B - może nie wystarczyć!

// Lepiej
#define STACK_SIZE  0x400  // 1KB
#define STACK_SIZE  0x800  // 2KB dla złożonych programów

/**
 * @brief  Problem 2: Brak kopiowania .data
 * 
 * Objaw: Zmienne globalne mają złe wartości
 * Przyczyna: Reset_Handler nie kopiuje .data
 */

int global_var = 42;  // Oczekujesz 42, dostajesz śmieci

// Rozwiązanie: Upewnij się że Reset_Handler kopiuje .data!

/**
 * @brief  Problem 3: Brak zerowania .bss
 * 
 * Objaw: Niezainicjalizowane zmienne nie są 0
 */

int array[100];  // Oczekujesz zer, dostajesz śmieci

// Rozwiązanie: Reset_Handler musi zerować .bss!

/**
 * @brief  Problem 4: Vector table w złym miejscu
 * 
 * Objaw: Nie startuje, od razu HardFault
 * Przyczyna: Vector table nie jest na początku Flash
 * 
 * Rozwiązanie: Sprawdź linker script - .isr_vector na początku
 */

/**
 * @brief  Problem 5: Złe SP (Stack Pointer)
 * 
 * Objaw: Natychmiastowy crash
 * Przyczyna: Pierwsza wartość w vector table jest zła
 */

// Poprawnie - koniec stosu
(void (*)(void))((uint32_t)stack + STACK_SIZE)

// ŹLE - początek stosu
(void (*)(void))((uint32_t)stack)  // BŁĄD!
```

### HardFault Handler dla Debugowania

```c
/**
 * @brief  Rozbudowany HardFault handler
 * 
 * Wyświetla informacje o crash w debuggerze
 */
void HardFault_Handler(void)
{
    // Rejestry procesora zachowane na stosie
    __asm volatile (
        "TST LR, #4        \n"  // Test bit 2 of LR
        "ITE EQ            \n"  // If-Then-Else
        "MRSEQ R0, MSP     \n"  // Main Stack Pointer
        "MRSNE R0, PSP     \n"  // Process Stack Pointer
        "B HardFault_Handler_C \n"
    );
}

void HardFault_Handler_C(uint32_t *hardfault_args)
{
    // Odczytaj rejestry z stosu
    volatile uint32_t r0  = hardfault_args[0];
    volatile uint32_t r1  = hardfault_args[1];
    volatile uint32_t r2  = hardfault_args[2];
    volatile uint32_t r3  = hardfault_args[3];
    volatile uint32_t r12 = hardfault_args[4];
    volatile uint32_t lr  = hardfault_args[5];  // Link Register
    volatile uint32_t pc  = hardfault_args[6];  // Program Counter (gdzie crash)
    volatile uint32_t psr = hardfault_args[7];  // Program Status Register
    
    // Odczytaj rejestry fault
    #define SCB_HFSR  (*(volatile uint32_t*)0xE000ED2C)
    #define SCB_CFSR  (*(volatile uint32_t*)0xE000ED28)
    #define SCB_BFAR  (*(volatile uint32_t*)0xE000ED38)
    #define SCB_MMFAR (*(volatile uint32_t*)0xE000ED34)
    
    volatile uint32_t hfsr  = SCB_HFSR;   // HardFault Status
    volatile uint32_t cfsr  = SCB_CFSR;   // Configurable Fault Status
    volatile uint32_t bfar  = SCB_BFAR;   // Bus Fault Address
    volatile uint32_t mmfar = SCB_MMFAR;  // MemManage Fault Address
    
    // Ustaw breakpoint tutaj i sprawdź zmienne w debuggerze
    while (1);
}
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_podstawy|Bare Metal - Podstawy]]
- [[stm32f429i_bare_metal_clock|Bare Metal - System zegarowy]]
- [[stm32f429i_bare_metal_nvic|Bare Metal - NVIC i przerwania]]
- [[stm32f429i_debugging|Debugowanie STM32]]

## 📝 Podsumowanie

### Kluczowe Koncepty

1. **Vector Table** - Tablica adresów handlerów na początku Flash
2. **Reset_Handler** - Pierwsza funkcja, kopiuje .data, zeruje .bss, wywołuje main()
3. **Linker Script** - Definiuje layout pamięci i sekcji
4. **Stack** - Rośnie w dół, musi być wystarczająco duży
5. **.data** - Zmienne z wartościami początkowymi (Flash → RAM)
6. **.bss** - Zmienne bez wartości (zerowane w RAM)

### Kolejność Wykonania
```
Power ON → Reset → Vector Table → Stack Pointer → Reset_Handler → 
Copy .data → Zero .bss → SystemInit() → main() → while(1)
```

### Minimalne Wymagania Projektu
- startup.c z vector table i Reset_Handler
- Linker script definiujący MEMORY i SECTIONS
- SystemInit() (opcjonalnie)
- main() - kod aplikacji

---

*Następna notatka: [[stm32f429i_bare_metal_nvic|Bare Metal - NVIC i Obsługa Przerwań]]*
