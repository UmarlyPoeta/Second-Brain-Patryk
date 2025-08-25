# Projekty i Ćwiczenia Laboratoryjne

## 🚀 Projekt 1: Stacja Pogodowa IoT

### Opis projektu
Kompletna stacja pogodowa z wyświetlaczem LCD, sensorem temperatury/wilgotności, czujnikiem ciśnienia oraz połączeniem WiFi do przesyłania danych do chmury.

### Komponenty
- ESP32 DevKit
- DHT22 (temperatura/wilgotność)
- BMP280 (ciśnienie/wysokość)
- LCD 16x2 z konwerterem I2C
- Fotoresystor (poziom światła)
- LED status (RGB)
- Przycisk konfiguracyjny

### Schemat połączeń
```
ESP32          | DHT22
GPIO21 (SDA)   | -
GPIO22 (SCL)   | -  
GPIO4          | Data
3.3V           | VCC
GND            | GND

ESP32          | LCD 16x2 (I2C)
GPIO21 (SDA)   | SDA
GPIO22 (SCL)   | SCL
5V             | VCC
GND            | GND

ESP32          | RGB LED
GPIO25         | Red
GPIO26         | Green
GPIO27         | Blue
GND            | Common Cathode
```

### Kod główny
```cpp
#include <WiFi.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <LiquidCrystal_I2C.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Pin definitions
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define BUTTON_PIN 0
#define LED_RED_PIN 25
#define LED_GREEN_PIN 26
#define LED_BLUE_PIN 27
#define LDR_PIN A0

// Objects
DHT dht(DHT_PIN, DHT_TYPE);
Adafruit_BMP280 bmp;
LiquidCrystal_I2C lcd(0x27, 16, 2);
WiFiClient espClient;
PubSubClient mqtt(espClient);

// Configuration
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "broker.mqtt.org";
const char* device_id = "weather_station_01";

struct SensorData {
    float temperature;
    float humidity;
    float pressure;
    float altitude;
    int lightLevel;
    uint32_t timestamp;
};

SensorData currentData;
unsigned long lastReading = 0;
unsigned long lastMQTT = 0;
const unsigned long READING_INTERVAL = 2000;
const unsigned long MQTT_INTERVAL = 30000;

void setup() {
    Serial.begin(115200);
    
    // Initialize peripherals
    pinMode(LED_RED_PIN, OUTPUT);
    pinMode(LED_GREEN_PIN, OUTPUT);
    pinMode(LED_BLUE_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    
    dht.begin();
    Wire.begin();
    lcd.init();
    lcd.backlight();
    
    // Initialize sensors
    if (!bmp.begin()) {
        Serial.println("BMP280 sensor not found!");
        setLED(255, 0, 0);  // Red error
        while (1);
    }
    
    // Configure BMP280
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                   Adafruit_BMP280::SAMPLING_X2,
                   Adafruit_BMP280::SAMPLING_X16,
                   Adafruit_BMP280::FILTER_X16,
                   Adafruit_BMP280::STANDBY_MS_500);
    
    lcd.setCursor(0, 0);
    lcd.print("Weather Station");
    lcd.setCursor(0, 1);
    lcd.print("Starting...");
    
    // Connect to WiFi
    connectWiFi();
    mqtt.setServer(mqtt_server, 1883);
    
    setLED(0, 255, 0);  // Green - ready
    delay(1000);
    setLED(0, 0, 0);    // Turn off
}

void loop() {
    unsigned long currentTime = millis();
    
    // Read sensors
    if (currentTime - lastReading >= READING_INTERVAL) {
        readSensors();
        updateDisplay();
        lastReading = currentTime;
    }
    
    // Send MQTT data
    if (currentTime - lastMQTT >= MQTT_INTERVAL) {
        if (!mqtt.connected()) {
            reconnectMQTT();
        }
        publishData();
        lastMQTT = currentTime;
    }
    
    mqtt.loop();
    
    // Handle button press
    if (digitalRead(BUTTON_PIN) == LOW) {
        handleButtonPress();
        delay(200);  // Debounce
    }
}

void readSensors() {
    currentData.temperature = dht.readTemperature();
    currentData.humidity = dht.readHumidity();
    currentData.pressure = bmp.readPressure() / 100.0F;  // hPa
    currentData.altitude = bmp.readAltitude(1013.25);
    currentData.lightLevel = analogRead(LDR_PIN);
    currentData.timestamp = millis();
    
    // Validate readings
    if (isnan(currentData.temperature) || isnan(currentData.humidity)) {
        Serial.println("DHT22 reading failed!");
        setLED(255, 100, 0);  // Orange warning
    } else {
        setLED(0, 0, 255);    // Blue - data OK
        delay(100);
        setLED(0, 0, 0);
    }
}

void updateDisplay() {
    lcd.clear();
    
    // Line 1: Temperature and Humidity
    lcd.setCursor(0, 0);
    lcd.printf("T:%.1fC H:%.0f%%", currentData.temperature, currentData.humidity);
    
    // Line 2: Pressure and Light
    lcd.setCursor(0, 1);
    lcd.printf("P:%.0f L:%d", currentData.pressure, currentData.lightLevel);
}

void publishData() {
    if (!mqtt.connected()) return;
    
    StaticJsonDocument<200> doc;
    doc["device_id"] = device_id;
    doc["timestamp"] = currentData.timestamp;
    doc["temperature"] = currentData.temperature;
    doc["humidity"] = currentData.humidity;
    doc["pressure"] = currentData.pressure;
    doc["altitude"] = currentData.altitude;
    doc["light_level"] = currentData.lightLevel;
    
    char buffer[256];
    serializeJson(doc, buffer);
    
    String topic = String("weather/") + device_id + "/data";
    mqtt.publish(topic.c_str(), buffer);
    
    Serial.println("Data published to MQTT");
}

void connectWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        setLED(0, 0, 255);  // Blue blink
        delay(100);
        setLED(0, 0, 0);
    }
    
    Serial.println();
    Serial.print("Connected! IP: ");
    Serial.println(WiFi.localIP());
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("WiFi Connected");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());
    delay(2000);
}

void reconnectMQTT() {
    while (!mqtt.connected()) {
        Serial.print("Connecting to MQTT...");
        
        if (mqtt.connect(device_id)) {
            Serial.println("connected");
            String topic = String("weather/") + device_id + "/status";
            mqtt.publish(topic.c_str(), "online");
        } else {
            Serial.print("failed, rc=");
            Serial.print(mqtt.state());
            Serial.println(" retrying in 5 seconds");
            delay(5000);
        }
    }
}

void handleButtonPress() {
    static int displayMode = 0;
    displayMode = (displayMode + 1) % 3;
    
    lcd.clear();
    switch (displayMode) {
        case 0:  // Standard display
            updateDisplay();
            break;
            
        case 1:  // Network info
            lcd.setCursor(0, 0);
            lcd.print("WiFi: Connected");
            lcd.setCursor(0, 1);
            lcd.print(WiFi.localIP());
            break;
            
        case 2:  // System info
            lcd.setCursor(0, 0);
            lcd.printf("Up: %lus", millis() / 1000);
            lcd.setCursor(0, 1);
            lcd.printf("Free: %dB", ESP.getFreeHeap());
            break;
    }
}

void setLED(int red, int green, int blue) {
    analogWrite(LED_RED_PIN, red);
    analogWrite(LED_GREEN_PIN, green);
    analogWrite(LED_BLUE_PIN, blue);
}
```

### Rozszerzenia projektu
1. **Web dashboard** - serwer HTTP z interfejsem użytkownika
2. **SD card logging** - zapis danych lokalnie
3. **Battery monitoring** - pomiar napięcia baterii
4. **Sleep mode** - oszczędzanie energii
5. **Calibration** - kalibracja sensorów

---

## 🚗 Projekt 2: Robot unikający przeszkód

### Opis projektu
Autonomiczny robot na podwoziu kołowym z sensorami odległości, który porusza się i omija przeszkody.

### Komponenty
- Arduino Uno
- Chassis robotyczne z silnikami DC
- HC-SR04 (ultrasonic sensor)
- L298N motor driver
- Servo SG90
- LED strip WS2812B
- Buzzer
- Power bank

### Kod główny
```cpp
#include <Servo.h>
#include <NewPing.h>
#include <Adafruit_NeoPixel.h>

// Pin definitions
#define TRIGGER_PIN 12
#define ECHO_PIN 11
#define SERVO_PIN 10
#define MOTOR_LEFT_A 7
#define MOTOR_LEFT_B 6
#define MOTOR_LEFT_PWM 5
#define MOTOR_RIGHT_A 4
#define MOTOR_RIGHT_B 3
#define MOTOR_RIGHT_PWM 2
#define BUZZER_PIN 8
#define LED_STRIP_PIN 9
#define NUM_LEDS 12

// Constants
#define MAX_DISTANCE 200
#define OBSTACLE_DISTANCE 20
#define TURN_TIME 600
#define SCAN_DELAY 500

// Objects
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);
Servo scanServo;
Adafruit_NeoPixel strip(NUM_LEDS, LED_STRIP_PIN, NEO_GRB + NEO_KHZ800);

// State machine
enum RobotState {
    MOVING_FORWARD,
    SCANNING,
    TURNING_LEFT,
    TURNING_RIGHT,
    BACKING_UP
};

RobotState currentState = MOVING_FORWARD;
unsigned long stateStartTime = 0;
int frontDistance = 0;
int leftDistance = 0;
int rightDistance = 0;

void setup() {
    Serial.begin(9600);
    
    // Initialize pins
    pinMode(MOTOR_LEFT_A, OUTPUT);
    pinMode(MOTOR_LEFT_B, OUTPUT);
    pinMode(MOTOR_LEFT_PWM, OUTPUT);
    pinMode(MOTOR_RIGHT_A, OUTPUT);
    pinMode(MOTOR_RIGHT_B, OUTPUT);
    pinMode(MOTOR_RIGHT_PWM, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    
    // Initialize servo and LED strip
    scanServo.attach(SERVO_PIN);
    scanServo.write(90);  // Center position
    
    strip.begin();
    strip.show();
    strip.setBrightness(50);
    
    // Startup sequence
    playStartupSound();
    animateStartupLEDs();
    
    Serial.println("Robot initialized and ready!");
    delay(1000);
}

void loop() {
    // State machine
    switch (currentState) {
        case MOVING_FORWARD:
            handleMovingForward();
            break;
            
        case SCANNING:
            handleScanning();
            break;
            
        case TURNING_LEFT:
            handleTurning();
            break;
            
        case TURNING_RIGHT:
            handleTurning();
            break;
            
        case BACKING_UP:
            handleBackingUp();
            break;
    }
    
    updateLEDs();
    delay(50);
}

void handleMovingForward() {
    moveForward(180);  // Medium speed
    frontDistance = measureDistance();
    
    if (frontDistance < OBSTACLE_DISTANCE && frontDistance > 0) {
        Serial.println("Obstacle detected! Starting scan...");
        stopMotors();
        changeState(SCANNING);
        playObstacleSound();
    }
}

void handleScanning() {
    if (millis() - stateStartTime < SCAN_DELAY) return;
    
    // Scan left
    scanServo.write(160);
    delay(300);
    leftDistance = measureDistance();
    Serial.print("Left distance: ");
    Serial.println(leftDistance);
    
    // Scan right
    scanServo.write(20);
    delay(300);
    rightDistance = measureDistance();
    Serial.print("Right distance: ");
    Serial.println(rightDistance);
    
    // Return to center
    scanServo.write(90);
    delay(300);
    
    // Decide direction
    if (leftDistance > rightDistance && leftDistance > OBSTACLE_DISTANCE) {
        Serial.println("Turning left");
        changeState(TURNING_LEFT);
    } else if (rightDistance > OBSTACLE_DISTANCE) {
        Serial.println("Turning right");
        changeState(TURNING_RIGHT);
    } else {
        Serial.println("No clear path - backing up");
        changeState(BACKING_UP);
    }
}

void handleTurning() {
    if (currentState == TURNING_LEFT) {
        turnLeft(200);
    } else {
        turnRight(200);
    }
    
    if (millis() - stateStartTime > TURN_TIME) {
        stopMotors();
        changeState(MOVING_FORWARD);
        Serial.println("Turn completed - moving forward");
    }
}

void handleBackingUp() {
    moveBackward(150);
    
    if (millis() - stateStartTime > 1000) {  // Back up for 1 second
        stopMotors();
        changeState(SCANNING);
        Serial.println("Backing completed - scanning again");
    }
}

void changeState(RobotState newState) {
    currentState = newState;
    stateStartTime = millis();
}

int measureDistance() {
    int distance = sonar.ping_cm();
    if (distance == 0) distance = MAX_DISTANCE;  // No echo = max distance
    return distance;
}

// Motor control functions
void moveForward(int speed) {
    digitalWrite(MOTOR_LEFT_A, HIGH);
    digitalWrite(MOTOR_LEFT_B, LOW);
    analogWrite(MOTOR_LEFT_PWM, speed);
    
    digitalWrite(MOTOR_RIGHT_A, HIGH);
    digitalWrite(MOTOR_RIGHT_B, LOW);
    analogWrite(MOTOR_RIGHT_PWM, speed);
}

void moveBackward(int speed) {
    digitalWrite(MOTOR_LEFT_A, LOW);
    digitalWrite(MOTOR_LEFT_B, HIGH);
    analogWrite(MOTOR_LEFT_PWM, speed);
    
    digitalWrite(MOTOR_RIGHT_A, LOW);
    digitalWrite(MOTOR_RIGHT_B, HIGH);
    analogWrite(MOTOR_RIGHT_PWM, speed);
}

void turnLeft(int speed) {
    digitalWrite(MOTOR_LEFT_A, LOW);
    digitalWrite(MOTOR_LEFT_B, HIGH);
    analogWrite(MOTOR_LEFT_PWM, speed);
    
    digitalWrite(MOTOR_RIGHT_A, HIGH);
    digitalWrite(MOTOR_RIGHT_B, LOW);
    analogWrite(MOTOR_RIGHT_PWM, speed);
}

void turnRight(int speed) {
    digitalWrite(MOTOR_LEFT_A, HIGH);
    digitalWrite(MOTOR_LEFT_B, LOW);
    analogWrite(MOTOR_LEFT_PWM, speed);
    
    digitalWrite(MOTOR_RIGHT_A, LOW);
    digitalWrite(MOTOR_RIGHT_B, HIGH);
    analogWrite(MOTOR_RIGHT_PWM, speed);
}

void stopMotors() {
    analogWrite(MOTOR_LEFT_PWM, 0);
    analogWrite(MOTOR_RIGHT_PWM, 0);
}

// LED animations
void updateLEDs() {
    switch (currentState) {
        case MOVING_FORWARD:
            setAllLEDs(0, 255, 0);  // Green - moving
            break;
            
        case SCANNING:
            scanningAnimation();
            break;
            
        case TURNING_LEFT:
            setAllLEDs(0, 0, 255);  // Blue - turning
            break;
            
        case TURNING_RIGHT:
            setAllLEDs(0, 0, 255);  // Blue - turning
            break;
            
        case BACKING_UP:
            setAllLEDs(255, 100, 0); // Orange - backing
            break;
    }
}

void setAllLEDs(int r, int g, int b) {
    for (int i = 0; i < NUM_LEDS; i++) {
        strip.setPixelColor(i, strip.Color(r, g, b));
    }
    strip.show();
}

void scanningAnimation() {
    static int scanPos = 0;
    static unsigned long lastScanUpdate = 0;
    
    if (millis() - lastScanUpdate > 100) {
        strip.clear();
        strip.setPixelColor(scanPos, strip.Color(255, 0, 0));  // Red scanning
        strip.show();
        
        scanPos = (scanPos + 1) % NUM_LEDS;
        lastScanUpdate = millis();
    }
}

void animateStartupLEDs() {
    // Rainbow startup animation
    for (int j = 0; j < 256; j++) {
        for (int i = 0; i < NUM_LEDS; i++) {
            strip.setPixelColor(i, wheel((i * 256 / NUM_LEDS + j) & 255));
        }
        strip.show();
        delay(20);
    }
    strip.clear();
    strip.show();
}

uint32_t wheel(byte wheelPos) {
    wheelPos = 255 - wheelPos;
    if (wheelPos < 85) {
        return strip.Color(255 - wheelPos * 3, 0, wheelPos * 3);
    }
    if (wheelPos < 170) {
        wheelPos -= 85;
        return strip.Color(0, wheelPos * 3, 255 - wheelPos * 3);
    }
    wheelPos -= 170;
    return strip.Color(wheelPos * 3, 255 - wheelPos * 3, 0);
}

// Sound effects
void playStartupSound() {
    int melody[] = {262, 294, 330, 349, 392};
    for (int i = 0; i < 5; i++) {
        tone(BUZZER_PIN, melody[i], 200);
        delay(250);
    }
    noTone(BUZZER_PIN);
}

void playObstacleSound() {
    for (int i = 0; i < 3; i++) {
        tone(BUZZER_PIN, 1000, 100);
        delay(150);
    }
    noTone(BUZZER_PIN);
}
```

---

## 🏠 Projekt 3: System Alarmowy IoT

### Komponenty
- ESP32 DevKit
- PIR sensor (HC-SR501)
- Reed switch (drzwi/okna)
- Buzzer
- OLED display 128x64
- Keypad 4x4
- Relay module

### Funkcje
- Detekcja ruchu i otwarcia drzwi/okien
- Konfiguracja przez keypad i OLED
- Powiadomienia przez WiFi/MQTT
- Aplikacja mobilna (Blynk)
- Harmonogram włączania/wyłączania

---

## 📝 Ćwiczenia Laboratoryjne

### Ćwiczenie 1: Podstawy GPIO
**Cel**: Nauka obsługi pinów cyfrowych I/O

**Zadania**:
1. Migająca LED z regulowaną częstotliwością
2. Przycisk z debouncing
3. Multipleksowanie LED (matrix 4x4)
4. Shift register 74HC595

### Ćwiczenie 2: ADC i DAC
**Cel**: Pomiary analogowe i generowanie sygnałów

**Zadania**:
1. Pomiar napięcia potencjometru
2. Termometr z LM35
3. Regulator jasności LED (PWM)
4. Prostownik sygnału audio

### Ćwiczenie 3: Protokoły komunikacyjne
**Cel**: Komunikacja między urządzeniami

**Zadania**:
1. UART: komunikacja Arduino ↔ PC
2. I2C: obsługa wyświetlacza OLED
3. SPI: komunikacja z modułem SD card
4. 1-Wire: sieć sensorów DS18B20

### Ćwiczenie 4: Sensory i aktuatory
**Cel**: Integracja urządzeń peryferyjnych

**Zadania**:
1. Pomiar odległości (HC-SR04)
2. Detekcja ruchu (PIR)
3. Sterowanie servo (SG90)
4. Sterowanie silnikiem krokowym

### Ćwiczenie 5: Systemy czasu rzeczywistego
**Cel**: Obsługa zadań z ograniczeniami czasowymi

**Zadania**:
1. Timer interrupts
2. Non-blocking delays
3. Simple scheduler
4. Priority handling

---

## 🛠️ Narzędzia pomiarowe

### Multimetr cyfrowy
- **Pomiary**: Napięcie, prąd, opór, ciągłość
- **Zastosowanie**: Weryfikacja połączeń, pomiar parametrów
- **Wskazówki**: Zawsze sprawdź zakres pomiarowy

### Logic Analyzer
- **Funkcja**: Analiza sygnałów cyfrowych
- **Kanały**: 8-16 kanałów jednocześnie
- **Software**: PulseView, Sigrok

### Oscyloskop
- **Funkcja**: Analiza przebiegów czasowych
- **Parametry**: Częstotliwość próbkowania, pasmo
- **Pomiary**: Amplituda, częstotliwość, czas narastania

### Generator funkcyjny
- **Funkcja**: Generowanie sygnałów testowych
- **Przebiegi**: Sinus, prostokąt, trójkąt, szum
- **Parametry**: Amplituda, częstotliwość, offset

---

## 📊 Dokumentacja projektów

### Struktura dokumentacji
1. **Specyfikacja funkcjonalna**
   - Wymagania użytkownika
   - Przypadki użycia
   - Interfejsy

2. **Projekt techniczny**
   - Architektura systemu
   - Schemat blokowy
   - Diagramy przepływu

3. **Implementacja**
   - Kod źródłowy z komentarzami
   - Instrukcje kompilacji
   - Konfiguracja środowiska

4. **Testy i walidacja**
   - Plan testów
   - Wyniki testów
   - Raporty błędów

5. **Instrukcja użytkownika**
   - Instalacja
   - Konfiguracja
   - Obsługa

### Narzędzia dokumentacji
- **Markdown**: README, wiki
- **Fritzing**: Schematy połączeń
- **KiCad**: Profesjonalne PCB
- **Draw.io**: Diagramy blokowe
- **Doxygen**: Dokumentacja kodu

## Powiązane tematy
- [[arduino_podstawy|Arduino - Podstawy]]
- [[raspberry_pi|Raspberry Pi]]
- [[sensory_i_aktuatory|Sensory i Aktuatory]]
- [[protokoly_komunikacyjne|Protokoły Komunikacyjne]]
- [[embedded_programming|Programowanie Embedded]]
- [[testing_embedded|Testowanie Systemów Embedded]]