# STM32F429I - PWM i Generowanie Sygnałów

## 🌊 Pulse Width Modulation (PWM)

### Wprowadzenie
PWM to technika generowania sygnałów o zmiennym wypełnieniu (duty cycle), szeroko stosowana do sterowania mocą, jasnością LED, prędkością silników i generowania sygnałów analogowych.

### Parametry PWM
- **Częstotliwość**: Liczba cykli na sekundę (Hz)
- **Duty Cycle**: Stosunek czasu HIGH do okresu (0-100%)
- **Rozdzielczość**: Liczba możliwych wartości duty cycle

```
     ┌──┐    ┌──┐    ┌──┐
     │  │    │  │    │  │
  ───┘  └────┘  └────┘  └────
  
  Period = 1/Frequency
  Duty Cycle = (Pulse Width / Period) × 100%
```

## ⚙️ Konfiguracja PWM

### Podstawowa konfiguracja PWM

```c
/**
 * @brief  Konfiguracja TIM3 Channel 1 dla PWM
 */
TIM_HandleTypeDef htim3;

void TIM3_PWM_Init(void)
{
    TIM_OC_InitTypeDef sConfigOC = {0};
    
    __HAL_RCC_TIM3_CLK_ENABLE();
    
    // Timer 3 @ 20 kHz PWM
    // Timer clock = 90 MHz (APB1 × 2)
    // PSC = 0 → 90 MHz
    // ARR = 4499 → 90MHz / 4500 = 20 kHz
    
    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 0;
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = 4499;  // ARR value
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    
    if (HAL_TIM_PWM_Init(&htim3) != HAL_OK) {
        Error_Handler();
    }
    
    // Konfiguracja kanału PWM
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 0;  // Początkowy duty cycle (CCR value)
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
    
    if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_1) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Konfiguracja GPIO dla PWM output
 */
void TIM3_PWM_GPIO_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // PA6 = TIM3_CH1
    GPIO_InitStruct.Pin = GPIO_PIN_6;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF2_TIM3;
    
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

/**
 * @brief  Start PWM
 */
void TIM3_PWM_Start(void)
{
    TIM3_PWM_GPIO_Init();
    TIM3_PWM_Init();
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
}
```

### Ustawianie duty cycle

```c
/**
 * @brief  Ustaw duty cycle (0-100%)
 */
void PWM_SetDutyCycle(TIM_HandleTypeDef *htim, uint32_t channel, float duty_percent)
{
    // Oblicz wartość CCR
    uint32_t period = __HAL_TIM_GET_AUTORELOAD(htim);
    uint32_t pulse = (uint32_t)((duty_percent / 100.0f) * period);
    
    // Ustaw wartość CCR
    __HAL_TIM_SET_COMPARE(htim, channel, pulse);
}

/**
 * @brief  Przykład użycia
 */
void PWM_Example(void)
{
    // 50% duty cycle
    PWM_SetDutyCycle(&htim3, TIM_CHANNEL_1, 50.0f);
    
    // 75% duty cycle
    PWM_SetDutyCycle(&htim3, TIM_CHANNEL_1, 75.0f);
    
    // 25% duty cycle
    PWM_SetDutyCycle(&htim3, TIM_CHANNEL_1, 25.0f);
}
```

## 💡 Sterowanie jasnością LED

### Płynne zmiany jasności

```c
/**
 * @brief  Płynne ściemnianie/rozjaśnianie LED
 */
void LED_Breathing_Effect(void)
{
    static float duty = 0.0f;
    static float step = 0.5f;  // Krok zmiany
    
    // Zmiana duty cycle
    duty += step;
    
    // Odwrócenie kierunku na krańcach
    if (duty >= 100.0f) {
        duty = 100.0f;
        step = -0.5f;
    } else if (duty <= 0.0f) {
        duty = 0.0f;
        step = 0.5f;
    }
    
    PWM_SetDutyCycle(&htim3, TIM_CHANNEL_1, duty);
}

/**
 * @brief  Wywołaj w pętli lub timerze
 */
void main_loop(void)
{
    while (1) {
        LED_Breathing_Effect();
        HAL_Delay(10);  // 10ms opóźnienie dla płynności
    }
}
```

### RGB LED z PWM

```c
/**
 * @brief  Struktura RGB LED
 */
typedef struct {
    TIM_HandleTypeDef *tim_red;
    uint32_t channel_red;
    TIM_HandleTypeDef *tim_green;
    uint32_t channel_green;
    TIM_HandleTypeDef *tim_blue;
    uint32_t channel_blue;
} RGB_PWM_LED_t;

/**
 * @brief  Ustawienie koloru RGB (0-255 dla każdego kanału)
 */
void RGB_SetColor(RGB_PWM_LED_t *led, uint8_t red, uint8_t green, uint8_t blue)
{
    float red_percent = (red / 255.0f) * 100.0f;
    float green_percent = (green / 255.0f) * 100.0f;
    float blue_percent = (blue / 255.0f) * 100.0f;
    
    PWM_SetDutyCycle(led->tim_red, led->channel_red, red_percent);
    PWM_SetDutyCycle(led->tim_green, led->channel_green, green_percent);
    PWM_SetDutyCycle(led->tim_blue, led->channel_blue, blue_percent);
}

/**
 * @brief  Przykłady kolorów
 */
void RGB_Examples(RGB_PWM_LED_t *led)
{
    RGB_SetColor(led, 255, 0, 0);      // Czerwony
    HAL_Delay(1000);
    
    RGB_SetColor(led, 0, 255, 0);      // Zielony
    HAL_Delay(1000);
    
    RGB_SetColor(led, 0, 0, 255);      // Niebieski
    HAL_Delay(1000);
    
    RGB_SetColor(led, 255, 255, 0);    // Żółty
    HAL_Delay(1000);
    
    RGB_SetColor(led, 255, 0, 255);    // Magenta
    HAL_Delay(1000);
    
    RGB_SetColor(led, 0, 255, 255);    // Cyan
    HAL_Delay(1000);
    
    RGB_SetColor(led, 255, 255, 255);  // Biały
    HAL_Delay(1000);
}
```

## 🔊 Generowanie dźwięku (Buzzer)

### PWM dla buzzera

```c
/**
 * @brief  Konfiguracja PWM dla buzzera
 */
void Buzzer_Init(void)
{
    TIM_HandleTypeDef htim4;
    TIM_OC_InitTypeDef sConfigOC = {0};
    
    __HAL_RCC_TIM4_CLK_ENABLE();
    
    // Zmienna częstotliwość dla różnych tonów
    htim4.Instance = TIM4;
    htim4.Init.Prescaler = 89;  // 90MHz / 90 = 1 MHz
    htim4.Init.Period = 1000;   // Zmieniane dla różnych częstotliwości
    htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
    
    HAL_TIM_PWM_Init(&htim4);
    
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 500;  // 50% duty cycle
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    
    HAL_TIM_PWM_ConfigChannel(&htim4, &sConfigOC, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_1);
}

/**
 * @brief  Odtwórz ton o określonej częstotliwości
 */
void Buzzer_PlayTone(uint32_t frequency_hz, uint32_t duration_ms)
{
    if (frequency_hz == 0) {
        HAL_TIM_PWM_Stop(&htim4, TIM_CHANNEL_1);
        return;
    }
    
    // Timer clock = 1 MHz (po prescaler)
    uint32_t period = (1000000 / frequency_hz) - 1;
    uint32_t pulse = period / 2;  // 50% duty
    
    __HAL_TIM_SET_AUTORELOAD(&htim4, period);
    __HAL_TIM_SET_COMPARE(&htim4, TIM_CHANNEL_1, pulse);
    
    HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_1);
    HAL_Delay(duration_ms);
    HAL_TIM_PWM_Stop(&htim4, TIM_CHANNEL_1);
}

/**
 * @brief  Odtwórz melodię
 */
#define NOTE_C4  262
#define NOTE_D4  294
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  494
#define NOTE_C5  523

void Buzzer_PlayMelody(void)
{
    // Do-Re-Mi-Fa-Sol-La-Si-Do
    Buzzer_PlayTone(NOTE_C4, 300);
    HAL_Delay(50);
    Buzzer_PlayTone(NOTE_D4, 300);
    HAL_Delay(50);
    Buzzer_PlayTone(NOTE_E4, 300);
    HAL_Delay(50);
    Buzzer_PlayTone(NOTE_F4, 300);
    HAL_Delay(50);
    Buzzer_PlayTone(NOTE_G4, 300);
    HAL_Delay(50);
    Buzzer_PlayTone(NOTE_A4, 300);
    HAL_Delay(50);
    Buzzer_PlayTone(NOTE_B4, 300);
    HAL_Delay(50);
    Buzzer_PlayTone(NOTE_C5, 300);
}
```

## 🚗 Sterowanie silnikiem DC

### PWM + kierunek (H-bridge)

```c
/**
 * @brief  Struktura dla silnika DC
 */
typedef struct {
    TIM_HandleTypeDef *pwm_timer;
    uint32_t pwm_channel;
    GPIO_TypeDef *dir_port;
    uint16_t dir_pin1;
    uint16_t dir_pin2;
} DCMotor_t;

/**
 * @brief  Inicjalizacja silnika DC
 */
void DCMotor_Init(DCMotor_t *motor)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    // GPIO dla kierunku
    GPIO_InitStruct.Pin = motor->dir_pin1 | motor->dir_pin2;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    
    HAL_GPIO_Init(motor->dir_port, &GPIO_InitStruct);
    
    // Start PWM (skonfigurowany wcześniej)
    HAL_TIM_PWM_Start(motor->pwm_timer, motor->pwm_channel);
}

/**
 * @brief  Sterowanie silnikiem
 * @param  speed: -100 do +100 (ujemne = wstecz)
 */
void DCMotor_SetSpeed(DCMotor_t *motor, int8_t speed)
{
    // Kierunek
    if (speed > 0) {
        // Do przodu
        HAL_GPIO_WritePin(motor->dir_port, motor->dir_pin1, GPIO_PIN_SET);
        HAL_GPIO_WritePin(motor->dir_port, motor->dir_pin2, GPIO_PIN_RESET);
    } else if (speed < 0) {
        // Do tyłu
        HAL_GPIO_WritePin(motor->dir_port, motor->dir_pin1, GPIO_PIN_RESET);
        HAL_GPIO_WritePin(motor->dir_port, motor->dir_pin2, GPIO_PIN_SET);
        speed = -speed;  // Wartość bezwzględna
    } else {
        // Stop
        HAL_GPIO_WritePin(motor->dir_port, motor->dir_pin1, GPIO_PIN_RESET);
        HAL_GPIO_WritePin(motor->dir_port, motor->dir_pin2, GPIO_PIN_RESET);
    }
    
    // Prędkość (PWM)
    PWM_SetDutyCycle(motor->pwm_timer, motor->pwm_channel, (float)speed);
}

/**
 * @brief  Przykład użycia
 */
DCMotor_t motor1 = {
    .pwm_timer = &htim3,
    .pwm_channel = TIM_CHANNEL_1,
    .dir_port = GPIOB,
    .dir_pin1 = GPIO_PIN_0,
    .dir_pin2 = GPIO_PIN_1
};

void Motor_Example(void)
{
    DCMotor_Init(&motor1);
    
    DCMotor_SetSpeed(&motor1, 50);   // 50% do przodu
    HAL_Delay(2000);
    
    DCMotor_SetSpeed(&motor1, -50);  // 50% do tyłu
    HAL_Delay(2000);
    
    DCMotor_SetSpeed(&motor1, 0);    // Stop
}
```

## 🔄 Servo motor

### PWM dla serwa (50 Hz, 1-2ms pulse)

```c
/**
 * @brief  Konfiguracja PWM dla servo (50 Hz)
 */
void Servo_Init(void)
{
    TIM_HandleTypeDef htim2;
    TIM_OC_InitTypeDef sConfigOC = {0};
    
    __HAL_RCC_TIM2_CLK_ENABLE();
    
    // Servo wymaga 50 Hz (20 ms okres)
    // Timer clock = 90 MHz
    // PSC = 89 → 1 MHz
    // ARR = 19999 → 1MHz / 20000 = 50 Hz
    
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 89;     // 90MHz / 90 = 1 MHz
    htim2.Init.Period = 19999;     // 20ms period = 50 Hz
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    
    HAL_TIM_PWM_Init(&htim2);
    
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 1500;  // 1.5ms = środek (90°)
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    
    HAL_TIM_PWM_ConfigChannel(&htim2, &sConfigOC, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
}

/**
 * @brief  Ustaw kąt serwa (0-180°)
 */
void Servo_SetAngle(TIM_HandleTypeDef *htim, uint32_t channel, uint8_t angle)
{
    // Servo: 1ms = 0°, 1.5ms = 90°, 2ms = 180°
    // Timer @ 1 MHz: 1 tick = 1 µs
    
    if (angle > 180) angle = 180;
    
    // Mapowanie 0-180° na 1000-2000 µs
    uint32_t pulse = 1000 + ((angle * 1000) / 180);
    
    __HAL_TIM_SET_COMPARE(htim, channel, pulse);
}

/**
 * @brief  Przykład użycia serwa
 */
void Servo_Example(void)
{
    Servo_Init();
    
    Servo_SetAngle(&htim2, TIM_CHANNEL_1, 0);     // 0°
    HAL_Delay(1000);
    
    Servo_SetAngle(&htim2, TIM_CHANNEL_1, 90);    // 90°
    HAL_Delay(1000);
    
    Servo_SetAngle(&htim2, TIM_CHANNEL_1, 180);   // 180°
    HAL_Delay(1000);
    
    // Płynny ruch
    for (uint8_t angle = 0; angle <= 180; angle++) {
        Servo_SetAngle(&htim2, TIM_CHANNEL_1, angle);
        HAL_Delay(10);
    }
}
```

## 🎛️ Zaawansowane tryby PWM

### Complementary PWM (dla mostków H)

```c
/**
 * @brief  PWM komplementarne z dead-time (TIM1/TIM8)
 */
void TIM1_Complementary_PWM_Init(void)
{
    TIM_HandleTypeDef htim1;
    TIM_OC_InitTypeDef sConfigOC = {0};
    TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {0};
    
    __HAL_RCC_TIM1_CLK_ENABLE();
    
    htim1.Instance = TIM1;
    htim1.Init.Prescaler = 0;
    htim1.Init.Period = 8999;  // 20 kHz @ 180 MHz
    htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim1.Init.RepetitionCounter = 0;
    
    HAL_TIM_PWM_Init(&htim1);
    
    // PWM Channel
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = 4500;  // 50% duty
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;  // Complementary
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
    sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;
    sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;
    
    HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1);
    
    // Dead-time configuration
    sBreakDeadTimeConfig.OffStateRunMode = TIM_OSSR_DISABLE;
    sBreakDeadTimeConfig.OffStateIDLEMode = TIM_OSSI_DISABLE;
    sBreakDeadTimeConfig.LockLevel = TIM_LOCKLEVEL_OFF;
    sBreakDeadTimeConfig.DeadTime = 100;  // Dead-time value
    sBreakDeadTimeConfig.BreakState = TIM_BREAK_DISABLE;
    sBreakDeadTimeConfig.BreakPolarity = TIM_BREAKPOLARITY_HIGH;
    sBreakDeadTimeConfig.AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE;
    
    HAL_TIMEx_ConfigBreakDeadTime(&htim1, &sBreakDeadTimeConfig);
    
    // Start complementary PWM
    HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_1);  // Complementary output
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);     // Normal output
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_timery|STM32F429I - Timery i liczniki]]
- [[stm32f429i_gpio|STM32F429I - GPIO]]
- [[stm32f429i_dac|STM32F429I - DAC]]
- [[sensory_i_aktuatory|Sensory i aktuatory]]

## 📝 Wzory i obliczenia

### Obliczanie parametrów PWM
```
PWM_Frequency = Timer_Clock / ((PSC + 1) × (ARR + 1))
Duty_Cycle_% = (CCR / ARR) × 100%
Pulse_Width = (CCR + 1) / Timer_Frequency

Rozdzielczość = ARR + 1
Np. ARR = 999 → 1000 poziomów (0-100.0%)
```

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
