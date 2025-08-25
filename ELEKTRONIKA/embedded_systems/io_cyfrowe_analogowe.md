# Wejścia/Wyjścia Cyfrowe i Analogowe

## Wejścia/wyjścia cyfrowe

### Podstawy sygnałów cyfrowych
- **Poziom logiczny 0**: Zazwyczaj 0V (GND)
- **Poziom logiczny 1**: Zazwyczaj VCC (3.3V lub 5V)
- **Threshold voltage**: Poziom przełączania (Vth)
- **Rise/Fall time**: Czas narastania i opadania sygnału

### Konfiguracja pinów GPIO

#### Arduino
```cpp
void setup() {
    pinMode(13, OUTPUT);     // Pin jako wyjście
    pinMode(2, INPUT);       // Pin jako wejście
    pinMode(3, INPUT_PULLUP); // Wejście z pull-up
    
    // Alternatywna składnia dla AVR
    DDRB |= (1 << PB5);      // Pin 13 jako wyjście
    DDRD &= ~(1 << PD2);     // Pin 2 jako wejście
}

void loop() {
    digitalWrite(13, HIGH);   // Ustaw pin 13 na HIGH
    delay(500);
    digitalWrite(13, LOW);    // Ustaw pin 13 na LOW
    delay(500);
    
    int buttonState = digitalRead(2); // Odczytaj pin 2
    if (buttonState == HIGH) {
        // Przycisk wciśnięty
    }
}
```

#### STM32 HAL
```c
GPIO_InitTypeDef GPIO_InitStruct = {0};

// Konfiguracja wyjścia
GPIO_InitStruct.Pin = GPIO_PIN_5;
GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;  // Push-pull
GPIO_InitStruct.Pull = GPIO_NOPULL;
GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

// Konfiguracja wejścia
GPIO_InitStruct.Pin = GPIO_PIN_0;
GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
GPIO_InitStruct.Pull = GPIO_PULLUP;
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

// Użycie
HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
GPIO_PinState buttonState = HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0);
```

### Rodzaje wyjść cyfrowych

#### Push-Pull Output
```
VCC ─┐
     │ PMOS (ON gdy OUTPUT=0)
     ├─── OUTPUT PIN
     │ NMOS (ON gdy OUTPUT=1) 
GND ─┘
```
- **Zalety**: Silne poziomy HIGH i LOW
- **Zastosowanie**: Standardowe wyjścia cyfrowe

#### Open-Drain/Open-Collector
```
VCC ─── R_pullup ─┐
                  ├─── OUTPUT PIN
                  │
                NMOS (ON gdy OUTPUT=0)
                  │
GND ─────────────┘
```
- **Zalety**: Możliwość łączenia wielu wyjść (Wire-AND)
- **Zastosowanie**: I2C, 1-Wire, sygnały przerwań

### Debouncing przycisków

#### Problem bouncing
```
Idealny:     ┌────────────
             │
─────────────┘

Rzeczywisty: ┌─┐ ┌┐ ┌─────
             │ │ ││ │
─────────────┘ └─┘└─┘
```

#### Software debouncing
```cpp
// Prosty debouncing z opóźnieniem
int lastButtonState = LOW;
int buttonState;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;

void loop() {
    int reading = digitalRead(buttonPin);
    
    if (reading != lastButtonState) {
        lastDebounceTime = millis();
    }
    
    if ((millis() - lastDebounceTime) > debounceDelay) {
        if (reading != buttonState) {
            buttonState = reading;
            
            if (buttonState == HIGH) {
                // Przycisk został wciśnięty
            }
        }
    }
    lastButtonState = reading;
}
```

#### Hardware debouncing
```
Button ─┬─── R ──── VCC
        │
        C
        │
       GND
```
- **RC Filter**: R=10kΩ, C=100nF
- **Schmitt Trigger**: 74HC14, 74HC132

### Multipleksowanie

#### 74HC595 Shift Register (Wyjścia)
```cpp
#include <ShiftOut.h>

const int dataPin = 8;   // DS (Data)
const int clockPin = 12; // SHCP (Shift Register Clock)
const int latchPin = 11; // STCP (Storage Register Clock)

void setup() {
    pinMode(dataPin, OUTPUT);
    pinMode(clockPin, OUTPUT);
    pinMode(latchPin, OUTPUT);
}

void writeShiftRegister(byte data) {
    digitalWrite(latchPin, LOW);
    shiftOut(dataPin, clockPin, MSBFIRST, data);
    digitalWrite(latchPin, HIGH);
}

void loop() {
    // Zapal kolejno LED-y
    for (int i = 0; i < 8; i++) {
        writeShiftRegister(1 << i);
        delay(200);
    }
}
```

#### 74HC165 Shift Register (Wejścia)
```cpp
const int loadPin = 8;    // PL (Parallel Load)
const int clockPin = 12;  // CP (Clock)
const int dataPin = 11;   // Q7 (Serial Data)

byte readShiftRegister() {
    byte result = 0;
    
    // Load parallel data
    digitalWrite(loadPin, LOW);
    delayMicroseconds(5);
    digitalWrite(loadPin, HIGH);
    delayMicroseconds(5);
    
    // Shift in data
    for (int i = 7; i >= 0; i--) {
        digitalWrite(clockPin, HIGH);
        delayMicroseconds(5);
        if (digitalRead(dataPin)) {
            result |= (1 << i);
        }
        digitalWrite(clockPin, LOW);
        delayMicroseconds(5);
    }
    
    return result;
}
```

## Wejścia/wyjścia analogowe

### ADC (Analog-to-Digital Converter)

#### Podstawowe parametry ADC
- **Rozdzielczość**: Liczba bitów (8-bit = 256 poziomów, 10-bit = 1024)
- **Częstotliwość próbkowania**: Maksymalna częstość konwersji
- **Napięcie referencyjne**: Vref określa zakres pomiarowy
- **Dokładność**: INL (Integral Non-Linearity), DNL (Differential Non-Linearity)

#### Arduino ADC
```cpp
void setup() {
    Serial.begin(9600);
    // Domyślnie: 10-bit, Vref = 5V (Uno) lub 3.3V (ESP32)
}

void loop() {
    int rawValue = analogRead(A0);  // 0-1023
    float voltage = rawValue * (5.0 / 1023.0);  // Konwersja na napięcie
    
    Serial.print("Raw: ");
    Serial.print(rawValue);
    Serial.print(" Voltage: ");
    Serial.println(voltage);
    
    delay(500);
}
```

#### Konfiguracja referencji napięcia
```cpp
void setup() {
    // analogReference(DEFAULT);    // 5V na Uno
    // analogReference(INTERNAL);   // 1.1V na Uno
    analogReference(EXTERNAL);   // Zewnętrzne Vref na AREF
}
```

#### AVR ADC (bare metal)
```c
#include <avr/io.h>

void adc_init() {
    // Vref = AVcc, right adjusted, ADC0
    ADMUX = (1 << REFS0);
    
    // Enable ADC, prescaler 128 (125kHz @ 16MHz)
    ADCSRA = (1 << ADEN) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
}

uint16_t adc_read(uint8_t channel) {
    // Select ADC channel
    ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);
    
    // Start conversion
    ADCSRA |= (1 << ADSC);
    
    // Wait for completion
    while (ADCSRA & (1 << ADSC));
    
    return ADC;
}
```

### DAC (Digital-to-Analog Converter)

#### Arduino (brak prawdziwego DAC)
```cpp
// Symulacja DAC przez PWM + filtr RC
void setup() {
    pinMode(9, OUTPUT);  // Pin z PWM
}

void loop() {
    // Generowanie fali sinusoidalnej
    for (int i = 0; i < 360; i += 5) {
        float sinValue = sin(i * PI / 180);
        int pwmValue = (int)(127.5 * sinValue + 127.5);  // 0-255
        analogWrite(9, pwmValue);
        delay(10);
    }
}
```

#### STM32 prawdziwy DAC
```c
// STM32F4 12-bit DAC
void dac_init() {
    __HAL_RCC_DAC_CLK_ENABLE();
    
    DAC_ChannelConfTypeDef sConfig = {0};
    sConfig.DAC_Trigger = DAC_TRIGGER_NONE;
    sConfig.DAC_OutputBuffer = DAC_OUTPUTBUFFER_ENABLE;
    
    HAL_DAC_ConfigChannel(&hdac, &sConfig, DAC_CHANNEL_1);
    HAL_DAC_Start(&hdac, DAC_CHANNEL_1);
}

void dac_write(uint16_t value) {
    HAL_DAC_SetValue(&hdac, DAC_CHANNEL_1, DAC_ALIGN_12B_R, value);
}
```

### PWM - modulacja szerokości impulsu

#### Podstawy PWM
```
Duty Cycle 25%:  ┌─┐   ┌─┐   ┌─┐
                 │ │   │ │   │ │
               ──┘ └───┘ └───┘ └───

Duty Cycle 75%:  ┌───┐ ┌───┐ ┌───┐
                 │   │ │   │ │   │
               ──┘   └─┘   └─┘   └─

Częstotliwość = 1 / Okres
Duty Cycle = (Ton / T) * 100%
```

#### Arduino PWM
```cpp
void setup() {
    pinMode(9, OUTPUT);  // Pin z obsługą PWM
}

void loop() {
    // Regulacja jasności LED
    for (int brightness = 0; brightness <= 255; brightness++) {
        analogWrite(9, brightness);
        delay(10);
    }
    
    for (int brightness = 255; brightness >= 0; brightness--) {
        analogWrite(9, brightness);
        delay(10);
    }
}
```

#### Konfiguracja częstotliwości PWM (AVR)
```c
// Timer2 Fast PWM, 62.5kHz
void setup_high_freq_pwm() {
    TCCR2A = (1 << COM2A1) | (1 << WGM21) | (1 << WGM20); // Fast PWM
    TCCR2B = (1 << CS20);  // No prescaler
    OCR2A = 128;  // 50% duty cycle
}

// Timer1 dla precyzyjnego PWM
void setup_precise_pwm() {
    TCCR1A = (1 << COM1A1) | (1 << WGM11); // Fast PWM, TOP=ICR1
    TCCR1B = (1 << WGM13) | (1 << WGM12) | (1 << CS10); // No prescaler
    ICR1 = 999;    // Częstotliwość = 16MHz / (999+1) = 16kHz
    OCR1A = 500;   // 50% duty cycle
}
```

### Filtrowanie sygnałów analogowych

#### Filtr RC (Low-pass)
```
Input ─── R ─── Output
              │
              C
              │
             GND

fc = 1 / (2π * R * C)  [Hz]
```

#### Filtr cyfrowy (Moving Average)
```cpp
const int SAMPLES = 10;
int readings[SAMPLES];
int index = 0;
int total = 0;

int smoothAnalogRead(int pin) {
    // Usuń starą wartość
    total -= readings[index];
    
    // Dodaj nową wartość
    readings[index] = analogRead(pin);
    total += readings[index];
    
    // Przejdź do następnej pozycji
    index = (index + 1) % SAMPLES;
    
    return total / SAMPLES;
}
```

#### Filtr Kalmana (uproszczony)
```cpp
class SimpleKalmanFilter {
private:
    float Q; // Process noise covariance
    float R; // Measurement noise covariance
    float P; // Estimation error covariance
    float K; // Kalman gain
    float X; // State estimate
    
public:
    SimpleKalmanFilter(float q, float r, float p, float initial_value) {
        Q = q; R = r; P = p; X = initial_value;
    }
    
    float update(float measurement) {
        // Prediction
        P = P + Q;
        
        // Update
        K = P / (P + R);
        X = X + K * (measurement - X);
        P = (1 - K) * P;
        
        return X;
    }
};

SimpleKalmanFilter filter(0.01, 0.1, 1, 0);

void loop() {
    int rawValue = analogRead(A0);
    float filteredValue = filter.update(rawValue);
    
    Serial.print("Raw: ");
    Serial.print(rawValue);
    Serial.print(" Filtered: ");
    Serial.println(filteredValue);
    
    delay(100);
}
```

## Zaawansowane techniki

### Interrupt-driven ADC
```cpp
volatile bool adcComplete = false;
volatile int adcResult;

ISR(ADC_vect) {
    adcResult = ADC;
    adcComplete = true;
}

void setup() {
    // Konfiguracja ADC z przerwaniami
    ADMUX = (1 << REFS0);  // AVcc reference
    ADCSRA = (1 << ADEN) | (1 << ADIE) | (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);
    sei();  // Enable interrupts
}

void startConversion(uint8_t channel) {
    ADMUX = (ADMUX & 0xF0) | (channel & 0x0F);
    ADCSRA |= (1 << ADSC);  // Start conversion
}

void loop() {
    if (!adcComplete) {
        startConversion(0);
    }
    
    if (adcComplete) {
        Serial.println(adcResult);
        adcComplete = false;
    }
}
```

### DMA ADC (STM32)
```c
uint16_t adc_buffer[100];  // Bufor dla 100 próbek

void adc_dma_init() {
    // Konfiguracja ADC w trybie ciągłym z DMA
    hadc1.Init.ScanConvMode = DISABLE;
    hadc1.Init.ContinuousConvMode = ENABLE;
    hadc1.Init.DMAContinuousRequests = ENABLE;
    
    HAL_ADC_Init(&hadc1);
    HAL_ADC_Start_DMA(&hadc1, (uint32_t*)adc_buffer, 100);
}

void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    // Callback po zakończeniu 100 konwersji
    // Przetwarzanie danych w adc_buffer
}
```

### Oversampling i decimation
```cpp
// Zwiększenie efektywnej rozdzielczości ADC
uint16_t oversampleADC(int pin, int samples) {
    uint32_t sum = 0;
    
    for (int i = 0; i < samples; i++) {
        sum += analogRead(pin);
    }
    
    // Dla n próbek, zyskujemy log2(n)/2 dodatkowych bitów
    // np. 16 próbek = 2 dodatkowe bity (12-bit zamiast 10-bit)
    return sum >> 2;  // Dzielenie przez 4 (16 próbek)
}
```

## Pomiar sygnałów specjalnych

### Pomiar częstotliwości
```cpp
volatile unsigned long pulseCount = 0;

void setup() {
    attachInterrupt(digitalPinToInterrupt(2), countPulse, RISING);
}

void countPulse() {
    pulseCount++;
}

float measureFrequency() {
    pulseCount = 0;
    delay(1000);  // Pomiar przez 1 sekundę
    return pulseCount;  // Hz
}
```

### Pomiar duty cycle
```cpp
unsigned long measureDutyCycle(int pin) {
    unsigned long highTime = pulseIn(pin, HIGH);
    unsigned long lowTime = pulseIn(pin, LOW);
    
    if (highTime == 0 || lowTime == 0) {
        return 0;  // Błąd pomiaru
    }
    
    return (highTime * 100) / (highTime + lowTime);  // Procenty
}
```

## Kalibracja i kompensacja

### Kalibracja ADC
```cpp
// Przechowywanie wartości kalibracyjnych w EEPROM
#include <EEPROM.h>

struct CalibrationData {
    float offset;
    float scale;
};

void calibrateADC() {
    CalibrationData cal;
    
    Serial.println("Kalibracja: podłącz 0V do A0");
    delay(5000);
    int zero = analogRead(A0);
    
    Serial.println("Kalibracja: podłącz znaną wartość do A0");
    delay(5000);
    int reference = analogRead(A0);
    float referenceVoltage = 3.3;  // Znana wartość
    
    cal.offset = zero;
    cal.scale = referenceVoltage / (reference - zero);
    
    EEPROM.put(0, cal);
}

float calibratedRead(int pin) {
    CalibrationData cal;
    EEPROM.get(0, cal);
    
    int raw = analogRead(pin);
    return (raw - cal.offset) * cal.scale;
}
```

## Powiązane tematy
- [[arduino_podstawy|Arduino - Podstawy]]
- [[mikrokontrolery_vs_mikroprocesory|Mikrokontrolery vs Mikroprocesory]]
- [[protokoly_komunikacyjne|Protokoły Komunikacyjne]]
- [[sensory_i_aktuatory|Sensory i Aktuatory]]
- [[interfejsy_sprzętowe|Interfejsy Sprzętowe]]
- [[signal_processing|Przetwarzanie Sygnałów w Embedded]]