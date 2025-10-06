# STM32F429I - RTC i Pomiar Czasu Rzeczywistego

## ⏰ Real-Time Clock (RTC)

### Wprowadzenie
RTC w STM32F429I to zaawansowany moduł do pomiaru czasu rzeczywistego z kalendarzem, alarmami i funkcją wake-up. Działa nawet gdy główny system jest w trybie niskiego poboru mocy.

### Charakterystyka RTC

| Parametr | Wartość |
|----------|---------|
| Źródło zegara | LSE (32.768 kHz), LSI, HSE/32 |
| Format czasu | 24h lub 12h (AM/PM) |
| Dokładność | ±20 ppm (z LSE) |
| Alarmy | 2 niezależne (Alarm A, Alarm B) |
| Backup registers | 20 rejestrów (80 bajtów) |
| Tamper detection | 2 piny wykrywania manipulacji |
| Calibracja | Cyfrowa kalibracja output |

### Architektura RTC

```
┌─────────────────────────────────────────┐
│              RTC Block                  │
│                                         │
│  ┌──────────┐      ┌──────────┐        │
│  │ LSE/LSI  │─────▶│ Prescaler│        │
│  │ 32.768kHz│      │          │        │
│  └──────────┘      └────┬─────┘        │
│                         │              │
│                  ┌──────▼──────┐       │
│                  │   Counter   │       │
│                  │ Time/Date   │       │
│                  └──────┬──────┘       │
│                         │              │
│          ┌──────────────┼──────────┐   │
│          │              │          │   │
│     ┌────▼────┐   ┌────▼────┐ ┌───▼───┐
│     │ Alarm A │   │ Alarm B │ │Wakeup │
│     └─────────┘   └─────────┘ └───────┘
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Backup Registers (20x32bit)   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 🔧 Konfiguracja RTC

### Inicjalizacja z LSE

```c
/**
 * @brief  Konfiguracja RTC z LSE (32.768 kHz)
 */
RTC_HandleTypeDef hrtc;

void RTC_Init(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};
    
    // Włącz dostęp do Backup Domain
    __HAL_RCC_PWR_CLK_ENABLE();
    HAL_PWR_EnableBkUpAccess();
    
    // Konfiguracja LSE
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_LSE;
    RCC_OscInitStruct.LSEState = RCC_LSE_ON;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
    
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
        Error_Handler();
    }
    
    // Wybierz LSE jako źródło RTC
    PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_RTC;
    PeriphClkInitStruct.RTCClockSelection = RCC_RTCCLKSOURCE_LSE;
    
    if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK) {
        Error_Handler();
    }
    
    // Włącz RTC
    __HAL_RCC_RTC_ENABLE();
    
    // Konfiguracja RTC
    hrtc.Instance = RTC;
    hrtc.Init.HourFormat = RTC_HOURFORMAT_24;
    hrtc.Init.AsynchPrediv = 127;  // Dla 32.768 kHz
    hrtc.Init.SynchPrediv = 255;   // RTC clock = 32768/(127+1)/(255+1) = 1 Hz
    hrtc.Init.OutPut = RTC_OUTPUT_DISABLE;
    hrtc.Init.OutPutPolarity = RTC_OUTPUT_POLARITY_HIGH;
    hrtc.Init.OutPutType = RTC_OUTPUT_TYPE_OPENDRAIN;
    
    if (HAL_RTC_Init(&hrtc) != HAL_OK) {
        Error_Handler();
    }
}
```

### Ustawienie czasu i daty

```c
/**
 * @brief  Ustawienie czasu RTC
 */
void RTC_SetTime(uint8_t hours, uint8_t minutes, uint8_t seconds)
{
    RTC_TimeTypeDef sTime = {0};
    
    sTime.Hours = hours;
    sTime.Minutes = minutes;
    sTime.Seconds = seconds;
    sTime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
    sTime.StoreOperation = RTC_STOREOPERATION_RESET;
    
    if (HAL_RTC_SetTime(&hrtc, &sTime, RTC_FORMAT_BIN) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Ustawienie daty RTC
 */
void RTC_SetDate(uint8_t year, uint8_t month, uint8_t date, uint8_t weekday)
{
    RTC_DateTypeDef sDate = {0};
    
    sDate.Year = year;     // 0-99 (2000-2099)
    sDate.Month = month;   // 1-12
    sDate.Date = date;     // 1-31
    sDate.WeekDay = weekday;  // 1-7 (Monday-Sunday)
    
    if (HAL_RTC_SetDate(&hrtc, &sDate, RTC_FORMAT_BIN) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Przykład: ustaw 15:30:00, 25 grudnia 2024, środa
 */
void Set_Example_DateTime(void)
{
    RTC_SetDate(24, 12, 25, RTC_WEEKDAY_WEDNESDAY);
    RTC_SetTime(15, 30, 0);
}
```

### Odczyt czasu i daty

```c
/**
 * @brief  Odczyt aktualnego czasu
 */
void RTC_GetTime(uint8_t *hours, uint8_t *minutes, uint8_t *seconds)
{
    RTC_TimeTypeDef sTime;
    
    HAL_RTC_GetTime(&hrtc, &sTime, RTC_FORMAT_BIN);
    
    *hours = sTime.Hours;
    *minutes = sTime.Minutes;
    *seconds = sTime.Seconds;
}

/**
 * @brief  Odczyt aktualnej daty
 */
void RTC_GetDate(uint8_t *year, uint8_t *month, uint8_t *date, uint8_t *weekday)
{
    RTC_DateTypeDef sDate;
    
    HAL_RTC_GetDate(&hrtc, &sDate, RTC_FORMAT_BIN);
    
    *year = sDate.Year;
    *month = sDate.Month;
    *date = sDate.Date;
    *weekday = sDate.WeekDay;
}

/**
 * @brief  Wyświetl aktualny czas
 */
void Print_DateTime(void)
{
    uint8_t hours, minutes, seconds;
    uint8_t year, month, date, weekday;
    
    RTC_GetTime(&hours, &minutes, &seconds);
    RTC_GetDate(&year, &month, &date, &weekday);
    
    const char* days[] = {"", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};
    
    printf("Date: 20%02d-%02d-%02d %s\r\n", year, month, date, days[weekday]);
    printf("Time: %02d:%02d:%02d\r\n", hours, minutes, seconds);
}
```

## ⏰ Alarmy RTC

### Konfiguracja Alarm A

```c
/**
 * @brief  Konfiguracja Alarm A
 */
void RTC_SetAlarm_A(uint8_t hours, uint8_t minutes, uint8_t seconds)
{
    RTC_AlarmTypeDef sAlarm = {0};
    
    sAlarm.AlarmTime.Hours = hours;
    sAlarm.AlarmTime.Minutes = minutes;
    sAlarm.AlarmTime.Seconds = seconds;
    sAlarm.AlarmTime.SubSeconds = 0;
    sAlarm.AlarmTime.DayLightSaving = RTC_DAYLIGHTSAVING_NONE;
    sAlarm.AlarmTime.StoreOperation = RTC_STOREOPERATION_RESET;
    
    // Maska - alarm gdy czas się zgadza (ignoruj datę)
    sAlarm.AlarmMask = RTC_ALARMMASK_DATEWEEKDAY;
    sAlarm.AlarmSubSecondMask = RTC_ALARMSUBSECONDMASK_ALL;
    sAlarm.AlarmDateWeekDaySel = RTC_ALARMDATEWEEKDAYSEL_DATE;
    sAlarm.AlarmDateWeekDay = 1;
    sAlarm.Alarm = RTC_ALARM_A;
    
    if (HAL_RTC_SetAlarm_IT(&hrtc, &sAlarm, RTC_FORMAT_BIN) != HAL_OK) {
        Error_Handler();
    }
    
    // Włącz przerwanie
    HAL_NVIC_SetPriority(RTC_Alarm_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(RTC_Alarm_IRQn);
}

/**
 * @brief  Alarm codziennie o określonej godzinie
 */
void RTC_SetDailyAlarm(uint8_t hour, uint8_t minute)
{
    RTC_AlarmTypeDef sAlarm = {0};
    
    sAlarm.AlarmTime.Hours = hour;
    sAlarm.AlarmTime.Minutes = minute;
    sAlarm.AlarmTime.Seconds = 0;
    
    // Ignoruj sekundy i datę - alarm codziennie o tej samej godzinie
    sAlarm.AlarmMask = RTC_ALARMMASK_DATEWEEKDAY | RTC_ALARMMASK_SECONDS;
    sAlarm.Alarm = RTC_ALARM_A;
    
    HAL_RTC_SetAlarm_IT(&hrtc, &sAlarm, RTC_FORMAT_BIN);
}

/**
 * @brief  Handler przerwania RTC Alarm
 */
void RTC_Alarm_IRQHandler(void)
{
    HAL_RTC_AlarmIRQHandler(&hrtc);
}

/**
 * @brief  Callback alarmu
 */
void HAL_RTC_AlarmAEventCallback(RTC_HandleTypeDef *hrtc)
{
    printf("Alarm A triggered!\r\n");
    
    // Wykonaj akcję
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);  // Toggle LED
}
```

### Alarm w określone dni tygodnia

```c
/**
 * @brief  Alarm w poniedziałki o 7:00
 */
void RTC_SetWeekdayAlarm(void)
{
    RTC_AlarmTypeDef sAlarm = {0};
    
    sAlarm.AlarmTime.Hours = 7;
    sAlarm.AlarmTime.Minutes = 0;
    sAlarm.AlarmTime.Seconds = 0;
    
    sAlarm.AlarmDateWeekDaySel = RTC_ALARMDATEWEEKDAYSEL_WEEKDAY;
    sAlarm.AlarmDateWeekDay = RTC_WEEKDAY_MONDAY;
    sAlarm.AlarmMask = RTC_ALARMMASK_NONE;  // Wszystkie pola muszą się zgadzać
    sAlarm.Alarm = RTC_ALARM_A;
    
    HAL_RTC_SetAlarm_IT(&hrtc, &sAlarm, RTC_FORMAT_BIN);
}
```

## ⏲️ Wake-up Timer

### Okresowe wybudzanie

```c
/**
 * @brief  Wake-up timer (co N sekund)
 */
void RTC_SetWakeupTimer(uint32_t seconds)
{
    // Wake-up co 'seconds' sekund
    // Clock: ck_spre (1 Hz) dla RTC_WAKEUPCLOCK_CK_SPRE_16BITS
    
    if (seconds > 65535) {
        // Dla dłuższych okresów użyj RTC_WAKEUPCLOCK_CK_SPRE_17BITS
        HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, seconds - 1, 
                                    RTC_WAKEUPCLOCK_CK_SPRE_17BITS);
    } else {
        HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, seconds - 1, 
                                    RTC_WAKEUPCLOCK_CK_SPRE_16BITS);
    }
    
    // Włącz przerwanie
    HAL_NVIC_SetPriority(RTC_WKUP_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(RTC_WKUP_IRQn);
}

/**
 * @brief  Handler przerwania Wake-up
 */
void RTC_WKUP_IRQHandler(void)
{
    HAL_RTCEx_WakeUpTimerIRQHandler(&hrtc);
}

/**
 * @brief  Callback wake-up
 */
void HAL_RTCEx_WakeUpTimerEventCallback(RTC_HandleTypeDef *hrtc)
{
    printf("Wake-up timer event!\r\n");
    
    // Wykonaj okresową akcję
    Read_Sensors();
}
```

## 💾 Backup Registers

### Zapis i odczyt danych

```c
/**
 * @brief  Zapis do backup register
 */
void RTC_WriteBackup(uint32_t reg_index, uint32_t data)
{
    // reg_index: 0-19 dla STM32F429
    HAL_PWR_EnableBkUpAccess();
    HAL_RTCEx_BKUPWrite(&hrtc, reg_index, data);
}

/**
 * @brief  Odczyt z backup register
 */
uint32_t RTC_ReadBackup(uint32_t reg_index)
{
    return HAL_RTCEx_BKUPRead(&hrtc, reg_index);
}

/**
 * @brief  Struktura danych w backup
 */
typedef struct {
    uint32_t boot_count;
    uint32_t last_error_code;
    uint32_t config_flags;
    uint32_t checksum;
} BackupData_t;

void Save_BackupData(BackupData_t *data)
{
    data->checksum = data->boot_count ^ data->last_error_code ^ data->config_flags;
    
    RTC_WriteBackup(RTC_BKP_DR0, data->boot_count);
    RTC_WriteBackup(RTC_BKP_DR1, data->last_error_code);
    RTC_WriteBackup(RTC_BKP_DR2, data->config_flags);
    RTC_WriteBackup(RTC_BKP_DR3, data->checksum);
}

void Load_BackupData(BackupData_t *data)
{
    data->boot_count = RTC_ReadBackup(RTC_BKP_DR0);
    data->last_error_code = RTC_ReadBackup(RTC_BKP_DR1);
    data->config_flags = RTC_ReadBackup(RTC_BKP_DR2);
    data->checksum = RTC_ReadBackup(RTC_BKP_DR3);
    
    // Weryfikacja checksum
    uint32_t calc_checksum = data->boot_count ^ data->last_error_code ^ data->config_flags;
    if (calc_checksum != data->checksum) {
        // Dane uszkodzone
        printf("Backup data corrupted!\r\n");
    }
}
```

## 📅 Aplikacje praktyczne

### Zegar cyfrowy

```c
/**
 * @brief  Prosty zegar cyfrowy
 */
void Digital_Clock_Application(void)
{
    RTC_Init();
    
    // Ustaw początkowy czas (jeśli pierwszy start)
    if (RTC_ReadBackup(RTC_BKP_DR0) != 0x32F2) {
        RTC_SetDate(24, 1, 1, RTC_WEEKDAY_MONDAY);
        RTC_SetTime(0, 0, 0);
        RTC_WriteBackup(RTC_BKP_DR0, 0x32F2);  // Marker inicjalizacji
    }
    
    while (1) {
        Print_DateTime();
        HAL_Delay(1000);
    }
}
```

### Logger z timestamp

```c
/**
 * @brief  Timestamp dla logów
 */
typedef struct {
    uint8_t year, month, day;
    uint8_t hour, minute, second;
    char message[64];
} LogEntry_t;

void Log_Event(const char *message)
{
    LogEntry_t log;
    
    // Pobierz timestamp
    RTC_GetDate(&log.year, &log.month, &log.day, NULL);
    RTC_GetTime(&log.hour, &log.minute, &log.second);
    
    // Kopiuj wiadomość
    strncpy(log.message, message, sizeof(log.message) - 1);
    
    // Zapisz do pamięci/SD/Flash
    Save_Log(&log);
    
    printf("[20%02d-%02d-%02d %02d:%02d:%02d] %s\r\n",
           log.year, log.month, log.day,
           log.hour, log.minute, log.second,
           log.message);
}
```

### Automatyczny alarm (budzik)

```c
/**
 * @brief  Programowalny budzik
 */
void Smart_Alarm_Clock(void)
{
    uint8_t alarm_hour = 7;
    uint8_t alarm_minute = 0;
    uint8_t alarm_enabled = 1;
    
    // Odczytaj ustawienia z backup
    alarm_enabled = RTC_ReadBackup(RTC_BKP_DR10);
    alarm_hour = RTC_ReadBackup(RTC_BKP_DR11);
    alarm_minute = RTC_ReadBackup(RTC_BKP_DR12);
    
    if (alarm_enabled) {
        RTC_SetDailyAlarm(alarm_hour, alarm_minute);
        printf("Alarm set for %02d:%02d\r\n", alarm_hour, alarm_minute);
    }
}

void HAL_RTC_AlarmAEventCallback(RTC_HandleTypeDef *hrtc)
{
    // Włącz buzzer/alarm
    Start_Alarm_Sound();
    
    // Włącz światło
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
    
    printf("ALARM! Wake up!\r\n");
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_power_modes|STM32F429I - Tryby niskiego poboru mocy]]
- [[stm32f429i_system_zegarowy|STM32F429I - System zegarowy]]
- [[stm32f429i_przerwania|STM32F429I - Przerwania]]

## 📝 Wzory i obliczenia

### Prescaler calculation
```
RTC_Clock = LSE_Frequency / ((AsynchPrediv + 1) × (SynchPrediv + 1))

Dla LSE 32.768 kHz:
AsynchPrediv = 127
SynchPrediv = 255
RTC_Clock = 32768 / (128 × 256) = 1 Hz ✓
```

### Dokładność czasu
```
LSE drift: ±20 ppm typowy
Error per day = 20 ppm × 86400 s = 1.728 s/day
Error per year ≈ 10.5 minutes

Z kalibracją: < 1 ppm możliwe
```

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
