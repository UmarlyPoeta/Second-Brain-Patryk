# STM32F429I - Timery i Liczniki

## ⏱️ Przegląd Timerów

### Rodzaje timerów w STM32F429I

STM32F429I posiada różne typy timerów dostosowane do różnych zastosowań:

| Typ | Liczba | Rozdzielczość | Magistrala | Częstotliwość |
|-----|--------|---------------|-----------|---------------|
| Advanced (TIM1, TIM8) | 2 | 16-bit | APB2 | 180 MHz |
| General-Purpose (TIM2-TIM5) | 4 | 32-bit | APB1 | 90 MHz |
| General-Purpose (TIM9-TIM14) | 6 | 16-bit | APB2/APB1 | 90/180 MHz |
| Basic (TIM6, TIM7) | 2 | 16-bit | APB1 | 90 MHz |

### Możliwości timerów

```
┌─────────────────────────────────────────────┐
│         Advanced Timers (TIM1, TIM8)        │
├─────────────────────────────────────────────┤
│ • PWM (do 6 kanałów + 3 komplementarne)    │
│ • Input Capture / Output Compare           │
│ • Dead-time generation                     │
│ • Break input                              │
│ • Repetition counter                       │
│ • Synchronizacja master/slave              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│    General Purpose Timers (TIM2-TIM5)       │
├─────────────────────────────────────────────┤
│ • 32-bit counter (TIM2, TIM5)              │
│ • PWM (4 kanały)                           │
│ • Input Capture / Output Compare           │
│ • Encoder mode                             │
│ • Trigger input/output                     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│        Basic Timers (TIM6, TIM7)            │
├─────────────────────────────────────────────┤
│ • Proste liczniki up-count                 │
│ • Trigger dla DAC                          │
│ • Timebase dla aplikacji                  │
└─────────────────────────────────────────────┘
```

## 🔧 Podstawowa konfiguracja timera

### Timer jako timebase (1 ms tick)

```c
/**
 * @brief  Konfiguracja TIM2 jako 1ms timebase
 */
TIM_HandleTypeDef htim2;

void TIM2_Init_1ms(void)
{
    __HAL_RCC_TIM2_CLK_ENABLE();
    
    // Timer clock = APB1_Timer = 90 MHz (gdy APB1 = 45 MHz)
    // Prescaler: 90MHz / 9000 = 10 kHz
    // Period: 10kHz / 10 = 1 kHz (1 ms)
    
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 8999;  // 90,000,000 / 9000 = 10,000 Hz
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 9;        // 10,000 / 10 = 1000 Hz (1 ms)
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    
    if (HAL_TIM_Base_Init(&htim2) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Uruchomienie timera z przerwaniem
 */
void TIM2_Start_Interrupt(void)
{
    HAL_NVIC_SetPriority(TIM2_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(TIM2_IRQn);
    
    HAL_TIM_Base_Start_IT(&htim2);
}

/**
 * @brief  Handler przerwania TIM2
 */
void TIM2_IRQHandler(void)
{
    HAL_TIM_IRQHandler(&htim2);
}

/**
 * @brief  Callback wywoływany co 1ms
 */
volatile uint32_t milliseconds = 0;

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM2) {
        milliseconds++;
    }
}
```

### Obliczanie parametrów timera

```c
/**
 * @brief  Funkcja pomocnicza do obliczania PSC i ARR
 * @param  timer_freq: Częstotliwość timera w Hz
 * @param  desired_freq: Pożądana częstotliwość w Hz
 * @param  psc: Wskaźnik na prescaler (output)
 * @param  arr: Wskaźnik na auto-reload (output)
 */
void Calculate_Timer_Parameters(uint32_t timer_freq, 
                                uint32_t desired_freq,
                                uint16_t* psc, 
                                uint32_t* arr)
{
    // Najpierw próbujemy znaleźć dzielnik dający dobrą rozdzielczość
    uint32_t total_div = timer_freq / desired_freq;
    
    // Szukamy optymalnego podziału na PSC i ARR
    *psc = 0;
    *arr = total_div - 1;
    
    // Jeśli ARR > 65535 dla 16-bit timera, zwiększ PSC
    if (*arr > 65535) {
        *psc = (total_div / 65536);
        *arr = (total_div / (*psc + 1)) - 1;
    }
    
    printf("Timer config: PSC=%u, ARR=%lu\r\n", *psc, *arr);
    printf("Actual freq: %lu Hz\r\n", timer_freq / ((*psc + 1) * (*arr + 1)));
}

// Przykład użycia
void Example_Calculate(void)
{
    uint16_t psc;
    uint32_t arr;
    
    // Timer clock = 90 MHz, desired = 1 kHz
    Calculate_Timer_Parameters(90000000, 1000, &psc, &arr);
}
```

## 📊 Input Capture

### Pomiar częstotliwości sygnału

```c
/**
 * @brief  Konfiguracja Input Capture do pomiaru częstotliwości
 */
TIM_HandleTypeDef htim3;
volatile uint32_t capture_value1 = 0;
volatile uint32_t capture_value2 = 0;
volatile uint8_t capture_done = 0;

void TIM3_InputCapture_Init(void)
{
    TIM_IC_InitTypeDef sConfigIC = {0};
    
    __HAL_RCC_TIM3_CLK_ENABLE();
    
    // Timer na maksymalnej częstotliwości
    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 0;  // 90 MHz
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = 0xFFFF;  // Maksymalny zakres
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    
    HAL_TIM_IC_Init(&htim3);
    
    // Konfiguracja Input Capture na kanale 1
    sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;
    sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;
    sConfigIC.ICFilter = 0;
    
    HAL_TIM_IC_ConfigChannel(&htim3, &sConfigIC, TIM_CHANNEL_1);
    
    // Uruchom IC
    HAL_TIM_IC_Start_IT(&htim3, TIM_CHANNEL_1);
}

/**
 * @brief  Callback Input Capture
 */
void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM3 && htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {
        static uint8_t first_capture = 1;
        
        if (first_capture) {
            capture_value1 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
            first_capture = 0;
        } else {
            capture_value2 = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
            first_capture = 1;
            capture_done = 1;
        }
    }
}

/**
 * @brief  Obliczenie częstotliwości z wartości IC
 */
float Calculate_Frequency(void)
{
    if (!capture_done) return 0.0f;
    
    uint32_t difference;
    
    if (capture_value2 > capture_value1) {
        difference = capture_value2 - capture_value1;
    } else {
        // Overflow
        difference = (0xFFFF - capture_value1) + capture_value2 + 1;
    }
    
    // Timer clock = 90 MHz
    float frequency = 90000000.0f / difference;
    
    capture_done = 0;
    return frequency;
}
```

### Pomiar szerokości impulsu (PWM Input)

```c
/**
 * @brief  Pomiar duty cycle i częstotliwości PWM
 */
volatile uint32_t pwm_period = 0;
volatile uint32_t pwm_duty = 0;

void TIM4_PWM_Input_Init(void)
{
    TIM_IC_InitTypeDef sConfigIC = {0};
    TIM_SlaveConfigTypeDef sSlaveConfig = {0};
    
    __HAL_RCC_TIM4_CLK_ENABLE();
    
    htim4.Instance = TIM4;
    htim4.Init.Prescaler = 89;  // 90MHz / 90 = 1 MHz
    htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim4.Init.Period = 0xFFFF;
    htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    
    HAL_TIM_IC_Init(&htim4);
    
    // Kanał 1 - pomiar okresu
    sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;
    sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;
    sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;
    sConfigIC.ICFilter = 0;
    HAL_TIM_IC_ConfigChannel(&htim4, &sConfigIC, TIM_CHANNEL_1);
    
    // Kanał 2 - pomiar duty cycle (na tym samym wejściu)
    sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_FALLING;
    sConfigIC.ICSelection = TIM_ICSELECTION_INDIRECTTI;
    HAL_TIM_IC_ConfigChannel(&htim4, &sConfigIC, TIM_CHANNEL_2);
    
    // Konfiguracja slave mode
    sSlaveConfig.SlaveMode = TIM_SLAVEMODE_RESET;
    sSlaveConfig.InputTrigger = TIM_TS_TI1FP1;
    HAL_TIM_SlaveConfigSynchro(&htim4, &sSlaveConfig);
    
    // Start PWM Input mode
    HAL_TIM_IC_Start_IT(&htim4, TIM_CHANNEL_1);
    HAL_TIM_IC_Start_IT(&htim4, TIM_CHANNEL_2);
}

void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM4) {
        if (htim->Channel == HAL_TIM_ACTIVE_CHANNEL_1) {
            pwm_period = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_1);
        } else if (htim->Channel == HAL_TIM_ACTIVE_CHANNEL_2) {
            pwm_duty = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_2);
        }
    }
}

/**
 * @brief  Oblicz częstotliwość i duty cycle
 */
void Get_PWM_Parameters(float* freq, float* duty_percent)
{
    if (pwm_period > 0) {
        // Timer clock = 1 MHz (po prescaler)
        *freq = 1000000.0f / pwm_period;
        *duty_percent = ((float)pwm_duty / pwm_period) * 100.0f;
    }
}
```

## ⚙️ Encoder Mode

### Konfiguracja trybu enkodera

```c
/**
 * @brief  Konfiguracja TIM3 jako enkoder
 */
TIM_HandleTypeDef htim3;

void TIM3_Encoder_Init(void)
{
    TIM_Encoder_InitTypeDef sConfig = {0};
    
    __HAL_RCC_TIM3_CLK_ENABLE();
    
    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 0;
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = 0xFFFF;  // 16-bit
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    
    // Tryb enkodera - oba zbocza na obu kanałach
    sConfig.EncoderMode = TIM_ENCODERMODE_TI12;
    
    // Konfiguracja kanału 1 (A)
    sConfig.IC1Polarity = TIM_ICPOLARITY_RISING;
    sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;
    sConfig.IC1Prescaler = TIM_ICPSC_DIV1;
    sConfig.IC1Filter = 10;  // Filtrowanie drgań
    
    // Konfiguracja kanału 2 (B)
    sConfig.IC2Polarity = TIM_ICPOLARITY_RISING;
    sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;
    sConfig.IC2Prescaler = TIM_ICPSC_DIV1;
    sConfig.IC2Filter = 10;
    
    HAL_TIM_Encoder_Init(&htim3, &sConfig);
    HAL_TIM_Encoder_Start(&htim3, TIM_CHANNEL_ALL);
}

/**
 * @brief  Odczyt pozycji enkodera
 */
int32_t Get_Encoder_Position(void)
{
    return (int32_t)__HAL_TIM_GET_COUNTER(&htim3);
}

/**
 * @brief  Odczyt kierunku obrotu
 */
int8_t Get_Encoder_Direction(void)
{
    // 1 = do przodu, -1 = do tyłu
    return __HAL_TIM_IS_TIM_COUNTING_DOWN(&htim3) ? -1 : 1;
}

/**
 * @brief  Reset pozycji enkodera
 */
void Reset_Encoder_Position(void)
{
    __HAL_TIM_SET_COUNTER(&htim3, 0);
}
```

## 🔄 Timer Synchronization

### Master-Slave Configuration

```c
/**
 * @brief  TIM1 jako master, TIM2 jako slave
 */
void TIM_MasterSlave_Config(void)
{
    TIM_HandleTypeDef htim1, htim2;
    TIM_MasterConfigTypeDef sMasterConfig = {0};
    TIM_SlaveConfigTypeDef sSlaveConfig = {0};
    
    // TIM1 jako Master
    __HAL_RCC_TIM1_CLK_ENABLE();
    htim1.Instance = TIM1;
    htim1.Init.Prescaler = 179;  // 180MHz / 180 = 1 MHz
    htim1.Init.Period = 999;     // 1 MHz / 1000 = 1 kHz
    HAL_TIM_Base_Init(&htim1);
    
    // Master Output Trigger (TRGO)
    sMasterConfig.MasterOutputTrigger = TIM_TRGO_UPDATE;
    sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_ENABLE;
    HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig);
    
    // TIM2 jako Slave (uruchamiany przez TIM1)
    __HAL_RCC_TIM2_CLK_ENABLE();
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 0;
    htim2.Init.Period = 999;
    HAL_TIM_Base_Init(&htim2);
    
    // Konfiguracja slave
    sSlaveConfig.SlaveMode = TIM_SLAVEMODE_TRIGGER;  // Start na trigger
    sSlaveConfig.InputTrigger = TIM_TS_ITR0;  // ITR0 = TIM1
    HAL_TIM_SlaveConfigSynchro(&htim2, &sSlaveConfig);
    
    // Uruchom TIM1 (TIM2 wystartuje automatycznie)
    HAL_TIM_Base_Start(&htim1);
}
```

## 🎯 One-Pulse Mode

```c
/**
 * @brief  Generowanie pojedynczego impulsu o określonej szerokości
 */
void TIM_OnePulse_Config(uint32_t pulse_width_us)
{
    TIM_HandleTypeDef htim9;
    TIM_OnePulse_InitTypeDef sConfig = {0};
    
    __HAL_RCC_TIM9_CLK_ENABLE();
    
    // Timer clock = 180 MHz, prescaler dla 1 MHz (1 us tick)
    htim9.Instance = TIM9;
    htim9.Init.Prescaler = 179;  // 180MHz / 180 = 1 MHz
    htim9.Init.Period = pulse_width_us;
    htim9.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim9.Init.CounterMode = TIM_COUNTERMODE_UP;
    
    HAL_TIM_OnePulse_Init(&htim9, TIM_OPMODE_SINGLE);
    
    // Konfiguracja kanału
    sConfig.OCMode = TIM_OCMODE_PWM2;
    sConfig.Pulse = pulse_width_us / 2;  // 50% duty
    sConfig.OCPolarity = TIM_OCPOLARITY_HIGH;
    HAL_TIM_OnePulse_ConfigChannel(&htim9, &sConfig, TIM_CHANNEL_1, TIM_CHANNEL_2);
    
    // Impuls zostanie wygenerowany po wystartowaniu
    HAL_TIM_OnePulse_Start(&htim9, TIM_CHANNEL_1);
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_pwm|STM32F429I - PWM]]
- [[stm32f429i_przerwania|STM32F429I - Przerwania]]
- [[stm32f429i_system_zegarowy|STM32F429I - System zegarowy]]
- [[stm32f429i_dma|STM32F429I - DMA]]

## 📝 Wzory i obliczenia

### Podstawowe wzory
```
Timer_Frequency = Timer_Clock / (Prescaler + 1)
Update_Frequency = Timer_Frequency / (Period + 1)
Update_Period = 1 / Update_Frequency

Dla 16-bit timera:
Max_Period = 65536 ticks

Dla 32-bit timera (TIM2, TIM5):
Max_Period = 4294967296 ticks
```

### Przykłady obliczeń
```
Cel: 1 kHz przy timer clock = 90 MHz

Metoda 1: PSC=8999, ARR=9
- 90,000,000 / 9000 = 10,000 Hz
- 10,000 / 10 = 1,000 Hz ✓

Metoda 2: PSC=89, ARR=999
- 90,000,000 / 90 = 1,000,000 Hz
- 1,000,000 / 1000 = 1,000 Hz ✓
```

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
