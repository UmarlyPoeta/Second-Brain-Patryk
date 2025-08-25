# Zarządzanie Pamięcią w Systemach Embedded

## Typy pamięci w mikrokontrolerach

### Flash Memory (Program Memory)
- **Przeznaczenie**: Kod programu, stałe, lookup tables
- **Charakterystyka**: Non-volatile, wolny zapis, szybki odczyt
- **Rozmiary**: 8KB-2MB (typowo w MCU)
- **Cykle write/erase**: ~10,000-100,000

```cpp
// Przechowywanie danych w Flash (Arduino/AVR)
#include <avr/pgmspace.h>

// Definicja tablicy w PROGMEM
const uint8_t lookup_table[] PROGMEM = {
    0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70,
    0x80, 0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0
};

const char welcome_msg[] PROGMEM = "System initialized successfully!";

// Odczyt z PROGMEM
uint8_t getValue(uint8_t index) {
    return pgm_read_byte_near(lookup_table + index);
}

void printWelcomeMessage() {
    char buffer[50];
    strcpy_P(buffer, welcome_msg);
    Serial.println(buffer);
}
```

### RAM (Data Memory)
- **Przeznaczenie**: Zmienne, stos, heap
- **Charakterystyka**: Volatile, szybki dostęp, ograniczona pojemność
- **Rozmiary**: 512B-64KB (typowo w MCU)

```cpp
// Monitorowanie użycia RAM (AVR)
int getFreeRAM() {
    extern int __heap_start, *__brkval;
    int v;
    return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}

// ESP32 - więcej informacji o pamięci
#ifdef ESP32
void printMemoryInfo() {
    Serial.println("=== Memory Information ===");
    Serial.printf("Free heap: %d bytes\n", ESP.getFreeHeap());
    Serial.printf("Largest free block: %d bytes\n", ESP.getMaxAllocHeap());
    Serial.printf("Total heap size: %d bytes\n", ESP.getHeapSize());
    Serial.printf("Free PSRAM: %d bytes\n", ESP.getFreePsram());
}
#endif
```

### EEPROM (Electrically Erasable Programmable ROM)
- **Przeznaczenie**: Konfiguracja, kalibracja, dane użytkownika
- **Charakterystyka**: Non-volatile, wolny zapis, długa żywotność
- **Rozmiary**: 256B-4KB (typowo w AVR)

```cpp
#include <EEPROM.h>

// Struktura konfiguracji
struct Config {
    uint16_t magic;
    uint8_t version;
    uint16_t sensorInterval;
    float calibrationValue;
    char deviceName[16];
    uint16_t crc;
};

class EEPROMManager {
private:
    static const uint16_t MAGIC_NUMBER = 0xCAFE;
    static const uint8_t CONFIG_VERSION = 1;
    
public:
    bool saveConfig(const Config& config) {
        Config configToSave = config;
        configToSave.magic = MAGIC_NUMBER;
        configToSave.version = CONFIG_VERSION;
        configToSave.crc = calculateCRC(configToSave);
        
        EEPROM.put(0, configToSave);
        return true;
    }
    
    bool loadConfig(Config& config) {
        EEPROM.get(0, config);
        
        if (config.magic != MAGIC_NUMBER || 
            config.version != CONFIG_VERSION ||
            config.crc != calculateCRC(config)) {
            return false;
        }
        return true;
    }
    
private:
    uint16_t calculateCRC(const Config& config) {
        uint16_t crc = 0;
        const uint8_t* data = (const uint8_t*)&config;
        
        for (size_t i = 0; i < sizeof(Config) - sizeof(config.crc); i++) {
            crc ^= data[i];
            for (int j = 0; j < 8; j++) {
                if (crc & 0x01) {
                    crc = (crc >> 1) ^ 0xA001;
                } else {
                    crc >>= 1;
                }
            }
        }
        return crc;
    }
};
```

## Zarządzanie stosem (Stack)

### Stack overflow detection
```cpp
class StackGuard {
private:
    static const uint16_t STACK_CANARY = 0xDEAD;
    uint16_t* canaryLocation;
    size_t stackDepth;
    
public:
    StackGuard() {
        // Umieść wartownika na stosie
        volatile uint16_t canary = STACK_CANARY;
        canaryLocation = (uint16_t*)&canary;
        stackDepth = 0;
    }
    
    void placeCanary() {
        volatile uint16_t canary = STACK_CANARY;
        stackDepth++;
    }
    
    bool checkStack() {
        return (*canaryLocation == STACK_CANARY);
    }
    
    size_t getMaxStackUsage() {
        uint16_t* current = canaryLocation;
        size_t usage = 0;
        
        // Szukaj pierwszego niezmodyfikowanego bajtu
        while (*current == STACK_CANARY && current > (uint16_t*)0x100) {
            current--;
            usage += sizeof(uint16_t);
        }
        
        return usage;
    }
};

// Użycie
StackGuard stackGuard;

void deepRecursiveFunction(int depth) {
    if (depth > 0) {
        stackGuard.placeCanary();
        
        volatile char buffer[64];  // Symulacja użycia stosu
        for (int i = 0; i < 64; i++) {
            buffer[i] = depth;
        }
        
        deepRecursiveFunction(depth - 1);
    }
    
    if (!stackGuard.checkStack()) {
        Serial.println("STACK OVERFLOW DETECTED!");
    }
}
```

## Zarządzanie stertą (Heap)

### Custom allocators
```cpp
class SimpleAllocator {
private:
    static const size_t HEAP_SIZE = 1024;
    uint8_t heap[HEAP_SIZE];
    size_t nextFree;
    
    struct Block {
        size_t size;
        bool inUse;
        Block* next;
    };
    
    Block* firstBlock;
    
public:
    SimpleAllocator() : nextFree(0), firstBlock(nullptr) {
        firstBlock = (Block*)heap;
        firstBlock->size = HEAP_SIZE - sizeof(Block);
        firstBlock->inUse = false;
        firstBlock->next = nullptr;
    }
    
    void* allocate(size_t size) {
        size = (size + 3) & ~3;  // Align to 4 bytes
        
        Block* current = firstBlock;
        while (current) {
            if (!current->inUse && current->size >= size) {
                // Split block if necessary
                if (current->size > size + sizeof(Block) + 4) {
                    Block* newBlock = (Block*)((uint8_t*)current + sizeof(Block) + size);
                    newBlock->size = current->size - size - sizeof(Block);
                    newBlock->inUse = false;
                    newBlock->next = current->next;
                    current->next = newBlock;
                    current->size = size;
                }
                
                current->inUse = true;
                return (uint8_t*)current + sizeof(Block);
            }
            current = current->next;
        }
        
        return nullptr;  // Out of memory
    }
    
    void deallocate(void* ptr) {
        if (!ptr) return;
        
        Block* block = (Block*)((uint8_t*)ptr - sizeof(Block));
        block->inUse = false;
        
        // Coalesce with next block if free
        if (block->next && !block->next->inUse) {
            block->size += sizeof(Block) + block->next->size;
            block->next = block->next->next;
        }
        
        // Coalesce with previous block if free
        Block* current = firstBlock;
        while (current && current->next != block) {
            current = current->next;
        }
        
        if (current && !current->inUse) {
            current->size += sizeof(Block) + block->size;
            current->next = block->next;
        }
    }
    
    void printStats() {
        Serial.println("=== Heap Statistics ===");
        Block* current = firstBlock;
        size_t totalFree = 0, totalUsed = 0;
        int blockCount = 0;
        
        while (current) {
            if (current->inUse) {
                totalUsed += current->size;
            } else {
                totalFree += current->size;
            }
            blockCount++;
            current = current->next;
        }
        
        Serial.printf("Total blocks: %d\n", blockCount);
        Serial.printf("Used memory: %d bytes\n", totalUsed);
        Serial.printf("Free memory: %d bytes\n", totalFree);
        Serial.printf("Fragmentation: %.1f%%\n", 
                     (float)(blockCount - 1) / blockCount * 100);
    }
};

SimpleAllocator customAllocator;

// Przykład użycia
void* my_malloc(size_t size) {
    return customAllocator.allocate(size);
}

void my_free(void* ptr) {
    customAllocator.deallocate(ptr);
}
```

### Memory pools
```cpp
template<typename T, size_t POOL_SIZE>
class MemoryPool {
private:
    struct Block {
        union {
            T data;
            Block* next;
        };
    };
    
    Block pool[POOL_SIZE];
    Block* freeList;
    size_t allocatedCount;
    
public:
    MemoryPool() : freeList(nullptr), allocatedCount(0) {
        // Initialize free list
        for (size_t i = 0; i < POOL_SIZE - 1; i++) {
            pool[i].next = &pool[i + 1];
        }
        pool[POOL_SIZE - 1].next = nullptr;
        freeList = &pool[0];
    }
    
    T* allocate() {
        if (!freeList) {
            return nullptr;  // Pool exhausted
        }
        
        Block* block = freeList;
        freeList = freeList->next;
        allocatedCount++;
        
        return &block->data;
    }
    
    void deallocate(T* ptr) {
        if (!ptr) return;
        
        Block* block = reinterpret_cast<Block*>(ptr);
        block->next = freeList;
        freeList = block;
        allocatedCount--;
    }
    
    size_t available() const {
        return POOL_SIZE - allocatedCount;
    }
    
    size_t used() const {
        return allocatedCount;
    }
    
    bool full() const {
        return allocatedCount == POOL_SIZE;
    }
};

// Przykład struktury
struct SensorReading {
    uint32_t timestamp;
    float temperature;
    float humidity;
    uint16_t batteryLevel;
};

MemoryPool<SensorReading, 10> sensorPool;

void takeSensorReading() {
    SensorReading* reading = sensorPool.allocate();
    if (reading) {
        reading->timestamp = millis();
        reading->temperature = 25.5;
        reading->humidity = 60.0;
        reading->batteryLevel = 3700;
        
        // Process reading...
        processReading(reading);
        
        // Return to pool
        sensorPool.deallocate(reading);
    } else {
        Serial.println("Sensor pool full!");
    }
}
```

## Circular Buffers

### Ring buffer implementation
```cpp
template<typename T, size_t SIZE>
class CircularBuffer {
private:
    T buffer[SIZE];
    volatile size_t head;
    volatile size_t tail;
    volatile size_t count;
    
public:
    CircularBuffer() : head(0), tail(0), count(0) {}
    
    bool push(const T& item) {
        if (full()) {
            return false;
        }
        
        buffer[head] = item;
        head = (head + 1) % SIZE;
        count++;
        return true;
    }
    
    bool pop(T& item) {
        if (empty()) {
            return false;
        }
        
        item = buffer[tail];
        tail = (tail + 1) % SIZE;
        count--;
        return true;
    }
    
    bool peek(T& item) const {
        if (empty()) {
            return false;
        }
        
        item = buffer[tail];
        return true;
    }
    
    void clear() {
        head = tail = count = 0;
    }
    
    bool empty() const { return count == 0; }
    bool full() const { return count == SIZE; }
    size_t size() const { return count; }
    size_t capacity() const { return SIZE; }
    float utilization() const { return (float)count / SIZE; }
};

// Przykład dla danych sensorowych
CircularBuffer<float, 64> temperatureBuffer;

void setup() {
    Serial.begin(115200);
}

void loop() {
    // Dodaj nowy pomiar
    float temperature = analogRead(A0) * 0.1;
    
    if (!temperatureBuffer.push(temperature)) {
        // Buffer pełny - usuń najstarszy element
        float oldValue;
        temperatureBuffer.pop(oldValue);
        temperatureBuffer.push(temperature);
        Serial.println("Buffer full, oldest value discarded");
    }
    
    // Oblicz średnią ruchomą
    if (temperatureBuffer.size() >= 10) {
        float sum = 0;
        CircularBuffer<float, 64> tempCopy = temperatureBuffer;
        
        for (size_t i = 0; i < 10; i++) {
            float value;
            if (tempCopy.pop(value)) {
                sum += value;
            }
        }
        
        float average = sum / 10.0;
        Serial.printf("Average temperature: %.2f\n", average);
    }
    
    delay(1000);
}
```

## Memory Alignment i Packing

### Structure packing
```cpp
// Bez packingu - compiler alignment
struct UnpackedStruct {
    uint8_t  flag;     // 1 byte
    uint32_t value;    // 4 bytes, aligned to 4-byte boundary
    uint16_t counter;  // 2 bytes
    uint8_t  status;   // 1 byte
};
// Rozmiar: prawdopodobnie 12 bajtów (padding)

// Z packingiem - zredukowane padding
struct __attribute__((packed)) PackedStruct {
    uint8_t  flag;     // 1 byte
    uint32_t value;    // 4 bytes, bez alignment
    uint16_t counter;  // 2 bytes
    uint8_t  status;   // 1 byte
};
// Rozmiar: 8 bajtów

void demonstrateAlignment() {
    Serial.printf("UnpackedStruct size: %d bytes\n", sizeof(UnpackedStruct));
    Serial.printf("PackedStruct size: %d bytes\n", sizeof(PackedStruct));
    
    // Sprawdź alignment poszczególnych pól
    UnpackedStruct unpacked;
    Serial.printf("Unpacked offsets: flag=%d, value=%d, counter=%d, status=%d\n",
                  (int)offsetof(UnpackedStruct, flag),
                  (int)offsetof(UnpackedStruct, value),
                  (int)offsetof(UnpackedStruct, counter),
                  (int)offsetof(UnpackedStruct, status));
                  
    PackedStruct packed;
    Serial.printf("Packed offsets: flag=%d, value=%d, counter=%d, status=%d\n",
                  (int)offsetof(PackedStruct, flag),
                  (int)offsetof(PackedStruct, value),
                  (int)offsetof(PackedStruct, counter),
                  (int)offsetof(PackedStruct, status));
}
```

## Cache i Memory Optimization

### Data locality optimization
```cpp
// Zła praktyka - rozrzucone dane
struct BadDataLayout {
    float temperatures[100];
    float humidities[100];
    uint32_t timestamps[100];
    bool valid[100];
};

// Dobra praktyka - data locality
struct GoodDataLayout {
    struct {
        float temperature;
        float humidity;
        uint32_t timestamp;
        bool valid;
    } readings[100];
};

// Jeszcze lepsza - SIMD friendly
struct OptimizedDataLayout {
    struct {
        float temperature;
        float humidity;
        uint32_t timestamp;
        uint8_t valid;  // Zmniejszony rozmiar
        uint8_t padding[3];  // Explicit padding for alignment
    } readings[100];
};

void processReadings(GoodDataLayout& data) {
    // Dostęp sekwencyjny - cache friendly
    for (int i = 0; i < 100; i++) {
        if (data.readings[i].valid) {
            float temp = data.readings[i].temperature;
            float hum = data.readings[i].humidity;
            // Process data that's likely in same cache line
            processTemperatureHumidity(temp, hum);
        }
    }
}
```

### String optimization
```cpp
class StaticString {
private:
    char* buffer;
    size_t capacity;
    size_t length;
    
public:
    StaticString(char* buf, size_t cap) : buffer(buf), capacity(cap), length(0) {
        if (capacity > 0) buffer[0] = '\0';
    }
    
    bool append(const char* str) {
        size_t strLen = strlen(str);
        if (length + strLen >= capacity) {
            return false;  // Not enough space
        }
        
        strcpy(buffer + length, str);
        length += strLen;
        return true;
    }
    
    bool append(int value) {
        char numStr[12];  // Enough for 32-bit int
        itoa(value, numStr, 10);
        return append(numStr);
    }
    
    void clear() {
        length = 0;
        if (capacity > 0) buffer[0] = '\0';
    }
    
    const char* c_str() const { return buffer; }
    size_t size() const { return length; }
    size_t available() const { return capacity - length - 1; }
};

// Użycie bez alokacji dynamicznej
void buildMessage() {
    char messageBuffer[128];
    StaticString message(messageBuffer, sizeof(messageBuffer));
    
    message.append("Temperature: ");
    message.append(25);
    message.append("°C, Humidity: ");
    message.append(60);
    message.append("%");
    
    Serial.println(message.c_str());
}
```

## Memory Protection

### Stack canaries
```cpp
#ifdef __AVR__
#include <avr/interrupt.h>

class StackCanary {
private:
    static const uint16_t CANARY_VALUE = 0xDEAD;
    static uint16_t canary;
    
public:
    static void init() {
        canary = CANARY_VALUE;
    }
    
    static bool check() {
        return (canary == CANARY_VALUE);
    }
    
    static void panic() {
        cli();  // Disable interrupts
        Serial.println("STACK CORRUPTION DETECTED!");
        Serial.flush();
        
        // Force watchdog reset or infinite loop
        while(1) {
            // Infinite loop to halt system
        }
    }
};

uint16_t StackCanary::canary = 0;

// Check canary periodically
void checkStackIntegrity() {
    if (!StackCanary::check()) {
        StackCanary::panic();
    }
}
#endif
```

### Memory encryption (simple XOR)
```cpp
class SimpleMemoryProtection {
private:
    static const uint8_t XOR_KEY = 0xAA;
    
public:
    static void encryptBuffer(uint8_t* data, size_t length) {
        for (size_t i = 0; i < length; i++) {
            data[i] ^= XOR_KEY;
        }
    }
    
    static void decryptBuffer(uint8_t* data, size_t length) {
        // XOR encryption is symmetric
        encryptBuffer(data, length);
    }
};

// Przykład zabezpieczonych danych
class SecureDataStore {
private:
    uint8_t encryptedData[64];
    size_t dataLength;
    
public:
    void storeData(const uint8_t* data, size_t length) {
        if (length > sizeof(encryptedData)) return;
        
        memcpy(encryptedData, data, length);
        SimpleMemoryProtection::encryptBuffer(encryptedData, length);
        dataLength = length;
    }
    
    bool retrieveData(uint8_t* output, size_t maxLength) {
        if (dataLength > maxLength) return false;
        
        memcpy(output, encryptedData, dataLength);
        SimpleMemoryProtection::decryptBuffer(output, dataLength);
        return true;
    }
};
```

## Memory Profiling i Debug

### Memory usage tracker
```cpp
class MemoryTracker {
private:
    static size_t totalAllocated;
    static size_t peakUsage;
    static size_t allocationCount;
    
public:
    static void* allocate(size_t size) {
        void* ptr = malloc(size + sizeof(size_t));
        if (ptr) {
            *(size_t*)ptr = size;
            totalAllocated += size;
            allocationCount++;
            
            if (totalAllocated > peakUsage) {
                peakUsage = totalAllocated;
            }
            
            return (uint8_t*)ptr + sizeof(size_t);
        }
        return nullptr;
    }
    
    static void deallocate(void* ptr) {
        if (ptr) {
            uint8_t* realPtr = (uint8_t*)ptr - sizeof(size_t);
            size_t size = *(size_t*)realPtr;
            totalAllocated -= size;
            allocationCount--;
            free(realPtr);
        }
    }
    
    static void printStats() {
        Serial.println("=== Memory Tracker Stats ===");
        Serial.printf("Current allocated: %d bytes\n", totalAllocated);
        Serial.printf("Peak usage: %d bytes\n", peakUsage);
        Serial.printf("Active allocations: %d\n", allocationCount);
    }
};

size_t MemoryTracker::totalAllocated = 0;
size_t MemoryTracker::peakUsage = 0;
size_t MemoryTracker::allocationCount = 0;

// Override new/delete dla automatycznego trackingu
void* operator new(size_t size) {
    return MemoryTracker::allocate(size);
}

void operator delete(void* ptr) {
    MemoryTracker::deallocate(ptr);
}
```

## Powiązane tematy
- [[embedded_programming|Programowanie Embedded]]
- [[mikrokontrolery_vs_mikroprocesory|Mikrokontrolery vs Mikroprocesory]]
- [[arduino_podstawy|Arduino - Podstawy]]
- [[optimization_embedded|Optymalizacja w Embedded]]
- [[debugging_embedded|Debugowanie w Embedded]]
- [[rtos_freertos|RTOS i FreeRTOS]]