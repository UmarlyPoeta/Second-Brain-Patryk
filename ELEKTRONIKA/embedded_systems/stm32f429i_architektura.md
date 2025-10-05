# STM32F429I - Architektura ARM Cortex-M4

## 🏗️ Architektura rdzenia ARM Cortex-M4

### Podstawowe informacje
- **Architektura**: ARMv7-M (32-bitowa RISC)
- **Pipeline**: 3-stopniowy
- **Typ architektury**: Harvard (oddzielne magistrale dla kodu i danych)
- **Endianness**: Little-endian (opcjonalnie big-endian)
- **Zestaw instrukcji**: Thumb-2

### Komponenty rdzenia

```
┌─────────────────────────────────────────────────┐
│           ARM Cortex-M4 Core                    │
│  ┌──────────────┐  ┌──────────────┐            │
│  │   Processor  │  │     FPU      │            │
│  │     Core     │  │  (Single-    │            │
│  │              │  │  Precision)  │            │
│  └──────┬───────┘  └──────┬───────┘            │
│         │                 │                     │
│  ┌──────▼─────────────────▼───────┐            │
│  │       NVIC (Nested Vector      │            │
│  │    Interrupt Controller)        │            │
│  └──────────────┬──────────────────┘            │
│                 │                               │
│  ┌──────────────▼──────────────────┐            │
│  │         Bus Matrix              │            │
│  └──┬──────┬──────┬─────┬──────────┘            │
└─────┼──────┼──────┼─────┼─────────────────────┘
      │      │      │     │
   I-Code D-Code System  DMA
   (Flash) (SRAM)  Bus   Bus
```

## 🧮 Jednostka Floating-Point (FPU)

### Charakterystyka FPU
- **Standard**: IEEE 754 single-precision
- **Typ**: FPv4-SP (Floating-Point Version 4 - Single Precision)
- **Rejestry**: 32 rejestry 32-bitowe (S0-S31)
- **Operacje**: 
  - Dodawanie, odejmowanie, mnożenie, dzielenie
  - Pierwiastek kwadratowy
  - Konwersje między typami
  - Operacje porównania

### Przykład użycia FPU

```c
#include "stm32f4xx_hal.h"
#include <math.h>

/**
 * @brief  Włączenie FPU w systemie
 */
void FPU_Enable(void)
{
    // Włącz dostęp do koprocesora FPU
    SCB->CPACR |= ((3UL << 10*2) | (3UL << 11*2));
    
    // Synchronizacja instrukcji
    __DSB();
    __ISB();
}

/**
 * @brief  Przykład obliczeń zmiennoprzecinkowych
 */
float calculate_distance(float x1, float y1, float x2, float y2)
{
    float dx = x2 - x1;
    float dy = y2 - y1;
    
    // FPU automatycznie użyte dla operacji float
    return sqrtf(dx*dx + dy*dy);
}

/**
 * @brief  Implementacja filtra dolnoprzepustowego
 */
typedef struct {
    float alpha;      // Współczynnik wygładzania (0-1)
    float prev_value; // Poprzednia wartość
} LowPassFilter_t;

float LowPassFilter_Update(LowPassFilter_t* filter, float new_value)
{
    // y[n] = α * x[n] + (1 - α) * y[n-1]
    filter->prev_value = filter->alpha * new_value + 
                        (1.0f - filter->alpha) * filter->prev_value;
    return filter->prev_value;
}
```

## 📊 Tryby pracy procesora

### Thread Mode vs Handler Mode

```c
// Thread Mode - kod aplikacji
void main_application(void)
{
    // Kod wykonywany w Thread Mode
    // Używa Main Stack Pointer (MSP) lub Process Stack Pointer (PSP)
    while(1) {
        // Aplikacja
    }
}

// Handler Mode - obsługa przerwań
void TIM2_IRQHandler(void)
{
    // Kod wykonywany w Handler Mode
    // Zawsze używa Main Stack Pointer (MSP)
    
    // Obsługa przerwania
    HAL_TIM_IRQHandler(&htim2);
}
```

### Poziomy uprzywilejowania
- **Privileged**: Pełny dostęp do wszystkich zasobów
- **Unprivileged**: Ograniczony dostęp (ochrona pamięci)

```c
/**
 * @brief  Zmiana poziomu uprzywilejowania
 */
void switch_to_unprivileged(void)
{
    // Ustawienie bitu nPRIV w rejestrze CONTROL
    __set_CONTROL(__get_CONTROL() | CONTROL_nPRIV_Msk);
    __ISB();
}

void switch_to_privileged(void)
{
    // Tylko przez SVC (Supervisor Call)
    __asm volatile("SVC 0");
}
```

## 🎯 NVIC - Kontroler przerwań

### Cechy NVIC w STM32F429I
- **Liczba przerwań**: 82 zewnętrzne linie przerwań
- **Poziomy priorytetów**: 16 (0-15, gdzie 0 = najwyższy)
- **Preemption**: Wsparcie dla przerwań zagnieżdżonych
- **Grupowanie priorytetów**: 4 bity (konfigurowane)

### Konfiguracja NVIC

```c
/**
 * @brief  Konfiguracja przerwania EXTI
 */
void EXTI_Config(void)
{
    // Włącz zegar GPIO
    __HAL_RCC_GPIOA_CLK_ENABLE();
    
    // Konfiguracja pinu jako wejście
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;  // Przerwanie na zbocze narastające
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
    
    // Konfiguracja NVIC
    HAL_NVIC_SetPriority(EXTI0_IRQn, 5, 0);  // Preemption=5, SubPriority=0
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
}

/**
 * @brief  Handler przerwania
 */
void EXTI0_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
}

/**
 * @brief  Callback przerwania EXTI
 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_0) {
        // Obsługa przerwania na pinie PA0
    }
}
```

### Grupowanie priorytetów

```c
/**
 * @brief  Ustawienie grupowania priorytetów
 */
void NVIC_PriorityGroupConfig(void)
{
    // 4 bity preemption, 0 bitów subpriority
    HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_4);
    
    // 3 bity preemption, 1 bit subpriority
    // HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_3);
    
    // 2 bity preemption, 2 bity subpriority
    // HAL_NVIC_SetPriorityGrouping(NVIC_PRIORITYGROUP_2);
}
```

## 💾 Memory Protection Unit (MPU)

### Funkcje MPU
- **Regiony**: 8 konfigurowalnych regionów pamięci
- **Ochrona**: Kontrola dostępu do pamięci
- **Rozmiary**: Od 32B do 4GB
- **Atrybuty**: Cacheable, bufferable, shareable

### Konfiguracja MPU

```c
/**
 * @brief  Konfiguracja regionu MPU
 */
void MPU_Config(void)
{
    MPU_Region_InitTypeDef MPU_InitStruct = {0};
    
    // Wyłącz MPU
    HAL_MPU_Disable();
    
    // Region 0: Flash (Read-Only, Executable)
    MPU_InitStruct.Enable = MPU_REGION_ENABLE;
    MPU_InitStruct.Number = MPU_REGION_NUMBER0;
    MPU_InitStruct.BaseAddress = 0x08000000;
    MPU_InitStruct.Size = MPU_REGION_SIZE_2MB;
    MPU_InitStruct.SubRegionDisable = 0x0;
    MPU_InitStruct.TypeExtField = MPU_TEX_LEVEL0;
    MPU_InitStruct.AccessPermission = MPU_REGION_PRIV_RO_URO;
    MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_ENABLE;
    MPU_InitStruct.IsShareable = MPU_ACCESS_NOT_SHAREABLE;
    MPU_InitStruct.IsCacheable = MPU_ACCESS_CACHEABLE;
    MPU_InitStruct.IsBufferable = MPU_ACCESS_NOT_BUFFERABLE;
    HAL_MPU_ConfigRegion(&MPU_InitStruct);
    
    // Region 1: SRAM (Read-Write, No Execute)
    MPU_InitStruct.Number = MPU_REGION_NUMBER1;
    MPU_InitStruct.BaseAddress = 0x20000000;
    MPU_InitStruct.Size = MPU_REGION_SIZE_256KB;
    MPU_InitStruct.AccessPermission = MPU_REGION_FULL_ACCESS;
    MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE;
    HAL_MPU_ConfigRegion(&MPU_InitStruct);
    
    // Włącz MPU
    HAL_MPU_Enable(MPU_PRIVILEGED_DEFAULT);
}
```

## 🔄 Magistrale systemowe

### AHB (Advanced High-performance Bus)
- **Prędkość**: Do 180 MHz
- **Szerokość**: 32 bity
- **Urządzenia**:
  - GPIO
  - DMA
  - FMC (pamięci zewnętrzne)
  - USB OTG
  - Ethernet

### APB1 (Advanced Peripheral Bus 1)
- **Prędkość**: Do 45 MHz
- **Urządzenia**:
  - Timery 2-7, 12-14
  - USART 2,3, UART 4,5,7,8
  - SPI 2,3
  - I2C 1-3
  - CAN 1,2
  - DAC

### APB2 (Advanced Peripheral Bus 2)
- **Prędkość**: Do 90 MHz
- **Urządzenia**:
  - Timery 1, 8-11
  - USART 1,6
  - SPI 1,4,5,6
  - ADC 1-3
  - SYSCFG

### Przykład konfiguracji zegarów magistral

```c
/**
 * @brief  Odczyt częstotliwości zegarów magistral
 */
void Get_Bus_Frequencies(void)
{
    uint32_t hclk_freq = HAL_RCC_GetHCLKFreq();   // AHB clock
    uint32_t pclk1_freq = HAL_RCC_GetPCLK1Freq(); // APB1 clock
    uint32_t pclk2_freq = HAL_RCC_GetPCLK2Freq(); // APB2 clock
    uint32_t sysclk_freq = HAL_RCC_GetSysClockFreq(); // System clock
    
    printf("SYSCLK: %lu MHz\r\n", sysclk_freq / 1000000);
    printf("HCLK:   %lu MHz\r\n", hclk_freq / 1000000);
    printf("PCLK1:  %lu MHz\r\n", pclk1_freq / 1000000);
    printf("PCLK2:  %lu MHz\r\n", pclk2_freq / 1000000);
}
```

## ⚡ Pipeline i wydajność

### 3-stopniowy pipeline
1. **Fetch**: Pobranie instrukcji z pamięci
2. **Decode**: Dekodowanie instrukcji
3. **Execute**: Wykonanie instrukcji

### Optymalizacja wydajności

```c
/**
 * @brief  Włączenie cache instrukcji i danych
 */
void Enable_CPU_Cache(void)
{
    // Włącz I-Cache (Instruction Cache)
    SCB_EnableICache();
    
    // Włącz D-Cache (Data Cache)
    SCB_EnableDCache();
}

/**
 * @brief  Prefetch buffer dla flash
 */
void Enable_Flash_Prefetch(void)
{
    // Włącz prefetch buffer
    __HAL_FLASH_PREFETCH_BUFFER_ENABLE();
    
    // Włącz ART Accelerator
    __HAL_FLASH_ART_ENABLE();
}
```

### Instrukcje DSP

```c
/**
 * @brief  Przykład użycia instrukcji SIMD
 */
int32_t saturating_add(int32_t a, int32_t b)
{
    // Użycie instrukcji QADD (saturating add)
    int32_t result;
    __asm volatile("QADD %0, %1, %2" : "=r"(result) : "r"(a), "r"(b));
    return result;
}

/**
 * @brief  Mnożenie z akumulacją (MAC)
 */
int32_t multiply_accumulate(int32_t acc, int32_t a, int32_t b)
{
    // result = acc + (a * b)
    return __SMLAL(a, b, acc);
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_wprowadzenie|STM32F429I - Wprowadzenie i specyfikacja]]
- [[stm32f429i_przerwania|STM32F429I - Przerwania i NVIC]]
- [[stm32f429i_system_zegarowy|STM32F429I - System zegarowy]]
- [[stm32f429i_dma|STM32F429I - DMA i transfer danych]]

## 📝 Podsumowanie

### Kluczowe cechy architektury
1. **FPU**: Szybkie operacje zmiennoprzecinkowe
2. **NVIC**: Zaawansowane zarządzanie przerwaniami
3. **MPU**: Ochrona pamięci
4. **DSP**: Instrukcje do przetwarzania sygnałów
5. **Pipeline**: Efektywne wykonywanie kodu

### Best practices
- Włącz FPU jeśli używasz obliczeń float
- Konfiguruj priorytety przerwań odpowiednio
- Używaj MPU dla aplikacji krytycznych
- Włącz cache i prefetch dla lepszej wydajności
- Wykorzystuj instrukcje DSP dla obliczeń sygnałowych

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
