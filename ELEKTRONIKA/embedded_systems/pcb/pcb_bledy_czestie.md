# Częste Błędy w Projektowaniu PCB

## 🎯 Wprowadzenie

Projektowanie PCB to proces pełen potencjalnych pułapek. Nawet doświadczeni projektanci mogą popełnić błędy, które prowadzą do niepoprawnego działania układu, problemów z produkcją lub zwiększonych kosztów. Ta notatka prezentuje najczęstsze błędy i sposoby ich uniknięcia.

## ⚡ Błędy elektryczne

### 1. Problemy z zasilaniem

#### Nieodpowiednie ścieżki zasilania
```
❌ Błąd:
VCC ──────0.1mm──────► MCU (5V, 500mA)

✅ Poprawnie:
VCC ──────1.2mm──────► MCU (5V, 500mA)
```

**Problem**: Za wąskie ścieżki zasilania powodują spadek napięcia
**Skutki**: Nieprawidłowe działanie, reset układu, przegrzewanie
**Rozwiązanie**: Oblicz szerokość ścieżki na podstawie prądu

#### Brak kondensatorów odsprzęgających
```
❌ Błąd:
VCC ──────────────────► MCU
                       (brak kondensatorów)

✅ Poprawnie:  
VCC ──┬── 100µF ──┬───► MCU
      └── 100nF ──┘
```

**Problem**: Zakłócenia na liniach zasilania
**Skutki**: Niestabilne działanie, błędy komunikacji
**Rozwiązanie**: 100nF ceramic + bulk electrolytic przy każdym IC

#### Nieprawidłowe uziemienie
```
❌ Błąd: Ground loops
Digital GND ──┬──── Analog GND
              │
              └──── Power GND

✅ Poprawnie: Star ground  
        ┌─── Digital GND
GND ────┼─── Analog GND
        └─── Power GND
```

### 2. Błędy sygnałowe

#### Nieustalony stan logiczny
```
❌ Błąd:
MCU_PIN ──────────────► Button ──── GND
(pin floating when button open)

✅ Poprawnie:
VCC ──┤10kΩ├── MCU_PIN ──► Button ──── GND
      (pull-up resistor)
```

**Problem**: Pin w stanie nieokreślonym
**Skutki**: Przypadkowe przełączenia, nieprzewidywalne zachowanie
**Rozwiązanie**: Pull-up/pull-down resistors

#### Brak terminacji linii wysokiej częstotliwości
```
❌ Błąd:
MCU ──────────────long trace──────────────► Load

✅ Poprawnie:
MCU ─────trace─────┤50Ω├─► Load
                          └─► GND
```

### 3. EMI/EMC problemy

#### Długie ścieżki zegara
```
❌ Błąd:
Crystal ──────long meandering trace──────► MCU

✅ Poprawnie:
Crystal ──short direct trace──► MCU
```

**Problem**: Clock sygnały jako anteny
**Skutki**: Promieniowanie EMI, problemy z certyfikacją
**Rozwiązanie**: Minimalna długość, ground plane pod trasą

## 🏗️ Błędy mechaniczne

### 1. Problemy z komponentami

#### Niewłaściwy footprint
```
❌ Błąd: SOIC-8 symbol → DIP-8 footprint
❌ Błąd: 0805 resistor → 0603 footprint
❌ Błąd: Pin 1 orientation mismatch
```

**Problem**: Komponent nie pasuje do płytki
**Skutki**: Niemożność montażu, błędne połączenia
**Rozwiązanie**: Dokładna weryfikacja datasheet vs footprint

#### Via in pad (dla THT)
```
❌ Błąd:
THT component pad with via inside

✅ Poprawnie:
Via offset from THT pads
```

**Problem**: Solder wciągana do via podczas lutowania
**Skutki**: Słabe połączenia lutownicze, zimne lutowie
**Rozwiązanie**: Via poza padami THT

### 2. Problemy z rozmiarami

#### Zbyt małe spacing
```
❌ Błąd:
Track ▓▓ Track (0.05mm spacing)

✅ Poprawnie:
Track ▓▓▓▓▓ Track (0.15mm+ spacing)
```

**Problem**: Poniżej możliwości producenta
**Skutki**: Zwarcia, wysoki koszt produkcji
**Rozwiązanie**: Design Rules Check z parametrami producenta

#### Nieodpowiednia grubość płytki
```
❌ Błędy:
- 0.6mm PCB with heavy components
- 3.2mm PCB for flexible application
- Wrong aspect ratio for vias (depth:diameter >10:1)
```

### 3. Thermal management

#### Brak odprowadzania ciepła
```
❌ Błąd:
High power IC on standard footprint
No thermal vias or heat spreading

✅ Poprawnie:
Thermal pad with multiple vias to ground plane
Large copper areas for heat spreading
```

## 📐 Błędy layoutu

### 1. Routing problems

#### Acid traps
```
❌ Błąd: Acute angles
Track ╲
      ╱ Track (sharp angle <90°)

✅ Poprawnie: Obtuse angles  
Track ╲
       ╲ Track (>90° or rounded)
```

**Problem**: Trawienie niecałkowite w ostrych kątach
**Skutki**: Zwarcia, niewiarygodne połączenia
**Rozwiązanie**: Unikaj kątów ostrych, używaj 45° lub łuków

#### Impedancja niekontrolowana
```
❌ Błąd:
High-speed signal with varying trace width
Different distances to reference plane

✅ Poprawnie:
Constant width, consistent stackup
Controlled impedance design
```

### 2. Layer stackup issues

#### Asymmetryczne stackup
```
❌ Błąd (warpage):
Layer 1: 35µm Cu
Core:    1.6mm  
Layer 2: 70µm Cu (unbalanced)

✅ Poprawnie:
Layer 1: 35µm Cu
Core:    1.6mm
Layer 2: 35µm Cu (balanced)
```

#### Brak reference planes
```
❌ Błąd:
Signal layer without adjacent ground/power plane

✅ Poprawnie:
Signal layer sandwiched between reference planes
```

## 🔧 Błędy w narzędziach CAD

### 1. Library errors

#### Niepoprawne pin assignments
```
❌ Błąd:
Schematic: MCU Pin 1 = VCC
Footprint: MCU Pin 1 = GND
(pin numbering mismatch)
```

**Problem**: Symbol nie pasuje do footprinta
**Skutki**: Katastrofalne błędy połączeń
**Rozwiązanie**: Cross-check symbol vs datasheet vs footprint

#### Błędne electrical types
```
❌ Błąd:
Input pin type = Power Output
Output pin = Input
```

### 2. Design rule setup

#### Nieprawidłowe constraints
```
❌ Błędne design rules:
Minimum trace width: 0.01mm (unrealistic)
Maximum via drill: 0.1mm (too small for current)
Clearance: 0.05mm (below fab capability)
```

### 3. Export errors

#### Niepełne pliki Gerber
```
❌ Missing layers:
- Drill files not generated
- Solder mask layers missing  
- No board outline
- Assembly drawings absent

✅ Complete set:
- All copper layers
- Solder mask (top/bottom)
- Silkscreen (top/bottom)  
- Drill files (PTH + NPTH)
- Pick & place files
- Assembly drawings
```

## 🧪 Błędy w testowaniu

### 1. Brak test points

#### Niedostępne sygnały
```
❌ Błąd:
Critical signals buried in BGA
No test access to power rails
Debug pins not broken out

✅ Poprawnie:
Test points on critical nets
Debug connector for programming
Probe access to key signals
```

### 2. Niewłaściwe debug provisions

#### Brak możliwości debugowania
```
❌ Błąd:
No JTAG connector
No UART debug pins  
No LED indicators
No jumpers for configuration

✅ Poprawnie:
Programming/debug interface
Status LEDs
Configuration options
```

## 💰 Błędy ekonomiczne

### 1. Over-engineering

#### Niepotrzebne features
```
❌ Nadmiarowe:
- 8-layer PCB for simple project
- Controlled impedance dla low-speed
- Expensive materials bez potrzeby
- Gold plating dla internal connections

✅ Optymalne:
- Minimum viable layer count
- Standard materials when adequate
- Cost-effective surface finish
```

### 2. Panel optimization

#### Niewykorzystany panel
```
❌ Błąd:
85mm × 85mm PCB on 100mm × 100mm panel
(poor utilization, high cost per piece)

✅ Better:
4× 42mm × 42mm PCBs on same panel
(better utilization, lower unit cost)
```

## 🏭 Błędy związane z produkcją

### 1. DFM violations

#### Nieprodukowalne features
```
❌ Problematyczne:
- 0.05mm vias (specialized process)
- Aspect ratio >8:1 dla via
- Track width <0.1mm (higher yield loss)
- Complex board shapes (routing cost)
```

### 2. Assembly issues

#### Problemy montażowe
```
❌ Błędy:
- Components too close for pick & place
- No fiducials for assembly machines  
- Mixed THT/SMD orientation
- No polarity markings on PCB

✅ Dobre praktyki:
- Adequate component spacing
- Fiducial markers in corners
- Consistent component orientation
- Clear polarity indicators
```

## 🛡️ Jak unikać błędów

### 1. Design reviews

#### Systematyczne przeglądy
```
Schematic review:
☐ All connections verified
☐ Power calculations checked
☐ Component values confirmed
☐ Net names consistent

Layout review:  
☐ DRC clean
☐ Component orientations
☐ Thermal considerations
☐ Test access provided

Manufacturing review:
☐ DFM compliant
☐ Assembly considerations
☐ Cost optimization
☐ Lead time realistic
```

### 2. Prototyping strategy

#### Iterative development
```
Phase 1: Proof of concept
- Basic functionality
- Key components only
- Hand assembly friendly

Phase 2: Engineering prototype  
- Full functionality
- Production-like components
- Basic testing

Phase 3: Production prototype
- Final specifications
- Production processes
- Full qualification
```

### 3. Checklists i automation

#### Pre-production checklist
```
Design verification:
☐ Schematic vs layout netlist match
☐ Component footprints verified
☐ Power integrity analysis
☐ Signal integrity review

Manufacturing readiness:
☐ Gerber files complete
☐ Pick & place files accurate
☐ Bill of materials final
☐ Assembly drawings complete

Quality assurance:
☐ Design rules compliant
☐ Test procedures defined
☐ Acceptance criteria set
☐ Backup plan prepared
```

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - sprawdzone metody
- [[pcb_testowanie_debug|Testowanie i Debug]] - identyfikacja problemów
- [[pcb_produkcja_wytwarzanie|Produkcja PCB]] - unikanie błędów produkcyjnych
- [[pcb_projekt_layoutu|Projekt Layoutu]] - właściwe praktyki layoutu
- [[pcb_narzedzia_kicad|KiCad]] - unikanie błędów w narzędziach

---

**🎯 Co dalej?**
Po zapoznaniu się z częstymi błędami, przejdź do [[pcb_najlepsze_praktyki|Najlepszych Praktyk]] aby poznać sprawdzone metody projektowania, lub [[pcb_testowanie_debug|Testowania i Debug]] aby nauczyć się identyfikować i naprawiać problemy.