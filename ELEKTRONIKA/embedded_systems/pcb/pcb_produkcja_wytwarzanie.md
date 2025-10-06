# Produkcja PCB - Proces Wytwarzania

## 🎯 Wprowadzenie

Produkcja PCB to złożony proces technologiczny przekształcający projekt cyfrowy w fizyczną płytkę drukowaną. Zrozumienie tego procesu pomaga projektantom tworzyć PCB, które są nie tylko funkcjonalne, ale też efektywne i ekonomiczne w produkcji.

## 🏭 Przegląd procesu produkcji

### Główne etapy

#### 1. Przygotowanie danych
- **CAD data**: pliki Gerber, drill files
- **Specification**: stackup, materials, finishing
- **Engineering questions**: clarification z producentem
- **DFM check**: Design for Manufacturing analysis

#### 2. Panelization
- **Individual PCBs**: umieszczenie na panelu
- **Tooling holes**: referencje produkcyjne
- **Breakaway tabs**: łączenie płytek
- **Fiducials**: markery dla maszyn

#### 3. Material preparation
- **Substrate cutting**: cięcie FR-4 na rozmiar
- **Copper cleaning**: przygotowanie powierzchni
- **Laminate preparation**: układanie warstw
- **Quality inspection**: kontrola materiałów

#### 4. Drilling
- **Via drilling**: otwory między warstwami
- **Through holes**: otwory komponentów
- **Tool selection**: odpowiednie wiertła
- **Plating preparation**: przygotowanie do platowania

#### 5. Plating
- **Copper plating**: powlekanie otworów
- **Surface finishing**: HASL, ENIG, OSP
- **Thickness control**: kontrola grubości
- **Quality testing**: testy elektryczne

#### 6. Imaging i etching
- **Photoresist**: aplikacja warstwy światłoczułej
- **Exposure**: naświetlanie przez maski
- **Development**: wywoływanie obrazu
- **Etching**: trawienie nadmiaru miedzi

#### 7. Final processing
- **Solder mask**: aplikacja maski lutowniczej
- **Silkscreen**: nadruk opisów
- **Surface finish**: ostateczne wykończenie
- **Testing**: testy elektryczne i wizualne

## 📊 Materiały PCB

### Substrate materials

#### FR-4 (Fire Retardant 4)
```
Composition: Fiberglass + Epoxy resin
Thickness: 0.1mm - 3.2mm standard
Temperature rating: 130°C continuous
Glass transition (Tg): 130-180°C
Decomposition (Td): >300°C
Dielectric constant: 4.3-4.7 @ 1MHz
```

**Charakterystyka:**
- **Standard**: 95% wszystkich PCB
- **Cost effective**: dobry stosunek jakość/cena
- **Mechanical strength**: wysoka wytrzymałość
- **Electrical**: dobre właściwości izolacyjne

#### High-performance materials
```
Rogers RO4003C:
- Dielectric constant: 3.38 ± 0.05
- Loss tangent: 0.0027 @ 10GHz
- Application: high-frequency RF

Polyimide (PI):
- Temperature: -269°C to +400°C
- Flexibility: flex PCB applications
- Chemical resistance: excellent

Aluminum core:
- Thermal conductivity: 1-8 W/mK
- Application: LED, power electronics
- Heat spreading: superior to FR-4
```

### Copper specifications

#### Copper weights
```
Weight [oz] | Thickness [μm] | Application
0.5         | 17.5          | Fine pitch, HDI
1           | 35            | Standard PCB
2           | 70            | Power, thermal
3+          | 105+          | High current
```

#### Copper purity
- **Electrodeposited**: 99.9%+ purity
- **Rolled**: mechanically superior
- **Annealed**: stress relief
- **Profile**: matte vs shiny finish

## ⚙️ Procesy produkcyjne

### Subtractive process (standard)

#### Workflow
1. **Start**: copper-clad substrate
2. **Pattern**: photoresist + etching
3. **Result**: trace pattern remains
4. **Advantage**: mature, cost-effective
5. **Limitation**: minimum feature size

```
Before etching:
████████████  ← Copper
▓▓▓▓▓▓▓▓▓▓▓▓  ← Photoresist
████████████  ← Substrate

After etching:
██  ████  ██  ← Remaining copper
▓▓▓▓▓▓▓▓▓▓▓▓  ← Substrate
```

### Additive process

#### Semi-additive
1. **Thin seed layer**: electroless copper
2. **Pattern plating**: build up tracks
3. **Etching**: remove seed layer
4. **Advantage**: better fine pitch capability

#### Full additive
1. **Catalyzed substrate**: no initial copper
2. **Direct plating**: copper only where needed
3. **No etching**: no waste
4. **Advantage**: environmental, precision

### HDI (High Density Interconnect)

#### Via formation
```
Laser drilling:
- CO2 laser: dielectric materials
- UV laser: polyimide, thin materials
- Precision: ±25μm typical
- Speed: 1000+ holes/second

Sequential lamination:
- Build up layer by layer
- Blind/buried vias
- Higher layer count
- Miniaturization
```

#### Applications
- **Mobile phones**: space constraints
- **BGA packages**: fine pitch requirements
- **Medical devices**: miniaturization
- **Aerospace**: weight reduction

## 🔧 Manufacturing processes

### Drilling

#### Mechanical drilling
```
Process parameters:
- Speed: 20,000-200,000 RPM
- Feed rate: 0.1-1.0mm/rev
- Tool life: 1000-10,000 holes
- Precision: ±0.05mm typical
```

**Advantages:**
- **High throughput**: fast for large holes
- **Cost effective**: standard tooling
- **Quality**: good hole quality

**Limitations:**
- **Tool wear**: frequent changes needed
- **Size range**: limited to drill sizes
- **Aspect ratio**: depth/diameter limits

#### Laser drilling
```
CO2 laser (wavelength 10.6μm):
- Materials: FR-4, polyimide
- Hole size: 0.1-0.6mm
- Quality: tapered holes
- Speed: very fast

UV laser (wavelength 355nm):
- Materials: all PCB materials
- Hole size: 0.025-0.2mm
- Quality: vertical walls
- Precision: ±10μm
```

### Plating processes

#### Electroless copper
```
Process steps:
1. Cleaning: remove contamination
2. Conditioning: surface preparation
3. Activation: palladium catalyst
4. Electroless Cu: chemical deposition
5. Quality: uniform, thin layer
```

**Characteristics:**
- **Thickness**: 0.2-1.0μm typical
- **Coverage**: excellent throwing power
- **Quality**: uniform over complex shapes
- **Function**: seed layer for electrolytic

#### Electrolytic copper
```
Process parameters:
- Current density: 1-5 A/dm²
- Temperature: 20-25°C
- Agitation: air or cathode movement
- Thickness control: time + current
```

**Build-up rates:**
- **Standard**: 25-50μm/hour
- **High speed**: up to 100μm/hour
- **Uniformity**: ±10% across panel
- **Quality**: bright, ductile deposit

### Surface finishes

#### HASL (Hot Air Solder Leveling)
```
Process:
1. Flux application
2. Immersion in solder bath (245°C)
3. Hot air leveling
4. Cleaning

Characteristics:
- Thickness: 1-40μm
- Solderability: excellent
- Cost: lowest
- Planarity: poor for fine pitch
```

#### ENIG (Electroless Nickel Immersion Gold)
```
Process layers:
1. Electroless Nickel: 3-8μm
2. Immersion Gold: 0.05-0.2μm

Advantages:
- Planarity: excellent for BGA
- Shelf life: 12+ months
- Wire bonding: gold bondable
- Multiple reflow: stable

Disadvantages:
- Cost: higher than HASL
- Black pad: potential reliability issue
```

#### OSP (Organic Solderability Preservative)
```
Characteristics:
- Thickness: 0.2-0.5μm organic
- Planarity: excellent
- Cost: low
- Shelf life: 6 months in dry conditions

Limitations:
- Single reflow: degrades with heat
- Testing: limited electrical test
- Handling: sensitive to contamination
```

## 📐 Design for Manufacturing (DFM)

### Minimum feature sizes

#### Standard capabilities
```
Feature                Min Size [mm]
Trace width           0.1
Trace spacing         0.1
Via drill             0.15
Via pad               0.25
Annular ring          0.05
Solder mask opening   0.1
```

#### Advanced capabilities
```
Feature                Min Size [mm]
Trace width           0.075
Trace spacing         0.075
Via drill             0.1
Micro via             0.05
Annular ring          0.025
HDI structures        <0.05
```

### Tolerances

#### Dimensional tolerances
```
Feature              Tolerance
Board dimensions     ±0.1mm
Hole positions       ±0.05mm
Hole sizes          ±0.05mm
Copper thickness     ±20%
Board thickness      ±10%
```

#### Registration tolerances
```
Layer to layer:      ±0.075mm
Solder mask:         ±0.05mm
Silkscreen:          ±0.1mm
Via in pad:          ±0.05mm
```

### Panelization guidelines

#### Panel constraints
```
Minimum panel size:   50×50mm
Maximum panel size:   610×457mm (24"×18")
Panel thickness:      same as PCB
Border requirements:  5mm minimum
```

#### V-scoring
```
V-score angle:        30° or 45°
Remaining thickness:  0.3-0.5mm
Score position:       ±0.1mm
Panel strength:       adequate support
```

#### Tab routing
```
Tab width:           3mm minimum
Tab thickness:       board thickness
Number of tabs:      based on PCB size
Break strength:      controlled force
```

## 🔍 Quality control

### Incoming inspection

#### Material verification
- **Thickness measurement**: micrometer
- **Copper weight**: cross-section
- **Surface quality**: visual inspection
- **Dimension check**: CMM measurement

#### Certificate verification
- **Material certifications**: IPC class
- **Test reports**: electrical, mechanical
- **Traceability**: lot numbers
- **Storage conditions**: humidity, temperature

### In-process testing

#### Electrical testing
```
Continuity test:
- Open circuits: resistance >10MΩ
- Short circuits: resistance <10Ω
- Isolation: >100MΩ @ 500V

Flying probe test:
- High speed testing
- Fine pitch capability
- Program generation from CAD
- Statistical process control
```

#### Dimensional inspection
- **Critical dimensions**: hole sizes, positions
- **Profile measurement**: board warpage
- **Layer registration**: X-ray inspection
- **Cross-sectioning**: internal structure

### Final inspection

#### Visual inspection
```
Criteria (IPC-A-600):
- Solder mask: coverage, adhesion
- Silkscreen: legibility, registration  
- Surface finish: uniformity, defects
- Edge quality: smooth, no delamination
```

#### Functional testing
- **Electrical test**: if test fixtures available
- **Impedance**: controlled impedance verification
- **Microsection**: internal quality
- **Reliability**: thermal cycling, if required

## 📊 Kosztorysowanie

### Factors wpływające na koszt

#### Podstawowe czynniki
```
Board size:          Cost per area
Layer count:         Exponential increase
Quantity:           Economy of scale
Lead time:          Rush charges apply
Complexity:         Feature size, density
```

#### Dodatkowe koszty
- **Tooling**: drill programming, fixtures
- **Testing**: electrical test fixtures
- **Special processes**: controlled impedance
- **Certifications**: IPC class, UL rating
- **Expedite fees**: fast delivery

### Optymalizacja kosztów

#### Design optimization
```
Standard sizes:      Use common panel sizes
Layer count:        Minimize layers needed
Via count:          Reduce drilling time
Feature sizes:      Use standard capabilities
Materials:          Standard FR-4 when possible
```

#### Volume considerations
- **Prototype**: 5-25 pieces, highest per-unit cost
- **Small batch**: 100-1000 pieces, moderate cost
- **Production**: 10,000+ pieces, lowest per-unit cost
- **NRE costs**: amortized over volume

## 🌍 Wybór producenta

### Kryteria wyboru

#### Capabilities
- **Technology**: matches design requirements
- **Capacity**: meets volume needs
- **Quality**: certified processes (ISO, IPC)
- **Lead time**: fits project schedule

#### Geographic considerations
```
Local/Regional:
+ Fast delivery
+ Easy communication
+ Prototyping support
- Higher cost

Asian:
+ Low cost
+ High volume capability
+ Advanced technology
- Longer lead time
- Communication barriers
```

### Populerni producenci

#### Prototype/Small volume
- **JLCPCB**: China, very low cost
- **PCBWay**: China, good quality
- **OSH Park**: USA, community focused
- **Eurocircuits**: Europe, fast delivery

#### Production volume
- **Advanced Circuits**: USA, mil-spec
- **TTM Technologies**: USA, aerospace
- **Multek**: Global, high-end
- **Elextronic**: Multi-location

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_projekt_layoutu|Projekt Layoutu]] - projektowanie przed produkcją
- [[pcb_warstwy_pcb|Warstwy PCB]] - struktura dla produkcji
- [[pcb_narzedzia_kicad|KiCad]] - przygotowanie plików produkcyjnych
- [[pcb_testowanie_debug|Testowanie i Debug]] - po otrzymaniu PCB
- [[pcb_montaz_komponenow|Montaż Komponentów]] - następny krok po produkcji
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - projektowanie dla produkcji

---

**🎯 Co dalej?**
Po zrozumieniu procesu produkcji, przejdź do [[pcb_montaz_komponenow|Montażu Komponentów]] aby poznać następny etap, lub [[pcb_testowanie_debug|Testowania i Debug]] aby nauczyć się weryfikować otrzymane PCB.