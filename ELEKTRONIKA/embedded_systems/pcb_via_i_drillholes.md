# Via i Otwory w PCB

## 🎯 Wprowadzenie

Via to pionowe połączenia elektryczne między warstwami PCB, umożliwiające prowadzenie sygnałów i zasilania przez strukturę wielowarstwową płytki. Prawidłowe projektowanie via jest kluczowe dla funkcjonalności, niezawodności i możliwości produkcyjnych PCB.

## 🔧 Rodzaje via

### Through-hole vias (najczęstsze)
```
┌─ Layer 1 (Top)
├─ Layer 2
├─ Layer 3  
└─ Layer 4 (Bottom)
   ↑
Wiertło przez wszystkie warstwy
```

**Charakterystyka:**
- **Połączenie**: wszystkie warstwy PCB
- **Manufacturing**: standardowe wiercenie
- **Koszt**: najniższy
- **Reliability**: najwyższa
- **Rozmiar**: 0.15mm - 6mm drill

### Blind vias
```
┌─ Layer 1 (Top) ←── Via start
├─ Layer 2      ←── Via end
├─ Layer 3
└─ Layer 4 (Bottom)
```

**Charakterystyka:**
- **Połączenie**: zewnętrzna do wewnętrznej warstwy
- **Manufacturing**: controlled depth drilling
- **Koszt**: wyższy niż through-hole
- **Zastosowanie**: high-density applications

### Buried vias
```
┌─ Layer 1 (Top)
├─ Layer 2      ←── Via start
├─ Layer 3      ←── Via end
└─ Layer 4 (Bottom)
```

**Charakterystyka:**
- **Połączenie**: tylko warstwy wewnętrzne
- **Manufacturing**: sequential lamination
- **Koszt**: najwyższy
- **Zastosowanie**: ultra-high density

### Microvias (HDI technology)
```
Charakterystyka:
- Rozmiar: <0.15mm drill diameter
- Aspect ratio: typically 1:1
- Formation: laser drilling
- Applications: BGA, fine-pitch components
```

## 📏 Projektowanie via

### Podstawowe parametry

#### Rozmiary standardowe
```
Drill Size [mm] | Finished Hole [mm] | Pad Size [mm] | Current [A]
0.15           | 0.15              | 0.25          | 0.3
0.20           | 0.20              | 0.35          | 0.7
0.25           | 0.25              | 0.45          | 1.0
0.30           | 0.30              | 0.50          | 1.4
0.40           | 0.40              | 0.65          | 2.0
0.50           | 0.50              | 0.75          | 2.7
```

#### Annular ring
```
Annular Ring = (Pad Diameter - Hole Diameter) / 2

Minimum values:
- Class 1: 0.05mm (2 mil)
- Class 2: 0.05mm (2 mil)  
- Class 3: 0.08mm (3 mil)
- HDI: 0.025mm (1 mil)
```

### Design rules

#### Aspect ratio
```
Aspect Ratio = Board Thickness / Hole Diameter

Recommendations:
- Standard PCB: <8:1
- High reliability: <6:1
- HDI: <1:1 (microvias)
- Thick PCB: special considerations
```

#### Via placement
- **Minimum spacing**: via edge to via edge ≥ 0.1mm
- **Via to track**: ≥ 0.1mm clearance
- **Via to pad**: avoid via in pad dla THT
- **Via to board edge**: ≥ 0.2mm minimum

## ⚡ Electrical characteristics

### Resistance
```
R_via = ρ × L / A

gdzie:
ρ = resistivity miedzi (1.72 × 10⁻⁸ Ωm @ 20°C)
L = length (board thickness)
A = cross-sectional area

Example dla 0.2mm via, 1.6mm thick board:
R = 1.72×10⁻⁸ × 1.6×10⁻³ / (π×(0.1×10⁻³)²) 
R ≈ 0.88 mΩ
```

### Inductance
```
L_via ≈ 5.08 × h × [ln(4×h/d) + 1] nH

gdzie:
h = via length (board thickness)
d = via diameter

Example dla 0.2mm via, 1.6mm board:
L ≈ 5.08 × 1.6 × [ln(4×1.6/0.2) + 1]
L ≈ 1.2 nH
```

### Capacitance
```
C_via ≈ 1.41 × εᵣ × D₁ / ln(D₂/D₁) pF

gdzie:
εᵣ = dielectric constant
D₁ = via diameter  
D₂ = clearance hole diameter in plane

Typical value: 0.5-2 pF per via
```

## 🌡️ Thermal management

### Thermal vias

#### Heat conduction
```
Thermal resistance:
R_th = L / (k × A)

gdzie:
k = copper thermal conductivity (400 W/mK)
L = via length
A = cross-sectional area

Multiple vias in parallel:
R_total = R_single / N (gdzie N = number of vias)
```

#### Thermal via design
```
Applications:
- Under power components (QFN, BGA)
- LED thermal management
- Power regulators heat spreading
- Ground plane thermal connection

Design guidelines:
- Via size: 0.2-0.3mm typically
- Spacing: 0.5-1.0mm on center
- Pattern: grid or honeycomb
- Plating: filled or tented
```

### Via filling

#### Filled vias
- **Conductive fill**: copper or silver
- **Non-conductive fill**: epoxy resin
- **Advantages**: flat surface, no voids
- **Applications**: via-in-pad, thermal management

#### Plugged vias
- **Process**: resin plug + plating over
- **Advantages**: flat surface, solderable
- **Cost**: moderate increase
- **Applications**: HDI, BGA applications

## 🔌 Via stitching

### Power/ground connection

#### Plane stitching
```
Purpose:
- Connect power planes on different layers
- Reduce inductance w power distribution
- Improve EMI performance
- Create uniform potential

Via pattern:
○ ○ ○ ○ ○
○ ○ ○ ○ ○
○ ○ ○ ○ ○

Spacing: 5-15mm typical
Size: 0.2-0.3mm adequate
```

### Ground stitching

#### EMI reduction
- **Ground loops**: minimize loop area
- **Return paths**: provide short return paths
- **Shield effectiveness**: connect shield layers
- **Mode conversion**: reduce common mode

#### Design guidelines
```
Stitching via placement:
- Along signal transitions
- At connector grounds  
- Around switching circuits
- Between analog/digital sections

Frequency considerations:
- λ/10 rule: via spacing < λ/10
- At 1GHz: spacing < 30mm
- At 100MHz: spacing < 300mm
```

## 🏭 Manufacturing considerations

### Drilling processes

#### Mechanical drilling
```
Process parameters:
- Speed: 20,000-150,000 RPM
- Feed rate: 0.05-0.5mm/rev
- Tool life: 500-5000 holes
- Accuracy: ±0.025mm

Advantages:
- High throughput dla large holes
- Good hole quality
- Established process

Limitations:
- Tool wear
- Minimum size ~0.1mm
- Aspect ratio limits
```

#### Laser drilling (HDI)
```
CO₂ laser (10.6μm):
- Materials: organic materials
- Hole size: 0.05-0.5mm
- Taper: 15-25°
- Speed: very high

UV laser (355nm):
- Materials: all PCB materials
- Hole size: 0.025-0.2mm
- Walls: nearly vertical
- Precision: ±10μm
```

### Plating quality

#### Copper plating uniformity
```
Factors affecting plating:
- Aspect ratio: higher = more difficult
- Hole density: crowded areas plate slower
- Agitation: fluid dynamics in holes
- Current distribution: uniform current needed

Quality metrics:
- Minimum copper thickness: 20μm
- Thickness variation: ±20%
- Void-free plating
- Good adhesion to barrel
```

#### Plating defects
- **Voids**: incomplete plating
- **Thin areas**: inadequate thickness
- **Nodules**: rough plating surface
- **Delamination**: poor adhesion

## 🔍 Via reliability

### Failure mechanisms

#### Thermal cycling
```
Failure modes:
- Barrel cracking: CTE mismatch stress
- Pad lifting: adhesion failure
- Plating fatigue: repeated thermal stress

Prevention:
- Proper aspect ratios
- Quality plating process
- Appropriate materials
- Design margins
```

#### Mechanical stress
- **Flexing**: PCB bending stress
- **Vibration**: dynamic loading
- **Assembly**: insertion forces
- **Handling**: manufacturing stress

### Reliability testing

#### Test methods
```
IPC standards:
- Thermal cycling: -55°C to +125°C
- Thermal shock: rapid temperature change
- Mechanical shock: drop testing
- Vibration: sinusoidal and random

Acceptance criteria:
- Resistance change: <10%
- No visual defects
- No electrical opens
- Insulation resistance maintained
```

## 🎯 Design best practices

### Via placement strategy

#### Signal via
```
Guidelines:
- Minimize usage: each via adds inductance
- Keep short: reduce parasitics
- Adjacent ground: provide return path
- Same net: multiple vias acceptable

High-speed considerations:
- Return path planning
- Impedance discontinuity
- Via stub resonance
- Differential pair handling
```

#### Power via
```
Guidelines:
- Multiple parallel: reduce inductance
- Distribute evenly: uniform power distribution
- Adequate size: current carrying capacity
- Thermal considerations: heat conduction

Power integrity:
- Low inductance path
- Decoupling capacitor connection
- Power plane stitching
- Ground bounce reduction
```

### Via optimization

#### Layer transition strategy
```
Minimize layer changes:
- Plan routing layers carefully
- Group nets by layer preference
- Use via arrays for buses
- Consider blind/buried vias dla HDI

Via reduction techniques:
- Careful component placement
- Routing order optimization
- Layer assignment planning
- Bus routing strategies
```

## 📊 Via current capacity

### Current calculations

#### Via current rating
```
Temperature rise equation:
ΔT = 1.09 × (I²×R) / (A^0.8)

gdzie:
ΔT = temperature rise [°C]
I = current [A]
R = via resistance [Ω]
A = via surface area [mm²]

Safe current limits:
0.2mm via: ~1A (10°C rise)
0.3mm via: ~2A (10°C rise)
0.4mm via: ~3A (10°C rise)
```

### Multiple via design

#### Parallel connection
```
Current sharing:
I_total = N × I_single (ideally)

Real conditions:
- Manufacturing variations
- Thermal effects
- Uneven current distribution

Design margin:
- Use 80% of calculated capacity
- Consider hottest operating conditions
- Account for manufacturing tolerances
```

## 🔗 Powiązane tematy
- [[pcb_warstwy_pcb|Warstwy PCB]] - struktura wielowarstwowa
- [[pcb_routing_sciezki|Routing Ścieżek]] - prowadzenie połączeń
- [[pcb_projekt_layoutu|Projekt Layoutu]] - planowanie via
- [[pcb_plane_zasilania|Płaszczyzny Zasilania]] - power distribution via
- [[pcb_plane_masy|Płaszczyzny Masy]] - ground stitching
- [[pcb_produkcja_wytwarzanie|Produkcja PCB]] - manufacturing aspects
- [[pcb_thermal_management|Zarządzanie Cieplne]] - thermal vias

---

**🎯 Co dalej?**
Po zrozumieniu projektowania via, przejdź do [[pcb_plane_zasilania|Płaszczyzn Zasilania]] i [[pcb_plane_masy|Płaszczyzn Masy]] aby nauczyć się efektywnego rozprowadzania mocy i sygnałów w strukturze wielowarstwowej.