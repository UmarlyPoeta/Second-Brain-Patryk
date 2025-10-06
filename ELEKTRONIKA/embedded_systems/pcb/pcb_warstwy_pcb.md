# Warstwy PCB - Struktura Wielowarstwowa

## 🎯 Wprowadzenie

Warstwy PCB to poziome poziomy materiału przewodzącego i izolacyjnego, które tworzą strukturę płytki drukowanej. Zrozumienie architektury warstw jest kluczowe dla projektowania wydajnych i niezawodnych PCB, szczególnie w aplikacjach wysokoczęstotliwościowych i wysokoprądowych.

## 📚 Podstawy struktury warstwowej

### Anatomia PCB

#### Podstawowe elementy
```
Solder Mask (Maska lutownicza)
Copper Layer (Warstwa miedziana)
Substrate/Core (Substrat)
Prepreg (Preimpregnated fiberglass)
Copper Layer (Warstwa miedziana)  
Solder Mask (Maska lutownicza)
```

#### Materiały
- **Substrate (Core)**: FR-4, CEM-1, Rogers
- **Copper**: 17μm (0.5oz), 35μm (1oz), 70μm (2oz)
- **Prepreg**: pre-impregnated fiberglass
- **Solder Mask**: typically green epoxy
- **Silkscreen**: white or black legend

### Numeracja warstw

#### Konwencja numerowania
```
2-layer PCB:
Layer 1 (Top)    - komponenty, sygnały
Layer 2 (Bottom) - sygnały, ground pour

4-layer PCB:
Layer 1 (Top)    - komponenty, sygnały
Layer 2 (Inner)  - Ground plane
Layer 3 (Inner)  - Power plane
Layer 4 (Bottom) - sygnały
```

## 🏗️ Rodzaje PCB według warstw

### 1-layer PCB (Single-sided)
```
Components
    ↓
┌─────────────┐
│ Copper Top  │
├─────────────┤
│   FR-4      │
└─────────────┘
```

**Charakterystyka:**
- **Zastosowanie**: bardzo proste układy, prototypy
- **Koszt**: najniższy
- **Routing**: tylko top layer
- **Ograniczenia**: bardzo ograniczone możliwości

### 2-layer PCB (Double-sided)
```
Components
    ↓
┌─────────────┐
│ Copper Top  │ ← Layer 1
├─────────────┤
│    FR-4     │ ← Core (1.6mm)
├─────────────┤
│Copper Bottom│ ← Layer 2
└─────────────┘
```

**Charakterystyka:**
- **Zastosowanie**: hobbystyczne projekty, proste układy komercyjne
- **Koszt**: niski
- **Routing**: obie strony dostępne
- **Ground**: ground pour na bottom layer

### 4-layer PCB
```
Components
    ↓
┌─────────────┐
│ Signal Top  │ ← Layer 1 (0.035mm Cu)
├─────────────┤
│   Prepreg   │ ← 0.2mm
├─────────────┤  
│Ground Plane │ ← Layer 2 (0.035mm Cu)
├─────────────┤
│    Core     │ ← 1.2mm FR-4
├─────────────┤
│Power Plane  │ ← Layer 3 (0.035mm Cu)
├─────────────┤
│   Prepreg   │ ← 0.2mm
├─────────────┤
│Signal Bottom│ ← Layer 4 (0.035mm Cu)
└─────────────┘
```

**Charakterystyka:**
- **Zastosowanie**: większość projektów komercyjnych
- **Zalety**: dedicated power/ground planes
- **EMI**: significant improvement
- **Koszt**: umiarkowany wzrost

### 6-layer PCB
```
Layer 1: Signal (Top)
Layer 2: Ground Plane
Layer 3: Signal (Inner)
Layer 4: Power Plane
Layer 5: Signal (Inner)
Layer 6: Signal (Bottom)
```

**Charakterystyka:**
- **Zastosowanie**: zaawansowane systemy cyfrowe
- **Routing**: dodatkowe warstwy sygnałowe
- **Power**: multiple power domains
- **Performance**: excellent signal integrity

### 8+ layer PCB
- **High-speed computing**: CPU, GPU boards
- **Telecommunications**: RF equipment
- **Aerospace**: critical applications
- **Cost**: significant increase

## ⚡ Funkcje warstw

### Signal layers (Warstwy sygnałowe)

#### Top layer (Component side)
- **Komponenty**: większość komponentów
- **Routing**: routing sygnałów
- **Test points**: punkty testowe
- **Connectors**: złącza i connectory

#### Bottom layer
- **SMD components**: dodatkowe komponenty
- **Routing**: alternatywne ścieżki
- **Ground pour**: plane'y masy
- **Through-hole**: nóżki komponentów THT

#### Inner signal layers
- **Dedicated routing**: specific signal types
- **High-speed signals**: controlled impedance
- **Differential pairs**: matched pairs
- **Shield layers**: between sensitive signals

### Power/Ground planes

#### Ground planes
- **Reference**: reference dla sygnałów
- **EMI shielding**: ekranowanie przed zakłóceniami
- **Current return**: ścieżki powrotu prądu
- **Thermal**: odprowadzanie ciepła

#### Power planes
- **Power distribution**: rozprowadzanie zasilania
- **Decoupling**: natural decoupling capacitance
- **Multiple voltages**: różne napięcia zasilania
- **Current capacity**: wysokie prądy

## 🎨 Stackup design

### Impedance control

#### Single-ended traces
```
Z₀ = 87/√(εᵣ+1.41) × ln(5.98h/(0.8w+t))

gdzie:
w = trace width
h = height to reference plane  
t = trace thickness
εᵣ = dielectric constant
```

#### Differential pairs
```
Z_diff = 2 × Z₀ × (1 - 0.48e^(-0.96s/h))

gdzie:
s = spacing between traces
h = height to reference plane
```

#### Typical impedances
- **Single-ended**: 50Ω standard
- **Differential**: 90Ω, 100Ω typical
- **High-speed**: matched to IC requirements

### Controlled impedance stackup

#### 4-layer example (1.6mm total)
```
Layer 1: 0.035mm Cu    Signal
Prepreg: 0.21mm        εᵣ=4.3
Layer 2: 0.035mm Cu    Ground  
Core:    1.065mm       εᵣ=4.5
Layer 3: 0.035mm Cu    Power
Prepreg: 0.21mm        εᵣ=4.3
Layer 4: 0.035mm Cu    Signal
```

**Impedances:**
- Layer 1: 50Ω ± 10% (trace width ~0.14mm)
- Layer 4: 50Ω ± 10% (trace width ~0.14mm)

### High-speed stackup

#### 8-layer high-performance
```
L1: Signal        (0.5oz Cu)
L2: Ground        (1oz Cu)
L3: Signal        (0.5oz Cu)
L4: Power         (1oz Cu)
L5: Power         (1oz Cu)
L6: Signal        (0.5oz Cu)  
L7: Ground        (1oz Cu)
L8: Signal        (0.5oz Cu)
```

**Features:**
- **Adjacent ground/power**: good decoupling
- **Signal sandwiching**: controlled impedance
- **Multiple power**: different voltage domains

## 🔌 Via stitching

### Layer interconnection

#### Via types for layer connection
- **Through vias**: all layers
- **Blind vias**: outer to inner
- **Buried vias**: inner to inner only

#### Via stitching applications
```
Power plane to power plane:
- Parallel via connection
- Reduced inductance  
- Current distribution

Ground plane stitching:
- EMI improvement
- Ground loops prevention
- Signal return paths
```

### Stitching patterns
```
Grid pattern:
○ ○ ○ ○ ○
○ ○ ○ ○ ○  
○ ○ ○ ○ ○

Perimeter pattern:
○─────────○
│         │
│  PCB    │
│         │
○─────────○
```

## 📐 Design guidelines

### Layer assignment

#### Signal assignment strategy
```
Layer 1: High-speed digital, critical signals
Layer 2: Ground reference
Layer 3: Power distribution  
Layer 4: Low-speed digital, analog
```

#### Power distribution
```
3.3V domain: Layer 3
5V domain: Split on Layer 3
12V domain: Separate layer or thick traces
GND: Dedicated layers (L2, L6 in 8-layer)
```

### Current carrying capacity

#### Plane current capacity
```
Current density = Current / (Width × Thickness)

Safe limits:
- External layers: 35A/mm² (1oz copper)
- Internal layers: 17.5A/mm² (1oz copper)
- Temperature rise: keep <10°C above ambient
```

#### Via current limits
```
Via size → Current capacity
0.2mm → 1A
0.3mm → 2A  
0.5mm → 4A
Multiple vias in parallel for higher currents
```

## 🛠️ Manufacturing considerations

### Fabrication constraints

#### Minimum features
```
Track width:    0.1mm (4 mil)
Track spacing:  0.1mm (4 mil)
Via size:       0.15mm drill
Via pad:        0.25mm minimum
Annular ring:   0.05mm minimum
```

#### Layer count effects
- **2-layer**: 1-2 day turnaround
- **4-layer**: 3-5 day turnaround
- **6+ layer**: 7-14 day turnaround
- **Cost**: exponential increase with layer count

### Assembly considerations

#### Component placement
- **Top heavy**: most components on top
- **Bottom**: only small, light components
- **Through-hole**: extends through all layers
- **Thermal**: heat-generating components

#### Reflow profiling
- **4-layer**: different thermal mass than 2-layer
- **6+ layer**: requires adjusted reflow profiles
- **Via thermal**: via can conduct heat away
- **Ground planes**: large thermal mass

## 🔍 Layer visualization

### CAD tools visualization

#### Layer colors (typical)
```
Red:     Top signal layer
Blue:    Bottom signal layer  
Green:   Internal ground planes
Magenta: Internal signal layers
Yellow:  Power planes
Cyan:    Mechanical layers
```

#### 3D visualization
- **Transparency**: see through layers
- **Cross-section**: cut view of stackup
- **Via visualization**: connection paths
- **Copper thickness**: visual thickness representation

### Documentation

#### Fabrication drawing
- **Stackup table**: layer by layer specification
- **Material spec**: FR-4 grade, Tg, Td
- **Copper weights**: oz per layer
- **Impedance requirements**: target values ±tolerance

#### Layer assignment table
```
Layer | Type    | Function        | Cu Weight
------|---------|-----------------|----------
  1   | Signal  | Component/Route | 1 oz
  2   | Plane   | Ground         | 1 oz
  3   | Plane   | +3.3V/+5V      | 1 oz  
  4   | Signal  | Route/Components| 1 oz
```

## 🎯 Best practices

### Design optimization

#### Signal integrity
- **Reference planes**: each signal layer needs reference
- **Return paths**: continuous ground beneath signals
- **Layer transitions**: minimize via usage
- **Crosstalk**: separate sensitive signals

#### Power integrity
- **Dedicated planes**: power and ground planes
- **Decoupling**: plane capacitance + discrete caps
- **Multiple domains**: separate power planes
- **Current paths**: low-impedance distribution

#### EMI/EMC
- **Ground planes**: continuous reference
- **Power planes**: reduce loop areas
- **Via stitching**: tie planes together
- **Edge coupling**: avoid signals at board edge

### Cost optimization

#### Layer count
- **Minimum viable**: use minimum necessary layers
- **Standard stackups**: stick to fab standard offerings
- **Panel utilization**: design for efficient paneling

#### Materials
- **Standard FR-4**: unless special requirements
- **Standard thickness**: 1.6mm most economical
- **Copper weight**: 1oz standard, heavier for high current

## 🔗 Powiązane tematy
- [[pcb_podstawy|Podstawy PCB]] - podstawowe pojęcia PCB
- [[pcb_projekt_layoutu|Projekt Layoutu]] - proces layoutu
- [[pcb_routing_sciezki|Routing Ścieżek]] - prowadzenie ścieżek między warstwami
- [[pcb_plane_zasilania|Płaszczyzny Zasilania]] - power planes design
- [[pcb_plane_masy|Płaszczyzny Masy]] - ground planes design  
- [[pcb_impedancja_kontrolowana|Impedancja Kontrolowana]] - kontrola impedancji w stackup
- [[pcb_via_i_drillholes|Via i Otwory]] - połączenia między warstwami
- [[pcb_produkcja_wytwarzanie|Produkcja PCB]] - wpływ na manufacturing

---

**🎯 Co dalej?**
Po zrozumieniu struktury warstw, przejdź do [[pcb_routing_sciezki|Routing Ścieżek]] aby nauczyć się prowadzić połączenia między warstwami, lub [[pcb_impedancja_kontrolowana|Impedancji Kontrolowanej]] dla zaawansowanych aplikacji.