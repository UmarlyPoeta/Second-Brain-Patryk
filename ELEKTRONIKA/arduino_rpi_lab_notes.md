# Systemy Wbudowane - Arduino i Raspberry Pi - Notatki Laboratoryjne

## Spis treści
1. [[#Arduino podstawy]]
2. [[#Raspberry Pi]]
3. [[#Mikrokontrolery i mikroprocesory]]
4. [[#Wejścia/wyjścia cyfrowe i analogowe]]
5. [[#Protokoły komunikacyjne]]
6. [[#Sensory i aktuatory]]
7. [[#Zarządzanie zasilaniem]]
8. [[#Koncepcje systemów czasu rzeczywistego]]
9. [[#Programowanie embedded]]
10. [[#Interfejsy sprzętowe]]
11. [[#Przykłady projektów i ćwiczenia laboratoryjne]]

---

## Arduino podstawy

### Hardware Arduino
- **Mikrokontroler**: Zazwyczaj ATmega328P (Arduino Uno), ATmega2560 (Arduino Mega)
- **Architektura**: 8-bitowa architektura Harvard
- **Taktowanie**: 16 MHz (większość modeli)
- **Pamięć**: 
  - Flash: 32KB (Uno), 256KB (Mega)
  - SRAM: 2KB (Uno), 8KB (Mega)
  - EEPROM: 1KB (Uno), 4KB (Mega)

### Popularne modele Arduino
- **Arduino Uno**: Podstawowy model, idealny do nauki
- **Arduino Nano**: Kompaktowa wersja Uno
- **Arduino Mega**: Więcej pinów I/O, większa pamięć
- **Arduino Leonardo**: Wbudowana obsługa USB HID
- **Arduino Pro Mini**: Bardzo mały, bez złączy USB

### Arduino IDE
- **Instalacja**: Download z arduino.cc
- **Struktura programu**:
```cpp
void setup() {
  // Kod wykonywany raz przy starcie
}

void loop() {
  // Kod wykonywany w pętli
}
```

### Podstawowe funkcje programowania Arduino
```cpp
// Konfiguracja pinów
pinMode(pin, INPUT/OUTPUT/INPUT_PULLUP);

// Operacje cyfrowe
digitalWrite(pin, HIGH/LOW);
int value = digitalRead(pin);

// Operacje analogowe
analogWrite(pin, value); // PWM 0-255
int value = analogRead(pin); // ADC 0-1023

// Opóźnienia
delay(ms);
delayMicroseconds(us);

// Komunikacja szeregowa
Serial.begin(9600);
Serial.print("tekst");
Serial.println("tekst z nową linią");
```

### Przykładowy kod - migająca dioda LED
```cpp
void setup() {
  pinMode(13, OUTPUT); // Pin 13 jako wyjście
}

void loop() {
  digitalWrite(13, HIGH); // Włącz LED
  delay(1000);            // Czekaj 1 sekundę
  digitalWrite(13, LOW);  // Wyłącz LED
  delay(1000);            // Czekaj 1 sekundę
}
```

---

## Raspberry Pi

### Hardware Raspberry Pi
- **Procesor**: ARM Cortex (różne modele)
- **Architektura**: 32-bit lub 64-bit ARM
- **RAM**: 512MB - 8GB (zależnie od modelu)
- **GPIO**: 40 pinów (modele 2B+, 3, 4)
- **Interfejsy**: USB, Ethernet, WiFi, Bluetooth, HDMI

### Modele Raspberry Pi
- **Pi Zero**: Najmniejszy, najtańszy
- **Pi 4B**: Najnowszy, najpotężniejszy
- **Pi 3B+**: Popularny wybór do projektów
- **Pi Compute Module**: Do zastosowań przemysłowych

### System operacyjny
- **Raspberry Pi OS**: Główny system (bazuje na Debian)
- **Ubuntu**: Alternatywa z lepszym wsparciem
- **Instalacja**: Raspberry Pi Imager

### GPIO (General Purpose Input/Output)
```python
import RPi.GPIO as GPIO
import time

# Konfiguracja
GPIO.setmode(GPIO.BCM)  # Numeracja BCM
GPIO.setup(18, GPIO.OUT)  # Pin 18 jako wyjście

# Migająca LED
try:
    while True:
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        time.sleep(1)
finally:
    GPIO.cleanup()  # Zawsze czyść GPIO
```

### Programowanie w Python
```python
# Odczyt cyfrowy
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
value = GPIO.input(pin)

# PWM
pwm = GPIO.PWM(pin, 1000)  # 1000 Hz
pwm.start(0)  # 0% duty cycle
pwm.ChangeDutyCycle(50)  # 50% duty cycle
```

---

## Mikrokontrolery i mikroprocesory

### Różnice podstawowe
| Cecha | Mikrokontroler | Mikroprocesor |
|-------|----------------|---------------|
| Pamięć | Wbudowana | Zewnętrzna |
| Koszt | Niski | Wyższy |
| Złożoność | Niska | Wysoka |
| Zastosowanie | Systemy wbudowane | Komputery |

### Architektura mikrokontrolerów
- **Harvard**: Oddzielna pamięć dla programu i danych
- **von Neumann**: Wspólna pamięć dla programu i danych

### Popularne rodziny mikrokontrolerów
- **AVR**: Atmel (Arduino)
- **PIC**: Microchip
- **ARM Cortex-M**: STM32, NXP
- **ESP32/ESP8266**: WiFi wbudowane

### Rejestry i porty
```cpp
// Bezpośrednie programowanie rejestrów (AVR)
DDRB |= (1 << PB5);   // Pin jako wyjście
PORTB |= (1 << PB5);  // Stan wysoki
PORTB &= ~(1 << PB5); // Stan niski
```

---

## Wejścia/wyjścia cyfrowe i analogowe

### Wejścia/wyjścia cyfrowe
- **Stan wysoki (HIGH)**: Zazwyczaj 3.3V lub 5V
- **Stan niski (LOW)**: 0V
- **Tryby**: INPUT, OUTPUT, INPUT_PULLUP

### Debouncing przycisków
```cpp
// Programowy debouncing
bool lastButtonState = LOW;
bool currentButtonState = LOW;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;

void loop() {
  int reading = digitalRead(buttonPin);
  
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != currentButtonState) {
      currentButtonState = reading;
      
      if (currentButtonState == HIGH) {
        // Przycisk został naciśnięty
      }
    }
  }
  
  lastButtonState = reading;
}
```

### Wejścia/wyjścia analogowe
- **ADC** (Analog-to-Digital Converter): Konwersja analog → cyfrowy
- **DAC** (Digital-to-Analog Converter): Konwersja cyfrowy → analog
- **PWM** (Pulse Width Modulation): Symulacja sygnału analogowego

### PWM - modulacja szerokości impulsu
```cpp
// Sterowanie jasnością LED przez PWM
int brightness = 0;
int fadeAmount = 5;

void loop() {
  analogWrite(ledPin, brightness);
  
  brightness = brightness + fadeAmount;
  
  if (brightness <= 0 || brightness >= 255) {
    fadeAmount = -fadeAmount;
  }
  
  delay(30);
}
```

---

## Protokoły komunikacyjne

### UART (Universal Asynchronous Receiver-Transmitter)
- **Asynchroniczny**: Bez sygnału zegara
- **Parametry**: Baud rate, bity danych, bit parzystości, bity stopu
- **Połączenie**: TX → RX, RX → TX, GND

```cpp
// Arduino UART
Serial.begin(9600);
Serial.print("Hello World");

// Odczyt danych
if (Serial.available()) {
  String data = Serial.readString();
}
```

### SPI (Serial Peripheral Interface)
- **Synchroniczny**: Wspólny sygnał zegara (SCK)
- **Master-Slave**: Jeden master, wiele slave'ów
- **Linie**: MOSI, MISO, SCK, SS/CS

```cpp
#include <SPI.h>

void setup() {
  SPI.begin();
  pinMode(SS, OUTPUT);
  digitalWrite(SS, HIGH);
}

void sendSPI(byte data) {
  digitalWrite(SS, LOW);   // Wybierz slave
  SPI.transfer(data);      // Prześlij dane
  digitalWrite(SS, HIGH);  // Zwolnij slave
}
```

### I2C (Inter-Integrated Circuit)
- **Dwuprzewodowy**: SDA (dane), SCL (zegar)
- **Adresowanie**: 7-bitowe lub 10-bitowe adresy
- **Multi-master**: Możliwość wielu masterów

```cpp
#include <Wire.h>

void setup() {
  Wire.begin(); // Jako master
  // Wire.begin(8); // Jako slave z adresem 8
}

void writeI2C(int address, byte data) {
  Wire.beginTransmission(address);
  Wire.write(data);
  Wire.endTransmission();
}

byte readI2C(int address) {
  Wire.requestFrom(address, 1);
  if (Wire.available()) {
    return Wire.read();
  }
  return 0;
}
```

---

## Sensory i aktuatory

### Popularne sensory
#### Sensor temperatury (DS18B20)
```cpp
#include <OneWire.h>
#include <DallasTemperature.h>

OneWire oneWire(2);
DallasTemperature sensors(&oneWire);

void setup() {
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();
  float temp = sensors.getTempCByIndex(0);
  Serial.println(temp);
  delay(1000);
}
```

#### Sensor odległości (HC-SR04)
```cpp
int trigPin = 9;
int echoPin = 10;

long readDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  long distance = duration * 0.034 / 2;
  
  return distance;
}
```

### Aktuatory
#### Servo motor
```cpp
#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9);
}

void loop() {
  for (int pos = 0; pos <= 180; pos++) {
    myServo.write(pos);
    delay(15);
  }
  for (int pos = 180; pos >= 0; pos--) {
    myServo.write(pos);
    delay(15);
  }
}
```

#### Silnik krokowy
```cpp
#include <Stepper.h>

const int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

void setup() {
  myStepper.setSpeed(60); // RPM
}

void loop() {
  myStepper.step(stepsPerRevolution);  // Obrót w prawo
  delay(500);
  myStepper.step(-stepsPerRevolution); // Obrót w lewo
  delay(500);
}
```

---

## Zarządzanie zasilaniem

### Tryby oszczędzania energii
#### Arduino - Sleep Mode
```cpp
#include <avr/sleep.h>
#include <avr/power.h>

void setup() {
  // Konfiguracja
}

void goToSleep() {
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  
  // Wyłącz niepotrzebne peryferia
  power_adc_disable();
  power_spi_disable();
  power_timer0_disable();
  power_timer1_disable();
  power_timer2_disable();
  power_twi_disable();
  
  sleep_mode(); // Przejdź w tryb uśpienia
  
  // Po przebudzeniu
  sleep_disable();
  power_all_enable();
}
```

### Pomiar poboru prądu
- **Multimetr w trybie amperomierza**
- **Moduły pomiarowe**: INA219, INA226
- **Oszyloskop** dla dynamicznych pomiarów

### Optymalizacja poboru energii
1. **Wyłączanie nieużywanych peryferiów**
2. **Obniżenie częstotliwości zegara**
3. **Używanie przerwań zamiast polling**
4. **Efektywne algorytmy**

---

## Koncepcje systemów czasu rzeczywistego

### Definicje
- **Hard Real-Time**: Przekroczenie terminu = katastrofa
- **Soft Real-Time**: Przekroczenie terminu = obniżenie jakości
- **Deterministyczność**: Przewidywalny czas wykonania

### RTOS (Real-Time Operating System)
#### FreeRTOS na ESP32
```cpp
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void task1(void *parameter) {
  while(1) {
    // Zadanie 1
    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void task2(void *parameter) {
  while(1) {
    // Zadanie 2
    vTaskDelay(pdMS_TO_TICKS(200));
  }
}

void setup() {
  xTaskCreate(task1, "Task1", 2048, NULL, 1, NULL);
  xTaskCreate(task2, "Task2", 2048, NULL, 1, NULL);
}

void loop() {
  // Puste - zadania działają w tle
}
```

### Przerwania (Interrupts)
```cpp
volatile bool buttonPressed = false;

void setup() {
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), buttonISR, FALLING);
}

void buttonISR() {
  buttonPressed = true; // Krótka procedura obsługi
}

void loop() {
  if (buttonPressed) {
    buttonPressed = false;
    // Obsługa naciśnięcia przycisku
  }
}
```

---

## Programowanie embedded

### Dobre praktyki
1. **Unikaj dynamicznej alokacji pamięci**
2. **Używaj const dla stałych**
3. **Optymalizuj rozmiar kodu**
4. **Testuj granice**

### Debugowanie
#### Serial Monitor
```cpp
#define DEBUG 1

#if DEBUG
  #define DEBUG_PRINT(x) Serial.print(x)
  #define DEBUG_PRINTLN(x) Serial.println(x)
#else
  #define DEBUG_PRINT(x)
  #define DEBUG_PRINTLN(x)
#endif
```

#### Obsługa błędów
```cpp
enum ErrorCode {
  NO_ERROR = 0,
  SENSOR_ERROR = 1,
  COMMUNICATION_ERROR = 2,
  MEMORY_ERROR = 3
};

ErrorCode initSensor() {
  if (!sensor.begin()) {
    return SENSOR_ERROR;
  }
  return NO_ERROR;
}
```

### Maszyny stanów
```cpp
enum State {
  IDLE,
  READING,
  PROCESSING,
  SENDING
};

State currentState = IDLE;

void stateMachine() {
  switch (currentState) {
    case IDLE:
      if (shouldStartReading()) {
        currentState = READING;
      }
      break;
      
    case READING:
      if (readingComplete()) {
        currentState = PROCESSING;
      }
      break;
      
    case PROCESSING:
      processData();
      currentState = SENDING;
      break;
      
    case SENDING:
      if (sendComplete()) {
        currentState = IDLE;
      }
      break;
  }
}
```

---

## Interfejsy sprzętowe

### Poziomy napięć
- **5V TTL**: Arduino Uno, klasyczne układy
- **3.3V CMOS**: ESP32, Raspberry Pi, nowoczesne układy
- **Konwertory poziomów**: Gdy trzeba łączyć różne napięcia

### Pull-up i Pull-down
```cpp
// Pull-up wewnętrzny
pinMode(pin, INPUT_PULLUP);

// Pull-up zewnętrzny - rezystor 10kΩ
// Pin → Rezystor → VCC
```

### Multipleksery
```cpp
// Multiplekser 74HC4051 (8:1)
int controlPins[] = {7, 8, 9}; // S0, S1, S2
int signalPin = A0;

int readMux(int channel) {
  // Ustaw adres kanału
  for (int i = 0; i < 3; i++) {
    digitalWrite(controlPins[i], (channel >> i) & 1);
  }
  
  delay(1); // Czas stabilizacji
  return analogRead(signalPin);
}
```

### Shift Register
```cpp
// 74HC595 - Serial to Parallel
int dataPin = 11;   // DS
int clockPin = 12;  // SHCP
int latchPin = 13;  // STCP

void shiftWrite(byte data) {
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, data);
  digitalWrite(latchPin, HIGH);
}
```

---

## Przykłady projektów i ćwiczenia laboratoryjne

### Projekt 1: Stacja pogodowa
```cpp
#include <DHT.h>
#include <LiquidCrystal.h>

DHT dht(2, DHT22);
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  dht.begin();
  lcd.begin(16, 2);
}

void loop() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temp);
  lcd.print("C");
  
  lcd.setCursor(0, 1);
  lcd.print("Wilg: ");
  lcd.print(humidity);
  lcd.print("%");
  
  delay(2000);
}
```

### Projekt 2: System alarmowy
```cpp
#include <Keypad.h>

const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

byte rowPins[ROWS] = {9, 8, 7, 6};
byte colPins[COLS] = {5, 4, 3, 2};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

String correctCode = "1234";
String enteredCode = "";
bool armed = false;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT); // LED alarmu
  pinMode(12, INPUT_PULLUP); // Sensor ruchu
}

void loop() {
  char key = keypad.getKey();
  
  if (key) {
    if (key == '#') {
      checkCode();
    } else if (key == '*') {
      enteredCode = "";
    } else {
      enteredCode += key;
    }
  }
  
  if (armed && digitalRead(12) == LOW) {
    triggerAlarm();
  }
}

void checkCode() {
  if (enteredCode == correctCode) {
    armed = !armed;
    Serial.println(armed ? "UZBROJONY" : "ROZBROJONNY");
  } else {
    Serial.println("ZLY KOD");
  }
  enteredCode = "";
}

void triggerAlarm() {
  digitalWrite(13, HIGH);
  Serial.println("ALARM!");
  delay(100);
  digitalWrite(13, LOW);
  delay(100);
}
```

### Projekt 3: Robot unikający przeszkód
```cpp
#include <Servo.h>

Servo servo;
int trigPin = 9;
int echoPin = 10;
int leftMotor1 = 3;
int leftMotor2 = 4;
int rightMotor1 = 5;
int rightMotor2 = 6;

void setup() {
  servo.attach(7);
  servo.write(90); // Pozycja środkowa
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(leftMotor1, OUTPUT);
  pinMode(leftMotor2, OUTPUT);
  pinMode(rightMotor1, OUTPUT);
  pinMode(rightMotor2, OUTPUT);
}

void loop() {
  int distance = getDistance();
  
  if (distance > 20) {
    moveForward();
  } else {
    stopMotors();
    
    // Sprawdź lewo
    servo.write(180);
    delay(500);
    int leftDistance = getDistance();
    
    // Sprawdź prawo  
    servo.write(0);
    delay(500);
    int rightDistance = getDistance();
    
    // Wróć do środka
    servo.write(90);
    delay(500);
    
    if (leftDistance > rightDistance) {
      turnLeft();
    } else {
      turnRight();
    }
    delay(500);
  }
}

int getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;
}

void moveForward() {
  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);
  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);
}

void turnLeft() {
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, HIGH);
  digitalWrite(rightMotor1, HIGH);
  digitalWrite(rightMotor2, LOW);
}

void turnRight() {
  digitalWrite(leftMotor1, HIGH);
  digitalWrite(leftMotor2, LOW);
  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, HIGH);
}

void stopMotors() {
  digitalWrite(leftMotor1, LOW);
  digitalWrite(leftMotor2, LOW);
  digitalWrite(rightMotor1, LOW);
  digitalWrite(rightMotor2, LOW);
}
```

### Ćwiczenia laboratoryjne

#### Ćwiczenie 1: Migająca LED z przyciskiem
**Cel**: Poznanie podstaw I/O cyfrowego
**Zadanie**: LED miga tylko gdy przycisk jest naciśnięty

#### Ćwiczenie 2: Pomiar temperatury
**Cel**: Praca z sensorami analogowymi  
**Zadanie**: Odczyt temperatury i wyświetlanie na Serial Monitor

#### Ćwiczenie 3: Komunikacja I2C
**Cel**: Nauka protokołów komunikacyjnych
**Zadanie**: Połączenie dwóch Arduino przez I2C

#### Ćwiczenie 4: System przerwań
**Cel**: Zrozumienie przerwań
**Zadanie**: Licznik impulsów z przerwaniami zewnętrznymi

#### Ćwiczenie 5: PWM i serwa
**Cel**: Sterowanie silnikami
**Zadanie**: Kontrola pozycji serwa potencjometrem

### Narzędzia pomiarowe
- **Multimetr**: Pomiar napięć, prądów, rezystancji
- **Oscyloskop**: Analiza sygnałów cyfrowych i analogowych  
- **Analizator protokołów**: Dekodowanie I2C, SPI, UART
- **Generator funkcyjny**: Generowanie sygnałów testowych

### Dokumentacja projektów
1. **Schemat elektryczny**
2. **Lista elementów (BOM)**
3. **Kod źródłowy z komentarzami**
4. **Instrukcja montażu**
5. **Testy i weryfikacja**

---

## Przydatne zasoby
- [Arduino Reference](https://www.arduino.cc/reference/)
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)
- [Datasheet Central](https://www.datasheetcatalog.org/)
- [Electronics Tutorials](https://www.electronics-tutorials.ws/)

**Tags**: #arduino #raspberrypi #embedded #mikrokontrolery #IoT #elektronika #programowanie