# Programowanie Embedded - Zaawansowane Techniki

## Dobre praktyki w kodzie embedded

### Organizacja kodu
```cpp
// main.h - definicje globalne
#ifndef MAIN_H
#define MAIN_H

#include <Arduino.h>

// Konfiguracja systemu
#define SYSTEM_VERSION "1.0.0"
#define DEBUG_MODE 1

// Definicje pinów
#define LED_STATUS_PIN 13
#define BUTTON_INPUT_PIN 2
#define SENSOR_POWER_PIN 8

// Definicje czasów (ms)
#define SENSOR_READ_INTERVAL 1000
#define LED_BLINK_PERIOD 500
#define DEBOUNCE_DELAY 50

// Struktury danych
typedef struct {
    float temperature;
    float humidity;
    uint32_t timestamp;
    bool valid;
} SensorData_t;

// Deklaracje funkcji
void setupHardware();
void handleSensorReading();
void updateStatusLED();

#endif
```

```cpp
// main.cpp - implementacja główna
#include "main.h"
#include "sensors.h"
#include "utils.h"

static SensorData_t currentData = {0};
static unsigned long lastSensorRead = 0;
static unsigned long lastLEDUpdate = 0;
static bool ledState = false;

void setup() {
    setupHardware();
    Serial.println("System started - Version: " SYSTEM_VERSION);
}

void loop() {
    unsigned long currentTime = millis();
    
    // Non-blocking sensor reading
    if (currentTime - lastSensorRead >= SENSOR_READ_INTERVAL) {
        handleSensorReading();
        lastSensorRead = currentTime;
    }
    
    // Non-blocking LED update
    if (currentTime - lastLEDUpdate >= LED_BLINK_PERIOD) {
        updateStatusLED();
        lastLEDUpdate = currentTime;
    }
    
    // Handle other tasks
    processCommands();
    updateWatchdog();
}

void setupHardware() {
    pinMode(LED_STATUS_PIN, OUTPUT);
    pinMode(BUTTON_INPUT_PIN, INPUT_PULLUP);
    pinMode(SENSOR_POWER_PIN, OUTPUT);
    
    digitalWrite(SENSOR_POWER_PIN, HIGH);  // Power up sensors
    digitalWrite(LED_STATUS_PIN, LOW);
    
    Serial.begin(115200);
    initSensors();
}
```

### Zarządzanie stanem systemu
```cpp
// state_machine.h
#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

typedef enum {
    STATE_INIT,
    STATE_IDLE,
    STATE_MEASURING,
    STATE_TRANSMITTING,
    STATE_SLEEP,
    STATE_ERROR
} SystemState_t;

typedef enum {
    EVENT_BUTTON_PRESS,
    EVENT_TIMER_EXPIRED,
    EVENT_DATA_READY,
    EVENT_TRANSMISSION_COMPLETE,
    EVENT_ERROR_OCCURRED,
    EVENT_WAKE_UP
} SystemEvent_t;

class StateMachine {
private:
    SystemState_t currentState;
    unsigned long stateEntryTime;
    
public:
    StateMachine() : currentState(STATE_INIT), stateEntryTime(0) {}
    
    void processEvent(SystemEvent_t event);
    SystemState_t getCurrentState() { return currentState; }
    unsigned long getStateTime() { return millis() - stateEntryTime; }
    
private:
    void changeState(SystemState_t newState);
    void handleInitState(SystemEvent_t event);
    void handleIdleState(SystemEvent_t event);
    void handleMeasuringState(SystemEvent_t event);
    void handleTransmittingState(SystemEvent_t event);
    void handleSleepState(SystemEvent_t event);
    void handleErrorState(SystemEvent_t event);
};

// Implementacja
void StateMachine::processEvent(SystemEvent_t event) {
    switch (currentState) {
        case STATE_INIT:
            handleInitState(event);
            break;
        case STATE_IDLE:
            handleIdleState(event);
            break;
        case STATE_MEASURING:
            handleMeasuringState(event);
            break;
        case STATE_TRANSMITTING:
            handleTransmittingState(event);
            break;
        case STATE_SLEEP:
            handleSleepState(event);
            break;
        case STATE_ERROR:
            handleErrorState(event);
            break;
    }
}

void StateMachine::changeState(SystemState_t newState) {
    if (currentState != newState) {
        Serial.print("State: ");
        Serial.print(currentState);
        Serial.print(" -> ");
        Serial.println(newState);
        
        currentState = newState;
        stateEntryTime = millis();
    }
}
```

## Debugowanie systemów embedded

### Serial Monitor debugging
```cpp
// debug.h
#ifndef DEBUG_H
#define DEBUG_H

#ifdef DEBUG_MODE
    #define DEBUG_PRINT(x)     Serial.print(x)
    #define DEBUG_PRINTLN(x)   Serial.println(x)
    #define DEBUG_PRINTF(...)  Serial.printf(__VA_ARGS__)
#else
    #define DEBUG_PRINT(x)
    #define DEBUG_PRINTLN(x)
    #define DEBUG_PRINTF(...)
#endif

// Debug levels
typedef enum {
    LOG_ERROR = 0,
    LOG_WARN  = 1,
    LOG_INFO  = 2,
    LOG_DEBUG = 3
} LogLevel_t;

class Logger {
private:
    LogLevel_t currentLevel;
    
public:
    Logger(LogLevel_t level = LOG_INFO) : currentLevel(level) {}
    
    void error(const char* message) { log(LOG_ERROR, "ERROR", message); }
    void warn(const char* message)  { log(LOG_WARN,  "WARN",  message); }
    void info(const char* message)  { log(LOG_INFO,  "INFO",  message); }
    void debug(const char* message) { log(LOG_DEBUG, "DEBUG", message); }
    
private:
    void log(LogLevel_t level, const char* levelStr, const char* message) {
        if (level <= currentLevel) {
            Serial.print("[");
            Serial.print(millis());
            Serial.print("] ");
            Serial.print(levelStr);
            Serial.print(": ");
            Serial.println(message);
        }
    }
};

extern Logger logger;
#endif

// Użycie
Logger logger(LOG_DEBUG);

void setup() {
    Serial.begin(115200);
    logger.info("System starting...");
}

void loop() {
    int sensorValue = analogRead(A0);
    
    if (sensorValue < 100) {
        logger.warn("Low sensor reading");
    } else if (sensorValue > 900) {
        logger.error("Sensor reading too high!");
    } else {
        logger.debug("Sensor OK");
    }
}
```

### Memory debugging
```cpp
// memory.h
#ifndef MEMORY_H
#define MEMORY_H

class MemoryMonitor {
public:
    static int getFreeRAM() {
        #ifdef __AVR__
        extern int __heap_start, *__brkval;
        int v;
        return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
        #elif defined(ESP32)
        return ESP.getFreeHeap();
        #elif defined(ESP8266)
        return ESP.getFreeHeap();
        #else
        return -1;  // Unknown platform
        #endif
    }
    
    static void printMemoryStats() {
        Serial.print("Free RAM: ");
        Serial.print(getFreeRAM());
        Serial.println(" bytes");
        
        #ifdef ESP32
        Serial.print("Free heap: ");
        Serial.print(ESP.getFreeHeap());
        Serial.println(" bytes");
        Serial.print("Largest free block: ");
        Serial.print(ESP.getMaxAllocHeap());
        Serial.println(" bytes");
        #endif
    }
};

// Stack overflow detection
class StackMonitor {
private:
    static const uint16_t STACK_CANARY = 0xDEAD;
    uint16_t* stackBase;
    
public:
    StackMonitor() {
        // Place canary at current stack position
        volatile uint16_t canary = STACK_CANARY;
        stackBase = (uint16_t*)&canary;
    }
    
    bool checkStack() {
        return (*stackBase == STACK_CANARY);
    }
};
#endif
```

### Watchdog Timer
```cpp
#include <avr/wdt.h>

class WatchdogTimer {
private:
    bool enabled;
    
public:
    WatchdogTimer() : enabled(false) {}
    
    void enable(uint8_t timeout = WDTO_2S) {
        wdt_enable(timeout);
        enabled = true;
        Serial.println("Watchdog enabled");
    }
    
    void disable() {
        if (enabled) {
            wdt_disable();
            enabled = false;
            Serial.println("Watchdog disabled");
        }
    }
    
    void reset() {
        if (enabled) {
            wdt_reset();
        }
    }
    
    void forceReset() {
        Serial.println("Forcing system reset...");
        Serial.flush();
        while(true) {
            // Wait for watchdog to reset system
        }
    }
};

WatchdogTimer watchdog;

void setup() {
    Serial.begin(115200);
    watchdog.enable(WDTO_8S);  // 8 second timeout
}

void loop() {
    // Main program tasks
    performSensorReading();
    processData();
    handleCommunication();
    
    // Reset watchdog to prevent system reset
    watchdog.reset();
    
    delay(100);
}
```

## Optymalizacja kodu

### Optymalizacja pamięci PROGMEM
```cpp
#include <avr/pgmspace.h>

// Przechowywanie stałych w pamięci Flash zamiast RAM
const char string_0[] PROGMEM = "Hello World";
const char string_1[] PROGMEM = "Sensor Error";
const char string_2[] PROGMEM = "System Ready";

const char* const string_table[] PROGMEM = {
    string_0,
    string_1,
    string_2
};

void printPROGMEMString(uint8_t index) {
    char buffer[30];
    strcpy_P(buffer, (char*)pgm_read_word(&(string_table[index])));
    Serial.println(buffer);
}

// Tablica lookup w PROGMEM
const uint16_t sin_table[] PROGMEM = {
    0, 6, 13, 19, 25, 31, 37, 44, 50, 56,
    62, 68, 74, 80, 86, 92, 98, 104, 109, 115
};

uint16_t getSinValue(uint8_t index) {
    return pgm_read_word_near(sin_table + index);
}
```

### Optymalizacja czasów wykonania
```cpp
// Unikaj dzielenia - użyj przesunięć bitowych
uint16_t divide_by_8(uint16_t value) {
    return value >> 3;  // Zamiast value / 8
}

uint16_t multiply_by_16(uint16_t value) {
    return value << 4;  // Zamiast value * 16
}

// Prekalkulacja wartości
class LookupTable {
private:
    static const uint8_t TABLE_SIZE = 256;
    uint16_t sqrtTable[TABLE_SIZE];
    
public:
    LookupTable() {
        // Prekalkuluj wartości przy inicjalizacji
        for (int i = 0; i < TABLE_SIZE; i++) {
            sqrtTable[i] = (uint16_t)(sqrt(i) * 100);  // x100 dla precyzji
        }
    }
    
    uint16_t fastSqrt(uint8_t value) {
        return sqrtTable[value];
    }
};

// Optymalizacja pętli
void optimizedLoop() {
    // Złe - sprawdza warunek za każdym razem
    for (int i = 0; i < getArraySize(); i++) {
        processElement(i);
    }
    
    // Dobre - cache'uj wartość
    int arraySize = getArraySize();
    for (int i = 0; i < arraySize; i++) {
        processElement(i);
    }
    
    // Jeszcze lepsze - odliczanie do zera (jeśli kolejność nie ma znaczenia)
    int arraySize = getArraySize();
    for (int i = arraySize - 1; i >= 0; i--) {
        processElement(i);
    }
}
```

### Volatile i atomic operations
```cpp
// Volatile dla zmiennych modyfikowanych w przerwaniach
volatile bool dataReady = false;
volatile uint32_t pulseCount = 0;
volatile uint16_t adcValue = 0;

ISR(TIMER1_OVF_vect) {
    dataReady = true;
    pulseCount++;
}

void loop() {
    if (dataReady) {
        // Atomic read dla większych typów
        cli();  // Disable interrupts
        uint32_t localPulseCount = pulseCount;
        sei();  // Enable interrupts
        
        processData(localPulseCount);
        dataReady = false;
    }
}

// Atomowe operacje dla ESP32/ARM
#ifdef ESP32
#include "esp32-hal.h"

volatile int32_t sharedCounter = 0;

void incrementCounter() {
    portENTER_CRITICAL(&mux);
    sharedCounter++;
    portEXIT_CRITICAL(&mux);
}

int32_t readCounter() {
    portENTER_CRITICAL(&mux);
    int32_t value = sharedCounter;
    portEXIT_CRITICAL(&mux);
    return value;
}
#endif
```

## Zarządzanie konfiguracją

### EEPROM configuration
```cpp
#include <EEPROM.h>

struct SystemConfig {
    uint16_t magic;           // Magic number for validation
    uint8_t version;          // Config version
    uint16_t sensorInterval;  // ms
    uint8_t ledBrightness;   // 0-255
    float calibrationOffset;
    float calibrationScale;
    char deviceName[16];
    uint16_t checksum;       // Simple checksum
};

class ConfigManager {
private:
    static const uint16_t MAGIC_NUMBER = 0xCAFE;
    static const uint8_t CONFIG_VERSION = 1;
    static const int CONFIG_ADDRESS = 0;
    
    SystemConfig config;
    
public:
    bool loadConfig() {
        EEPROM.get(CONFIG_ADDRESS, config);
        
        // Validate magic number and checksum
        if (config.magic != MAGIC_NUMBER || 
            config.version != CONFIG_VERSION ||
            !validateChecksum()) {
            
            Serial.println("Invalid config, loading defaults");
            loadDefaults();
            return false;
        }
        
        Serial.println("Config loaded successfully");
        return true;
    }
    
    void saveConfig() {
        config.magic = MAGIC_NUMBER;
        config.version = CONFIG_VERSION;
        calculateChecksum();
        
        EEPROM.put(CONFIG_ADDRESS, config);
        Serial.println("Config saved");
    }
    
    void loadDefaults() {
        config.magic = MAGIC_NUMBER;
        config.version = CONFIG_VERSION;
        config.sensorInterval = 1000;
        config.ledBrightness = 128;
        config.calibrationOffset = 0.0;
        config.calibrationScale = 1.0;
        strcpy(config.deviceName, "Sensor_01");
        
        saveConfig();
    }
    
    // Getters/Setters
    uint16_t getSensorInterval() { return config.sensorInterval; }
    void setSensorInterval(uint16_t interval) { config.sensorInterval = interval; }
    
    uint8_t getLedBrightness() { return config.ledBrightness; }
    void setLedBrightness(uint8_t brightness) { config.ledBrightness = brightness; }
    
private:
    void calculateChecksum() {
        uint16_t sum = 0;
        uint8_t* data = (uint8_t*)&config;
        for (size_t i = 0; i < sizeof(config) - sizeof(config.checksum); i++) {
            sum += data[i];
        }
        config.checksum = sum;
    }
    
    bool validateChecksum() {
        uint16_t sum = 0;
        uint8_t* data = (uint8_t*)&config;
        for (size_t i = 0; i < sizeof(config) - sizeof(config.checksum); i++) {
            sum += data[i];
        }
        return (sum == config.checksum);
    }
};

ConfigManager configManager;

void setup() {
    Serial.begin(115200);
    
    if (!configManager.loadConfig()) {
        Serial.println("Using default configuration");
    }
    
    // Use configuration
    uint16_t interval = configManager.getSensorInterval();
    Serial.print("Sensor interval: ");
    Serial.println(interval);
}
```

## Command Line Interface (CLI)

### Simple CLI implementation
```cpp
class CommandProcessor {
private:
    static const int MAX_COMMAND_LENGTH = 64;
    char commandBuffer[MAX_COMMAND_LENGTH];
    int bufferIndex;
    
public:
    CommandProcessor() : bufferIndex(0) {
        memset(commandBuffer, 0, MAX_COMMAND_LENGTH);
    }
    
    void processInput() {
        while (Serial.available()) {
            char c = Serial.read();
            
            if (c == '\n' || c == '\r') {
                if (bufferIndex > 0) {
                    commandBuffer[bufferIndex] = '\0';
                    executeCommand(commandBuffer);
                    bufferIndex = 0;
                    memset(commandBuffer, 0, MAX_COMMAND_LENGTH);
                }
                Serial.print("> ");
            } else if (c == '\b' || c == 127) {  // Backspace
                if (bufferIndex > 0) {
                    bufferIndex--;
                    commandBuffer[bufferIndex] = '\0';
                    Serial.print("\b \b");  // Clear character
                }
            } else if (bufferIndex < MAX_COMMAND_LENGTH - 1) {
                commandBuffer[bufferIndex++] = c;
                Serial.print(c);  // Echo character
            }
        }
    }
    
private:
    void executeCommand(const char* command) {
        Serial.println();  // New line after command
        
        // Parse command and arguments
        char* token = strtok((char*)command, " ");
        if (token == NULL) return;
        
        String cmd = String(token);
        cmd.toLowerCase();
        
        if (cmd == "help") {
            printHelp();
        } else if (cmd == "status") {
            printStatus();
        } else if (cmd == "reset") {
            Serial.println("Resetting system...");
            delay(1000);
            asm volatile ("  jmp 0");  // AVR reset
        } else if (cmd == "config") {
            handleConfigCommand();
        } else if (cmd == "sensor") {
            handleSensorCommand();
        } else {
            Serial.println("Unknown command. Type 'help' for available commands.");
        }
    }
    
    void printHelp() {
        Serial.println("Available commands:");
        Serial.println("  help     - Show this help");
        Serial.println("  status   - Show system status");
        Serial.println("  reset    - Reset the system");
        Serial.println("  config   - Show configuration");
        Serial.println("  sensor   - Read sensor values");
    }
    
    void printStatus() {
        Serial.println("System Status:");
        Serial.print("  Uptime: ");
        Serial.print(millis() / 1000);
        Serial.println(" seconds");
        Serial.print("  Free RAM: ");
        Serial.print(MemoryMonitor::getFreeRAM());
        Serial.println(" bytes");
        Serial.print("  Version: ");
        Serial.println(SYSTEM_VERSION);
    }
    
    void handleConfigCommand() {
        Serial.println("Configuration:");
        Serial.print("  Sensor interval: ");
        Serial.print(configManager.getSensorInterval());
        Serial.println(" ms");
        Serial.print("  LED brightness: ");
        Serial.println(configManager.getLedBrightness());
    }
    
    void handleSensorCommand() {
        Serial.println("Sensor readings:");
        int value = analogRead(A0);
        Serial.print("  A0: ");
        Serial.println(value);
        
        // Add more sensors as needed
    }
};

CommandProcessor cli;

void setup() {
    Serial.begin(115200);
    Serial.println("System ready");
    Serial.print("> ");
}

void loop() {
    cli.processInput();
    // Other tasks...
}
```

## Over-the-Air (OTA) Updates

### ESP32 OTA Example
```cpp
#ifdef ESP32
#include <WiFi.h>
#include <ArduinoOTA.h>

void setupOTA() {
    ArduinoOTA.setHostname("ESP32-Sensor");
    ArduinoOTA.setPassword("admin123");
    
    ArduinoOTA.onStart([]() {
        String type = (ArduinoOTA.getCommand() == U_FLASH) ? "sketch" : "filesystem";
        Serial.println("Start updating " + type);
    });
    
    ArduinoOTA.onEnd([]() {
        Serial.println("\nEnd");
    });
    
    ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
        Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
    });
    
    ArduinoOTA.onError([](ota_error_t error) {
        Serial.printf("Error[%u]: ", error);
        if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
        else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
        else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
        else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
        else if (error == OTA_END_ERROR) Serial.println("End Failed");
    });
    
    ArduinoOTA.begin();
    Serial.println("OTA Ready");
}

void loop() {
    ArduinoOTA.handle();
    // Other tasks...
}
#endif
```

## Powiązane tematy
- [[arduino_podstawy|Arduino - Podstawy]]
- [[mikrokontrolery_vs_mikroprocesory|Mikrokontrolery vs Mikroprocesory]]
- [[memory_management|Zarządzanie Pamięcią w Embedded]]
- [[testing_embedded|Testowanie Systemów Embedded]]
- [[rtos_freertos|RTOS i FreeRTOS]]
- [[debugging_embedded|Debugowanie w Embedded]]