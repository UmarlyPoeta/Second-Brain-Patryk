# Arduino - Podstawy

## Hardware Arduino
- **Mikrokontroler**: Zazwyczaj ATmega328P (Arduino Uno), ATmega2560 (Arduino Mega)
- **Architektura**: 8-bitowa architektura Harvard
- **Taktowanie**: 16 MHz (większość modeli)
- **Pamięć**: 
  - Flash: 32KB (Uno), 256KB (Mega)
  - SRAM: 2KB (Uno), 8KB (Mega)
  - EEPROM: 1KB (Uno), 4KB (Mega)

## Popularne modele Arduino
- **Arduino Uno**: Podstawowy model, idealny do nauki
- **Arduino Nano**: Kompaktowa wersja Uno
- **Arduino Mega**: Więcej pinów I/O, większa pamięć
- **Arduino Leonardo**: Wbudowana obsługa USB HID
- **Arduino Pro Mini**: Bardzo mały, bez złączy USB
- **Arduino ESP32**: WiFi i Bluetooth wbudowane
- **Arduino MKR**: Rodzina z wbudowaną łącznością (WiFi, GSM, LoRa)

## Arduino IDE i środowisko programistyczne
### Instalacja i konfiguracja
- **Arduino IDE**: Download z arduino.cc
- **VS Code + PlatformIO**: Profesjonalne środowisko programistyczne
- **Arduino CLI**: Narzędzie linii poleceń

### Struktura programu Arduino
```cpp
void setup() {
  // Kod wykonywany raz przy starcie
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  // Kod wykonywany w pętli
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
  delay(1000);
}
```

## Podstawowe funkcje programowania Arduino

### Funkcje cyfrowe I/O
```cpp
// Ustawienie pinu jako wejście lub wyjście
pinMode(pin, INPUT);    // lub OUTPUT, INPUT_PULLUP
digitalWrite(pin, HIGH); // lub LOW
int value = digitalRead(pin);
```

### Funkcje analogowe I/O
```cpp
// Odczyt analogowy (0-1023)
int value = analogRead(A0);
// Wyjście PWM (0-255)
analogWrite(pin, 128);
```

### Funkcje czasu
```cpp
delay(1000);           // Opóźnienie w milisekundach
delayMicroseconds(100); // Opóźnienie w mikrosekundach
unsigned long time = millis(); // Czas od uruchomienia w ms
unsigned long utime = micros(); // Czas w mikrosekundach
```

### Komunikacja szeregowa
```cpp
Serial.begin(9600);    // Inicjalizacja portu szeregowego
Serial.print("Tekst");
Serial.println("Tekst z nową linią");
Serial.read();         // Odczyt jednego bajtu
Serial.available();    // Liczba dostępnych bajtów
```

## Przykładowy kod - migająca dioda LED

```cpp
// Migająca dioda LED z regulowaną częstotliwością
const int LED_PIN = 13;
const int BUTTON_PIN = 2;
int blinkDelay = 500;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  // Miganie LED
  digitalWrite(LED_PIN, HIGH);
  delay(blinkDelay);
  digitalWrite(LED_PIN, LOW);
  delay(blinkDelay);
  
  // Sprawdzenie przycisku
  if (digitalRead(BUTTON_PIN) == LOW) {
    blinkDelay = (blinkDelay == 500) ? 100 : 500;
    delay(200); // Debouncing
  }
  
  Serial.println("LED migla");
}
```

## Biblioteki Arduino

### Podstawowe biblioteki
- **Wire.h**: Komunikacja I2C
- **SPI.h**: Komunikacja SPI
- **SoftwareSerial.h**: Dodatkowe porty szeregowe
- **EEPROM.h**: Obsługa pamięci EEPROM
- **Servo.h**: Sterowanie serwo silnikami

### Instalacja bibliotek
```cpp
// W Arduino IDE: Sketch → Include Library → Manage Libraries
// Lub przez PlatformIO: lib_deps w platformio.ini
```

## Bootloader i programowanie

### Bootloader Arduino
- **Optiboot**: Standardowy bootloader dla większości Arduino
- **Funkcja**: Umożliwia programowanie przez port szeregowy
- **Rozmiar**: ~512 bajtów we flash memory

### Programowanie przez ISP
```cpp
// Programowanie przez In-System Programming
// Wymagany programator (np. USBasp, Arduino jako ISP)
// Bezpośredni dostęp do mikrokontrolera
```

## Optymalizacja kodu Arduino

### Zarządzanie pamięcią
```cpp
// Używanie PROGMEM dla stałych
const char text[] PROGMEM = "Tekst w pamięci Flash";

// Unikanie fragmentacji stosu
String tekst = "Użyj char[] zamiast String";
```

### Optymalizacja czasów wykonania
```cpp
// Unikanie delay() w aplikacjach czasu rzeczywistego
unsigned long lastTime = 0;
const unsigned long interval = 1000;

void loop() {
  unsigned long currentTime = millis();
  if (currentTime - lastTime >= interval) {
    lastTime = currentTime;
    // Kod do wykonania co sekundę
  }
}
```

## Debugowanie Arduino

### Serial Monitor debugging
```cpp
void debugPrint(String message) {
  #ifdef DEBUG
  Serial.println(String(millis()) + ": " + message);
  #endif
}
```

### LED indicators
```cpp
void errorBlink(int count) {
  for(int i = 0; i < count; i++) {
    digitalWrite(13, HIGH);
    delay(200);
    digitalWrite(13, LOW);
    delay(200);
  }
}
```

## Powiązane tematy
- [[raspberry_pi|Raspberry Pi]]
- [[mikrokontrolery_vs_mikroprocesory|Mikrokontrolery vs Mikroprocesory]]
- [[io_cyfrowe_analogowe|Wejścia/Wyjścia Cyfrowe i Analogowe]]
- [[protokoly_komunikacyjne|Protokoły Komunikacyjne]]
- [[embedded_programming|Programowanie Embedded]]