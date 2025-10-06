# STM32F429I - System Zegarowy i Konfiguracja RCC

## ⏰ Reset and Clock Control (RCC)

### Wprowadzenie
RCC (Reset and Clock Control) to peryferyjne odpowiedzialne za zarządzanie zegarami w mikrokontrolerze STM32F429I. Prawidłowa konfiguracja systemu zegarowego jest kluczowa dla działania wszystkich peryferyjnych i osiągnięcia maksymalnej wydajności.

## 🎯 Źródła zegarów

### Główne źródła zegarów

```
┌─────────────────────────────────────────────────────┐
│              Źródła zegarów                         │
│                                                      │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐   │
│  │  HSI   │  │  HSE   │  │  PLL   │  │  LSI   │   │
│  │ 16 MHz │  │ 8-26   │  │ Main   │  │ 32 kHz │   │
│  │Internal│  │ MHz    │  │        │  │Internal│   │
│  │        │  │External│  │        │  │        │   │
│  └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘   │
│      │           │           │           │         │
│      └───────┬───┴───────┬───┘           │         │
│              │           │               │         │
│         ┌────▼───────────▼────┐     ┌────▼────┐   │
│         │    System Clock     │     │   LSE   │   │
│         │      Mux            │     │ 32.768  │   │
│         └─────────┬───────────┘     │  kHz    │   │
│                   │                 └─────────┘   │
│              ┌────▼────┐                          │
│              │ SYSCLK  │                          │
│              │180 MHz  │                          │
│              └─────────┘                          │
└─────────────────────────────────────────────────────┘
```

#### HSI (High-Speed Internal)
- **Częstotliwość**: 16 MHz ±1%
- **Charakterystyka**: 
  - Wbudowany oscylator RC
  - Szybki start (~2 µs)
  - Mniejsza dokładność niż HSE
  - Wrażliwy na temperaturę i napięcie

#### HSE (High-Speed External)
- **Częstotliwość**: 4-26 MHz (typowo 8 MHz)
- **Charakterystyka**:
  - Wymaga zewnętrznego kwarcu lub oscylatora
  - Wysoka dokładność (±50 ppm)
  - Dłuższy czas startu (~2 ms dla kwarcu)
  - Stabilny w szerokim zakresie temperatur

#### LSI (Low-Speed Internal)
- **Częstotliwość**: 32 kHz ±47%
- **Zastosowanie**: 
  - Watchdog (IWDG)
  - RTC w trybie low-power

#### LSE (Low-Speed External)
- **Częstotliwość**: 32.768 kHz
- **Zastosowanie**:
  - RTC (Real-Time Clock)
  - Precyzyjne odmierzanie czasu

## 🔧 PLL (Phase-Locked Loop)

### Konfiguracja PLL

```
       HSE/HSI
          │
      ┌───▼───┐
      │  /M   │  VCO input: 1-2 MHz (zalecane)
      └───┬───┘
          │
      ┌───▼───┐
      │  ×N   │  VCO output: 100-432 MHz
      └───┬───┘
          │
    ┌─────┼─────┐
    │     │     │
┌───▼─┐ ┌─▼──┐ ┌▼──┐
│ /P  │ │ /Q │ │/R │
└──┬──┘ └─┬──┘ └┬──┘
   │      │     │
SYSCLK  USB   SAI
180MHz  48MHz
```

### Parametry PLL
- **M (dzielnik wejściowy)**: 2-63
- **N (mnożnik)**: 50-432
- **P (dzielnik główny)**: 2, 4, 6, 8
- **Q (dzielnik USB/SDIO)**: 2-15
- **R (dzielnik SAI)**: 2-7

### Formuła PLL
```
VCO_IN = HSE / M         (musi być 1-2 MHz)
VCO_OUT = VCO_IN × N     (musi być 100-432 MHz)
SYSCLK = VCO_OUT / P     (max 180 MHz)
USB_CLK = VCO_OUT / Q    (powinno być 48 MHz dla USB)
```

### Przykład konfiguracji PLL

```c
/**
 * @brief  Konfiguracja PLL dla 180 MHz z HSE 8 MHz
 */
void PLL_Config_180MHz(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    
    // HSE jako źródło PLL
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
    RCC_OscInitStruct.HSEState = RCC_HSE_ON;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
    
    // Obliczenia:
    // VCO_IN = 8 MHz / 8 = 1 MHz ✓
    // VCO_OUT = 1 MHz × 360 = 360 MHz ✓
    // SYSCLK = 360 MHz / 2 = 180 MHz ✓
    // USB_CLK = 360 MHz / 7.5 = 48 MHz ✓
    
    RCC_OscInitStruct.PLL.PLLM = 8;    // Dzielnik wejściowy
    RCC_OscInitStruct.PLL.PLLN = 360;  // Mnożnik
    RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2; // Dzielnik SYSCLK
    RCC_OscInitStruct.PLL.PLLQ = 7;    // Dzielnik USB (360/7.5=48MHz)
    
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
        Error_Handler();
    }
}
```

## ⚡ Over-Drive Mode

### Wymagania dla 180 MHz
Dla osiągnięcia maksymalnej częstotliwości 180 MHz wymagane jest włączenie trybu Over-Drive:

```c
/**
 * @brief  Włączenie Over-Drive Mode
 */
HAL_StatusTypeDef Enable_OverDrive(void)
{
    HAL_StatusTypeDef status;
    
    // Włącz zegar PWR
    __HAL_RCC_PWR_CLK_ENABLE();
    
    // Ustaw skalowanie napięcia na Scale 1
    __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
    
    // Poczekaj na ustabilizowanie napięcia
    while(__HAL_PWR_GET_FLAG(PWR_FLAG_VOSRDY) == RESET) {}
    
    // Włącz Over-Drive
    status = HAL_PWREx_EnableOverDrive();
    
    return status;
}
```

## 🚌 Konfiguracja zegarów magistral

### Dzielniki zegarów

```c
/**
 * @brief  Konfiguracja zegarów systemowych i magistral
 */
void System_Clock_Config(void)
{
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
    
    // Konfiguracja wszystkich zegarów systemowych
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK |      // AHB
                                  RCC_CLOCKTYPE_SYSCLK |    // System
                                  RCC_CLOCKTYPE_PCLK1 |     // APB1
                                  RCC_CLOCKTYPE_PCLK2;      // APB2
    
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    
    // HCLK = SYSCLK / 1 = 180 MHz (AHB)
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    
    // PCLK1 = HCLK / 4 = 45 MHz (APB1, max 45 MHz)
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
    
    // PCLK2 = HCLK / 2 = 90 MHz (APB2, max 90 MHz)
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;
    
    // FLASH_LATENCY_5: 5 cykli wait state dla 180 MHz @ 3.3V
    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK) {
        Error_Handler();
    }
}
```

### Maksymalne częstotliwości magistral
| Magistrala | Max częstotliwość | Dzielnik dla 180 MHz |
|------------|-------------------|----------------------|
| SYSCLK     | 180 MHz          | /1                   |
| AHB (HCLK) | 180 MHz          | /1                   |
| APB1       | 45 MHz           | /4                   |
| APB2       | 90 MHz           | /2                   |

## 🔌 Włączanie zegarów peryferyjnych

### Makra HAL do włączania zegarów

```c
/**
 * @brief  Przykłady włączania zegarów peryferyjnych
 */
void Enable_Peripheral_Clocks(void)
{
    // GPIO (magistrala AHB1)
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();
    
    // DMA (magistrala AHB1)
    __HAL_RCC_DMA1_CLK_ENABLE();
    __HAL_RCC_DMA2_CLK_ENABLE();
    
    // Timery (magistrala APB1)
    __HAL_RCC_TIM2_CLK_ENABLE();
    __HAL_RCC_TIM3_CLK_ENABLE();
    
    // Timery zaawansowane (magistrala APB2)
    __HAL_RCC_TIM1_CLK_ENABLE();
    
    // USART (magistrala APB2)
    __HAL_RCC_USART1_CLK_ENABLE();
    
    // USART (magistrala APB1)
    __HAL_RCC_USART2_CLK_ENABLE();
    
    // SPI (magistrala APB2)
    __HAL_RCC_SPI1_CLK_ENABLE();
    
    // I2C (magistrala APB1)
    __HAL_RCC_I2C1_CLK_ENABLE();
    
    // ADC (magistrala APB2)
    __HAL_RCC_ADC1_CLK_ENABLE();
    
    // USB OTG FS (magistrala AHB2)
    __HAL_RCC_USB_OTG_FS_CLK_ENABLE();
}
```

### Zegary timerów
**Ważne**: Zegary timerów są automatycznie mnożone gdy dzielnik APB != 1:
- APB1 Timer Clock = APB1_CLK × 2 = 90 MHz (gdy APB1 = 45 MHz)
- APB2 Timer Clock = APB2_CLK × 2 = 180 MHz (gdy APB2 = 90 MHz)

```c
/**
 * @brief  Odczyt częstotliwości zegarów timerów
 */
uint32_t Get_Timer_Clock(TIM_TypeDef* TIMx)
{
    uint32_t pclk, tim_clk;
    
    // Sprawdź na której magistrali jest timer
    if ((TIMx == TIM1) || (TIMx == TIM8) || (TIMx == TIM9) ||
        (TIMx == TIM10) || (TIMx == TIM11)) {
        // Timer na APB2
        pclk = HAL_RCC_GetPCLK2Freq();
        // Jeśli dzielnik APB2 != 1, timer clock = PCLK2 × 2
        if ((RCC->CFGR & RCC_CFGR_PPRE2) != 0) {
            tim_clk = pclk * 2;
        } else {
            tim_clk = pclk;
        }
    } else {
        // Timer na APB1
        pclk = HAL_RCC_GetPCLK1Freq();
        // Jeśli dzielnik APB1 != 1, timer clock = PCLK1 × 2
        if ((RCC->CFGR & RCC_CFGR_PPRE1) != 0) {
            tim_clk = pclk * 2;
        } else {
            tim_clk = pclk;
        }
    }
    
    return tim_clk;
}
```

## 🛡️ Clock Security System (CSS)

### CSS - Zabezpieczenie zegara

```c
/**
 * @brief  Włączenie Clock Security System
 */
void Enable_CSS(void)
{
    // CSS monitoruje HSE i przełącza na HSI w przypadku awarii
    HAL_RCC_EnableCSS();
}

/**
 * @brief  Callback awarii HSE
 */
void HAL_RCC_CSSCallback(void)
{
    // HSE zawiódł - system przełączył się na HSI
    // Obsługa błędu (np. LED, log, restart)
    
    // Próba ponownej inicjalizacji HSE
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
    RCC_OscInitStruct.HSEState = RCC_HSE_ON;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
    
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) == HAL_OK) {
        // HSE przywrócony
    }
}
```

## 📊 RTC Clock Configuration

### Konfiguracja zegara RTC

```c
/**
 * @brief  Konfiguracja RTC z LSE
 */
void RTC_Clock_Config(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};
    
    // Włącz LSE
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
    
    // Włącz zegar RTC
    __HAL_RCC_RTC_ENABLE();
}
```

## 🔍 Diagnostyka zegarów

### MCO (Microcontroller Clock Output)

```c
/**
 * @brief  Wyprowadzenie zegarów na piny MCO
 */
void MCO_Output_Config(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    
    // MCO1 - PA8 (może wyprowadzić: HSI, LSE, HSE, PLL)
    __HAL_RCC_GPIOA_CLK_ENABLE();
    GPIO_InitStruct.Pin = GPIO_PIN_8;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF0_MCO;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // Wyprowadź SYSCLK/4 na MCO1
    HAL_RCC_MCOConfig(RCC_MCO1, RCC_MCO1SOURCE_PLLCLK, RCC_MCODIV_4);
    
    // MCO2 - PC9 (może wyprowadzić: SYSCLK, PLLI2S, HSE, PLL)
    __HAL_RCC_GPIOC_CLK_ENABLE();
    GPIO_InitStruct.Pin = GPIO_PIN_9;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
    
    // Wyprowadź SYSCLK/5 na MCO2
    HAL_RCC_MCOConfig(RCC_MCO2, RCC_MCO2SOURCE_SYSCLK, RCC_MCODIV_5);
}
```

### Odczyt częstotliwości zegarów

```c
/**
 * @brief  Wyświetlenie informacji o zegarach
 */
void Print_Clock_Info(void)
{
    printf("=== System Clock Configuration ===\r\n");
    printf("SYSCLK: %lu MHz\r\n", HAL_RCC_GetSysClockFreq() / 1000000);
    printf("HCLK:   %lu MHz\r\n", HAL_RCC_GetHCLKFreq() / 1000000);
    printf("PCLK1:  %lu MHz\r\n", HAL_RCC_GetPCLK1Freq() / 1000000);
    printf("PCLK2:  %lu MHz\r\n", HAL_RCC_GetPCLK2Freq() / 1000000);
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_wprowadzenie|STM32F429I - Wprowadzenie]]
- [[stm32f429i_architektura|STM32F429I - Architektura]]
- [[stm32f429i_timery|STM32F429I - Timery i liczniki]]
- [[stm32f429i_power_modes|STM32F429I - Tryby niskiego poboru mocy]]

## 📝 Checkli sta konfiguracji

### Podstawowa konfiguracja 180 MHz
- [ ] Włącz HSE (8 MHz)
- [ ] Skonfiguruj PLL: M=8, N=360, P=2, Q=7
- [ ] Włącz Over-Drive Mode
- [ ] Ustaw dzielniki: AHB=/1, APB1=/4, APB2=/2
- [ ] Ustaw Flash Latency = 5
- [ ] Włącz CSS dla monitoringu HSE
- [ ] Zweryfikuj częstotliwości magistral

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
