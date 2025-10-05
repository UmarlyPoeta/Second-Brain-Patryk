# STM32F429I - Debugowanie przez SWD/JTAG

## 🔍 Debug Interfaces

### Wprowadzenie
STM32F429I obsługuje zaawansowane interfejsy debugowania pozwalające na analizę i diagnozę aplikacji embedded w czasie rzeczywistym.

### Dostępne interfejsy

| Interface | Piny | Prędkość | Funkcje |
|-----------|------|----------|---------|
| SWD (Serial Wire Debug) | SWDIO, SWCLK (2 piny) | Do 50 MHz | Debug, programming |
| JTAG | TMS, TCK, TDI, TDO, TRST (5 pinów) | Do 50 MHz | Debug, programming, boundary scan |
| SWO (Serial Wire Output) | SWO (1 pin) | Do 2 MHz | printf, ITM, tracing |

### Piny Debug

```
SWD Interface:
- PA13: SWDIO (Serial Wire Data I/O)
- PA14: SWCLK (Serial Wire Clock)
- PB3:  SWO (Serial Wire Output - opcjonalny)

JTAG Interface:
- PA13: TMS (Test Mode Select)
- PA14: TCK (Test Clock)
- PA15: TDI (Test Data In)
- PB3:  TRST (Test Reset - opcjonalny)
- PB4:  TDO (Test Data Out)
```

## 🛠️ Debuggery i programatory

### ST-LINK V2/V3

```c
/**
 * @brief  Konfiguracja dla ST-LINK
 */
// Domyślnie włączone w systemie
// Piny SWDIO i SWCLK są zawsze dostępne do debugowania

// Aby wyłączyć debug (oszczędność energii):
void Disable_Debug_Access(void)
{
    __HAL_AFIO_REMAP_SWJ_DISABLE();  // Wyłącz JTAG i SWD
}

// Wyłącz tylko JTAG, zostaw SWD:
void Disable_JTAG_Keep_SWD(void)
{
    __HAL_AFIO_REMAP_SWJ_NOJTAG();  // Zwolnij piny JTAG dla GPIO
}
```

### J-Link

```c
/**
 * @brief  Konfiguracja dla J-Link (identyczna jak ST-LINK)
 */
// J-Link automatycznie wykrywa interfejs SWD/JTAG
// Zalecane ustawienia:
// - Interface: SWD
// - Speed: 4 MHz (bezpieczna prędkość)
// - Reset: Connect under reset
```

## 📡 SWO - Serial Wire Output

### Konfiguracja SWO

```c
/**
 * @brief  Konfiguracja SWO dla ITM printf
 */
void SWO_Init(void)
{
    // Włącz TPIU (Trace Port Interface Unit)
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
    
    // Konfiguracja SWO prescaler
    // SWO_freq = CPU_freq / (Prescaler + 1)
    // Dla 180 MHz CPU i 2 MHz SWO: Prescaler = 89
    TPI->ACPR = 89;
    
    // Wyłącz formatowanie
    TPI->SPPR = 2;  // NRZ (No Return to Zero)
    
    // Konfiguracja TPIU
    TPI->FFCR = 0x00000100;  // Disable formatter
    
    // Konfiguracja ITM
    ITM->LAR = 0xC5ACCE55;  // Unlock ITM
    ITM->TCR = ITM_TCR_ITMENA_Msk | ITM_TCR_SYNCENA_Msk;
    ITM->TER = 0xFFFFFFFF;  // Enable all stimulus ports
}

/**
 * @brief  Printf przez SWO (ITM)
 */
int _write(int file, char *ptr, int len)
{
    for (int i = 0; i < len; i++) {
        ITM_SendChar((*ptr++));
    }
    return len;
}

/**
 * @brief  Przykład użycia
 */
void SWO_Printf_Example(void)
{
    SWO_Init();
    
    printf("STM32F429 SWO Debug\r\n");
    printf("CPU Freq: %lu MHz\r\n", HAL_RCC_GetSysClockFreq() / 1000000);
    printf("Temperature: %.2f C\r\n", Read_Temperature());
}
```

### ITM Channels

```c
/**
 * @brief  Wysyłanie danych na różne kanały ITM
 */
void ITM_SendData(uint8_t channel, uint32_t data)
{
    while (ITM->PORT[channel].u32 == 0);  // Czekaj aż port gotowy
    ITM->PORT[channel].u32 = data;
}

/**
 * @brief  Przykład: różne kanały dla różnych typów danych
 */
void Multi_Channel_ITM(void)
{
    // Kanał 0: Ogólne logi
    ITM_SendChar('L');
    ITM_SendChar('O');
    ITM_SendChar('G');
    
    // Kanał 1: Dane sensorów
    ITM->PORT[1].u32 = (uint32_t)(temperature * 100);
    
    // Kanał 2: Błędy
    ITM->PORT[2].u32 = error_code;
    
    // Kanał 3: Performance counters
    ITM->PORT[3].u32 = cycle_count;
}
```

## 🔬 Breakpoints i Watchpoints

### Hardware breakpoints

```c
/**
 * @brief  ARM Cortex-M4 ma 6 hardware breakpoints
 */
// Ustawiane przez debugger
// W GDB:
// (gdb) break main
// (gdb) break file.c:123
// (gdb) break function_name

// W STM32CubeIDE:
// Kliknij na marginesie linii kodu

/**
 * @brief  Conditional breakpoint
 */
void Debug_Example(void)
{
    for (int i = 0; i < 1000; i++) {
        // Breakpoint: break if i == 500
        Process_Data(i);
    }
}
```

### Data watchpoints

```c
/**
 * @brief  4 hardware watchpoints
 */
volatile uint32_t critical_variable = 0;

// W GDB:
// (gdb) watch critical_variable
// Zatrzyma się gdy wartość się zmieni

/**
 * @brief  Przykład debugowania race condition
 */
void Thread1(void)
{
    critical_variable++;  // Watchpoint zatrzyma się tutaj
}

void Thread2(void)
{
    critical_variable--;  // I tutaj
}
```

## 📊 Performance profiling

### DWT (Data Watchpoint and Trace)

```c
/**
 * @brief  Cycle counter dla pomiarów wydajności
 */
void DWT_Init(void)
{
    // Włącz DWT
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
    
    // Reset cycle counter
    DWT->CYCCNT = 0;
    
    // Włącz cycle counter
    DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
}

/**
 * @brief  Pomiar czasu wykonania funkcji
 */
void Measure_Function_Time(void)
{
    uint32_t start, end, cycles;
    
    DWT->CYCCNT = 0;
    start = DWT->CYCCNT;
    
    // Funkcja do zmierzenia
    Complex_Function();
    
    end = DWT->CYCCNT;
    cycles = end - start;
    
    // Przelicz na mikrosekundy (180 MHz = 180 cycles/µs)
    float time_us = cycles / 180.0f;
    
    printf("Function took %lu cycles (%.2f µs)\r\n", cycles, time_us);
}

/**
 * @brief  Makro do łatwego profilowania
 */
#define PROFILE_START()  uint32_t _profile_start = DWT->CYCCNT
#define PROFILE_END(name) do { \
    uint32_t _cycles = DWT->CYCCNT - _profile_start; \
    printf("%s: %lu cycles\r\n", name, _cycles); \
} while(0)

void Profile_Example(void)
{
    PROFILE_START();
    
    // Kod do zmierzenia
    for (int i = 0; i < 1000; i++) {
        Process_Data(i);
    }
    
    PROFILE_END("Process loop");
}
```

### PC Sampling

```c
/**
 * @brief  Profilowanie przez sampling (wymaga debuggera)
 */
// W STM32CubeIDE:
// Window -> Show View -> SWV -> Statistical Profiling
// Start -> Sample at 1 kHz
// Pokaże % czasu spędzonego w każdej funkcji
```

## 🐛 Live Expressions

### Real-time monitoring

```c
/**
 * @brief  Zmienne do monitorowania w czasie rzeczywistym
 */
volatile uint32_t debug_counter = 0;
volatile float debug_temperature = 0;
volatile uint8_t debug_state = 0;

void Debug_Update_Variables(void)
{
    debug_counter++;
    debug_temperature = Read_Temperature();
    debug_state = Get_System_State();
    
    // W STM32CubeIDE:
    // Window -> Show View -> Live Expressions
    // Dodaj zmienne do monitorowania
}
```

## 🔥 Fault Handlers

### Hard Fault debugging

```c
/**
 * @brief  Enhanced Hard Fault Handler
 */
void HardFault_Handler(void)
{
    __asm volatile
    (
        "TST LR, #4                 \n"  // Test bit 2 of LR
        "ITE EQ                     \n"
        "MRSEQ R0, MSP              \n"  // If 0, use MSP
        "MRSNE R0, PSP              \n"  // If 1, use PSP
        "B HardFault_Handler_C      \n"
    );
}

/**
 * @brief  C Handler z analizą błędu
 */
void HardFault_Handler_C(uint32_t *hardfault_args)
{
    // Stack frame:
    // hardfault_args[0] = R0
    // hardfault_args[1] = R1
    // hardfault_args[2] = R2
    // hardfault_args[3] = R3
    // hardfault_args[4] = R12
    // hardfault_args[5] = LR
    // hardfault_args[6] = PC  (adres błędu!)
    // hardfault_args[7] = xPSR
    
    volatile uint32_t stacked_r0 = hardfault_args[0];
    volatile uint32_t stacked_r1 = hardfault_args[1];
    volatile uint32_t stacked_r2 = hardfault_args[2];
    volatile uint32_t stacked_r3 = hardfault_args[3];
    volatile uint32_t stacked_r12 = hardfault_args[4];
    volatile uint32_t stacked_lr = hardfault_args[5];
    volatile uint32_t stacked_pc = hardfault_args[6];
    volatile uint32_t stacked_psr = hardfault_args[7];
    
    // CFSR - Configurable Fault Status Register
    volatile uint32_t cfsr = SCB->CFSR;
    volatile uint32_t hfsr = SCB->HFSR;
    volatile uint32_t dfsr = SCB->DFSR;
    volatile uint32_t afsr = SCB->AFSR;
    volatile uint32_t mmar = SCB->MMFAR;  // Memory Management Fault Address
    volatile uint32_t bfar = SCB->BFAR;   // Bus Fault Address
    
    printf("\r\n=== HARD FAULT ===\r\n");
    printf("PC:   0x%08lX\r\n", stacked_pc);
    printf("LR:   0x%08lX\r\n", stacked_lr);
    printf("PSR:  0x%08lX\r\n", stacked_psr);
    printf("CFSR: 0x%08lX\r\n", cfsr);
    printf("HFSR: 0x%08lX\r\n", hfsr);
    
    // Analiza typu błędu
    if (cfsr & (1 << 7)) {  // MMARVALID
        printf("Memory Management Fault at: 0x%08lX\r\n", mmar);
    }
    if (cfsr & (1 << 15)) {  // BFARVALID
        printf("Bus Fault at: 0x%08lX\r\n", bfar);
    }
    if (cfsr & (1 << 25)) {  // DIVBYZERO
        printf("Division by zero!\r\n");
    }
    if (cfsr & (1 << 24)) {  // UNALIGNED
        printf("Unaligned access!\r\n");
    }
    
    // Zapisz do backup register
    RTC_WriteBackup(RTC_BKP_DR10, stacked_pc);
    RTC_WriteBackup(RTC_BKP_DR11, cfsr);
    
    // Nieskończona pętla dla debuggera
    while (1) {
        __NOP();
    }
}
```

### Usage Fault Handler

```c
/**
 * @brief  Włączenie Usage Fault
 */
void Enable_UsageFault(void)
{
    SCB->SHCSR |= SCB_SHCSR_USGFAULTENA_Msk;
}

/**
 * @brief  Usage Fault Handler
 */
void UsageFault_Handler(void)
{
    uint32_t ufsr = (SCB->CFSR >> 16) & 0xFFFF;
    
    printf("Usage Fault!\r\n");
    
    if (ufsr & (1 << 9)) {
        printf("Division by zero\r\n");
    }
    if (ufsr & (1 << 8)) {
        printf("Unaligned access\r\n");
    }
    if (ufsr & (1 << 3)) {
        printf("No coprocessor\r\n");
    }
    if (ufsr & (1 << 2)) {
        printf("Invalid PC load\r\n");
    }
    if (ufsr & (1 << 1)) {
        printf("Invalid state\r\n");
    }
    if (ufsr & (1 << 0)) {
        printf("Undefined instruction\r\n");
    }
    
    while (1);
}
```

## 🧰 Debugging Best Practices

### Assert makra

```c
/**
 * @brief  Custom assert implementation
 */
#ifdef DEBUG
    #define ASSERT(expr) \
        if (!(expr)) { \
            printf("ASSERT failed: %s:%d %s\r\n", __FILE__, __LINE__, #expr); \
            __BKPT(0); \
        }
#else
    #define ASSERT(expr)
#endif

/**
 * @brief  Użycie assert
 */
void Safe_Function(uint32_t *ptr, uint32_t size)
{
    ASSERT(ptr != NULL);
    ASSERT(size > 0);
    ASSERT(size < MAX_SIZE);
    
    // Kod funkcji...
}
```

### Debug logging levels

```c
/**
 * @brief  System logowania z poziomami
 */
typedef enum {
    LOG_LEVEL_NONE = 0,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_WARNING,
    LOG_LEVEL_INFO,
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_VERBOSE
} LogLevel_t;

LogLevel_t current_log_level = LOG_LEVEL_DEBUG;

#define LOG_ERROR(...)   if (current_log_level >= LOG_LEVEL_ERROR)   printf("[ERROR] " __VA_ARGS__)
#define LOG_WARNING(...) if (current_log_level >= LOG_LEVEL_WARNING) printf("[WARN]  " __VA_ARGS__)
#define LOG_INFO(...)    if (current_log_level >= LOG_LEVEL_INFO)    printf("[INFO]  " __VA_ARGS__)
#define LOG_DEBUG(...)   if (current_log_level >= LOG_LEVEL_DEBUG)   printf("[DEBUG] " __VA_ARGS__)

void Debug_Logging_Example(void)
{
    LOG_ERROR("Critical error occurred!\r\n");
    LOG_WARNING("Temperature high: %.1f C\r\n", temp);
    LOG_INFO("System initialized\r\n");
    LOG_DEBUG("Counter value: %lu\r\n", counter);
}
```

## 🔗 Powiązane tematy

- [[stm32cube_ide|STM32CubeIDE]]
- [[stm32f429i_gpio|STM32F429I - GPIO]]
- [[stm32f429i_uart|STM32F429I - UART]]

## 📝 Debug Checklist

### Pre-release debugging
- [ ] Test wszystkich error paths
- [ ] Sprawdź stack usage
- [ ] Profiluj wydajność krytycznych funkcji
- [ ] Test watchdog recovery
- [ ] Test power modes wake-up
- [ ] Sprawdź memory leaks
- [ ] Test fault handlers
- [ ] Verify all assert statements
- [ ] Test edge cases i boundary conditions
- [ ] Long-term stability test (24h+)

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
