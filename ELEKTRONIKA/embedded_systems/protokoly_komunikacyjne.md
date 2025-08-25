# Protokoły Komunikacyjne w Systemach Embedded

## UART (Universal Asynchronous Receiver-Transmitter)

### Podstawy UART
- **Rodzaj**: Asynchroniczny, punkt-punkt
- **Przewody**: TX (transmit), RX (receive), GND
- **Konfiguracja**: Baud rate, data bits, parity, stop bits
- **Przykład**: 9600-8-N-1 (9600 bps, 8 bitów danych, no parity, 1 stop bit)

### Format ramki UART
```
Start bit | Data bits (5-9) | Parity (opt.) | Stop bit(s)
    0     |   D0 D1...D7    |       P       |   1 (lub 2)
```

### Arduino UART
```cpp
void setup() {
    Serial.begin(9600);      // UART0 (pins 0,1)
    Serial1.begin(115200);   // UART1 na Mega (pins 19,18)
}

void loop() {
    // Wysyłanie danych
    Serial.println("Hello World");
    Serial.print("Wartość: ");
    Serial.println(123);
    
    // Odbieranie danych
    if (Serial.available() > 0) {
        String receivedData = Serial.readString();
        receivedData.trim();  // Usuń whitespace
        Serial.println("Odebrano: " + receivedData);
    }
}
```

### SoftwareSerial (dodatkowe porty)
```cpp
#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX

void setup() {
    Serial.begin(9600);
    mySerial.begin(9600);
}

void loop() {
    // Przekazywanie danych między portami
    if (mySerial.available()) {
        Serial.write(mySerial.read());
    }
    if (Serial.available()) {
        mySerial.write(Serial.read());
    }
}
```

### Protokoły na bazie UART

#### Modbus RTU
```cpp
// Przykład ramki Modbus RTU
struct ModbusFrame {
    uint8_t slaveAddress;
    uint8_t functionCode;
    uint16_t startAddress;
    uint16_t quantity;
    uint16_t crc;
};

uint16_t calculateCRC16(uint8_t *data, uint8_t length) {
    uint16_t crc = 0xFFFF;
    for (uint8_t i = 0; i < length; i++) {
        crc ^= data[i];
        for (uint8_t j = 0; j < 8; j++) {
            if (crc & 0x0001) {
                crc = (crc >> 1) ^ 0xA001;
            } else {
                crc >>= 1;
            }
        }
    }
    return crc;
}
```

#### AT Commands (GSM/WiFi moduły)
```cpp
String sendATCommand(String command, int timeout = 1000) {
    Serial1.println(command);
    
    unsigned long startTime = millis();
    String response = "";
    
    while (millis() - startTime < timeout) {
        if (Serial1.available()) {
            response += Serial1.readString();
            if (response.indexOf("OK") != -1 || response.indexOf("ERROR") != -1) {
                break;
            }
        }
    }
    return response;
}

void setup() {
    Serial1.begin(115200);  // GSM module
    
    String response = sendATCommand("AT");  // Test
    if (response.indexOf("OK") != -1) {
        Serial.println("Moduł odpowiada");
    }
}
```

## SPI (Serial Peripheral Interface)

### Podstawy SPI
- **Rodzaj**: Synchroniczny, master-slave
- **Przewody**: MOSI (Master Out Slave In), MISO (Master In Slave Out), SCK (Serial Clock), SS/CS (Slave Select)
- **Konfiguracja**: Clock polarity (CPOL), Clock phase (CPHA)
- **Prędkość**: Bardzo wysoka (MHz)

### Modi SPI
```
Mode 0: CPOL=0, CPHA=0  (Clock idle LOW, sample on rising edge)
Mode 1: CPOL=0, CPHA=1  (Clock idle LOW, sample on falling edge)
Mode 2: CPOL=1, CPHA=0  (Clock idle HIGH, sample on falling edge)
Mode 3: CPOL=1, CPHA=1  (Clock idle HIGH, sample on rising edge)
```

### Arduino SPI
```cpp
#include <SPI.h>

const int chipSelectPin = 10;

void setup() {
    SPI.begin();
    pinMode(chipSelectPin, OUTPUT);
    digitalWrite(chipSelectPin, HIGH);  // Slave nieaktywny
    
    // Konfiguracja SPI
    SPI.setClockDivider(SPI_CLOCK_DIV16);  // 1MHz przy 16MHz
    SPI.setDataMode(SPI_MODE0);
    SPI.setBitOrder(MSBFIRST);
}

byte spiTransfer(byte data) {
    digitalWrite(chipSelectPin, LOW);   // Aktywuj slave
    byte result = SPI.transfer(data);   // Wyślij i odbierz
    digitalWrite(chipSelectPin, HIGH);  // Deaktywuj slave
    return result;
}

void loop() {
    byte response = spiTransfer(0xAA);
    Serial.println(response, HEX);
    delay(1000);
}
```

### SPI z wieloma urządzeniami
```cpp
const int device1CS = 10;
const int device2CS = 9;

void selectDevice(int device) {
    digitalWrite(device1CS, device == 1 ? LOW : HIGH);
    digitalWrite(device2CS, device == 2 ? LOW : HIGH);
}

void communicateWithDevice1() {
    selectDevice(1);
    SPI.transfer(0x01);  // Komenda dla device1
    byte response = SPI.transfer(0x00);  // Dummy byte dla odpowiedzi
    selectDevice(0);     // Deselect all
}
```

### AVR SPI (bare metal)
```c
void spi_master_init() {
    // Ustaw MOSI i SCK jako wyjście
    DDRB |= (1 << PB3) | (1 << PB5) | (1 << PB2);  // MOSI, SCK, SS
    
    // Włącz SPI, Master mode, clock/16
    SPCR = (1 << SPE) | (1 << MSTR) | (1 << SPR0);
}

uint8_t spi_transfer(uint8_t data) {
    SPDR = data;                    // Rozpocznij transmisję
    while (!(SPSR & (1 << SPIF)));  // Czekaj na zakończenie
    return SPDR;                    // Zwróć odebrane dane
}
```

## I2C (Inter-Integrated Circuit)

### Podstawy I2C
- **Rodzaj**: Synchroniczny, multi-master, multi-slave
- **Przewody**: SDA (Serial Data), SCL (Serial Clock)
- **Adresy**: 7-bit (128 adresów) lub 10-bit
- **Prędkość**: Standard (100kHz), Fast (400kHz), Fast+ (1MHz)

### Protokół I2C
```
Start | Slave Addr + R/W | ACK | Data | ACK | ... | Stop
  S   |    7 bits + 1    | A/N |  8   | A/N | ... |  P
```

### Arduino I2C (Wire library)
```cpp
#include <Wire.h>

#define SLAVE_ADDRESS 0x48  // Adres urządzenia slave

void setup() {
    Wire.begin();        // Master mode
    Serial.begin(9600);
}

// Zapis danych do slave
void writeToSlave(uint8_t reg, uint8_t data) {
    Wire.beginTransmission(SLAVE_ADDRESS);
    Wire.write(reg);     // Adres rejestru
    Wire.write(data);    // Dane do zapisu
    uint8_t error = Wire.endTransmission();
    
    if (error != 0) {
        Serial.print("I2C Error: ");
        Serial.println(error);
    }
}

// Odczyt danych z slave
uint8_t readFromSlave(uint8_t reg) {
    // Zapisz adres rejestru
    Wire.beginTransmission(SLAVE_ADDRESS);
    Wire.write(reg);
    Wire.endTransmission(false);  // Restart zamiast stop
    
    // Czytaj dane
    Wire.requestFrom(SLAVE_ADDRESS, 1);
    if (Wire.available()) {
        return Wire.read();
    }
    return 0;  // Błąd
}

void loop() {
    writeToSlave(0x01, 0xFF);
    uint8_t value = readFromSlave(0x01);
    Serial.println(value, HEX);
    delay(1000);
}
```

### I2C Scanner
```cpp
void scanI2C() {
    Serial.println("Skanowanie urządzeń I2C...");
    
    for (uint8_t address = 1; address < 127; address++) {
        Wire.beginTransmission(address);
        uint8_t error = Wire.endTransmission();
        
        if (error == 0) {
            Serial.print("Urządzenie na adresie 0x");
            if (address < 16) Serial.print("0");
            Serial.println(address, HEX);
        }
    }
}
```

### I2C Slave (Arduino)
```cpp
#include <Wire.h>

volatile uint8_t registers[16] = {0};  // Tablica rejestrów
volatile uint8_t currentRegister = 0;

void setup() {
    Wire.begin(0x48);                // Tryb slave, adres 0x48
    Wire.onReceive(receiveEvent);    // Callback dla odbioru
    Wire.onRequest(requestEvent);    // Callback dla żądania danych
}

void receiveEvent(int bytes) {
    if (bytes >= 1) {
        currentRegister = Wire.read();  // Pierwszy bajt to adres rejestru
    }
    
    while (Wire.available()) {
        if (currentRegister < 16) {
            registers[currentRegister] = Wire.read();
            currentRegister++;
        }
    }
}

void requestEvent() {
    if (currentRegister < 16) {
        Wire.write(registers[currentRegister]);
    }
}

void loop() {
    // Główna logika slave
    delay(100);
}
```

## CAN Bus (Controller Area Network)

### Podstawy CAN
- **Zastosowanie**: Automotive, industrial automation
- **Przewody**: CAN_H, CAN_L (differential pair)
- **Prędkość**: 125kbps - 1Mbps
- **Arbitraż**: CSMA/CD z priorytetami

### Format ramki CAN
```
SOF | ID (11/29-bit) | RTR | IDE | r0 | DLC | Data (0-8B) | CRC | ACK | EOF
```

### Arduino CAN (MCP2515)
```cpp
#include <SPI.h>
#include "mcp2515_can.h"

mcp2515_can CAN(10);  // CS pin 10

void setup() {
    Serial.begin(115200);
    
    while (CAN_OK != CAN.begin(CAN_500KBPS)) {
        Serial.println("CAN init fail, retry...");
        delay(100);
    }
    Serial.println("CAN init ok!");
}

void sendCANMessage(uint32_t id, uint8_t *data, uint8_t length) {
    CAN.sendMsgBuf(id, 0, length, data);  // Standardowy frame
}

void loop() {
    uint8_t data[8] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
    sendCANMessage(0x123, data, 8);
    
    // Odbieranie wiadomości
    uint8_t len;
    uint8_t buf[8];
    uint32_t canId;
    
    if (CAN_MSGAVAIL == CAN.checkReceive()) {
        CAN.readMsgBuf(&canId, &len, buf);
        Serial.print("ID: 0x");
        Serial.print(canId, HEX);
        Serial.print(" Data: ");
        for (int i = 0; i < len; i++) {
            Serial.print(buf[i], HEX);
            Serial.print(" ");
        }
        Serial.println();
    }
    
    delay(1000);
}
```

## 1-Wire Protocol

### Podstawy 1-Wire
- **Dallas Semiconductor**: Jeden przewód + GND
- **Zastosowanie**: Sensory temperatury (DS18B20), RTC, EEPROM
- **Adresowanie**: 64-bitowy unikalny adres ROM

### Arduino OneWire
```cpp
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
    Serial.begin(9600);
    sensors.begin();
    
    // Znajdź urządzenia
    Serial.print("Liczba urządzeń: ");
    Serial.println(sensors.getDeviceCount());
}

void loop() {
    sensors.requestTemperatures();  // Żądanie pomiaru
    
    float tempC = sensors.getTempCByIndex(0);  // Pierwszy sensor
    
    if (tempC != DEVICE_DISCONNECTED_C) {
        Serial.print("Temperatura: ");
        Serial.print(tempC);
        Serial.println("°C");
    } else {
        Serial.println("Błąd odczytu sensora");
    }
    
    delay(1000);
}
```

## Ethernet i TCP/IP

### Arduino Ethernet
```cpp
#include <Ethernet.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 1, 177);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

EthernetServer server(80);  // HTTP server

void setup() {
    Ethernet.begin(mac, ip, gateway, subnet);
    server.begin();
    Serial.print("Server IP: ");
    Serial.println(Ethernet.localIP());
}

void loop() {
    EthernetClient client = server.available();
    
    if (client) {
        String request = "";
        while (client.connected()) {
            if (client.available()) {
                char c = client.read();
                request += c;
                
                if (request.endsWith("\r\n\r\n")) {
                    // HTTP response
                    client.println("HTTP/1.1 200 OK");
                    client.println("Content-Type: text/html");
                    client.println();
                    client.println("<h1>Arduino Web Server</h1>");
                    client.println("<p>Temperature: 25°C</p>");
                    break;
                }
            }
        }
        client.stop();
    }
}
```

## WiFi (ESP32/ESP8266)

### ESP32 WiFi
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "your_network";
const char* password = "your_password";

WebServer server(80);

void handleRoot() {
    String html = "<html><body>";
    html += "<h1>ESP32 Web Server</h1>";
    html += "<p>Uptime: " + String(millis() / 1000) + " seconds</p>";
    html += "</body></html>";
    
    server.send(200, "text/html", html);
}

void setup() {
    Serial.begin(115200);
    
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    
    server.on("/", handleRoot);
    server.begin();
}

void loop() {
    server.handleClient();
}
```

### MQTT (ESP32)
```cpp
#include <WiFi.h>
#include <PubSubClient.h>

const char* mqtt_server = "192.168.1.100";
const char* mqtt_topic = "sensors/temperature";

WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("] ");
    
    String message = "";
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    Serial.println(message);
}

void setup() {
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
    
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);
}

void reconnect() {
    while (!client.connected()) {
        if (client.connect("ESP32Client")) {
            client.subscribe("commands/led");
        } else {
            delay(5000);
        }
    }
}

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    
    // Publikuj dane co 10 sekund
    static unsigned long lastMsg = 0;
    if (millis() - lastMsg > 10000) {
        lastMsg = millis();
        float temperature = 25.5;  // Przykładowa wartość
        String msg = String(temperature);
        client.publish(mqtt_topic, msg.c_str());
    }
}
```

## Bluetooth (Classic i BLE)

### HC-05 Bluetooth Classic
```cpp
#include <SoftwareSerial.h>

SoftwareSerial bluetooth(2, 3);  // RX, TX

void setup() {
    Serial.begin(9600);
    bluetooth.begin(9600);
    
    Serial.println("Bluetooth Ready");
}

void loop() {
    // Przekazywanie danych między Serial i Bluetooth
    if (bluetooth.available()) {
        String data = bluetooth.readString();
        Serial.println("BT: " + data);
        
        // Echo z dodatkową informacją
        bluetooth.println("Echo: " + data);
    }
    
    if (Serial.available()) {
        String data = Serial.readString();
        bluetooth.println(data);
    }
}
```

### ESP32 BLE
```cpp
#include "BLEDevice.h"
#include "BLEServer.h"
#include "BLEUtils.h"
#include "BLE2902.h"

#define SERVICE_UUID        "12345678-1234-1234-1234-123456789abc"
#define CHARACTERISTIC_UUID "87654321-4321-4321-4321-cba987654321"

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;

class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        Serial.println("Client connected");
    }
    
    void onDisconnect(BLEServer* pServer) {
        Serial.println("Client disconnected");
        pServer->startAdvertising();  // Restart advertising
    }
};

void setup() {
    Serial.begin(115200);
    
    BLEDevice::init("ESP32 Sensor");
    pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());
    
    BLEService *pService = pServer->createService(SERVICE_UUID);
    pCharacteristic = pService->createCharacteristic(
                        CHARACTERISTIC_UUID,
                        BLECharacteristic::PROPERTY_READ |
                        BLECharacteristic::PROPERTY_NOTIFY
                      );

    pService->start();
    pServer->getAdvertising()->start();
    Serial.println("BLE Server started");
}

void loop() {
    // Wysyłaj dane co 5 sekund
    static unsigned long lastTime = 0;
    if (millis() - lastTime > 5000) {
        lastTime = millis();
        
        String sensorData = "Temperature: 25.5C";
        pCharacteristic->setValue(sensorData.c_str());
        pCharacteristic->notify();
        
        Serial.println("Data sent: " + sensorData);
    }
    delay(100);
}
```

## Protokoły przemysłowe

### RS485 (Modbus)
```cpp
#include <SoftwareSerial.h>

SoftwareSerial rs485(2, 3);  // RX, TX
const int enablePin = 4;      // DE/RE pin

void setup() {
    Serial.begin(9600);
    rs485.begin(9600);
    pinMode(enablePin, OUTPUT);
    digitalWrite(enablePin, LOW);  // Receive mode
}

void sendRS485(String data) {
    digitalWrite(enablePin, HIGH);  // Transmit mode
    delay(1);
    rs485.println(data);
    rs485.flush();  // Czekaj na wysłanie
    delay(1);
    digitalWrite(enablePin, LOW);   // Receive mode
}

void loop() {
    // Wysyłaj zapytanie Modbus
    sendRS485(":010300000001FA");  // Read holding register
    
    // Odbieraj odpowiedź
    if (rs485.available()) {
        String response = rs485.readString();
        Serial.println("RS485: " + response);
    }
    
    delay(1000);
}
```

## Debugowanie komunikacji

### Logic Analyzer integration
```cpp
// Dodaj piny debug dla analizy
const int DEBUG_TX = 13;
const int DEBUG_RX = 12;

void debugPulse(int pin, int duration = 100) {
    digitalWrite(pin, HIGH);
    delayMicroseconds(duration);
    digitalWrite(pin, LOW);
}

// Użyj w komunikacji
void spiTransferWithDebug(byte data) {
    debugPulse(DEBUG_TX);  // Sygnał rozpoczęcia
    byte result = SPI.transfer(data);
    debugPulse(DEBUG_RX);  // Sygnał zakończenia
}
```

### Protocol analyzer w Serial Monitor
```cpp
void printHex(uint8_t *data, int length, String prefix = "") {
    Serial.print(prefix);
    for (int i = 0; i < length; i++) {
        if (data[i] < 16) Serial.print("0");
        Serial.print(data[i], HEX);
        Serial.print(" ");
    }
    Serial.println();
}

// Użycie
uint8_t buffer[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x01};
printHex(buffer, 6, "TX: ");
```

## Powiązane tematy
- [[arduino_podstawy|Arduino - Podstawy]]
- [[raspberry_pi|Raspberry Pi]]
- [[sensory_i_aktuatory|Sensory i Aktuatory]]
- [[io_cyfrowe_analogowe|Wejścia/Wyjścia Cyfrowe i Analogowe]]
- [[network_protocols|Protokoły Sieciowe w Embedded]]
- [[industrial_protocols|Protokoły Przemysłowe]]