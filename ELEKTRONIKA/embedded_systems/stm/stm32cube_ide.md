# STM32CubeIDE - Środowisko Programistyczne

## 🖥️ STM32CubeIDE

### Wprowadzenie
STM32CubeIDE to bezpłatne, zintegrowane środowisko programistyczne (IDE) od STMicroelectronics dla mikrokontrolerów STM32, bazujące na Eclipse. Łączy w sobie STM32CubeMX (konfigurator) z kompletn ym IDE do programowania i debugowania.

### Główne funkcje
- Konfiguracja graficzna (CubeMX)
- Edytor kodu z IntelliSense
- Kompilator GCC ARM
- Debugger GDB z ST-LINK
- Profilowanie i analiza wydajności
- Zarządzanie projektami
- Integracja z Git

## 🚀 Tworzenie nowego projektu

### Krok po kroku

```
1. File → New → STM32 Project
2. Target Selection:
   - MCU/MPU Selector → wpisz "STM32F429ZI"
   - Wybierz dokładny model (np. STM32F429ZITx)
   - Next
3. Project Setup:
   - Project Name: "STM32F429_Example"
   - Targeted Language: C lub C++
   - Targeted Binary Type: Executable
   - Targeted Project Type: STM32Cube
   - Finish
4. Initialize peripherals with default mode: Yes/No
```

### Struktura projektu

```
STM32F429_Example/
├── Core/
│   ├── Inc/           # Header files
│   │   ├── main.h
│   │   ├── stm32f4xx_it.h
│   │   └── stm32f4xx_hal_conf.h
│   ├── Src/           # Source files
│   │   ├── main.c
│   │   ├── stm32f4xx_it.c
│   │   ├── stm32f4xx_hal_msp.c
│   │   └── system_stm32f4xx.c
│   └── Startup/       # Startup code
│       └── startup_stm32f429zitx.s
├── Drivers/
│   ├── STM32F4xx_HAL_Driver/  # HAL library
│   └── CMSIS/                 # CMSIS files
├── Middlewares/       # Optional middleware (FreeRTOS, USB, etc.)
├── .settings/         # Eclipse settings
├── Debug/             # Debug build output
├── Release/           # Release build output
├── STM32F429ZITX_FLASH.ld  # Linker script
└── STM32F429_Example.ioc    # CubeMX configuration
```

## ⚙️ CubeMX Configuration

### Pinout & Configuration

```c
/**
 * @brief  Przykład konfiguracji w CubeMX
 */
// 1. Pinout & Configuration tab
//    - Kliknij pin → Wybierz funkcję (np. GPIO_Output, USART1_TX)
//    - Alternatywnie: Connectivity → USART1 → Mode: Asynchronous

// 2. System Core → RCC
//    - HSE: Crystal/Ceramic Resonator (8 MHz)
//    - LSE: Crystal/Ceramic Resonator (32.768 kHz)

// 3. Clock Configuration tab
//    - Ustaw HCLK na 180 MHz
//    - CubeMX automatycznie obliczy PLL parameters

// 4. Connectivity → USART1
//    - Mode: Asynchronous
//    - Baud Rate: 115200
//    - Word Length: 8 Bits
//    - Stop Bits: 1
//    - Parity: None

// 5. Project Manager → Project
//    - Project Settings → Generate code

// Wygenerowany kod w main.c:
void SystemClock_Config(void);  // Auto-generated
static void MX_GPIO_Init(void); // Auto-generated
static void MX_USART1_UART_Init(void); // Auto-generated
```

### Typowa konfiguracja dla STM32F429I

```c
/**
 * @brief  Rekomendowana konfiguracja RCC
 */
// Clock Configuration:
// Input: HSE 8 MHz
// PLL_M: 8
// PLL_N: 360
// PLL_P: 2
// PLL_Q: 7
// SYSCLK: 180 MHz
// AHB: 180 MHz
// APB1: 45 MHz
// APB2: 90 MHz

/**
 * @brief  Kod użytkownika - sekcje USER CODE
 */
int main(void)
{
  /* USER CODE BEGIN 1 */
  // Tu dodaj inicjalizację przed HAL_Init
  /* USER CODE END 1 */

  HAL_Init();
  SystemClock_Config();
  MX_GPIO_Init();
  MX_USART1_UART_Init();
  
  /* USER CODE BEGIN 2 */
  // Tu dodaj inicjalizację przed main loop
  printf("System started\r\n");
  /* USER CODE END 2 */

  while (1)
  {
    /* USER CODE BEGIN 3 */
    // Tu dodaj kod main loop
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    HAL_Delay(1000);
    /* USER CODE END 3 */
  }
}
```

## 🔨 Build Configurations

### Debug vs Release

```c
/**
 * @brief  Build configurations
 */
// Debug Configuration:
// - Optimization: -Og (Debug optimization)
// - Debug Info: -g3 (Maximum debug info)
// - Assertions: Enabled
// - Size: Większy executable

// Release Configuration:
// - Optimization: -O3 lub -Os (Size optimization)
// - Debug Info: None or minimal
// - Assertions: Disabled
// - Size: Mniejszy, szybszy kod

// Project → Properties → C/C++ Build → Settings
// - Tool Settings → MCU GCC Compiler → Optimization
//   Debug:   -Og
//   Release: -Os (size) lub -O3 (speed)
```

### Custom Build Steps

```bash
# Project → Properties → C/C++ Build → Settings → Build Steps

# Pre-build:
echo "Building $(PROJECT_NAME)..."
date > build_timestamp.txt

# Post-build (generowanie .bin):
arm-none-eabi-objcopy -O binary "${BuildArtifactFileBaseName}.elf" "${BuildArtifactFileBaseName}.bin"

# Post-build (wyświetl rozmiar):
arm-none-eabi-size "${BuildArtifactFileName}"
```

## 🐛 Debugging

### Debug Configuration

```c
/**
 * @brief  Konfiguracja debuggera
 */
// Run → Debug Configurations
// - GDB OpenOCD Debugging
//   - Debugger tab:
//     - OpenOCD Setup:
//       Config options: -f board/stm32f429discovery.cfg
//     - GDB Client Setup:
//       Executable: arm-none-eabi-gdb
//   - Startup tab:
//     - Initial reset: Enabled
//     - Load executable: Enabled
//     - Resume: Enabled

/**
 * @brief  Live Expressions
 */
// Window → Show View → SWV → SWV Live Expressions
// Dodaj zmienne do monitorowania w czasie rzeczywistym
volatile uint32_t live_counter = 0;
volatile float live_temperature = 0.0f;
```

### SWV (Serial Wire Viewer)

```c
/**
 * @brief  Konfiguracja SWV
 */
// Run → Debug Configurations → Startup tab
// - Enable Serial Wire Viewer (SWV)
// - Core Clock: 180 MHz
// - SWO Clock: 2000000 (2 MHz)

/**
 * @brief  Printf przez SWV ITM
 */
int _write(int file, char *ptr, int len)
{
    for (int i = 0; i < len; i++) {
        ITM_SendChar((*ptr++));
    }
    return len;
}

// Window → Show View → SWV → SWV ITM Data Console
// - Configure Trace:
//   - Enable Port 0
//   - Start Trace
```

### Breakpoints i watchpoints

```c
/**
 * @brief  Różne typy breakpointów
 */
// Regular breakpoint:
// - Kliknij dwukrotnie na marginesie linii
// - Lub: Run → Toggle Breakpoint

// Conditional breakpoint:
void debug_loop(void)
{
    for (int i = 0; i < 1000; i++) {
        Process(i);  // Breakpoint: i == 500
    }
}
// Prawy klik na breakpoint → Breakpoint Properties
// - Conditional: Enabled
// - Condition: i == 500

// Data watchpoint:
volatile uint32_t watch_me = 0;
// Run → Add Watchpoint
// - Expression: watch_me
// - Access: Write / Read & Write
```

## 📊 Performance Analysis

### Statistical Profiling

```c
/**
 * @brief  Profilowanie kodu
 */
// Window → Show View → SWV → Statistical Profiling
// - Configuration:
//   - Sampling frequency: 1000 Hz
//   - Trace buffer size: 4096
// - Start
// - Run program
// - Stop
// - Wynik: % czasu w każdej funkcji

void performance_critical_function(void)
{
    // Ta funkcja będzie widoczna w profilu
    for (int i = 0; i < 10000; i++) {
        complex_calculation(i);
    }
}
```

### Memory usage

```bash
# Automatycznie wyświetlane po build:
# 
# text    data     bss     dec     hex filename
# 8432     108   1572   10112    2780 Example.elf
#
# text: Code (Flash)
# data: Initialized variables (Flash + RAM)
# bss:  Uninitialized variables (RAM)

# Szczegółowa analiza:
# Window → Show View → Build Analyzer
# - Pokaże rozmiar każdej funkcji i zmiennej
```

## 🔧 Advanced Features

### Code Generator Options

```c
/**
 * @brief  CubeMX Advanced Settings
 */
// Project Manager → Advanced Settings
// - Driver Selector:
//   - HAL (domyślny) - wysoki poziom
//   - LL (Low-Layer) - niski poziom, szybszy
// - Register Callbacks: Enabled
//   - Pozwala na dynamiczną rejestrację callbacków

/**
 * @brief  Przykład z HAL Callbacks
 */
void Custom_UART_RxCallback(UART_HandleTypeDef *huart)
{
    // Custom callback
}

// W main.c:
HAL_UART_RegisterCallback(&huart1, HAL_UART_RX_COMPLETE_CB_ID, 
                         Custom_UART_RxCallback);
```

### FreeRTOS Integration

```c
/**
 * @brief  Dodawanie FreeRTOS
 */
// Middleware → FREERTOS → Interface: CMSIS_V2
// - Config parameters:
//   - Total heap size: 15360 bytes
//   - Minimal stack size: 128 words
// - Advanced settings:
//   - USE_TICKLESS_IDLE: Enabled
//   - Tasks and Queues:
//     - Add Task: "defaultTask", Priority: Normal, Stack: 128

/* USER CODE BEGIN Header_StartDefaultTask */
void StartDefaultTask(void *argument)
{
  for(;;)
  {
    // Task code
    osDelay(1);
  }
}
/* USER CODE END Header_StartDefaultTask */
```

## 📦 Libraries and Middleware

### USB Library

```c
/**
 * @brief  Konfiguracja USB CDC
 */
// Middleware → USB_DEVICE
// - Class For FS IP: Communication Device Class (CDC)
// - Device Descriptor:
//   - VID: 0x0483
//   - PID: 0x5740
//   - Product String: "STM32 Virtual ComPort"

// Użycie:
uint8_t UserTxBuffer[APP_TX_DATA_SIZE];
CDC_Transmit_FS(UserTxBuffer, strlen((char*)UserTxBuffer));
```

### FAT Filesystem

```c
/**
 * @brief  Konfiguracja FatFs
 */
// Middleware → FATFS
// - Mode: SD Card
// - Platform Settings:
//   - Detect_SDIO: PC13

// Użycie:
FATFS FatFs;
FIL MyFile;

f_mount(&FatFs, "", 0);
f_open(&MyFile, "test.txt", FA_WRITE | FA_CREATE_ALWAYS);
f_write(&MyFile, "Hello World", 11, &byteswritten);
f_close(&MyFile);
```

## 🔗 Version Control (Git)

### Git Integration

```bash
# Team → Share Project → Git
# - Create a Git repository
# - Location: Use or create repository in parent folder

# .gitignore dla STM32CubeIDE:
Debug/
Release/
*.o
*.elf
*.bin
*.hex
*.map
.metadata/
.settings/

# Keep:
Core/
Drivers/
*.ioc
*.ld
```

### Workflow

```bash
# 1. Commit po każdej istotnej zmianie
# Team → Commit
# - Message: "Add UART communication"
# - Files: Select all modified

# 2. Porównanie zmian
# Prawy klik na plik → Compare With → HEAD Revision

# 3. Historia
# Team → Show in History
```

## 🔗 Powiązane tematy

- [[stm32f429i_wprowadzenie|STM32F429I - Wprowadzenie]]
- [[stm32f429i_debugging|STM32F429I - Debugowanie]]
- [[stm32f429i_gpio|STM32F429I - GPIO]]

## 📝 Shortcuts i Tips

### Przydatne skróty klawiszowe
```
Ctrl + Space:     Auto-complete
Ctrl + Shift + F: Format code
Ctrl + Shift + O: Organize includes
F3:               Go to definition
Ctrl + H:         Search in project
Ctrl + B:         Build project
F11:              Debug
Ctrl + F11:       Run
F5:               Step into
F6:               Step over
F7:               Step return
Ctrl + Shift + B: Build all
```

### Tips
1. Używaj USER CODE sections - kod nie zostanie nadpisany
2. Regularnie regeneruj kod z CubeMX
3. Włącz Auto-Save przed debug
4. Używaj Live Expressions do monitorowania
5. Profiluj przed optymalizacją
6. Konfiguruj .gitignore odpowiednio
7. Backup pliku .ioc przed większymi zmianami

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
