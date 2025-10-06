# STM32F429I - Bare Metal - NVIC i Obsługa Przerwań

## 🎯 NVIC - Nested Vectored Interrupt Controller

### Czym Jest NVIC?

```
NVIC to kontroler przerwań w Cortex-M4.
Zarządza wszystkimi przerwaniami zewnętrznymi i wewnętrznymi.

Cechy NVIC w STM32F429:
- 91 przerwań zewnętrznych (IRQ0-IRQ90)
- 16 poziomów priorytetów (0-15)
- Zagnieżdżanie przerwań
- Masking (włączanie/wyłączanie)
- Pending (oczekujące przerwania)
```

## 📋 Rejestry NVIC

### Adresy Bazowe

```c
/**
 * @brief  NVIC Base Address
 */
#define NVIC_BASE  0xE000E100UL

/**
 * @brief  Struktura NVIC (uproszczona)
 */
typedef struct {
    volatile uint32_t ISER[8];    // 0x000: Interrupt Set Enable Register
    uint32_t RESERVED0[24];
    volatile uint32_t ICER[8];    // 0x080: Interrupt Clear Enable Register
    uint32_t RESERVED1[24];
    volatile uint32_t ISPR[8];    // 0x100: Interrupt Set Pending Register
    uint32_t RESERVED2[24];
    volatile uint32_t ICPR[8];    // 0x180: Interrupt Clear Pending Register
    uint32_t RESERVED3[24];
    volatile uint32_t IABR[8];    // 0x200: Interrupt Active Bit Register
    uint32_t RESERVED4[56];
    volatile uint8_t  IP[240];    // 0x300: Interrupt Priority Register
    uint32_t RESERVED5[644];
    volatile uint32_t STIR;       // 0xE00: Software Trigger Interrupt Register
} NVIC_Type;

#define NVIC  ((NVIC_Type*)NVIC_BASE)
```

### Numery Przerwań (IRQ Numbers)

```c
/**
 * @brief  IRQ Numbers dla STM32F429
 * 
 * W Vector Table: IRQn + 16
 * (16 to przerwania Cortex-M4: Reset, NMI, HardFault, etc.)
 */
typedef enum {
    // Cortex-M4 wewnętrzne (negatywne numery)
    NonMaskableInt_IRQn     = -14,
    HardFault_IRQn          = -13,
    MemoryManagement_IRQn   = -12,
    BusFault_IRQn           = -11,
    UsageFault_IRQn         = -10,
    SVCall_IRQn             = -5,
    DebugMonitor_IRQn       = -4,
    PendSV_IRQn             = -2,
    SysTick_IRQn            = -1,
    
    // STM32F429 zewnętrzne (0-90)
    WWDG_IRQn               = 0,   // Window WatchDog
    PVD_IRQn                = 1,   // PVD through EXTI
    TAMP_STAMP_IRQn         = 2,   // Tamper and TimeStamps
    RTC_WKUP_IRQn           = 3,   // RTC Wakeup
    FLASH_IRQn              = 4,   // FLASH
    RCC_IRQn                = 5,   // RCC
    EXTI0_IRQn              = 6,   // EXTI Line0
    EXTI1_IRQn              = 7,   // EXTI Line1
    // ...
    USART1_IRQn             = 37,  // USART1
    USART2_IRQn             = 38,  // USART2
    // ...
    TIM2_IRQn               = 28,  // TIM2
    TIM3_IRQn               = 29,  // TIM3
    // ...
    DMA1_Stream0_IRQn       = 11,  // DMA1 Stream 0
    // ... łącznie 91 przerwań (0-90)
} IRQn_Type;
```

## 🔧 Włączanie i Wyłączanie Przerwań

### ISER - Interrupt Set Enable Register

```
NVIC_ISER[0-7] - 8 rejestrów po 32 bity = 256 bitów

Każdy bit odpowiada jednem przerwaniu:
- Bit 0 w ISER[0] = IRQ0 (WWDG)
- Bit 1 w ISER[0] = IRQ1 (PVD)
- ...
- Bit 31 w ISER[0] = IRQ31
- Bit 0 w ISER[1] = IRQ32
- ...
- Bit 26 w ISER[2] = IRQ90 (ostatnie)

Obliczenie indeksu:
ISER[IRQn / 32] |= (1 << (IRQn % 32))
```

### Przykłady Włączania Przerwań

```c
/**
 * @brief  Włączanie przerwania - krok po kroku
 */
void Enable_USART1_IRQ_Manual(void)
{
    // USART1_IRQn = 37
    
    // KROK 1: Oblicz który rejestr ISER
    uint8_t reg_index = 37 / 32;  // 37 / 32 = 1 -> ISER[1]
    
    // KROK 2: Oblicz pozycję bitu
    uint8_t bit_pos = 37 % 32;    // 37 % 32 = 5
    
    // KROK 3: Ustaw bit
    NVIC->ISER[reg_index] |= (1 << bit_pos);
    // NVIC->ISER[1] |= (1 << 5);
    
    // Teraz USART1 interrupt jest włączony w NVIC
}

/**
 * @brief  Uniwersalna funkcja włączania przerwania
 */
void NVIC_EnableIRQ(IRQn_Type IRQn)
{
    // Sprawdź czy IRQn jest poprawny
    if ((int32_t)IRQn >= 0) {
        NVIC->ISER[IRQn / 32] = (1 << (IRQn % 32));
    }
}

/**
 * @brief  Przykłady użycia
 */
void Enable_Interrupts_Examples(void)
{
    // Włącz USART1
    NVIC_EnableIRQ(USART1_IRQn);
    
    // Włącz TIM2
    NVIC_EnableIRQ(TIM2_IRQn);
    
    // Włącz EXTI0
    NVIC_EnableIRQ(EXTI0_IRQn);
    
    // Włącz DMA1 Stream 0
    NVIC_EnableIRQ(DMA1_Stream0_IRQn);
}
```

### ICER - Interrupt Clear Enable Register

```c
/**
 * @brief  Wyłączanie przerwania
 */
void NVIC_DisableIRQ(IRQn_Type IRQn)
{
    if ((int32_t)IRQn >= 0) {
        NVIC->ICER[IRQn / 32] = (1 << (IRQn % 32));
    }
}

/**
 * @brief  Przykład - tymczasowe wyłączenie przerwania
 */
void Critical_Section_Example(void)
{
    // Wyłącz przerwanie na czas krytycznej sekcji
    NVIC_DisableIRQ(USART1_IRQn);
    
    // Krytyczna sekcja - nie może być przerwana przez USART1
    // ...
    
    // Włącz z powrotem
    NVIC_EnableIRQ(USART1_IRQn);
}
```

## 🎚️ Priorytety Przerwań

### Rejestr IP - Interrupt Priority

```
NVIC_IP[0-239] - 240 bajtów (8-bit dla każdego przerwania)

STM32F429 używa tylko 4 górnych bitów:
- Bity 7-4: Priority (0-15)
- Bity 3-0: Nieużywane (zawsze 0)

Priority:
0 = Najwyższy priorytet
15 = Najniższy priorytet
```

### Ustawianie Priorytetów

```c
/**
 * @brief  Ustawienie priorytetu - szczegółowo
 */
void Set_USART1_Priority_Manual(uint8_t priority)
{
    // USART1_IRQn = 37
    
    // KROK 1: Priority musi być 0-15
    priority &= 0x0F;
    
    // KROK 2: Przesunięcie w lewo o 4 bity (STM32 używa bitów 7-4)
    uint8_t priority_shifted = priority << 4;
    
    // KROK 3: Ustaw w rejestrze IP
    NVIC->IP[37] = priority_shifted;
}

/**
 * @brief  Uniwersalna funkcja ustawienia priorytetu
 */
void NVIC_SetPriority(IRQn_Type IRQn, uint32_t priority)
{
    if ((int32_t)IRQn >= 0) {
        // Zewnętrzne przerwania
        NVIC->IP[IRQn] = (priority << 4) & 0xF0;
    } else {
        // System exceptions (SysTick, PendSV, etc.)
        // Używają SCB->SHP[] zamiast NVIC->IP[]
        #define SCB_BASE  0xE000ED00UL
        volatile uint8_t *SHP = (volatile uint8_t*)(SCB_BASE + 0x18);
        SHP[((uint32_t)IRQn & 0xF) - 4] = (priority << 4) & 0xF0;
    }
}

/**
 * @brief  Przykłady priorytetów
 */
void Configure_Priorities_Example(void)
{
    // Wysoki priorytet dla krytycznych przerwań
    NVIC_SetPriority(USART1_IRQn, 0);  // Najwyższy
    NVIC_SetPriority(TIM2_IRQn, 1);    // Bardzo wysoki
    
    // Średni priorytet
    NVIC_SetPriority(EXTI0_IRQn, 5);   // Średni
    
    // Niski priorytet
    NVIC_SetPriority(DMA1_Stream0_IRQn, 10);  // Niski
    NVIC_SetPriority(SysTick_IRQn, 15);       // Najniższy
}
```

### Zagnieżdżanie Przerwań

```c
/**
 * @brief  Jak działa zagnieżdżanie przerwań?
 * 
 * Przykład:
 * - USART1 (priority 5) jest obsługiwane
 * - Przychodzi TIM2 (priority 1)
 * - TIM2 przerywa USART1 (wyższy priorytet!)
 * - Po TIM2, wraca do USART1
 * 
 * Reguły:
 * 1. Niższy numer = wyższy priorytet
 * 2. Przerwanie może przerwać inne o niższym priorytecie
 * 3. Nie może przerwać równego lub wyższego priorytetu
 */

void USART1_IRQHandler(void)
{
    // Priority 5
    // ...
    // <-- TIM2 (priority 1) może przerwać tutaj!
    // ...
}

void TIM2_IRQHandler(void)
{
    // Priority 1
    // ...
    // <-- USART1 (priority 5) NIE może przerwać tutaj!
    // ...
}
```

## 🚨 Pending i Active

### ISPR/ICPR - Pending Registers

```c
/**
 * @brief  Pending = przerwanie czeka na obsługę
 * 
 * Przerwanie jest pending gdy:
 * 1. Event wystąpił (np. UART received data)
 * 2. Ale przerwanie nie jest jeszcze obsługiwane
 * 
 * Może być pending z różnych powodów:
 * - Przerwanie wyłączone (ISER)
 * - Niższy priorytet niż aktualnie obsługiwane
 * - Globalne przerwania wyłączone (PRIMASK)
 */

/**
 * @brief  Ustawienie przerwania jako pending (software trigger)
 */
void NVIC_SetPendingIRQ(IRQn_Type IRQn)
{
    if ((int32_t)IRQn >= 0) {
        NVIC->ISPR[IRQn / 32] = (1 << (IRQn % 32));
    }
}

/**
 * @brief  Wyczyszczenie pending flag
 */
void NVIC_ClearPendingIRQ(IRQn_Type IRQn)
{
    if ((int32_t)IRQn >= 0) {
        NVIC->ICPR[IRQn / 32] = (1 << (IRQn % 32));
    }
}

/**
 * @brief  Sprawdzenie czy przerwanie jest pending
 */
uint32_t NVIC_GetPendingIRQ(IRQn_Type IRQn)
{
    if ((int32_t)IRQn >= 0) {
        return (NVIC->ISPR[IRQn / 32] & (1 << (IRQn % 32))) ? 1 : 0;
    }
    return 0;
}

/**
 * @brief  Software interrupt trigger - przykład
 */
void Trigger_Software_Interrupt(void)
{
    // Wywołaj przerwanie software'owo (bez hardware event)
    NVIC_SetPendingIRQ(USART1_IRQn);
    
    // Handler USART1_IRQHandler() zostanie wykonany
}
```

## 🔐 Globalne Włączanie/Wyłączanie Przerwań

### PRIMASK, FAULTMASK, BASEPRI

```c
/**
 * @brief  PRIMASK - Prosty global interrupt enable/disable
 * 
 * PRIMASK = 0: Wszystkie przerwania włączone
 * PRIMASK = 1: Wszystkie przerwania wyłączone (oprócz NMI i HardFault)
 */

// Inline assembly dla PRIMASK
static inline void __disable_irq(void)
{
    __asm volatile ("cpsid i" : : : "memory");  // Set PRIMASK = 1
}

static inline void __enable_irq(void)
{
    __asm volatile ("cpsie i" : : : "memory");  // Clear PRIMASK = 0
}

/**
 * @brief  Użycie __disable_irq / __enable_irq
 */
void Critical_Section(void)
{
    __disable_irq();
    
    // Krytyczna sekcja - żadne przerwania nie mogą przerwać
    // UWAGA: Trzymaj to jak najkrótsze!
    volatile_shared_variable = new_value;
    
    __enable_irq();
}

/**
 * @brief  BASEPRI - Maskowanie według priorytetu
 * 
 * BASEPRI = 0: Wszystkie przerwania włączone
 * BASEPRI = N: Blokuj przerwania o priorytecie >= N (niższe w hierarchii)
 */

static inline void __set_BASEPRI(uint32_t basePri)
{
    __asm volatile ("msr BASEPRI, %0" : : "r" (basePri) : "memory");
}

static inline uint32_t __get_BASEPRI(void)
{
    uint32_t result;
    __asm volatile ("mrs %0, BASEPRI" : "=r" (result));
    return result;
}

/**
 * @brief  Przykład BASEPRI - blokuj tylko niskie priorytety
 */
void Medium_Critical_Section(void)
{
    // Zablokuj przerwania o priorytecie 5 i wyższym (numerycznie)
    __set_BASEPRI(5 << 4);  // Shift bo STM32 używa bitów 7-4
    
    // Krytyczna sekcja
    // Przerwania 0-4 mogą przerwać (wysokie priorytety)
    // Przerwania 5-15 są zablokowane
    
    __set_BASEPRI(0);  // Odblokuj wszystkie
}
```

## 🎯 Kompletny Przykład: Przycisk z Przerwaniem EXTI

### EXTI - External Interrupt Controller

```c
/**
 * @brief  EXTI Base Address
 */
#define EXTI_BASE   0x40013C00UL
#define SYSCFG_BASE 0x40013800UL

/**
 * @brief  Struktura EXTI
 */
typedef struct {
    volatile uint32_t IMR;    // 0x00: Interrupt mask register
    volatile uint32_t EMR;    // 0x04: Event mask register
    volatile uint32_t RTSR;   // 0x08: Rising trigger selection register
    volatile uint32_t FTSR;   // 0x0C: Falling trigger selection register
    volatile uint32_t SWIER;  // 0x10: Software interrupt event register
    volatile uint32_t PR;     // 0x14: Pending register
} EXTI_TypeDef;

/**
 * @brief  Struktura SYSCFG
 */
typedef struct {
    volatile uint32_t MEMRMP;
    volatile uint32_t PMC;
    volatile uint32_t EXTICR[4];  // 0x08: External interrupt configuration
    // ...
} SYSCFG_TypeDef;

#define EXTI   ((EXTI_TypeDef*)EXTI_BASE)
#define SYSCFG ((SYSCFG_TypeDef*)SYSCFG_BASE)

/**
 * @brief  Konfiguracja przycisku PA0 z przerwaniem
 * 
 * KROK PO KROKU:
 * 1. Włącz zegary (GPIOA, SYSCFG)
 * 2. Skonfiguruj PA0 jako input z pull-down
 * 3. Podłącz PA0 do EXTI0 przez SYSCFG
 * 4. Skonfiguruj EXTI0 (rising edge)
 * 5. Włącz przerwanie EXTI0 w NVIC
 */

void Button_EXTI_Init(void)
{
    // KROK 1: Włącz zegary
    RCC->AHB1ENR |= (1 << 0);   // GPIOA
    RCC->APB2ENR |= (1 << 14);  // SYSCFG
    
    // KROK 2: PA0 jako input z pull-down
    GPIOA->MODER &= ~(0x3 << 0);  // Input mode
    GPIOA->PUPDR &= ~(0x3 << 0);
    GPIOA->PUPDR |= (0x2 << 0);   // Pull-down
    
    // KROK 3: Podłącz PA0 do EXTI0
    // SYSCFG_EXTICR[0] kontroluje EXTI0-EXTI3
    // Bity 0-3: EXTI0
    // 0000 = PA, 0001 = PB, 0010 = PC, etc.
    SYSCFG->EXTICR[0] &= ~(0xF << 0);  // Wyczyść
    SYSCFG->EXTICR[0] |= (0x0 << 0);   // PA (0x0)
    
    // KROK 4: Konfiguruj EXTI0
    // Rising edge trigger (przycisk przyciśnięty = LOW->HIGH)
    EXTI->RTSR |= (1 << 0);   // Rising trigger enable
    EXTI->FTSR &= ~(1 << 0);  // Falling trigger disable
    
    // Unmask EXTI0 (włącz)
    EXTI->IMR |= (1 << 0);
    
    // KROK 5: Włącz EXTI0 w NVIC
    NVIC_SetPriority(EXTI0_IRQn, 5);  // Średni priorytet
    NVIC_EnableIRQ(EXTI0_IRQn);
}

/**
 * @brief  Handler przerwania EXTI0
 */
void EXTI0_IRQHandler(void)
{
    // Sprawdź czy to rzeczywiście EXTI0
    if (EXTI->PR & (1 << 0)) {
        // EXTI0 pending flag jest ustawiony
        
        // Twój kod obsługi przycisku
        // np. toggle LED
        GPIOA->ODR ^= (1 << 5);
        
        // WAŻNE: Wyczyść pending flag!
        EXTI->PR = (1 << 0);  // W EXTI->PR: zapis 1 = clear
    }
}
```

## ⏱️ SysTick - System Timer

### Konfiguracja SysTick

```c
/**
 * @brief  SysTick Base Address
 */
#define SysTick_BASE  0xE000E010UL

/**
 * @brief  Struktura SysTick
 */
typedef struct {
    volatile uint32_t CTRL;   // 0x00: Control and Status Register
    volatile uint32_t LOAD;   // 0x04: Reload Value Register
    volatile uint32_t VAL;    // 0x08: Current Value Register
    volatile uint32_t CALIB;  // 0x0C: Calibration Value Register
} SysTick_Type;

#define SysTick  ((SysTick_Type*)SysTick_BASE)

/**
 * @brief  Konfiguracja SysTick dla 1ms tick @ 16 MHz HSI
 * 
 * SysTick_LOAD = (clock_freq / tick_freq) - 1
 * Dla 1ms @ 16 MHz: LOAD = (16,000,000 / 1,000) - 1 = 15,999
 */
void SysTick_Init_1ms(void)
{
    // KROK 1: Wyłącz SysTick na czas konfiguracji
    SysTick->CTRL = 0;
    
    // KROK 2: Ustaw reload value
    SysTick->LOAD = 16000 - 1;  // 1ms @ 16 MHz
    
    // KROK 3: Wyczyść current value
    SysTick->VAL = 0;
    
    // KROK 4: Konfiguruj i włącz
    // Bit 0: ENABLE
    // Bit 1: TICKINT (interrupt enable)
    // Bit 2: CLKSOURCE (1=processor clock, 0=external)
    SysTick->CTRL = (1 << 0)   // Enable
                  | (1 << 1)   // Interrupt enable
                  | (1 << 2);  // Processor clock
}

/**
 * @brief  Zmienne dla delay
 */
volatile uint32_t systick_counter = 0;

/**
 * @brief  SysTick Handler
 */
void SysTick_Handler(void)
{
    systick_counter++;
}

/**
 * @brief  Delay funkcja używająca SysTick
 */
void delay_ms(uint32_t ms)
{
    uint32_t start = systick_counter;
    while ((systick_counter - start) < ms);
}

/**
 * @brief  Przykład użycia
 */
int main(void)
{
    SystemInit();
    SysTick_Init_1ms();
    
    // Włącz LED
    RCC->AHB1ENR |= (1 << 0);
    GPIOA->MODER &= ~(0x3 << 10);
    GPIOA->MODER |= (0x1 << 10);
    
    while (1) {
        GPIOA->ODR ^= (1 << 5);
        delay_ms(500);  // Dokładny delay!
    }
}
```

## 🐛 Debugging Przerwań

### Sprawdzanie Stanów

```c
/**
 * @brief  Funkcje debugowania przerwań
 */

// Czy przerwanie jest włączone?
uint32_t Is_IRQ_Enabled(IRQn_Type IRQn)
{
    return (NVIC->ISER[IRQn / 32] & (1 << (IRQn % 32))) ? 1 : 0;
}

// Jaki priorytet ma przerwanie?
uint32_t Get_IRQ_Priority(IRQn_Type IRQn)
{
    return (NVIC->IP[IRQn] >> 4) & 0x0F;
}

// Czy przerwanie jest pending?
uint32_t Is_IRQ_Pending(IRQn_Type IRQn)
{
    return (NVIC->ISPR[IRQn / 32] & (1 << (IRQn % 32))) ? 1 : 0;
}

// Czy przerwanie jest active?
uint32_t Is_IRQ_Active(IRQn_Type IRQn)
{
    return (NVIC->IABR[IRQn / 32] & (1 << (IRQn % 32))) ? 1 : 0;
}

/**
 * @brief  Debug info - wypisz stan wszystkich przerwań
 */
void Print_NVIC_Status(void)
{
    // W debuggerze ustaw breakpoint i sprawdź zmienne
    
    for (int i = 0; i < 91; i++) {
        if (Is_IRQ_Enabled(i)) {
            volatile uint32_t priority = Get_IRQ_Priority(i);
            volatile uint32_t pending = Is_IRQ_Pending(i);
            volatile uint32_t active = Is_IRQ_Active(i);
            
            // Sprawdź w debuggerze
            __asm("nop");
        }
    }
}
```

### Typowe Problemy

```c
/**
 * @brief  Problem 1: Przerwanie się nie wywołuje
 * 
 * Checklist:
 * 1. Czy zegar peryferyjnego jest włączony? (RCC_APBxENR)
 * 2. Czy peryferyjne jest skonfigurowane do generowania przerwań?
 * 3. Czy przerwanie jest włączone w NVIC? (ISER)
 * 4. Czy globalne przerwania są włączone? (PRIMASK)
 * 5. Czy pending flag jest czyszczona w handlerze?
 */

/**
 * @brief  Problem 2: Przerwanie wywołuje się non-stop
 * 
 * Przyczyna: Nie wyczyszczono pending flag w handlerze!
 */

void EXTI0_IRQHandler_WRONG(void)
{
    // Twój kod
    GPIOA->ODR ^= (1 << 5);
    
    // BŁĄD: Brak wyczyszczenia EXTI->PR!
    // Handler będzie wywoływany w kółko!
}

void EXTI0_IRQHandler_CORRECT(void)
{
    if (EXTI->PR & (1 << 0)) {
        // Twój kod
        GPIOA->ODR ^= (1 << 5);
        
        // POPRAWNIE: Wyczyść pending flag
        EXTI->PR = (1 << 0);
    }
}

/**
 * @brief  Problem 3: Handler ma złą nazwę
 * 
 * Handler MUSI mieć dokładnie taką nazwę jak w vector table!
 */

// ŹLE - handler się nie wywoła
void USART1_Handler(void) { }      // Brak _IRQ
void usart1_IRQHandler(void) { }   // Małe litery

// DOBRZE
void USART1_IRQHandler(void) { }   // ✓
```

## 🔗 Powiązane Tematy

- [[stm32f429i_bare_metal_startup|Bare Metal - Startup Code]]
- [[stm32f429i_bare_metal_gpio|Bare Metal - GPIO]]
- [[stm32f429i_bare_metal_exti|Bare Metal - EXTI szczegółowo]]
- [[stm32f429i_przerwania|Przerwania z HAL - porównanie]]

## 📝 Podsumowanie

### Kluczowe Rejestry NVIC
- **ISER** - Enable interrupt
- **ICER** - Disable interrupt
- **ISPR** - Set pending
- **ICPR** - Clear pending
- **IP** - Set priority (0-15)

### Kolejność Konfiguracji Przerwania
1. Skonfiguruj peryferyjne (GPIO, UART, etc.)
2. Włącz generowanie przerwań w peryferyjnym
3. Ustaw priorytet: `NVIC_SetPriority(IRQn, priority)`
4. Włącz w NVIC: `NVIC_EnableIRQ(IRQn)`
5. Włącz globalne przerwania: `__enable_irq()`

### Handler Przerwania - Must Have
```c
void XXX_IRQHandler(void) {
    // 1. Sprawdź który event
    if (PERIPHERAL->FLAG & FLAG_BIT) {
        // 2. Obsługa
        // ...
        // 3. WYCZYŚĆ FLAG! (WAŻNE!)
        PERIPHERAL->FLAG = FLAG_BIT;
    }
}
```

---

*Następna notatka: [[stm32f429i_bare_metal_uart|Bare Metal - UART Komunikacja]]*
