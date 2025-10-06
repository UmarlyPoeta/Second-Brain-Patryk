# KiCad - Narzędzie do Projektowania PCB

## 🎯 Wprowadzenie

KiCad to kompletny, darmowy i open-source pakiet narzędzi do projektowania elektroniki. Składa się z edytora schematów, projektanta PCB, przeglądarki bibliotek, kalkulatora ścieżek i 3D viewer. To idealne narzędzie dla początkujących uczących się projektowania PCB.

## 📦 Komponenty KiCad

### Główne aplikacje

#### KiCad Project Manager
- **Centrum kontrolne**: zarządzanie projektami
- **Pliki projektu**: .pro, .kicad_pro  
- **Integracja**: łączy wszystkie narzędzia
- **Backup**: automatyczne kopie zapasowe

#### Eeschema (Schematic Editor)
- **Tworzenie schematów**: electrical design entry
- **Symbol libraries**: biblioteki komponentów
- **ERC**: Electrical Rules Check
- **Netlist generation**: export do PCB

#### Pcbnew (PCB Editor)  
- **Layout design**: projektowanie PCB
- **Footprint libraries**: biblioteki obudów
- **DRC**: Design Rules Check
- **Gerber export**: pliki produkcyjne

#### Dodatkowe narzędzia
- **3D Viewer**: wizualizacja 3D PCB
- **GerbView**: podgląd plików Gerber
- **Bitmap2Component**: konwersja grafik
- **PCB Calculator**: kalkulatory projektowe

## 🚀 Pierwsze kroki

### Instalacja

#### Download i instalacja
1. **Oficjalna strona**: https://kicad.org/download/
2. **Stable release**: najnowsza stabilna wersja
3. **Libraries**: instaluj wszystkie biblioteki
4. **Platform**: Windows, macOS, Linux

#### Pierwsza konfiguracja
```
Preferences → Configure Paths:
KICAD_SYMBOL_DIR - ścieżka do symboli
KICAD_FOOTPRINT_DIR - ścieżka do footprintów
KICAD_3DMODEL_DIR - ścieżka do modeli 3D
```

### Nowy projekt

#### Tworzenie projektu
1. **File → New → Project**
2. **Wybierz lokalizację**: dedykowany folder
3. **Nazwa projektu**: opisowa nazwa
4. **Template**: pusty lub z template

#### Struktura plików projektu
```
MojProjekt/
├── MojProjekt.kicad_pro    # Project file  
├── MojProjekt.kicad_sch    # Schematic
├── MojProjekt.kicad_pcb    # PCB layout
├── fp-lib-table           # Footprint libraries
├── sym-lib-table          # Symbol libraries
└── gerbers/              # Output files
```

## ⚡ Projektowanie schematów

### Podstawy Eeschema

#### Interface
```
Toolbar po lewej:
- Select tool
- Place symbol  
- Place power port
- Place wire
- Place bus
- Place junction
- Place label
```

#### Skróty klawiszowe
```
A - Add symbol
P - Add power symbol
W - Place wire  
L - Place label
R - Rotate component
M - Move component
C - Copy component
Del - Delete
```

### Dodawanie komponentów

#### Placement workflow
1. **Naciśnij 'A'**: Add Symbol dialog
2. **Wpisz nazwę**: np. "LM358", "arduino"
3. **Wybierz z listy**: dokładny symbol
4. **Umieść na schemacie**: kliknij lokalizację
5. **Ustaw wartość**: double-click na symbol

#### Popularne komponenty
```
Resistor: R, R_Small
Capacitor: C, C_Small  
LED: LED
Connector: Conn_01x02, Conn_01x04
MCU: MCU_Module:Arduino_UNO_R3
OpAmp: Amplifier_Operational:LM358
```

### Łączenie elementów

#### Wires (przewody)
- **Place wire**: naciśnij 'W'
- **Connection**: wire kończy się na pinie
- **Junction**: kropka na skrzyżowaniu = połączenie
- **No connection**: X na nieużywanym pinie

#### Labels i global labels
```
Label: lokalna nazwa w obrębie sheet
Global label: nazwa globalna w projekcie
Hierarchical label: dla hierarchical sheets
```

#### Power symbols
- **VCC, +5V, +3V3**: positive supply
- **GND**: ground connection
- **VDD, VEE**: różne konwencje zasilania

### Hierarchical design

#### Multiple sheets
1. **Place hierarchical sheet**: prostokąt na schemacie
2. **Create new sheet**: nowy plik .kicad_sch
3. **Hierarchical pins**: połączenia między sheets
4. **Navigation**: Alt+click na sheet

#### Benefits
- **Organization**: podział na moduły funkcjonalne
- **Reusability**: moduły w różnych projektach
- **Collaboration**: różne osoby = różne sheets

## 🎨 Projektowanie PCB

### Import do Pcbnew

#### Netlist workflow (starszy)
1. **Generate netlist**: Tools → Generate Netlist
2. **Export**: save .net file
3. **Import w Pcbnew**: Tools → Load Netlist

#### Modern workflow (update PCB)
1. **Tools → Update PCB from Schematic** (F8)
2. **Automatic matching**: components matched by reference
3. **Update changes**: nowe komponenty, usunięte nets

### Board setup

#### Page settings
- **Board size**: custom size lub standard
- **Title block**: informacje o projekcie
- **Revision**: tracking wersji

#### Design rules
```
Net Classes:
Default: 0.25mm width, 0.2mm clearance
Power: 0.5mm width, 0.2mm clearance  
Signal: 0.2mm width, 0.15mm clearance
```

#### Stackup (4-layer example)
```
Layer 1: F.Cu (Signal, 35μm)
Layer 2: In1.Cu (GND, 35μm)  
Layer 3: In2.Cu (Power, 35μm)
Layer 4: B.Cu (Signal, 35μm)
Total thickness: 1.6mm
```

### Placement komponentów

#### Placement workflow  
1. **All components**: import all footprints
2. **Initial placement**: Auto-place lub manual
3. **Functional grouping**: związane komponenty razem
4. **Optimize**: iteracyjne poprawki

#### Placement guidelines
- **MCU central**: mikrokontroler w centrum
- **Power input**: przy krawędzi
- **High-speed**: komponenty blisko siebie
- **Analog/digital**: separation

### Routing

#### Interactive router
1. **Route tracks**: naciśnij 'X' lub menu
2. **Select net**: kliknij na pad
3. **Route path**: prowadź ścieżkę do celu
4. **Layer switching**: 'V' switch via
5. **Finish**: double-click na target pad

#### Advanced routing
- **Differential pairs**: Tools → Route Differential Pair
- **Length tuning**: Tools → Tune Track Length
- **Push & Shove**: automatic obstacle avoidance

## 📚 Biblioteki w KiCad

### Symbol libraries

#### Tworzenie symboli
1. **Symbol Editor**: Tools → Symbol Editor
2. **New library**: File → New Library  
3. **New symbol**: File → New Symbol
4. **Draw symbol**: Place pins, graphic lines
5. **Properties**: set electrical type, pin names

#### Pin electrical types
```
Input: receives signals
Output: drives signals
Bidirectional: I/O pins  
Power input: VCC, VDD
Power output: voltage regulators
Passive: R, L, C components
```

### Footprint libraries

#### Tworzenie footprintów
1. **Footprint Editor**: Tools → Footprint Editor
2. **New library**: File → New Library
3. **New footprint**: File → New Footprint  
4. **Draw footprint**: Place pads, courtyard
5. **3D settings**: assign 3D model

#### Footprint elements
- **Pads**: miejsca lutowania
- **Courtyard**: obszar komponentu
- **Fab layer**: assembly drawing
- **Silkscreen**: visible markings

### Zarządzanie bibliotekami

#### Library tables
```
Symbol Library Table:
Nickname | Library Path | Plugin Type
arduino  | ${KICAD_SYMBOL_DIR}/MCU_Module.kicad_sym | KiCad

Footprint Library Table:  
Nickname | Library Path | Plugin Type
arduino  | ${KICAD_FOOTPRINT_DIR}/Module.pretty | KiCad
```

#### Custom libraries
1. **Create library folder**: MyLibrary.pretty
2. **Add to table**: Preferences → Manage Footprint Libraries
3. **Verify path**: test library access

## 🏭 Produkcja i export

### Design Rule Check (DRC)

#### Run DRC
1. **Inspect → Design Rules Checker**
2. **Run DRC**: check all violations
3. **Review errors**: fix critical violations
4. **Warnings**: evaluate if acceptable

#### Common DRC errors
- **Clearance**: tracks too close
- **Via size**: drill too small
- **Copper area**: isolated copper  
- **Connectivity**: unconnected nets

### Gerber export

#### Plot settings
1. **File → Plot**
2. **Select layers**: F.Cu, B.Cu, F.Mask, B.Mask, etc.
3. **Output directory**: gerbers/
4. **Format**: Gerber X2 format
5. **Options**: plot reference, value

#### Standard gerber set
```
Layers to export:
- F.Cu, B.Cu (copper layers)
- F.Mask, B.Mask (solder mask)  
- F.Silkscreen, B.Silkscreen
- Edge.Cuts (board outline)
- F.Fab, B.Fab (assembly)
```

### Drill files

#### Generate drill files
1. **File → Fabrication Outputs → Drill Files**
2. **Output directory**: same as gerbers
3. **Format**: Excellon format
4. **Units**: millimeters
5. **Generate**: create drill files

### Pick & place files

#### Assembly export
1. **File → Fabrication Outputs → Component Placement**
2. **Format**: CSV format  
3. **Units**: millimeters
4. **Include**: only SMD components
5. **Output**: .csv file for assembly

## 🎯 Wskazówki i tricks

### Workflow optimization

#### Project templates
- **Create templates**: save common project structures  
- **Standard components**: frequently used parts
- **Design rules**: company/personal standards
- **Library setup**: pre-configured libraries

#### Backup strategy
```
Version control:
git init
git add *.kicad_*
git commit -m "Initial PCB design"

Cloud backup:
- Dropbox, Google Drive
- Automated sync
- Version history
```

### Keyboard shortcuts

#### Essential shortcuts
```
Schematic (Eeschema):
A - Add symbol
W - Wire  
L - Label
R - Rotate
M - Move

PCB (Pcbnew):
X - Route track
V - Add via
M - Move
R - Rotate  
F - Flip to other side
```

### Tips dla początkujących

#### Schematic best practices
- **One function per sheet**: for complex designs
- **Clear labels**: descriptive net names
- **Power symbols**: use proper power symbols
- **No-connect**: mark unused pins with X

#### PCB best practices  
- **Ground plane**: use copper pour for ground
- **Track width**: calculate for current requirements
- **Via placement**: minimize usage
- **Silkscreen**: clear component labels

### Troubleshooting

#### Common problems
```
Problem: Component not updating from schematic
Solution: Tools → Update PCB from Schematic

Problem: DRC clearance violations  
Solution: Increase track spacing or reduce width

Problem: Missing footprints
Solution: Check footprint library table paths

Problem: Gerber files incomplete
Solution: Verify all required layers selected
```

## 🔗 Zasoby i społeczność

### Oficjalne zasoby
- **Documentation**: https://docs.kicad.org/
- **Forum**: https://forum.kicad.info/
- **Libraries**: https://kicad.github.io/
- **YouTube**: oficjalne tutorials

### Społeczność
- **Reddit**: r/KiCad
- **Discord**: KiCad Community
- **GitHub**: open source contributions
- **Local groups**: meetups i warsztaty

### Learning resources
- **Getting Started in KiCad**: official guide
- **Contextual Electronics**: advanced tutorials  
- **Phil's Lab**: PCB design videos
- **Robert Feranec**: professional PCB design

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_schemat_elektryczny|Schemat Elektryczny]] - projektowanie schematów
- [[pcb_biblioteki_komponentow|Biblioteki Komponentów]] - zarządzanie bibliotekami
- [[pcb_projekt_layoutu|Projekt Layoutu]] - proces layoutu
- [[pcb_produkcja_wytwarzanie|Produkcja PCB]] - przygotowanie do produkcji
- [[pcb_projekty_praktyczne|Projekty Praktyczne]] - przykłady w KiCad

---

**🎯 Co dalej?**
Po opanowaniu KiCad, spróbuj [[pcb_projekty_praktyczne|Projektów Praktycznych]] aby zastosować zdobytą wiedzę w rzeczywistych projektach, lub przejdź do [[pcb_produkcja_wytwarzanie|Produkcji PCB]] aby nauczyć się przygotowywać pliki do wytwarzania.