# STM32F429I - Watchdog i Nadzór Systemu

## 🐕 Watchdog Timers

### Wprowadzenie
STM32F429I posiada dwa watchdogi służące do wykrywania i resetowania systemu w przypadku zawieszenia programu (deadlock, infinite loop).

### Dostępne watchdogi

| Watchdog | Zegar | Zakres timeout | Użycie |
|----------|-------|----------------|--------|
| IWDG (Independent) | LSI (~32 kHz) | 0.1 ms - 32 s | Najbezpieczniejszy |
| WWDG (Window) | PCLK1 | 0.05 ms - 66 ms | Precyzyjne okno czasowe |

## 🔒 IWDG - Independent Watchdog

### Charakterystyka
- Niezależny zegar LSI
- Działa nawet w Stop/Standby
- Nie może być zatrzymany po uruchomieniu
- Resetuje MCU gdy nie zostanie odświeżony

### Architektura IWDG

```
┌─────────────────────────────────────┐
│         IWDG Block                  │
│                                     │
│  ┌─────────┐    ┌──────────┐       │
│  │  LSI    │───▶│ Prescaler│       │
│  │ 32 kHz  │    │ /4-/256  │       │
│  └─────────┘    └────┬─────┘       │
│                      │              │
│               ┌──────▼──────┐      │
│               │ 12-bit      │      │
│               │ Down Counter│      │
│               └──────┬──────┘      │
│                      │              │
│                   Reload?           │
│                      │              │
│                   ┌──▼──┐           │
│                   │Reset│           │
│                   └─────┘           │
└─────────────────────────────────────┘
```

### Konfiguracja IWDG

```c
/**
 * @brief  Inicjalizacja IWDG
 */
IWDG_HandleTypeDef hiwdg;

void IWDG_Init(uint32_t timeout_ms)
{
    // LSI frequency ≈ 32 kHz (może być 30-40 kHz)
    // Prescaler options: 4, 8, 16, 32, 64, 128, 256
    // Reload value: 0-4095 (12-bit)
    
    // Obliczenia dla timeout_ms
    // timeout = (Prescaler × Reload) / LSI_Frequency
    // Przykład: 1000ms @ 32kHz, Prescaler=32
    // Reload = (1000ms × 32000Hz) / (32 × 1000) = 1000
    
    hiwdg.Instance = IWDG;
    hiwdg.Init.Prescaler = IWDG_PRESCALER_32;  // LSI/32
    hiwdg.Init.Reload = 1000;  // ~1 second timeout
    
    if (HAL_IWDG_Init(&hiwdg) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Obliczenie parametrów IWDG
 */
void IWDG_Calculate_Init(uint32_t timeout_ms)
{
    uint32_t prescaler_value;
    uint32_t reload_value;
    uint32_t lsi_freq = 32000;  // Typowa wartość LSI
    
    // Dobierz prescaler i reload
    for (uint8_t prescaler_div = 4; prescaler_div <= 256; prescaler_div *= 2) {
        reload_value = (timeout_ms * lsi_freq) / (prescaler_div * 1000);
        
        if (reload_value <= 4095) {
            // Znaleziono odpowiednie wartości
            break;
        }
    }
    
    // Konwersja do HAL defines
    uint32_t prescaler;
    switch (prescaler_div) {
        case 4:   prescaler = IWDG_PRESCALER_4; break;
        case 8:   prescaler = IWDG_PRESCALER_8; break;
        case 16:  prescaler = IWDG_PRESCALER_16; break;
        case 32:  prescaler = IWDG_PRESCALER_32; break;
        case 64:  prescaler = IWDG_PRESCALER_64; break;
        case 128: prescaler = IWDG_PRESCALER_128; break;
        case 256: prescaler = IWDG_PRESCALER_256; break;
    }
    
    hiwdg.Init.Prescaler = prescaler;
    hiwdg.Init.Reload = reload_value;
    
    HAL_IWDG_Init(&hiwdg);
}

/**
 * @brief  Odświeżenie watchdoga (kick the dog)
 */
void IWDG_Refresh(void)
{
    HAL_IWDG_Refresh(&hiwdg);
}

/**
 * @brief  Przykład użycia w main loop
 */
void main_with_iwdg(void)
{
    IWDG_Init(2000);  // 2 sekundy timeout
    
    while (1) {
        // Główna pętla programu
        Do_Important_Task();
        
        // Odśwież watchdog - system działa prawidłowo
        IWDG_Refresh();
        
        HAL_Delay(500);
    }
}
```

### Wykrywanie resetu przez IWDG

```c
/**
 * @brief  Sprawdzenie czy był reset przez watchdog
 */
void Check_Reset_Source(void)
{
    if (__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST) != RESET) {
        printf("System reset by IWDG!\r\n");
        
        // Zaloguj event
        Log_Event("IWDG Reset");
        
        // Wyczyść flagę
        __HAL_RCC_CLEAR_RESET_FLAGS();
    }
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_WWDGRST) != RESET) {
        printf("System reset by WWDG!\r\n");
        __HAL_RCC_CLEAR_RESET_FLAGS();
    }
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_PORRST) != RESET) {
        printf("Power-on reset\r\n");
        __HAL_RCC_CLEAR_RESET_FLAGS();
    }
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_SFTRST) != RESET) {
        printf("Software reset\r\n");
        __HAL_RCC_CLEAR_RESET_FLAGS();
    }
}
```

## 🪟 WWDG - Window Watchdog

### Charakterystyka
- Taktowany z PCLK1
- Okno czasowe - odświeżenie może nastąpić tylko w określonym przedziale
- Może generować przerwanie przed resetem
- Można zatrzymać podczas debugowania

### Konfiguracja WWDG

```c
/**
 * @brief  Konfiguracja WWDG
 */
WWDG_HandleTypeDef hwwdg;

void WWDG_Init(void)
{
    __HAL_RCC_WWDG_CLK_ENABLE();
    
    // PCLK1 = 45 MHz
    // WWDG clock = PCLK1 / 4096 / 8 = ~1.4 kHz
    
    hwwdg.Instance = WWDG;
    hwwdg.Init.Prescaler = WWDG_PRESCALER_8;  // /4096/8
    hwwdg.Init.Window = 80;   // Dolna granica okna (64-127)
    hwwdg.Init.Counter = 127; // Wartość startowa (max)
    hwwdg.Init.EWIMode = WWDG_EWI_ENABLE;  // Early Wakeup Interrupt
    
    if (HAL_WWDG_Init(&hwwdg) != HAL_OK) {
        Error_Handler();
    }
    
    // Włącz przerwanie Early Warning
    HAL_NVIC_SetPriority(WWDG_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(WWDG_IRQn);
}

/**
 * @brief  Odświeżenie WWDG
 */
void WWDG_Refresh(void)
{
    // Musi być wywołane gdy Counter > Window (np. 80-127)
    // Wywołanie poza oknem spowoduje reset!
    HAL_WWDG_Refresh(&hwwdg);
}

/**
 * @brief  Handler przerwania WWDG
 */
void WWDG_IRQHandler(void)
{
    HAL_WWDG_IRQHandler(&hwwdg);
}

/**
 * @brief  Early Warning Callback (tuż przed resetem)
 */
void HAL_WWDG_EarlyWakeupCallback(WWDG_HandleTypeDef *hwwdg)
{
    // Ostatnia szansa przed resetem
    printf("WWDG Early Warning! System will reset soon!\r\n");
    
    // Zapisz krytyczne dane
    Save_Critical_Data();
    
    // Odśwież watchdog
    HAL_WWDG_Refresh(hwwdg);
}
```

### Obliczanie timeout WWDG

```c
/**
 * @brief  Obliczenia dla WWDG
 */
void WWDG_Calculate_Timeout(void)
{
    // T_wwdg = T_pclk1 × 4096 × 2^WDGTB × (Counter - Window + 1)
    
    uint32_t pclk1_freq = 45000000;  // 45 MHz
    uint32_t prescaler = 8;          // 2^WDGTB (1,2,4,8)
    uint32_t counter = 127;
    uint32_t window = 80;
    
    // Czas w ms
    float timeout_ms = (4096.0f * prescaler * (counter - window + 1)) / 
                       (pclk1_freq / 1000.0f);
    
    printf("WWDG timeout window: %.2f ms\r\n", timeout_ms);
    
    // Dla PCLK1=45MHz, Prescaler=8, Counter=127, Window=80:
    // timeout ≈ 34 ms (musimy odświeżyć w tym oknie)
}
```

## 🛡️ Strategie nadzoru systemu

### Multi-level watchdog

```c
/**
 * @brief  System z dwoma watchdogami
 */
typedef struct {
    uint32_t task1_counter;
    uint32_t task2_counter;
    uint32_t task3_counter;
    uint32_t main_loop_counter;
} SystemHealth_t;

SystemHealth_t health = {0};

void Multi_Watchdog_System(void)
{
    // IWDG - główny watchdog (32s timeout)
    IWDG_Init(32000);
    
    // WWDG - szybki watchdog dla krytycznych zadań
    WWDG_Init();
    
    while (1) {
        // Zadanie 1
        Task1_Execute();
        health.task1_counter++;
        
        // Zadanie 2
        Task2_Execute();
        health.task2_counter++;
        
        // Zadanie 3
        Task3_Execute();
        health.task3_counter++;
        
        health.main_loop_counter++;
        
        // Sprawdź zdrowie systemu
        if (Check_System_Health(&health)) {
            IWDG_Refresh();   // Wszystko OK
            WWDG_Refresh();
        } else {
            // Nie odświeżamy watchdoga - pozwól na reset
            printf("System unhealthy - allowing watchdog reset\r\n");
        }
        
        HAL_Delay(100);
    }
}

/**
 * @brief  Sprawdzenie zdrowia systemu
 */
uint8_t Check_System_Health(SystemHealth_t *health)
{
    static uint32_t last_check = 0;
    uint32_t now = HAL_GetTick();
    
    if (now - last_check > 1000) {  // Co sekundę
        // Sprawdź czy wszystkie zadania działają
        if (health->task1_counter == 0 || 
            health->task2_counter == 0 ||
            health->task3_counter == 0) {
            return 0;  // Unhealthy
        }
        
        // Sprawdź stack overflow
        if (Check_Stack_Overflow()) {
            return 0;
        }
        
        // Sprawdź temperature
        float temp = Read_Temperature();
        if (temp > 85.0f) {
            return 0;  // Overheating
        }
        
        // Reset counters
        health->task1_counter = 0;
        health->task2_counter = 0;
        health->task3_counter = 0;
        
        last_check = now;
    }
    
    return 1;  // Healthy
}
```

### Task watchdog (software)

```c
/**
 * @brief  Software watchdog dla zadań
 */
#define MAX_TASKS 8

typedef struct {
    uint8_t enabled;
    uint32_t timeout_ms;
    uint32_t last_kick;
    const char* name;
} TaskWatchdog_t;

TaskWatchdog_t task_watchdogs[MAX_TASKS];

/**
 * @brief  Inicjalizacja task watchdog
 */
void TaskWatchdog_Init(uint8_t task_id, const char* name, uint32_t timeout_ms)
{
    if (task_id < MAX_TASKS) {
        task_watchdogs[task_id].enabled = 1;
        task_watchdogs[task_id].timeout_ms = timeout_ms;
        task_watchdogs[task_id].last_kick = HAL_GetTick();
        task_watchdogs[task_id].name = name;
    }
}

/**
 * @brief  Kick task watchdog
 */
void TaskWatchdog_Kick(uint8_t task_id)
{
    if (task_id < MAX_TASKS && task_watchdogs[task_id].enabled) {
        task_watchdogs[task_id].last_kick = HAL_GetTick();
    }
}

/**
 * @brief  Sprawdź wszystkie task watchdogi
 */
void TaskWatchdog_Check(void)
{
    uint32_t now = HAL_GetTick();
    
    for (uint8_t i = 0; i < MAX_TASKS; i++) {
        if (task_watchdogs[i].enabled) {
            uint32_t elapsed = now - task_watchdogs[i].last_kick;
            
            if (elapsed > task_watchdogs[i].timeout_ms) {
                printf("Task watchdog timeout: %s\r\n", task_watchdogs[i].name);
                
                // Akcja naprawcza
                Reset_Task(i);
                
                // Lub pozwól na reset systemu
                // (nie odświeżaj IWDG)
            }
        }
    }
}

/**
 * @brief  Przykład użycia w RTOS
 */
void Task_Communication(void *argument)
{
    TaskWatchdog_Init(0, "Communication", 5000);
    
    while (1) {
        // Wykonaj zadanie
        Process_Communication();
        
        // Kick watchdog
        TaskWatchdog_Kick(0);
        
        osDelay(1000);
    }
}
```

## 🚨 Recovery strategies

### Graceful degradation

```c
/**
 * @brief  Degradacja funkcjonalna przy problemach
 */
typedef enum {
    MODE_NORMAL,
    MODE_REDUCED,
    MODE_MINIMAL,
    MODE_SAFE
} SystemMode_t;

SystemMode_t current_mode = MODE_NORMAL;

void Watchdog_Recovery_Strategy(void)
{
    uint32_t reset_count = RTC_ReadBackup(RTC_BKP_DR0);
    
    if (__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST)) {
        reset_count++;
        RTC_WriteBackup(RTC_BKP_DR0, reset_count);
        
        printf("Watchdog reset #%lu\r\n", reset_count);
        
        if (reset_count >= 3) {
            // Po 3 resetach - tryb bezpieczny
            current_mode = MODE_SAFE;
            printf("Entering SAFE mode\r\n");
            
            // Wyłącz wszystkie nieistotne funkcje
            Disable_NonCritical_Features();
            
            // Zwiększ timeout watchdoga
            IWDG_Init(10000);  // 10s timeout
        }
        else if (reset_count >= 2) {
            // Po 2 resetach - tryb minimalny
            current_mode = MODE_MINIMAL;
            Disable_Optional_Features();
        }
        else {
            // Pierwszy reset - tryb zredukowany
            current_mode = MODE_REDUCED;
        }
        
        __HAL_RCC_CLEAR_RESET_FLAGS();
    } else {
        // Normalny start - reset licznika
        reset_count = 0;
        RTC_WriteBackup(RTC_BKP_DR0, 0);
        current_mode = MODE_NORMAL;
    }
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_power_modes|STM32F429I - Tryby niskiego poboru mocy]]
- [[stm32f429i_rtc|STM32F429I - RTC]]
- [[stm32f429i_system_zegarowy|STM32F429I - System zegarowy]]

## 📝 Porównanie IWDG vs WWDG

| Cecha | IWDG | WWDG |
|-------|------|------|
| Niezależność | Tak (LSI) | Nie (PCLK1) |
| Zatrzymanie w debug | Nie* | Tak |
| Zakres timeout | 0.1ms - 32s | 0.05ms - 66ms |
| Okno czasowe | Nie | Tak |
| Early warning | Nie | Tak |
| Zastosowanie | Ogólne | Precyzyjne timing |

*Można włączyć zatrzymanie przez DBGMCU_APB1_FZ

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
