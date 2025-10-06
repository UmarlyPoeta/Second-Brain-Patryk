# STM32F429I - Wprowadzenie i Specyfikacja

## 📋 Wprowadzenie

STM32F429I to zaawansowany 32-bitowy mikrokontroler z rodziny STM32F4 firmy STMicroelectronics, oparty na rdzeniu ARM Cortex-M4 z jednostką FPU (Floating Point Unit). Jest to jeden z najpotężniejszych mikrokontrolerów w tej serii, zaprojektowany dla wymagających aplikacji embedded wymagających wysokiej wydajności obliczeniowej i zaawansowanych interfejsów graficznych.

## 🔧 Specyfikacja techniczna

### Procesor
- **Rdzeń**: ARM Cortex-M4 z FPU
- **Częstotliwość**: do 180 MHz
- **Wydajność**: 225 DMIPS (Dhrystone MIPS)
- **Architektura**: Harvard ARMv7-M
- **DSP**: Instrukcje DSP do przetwarzania sygnałów

### Pamięć
- **Flash**: 2 MB (dual bank, możliwość read-while-write)
- **RAM**: 256 KB SRAM (w tym 64 KB CCM RAM)
- **Pamięć zewnętrzna**: 
  - FMC (Flexible Memory Controller)
  - Obsługa SDRAM, SRAM, NOR Flash, NAND Flash
  - Do 4 GB przestrzeni adresowej

### Zasilanie
- **Napięcie zasilania**: 1.8V - 3.6V
- **Tryby niskiego poboru mocy**:
  - Sleep
  - Stop (z RTC)
  - Standby
- **Pobór prądu**:
  - Run: ~50 mA @ 180 MHz
  - Stop: ~200 μA
  - Standby: ~2 μA

### Peryferyjne

#### Interfejsy komunikacyjne
- **UART/USART**: 4x USART, 4x UART (do 11.25 Mbit/s)
- **SPI**: 6x (do 45 Mbit/s)
- **I2C**: 3x (Fast Mode Plus do 1 MHz)
- **CAN**: 2x CAN 2.0B
- **USB**: 2x USB OTG (Full-Speed i High-Speed)
- **Ethernet**: MAC 10/100 z MII/RMII
- **SDIO**: interfejs do kart SD/MMC

#### Timery i liczniki
- **Timery ogólnego przeznaczenia**: 12x (16-bit i 32-bit)
- **Timery zaawansowane**: 2x (16-bit)
- **Timery podstawowe**: 2x (16-bit)
- **Watchdog**: 2x (niezależny i okienkowy)
- **SysTick**: Timer systemowy 24-bit

#### Konwertery analogowe
- **ADC**: 3x 12-bit (do 2.4 MSPS)
- **DAC**: 2x 12-bit
- **Kanały**: do 24 kanałów ADC
- **Rozdzielczość**: 6, 8, 10, 12 bitów (programowalna)

#### Interfejs graficzny
- **LCD-TFT**: kontroler do wyświetlaczy graficznych
- **Rozdzielczość**: do 1024x768
- **Warstwy**: 2 niezależne warstwy graficzne
- **Chroma keying**: wsparcie dla efektów przezroczystości
- **DMA2D**: akcelerator graficzny 2D (Chrom-ART)

### GPIO
- **Liczba pinów I/O**: do 168 (w zależności od obudowy)
- **Prędkość**: do 90 MHz
- **Obsługiwane tryby**:
  - Input (floating, pull-up, pull-down)
  - Output (push-pull, open-drain)
  - Alternate Function
  - Analog

## 📦 Warianty obudowy

### Dostępne pakiety
- **LQFP100**: 100 pinów (14x14 mm)
- **LQFP144**: 144 piny (20x20 mm)
- **LQFP176**: 176 pinów (24x24 mm)
- **UFBGA176**: 176 pinów BGA (10x10 mm)
- **WLCSP168**: 168 pinów wafer-level chip-scale package

### Różnice między wariantami
| Wariant | Flash | RAM | Pins | GPIO |
|---------|-------|-----|------|------|
| STM32F429ZI | 2 MB | 256 KB | 144 | 114 |
| STM32F429VI | 2 MB | 256 KB | 100 | 82 |
| STM32F429BI | 2 MB | 256 KB | 208 | 168 |

## 🎯 Typowe zastosowania

### Aplikacje graficzne
- Wyświetlacze HMI (Human-Machine Interface)
- Sterowniki LCD/TFT
- Terminale przemysłowe
- Urządzenia medyczne z GUI

### Aplikacje przemysłowe
- PLC (Programmable Logic Controller)
- Systemy sterowania silnikami
- Przemysłowe systemy pomiarowe
- Automatyka budynkowa

### Komunikacja
- Bramy sieciowe (gateway)
- Konwertery protokołów
- Urządzenia IoT
- Systemy monitoringu

### Audio i multimedia
- Procesory audio DSP
- Odtwarzacze multimedialne
- Systemy nagłośnienia
- Efekty dźwiękowe

## 🔗 Blokowy schemat układu

```
┌─────────────────────────────────────────────────┐
│              ARM Cortex-M4 @ 180MHz             │
│                    + FPU + MPU                   │
└────────────┬────────────────────────┬────────────┘
             │                        │
    ┌────────▼────────┐      ┌───────▼────────┐
    │  2MB Flash      │      │  256KB SRAM    │
    │  (Dual Bank)    │      │  64KB CCM      │
    └─────────────────┘      └────────────────┘
             │                        │
    ┌────────▼────────────────────────▼────────┐
    │           AHB/APB Bus Matrix             │
    └────┬────┬────┬────┬────┬────┬────┬───────┘
         │    │    │    │    │    │    │
    ┌────▼┐ ┌─▼──┐ ┌▼──┐ ┌▼─┐ ┌▼──┐ ┌▼──┐ ┌▼────┐
    │GPIO │ │TIM │ │ADC│ │DAC│ │DMA│ │USB│ │LCD- │
    │168  │ │×14 │ │×3 │ │×2 │ │×2 │ │OTG│ │TFT  │
    └─────┘ └────┘ └───┘ └───┘ └───┘ └───┘ └─────┘
         │    │      │     │     │     │      │
    ┌────▼────▼──────▼─────▼─────▼─────▼──────▼───┐
    │  UART/SPI/I2C/CAN/Ethernet/SDIO/FMC        │
    └────────────────────────────────────────────┘
```

## 💻 Podstawowa konfiguracja startowa

### Minimalny kod startowy (HAL)

```c
#include "stm32f4xx_hal.h"

/**
 * @brief  Konfiguracja zegara systemowego na 180 MHz
 * @retval None
 */
void SystemClock_Config(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    // Włącz zasilanie regulatora napięcia
    __HAL_RCC_PWR_CLK_ENABLE();
    __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

    // Inicjalizacja oscylatora HSE i PLL
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
    RCC_OscInitStruct.HSEState = RCC_HSE_ON;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
    RCC_OscInitStruct.PLL.PLLM = 8;   // HSE/8 = 1 MHz
    RCC_OscInitStruct.PLL.PLLN = 360; // 1 MHz * 360 = 360 MHz
    RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2; // 360/2 = 180 MHz
    RCC_OscInitStruct.PLL.PLLQ = 7;   // Dla USB (48 MHz)
    
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
        Error_Handler();
    }

    // Włącz Over-Drive dla 180 MHz
    if (HAL_PWREx_EnableOverDrive() != HAL_OK) {
        Error_Handler();
    }

    // Konfiguracja zegarów magistral
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | 
                                  RCC_CLOCKTYPE_SYSCLK |
                                  RCC_CLOCKTYPE_PCLK1 | 
                                  RCC_CLOCKTYPE_PCLK2;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;   // 180 MHz
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;    // 45 MHz
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;    // 90 MHz

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK) {
        Error_Handler();
    }
}

/**
 * @brief  Funkcja główna
 */
int main(void)
{
    // Reset wszystkich peryferyjnych
    HAL_Init();
    
    // Konfiguracja zegara systemowego
    SystemClock_Config();
    
    // Pętla główna
    while (1) {
        // Kod aplikacji
    }
}
```

## 📚 Dokumentacja i zasoby

### Dokumenty referencyjne
- **Reference Manual** (RM0090): Kompletny opis peryferyjnych
- **Datasheet**: Parametry elektryczne i mechaniczne
- **Programming Manual** (PM0214): Programowanie rdzenia Cortex-M4
- **Errata Sheet**: Znane błędy i obejścia

### Narzędzia programistyczne
- **STM32CubeMX**: Generator kodu i konfigurator pinów
- **STM32CubeIDE**: Zintegrowane środowisko programistyczne
- **STM32CubeProgrammer**: Narzędzie do programowania
- **STM32CubeMonitor**: Monitoring i debugowanie w czasie rzeczywistym

### Biblioteki
- **HAL** (Hardware Abstraction Layer): Wysoki poziom abstrakcji
- **LL** (Low-Layer): Niskopoziomowy dostęp do rejestrów
- **CMSIS**: Standard ARM dla mikrokontrolerów Cortex-M

## 🔗 Powiązane tematy

- [[stm32f429i_architektura|STM32F429I - Architektura ARM Cortex-M4]]
- [[stm32f429i_system_zegarowy|STM32F429I - System zegarowy i RCC]]
- [[stm32f429i_gpio|STM32F429I - GPIO i konfiguracja pinów]]
- [[stm32cube_ide|STM32CubeIDE - Środowisko programistyczne]]
- [[mikrokontrolery_vs_mikroprocesory|Mikrokontrolery vs Mikroprocesory]]

## 📝 Notatki praktyczne

### Ważne uwagi
1. **Over-Drive Mode**: Wymagany dla częstotliwości >168 MHz
2. **Flash Latency**: Musi być odpowiednio ustawiony dla wysokich częstotliwości
3. **Zasilanie**: 1.8V Core przy maksymalnej częstotliwości
4. **Chłodzenie**: Przy pełnym obciążeniu może być potrzebne

### Typowe problemy
1. **Brak stabilnego zegara**: Sprawdź kondensatory przy oscylatorze HSE
2. **Reset podczas bootowania**: Niedostateczne zasilanie
3. **Nieprawidłowa prędkość UART**: Błędna konfiguracja zegarów APB

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
