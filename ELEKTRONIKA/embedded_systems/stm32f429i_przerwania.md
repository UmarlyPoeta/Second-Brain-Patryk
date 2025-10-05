# STM32F429I - Przerwania i NVIC

## 🎯 Nested Vectored Interrupt Controller (NVIC)

### Wprowadzenie
NVIC to kontroler przerwań w rdzeniu ARM Cortex-M4, który zarządza wszystkimi przerwaniami w mikrokontrolerze STM32F429I. Umożliwia zaawansowane zarządzanie priorytetami i zagnieżdżanie przerwań.

## 📊 Charakterystyka NVIC w STM32F429I

### Podstawowe informacje
- **Liczba przerwań zewnętrznych**: 82 linie IRQ
- **Poziomy priorytetów**: 16 (4 bity konfiguracyjne)
- **Priorytety preemptive**: Tak (zagnieżdżanie przerwań)
- **Sub-priorytety**: Tak (kolejkowanie przy tym samym priorytecie)

### Tabela wektorów przerwań (wybrane)
| IRQ Number | Przerwanie | Opis |
|------------|------------|------|
| -14 | NMI | Non-Maskable Interrupt |
| -13 | HardFault | Błąd krytyczny |
| -5 | SVCall | Supervisor call |
| -2 | PendSV | Pendable service request |
| -1 | SysTick | Timer systemowy |
| 0-6 | EXTI0-4, EXTI9_5, EXTI15_10 | Przerwania zewnętrzne |
| 18 | DMA1_Stream0 | DMA Stream 0 |
| 27 | TIM1_UP_TIM10 | Timer 1 update |
| 28 | TIM1_CC | Timer 1 capture/compare |
| 38 | USART1 | USART1 global |
| 56 | TIM6_DAC | Timer 6 i DAC |
| 67 | OTG_FS | USB OTG Full Speed |

## 🔧 Konfiguracja priorytetów

### Priority Grouping
STM32F429I używa 4-bitowych priorytetów (0-15), które można podzielić na:
- **Preemption Priority**: Może przerwać inne przerwanie o niższym priorytecie
- **Sub Priority**: Kolejność obsługi przy tym samym priorytecie preemption

```c
/**
 * @brief  Konfiguracja grupowania priorytetów
 */
void NVIC_PriorityGroup_Config(void)
{
    // Domyślna konfiguracja STM32: GROUP 4
    // 4 bity preemption (0-15), 0 bitów sub-priority
    HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_4);
    
    // Inne możliwości:
    // NVIC_PRIORITYGROUP_0: 0 bitów preempt, 4 bity sub (16 sub-priorytetów)
    // NVIC_PRIORITYGROUP_1: 1 bit preempt, 3 bity sub (2 preempt, 8 sub)
    // NVIC_PRIORITYGROUP_2: 2 bity preempt, 2 bity sub (4 preempt, 4 sub)
    // NVIC_PRIORITYGROUP_3: 3 bity preempt, 1 bit sub (8 preempt, 2 sub)
    // NVIC_PRIORITYGROUP_4: 4 bity preempt, 0 bitów sub (16 preempt, 1 sub)
}
```

### Ustawianie priorytetów

```c
/**
 * @brief  Przykład konfiguracji priorytetów różnych przerwań
 */
void Configure_Interrupt_Priorities(void)
{
    // Wysoki priorytet dla krytycznych operacji
    // Timer 1 - priorytet 0 (najwyższy)
    HAL_NVIC_SetPriority(TIM1_UP_TIM10_IRQn, 0, 0);
    
    // USART - priorytet 5
    HAL_NVIC_SetPriority(USART1_IRQn, 5, 0);
    
    // EXTI (przycisk) - priorytet 10
    HAL_NVIC_SetPriority(EXTI15_10_IRQn, 10, 0);
    
    // DMA - priorytet 3
    HAL_NVIC_SetPriority(DMA1_Stream0_IRQn, 3, 0);
    
    // Niższy priorytet dla mniej krytycznych operacji
    HAL_NVIC_SetPriority(TIM6_DAC_IRQn, 15, 0);
}
```

## 🔄 Przerwania zewnętrzne (EXTI)

### Linie EXTI
- **EXTI0 - EXTI15**: Połączone z pinami GPIO
- **EXTI16**: PVD (Power Voltage Detector)
- **EXTI17**: RTC Alarm
- **EXTI18**: USB OTG FS Wakeup
- **EXTI19**: Ethernet Wakeup
- **EXTI20**: USB OTG HS Wakeup
- **EXTI21**: RTC Tamper/Timestamp
- **EXTI22**: RTC Wakeup

### Konfiguracja EXTI GPIO

```c
/**
 * @brief  Konfiguracja przerwania na przycisku
 */
void Button_EXTI_Config(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    // Włącz zegar portu
    __HAL_RCC_GPIOC_CLK_ENABLE();
    
    // Konfiguracja pinu PC13 (przycisk USER)
    GPIO_InitStruct.Pin = GPIO_PIN_13;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;  // Przerwanie na zbocze opadające
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
    
    // Konfiguracja NVIC dla EXTI15_10
    HAL_NVIC_SetPriority(EXTI15_10_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);
}

/**
 * @brief  Handler przerwania
 */
void EXTI15_10_IRQHandler(void)
{
    // HAL obsługuje sprawdzanie źródła przerwania
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_13);
}

/**
 * @brief  Callback wywoływany po obsłudze przerwania
 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_13) {
        // Akcja po wciśnięciu przycisku
        Button_Pressed_Flag = 1;
    }
}
```

### Obsługa wielu linii EXTI

```c
/**
 * @brief  Obsługa wielu przycisków na różnych liniach EXTI
 */
volatile uint8_t button_flags = 0;

#define BUTTON1_FLAG (1 << 0)
#define BUTTON2_FLAG (1 << 1)
#define BUTTON3_FLAG (1 << 2)

void Multiple_Buttons_Init(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    
    // Button 1 na PA0 (EXTI0)
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;
    GPIO_InitStruct.Pull = GPIO_PULLDOWN;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    HAL_NVIC_SetPriority(EXTI0_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
    
    // Button 2 na PB1 (EXTI1)
    GPIO_InitStruct.Pin = GPIO_PIN_1;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
    HAL_NVIC_SetPriority(EXTI1_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(EXTI1_IRQn);
    
    // Button 3 na PA5 (EXTI9_5)
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    HAL_NVIC_SetPriority(EXTI9_5_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(EXTI9_5_IRQn);
}

// Handlery
void EXTI0_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
}

void EXTI1_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_1);
}

void EXTI9_5_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_5);
}

void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    switch(GPIO_Pin) {
        case GPIO_PIN_0:
            button_flags |= BUTTON1_FLAG;
            break;
        case GPIO_PIN_1:
            button_flags |= BUTTON2_FLAG;
            break;
        case GPIO_PIN_5:
            button_flags |= BUTTON3_FLAG;
            break;
    }
}
```

## ⏱️ SysTick Timer

### Charakterystyka
- **Szerokość**: 24-bit downcounter
- **Częstotliwość**: Typowo HCLK/8 lub HCLK
- **Zastosowanie**: HAL_Delay(), timebase dla RTOS

### Konfiguracja SysTick

```c
/**
 * @brief  Inicjalizacja SysTick (wykonywana przez HAL_Init)
 */
void SysTick_Config_Example(void)
{
    // SysTick skonfigurowany na 1ms tick
    // Przy HCLK = 180 MHz: 180000000 / 1000 = 180000 ticków
    HAL_SYSTICK_Config(SystemCoreClock / 1000);  // 1 ms tick
    
    // Priorytet SysTick (najniższy możliwy dla RTOS)
    HAL_NVIC_SetPriority(SysTick_IRQn, 15, 0);
}

/**
 * @brief  Handler SysTick (wywoływany co 1ms)
 */
void SysTick_Handler(void)
{
    HAL_IncTick();  // Inkrementacja licznika HAL
    
    // Własny kod można dodać tutaj
    // UWAGA: Powinien być jak najkrótszy!
}

/**
 * @brief  Własny callback SysTick (1kHz)
 */
void HAL_SYSTICK_Callback(void)
{
    // Wywoływane co 1ms
    static uint32_t counter = 0;
    counter++;
    
    if (counter >= 1000) {  // Co 1 sekundę
        counter = 0;
        // Akcja co sekundę
        seconds_counter++;
    }
}
```

## 🎭 Przerwania timerów

### Timer Update Interrupt

```c
/**
 * @brief  Konfiguracja przerwania timera
 */
void TIM2_Interrupt_Config(void)
{
    TIM_HandleTypeDef htim2;
    
    __HAL_RCC_TIM2_CLK_ENABLE();
    
    // Timer 2 na 1 kHz (1ms)
    // Timer clock = 90 MHz (APB1 × 2)
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 8999;      // 90MHz / 9000 = 10 kHz
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 9;            // 10kHz / 10 = 1 kHz
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    
    HAL_TIM_Base_Init(&htim2);
    
    // Włącz przerwanie update
    HAL_NVIC_SetPriority(TIM2_IRQn, 3, 0);
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
 * @brief  Callback update timera
 */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM2) {
        // Kod wykonywany co 1ms
        millisecond_flag = 1;
    }
}
```

## 📡 Przerwania komunikacyjne

### UART Interrupt

```c
/**
 * @brief  Przerwanie odbioru UART
 */
uint8_t rx_buffer[100];
volatile uint8_t rx_index = 0;

void USART1_RX_Interrupt_Config(void)
{
    // Konfiguracja USART (przykład uproszczony)
    __HAL_UART_ENABLE_IT(&huart1, UART_IT_RXNE);  // RX Not Empty
    
    HAL_NVIC_SetPriority(USART1_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(USART1_IRQn);
}

void USART1_IRQHandler(void)
{
    HAL_UART_IRQHandler(&huart1);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1) {
        // Odebrano bajt
        uint8_t received_byte = huart->Instance->DR;
        
        if (rx_index < sizeof(rx_buffer)) {
            rx_buffer[rx_index++] = received_byte;
        }
        
        // Sprawdź koniec linii
        if (received_byte == '\n') {
            // Przetwórz całą linię
            Process_Command(rx_buffer, rx_index);
            rx_index = 0;
        }
    }
}
```

## 🚨 Obsługa błędów i wyjątków

### Hard Fault Handler

```c
/**
 * @brief  Handler błędu krytycznego
 */
void HardFault_Handler(void)
{
    // Zapisz stan dla debugowania
    volatile uint32_t* stack_ptr;
    
    // Pobierz wskaźnik stosu
    __asm volatile ("MRS %0, MSP" : "=r" (stack_ptr));
    
    // Stack frame zawiera:
    // stack_ptr[0] = R0
    // stack_ptr[1] = R1
    // stack_ptr[2] = R2
    // stack_ptr[3] = R3
    // stack_ptr[4] = R12
    // stack_ptr[5] = LR (Link Register)
    // stack_ptr[6] = PC (Program Counter) - adres błędu
    // stack_ptr[7] = xPSR
    
    uint32_t fault_pc = stack_ptr[6];
    
    // Nieskończona pętla lub reset
    while(1) {
        // Blink LED lub inna sygnalizacja błędu
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        for(volatile uint32_t i = 0; i < 1000000; i++);
    }
}
```

### Usage Fault (wymaga włączenia)

```c
/**
 * @brief  Włączenie Usage Fault
 */
void Enable_UsageFault(void)
{
    // Włącz Usage Fault exception
    SCB->SHCSR |= SCB_SHCSR_USGFAULTENA_Msk;
}

void UsageFault_Handler(void)
{
    // Obsługa błędów użytkowania:
    // - Dzielenie przez zero
    // - Nieprawidłowe wyrównanie
    // - Nieprawidłowa instrukcja
    
    uint32_t ufsr = SCB->CFSR & 0xFFFF;  // Usage Fault Status Register
    
    if (ufsr & (1 << 9)) {
        // Dzielenie przez zero
    }
    
    while(1);
}
```

## 💡 Best Practices

### Zasady programowania przerwań

```c
/**
 * @brief  Dobre praktyki w przerwaniach
 */

// ❌ ZŁE - długie operacje w przerwaniu
void BAD_IRQHandler(void)
{
    HAL_Delay(100);  // NIGDY nie używaj delay w przerwaniu!
    printf("Long operation");  // I/O operations są wolne
}

// ✅ DOBRE - krótkie, ustawienie flagi
volatile uint8_t event_flag = 0;

void GOOD_IRQHandler(void)
{
    // Tylko ustawienie flagi
    event_flag = 1;
    
    // Ewentualnie szybka operacja
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
}

// Obsługa w main loop
void main_loop(void)
{
    if (event_flag) {
        event_flag = 0;
        
        // Długa operacja w main loop
        Process_Event();
    }
}
```

### Ochrona danych współdzielonych

```c
/**
 * @brief  Atomic operations dla zmiennych współdzielonych
 */
volatile uint32_t shared_counter = 0;

// W przerwaniu
void ISR_Increment(void)
{
    shared_counter++;  // Atomic dla 32-bit na Cortex-M4
}

// W main
void Main_Read(void)
{
    // Wyłącz przerwania na czas odczytu (jeśli > 32-bit)
    __disable_irq();
    uint32_t local_copy = shared_counter;
    __enable_irq();
    
    // Użyj local_copy
}

// Dla operacji nieatomowych
void Complex_Shared_Update(void)
{
    __disable_irq();
    // Operacje na współdzielonych danych
    shared_struct.field1 = value1;
    shared_struct.field2 = value2;
    __enable_irq();
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_architektura|STM32F429I - Architektura]]
- [[stm32f429i_gpio|STM32F429I - GPIO]]
- [[stm32f429i_timery|STM32F429I - Timery]]
- [[stm32f429i_dma|STM32F429I - DMA]]

## 📝 Checklist konfiguracji przerwań

- [ ] Ustaw priority grouping (zwykle PRIORITYGROUP_4)
- [ ] Skonfiguruj priorytety zgodnie z ważnością
- [ ] Włącz zegar peryferyjnego
- [ ] Skonfiguruj peryferyjne (GPIO, Timer, UART, etc.)
- [ ] Ustaw priorytet przerwania w NVIC
- [ ] Włącz przerwanie w NVIC
- [ ] Zaimplementuj handler i callback
- [ ] Testuj zagnieżdżanie przerwań
- [ ] Sprawdź czas wykonania ISR (powinien być < 10% czasu)

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
