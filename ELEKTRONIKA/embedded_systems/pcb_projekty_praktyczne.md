# Projekty Praktyczne PCB

## 🎯 Wprowadzenie

Praktyka to najlepszy sposób nauki projektowania PCB. Ta notatka przedstawia szereg projektów o rosnącej złożoności, które pozwolą Ci zastosować zdobytą wiedzę teoretyczną w rzeczywistych projektach. Każdy projekt zawiera pełną specyfikację, wskazówki projektowe i typowe problemy.

## 🚀 Projekt 1: Migacz LED (Poziom: Początkujący)

### Specyfikacja projektu
```
Cel: Nauka podstaw schematów i layoutu
Funkcjonalność: Migający LED z regulowaną częstotliwością
Zasilanie: 9V battery
Wymiary: maksymalnie 50×50mm
Technologia: THT (przez otwory)
```

### Schemat funkcjonalny
```
Battery 9V → LM7805 → +5V → 555 Timer → LED + Rezystor
                 ↓
               GND ← Potencjometr (częstotliwość)
```

### Lista komponentów (BOM)
```
U1: LM7805 voltage regulator (TO-220)
U2: NE555P timer IC (DIP-8)  
R1: 10kΩ resistor (1/4W)
R2: 330Ω resistor (1/4W)
R3: 1kΩ resistor (1/4W)
RV1: 100kΩ potentiometer
C1: 100µF/16V electrolytic
C2: 100nF ceramic
C3: 10µF/16V electrolytic
D1: 5mm LED (red)
J1: DC jack 2.1mm
SW1: SPST switch
```

### Wskazówki projektowe

#### Schemat
1. **Regulator 7805**: dodaj kondensatory input/output
2. **555 Timer**: sprawdź pinout w datasheet
3. **LED current**: oblicz rezystor ograniczający prąd
4. **Power switch**: dla oszczędności baterii

#### Layout
```
Rozmieszczenie sugerowane:
DC Jack → Switch → 7805 → 555 → LED
                    ↓
                 Ground plane (bottom layer)
```

#### Design considerations
- **Trace width**: 0.3mm dla zasilania, 0.2mm dla sygnałów
- **Ground plane**: użyj bottom layer jako ground
- **Component spacing**: minimum 2.54mm między elementami
- **Mounting holes**: 4 rogi, M3 screws

### Typowe problemy i rozwiązania

#### Problem: LED nie świeci
- **Check**: polarność LED (długa nóżka = anoda)
- **Check**: wartość rezystora (czy nie za duża?)
- **Check**: połączenia zasilania

#### Problem: Nieprawidłowa częstotliwość
- **Check**: wartości R i C w obwodzie 555
- **Check**: połączenie potencjometru
- **Modify**: zmień R1 lub C2 dla innej częstotliwości

## ⚡ Projekt 2: Arduino Shield (Poziom: Średniozaawansowany)

### Specyfikacja projektu
```
Cel: Projektowanie standardowego shield dla Arduino Uno
Funkcjonalność: Sensor breakout + LCD display + buttons
Form factor: Arduino Uno R3 compatible
Technologia: Mixed THT + SMD
Power: 5V/3.3V from Arduino
```

### Blok diagram
```
Arduino Uno R3
     ↓
Shield Interface
     ├── I2C LCD 16×2
     ├── DHT22 Temperature sensor  
     ├── 3× Push buttons
     ├── 3× LEDs (status)
     └── Potentiometer (contrast)
```

### Szczegółowy schemat

#### Connections
```
Arduino → Shield:
D2  → Button 1
D3  → Button 2  
D4  → Button 3
D5  → DHT22 Data
D6  → LED 1 (Green)
D7  → LED 2 (Yellow)
D8  → LED 3 (Red)
A4  → LCD SDA (I2C)
A5  → LCD SCL (I2C)
5V  → VCC Rail
GND → GND Rail
```

#### Component details
```
LCD Interface (I2C):
- PCF8574 I2C backpack
- 16×2 character LCD
- Contrast potentiometer

Sensors:
- DHT22: temperature/humidity
- Pull-up resistor 10kΩ

User Interface:  
- 3× tactile switches
- 3× 5mm LEDs
- Pull-up resistors dla buttons
```

### Layout guidelines

#### Mechanical constraints
- **Arduino mounting**: holes compatible z Uno R3
- **Connector placement**: match Arduino pin layout exactly
- **Component height**: nie blokuj USB/power connectors
- **Access**: buttons i potencjometr dostępne z góry

#### Electrical layout
```
Layer assignment (2-layer):
Top:    Components + routing
Bottom: Ground plane + power traces

Critical considerations:
- I2C pullups przy Arduino pins
- Decoupling caps przy każdym IC
- LED current limiting resistors
- Button debouncing (software)
```

### Arduino library considerations

#### Pin definitions
```cpp
// Shield pin definitions
#define BUTTON_1    2
#define BUTTON_2    3  
#define BUTTON_3    4
#define DHT_PIN     5
#define LED_GREEN   6
#define LED_YELLOW  7
#define LED_RED     8
#define LCD_SDA     A4
#define LCD_SCL     A5
```

## 🔧 Projekt 3: ESP32 Development Board (Poziom: Zaawansowany)

### Specyfikacja projektu
```
Cel: Custom ESP32 development board
MCU: ESP32-WROOM-32E module
USB: USB-C connector with CP2102 bridge
Power: 3.3V/5V switching, battery charging
Peripherals: RGB LED, buttons, SD card, sensors
Size: 50×25mm (compact)
Technology: SMD components
```

### System architecture
```
USB-C → CP2102 → ESP32-WROOM-32E
  ↓
Battery Charger (TP4056)
  ↓  
3.3V Regulator (AMS1117-3.3)
  ↓
Peripherals:
├── WS2812B RGB LED
├── 2× User buttons  
├── Reset button
├── Micro SD card slot
└── Sensor headers (I2C/SPI)
```

### Detailed design

#### Power management
```
Power tree:
USB 5V → TP4056 → LiPo Battery (optional)
       → AMS1117-3.3 → ESP32 + peripherals

Features:
- Battery charging indication
- Low battery detection  
- Power switch
- Current measurement test points
```

#### USB interface
```
CP2102N USB-UART Bridge:
- USB-C connector
- Automatic reset circuit
- Boot mode selection
- TX/RX LEDs

Auto-programming circuit:
DTR → C1 → EN (Reset)
RTS → C2 → GPIO0 (Boot)
```

### High-speed design considerations

#### WiFi/Bluetooth antenna
- **Keep-out zones**: no copper under antenna
- **Ground plane**: solid ground under ESP32
- **Crystal layout**: short traces, ground shield
- **Decoupling**: multiple capacitors różnych wartości

#### Signal integrity
```
Critical nets:
- Crystal oscillator: <5mm traces
- USB differential pairs: 90Ω impedance
- SPI flash: length matched
- Power supply: low ESR decoupling
```

### Layout challenges

#### Mechanical constraints
- **USB-C connector**: proper pad design
- **ESP32 module**: thermal pad grounding
- **SD card**: proper card detect switching
- **Antenna**: edge placement

#### Thermal management
```
Heat sources:
- ESP32: główne źródło ciepła
- Regulators: 3.3V regulator
- USB: charging current

Solutions:
- Thermal vias under ESP32
- Ground plane heat spreading  
- Component placement optimization
```

## 🎨 Projekt 4: Audio Amplifier (Poziom: Ekspert)

### Specyfikacja zaawansowana
```
Cel: High-fidelity stereo amplifier
Power: 2×15W @ 8Ω, Class D
Input: Line level, balanced XLR
Output: Speaker terminals
Supply: ±15V linear supply
THD: <0.1% @ 1kHz
SNR: >100dB
```

### Analog design considerations

#### Audio path
```
Input stage:
XLR → Differential input → Volume control → Class D amp

Critical requirements:
- Balanced input design
- Low noise op-amps
- Proper grounding scheme
- EMI filtering
```

#### Power supply design
```
Transformer → Bridge rectifier → Filter caps → Regulators

Requirements:
- Low ripple (<1mVp-p)
- Fast transient response
- Thermal management
- Safety isolation
```

### Advanced layout techniques

#### Analog/digital separation
- **Physical separation**: analog i digital sections
- **Ground isolation**: star ground configuration  
- **Power separation**: separate analog/digital supplies
- **Filtering**: RF filtering na digital clock lines

#### EMI/EMC design
- **Shielding**: ground planes, enclosure
- **Filtering**: common mode chokes, ferrites
- **Layout**: minimize loop areas
- **Cables**: proper shielding, grounding

## 🧪 Project testing methodology

### Design verification

#### Simulation phase
```
SPICE simulations:
☐ DC operating points
☐ AC frequency response  
☐ Transient analysis
☐ Noise analysis
☐ Monte Carlo tolerance
```

#### Prototype testing
```
Electrical tests:
☐ Power supply voltages
☐ Current consumption
☐ Signal integrity
☐ Frequency response
☐ Distortion measurement

Environmental tests:
☐ Temperature cycling
☐ Humidity exposure
☐ Vibration testing
☐ EMC compliance
```

### Troubleshooting guide

#### Common issues
```
Power problems:
- Voltage regulators overheating
- Insufficient decoupling
- Ground loops
- Power sequencing

Signal problems:
- Impedance mismatches
- Crosstalk between signals
- Clock jitter
- Analog interference

Manufacturing issues:
- Solder bridges
- Component orientation
- Missing components  
- Cold solder joints
```

## 📊 Project management tips

### Documentation standards

#### Design package
```
Complete documentation:
☐ Requirements specification
☐ Schematic (PDF + source)
☐ Layout plots
☐ Bill of materials
☐ Assembly drawings
☐ Test procedures
☐ User manual
```

#### Version control
- **Git repository**: wszystkie źródłowe pliki
- **Release tags**: major milestones
- **Change logs**: dokumentacja zmian
- **Backup strategy**: multiple locations

### Cost optimization

#### Design trade-offs
```
Cost factors:
- Component count: fewer = cheaper
- PCB complexity: layers, size, features
- Assembly: hand vs automated
- Testing: in-circuit vs functional
- Enclosure: standard vs custom
```

## 🔗 Recursos i dalszy rozwój

### Learning path progression
```
Beginner → Intermediate → Advanced → Expert
    ↓            ↓            ↓         ↓
 Simple      Arduino     Mixed      RF/Analog
 circuits    shields     technology  designs
```

### Community resources
- **GitHub**: open source PCB projects
- **Hackaday**: project inspiration  
- **Reddit**: r/PrintedCircuitBoard
- **Forums**: EEVBlog, AllAboutCircuits

### Professional development
- **Certifications**: IPC standards training
- **Courses**: university electronics courses
- **Internships**: electronics companies
- **Conferences**: PCB design conferences

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_narzedzia_kicad|KiCad]] - narzędzie do realizacji projektów
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - standardy projektowe
- [[pcb_testowanie_debug|Testowanie i Debug]] - weryfikacja projektów
- [[pcb_produkcja_wytwarzanie|Produkcja PCB]] - realizacja projektów
- [[pcb_bledy_czestie|Częste Błędy]] - unikanie problemów

---

**🎯 Co dalej?**
Wybierz projekt odpowiedni do swojego poziomu i zacznij projektować! Każdy ukończony projekt znacząco zwiększa Twoje umiejętności. Pamiętaj o dokumentowaniu procesu i dzieleniu się rezultatami ze społecznością.