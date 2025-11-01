# Słowo kluczowe const w Embedded C

## Wprowadzenie

`const` w programowaniu embedded ma kluczowe znaczenie nie tylko dla poprawności kodu, ale przede wszystkim dla **optymalizacji wykorzystania pamięci**. Dane oznaczone jako `const` trafiają do pamięci Flash zamiast RAM, co jest krytyczne w systemach o ograniczonych zasobach.

## Podstawy const

### Stałe dane
```c
const uint32_t max_value = 1000;
const float pi = 3.14159f;

// Próba modyfikacji - błąd kompilacji
max_value = 2000;  // BŁĄD!
```

### const vs #define
```c
// Makro preprocesora
#define MAX_SIZE 100

// Stała const
const uint16_t max_size = 100;
```

| Cecha | #define | const |
|-------|---------|-------|
| Type safety | ❌ Nie | ✅ Tak |
| Debugowanie | ❌ Trudne | ✅ Łatwe |
| Scope | Globalny | Można ograniczyć |
| Pamięć | Nie zajmuje | Zajmuje Flash |
| Wskaźnik | ❌ Nie można | ✅ Można |

### Zalety const
```c
// ✅ Typ checking
const uint32_t timeout = 1000;
const float voltage = 3.3f;

// ✅ Można tworzyć wskaźniki
const uint32_t *ptr = &timeout;

// ✅ Scope kontrola
void function(void) {
    const uint8_t local_const = 10;  // Tylko w funkcji
}

// ✅ Debugowanie - widoczne w debuggerze
```

## const a pamięć Flash vs RAM

### Umieszczenie w Flash (oszczędność RAM!)
```c
// Tablica const - w Flash, nie zajmuje RAM!
const uint8_t sine_table[256] = {
    128, 131, 134, 137, 140, 143, 146, 149,
    // ... reszta wartości
};

// Tablica bez const - w RAM, marnowanie cennej pamięci!
uint8_t sine_table_ram[256] = { /* ... */ };

// Oszczędność: 256 bajtów RAM!
```

### Tablice lookup
```c
// Tabela gamma correction - 1KB w Flash zamiast RAM
const uint8_t gamma_table[256] = {
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
    // ... pełna tabela
};

// Użycie
uint8_t corrected_value = gamma_table[raw_value];
```

### Stringi
```c
// ✅ DOBRZE - string w Flash
const char* message = "Hello World";

// ✅ JESZCZE LEPIEJ
const char message[] = "Hello World";

// ❌ ŹLE - string w RAM!
char message[] = "Hello World";
```

## Różne użycia const

### 1. Wskaźnik do const danych
```c
const uint8_t *ptr;

uint8_t data = 100;
ptr = &data;      // OK

*ptr = 200;       // BŁĄD - dane są const
ptr = &other;     // OK - wskaźnik nie jest const
```

### 2. Const wskaźnik
```c
uint8_t * const ptr = &data;

*ptr = 200;       // OK - dane nie są const
ptr = &other;     // BŁĄD - wskaźnik jest const
```

### 3. Const wskaźnik do const danych
```c
const uint8_t * const ptr = &data;

*ptr = 200;       // BŁĄD - dane są const
ptr = &other;     // BŁĄD - wskaźnik jest const
```

### Przykłady praktyczne
```c
// Funkcja przyjmująca dane tylko do odczytu
void process_data(const uint8_t *data, uint16_t length) {
    for(uint16_t i = 0; i < length; i++) {
        uart_send(data[i]);  // OK - tylko odczyt
        // data[i] = 0;      // BŁĄD - próba modyfikacji
    }
}

// Tablica parametrów konfiguracyjnych w Flash
const uint32_t baud_rates[] = {
    9600, 19200, 38400, 57600, 115200
};

// Funkcja zwracająca const wskaźnik
const char* get_error_message(uint8_t error_code) {
    static const char* errors[] = {
        "No error",
        "Timeout",
        "Invalid parameter",
        "Hardware failure"
    };
    
    if(error_code < 4) {
        return errors[error_code];
    }
    return "Unknown error";
}
```

## const w strukturach

### Pola const w strukturze
```c
typedef struct {
    const uint32_t id;        // Można ustawić tylko raz
    uint32_t value;           // Można modyfikować
    const uint8_t version;    // Const
} config_t;

// Inicjalizacja
config_t cfg = {
    .id = 0x12345678,
    .value = 0,
    .version = 1
};

cfg.value = 100;      // OK
cfg.id = 0;           // BŁĄD - const
```

### Cała struktura const
```c
typedef struct {
    uint32_t address;
    uint16_t size;
    uint8_t type;
} memory_region_t;

// Stała definicja regionów pamięci - w Flash!
const memory_region_t memory_map[] = {
    {0x08000000, 64*1024, FLASH_TYPE},
    {0x20000000, 20*1024, SRAM_TYPE},
    {0x40000000, 512*1024*1024, PERIPH_TYPE}
};
```

## const z volatile

### Rejestry tylko do odczytu
```c
// Typowy przypadek - status rejestry, ID chipu
const volatile uint32_t *chip_id_reg = 
    (const volatile uint32_t*)0x1FFF7A10;

uint32_t id = *chip_id_reg;  // OK - odczyt
*chip_id_reg = 0;            // BŁĄD - const

// Struktura rejestrów
typedef struct {
    volatile uint32_t CR;           // Read/Write
    const volatile uint32_t SR;     // Read-only status
    volatile uint32_t DR;           // Read/Write data
    const volatile uint32_t ID;     // Read-only ID
} PERIPHERAL_TypeDef;
```

## const w funkcjach

### Parametry const
```c
// Obietnica: funkcja nie modyfikuje danych
uint16_t calculate_checksum(const uint8_t *data, uint16_t length) {
    uint16_t sum = 0;
    for(uint16_t i = 0; i < length; i++) {
        sum += data[i];  // Tylko odczyt
    }
    return sum;
}

// Użycie
const uint8_t packet[] = {0x01, 0x02, 0x03};
uint16_t crc = calculate_checksum(packet, sizeof(packet));
```

### Zwracanie const wskaźników
```c
// Zwraca wskaźnik do danych w Flash
const char* get_version(void) {
    return "v1.2.3";  // String literal w Flash
}

// Użycie
const char *ver = get_version();
uart_send_string(ver);
```

## Optymalizacja z const

### Tablice lookup w Flash
```c
// Tabela konwersji 7-segment display - 10 bajtów w Flash
const uint8_t seven_seg_digits[10] = {
    0b00111111,  // 0
    0b00000110,  // 1
    0b01011011,  // 2
    0b01001111,  // 3
    0b01100110,  // 4
    0b01101101,  // 5
    0b01111101,  // 6
    0b00000111,  // 7
    0b01111111,  // 8
    0b01101111   // 9
};

void display_digit(uint8_t digit) {
    if(digit < 10) {
        PORTB = seven_seg_digits[digit];
    }
}
```

### Duże struktury danych
```c
// Bitmapa 128x64 = 1024 bajty w Flash, nie w RAM!
const uint8_t logo_bitmap[1024] = {
    0xFF, 0xFF, 0xFF, 0xFF, // ...
    // Pełna bitmapa
};

void display_logo(void) {
    // DMA może czytać bezpośrednio z Flash
    lcd_draw_bitmap(0, 0, logo_bitmap, 128, 64);
}
```

### Tabele konfiguracyjne
```c
typedef struct {
    uint32_t gpio_port;
    uint16_t pin;
    uint8_t mode;
} pin_config_t;

// Konfiguracja wszystkich pinów - w Flash
const pin_config_t pin_config[] = {
    {GPIOA_BASE, 0, GPIO_MODE_INPUT},
    {GPIOA_BASE, 1, GPIO_MODE_OUTPUT},
    {GPIOA_BASE, 5, GPIO_MODE_AF},
    // ... wszystkie piny
};

void init_all_pins(void) {
    for(uint8_t i = 0; i < sizeof(pin_config)/sizeof(pin_config[0]); i++) {
        gpio_init(pin_config[i].gpio_port, 
                  pin_config[i].pin, 
                  pin_config[i].mode);
    }
}
```

## const w różnych kontekstach

### Zmienne globalne const
```c
// W pliku .c
const uint32_t system_frequency = 168000000;  // W Flash
const uint8_t hardware_version = 2;

// W pliku .h
extern const uint32_t system_frequency;
extern const uint8_t hardware_version;
```

### Static const w funkcji
```c
uint32_t get_random_seed(void) {
    // Inicjalizowana tylko raz, przechowywana w Flash
    static const uint32_t seed_table[] = {
        0x12345678, 0x9ABCDEF0, 0x11223344, 0x55667788
    };
    
    static uint8_t index = 0;
    return seed_table[index++ % 4];
}
```

### const w enumach i #define
```c
// Enum - wartości są const, ale typ jest int
typedef enum {
    STATE_IDLE = 0,
    STATE_ACTIVE,
    STATE_ERROR
} state_t;

// Gdy potrzebujesz konkretnego typu:
const uint8_t STATE_IDLE = 0;
const uint8_t STATE_ACTIVE = 1;
const uint8_t STATE_ERROR = 2;
```

## Przykłady zaawansowane

### Menu system
```c
typedef struct {
    const char *text;
    void (*action)(void);
} menu_item_t;

// Cała struktura menu w Flash
const menu_item_t main_menu[] = {
    {"1. Settings", settings_menu},
    {"2. Diagnostics", diagnostics_menu},
    {"3. About", about_screen},
    {"4. Exit", exit_menu}
};

const uint8_t menu_size = sizeof(main_menu) / sizeof(menu_item_t);

void display_menu(void) {
    for(uint8_t i = 0; i < menu_size; i++) {
        lcd_print(main_menu[i].text);
    }
}

void handle_menu_selection(uint8_t selection) {
    if(selection < menu_size) {
        main_menu[selection].action();
    }
}
```

### Tabele sinus/cosinus
```c
// Tabela sinusa 0-90° co 1° (oszczędność Flash vs RAM)
const int16_t sin_table_90[91] = {
    0, 17, 35, 52, 70, 87, 105, 122, 139, 156,
    // ... wartości * 1000 dla precyzji
};

int16_t fast_sin(uint16_t angle_deg) {
    angle_deg = angle_deg % 360;
    
    if(angle_deg <= 90) {
        return sin_table_90[angle_deg];
    } else if(angle_deg <= 180) {
        return sin_table_90[180 - angle_deg];
    } else if(angle_deg <= 270) {
        return -sin_table_90[angle_deg - 180];
    } else {
        return -sin_table_90[360 - angle_deg];
    }
}
```

### Protokół komunikacyjny
```c
typedef struct {
    uint8_t cmd_id;
    const char *name;
    uint8_t expected_length;
    void (*handler)(const uint8_t *data);
} command_t;

const command_t commands[] = {
    {0x01, "READ",  4, handle_read_command},
    {0x02, "WRITE", 8, handle_write_command},
    {0x03, "RESET", 0, handle_reset_command},
};

void process_command(uint8_t cmd_id, const uint8_t *data) {
    for(uint8_t i = 0; i < sizeof(commands)/sizeof(command_t); i++) {
        if(commands[i].cmd_id == cmd_id) {
            commands[i].handler(data);
            return;
        }
    }
}
```

## Częste błędy

### Błąd 1: Modyfikacja const przez wskaźnik
```c
const uint32_t value = 100;

// ❌ Obejście const - undefined behavior!
uint32_t *ptr = (uint32_t*)&value;
*ptr = 200;  // Może crashować lub nie działać
```

### Błąd 2: Przekazywanie const jako non-const
```c
void modify_data(uint8_t *data, uint16_t len) {
    data[0] = 0xFF;
}

const uint8_t buffer[10] = {0};
modify_data(buffer, 10);  // Warning! Usuwa const
```

### Błąd 3: Zapominanie o const dla dużych danych
```c
// ❌ Marnowanie 1KB RAM!
uint8_t font_data[1024] = { /* dane */ };

// ✅ 1KB w Flash
const uint8_t font_data[1024] = { /* dane */ };
```

## const w różnych kompilatorach

### GCC attributes
```c
// Wymuszenie umieszczenia w Flash
const uint8_t data[100] __attribute__((section(".rodata")));

// Wyrównanie
const uint32_t aligned_data[100] __attribute__((aligned(16)));
```

### PROGMEM (AVR)
```c
#include <avr/pgmspace.h>

// Explicit umieszczenie w Flash (AVR)
const uint8_t data[100] PROGMEM = { /* ... */ };

// Odczyt wymaga specjalnych funkcji
uint8_t value = pgm_read_byte(&data[index]);
```

## Weryfikacja umieszczenia w pamięci

### Mapa pamięci (map file)
```bash
# Kompilacja z mapą
arm-none-eabi-gcc ... -Wl,-Map=output.map

# W pliku output.map szukaj:
# .rodata - dane const w Flash
# .data   - dane inicjalizowane w RAM
# .bss    - dane niezainicjalizowane w RAM
```

### Sprawdzenie w runtime
```c
#define FLASH_BASE 0x08000000
#define FLASH_END  0x08100000
#define SRAM_BASE  0x20000000
#define SRAM_END   0x20020000

bool is_in_flash(const void *ptr) {
    uint32_t addr = (uint32_t)ptr;
    return (addr >= FLASH_BASE) && (addr < FLASH_END);
}

bool is_in_sram(const void *ptr) {
    uint32_t addr = (uint32_t)ptr;
    return (addr >= SRAM_BASE) && (addr < SRAM_END);
}

// Test
const uint8_t flash_data[] = {1, 2, 3};
uint8_t ram_data[] = {1, 2, 3};

// is_in_flash(&flash_data) == true
// is_in_sram(&ram_data) == true
```

## Podsumowanie

### Używaj const dla:
- ✅ Tablic lookup (sine, gamma, itp.)
- ✅ Stringów tekstowych
- ✅ Konfiguracji sprzętowej
- ✅ Bitmap, fonty, ikony
- ✅ Parametrów funkcji (tylko odczyt)
- ✅ Rejestrów tylko do odczytu
- ✅ Wszystkich danych które się nie zmieniają

### Korzyści:
- 💾 Oszczędność RAM (dane w Flash)
- 🔒 Ochrona przed modyfikacją
- ✅ Type safety
- 🐛 Łatwiejsze debugowanie
- 📊 Kompilator może lepiej optymalizować

### Pamiętaj:
- const w embedded = Flash, nie RAM!
- Używaj const wszędzie gdzie możliwe
- const z volatile dla rejestrów RO
- const nie czyni kodu wolniejszym

## Powiązane tematy
- [[typy_danych_embedded_c|Typy danych w Embedded C]]
- [[volatile_keyword|Słowo kluczowe volatile]]
- [[optymalizacja_pamieci|Optymalizacja wykorzystania pamięci]]
- [[wskazniki_adresowanie|Wskaźniki i adresowanie pamięci]]
