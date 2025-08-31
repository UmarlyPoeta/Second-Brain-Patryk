# Schemat Elektryczny - Projektowanie

## 🎯 Wprowadzenie

Schemat elektryczny to graficzny opis połączeń w układzie elektronicznym. To pierwszy i najważniejszy krok w projektowaniu PCB - wszystkie późniejsze etapy bazują na poprawnie zaprojektowanym schemacie. Dobry schemat to fundament udanego projektu.

## 📐 Podstawy schematów

### Cel schematu elektrycznego
- **Dokumentacja**: opis funkcjonalności układu
- **Komunikacja**: zrozumiały język między inżynierami
- **Podstawa PCB**: layout bazuje na schemacie
- **Troubleshooting**: podstawa do diagnozy problemów

### Rodzaje schematów
- **Schematic capture**: schemat funkcjonalny
- **Block diagram**: ogólna architektura systemu
- **Timing diagram**: relacje czasowe sygnałów
- **Flowchart**: algorytm działania

## 🔤 Symbole i oznaczenia

### Podstawowe symbole
→ Zobacz szczegółowy przegląd w [[pcb_symbole_graficzne|Symbole Graficzne]]

#### Komponenty pasywne
```
R = Rezystor     ┌─────┐
                 │  R  │
                 └─────┘

C = Kondensator  ├─────┤
                 
L = Cewka        ┌∼∼∼∼∼┐
                 └─────┘
```

#### Komponenty aktywne
```
Q = Tranzystor   ┌─ C
                 │ /
               B ─│
                 │ \
                 └─ E

U = IC          ┌─────┐
                │  U1 │
                │     │
                └─────┘
```

### Standardy oznaczeń
- **IEEE 315**: amerykański standard
- **IEC 60617**: międzynarodowy standard europejski
- **Oznaczenia pozycyjne**: R1, C1, U1, etc.

## 🎨 Zasady projektowania schematu

### Układ i organizacja

#### Kierunek przepływu sygnałów
- **Lewa → Prawa**: wejście do wyjścia
- **Góra → Dół**: zasilanie do masy
- **Logiczny flow**: intuicyjny układ

#### Grupowanie funkcjonalne
- **Power supply**: osobna sekcja
- **Mikrokontoler**: centralnie
- **Interfejsy**: po bokach
- **Analog/Digital**: separacja

### Zasady rysowania

#### Linie połączeń (nets)
- **Proste linie**: unikaj niepotrzebnych załamań
- **90° kąty**: tylko gdy konieczne
- **Skrzyżowania**: kropka = połączenie, brak kropki = brak połączenia
- **Długość**: minimalna konieczna

#### Orientacja komponentów
- **Jednolita**: wszystkie IC w tym samym kierunku
- **Logiczna**: wejścia z lewej, wyjścia z prawej
- **Czytelnośc**: etykiety horyzontalne gdy możliwe

### Naming convention

#### Oznaczenia komponentów
```
R1, R2, R3...    - rezystory
C1, C2, C3...    - kondensatory
L1, L2, L3...    - cewki
D1, D2, D3...    - diody
Q1, Q2, Q3...    - tranzystory
U1, U2, U3...    - układy scalone
J1, J2, J3...    - złącza/connectory
SW1, SW2...      - przełączniki
```

#### Nazwy sieci (nets)
- **Zasilanie**: VCC, VDD, +5V, +3V3
- **Masa**: GND, DGND, AGND
- **Sygnały**: SDA, SCL, UART_TX, PWM1
- **Taktowanie**: XTAL1, CLK, OSC_IN

## ⚡ Sekcje typowego schematu

### 1. Zasilanie (Power Supply)

#### Regulacja napięcia
```
VIN ─┬─ C1 ─┬─ U1(REG) ─┬─ C2 ─┬─ VOUT
     │      │  (LM7805) │      │
     └─ GND ┴───────────┴─ GND ┴─ GND
```

#### Filtrowanie
- **Kondensatory wejściowe**: eliminacja zakłóceń z sieci
- **Kondensatory wyjściowe**: stabilizacja napięcia
- **Ferrite beads**: tłumienie wysokich częstotliwości

#### Pomiary i wskaźniki
- **LED power**: wskaźnik zasilania
- **Test points**: punkty pomiarowe
- **Fuses**: bezpieczniki

### 2. Mikrokontroler (MCU)

#### Minimalna konfiguracja
```
- Power pins: VCC, GND
- Decoupling capacitors: 100nF ceramic
- Reset circuit: przycisk + pull-up
- Programming interface: JTAG/SWD/UART
```

#### Taktowanie
- **Kwarc zewnętrzny**: precyzja ±20ppm
- **Oscylator wewnętrzny**: ±1-2% accuracy
- **Load capacitors**: zwykle 18-22pF

#### Reset circuit
```
VCC ──┬─ R1 ─┬─ RESET
      │      │
      └─ C1 ─┴─ SW1 ─ GND
```

### 3. Interfejsy komunikacyjne

#### UART
```
MCU_TX ─────────── RX_Device
MCU_RX ─────────── TX_Device
GND ───────────── GND
```

#### SPI
```
MCU_SCK ──────── SCK_Device
MCU_MOSI ─────── MOSI_Device  
MCU_MISO ─────── MISO_Device
MCU_CS ───────── CS_Device
```

#### I2C
```
MCU_SDA ──┬─ R_PU ─ VCC
          └──────── SDA_Device
          
MCU_SCL ──┬─ R_PU ─ VCC  
          └──────── SCL_Device
```

### 4. Analog frontend

#### ADC conditioning
- **Voltage dividers**: skalowanie napięcia
- **Op-amp buffers**: izolacja impedancji
- **Anti-aliasing filters**: RC lub aktywne
- **ESD protection**: TVS diodes

#### Reference voltage
- **Precision references**: LM4040, REF3030
- **Filtering**: RC networks dla noise
- **Buffering**: op-amp follower

## 🧪 Weryfikacja schematu

### Design Rules Check (DRC)

#### Elektryczne zasady
- **Unconnected pins**: wszystkie piny podłączone
- **Power connections**: prawidłowe zasilanie
- **Pin types**: input nie może napędzać input
- **Short circuits**: sprawdzenie zwarć

#### Komponenty
- **Values assigned**: wszystkie wartości określone
- **Footprints assigned**: wszystkie footprinty przypisane
- **Part numbers**: jeśli wymagane

### Circuit analysis

#### DC analysis
- **Operating points**: sprawdzenie punktów pracy
- **Power calculations**: pobór mocy
- **Voltage levels**: zgodność logiczna 3.3V/5V

#### AC analysis
- **Frequency response**: filtry, wzmacniacze
- **Stability**: pętle sprzężenia zwrotnego
- **Noise analysis**: SNR, szumy

## 📊 Symulacje SPICE

### Rodzaje analiz
- **DC Operating Point**: punkty pracy
- **AC Small-Signal**: charakterystyki częstotliwościowe
- **Transient**: analiza czasowa
- **Monte Carlo**: analiza tolerancji

### Popularne symulatory
- **LTSpice**: darmowy od Linear Technology
- **TINA-TI**: darmowy od Texas Instruments
- **Multisim**: komercjalny od National Instruments
- **KiCad Spice**: wbudowany w KiCad

## 🎯 Best Practices

### Czytelność schematu

#### Organizacja
- **Hierarchical sheets**: podział na logiczne bloki
- **Consistent spacing**: jednolite odstępy
- **No crossing wires**: unikaj krzyżujących się linii
- **Power rails**: na górze i dole schematu

#### Dokumentacja
- **Title block**: informacje o projekcie
- **Revision control**: śledzenie wersji
- **Notes**: ważne informacje projektowe
- **Component values**: wszystkie wartości widoczne

### Projektowe
- **Redundancy**: backup circuits dla krytycznych funkcji
- **Test points**: dostęp do kluczowych sygnałów
- **Debug interfaces**: UART, JTAG
- **Status LEDs**: wskaźniki stanu

### Produkcyjne
- **Standard parts**: komponenty łatwo dostępne
- **Derating**: margines bezpieczeństwa
- **Alternative parts**: backup komponenty
- **Assembly notes**: instrukcje montażu

## 🔍 Częste błędy

### Elektryczne
- **Floating inputs**: nie podłączone wejścia cyfrowe
- **Missing pull-ups**: I2C, reset lines
- **Power sequencing**: nieprawidłowa kolejność włączania
- **Ground loops**: wielokrotne ścieżki masy

### Projektowe
- **Pin assignments**: nieoptymalne przypisanie pinów
- **Pinout mismatch**: niezgodność z footprintem
- **Missing decoupling**: brak kondensatorów odsprzęgających
- **Inadequate current paths**: za wąskie ścieżki zasilania

### Dokumentacyjne
- **Missing references**: brak oznaczeń komponentów
- **Inconsistent naming**: niejednolite nazwy sieci
- **No schematic notes**: brak dokumentacji decyzji projektowych

## 🛠️ Narzędzia do schematów

### Profesjonalne
- **Altium Designer**: standard przemysłowy
- **Cadence OrCAD**: zaawansowane symulacje
- **Mentor Graphics**: enterprise solutions

### Open source / hobby
- **KiCad**: kompletny, darmowy pakiet
- **Eagle**: popularny, ograniczona wersja darmowa  
- **DipTrace**: prosty w użyciu
→ Zobacz [[pcb_narzedzia_kicad|KiCad]] dla szczegółów

## 📚 Hierarchical Design

### Sheet hierarchy
- **Top-level sheet**: główny schemat
- **Sub-sheets**: moduły funkcjonalne
- **Hierarchical labels**: połączenia między sheets
- **Global labels**: sygnały dostępne wszędzie

### Modular approach
- **Power supply module**: regulacja napięć
- **MCU module**: mikrokontroler + podstawowe funkcje  
- **Interface modules**: UART, SPI, I2C
- **Analog modules**: conditioning, ADC

### Benefits
- **Organizacja**: podział na zarządzalne części
- **Reusability**: moduły do kolejnych projektów
- **Team work**: podział pracy między członków zespołu
- **Maintenance**: łatwiejsze modyfikacje

## 🔗 Powiązane tematy
- [[pcb_podstawy|Podstawy PCB]] - podstawowe pojęcia
- [[pcb_komponenty_elektroniczne|Komponenty Elektroniczne]] - elementy schematów  
- [[pcb_symbole_graficzne|Symbole Graficzne]] - standardowe symbole
- [[pcb_biblioteki_komponentow|Biblioteki Komponentów]] - zarządzanie symbolami
- [[pcb_projekt_layoutu|Projekt Layoutu]] - od schematu do PCB
- [[pcb_narzedzia_kicad|KiCad]] - praktyczne narzędzie do schematów

---

**🎯 Co dalej?**
Po opanowaniu projektowania schematów, przejdź do [[pcb_symbole_graficzne|Symboli Graficznych]] aby poznać standardowe oznaczenia komponentów, lub bezpośrednio do [[pcb_projekt_layoutu|Projektu Layoutu]] aby zacząć przekształcać schemat w fizyczną płytkę PCB.