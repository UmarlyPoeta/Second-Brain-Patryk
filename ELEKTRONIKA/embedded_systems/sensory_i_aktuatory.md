# Sensory i Aktuatory

## Sensory temperatury

### DS18B20 (1-Wire)
- **Zakres**: -55°C do +125°C
- **Rozdzielczość**: 9-12 bitów (0.5°C - 0.0625°C)
- **Interfejs**: 1-Wire digital
- **Zasilanie**: 3.0V - 5.5V lub parasitic power

```cpp
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
    Serial.begin(9600);
    sensors.begin();
    sensors.setResolution(12);  // 12-bit resolution
}

void loop() {
    sensors.requestTemperatures();
    
    float tempC = sensors.getTempCByIndex(0);
    if (tempC != DEVICE_DISCONNECTED_C) {
        Serial.print("Temperatura: ");
        Serial.print(tempC);
        Serial.println("°C");
    }
    delay(1000);
}
```

### DHT22 (AM2302) - Temperatura i Wilgotność
```cpp
#include "DHT.h"

#define DHT_PIN 2
#define DHT_TYPE DHT22

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    Serial.begin(9600);
    dht.begin();
}

void loop() {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    
    if (isnan(humidity) || isnan(temperature)) {
        Serial.println("Błąd odczytu DHT22");
        return;
    }
    
    float heatIndex = dht.computeHeatIndex(temperature, humidity, false);
    
    Serial.print("Wilgotność: ");
    Serial.print(humidity);
    Serial.print("%\t");
    Serial.print("Temperatura: ");
    Serial.print(temperature);
    Serial.print("°C\t");
    Serial.print("Odczucie: ");
    Serial.print(heatIndex);
    Serial.println("°C");
    
    delay(2000);
}
```

### LM35 (Analogowy)
```cpp
const int LM35_PIN = A0;
const float VREF = 5.0;  // Napięcie referencyjne
const int ADC_RESOLUTION = 1024;  // 10-bit ADC

void setup() {
    Serial.begin(9600);
    analogReference(DEFAULT);  // 5V reference
}

void loop() {
    int rawValue = analogRead(LM35_PIN);
    float voltage = (rawValue * VREF) / ADC_RESOLUTION;
    float temperatureC = voltage * 100.0;  // 10mV/°C
    
    Serial.print("ADC: ");
    Serial.print(rawValue);
    Serial.print("\tVoltage: ");
    Serial.print(voltage, 3);
    Serial.print("V\tTemperature: ");
    Serial.print(temperatureC, 1);
    Serial.println("°C");
    
    delay(500);
}
```

### BME280 (I2C) - Temperatura, Wilgotność, Ciśnienie
```cpp
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

Adafruit_BME280 bme;

void setup() {
    Serial.begin(9600);
    
    if (!bme.begin(0x76)) {  // Adres I2C BME280
        Serial.println("BME280 nie znaleziony!");
        while (1);
    }
    
    Serial.println("BME280 test");
}

void loop() {
    Serial.print("Temperature = ");
    Serial.print(bme.readTemperature());
    Serial.println(" °C");
    
    Serial.print("Pressure = ");
    Serial.print(bme.readPressure() / 100.0F);
    Serial.println(" hPa");
    
    Serial.print("Humidity = ");
    Serial.print(bme.readHumidity());
    Serial.println(" %");
    
    Serial.print("Altitude = ");
    Serial.print(bme.readAltitude(1013.25));  // Sea level pressure
    Serial.println(" m");
    
    Serial.println();
    delay(2000);
}
```

## Sensory odległości

### HC-SR04 (Ultrasonic)
- **Zakres**: 2cm - 400cm
- **Rozdzielczość**: 3mm
- **Częstotliwość**: 40kHz
- **Interfejs**: Digital trigger/echo

```cpp
const int TRIG_PIN = 9;
const int ECHO_PIN = 10;
const float SOUND_SPEED = 0.034;  // cm/μs

void setup() {
    Serial.begin(9600);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

float measureDistance() {
    // Wygeneruj impuls trigger (10μs)
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    // Zmierz czas echo
    long duration = pulseIn(ECHO_PIN, HIGH);
    
    // Oblicz odległość (czas/2 * prędkość dźwięku)
    float distance = (duration * SOUND_SPEED) / 2;
    
    return distance;
}

void loop() {
    float distance = measureDistance();
    
    Serial.print("Odległość: ");
    if (distance > 400 || distance < 2) {
        Serial.println("Poza zakresem");
    } else {
        Serial.print(distance);
        Serial.println(" cm");
    }
    
    delay(500);
}
```

### VL53L0X (Laser ToF - Time of Flight)
```cpp
#include "Adafruit_VL53L0X.h"

Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup() {
    Serial.begin(9600);
    
    if (!lox.begin()) {
        Serial.println("VL53L0X nie znaleziony!");
        while(1);
    }
    
    Serial.println("VL53L0X gotowy");
}

void loop() {
    VL53L0X_RangingMeasurementData_t measure;
    
    lox.rangingTest(&measure, false);
    
    if (measure.RangeStatus != 4) {  // Phase failures have status 4
        Serial.print("Odległość (mm): ");
        Serial.println(measure.RangeMilliMeter);
    } else {
        Serial.println("Poza zakresem");
    }
    
    delay(100);
}
```

## Sensory ruchu i orientacji

### MPU6050 (IMU - Accelerometer + Gyroscope)
```cpp
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
    Serial.begin(9600);
    Wire.begin();
    
    if (!mpu.begin()) {
        Serial.println("MPU6050 nie znaleziony!");
        while (1);
    }
    
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    
    Serial.println("MPU6050 gotowy");
}

void loop() {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    
    // Akcelerometr (m/s²)
    Serial.print("Acceleration X: ");
    Serial.print(a.acceleration.x);
    Serial.print(", Y: ");
    Serial.print(a.acceleration.y);
    Serial.print(", Z: ");
    Serial.print(a.acceleration.z);
    Serial.println(" m/s²");
    
    // Żyroskop (rad/s)
    Serial.print("Rotation X: ");
    Serial.print(g.gyro.x);
    Serial.print(", Y: ");
    Serial.print(g.gyro.y);
    Serial.print(", Z: ");
    Serial.print(g.gyro.z);
    Serial.println(" rad/s");
    
    // Temperatura
    Serial.print("Temperature: ");
    Serial.print(temp.temperature);
    Serial.println(" °C");
    
    Serial.println();
    delay(500);
}
```

### HC-SR501 (PIR Motion Detector)
```cpp
const int PIR_PIN = 2;
const int LED_PIN = 13;

volatile bool motionDetected = false;

void setup() {
    Serial.begin(9600);
    pinMode(PIR_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
    
    attachInterrupt(digitalPinToInterrupt(PIR_PIN), motionISR, CHANGE);
    
    Serial.println("PIR sensor ready");
    delay(60000);  // Czas kalibracji PIR (60s)
}

void motionISR() {
    motionDetected = digitalRead(PIR_PIN);
}

void loop() {
    if (motionDetected) {
        Serial.println("Ruch wykryty!");
        digitalWrite(LED_PIN, HIGH);
        delay(5000);  // LED świeci przez 5s
        digitalWrite(LED_PIN, LOW);
        motionDetected = false;
    }
    
    delay(100);
}
```

## Sensory światła

### LDR (Light Dependent Resistor)
```cpp
const int LDR_PIN = A0;
const int LED_PIN = 9;

void setup() {
    Serial.begin(9600);
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    int ldrValue = analogRead(LDR_PIN);
    float lightLevel = (float)ldrValue / 1023.0 * 100.0;  // Procenty
    
    // Automatyczna regulacja jasności LED
    int ledBrightness = map(ldrValue, 0, 1023, 255, 0);  // Odwrócona zależność
    analogWrite(LED_PIN, ledBrightness);
    
    Serial.print("Światło: ");
    Serial.print(lightLevel, 1);
    Serial.print("%\tJasność LED: ");
    Serial.println(ledBrightness);
    
    delay(200);
}
```

### BH1750 (Digital Light Sensor)
```cpp
#include <BH1750.h>
#include <Wire.h>

BH1750 lightMeter;

void setup() {
    Serial.begin(9600);
    Wire.begin();
    
    if (!lightMeter.begin()) {
        Serial.println("BH1750 nie znaleziony!");
        while (1);
    }
    
    Serial.println("BH1750 gotowy");
}

void loop() {
    float lux = lightMeter.readLightLevel();
    
    Serial.print("Światło: ");
    Serial.print(lux);
    Serial.println(" lx");
    
    // Klasyfikacja poziomu światła
    if (lux < 10) {
        Serial.println("Ciemno");
    } else if (lux < 100) {
        Serial.println("Słabe oświetlenie");
    } else if (lux < 1000) {
        Serial.println("Normalne oświetlenie");
    } else {
        Serial.println("Jasne oświetlenie");
    }
    
    delay(1000);
}
```

## Aktuatory - Silniki

### Servo Motor (SG90)
```cpp
#include <Servo.h>

Servo myServo;
const int SERVO_PIN = 9;

void setup() {
    Serial.begin(9600);
    myServo.attach(SERVO_PIN);
    myServo.write(90);  // Pozycja środkowa
    Serial.println("Servo gotowe");
}

void loop() {
    // Pełny obrót tam i z powrotem
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

### Silnik krokowy (28BYJ-48 + ULN2003)
```cpp
#include <Stepper.h>

const int STEPS_PER_REVOLUTION = 2048;  // 28BYJ-48: 64 * 32 = 2048
Stepper myStepper(STEPS_PER_REVOLUTION, 8, 10, 9, 11);

void setup() {
    Serial.begin(9600);
    myStepper.setSpeed(10);  // RPM
    Serial.println("Stepper motor ready");
}

void loop() {
    Serial.println("Obrót w prawo");
    myStepper.step(STEPS_PER_REVOLUTION);
    delay(1000);
    
    Serial.println("Obrót w lewo");
    myStepper.step(-STEPS_PER_REVOLUTION);
    delay(1000);
}
```

### Silnik DC z mostkiem H (L298N)
```cpp
// L298N Motor Driver
const int MOTOR_A_IN1 = 7;
const int MOTOR_A_IN2 = 6;
const int MOTOR_A_EN = 5;   // PWM pin

const int MOTOR_B_IN3 = 4;
const int MOTOR_B_IN4 = 3;
const int MOTOR_B_EN = 2;   // PWM pin

void setup() {
    pinMode(MOTOR_A_IN1, OUTPUT);
    pinMode(MOTOR_A_IN2, OUTPUT);
    pinMode(MOTOR_A_EN, OUTPUT);
    
    pinMode(MOTOR_B_IN3, OUTPUT);
    pinMode(MOTOR_B_IN4, OUTPUT);
    pinMode(MOTOR_B_EN, OUTPUT);
}

void controlMotor(int motor, int speed, bool direction) {
    // motor: 0=A, 1=B
    // speed: 0-255
    // direction: true=forward, false=backward
    
    if (motor == 0) {  // Motor A
        analogWrite(MOTOR_A_EN, abs(speed));
        digitalWrite(MOTOR_A_IN1, direction);
        digitalWrite(MOTOR_A_IN2, !direction);
    } else {  // Motor B
        analogWrite(MOTOR_B_EN, abs(speed));
        digitalWrite(MOTOR_B_IN3, direction);
        digitalWrite(MOTOR_B_IN4, !direction);
    }
}

void stopMotor(int motor) {
    if (motor == 0) {
        digitalWrite(MOTOR_A_IN1, LOW);
        digitalWrite(MOTOR_A_IN2, LOW);
        analogWrite(MOTOR_A_EN, 0);
    } else {
        digitalWrite(MOTOR_B_IN3, LOW);
        digitalWrite(MOTOR_B_IN4, LOW);
        analogWrite(MOTOR_B_EN, 0);
    }
}

void loop() {
    // Jazda do przodu
    controlMotor(0, 200, true);   // Motor A do przodu
    controlMotor(1, 200, true);   // Motor B do przodu
    delay(2000);
    
    // Stop
    stopMotor(0);
    stopMotor(1);
    delay(1000);
    
    // Jazda do tyłu
    controlMotor(0, 150, false);  // Motor A do tyłu
    controlMotor(1, 150, false);  // Motor B do tyłu
    delay(2000);
    
    // Obrót w miejscu
    controlMotor(0, 180, true);   // Motor A do przodu
    controlMotor(1, 180, false);  // Motor B do tyłu
    delay(1000);
    
    stopMotor(0);
    stopMotor(1);
    delay(2000);
}
```

## Aktuatory - Inne

### Przekaźnik (Relay)
```cpp
const int RELAY_PIN = 8;
const int BUTTON_PIN = 2;

bool relayState = false;
bool lastButtonState = false;

void setup() {
    Serial.begin(9600);
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    digitalWrite(RELAY_PIN, LOW);  // Relay OFF
}

void loop() {
    bool buttonState = digitalRead(BUTTON_PIN);
    
    // Wykryj naciśnięcie przycisku (falling edge)
    if (lastButtonState == HIGH && buttonState == LOW) {
        relayState = !relayState;
        digitalWrite(RELAY_PIN, relayState);
        
        Serial.print("Relay: ");
        Serial.println(relayState ? "ON" : "OFF");
        
        delay(200);  // Debouncing
    }
    
    lastButtonState = buttonState;
}
```

### Buzzer (Piezoelectric)
```cpp
const int BUZZER_PIN = 8;

// Nuty muzyczne (częstotliwości w Hz)
#define NOTE_C4  262
#define NOTE_D4  294
#define NOTE_E4  330
#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  494
#define NOTE_C5  523

void setup() {
    pinMode(BUZZER_PIN, OUTPUT);
}

void playTone(int frequency, int duration) {
    tone(BUZZER_PIN, frequency, duration);
    delay(duration);
    noTone(BUZZER_PIN);
}

void playMelody() {
    int melody[] = {NOTE_C4, NOTE_D4, NOTE_E4, NOTE_F4, NOTE_G4, NOTE_A4, NOTE_B4, NOTE_C5};
    int duration = 500;
    
    for (int i = 0; i < 8; i++) {
        playTone(melody[i], duration);
        delay(50);  // Pauza między nutami
    }
}

void alarmSound() {
    for (int i = 0; i < 5; i++) {
        playTone(1000, 200);  // Wysoki ton
        delay(100);
        playTone(500, 200);   // Niski ton
        delay(100);
    }
}

void loop() {
    playMelody();
    delay(2000);
    
    alarmSound();
    delay(3000);
}
```

### LED Strip (WS2812B - NeoPixel)
```cpp
#include <Adafruit_NeoPixel.h>

#define LED_PIN    6
#define NUM_LEDS   30

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
    strip.begin();
    strip.show();  // Initialize all pixels to 'off'
    strip.setBrightness(50);  // 0-255
}

void colorWipe(uint32_t color, int wait) {
    for (int i = 0; i < strip.numPixels(); i++) {
        strip.setPixelColor(i, color);
        strip.show();
        delay(wait);
    }
}

void rainbow(int wait) {
    for (long firstPixelHue = 0; firstPixelHue < 5 * 65536; firstPixelHue += 256) {
        for (int i = 0; i < strip.numPixels(); i++) {
            int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
            strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
        }
        strip.show();
        delay(wait);
    }
}

void loop() {
    // Red wipe
    colorWipe(strip.Color(255, 0, 0), 50);
    delay(500);
    
    // Green wipe
    colorWipe(strip.Color(0, 255, 0), 50);
    delay(500);
    
    // Blue wipe
    colorWipe(strip.Color(0, 0, 255), 50);
    delay(500);
    
    // Rainbow
    rainbow(10);
    
    // Clear
    colorWipe(strip.Color(0, 0, 0), 50);
    delay(1000);
}
```

## Kalibracja sensorów

### Kalibracja dwupunktowa (linear)
```cpp
// Przykład dla sensora analogowego
struct CalibrationData {
    float rawMin, rawMax;
    float realMin, realMax;
    float slope, offset;
};

CalibrationData cal = {0, 1023, 0.0, 100.0, 0, 0};

void calculateCalibration() {
    cal.slope = (cal.realMax - cal.realMin) / (cal.rawMax - cal.rawMin);
    cal.offset = cal.realMin - cal.slope * cal.rawMin;
}

float calibratedRead(int pin) {
    int raw = analogRead(pin);
    return cal.slope * raw + cal.offset;
}

void performCalibration() {
    Serial.println("Kalibracja: ustaw sensor na wartość minimalną");
    delay(5000);
    int rawMin = 0;
    for (int i = 0; i < 100; i++) {
        rawMin += analogRead(A0);
        delay(10);
    }
    cal.rawMin = rawMin / 100.0;
    
    Serial.println("Kalibracja: ustaw sensor na wartość maksymalną");
    delay(5000);
    int rawMax = 0;
    for (int i = 0; i < 100; i++) {
        rawMax += analogRead(A0);
        delay(10);
    }
    cal.rawMax = rawMax / 100.0;
    
    calculateCalibration();
    Serial.println("Kalibracja zakończona");
}
```

## Multipleksowanie sensorów

### Analogowy multiplekser (CD74HC4067)
```cpp
const int MUX_S0 = 2;
const int MUX_S1 = 3;
const int MUX_S2 = 4;
const int MUX_S3 = 5;
const int MUX_SIG = A0;

void setup() {
    Serial.begin(9600);
    pinMode(MUX_S0, OUTPUT);
    pinMode(MUX_S1, OUTPUT);
    pinMode(MUX_S2, OUTPUT);
    pinMode(MUX_S3, OUTPUT);
}

void selectMuxChannel(int channel) {
    digitalWrite(MUX_S0, channel & 0x01);
    digitalWrite(MUX_S1, (channel >> 1) & 0x01);
    digitalWrite(MUX_S2, (channel >> 2) & 0x01);
    digitalWrite(MUX_S3, (channel >> 3) & 0x01);
}

int readMuxChannel(int channel) {
    selectMuxChannel(channel);
    delayMicroseconds(10);  // Stabilizacja
    return analogRead(MUX_SIG);
}

void loop() {
    for (int i = 0; i < 16; i++) {
        int value = readMuxChannel(i);
        Serial.print("Channel ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(value);
    }
    Serial.println("---");
    delay(1000);
}
```

## Powiązane tematy
- [[io_cyfrowe_analogowe|Wejścia/Wyjścia Cyfrowe i Analogowe]]
- [[protokoly_komunikacyjne|Protokoły Komunikacyjne]]
- [[arduino_podstawy|Arduino - Podstawy]]
- [[interfejsy_sprzętowe|Interfejsy Sprzętowe]]
- [[projekty_i_cwiczenia|Projekty i Ćwiczenia Laboratoryjne]]
- [[signal_processing|Przetwarzanie Sygnałów w Embedded]]