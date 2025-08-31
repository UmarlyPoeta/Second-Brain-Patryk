# Symbole Graficzne w Schematach

## 🎯 Wprowadzenie

Symbole graficzne to ustandaryzowane reprezentacje komponentów elektronicznych w schematach. Znajomość standardowych symboli jest niezbędna do czytania i projektowania schematów elektrycznych. Ta notatka przedstawia najważniejsze symbole używane w elektronice.

## 📚 Standardy symboli

### Główne standardy
- **IEEE 315** (USA): American National Standard
- **IEC 60617** (International): European/International Standard
- **DIN 40700** (Germany): German standard
- **BS 3939** (UK): British standard

### Różnice między standardami
- **Rezystor**: prostokąt (IEC) vs zygzak (IEEE)
- **Kondensator**: równoległe linie vs curved line
- **Induktor**: prostokątna spirala vs curved coils

## 🔧 Komponenty pasywne

### Rezystory

#### Symbol IEEE (American)
```
     ╭─╮╱╲╱╲╱╲╱─╮
────╱  ╲╱╲╱╲╱╲╱  ╲────
    ╰─╱           ╲─╯
         R
```

#### Symbol IEC (European)
```
    ┌─────────────┐
────┤      R      ├────
    └─────────────┘
```

#### Rodzaje rezystorów
- **Variable resistor**: strzałka przez symbol
- **Potentiometer**: strzałka z boku + trzeci pin
- **Thermistor**: symbol + T
- **LDR**: symbol + światło

### Kondensatory

#### Symbol podstawowy
```
    │  │
────┤  ├────
    │  │
      C
```

#### Kondensator polaryzowany (elektrolityczny)
```
    │  ├─
────┤  │ + ────
    │  │
      C
```

#### Kondensator zmiennej pojemności
```
    │  │
────┤  ├────
    │  │ ╱
      C╱
```

### Indukcyjności (Cewki)

#### Symbol podstawowy
```
    ╭─╴─╴─╴─╴─╮
────╯  ∩∩∩∩∩  ╰────
       L
```

#### Induktor z rdzeniem
```
    ╭─╴─╴─╴─╴─╮
────╯  ∩∩∩∩∩  ╰────
       ║║║
       L
```

#### Transformator
```
    ╭─╴─╴─╮    ╭─╴─╴─╮
────╯ ∩∩∩ ╰────╯ ∩∩∩ ╰────
      ║║        ║║
      L1        L2
```

## ⚡ Komponenty półprzewodnikowe

### Diody

#### Dioda prostownicza
```
    ─────►├─────
         D
```

#### Dioda Zenera
```
    ─────►├┤─────
         Z
```

#### LED
```
    ─────►├──── ╱ ╱
         LED  ╱ ╱
```

#### Photodioda  
```
    ─────►├─────
         PD ╲ ╲
            ╲ ╲
```

#### Dioda Schottky'ego
```
    ─────►├┐─────
         S └
```

### Tranzystory bipolarne

#### NPN
```
        C
        │
    ────├──── B
        │╱
        ▼
        │
        E
```

#### PNP
```
        C
        │
        ▲
    ────├──── B
        │╲
        │
        E
```

#### Darlington NPN
```
        C
        │
        ├─┐
    ────├─┤──── B
        │ │╱
        ▼ ▼
        │
        E
```

### Tranzystory polowe

#### JFET N-channel
```
        D
        │
    ────┤──── G
        │
        │
        S
```

#### MOSFET N-channel Enhancement
```
        D
        │
        ├─┐
    ────┤ │──── G
        ├─┘
        │
        S
```

#### MOSFET P-channel Enhancement
```
        D
        │
        ○
        ├─┐
    ────┤ │──── G
        ├─┘
        │
        S
```

## 🔌 Złącza i interfejsy

### Złącza podstawowe

#### Connector (generic)
```
    ○ ── 1
    ○ ── 2
    ○ ── 3
    ○ ── 4
```

#### Plug & Socket
```
    Plug:           Socket:
    ─── ○           ○ ───
    ─── ○           ○ ───
    ─── ○           ○ ───
```

### Złącza specjalne

#### USB
```
    ┌─────┐
    │ USB │
    │  A  │
    └──┬──┘
       │
    1──┤ VBUS
    2──┤ D-
    3──┤ D+
    4──┤ GND
```

#### RJ45 (Ethernet)
```
    ┌─────────┐
    │ RJ45    │
    │ [::::]  │
    └─┬─┬─┬─┬─┘
      1 2 3 8
```

## 🔘 Przełączniki i przyciski

### Przełączniki mechaniczne

#### SPST (Single Pole Single Throw)
```
    ○ ──┘     ○
```

#### SPDT (Single Pole Double Throw)
```
         ○
        ╱
    ○ ─┘
        ╲
         ○
```

#### DPDT (Double Pole Double Throw)
```
         ○     ○
        ╱      ╱
    ○ ─┘   ○ ─┘
        ╲      ╲
         ○     ○
```

### Przyciski

#### Push button (NO - Normally Open)
```
    ○ ──┐ ╲──── ○
        └─────┘
```

#### Push button (NC - Normally Closed)
```
    ○ ──┤╱──── ○
        └─────┘
```

## 🏭 Układy scalone

### Operational Amplifier
```
       ╲
    +──│ ╲
       │  ├── OUT
    ───│ ╱
       ╱
```

### Logic Gates

#### AND Gate
```
    ─────┐
         │ ╲
    ─────┤  ├── OUT
         │ ╱
    ─────┘
```

#### OR Gate
```
    ───╭─┐
       │  ╲
    ───┤   ├── OUT
       │  ╱
    ───╰─┘
```

#### NOT Gate (Inverter)
```
    ──────►○── OUT
```

#### NAND Gate
```
    ─────┐
         │ ╲
    ─────┤  ├○── OUT
         │ ╱
    ─────┘
```

### Microcontroller (generic)
```
    ┌─────────────┐
    │    MCU      │
    │             │
 P1 ├─ 1      8 ─┤ P8
 P2 ├─ 2      7 ─┤ P7
GND ├─ 3      6 ─┤ VCC
CLK ├─ 4      5 ─┤ RST
    └─────────────┘
```

## 🔋 Zasilanie i masa

### Symbole zasilania

#### VCC/VDD (pozytywne zasilanie)
```
    ────┬──── +5V
        │
       ╱│╲
      ╱ │ ╲
     ╱  │  ╲
        │
```

#### Masa (Ground)
```
    ────┬──── GND
        │
        ├──
        ├───
        ├────
        │
```

#### Masa analogowa/cyfrowa
```
    ────┬──── AGND
        │
       ╱▲╲
      ╱ │ ╲
     ╱  │  ╲
        │
        
    ────┬──── DGND
        │
       ■■■
       ■■■
       ■■■
```

### Baterie

#### Single cell
```
    ────┤├+─── +
         │
         │
    ─────┴──── -
```

#### Multi-cell battery
```
    ────┤├+┤├+─── +
          │  │
          │  │
    ──────┴──┴──── -
```

## 📡 Sygnały i źródła

### Źródła napięcia

#### DC Voltage Source
```
       +
    ───(+)───
       (-)
       -
```

#### AC Voltage Source
```
    ───(∼)───
```

### Generatory sygnałów

#### Function Generator
```
    ┌─────────┐
    │   ∿∿∿   │
    │  FUNC   │
    └────┬────┘
         │
    ─────┴─────
```

#### Crystal Oscillator
```
    ┌─────────┐
    │ ◊   ◊   │
    │  XTAL   │
    └──┬───┬──┘
       │   │
```

## 🎛️ Instrumenty pomiarowe

### Multimetr
```
    ┌─────────┐
    │    V    │
    │  ─ A ─  │
    │   Ω     │
    └──┬───┬──┘
       │   │
```

### Oscyloskop
```
    ┌─────────┐
    │  ╭─╮    │
    │ ╱   ╲   │
    │╱     ╲  │
    └───┬─────┘
        │
```

## 🎯 Zasady używania symboli

### Standardizacja
- **Consistent library**: używaj jednego standardu w projekcie
- **Company standards**: trzymaj się firmowych bibliotek
- **Documentation**: dokumentuj nietypowe symbole

### Orientacja
- **Inputs left**: wejścia z lewej strony
- **Outputs right**: wyjścia z prawej strony  
- **Power up**: zasilanie u góry
- **Ground down**: masa na dole

### Labeling
- **Reference designators**: R1, C1, U1
- **Values**: 10kΩ, 100nF, LM358
- **Pin numbers**: widoczne dla IC
- **Net names**: sygnały opisane

### Czytelność
- **Symbol size**: odpowiedni do złożoności
- **Text size**: czytelny po wydrukowaniu
- **Spacing**: adequate space between components
- **Alignment**: symbols aligned to grid

## 🛠️ Tworzenie custom symboli

### Design guidelines
- **Pin placement**: logiczny układ pinów
- **Symbol shape**: reprezentatywny dla funkcji
- **Text placement**: nie zakrywa połączeń
- **Pin types**: prawidłowo zdefiniowane (input/output/power)

### Pin electrical types
- **Input**: sygnały wejściowe
- **Output**: sygnały wyjściowe
- **Bidirectional**: I/O pins
- **Power**: zasilanie
- **Passive**: komponenty pasywne

## 🔗 Powiązane tematy
- [[pcb_schemat_elektryczny|Schemat Elektryczny]] - projektowanie schematów
- [[pcb_komponenty_elektroniczne|Komponenty Elektroniczne]] - fizyczne komponenty
- [[pcb_biblioteki_komponentow|Biblioteki Komponentów]] - zarządzanie symbolami
- [[pcb_narzedzia_kicad|KiCad]] - tworzenie symboli w KiCad
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - standardy projektowe

---

**🎯 Co dalej?**
Po zapoznaniu się z symbolami, przejdź do [[pcb_biblioteki_komponentow|Bibliotek Komponentów]] aby nauczyć się zarządzać symbolami i footprintami, lub do [[pcb_projekt_layoutu|Projektu Layoutu]] aby zacząć przekształcać symbole w fizyczny layout.