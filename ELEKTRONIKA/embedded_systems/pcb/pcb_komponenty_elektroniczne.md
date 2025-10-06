# Komponenty Elektroniczne w PCB

## 🎯 Wprowadzenie

Komponenty elektroniczne to building blocks każdego układu elektronicznego. Znajomość różnych typów komponentów, ich właściwości i zastosowań jest kluczowa dla projektowania PCB. Ta notatka przedstawia przegląd najważniejszych komponentów używanych w projektowaniu płytek drukowanych.

## 📦 Technologie montażu

### THT - Through-Hole Technology
- **Opis**: komponenty przewlekane przez otwory w PCB
- **Zalety**: mocne połączenia mechaniczne, łatwość ręcznego montażu
- **Wady**: większe rozmiary, gorszy routing
- **Zastosowanie**: prototypy, komponenty dużej mocy, złącza

### SMD/SMT - Surface Mount Technology  
- **Opis**: komponenty montowane na powierzchni PCB
- **Zalety**: miniaturyzacja, automatyzacja, lepsza wydajność przy wysokich częstotliwościach
- **Wady**: trudniejsza naprawa, wymaga specjalnego sprzętu
- **Zastosowanie**: produkcja masowa, układy kompaktowe

## 🔧 Komponenty pasywne

### Rezystory

#### Rodzaje
- **Carbon film**: tanie, podstawowe zastosowania
- **Metal film**: większa precyzja, lepszy współczynnik temperaturowy
- **Wirewound**: wysokie moce, precyzyjne wartości
- **SMD thick/thin film**: powierzchniowe, kompaktowe

#### Oznaczenia wartości
```
Kod kolorowy (THT):
Brązowy-Czarny-Czerwony-Złoty = 10 x 100 = 1kΩ ±5%

Kod numeryczny (SMD):
103 = 10 x 10³ = 10kΩ
472 = 47 x 10² = 4.7kΩ
```

#### Parametry kluczowe
- **Wartość nominalna**: 1Ω do 10MΩ+
- **Tolerancja**: ±1%, ±5%, ±10%
- **Moc**: 1/8W do 100W+
- **Współczynnik temperaturowy**: ppm/°C

#### Popularne obudowy SMD
- **0603** (1.6×0.8mm): uniwersalne
- **0805** (2.0×1.25mm): łatwsze w montażu ręcznym
- **1206** (3.2×1.6mm): większe moce
- **2512** (6.4×3.2mm): wysokie moce

### Kondensatory

#### Rodzaje dielektryków

##### Ceramiczne (MLCC)
- **C0G/NP0**: stabilne, audio, timing
- **X7R**: uniwersalne, ogólne zastosowania  
- **Y5V**: wysokie pojemności, zasilanie

##### Elektrolityczne
- **Aluminiowe**: zasilanie, filtrowanie
- **Tantalowe**: kompaktowe, stabilne
- **Polimerowe**: niski ESR, szybkie przejściowe

##### Foliowe
- **Polipropylene**: audio, high-end
- **Polyester**: ogólne zastosowania

#### Parametry kluczowe
- **Pojemność**: 1pF do 100mF+
- **Napięcie robocze**: 6.3V do 1000V+
- **Tolerancja**: ±5%, ±10%, ±20%
- **ESR**: equivalent series resistance
- **Temperatura pracy**: -55°C do +125°C

#### Kody pojemności (ceramiczne)
```
104 = 10 x 10⁴ pF = 100nF = 0.1μF
225 = 22 x 10⁵ pF = 2.2μF
```

### Indukcyjności (Cewki)

#### Rodzaje
- **Air core**: wysokie częstotliwości, RF
- **Ferrite core**: ogólne zastosowania
- **Iron core**: zasilanie, filtry
- **Toroidal**: niski poziom zakłóceń

#### Zastosowania
- **Filtry zasilania**: tłumienie zakłóceń
- **Resonant circuits**: filtry, oscylatory
- **Energy storage**: zasilacze impulsowe
- **EMI suppression**: redukcja zakłóceń

#### Popularne wartości
- **nH range**: 1-100nH dla RF
- **μH range**: 1-1000μH dla zasilania
- **mH range**: filtry audio, transformatory

## 🔌 Komponenty aktywne

### Diody

#### Rodzaje i zastosowania

##### Diody prostownicze
- **1N4007**: 1000V, 1A - uniwersalna
- **Schottky**: niskie napięcie przewodzenia, szybkie
- **Fast recovery**: zasilacze impulsowe

##### Diody sygnałowe  
- **1N4148**: uniwersalna dioda sygnałowa
- **BAT54**: Schottky SMD, switching

##### Diody specjalne
- **Zener**: stabilizacja napięcia
- **LED**: wskaźniki, oświetlenie
- **Photodiodes**: sensory światła

#### Parametry kluczowe
- **Forward voltage** (Vf): typowo 0.7V (Si), 0.3V (Schottky)
- **Reverse voltage**: maksymalne napięcie wsteczne
- **Forward current**: maksymalny prąd przewodzenia
- **Recovery time**: czas przełączania

### Tranzystory

#### Tranzystory bipolarne (BJT)

##### NPN (najpopularniejsze)
- **2N3904**: uniwersalny tranzystor sygnałowy NPN
- **BC547**: europejski odpowiednik 2N3904
- **2N2222**: większa moc, switching

##### PNP
- **2N3906**: komplementarny do 2N3904
- **BC557**: komplementarny do BC547

##### Parametry kluczowe
- **hFE (β)**: współczynnik wzmocnienia prądowego
- **IC max**: maksymalny prąd kolektora
- **VCE max**: maksymalne napięcie kolektor-emiter
- **Power dissipation**: maksymalna moc tracona

#### Tranzystory polowe (FET)

##### MOSFET
- **N-channel enhancement**: najczęściej używane
- **P-channel enhancement**: dla high-side switching
- **Logic level**: włączanie 3.3V/5V sygnałem

##### Popularne MOSFET
- **IRF540N**: 100V, 33A N-channel (THT)
- **BSS138**: low-voltage level shifter
- **AO3401**: -30V, -4A P-channel (SOT-23)

##### Parametry kluczowe
- **VDS**: napięcie drain-source
- **ID**: prąd drain
- **RDS(on)**: opór w stanie włączonym
- **VGS(th)**: napięcie bramki włączenia

## 🔗 Komponenty łączące

### Złącza (Connectors)

#### Rodzaje
- **Pin headers**: 2.54mm pitch, prototyping
- **JST**: kompaktowe złącza zasilania
- **USB**: A, B, C, micro, mini
- **RJ45**: Ethernet
- **SMA/MCX**: RF connections

#### Parametry
- **Pitch**: odstęp między pinami (2.54mm, 1.27mm, 0.5mm)
- **Current rating**: maksymalny prąd
- **Voltage rating**: maksymalne napięcie
- **Mating cycles**: liczba połączeń/rozłączeń

### Przełączniki i przyciski

#### Tact switches
- **6×6mm**: standardowy rozmiar
- **Height variants**: 4.3mm, 5mm, 7mm, 9mm
- **Force**: 160gf, 260gf, 520gf

#### Toggle switches
- **SPST**: Single Pole Single Throw
- **SPDT**: Single Pole Double Throw
- **DPDT**: Double Pole Double Throw

## 🧠 Układy scalone (IC)

### Obudowy (Packages)

#### THT Packages
- **DIP** (Dual In-line Package): 8, 14, 16, 20, 28, 40 pinów
- **TO-220**: regulators, power MOSFETs
- **TO-92**: małe tranzystory, voltage references

#### SMD Packages
- **SOIC** (Small Outline IC): 8, 14, 16, 20, 28 pinów
- **QFP** (Quad Flat Package): 32, 44, 64, 100+ pinów
- **BGA** (Ball Grid Array): wysokiej gęstości
- **SOT-23**: małe IC (3-8 pinów)
- **QFN**: Quad Flat No-leads, termiczny pad

### Popularne familie IC

#### Mikrokontrolery
- **Arduino**: ATmega328P, ATmega32U4
- **ESP32/ESP8266**: WiFi + MCU
- **STM32**: ARM Cortex-M
- **PIC**: Microchip

#### Operational Amplifiers
- **LM358**: dual op-amp, ogólny
- **TL072**: JFET input, audio
- **LM741**: klasyczny single op-amp

#### Regulatory napięcia
- **LM7805**: +5V linear regulator
- **AMS1117**: LDO 3.3V/5V
- **LM2596**: switching step-down

## ⚡ Komponenty mocy

### Diody mocy
- **1N5822**: 40V, 3A Schottky
- **MBR10100**: 100V, 10A Schottky  
- **UF4007**: ultra-fast recovery

### Tranzystory mocy
- **IRF540N**: 100V, 33A N-MOSFET
- **IRFP250N**: 200V, 30A N-MOSFET
- **TIP120**: NPN Darlington, TO-220

### Regulatory mocy
- **LM2596**: 3A switching regulator
- **XL6009**: boost converter
- **LM317**: adjustable linear regulator

## 🎨 Dobór komponentów

### Kryteria wyboru

#### Parametry elektryczne
- Wartości nominalne z marginesem bezpieczeństwa
- Tolerancje odpowiednie do aplikacji
- Parametry dynamiczne (frequency response)

#### Parametry mechaniczne
- Rozmiar i obudowa dopasowane do PCB
- Temperatura pracy
- Vibracje i wstrząsy

#### Parametry ekonomiczne
- Koszt komponentu
- Dostępność (avoid obsolescence)
- Minimum order quantities

### Derating guidelines
- **Napięcie**: używaj 70-80% maksymalnego
- **Prąd**: używaj 70-80% maksymalnego  
- **Moc**: używaj 50-70% maksymalnej
- **Temperatura**: zachowaj margines 20°C

## 📚 Bibliografie komponentów

### Standardowe biblioteki
- **Arduino**: podstawowe komponenty
- **SparkFun**: szerokai gama
- **Adafruit**: popularne breakout boards

### Tworzenie własnych
- Footprint + Symbol + 3D model
- Datasheet-driven design
- Weryfikacja rzeczywistymi komponentami
- → Zobacz [[pcb_biblioteki_komponentow|Biblioteki Komponentów]]

## 🔍 Identyfikacja komponentów

### Oznaczenia standardowe
```
R = Resistor
C = Capacitor  
L = Inductor
D = Diode
Q = Transistor
U/IC = Integrated Circuit
J = Connector
SW = Switch
```

### Reading datasheets
- **Absolute maximum ratings**: nigdy nie przekraczaj
- **Electrical characteristics**: typowe wartości
- **Package information**: wymiary mechaniczne
- **Application circuits**: przykładowe zastosowania

## 🔗 Powiązane tematy
- [[pcb_podstawy|Podstawy PCB]] - podstawowe pojęcia PCB
- [[pcb_schemat_elektryczny|Schemat Elektryczny]] - umieszczanie komponentów w schemacie
- [[pcb_biblioteki_komponentow|Biblioteki Komponentów]] - tworzenie footprintów
- [[pcb_projekt_layoutu|Projekt Layoutu]] - rozmieszczenie komponentów
- [[pcb_montaz_komponenow|Montaż Komponentów]] - technologie montażu
- [[pcb_testowanie_debug|Testowanie i Debug]] - troubleshooting komponentów

---

**🎯 Co dalej?**
Po zapoznaniu się z komponentami, przejdź do [[pcb_schemat_elektryczny|Schematu Elektrycznego]] aby nauczyć się projektować połączenia elektryczne między komponentami.