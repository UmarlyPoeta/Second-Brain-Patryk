# Impedancja Kontrolowana w PCB

## 🎯 Wprowadzenie

Impedancja kontrolowana to kluczowy aspekt projektowania high-speed PCB, gdzie trace'y są projektowane z określoną impedancją charakterystyczną. Kontrola impedancji jest niezbędna dla zachowania integralności sygnałów w aplikacjach wysokiej częstotliwości.

## 📚 Podstawy impedancji

### Definicja impedancji charakterystycznej

#### Impedancja linii transmisyjnej
```
Z₀ = √(L/C)

gdzie:
L = inductance per unit length
C = capacitance per unit length

Physical meaning:
- Stosunek napięcia do prądu w fali biegnącej
- Niezależna od długości linii
- Określona przez geometrię i materiały
```

### Kiedy impedancja ma znaczenie?

#### Kryteria projektowe
```
Reguła rise time:
tᵣ < 2 × tᵨ

gdzie:
tᵣ = rise time sygnału
tᵨ = propagation delay linii

Praktyczne kryteria:
- Clock frequency >50MHz
- Rise time <2ns  
- Trace length >2.5cm (1 inch)
- Digital edges <1ns
```

#### Skutki niepasującej impedancji
```
Signal integrity problems:
- Reflections: odbicia na końcach linii
- Ringing: oscylacje sygnału
- Overshoot/undershoot: przekroczenia poziomów
- EMI: promieniowanie elektromagnetyczne
- Timing errors: opóźnienia i jitter
```

## 📐 Rodzaje linii transmisyjnych

### Microstrip

#### Konfiguracja
```
Signal trace (width W)
    ↓
┌─────────────┐ ← Solder mask
├─────────────┤ ← Substrate (thickness H)
└─────────────┘ ← Ground plane
```

#### Wzór na impedancję
```
Z₀ = (87/√(εᵣ+1.41)) × ln(5.98H/(0.8W+T))

gdzie:
W = trace width
H = substrate thickness
T = trace thickness  
εᵣ = dielectric constant

Typical values:
- Z₀ = 50Ω most common
- εᵣ = 4.3 for FR-4
- H = 0.2mm typical
```

### Stripline

#### Konfiguracja
```
┌─────────────┐ ← Ground plane
├─────────────┤ ← Substrate (H1)
│─────────────│ ← Signal trace (W)
├─────────────┤ ← Substrate (H2)  
└─────────────┘ ← Ground plane
```

#### Wzór na impedancję
```
Z₀ = (60/√εᵣ) × ln(4H/(0.67π(0.8W+T)))

gdzie:
H = total dielectric thickness (H1+H2)
W = trace width
T = trace thickness

Benefits:
- Better EMI shielding
- More stable impedance
- Less crosstalk
```

### Coplanar waveguide

#### Struktura
```
GND   Signal   GND
 │       │      │
┌┴─┐   ┌─┴─┐   ┌┴─┐
│   │   │   │   │   │
├───┼───┼───┼───┼───┤ ← Substrate
└───────┴───┴───────┘ ← Ground plane
```

#### Applications
- **RF circuits**: precise impedance control
- **High-speed digital**: tight coupling control
- **Flex circuits**: limited layer count
- **Test fixtures**: probe access

## ⚡ Differential pairs

### Differential signaling basics

#### Advantages
```
Benefits:
- Common mode noise rejection
- Lower EMI emission  
- Better signal integrity
- Higher noise immunity
- Reduced power consumption
```

#### Common applications
```
Protocols using differential:
- USB: 90Ω differential
- Ethernet: 100Ω differential
- HDMI: 100Ω differential
- SATA: 100Ω differential
- DDR memory: 100Ω differential
- LVDS: 100Ω differential
```

### Differential pair design

#### Key parameters
```
Differential impedance: Zdiff
Common mode impedance: Zcommon
Single-ended impedance: Z₀

Relationships:
Zdiff ≈ 2 × Z₀ × (1 - k)
gdzie k = coupling factor

Typical targets:
- Zdiff = 90Ω, 100Ω
- Z₀ = 45Ω, 50Ω
```

#### Layout rules
```
Spacing rules:
- S = spacing between traces
- W = trace width
- Typical S/W ratio = 1:1 to 2:1

Length matching:
- Intra-pair matching: ±0.05mm
- Pair-to-pair matching: ±0.1mm
- Via matching: symmetric placement

Routing constraints:
- Keep pairs together
- Avoid via unless necessary
- Minimize layer changes
- Maintain spacing over gaps
```

## 🎨 Stackup design

### 4-layer controlled impedance

#### Example stackup
```
Layer 1: Signal (0.035mm Cu)
Prepreg: 0.21mm (εᵣ=4.2)
Layer 2: Ground (0.035mm Cu)
Core: 1.065mm (εᵣ=4.5)
Layer 3: Power (0.035mm Cu)  
Prepreg: 0.21mm (εᵣ=4.2)
Layer 4: Signal (0.035mm Cu)

Total: 1.6mm standard
```

#### Impedance calculations
```
Layer 1 microstrip:
- Target: 50Ω
- Width: ~0.14mm
- Spacing to GND: 0.21mm

Layer 4 microstrip:
- Target: 50Ω  
- Width: ~0.14mm
- Spacing to power: 0.21mm

Differential pairs:
- Target: 100Ω
- Trace width: 0.1mm
- Spacing: 0.1mm
```

### High-speed stackup

#### 6-layer example
```
L1: Signal (microstrip 50Ω)
L2: Ground plane
L3: Signal (stripline 50Ω)
L4: Power plane
L5: Signal (stripline 50Ω)
L6: Signal (microstrip 50Ω)

Benefits:
- Multiple signal routing layers
- Excellent shielding
- Controlled impedance options
- Power integrity
```

#### Layer assignment strategy
```
Signal assignment:
L1: High-speed, length-matched signals
L3: Medium-speed signals  
L5: Low-speed signals
L6: I/O, connectors

Reference assignment:
L2: Primary ground reference
L4: Power distribution + reference
```

## 🔧 Design calculations

### Impedance calculation tools

#### Hand calculations
```
Microstrip approximation:
Z₀ ≈ 87/√(εᵣ+1.41) × ln(5.98h/(0.8w+t))

More accurate (IPC-2141):
Include copper thickness effects
Account dla solder mask
Consider manufacturing tolerances
Surface roughness corrections
```

#### CAD tool calculators
```
Built-in calculators:
- Altium Designer: Layer Stack Manager
- KiCad: Calculator Tools
- Saturn PCB Toolkit: Free tool
- Polar Si9000: Professional tool

Capabilities:
- Multiple transmission line types
- Manufacturing tolerance analysis
- What-if scenarios
- Documentation generation
```

### Tolerance analysis

#### Manufacturing variations
```
Factors affecting impedance:
- Trace width: ±0.025mm (±1 mil)
- Dielectric thickness: ±10%
- Dielectric constant: ±0.2
- Copper thickness: ±20%

Total tolerance:
Typically ±10% dla production PCB
±5% dla controlled impedance
±2% dla precision applications
```

#### Design margins
```
Design considerations:
- Specify realistic tolerances
- Account dla manufacturing spread
- Consider temperature effects
- Plan dla worst-case scenarios

Typical specifications:
- Single-ended: 50Ω ±10%
- Differential: 100Ω ±10%  
- High-speed: tighter tolerances
```

## 📊 Simulation and modeling

### Field solvers

#### 2D field solvers
```
Cross-section analysis:
- Saturn PCB Toolkit
- Polar Si9000  
- CST PCB Studio
- ADS LineCalc

Capabilities:
- Multi-dielectric stackups
- Coupled line analysis
- Frequency-dependent effects
- Manufacturing tolerance
```

#### 3D electromagnetic simulation
```
Full-wave analysis:
- Ansys HFSS
- CST Microwave Studio
- Keysight ADS (Momentum)
- Cadence SIwave

Applications:
- Via modeling
- Connector transitions
- Bent/curved traces
- Complex structures
```

### Measurement techniques

#### TDR (Time Domain Reflectometry)
```
TDR principles:
- Send fast edge down line
- Measure reflected signal
- Calculate impedance profile
- Identify discontinuities

Equipment needed:
- TDR instrument (or sampling scope)
- High-bandwidth probe
- 50Ω coax reference
- Calibration standards
```

#### Frequency domain measurements
```
Network analyzer methods:
- S-parameter measurements
- Impedance vs frequency
- Insertion loss
- Return loss

Calibration requirements:
- SOLT (Short-Open-Load-Thru)
- De-embedding fixtures
- Reference planes
- Measurement uncertainty
```

## 🎯 High-speed design techniques

### Via design

#### Via impedance
```
Via inductance:
L ≈ 5.08 × h × [ln(4h/d) + 1] nH

gdzie:
h = via length (board thickness)
d = via diameter

Impedance discontinuity:
ΔZ = jωL dla inductive via
Significant at >1GHz
```

#### Via optimization
```
Reduction techniques:
- Minimize via length
- Use larger via diameter
- Add ground vias nearby
- Back-drilling (remove stubs)
- Micro-vias dla HDI

Stub resonance:
f ≈ c/(4 × l × √εᵣ)
where l = stub length
```

### Length matching

#### Matching requirements
```
Applications needing matching:
- Clock distribution: <±0.1mm
- Memory interfaces: <±0.05mm
- High-speed serial: <±0.1mm
- Parallel buses: <±0.2mm

Delay differences:
Δt = ΔL/(c/√εₑff)
where εₑff = effective dielectric constant
```

#### Serpentine routing
```
Meander techniques:
- Trombone patterns
- Accordion routing
- S-curves
- Spiral inductors

Design rules:
- Maintain impedance
- Avoid sharp corners  
- Keep spacing adequate
- Minimize crosstalk
```

## 🏭 Manufacturing considerations

### Fabrication control

#### Process control
```
Critical parameters:
- Etch process control
- Dielectric thickness
- Registration accuracy
- Copper plating uniformity
- Surface roughness

Test coupons:
- Include on production panels
- Same stackup as design
- Test impedance after fabrication
- Statistical process control
```

#### Documentation requirements
```
Impedance control specification:
☐ Target impedance ± tolerance
☐ Stackup details
☐ Trace geometry
☐ Test coupon requirements
☐ Test frequency
☐ Acceptance criteria
☐ Test method (TDR, VNA)
```

### Cost implications

#### Controlled impedance pricing
```
Cost factors:
- Additional test coupons
- TDR/VNA testing
- Tighter process control
- Documentation requirements
- Potential rework costs

Typical adders:
- 15-30% over standard PCB
- Volume discounts available
- Express services cost more
```

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_warstwy_pcb|Warstwy PCB]] - stackup design
- [[pcb_routing_sciezki|Routing Ścieżek]] - high-speed routing
- [[pcb_plane_masy|Płaszczyzny Masy]] - reference planes
- [[pcb_via_i_drillholes|Via i Otwory]] - via effects on impedance
- [[pcb_emi_emc|EMI/EMC]] - signal integrity and EMC
- [[pcb_testowanie_debug|Testowanie i Debug]] - impedance testing

---

**🎯 Co dalej?**
Po opanowaniu impedancji kontrolowanej, przejdź do [[pcb_emi_emc|EMI/EMC]] aby zrozumieć electromagnetic compatibility aspects, lub [[pcb_testowanie_debug|Testowania i Debug]] dla verification techniques high-speed designs.