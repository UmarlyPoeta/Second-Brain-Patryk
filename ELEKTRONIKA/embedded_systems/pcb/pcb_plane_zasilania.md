# Płaszczyzny Zasilania w PCB

## 🎯 Wprowadzenie

Płaszczyzny zasilania (power planes) to dedykowane warstwy miedzianne w PCB służące do dystrybucji napięć zasilających. Właściwe projektowanie płaszczyzn zasilania jest kluczowe dla niezawodnego działania układów elektronicznych, szczególnie w aplikacjach wysokich częstotliwości i dużych prądów.

## 📚 Podstawy płaszczyzn zasilania

### Czym są power planes?

#### Definicja i funkcje
```
Power plane to:
- Ciągła warstwa miedzi dedykowana zasilaniu
- Niska impedancja dla dystrybucji mocy
- Pojemność odsprzęgająca z ground plane
- Ekranowanie sygnałów
- Odprowadzanie ciepła
```

#### Zalety vs individual traces
```
Power planes vs ścieżki zasilania:

✅ Zalety planes:
- Bardzo niska impedancja
- Uniform voltage distribution
- Natural decoupling capacitance
- EMI shielding
- Thermal spreading
- Current handling capability

❌ Wady:
- Wyższa liczba warstw
- Zwiększony koszt
- Complexity w projektowaniu
```

### Rodzaje konfiguracji

#### Dedicated power planes
```
4-layer stackup:
Layer 1: Signal (Top)
Layer 2: Ground Plane (solid)
Layer 3: Power Plane (+3.3V, +5V)
Layer 4: Signal (Bottom)

Benefits:
- Clean power distribution
- Excellent decoupling
- Good EMI performance
```

#### Split power planes
```
Single layer z multiple voltages:
+5V region | +3.3V region | +12V region

Considerations:
- Avoid splits under high-speed signals
- Proper bridging between regions
- Return path planning
- Slot radiation issues
```

#### Power islands
```
Mixed approach:
- Large copper pours for power
- Individual traces dla specific needs
- Islands connected via ferrite beads
- Local regulation points

Applications:
- Mixed analog/digital supplies
- Low noise requirements
- Multiple voltage domains
```

## ⚡ Electrical characteristics

### Impedance characteristics

#### Plane pair impedance
```
Z₀ = √(L/C)

gdzie:
L = inductance per unit area
C = capacitance per unit area

Typical values:
- Power/ground plane pair: 0.01-0.1Ω @ DC
- High frequency: inductive reactance increases
- Resonant frequency: depends on dimensions
```

#### Capacitance between planes
```
C = ε₀ × εᵣ × A / d

gdzie:
ε₀ = free space permittivity
εᵣ = relative permittivity (FR-4 ≈ 4.3)
A = overlap area
d = dielectric thickness

Example:
100mm × 100mm planes, 0.2mm separation
C = 8.85×10⁻¹² × 4.3 × 0.01 / 0.0002 = 1.9nF
```

### Current carrying capacity

#### Current density limits
```
Safe current densities dla internal planes:
- 1oz copper (35µm): 10A/mm² width
- 2oz copper (70µm): 20A/mm² width  
- Temperature rise: <10°C above ambient

Derating factors:
- Internal layers: 50% of external
- Multiple current paths: parallel combination
- Thermal vias: heat extraction improvement
```

#### Voltage drop calculations
```
V_drop = I × R = I × (ρ × L / A)

gdzie:
ρ = copper resistivity (1.7×10⁻⁸ Ωm @ 20°C)
L = current path length
A = cross-sectional area

For plane: A = width × thickness
Path length: depends on current distribution
```

## 🎨 Design strategies

### Solid planes approach

#### When to use solid planes
```
Applications:
- High current requirements (>5A)
- Low noise analog circuits
- High-speed digital (>100MHz)
- EMI-critical applications
- Thermal management needs

Design considerations:
- Minimize plane cuts/splits
- Provide via stitching to ground
- Consider thermal expansion
- Plan test point access
```

#### Plane pair design
```
Optimal stackup dla power integrity:
Layer 1: Signal
Layer 2: Ground (reference)
Layer 3: Power (+3.3V)
Layer 4: Signal

Benefits:
- Low impedance power distribution
- Natural decoupling capacitance
- Excellent EMI performance
- Thermal advantages
```

### Split plane strategies

#### Voltage domain separation
```
Design principles:
- Group components by voltage
- Minimize inter-domain signal routing
- Provide proper return paths
- Bridge domains gdzie necessary

Bridging techniques:
- Ferrite beads dla isolation
- Series resistance dla damping
- Capacitive coupling dla AC
- Direct connection dla DC
```

#### Return path management
```
Critical rule:
Signals must have continuous return path

Problem areas:
- Crossing plane splits
- Via transitions between layers
- Connector areas
- Power domain boundaries

Solutions:
- Stitching vias across gaps
- Ground pour strategies
- Layer assignment planning
```

## 🔧 Via strategies

### Power distribution vias

#### Via count dla current
```
Current sharing calculations:
Total current = N × I_via

Where N = number of parallel vias
I_via depends on via size i thermal limits

Example:
5A total current, 0.3mm vias (1A each)
Minimum 5 vias required
Recommend 7-8 vias dla margin
```

#### Via placement patterns
```
Regular grid:
○ ○ ○ ○ ○
○ ○ ○ ○ ○
○ ○ ○ ○ ○

Advantages: uniform distribution
Spacing: 5-10mm typical

Clustered approach:
  ○○○
  ○IC○  
  ○○○

Advantages: localized low impedance
Applications: high current ICs
```

### Via stitching

#### Ground-power plane connection
```
Purpose:
- Reduce plane pair inductance
- Improve transient response
- Enhance thermal coupling
- EMI improvement

Spacing guidelines:
- λ/10 rule: spacing < wavelength/10
- Practical: 10-20mm dla <100MHz
- High-speed: 5-10mm spacing
```

## 🌡️ Thermal management

### Heat dissipation

#### Thermal vias
```
Thermal via design:
- Size: 0.2-0.3mm diameter adequate
- Spacing: 0.5-1.0mm centers
- Pattern: grid or honeycomb
- Fill: filled vias dla best thermal transfer

Thermal resistance:
Single via: ~40°C/W typical
Array of vias: R_total = R_single / N
```

#### Thermal spreading
```
Power plane thermal benefits:
- Large copper area: heat spreading
- Via connections: inter-layer transfer
- Component thermal pads: direct connection
- Heat sink attachment: thermal interface

Design considerations:
- Copper thickness: thicker = better
- Via density: more = lower thermal resistance
- Plane area: larger = better spreading
```

### Hot spot management

#### Component placement
```
Thermal design rules:
- Heat sources: spread across board
- Thermal coupling: via thermal pads
- Air flow: consider cooling direction
- Sensitive components: away from heat sources

Power density limits:
- General PCB: <2W/cm² without special cooling
- High-power: thermal vias + heat sinks
- LED applications: aluminum core PCB
```

## 📊 Power integrity analysis

### Impedance analysis

#### Plane resonances
```
Cavity resonance frequency:
f_mn = (c/2√εᵣ) × √[(m/L)² + (n/W)²]

gdzie:
L, W = plane dimensions
m, n = mode numbers (1,1 dla fundamental)
c = speed of light
εᵣ = dielectric constant

Example dla 100mm × 100mm plane:
f₁₁ ≈ 1.05GHz (FR-4, εᵣ=4.3)
```

#### Simulation tools
```
Power integrity analysis:
- SIwave (Ansys): frequency domain
- PowerSI (Cadence): time/frequency domain
- CST Studio: 3D electromagnetic
- ADS Momentum: planar structures

Analysis types:
- Z-parameter extraction
- Impedance vs frequency
- Current density mapping
- Via impedance effects
```

### Decoupling strategy

#### Hierarchical decoupling
```
Decoupling capacitor strategy:
Bulk: 10-100µF (low frequency)
Intermediate: 1-10µF (mid frequency)  
Local: 10-100nF (high frequency)

Placement rules:
- Closest to power pins
- Via directly to planes
- Multiple values dla broadband
- ESR consideration dla damping
```

#### Plane capacitance utilization
```
Distributed capacitance:
Plane pair acts as distributed capacitor
Effective dla mid-frequencies
Augments discrete decoupling caps

Limitations:
- Resonances at high frequencies
- Non-uniform current distribution
- Via inductances
```

## 🔌 Special considerations

### Mixed-signal design

#### Analog power planes
```
Analog supply requirements:
- Low noise: minimize digital coupling
- Separate regulation: analog LDO
- Star grounding: single point connection
- Shielding: guard traces/planes

Layout techniques:
- Separate analog power plane
- Ferrite bead isolation
- Local regulation at analog section
- Return path planning
```

#### Digital power considerations
```
Digital supply characteristics:
- High current transients
- Switching noise
- Multiple voltage domains
- Clock distribution coupling

Design approach:
- Solid power planes
- Multiple decoupling capacitors
- Via stitching
- Proper layer stackup
```

### High-frequency design

#### Power delivery network (PDN)
```
PDN components:
- VRM (Voltage Regulator Module)
- Bulk capacitors
- PCB power planes
- Decoupling capacitors
- IC power pins

Target impedance:
Z_target = V_ripple / I_transient

Example: 5% ripple, 1A transient
Z = 0.05×3.3V / 1A = 0.165Ω
```

### Power sequencing

#### Supply ordering
```
Sequencing requirements:
- Core before I/O supplies
- Analog before digital (sometimes)
- Voltage level considerations
- Inrush current limiting

Implementation:
- Sequencing controllers
- Power good signals
- Soft start circuits
- Load switches
```

## 🛠️ Layout best practices

### Routing around planes

#### Signal routing over planes
```
Best practices:
- Route signals over continuous plane
- Avoid routing over plane splits
- Provide return path planning
- Use appropriate via stitching

Layer assignment:
- High-speed signals: over solid planes
- Low-speed signals: can cross splits
- Critical clocks: dedicated routing
```

#### Via placement strategy
```
Power via guidelines:
- Multiple vias dla high current
- Close to component power pins
- Grid pattern dla uniform distribution
- Adequate via size dla current

Thermal via considerations:
- Under high-power components
- Connect to heat spreading planes
- Filled vias dla best thermal transfer
```

### Manufacturing considerations

#### Fabrication constraints
```
Minimum features:
- Plane to plane spacing: 0.1mm
- Via to plane clearance: 0.05mm
- Plane edge to track: 0.2mm
- Thermal relief connections: adequate

Cost implications:
- Additional layers increase cost
- Complex plane shapes
- Via count impact
- Testing requirements
```

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_warstwy_pcb|Warstwy PCB]] - struktura wielowarstwowa
- [[pcb_plane_masy|Płaszczyzny Masy]] - ground plane design
- [[pcb_via_i_drillholes|Via i Otwory]] - via design dla power
- [[pcb_routing_sciezki|Routing Ścieżek]] - power routing techniques
- [[pcb_thermal_management|Zarządzanie Cieplne]] - thermal aspects
- [[pcb_emi_emc|EMI/EMC]] - power plane EMI considerations

---

**🎯 Co dalej?**
Po zrozumieniu płaszczyzn zasilania, przejdź do [[pcb_plane_masy|Płaszczyzn Masy]] aby poznać grounding strategies, lub [[pcb_thermal_management|Zarządzania Cieplnego]] dla thermal design considerations.