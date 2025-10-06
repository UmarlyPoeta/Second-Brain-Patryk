# STM32F429I - Tryby Niskiego Poboru Mocy

## ⚡ Power Management

### Wprowadzenie
STM32F429I oferuje zaawansowane tryby niskiego poboru mocy, umożliwiające znaczne zmniejszenie zużycia energii w aplikacjach battery-powered.

### Tryby pracy

| Tryb | Pobór prądu | CPU | Peryferyjne | Wake-up time |
|------|-------------|-----|-------------|--------------|
| Run | ~50 mA @ 180 MHz | ON | ON | - |
| Sleep | ~30 mA | OFF | ON | Natychmiastowy |
| Stop | ~200 μA | OFF | OFF (RTC ON) | ~5 μs |
| Standby | ~2 μA | OFF | OFF | ~50 μs |

## 😴 Sleep Mode

### Charakterystyka
- CPU zatrzymany
- Wszystkie peryferyjne działają
- Zegary pozostają włączone
- Najmniejsze oszczędności energii

### Wejście w Sleep Mode

```c
/**
 * @brief  Sleep Mode (CPU stop, peripherals running)
 */
void Enter_Sleep_Mode(void)
{
    // Opcja 1: Sleep Now - natychmiastowe wejście
    HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
    
    // Po wybudzeniu kod kontynuowany od tego miejsca
    printf("Woke up from Sleep mode\r\n");
}

/**
 * @brief  Sleep-on-Exit (dla RTOS)
 */
void Enter_Sleep_On_Exit(void)
{
    // Automatyczne wejście w sleep po wyjściu z ISR
    HAL_PWR_EnableSleepOnExit();
    
    // Wyłączenie Sleep-on-Exit
    // HAL_PWR_DisableSleepOnExit();
}

/**
 * @brief  Wybudzenie przez przerwanie
 */
void EXTI0_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
    // CPU automatycznie wychodzi z Sleep
}
```

## 🛑 Stop Mode

### Charakterystyka
- Wszystkie zegary zatrzymane (oprócz LSI/LSE)
- Regulator napięcia może być w trybie low-power
- RTC może działać
- Zawartość SRAM zachowana
- Znaczne oszczędności energii

### Wejście w Stop Mode

```c
/**
 * @brief  Stop Mode z Low Power Regulator
 */
void Enter_Stop_Mode(void)
{
    // Konfiguracja wake-up source (np. przycisk)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    HAL_NVIC_SetPriority(EXTI0_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
    
    // Clear wake-up flag
    __HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);
    
    // Enter Stop Mode
    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_SLEEPENTRY_WFI);
    
    // Po wybudzeniu - przywróć zegary!
    SystemClock_Config();
    
    printf("Woke up from Stop mode\r\n");
}

/**
 * @brief  Stop Mode z Main Regulator (szybsze wybudzenie)
 */
void Enter_Stop_MainRegulator(void)
{
    HAL_PWR_EnterSTOPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
    SystemClock_Config();
}
```

### RTC Wake-up Timer

```c
/**
 * @brief  Wybudzenie z Stop Mode przez RTC
 */
void Enter_Stop_RTC_Wakeup(uint32_t seconds)
{
    RTC_HandleTypeDef hrtc;
    
    // Konfiguracja RTC Wake-up
    __HAL_RCC_PWR_CLK_ENABLE();
    HAL_PWR_EnableBkUpAccess();
    
    // RTC clock source (LSE)
    __HAL_RCC_LSE_CONFIG(RCC_LSE_ON);
    while(__HAL_RCC_GET_FLAG(RCC_FLAG_LSERDY) == RESET);
    
    __HAL_RCC_RTC_CONFIG(RCC_RTCCLKSOURCE_LSE);
    __HAL_RCC_RTC_ENABLE();
    
    // Konfiguracja RTC Wake-up timer
    hrtc.Instance = RTC;
    hrtc.Init.HourFormat = RTC_HOURFORMAT_24;
    hrtc.Init.AsynchPrediv = 127;
    hrtc.Init.SynchPrediv = 255;
    hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;
    hrtc.Init.OutPutPolarity = RTC_OUTPUT_POLARITY_HIGH;
    hrtc.Init.OutPutType = RTC_OUTPUT_TYPE_OPENDRAIN;
    
    HAL_RTC_Init(&hrtc);
    
    // Wake-up po określonym czasie
    HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, seconds, RTC_WAKEUPCLOCK_CK_SPRE_16BITS);
    
    // Włącz przerwanie RTC
    HAL_NVIC_SetPriority(RTC_WKUP_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(RTC_WKUP_IRQn);
    
    // Enter Stop Mode
    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERREGULATOR_ON, PWR_SLEEPENTRY_WFI);
    
    // Po wybudzeniu
    SystemClock_Config();
}

/**
 * @brief  RTC Wake-up Handler
 */
void RTC_WKUP_IRQHandler(void)
{
    HAL_RTCEx_WakeUpTimerIRQHandler(&hrtc);
}

void HAL_RTCEx_WakeUpTimerEventCallback(RTC_HandleTypeDef *hrtc)
{
    // Wybudzenie z Stop mode
}
```

## 💤 Standby Mode

### Charakterystyka
- Najniższy pobór prądu (~2 μA)
- Cała zawartość SRAM tracona (oprócz backup registers)
- RTC może działać
- Tylko RTC alarm, WKUP pin, lub reset mogą wybudzić
- Reset po wybudzeniu

### Wejście w Standby Mode

```c
/**
 * @brief  Standby Mode
 */
void Enter_Standby_Mode(void)
{
    // Włącz dostęp do backup domain
    __HAL_RCC_PWR_CLK_ENABLE();
    HAL_PWR_EnableBkUpAccess();
    
    // Konfiguracja WKUP pin (PA0)
    HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1);
    
    // Clear standby flag
    __HAL_PWR_CLEAR_FLAG(PWR_FLAG_SB);
    __HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);
    
    // Enter Standby Mode
    HAL_PWR_EnterSTANDBYMode();
    
    // Ten kod nie zostanie wykonany!
    // Po wybudzeniu następuje reset
}

/**
 * @brief  Sprawdzenie przyczyny resetu
 */
void Check_Wakeup_Reason(void)
{
    if (__HAL_PWR_GET_FLAG(PWR_FLAG_SB) != RESET) {
        // Wybudzenie ze Standby
        __HAL_PWR_CLEAR_FLAG(PWR_FLAG_SB);
        __HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);
        
        printf("Woke up from Standby\r\n");
    } else {
        // Normalny reset lub power-on
        printf("Normal power-on\r\n");
    }
}
```

### Backup Registers (zachowane w Standby)

```c
/**
 * @brief  Zapis danych do Backup Registers
 */
void Save_To_Backup_Register(uint32_t value)
{
    HAL_PWR_EnableBkUpAccess();
    
    // STM32F429 ma 20 backup registers (RTC_BKP0R - RTC_BKP19R)
    HAL_RTCEx_BKUPWrite(&hrtc, RTC_BKP_DR0, value);
}

/**
 * @brief  Odczyt z Backup Registers
 */
uint32_t Read_From_Backup_Register(void)
{
    return HAL_RTCEx_BKUPRead(&hrtc, RTC_BKP_DR0);
}

/**
 * @brief  Przykład: licznik wybudzeń
 */
void Increment_Wakeup_Counter(void)
{
    uint32_t counter = Read_From_Backup_Register();
    counter++;
    Save_To_Backup_Register(counter);
    
    printf("Wakeup count: %lu\r\n", counter);
}
```

## 📊 Optymalizacja poboru mocy

### Wyłączanie nieużywanych peryferynych

```c
/**
 * @brief  Wyłącz wszystkie nieużywane peryferyjne
 */
void Disable_Unused_Peripherals(void)
{
    // Wyłącz nieużywane porty GPIO
    __HAL_RCC_GPIOB_CLK_DISABLE();
    __HAL_RCC_GPIOC_CLK_DISABLE();
    __HAL_RCC_GPIOD_CLK_DISABLE();
    // ...
    
    // Wyłącz nieużywane peryferyjne
    __HAL_RCC_SPI1_CLK_DISABLE();
    __HAL_RCC_I2C1_CLK_DISABLE();
    __HAL_RCC_USART1_CLK_DISABLE();
    // ...
    
    // Ustaw nieużywane piny jako analog (najmniejszy pobór)
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Mode = GPIO_MODE_ANALOG;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    
    GPIO_InitStruct.Pin = GPIO_PIN_All;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
    // ...
}
```

### Dynamiczne skalowanie częstotliwości

```c
/**
 * @brief  Przełączenie na niższą częstotliwość
 */
void Switch_To_Low_Speed(void)
{
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
    
    // Przełącz SYSCLK na HSI (16 MHz)
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_SYSCLK;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
    
    HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0);
    
    // Wyłącz PLL
    __HAL_RCC_PLL_DISABLE();
    
    // Wyłącz HSE (jeśli nie jest potrzebny)
    __HAL_RCC_HSE_CONFIG(RCC_HSE_OFF);
}

/**
 * @brief  Powrót do pełnej prędkości
 */
void Switch_To_High_Speed(void)
{
    SystemClock_Config();  // 180 MHz
}
```

### Voltage Scaling

```c
/**
 * @brief  Voltage Scaling dla oszczędności energii
 */
void Configure_Voltage_Scaling(void)
{
    __HAL_RCC_PWR_CLK_ENABLE();
    
    // Scale 1: Max performance (1.8V core)
    __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
    
    // Scale 2: Medium performance (~144 MHz max)
    // __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE2);
    
    // Scale 3: Low performance (~120 MHz max, lowest power)
    // __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);
}
```

## 🔋 Przykładowa aplikacja battery-powered

### Cykliczne pomiary z sleep

```c
/**
 * @brief  Aplikacja z okresowymi pomiarami
 */
void Battery_Powered_Application(void)
{
    // Inicjalizacja
    SystemClock_Config();
    RTC_Init();
    ADC_Init();
    
    while (1) {
        // Pomiar
        float temperature = Read_Temperature();
        float battery_voltage = Read_Battery_Voltage();
        
        // Transmisja danych (np. przez LoRa)
        Transmit_Data(temperature, battery_voltage);
        
        // Zapisz stan do backup register
        Save_State_To_Backup();
        
        // Sleep na 5 minut
        Enter_Stop_RTC_Wakeup(300);  // 300 sekund
        
        // Po wybudzeniu kontynuuj pętlę
    }
}
```

### Wykrywanie low battery

```c
/**
 * @brief  Monitorowanie napięcia baterii
 */
void Monitor_Battery_Voltage(void)
{
    float vbat = ADC_ReadVBAT();
    
    if (vbat < 2.5f) {
        // Krytycznie niskie napięcie
        printf("Critical battery voltage!\r\n");
        
        // Zapisz krytyczne dane
        Save_Critical_Data();
        
        // Wejdź w deep sleep
        Enter_Standby_Mode();
    }
    else if (vbat < 3.0f) {
        // Niskie napięcie - ograniczwydajność
        printf("Low battery - switching to power save mode\r\n");
        
        // Zmniejsz częstotliwość
        Switch_To_Low_Speed();
        
        // Wyłącz nieużywane peryferyjne
        Disable_Unused_Peripherals();
    }
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_rtc|STM32F429I - RTC]]
- [[stm32f429i_system_zegarowy|STM32F429I - System zegarowy]]
- [[stm32f429i_adc|STM32F429I - ADC]]

## 📝 Porównanie trybów

### Wybór trybu dla aplikacji

| Aplikacja | Zalecany tryb | Uwagi |
|-----------|---------------|-------|
| Always-on sensor | Sleep | Peryferyjne działają |
| Okresowe pomiary (sekundy) | Stop | RTC wake-up |
| Okresowe pomiary (minuty/godziny) | Standby | Najniższy pobór |
| Czekanie na event | Sleep/Stop | Zależnie od czasu |
| Bateria + WiFi | Stop między transmisjami | Szybkie wybudzenie |

### Typowe pobory prądu

```
Run mode (180 MHz): ~50 mA
Run mode (16 MHz):  ~10 mA
Sleep mode:         ~30 mA
Stop mode:          ~200 μA
Standby mode:       ~2 μA
```

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
