# EMI/EMC w Projektowaniu PCB

## 🎯 Wprowadzenie

EMI/EMC (Electromagnetic Interference/Electromagnetic Compatibility) to kluczowy aspekt projektowania PCB, szczególnie w dzisiejszym świecie pełnym urządzeń elektronicznych. Właściwe uwzględnienie zasad EMI/EMC na etapie projektowania PCB może zaoszczędzić znaczne koszty i czas w późniejszych fazach rozwoju produktu.

## 📚 Podstawowe pojęcia

### Definicje
- **EMI**: Electromagnetic Interference - zakłócenia elektromagnetyczne
- **EMC**: Electromagnetic Compatibility - kompatybilność elektromagnetyczna  
- **Emission**: energia elektromagnetyczna emitowana przez urządzenie
- **Immunity**: odporność na zewnętrzne zakłócenia elektromagnetyczne

### Rodzaje zakłóceń

#### Według sposobu przenoszenia
```
Conducted EMI:
- Przenoszenie przez przewody
- Częstotliwość: 150kHz - 30MHz
- Źródła: switching regulators, clocks

Radiated EMI:
- Przenoszenie przez pole elektromagnetyczne
- Częstotliwość: 30MHz - 1GHz+  
- Źródła: clock signals, digital switching
```

#### Według charakteru
```
Common Mode:
- Sygnały w fazę na obu przewodach
- Return przez ground/chassis
- Główne źródło promieniowania

Differential Mode:
- Sygnały w przeciwfazie
- Return przez drugi przewód
- Mniejsze promieniowanie
```

## ⚡ Źródła zakłóceń w PCB

### Switching circuits

#### Digital switching
```
Źródła EMI:
- Clock signals: fundamental + harmonics
- Bus transitions: simultaneous switching  
- Power supply switching: regulators
- Crystal oscillators: clock generation

Mechanizm:
dI/dt i dV/dt → E-field i H-field → radiation
```

#### Switching power supplies
```
Primary EMI sources:
- Power switch transitions
- Transformer/inductor ringing
- Diode recovery current
- Input/output filtering inadequate

Frequency spectrum:
- Fundamental: switching frequency
- Harmonics: up to 50×fundamental
- Broad spectrum: fast transitions
```

### Clock distribution

#### Clock harmonics
```
Square wave spectrum:
f₀, 3f₀, 5f₀, 7f₀, 9f₀...

Amplitude reduction:
- Slower rise times: reduce high-frequency content
- Spread spectrum: distribute energy
- Clock gating: reduce activity
```

## 🛡️ Emission control techniques

### Ground plane design

#### Solid ground planes
```
Benefits dla EMI:
- Return current path: minimize loop area
- Reference potential: stable ground
- Shielding: electric field containment
- Heat spreading: thermal management

Design rules:
- Continuous: avoid splits gdy possible
- Large area: maximize coverage  
- Multiple layers: stitching vias
- Low impedance: wide connections
```

#### Ground loops prevention
```
Problem:
Multiple ground paths → current loops → magnetic field

Solutions:
- Single point grounding (low freq)
- Solid ground plane (high freq)
- Ground stitching vias
- Proper connector grounding
```

### Power distribution

#### Power plane strategies
```
Solid power planes:
- Uniform voltage distribution
- Low inductance: fast transients
- Decoupling capacitance: plane-to-plane
- Heat spreading: thermal management

Split planes considerations:
- Avoid gdy possible dla EMI
- If needed: proper bridging
- Return path planning
- Slot radiation issues
```

#### Decoupling network
```
Hierarchical decoupling:
Bulk (100µF) → Intermediate (1-10µF) → Local (100nF)

Placement rules:
- Close to IC: minimize inductance
- Multiple values: different frequencies
- Via placement: direct to planes
- ESR considerations: damping
```

### Layout techniques

#### Component placement
```
EMI-friendly placement:
- High-speed circuits: center of board
- Clock sources: away from I/O
- Switching supplies: isolated section
- Sensitive analog: quiet corner

Distance rules:
- 3W rule: adjacent tracks spacing
- High/low speed separation
- Analog/digital isolation
- Crystal positioning: shield with ground
```

#### Trace routing
```
EMI reduction techniques:
- Minimize loop area: tight coupling
- Reference plane: continuous ground
- Avoid plane splits: no crossing gaps
- Layer transitions: minimize vias

Trace geometry:
- Width consistency: controlled impedance
- Length matching: reduce skew
- Right angles: avoid sharp corners
- Symmetry: balanced layouts
```

## 📻 High-frequency considerations

### Transmission line effects

#### When traces become transmission lines
```
Criterion:
Rise time < 2 × Propagation delay

Practical:
- Length > 2.5cm @ 1ns rise time
- Length > 12.5cm @ 5ns rise time
- Always consider dla clock >50MHz
```

#### Impedance control
```
Target impedances:
- Single-ended: 50Ω (standard)
- Differential: 100Ω (Ethernet, USB)
- High-speed memory: 40Ω typical

Stackup considerations:
- Consistent dielectric thickness
- Controlled trace geometry
- Reference plane proximity
```

### Signal integrity vs EMI

#### Termination strategies
```
Series termination:
- At source: reduces reflections
- Slower edges: less EMI
- Power consumption: lower

Parallel termination:
- At load: absorbs reflections  
- Faster edges: potential EMI
- Power consumption: higher

EMI optimal: series termination
```

## 🔌 Filtering techniques

### Common mode filtering

#### Common mode chokes
```
Applications:
- Power supply inputs
- Cable interfaces  
- I/O connections
- Clock distribution

Design considerations:
- Impedance: high for common mode
- Frequency range: target interference
- Saturation: differential current rating
- Size: board space constraints
```

#### Capacitive filtering
```
Y-capacitors (line-to-ground):
- Value: 1-10nF typical
- Voltage rating: safety requirements
- Safety approval: UL, VDE
- Leakage current: limit per standards

X-capacitors (line-to-line):  
- Value: 0.1-1µF typical
- Self-healing: metallized film
- Safety class: X1, X2 rating
```

### Power supply filtering

#### Input filtering
```
π-filter configuration:
C1 → L → C2

Design considerations:
- C1: switching frequency filter
- L: common mode choke
- C2: high frequency bypass
- Ground plane: proper return
```

#### Point-of-load filtering
```
Local filtering at ICs:
- 100nF ceramic: high frequency
- 1-10µF tantalum: intermediate  
- Ferrite beads: high frequency suppression
- Via placement: minimize inductance
```

## 📐 Mechanical EMC design

### Shielding techniques

#### PCB-level shielding
```
Ground planes:
- Electric field shielding
- Reference potential
- Return current path
- Thermal spreading

Guard traces:
- Around sensitive circuits
- Grounded traces: electric field reduction
- Differential mode suppression
```

#### Enclosure integration
```
PCB-to-chassis connection:
- Multiple ground points
- Low impedance bonds
- Gasket interfaces dla RF
- Grounding screws: short, wide

Aperture control:
- Slot length: <λ/20 dla effective shielding
- Honeycomb patterns: high frequency
- Conductive gaskets: EMI sealing
```

### Cable management

#### Cable as antennas
```
Common mode currents:
- Cable becomes monopole antenna
- Efficiency increases z frequency
- Ground plane discontinuity: major source

Prevention:
- Proper cable grounding
- Ferrite suppressors
- Twisted pair wiring
- Shield termination
```

#### Connector grounding
```
Best practices:
- 360° shield connection
- Multiple ground pins
- Short return paths
- Backshell grounding
```

## 📊 EMC testing considerations

### Pre-compliance testing

#### Radiated emissions
```
Test setup simulation:
- Ground plane: simulate test environment
- Cable routing: realistic positioning
- Load conditions: worst-case scenarios
- Frequency range: regulatory limits

Near-field probing:
- H-field loops: magnetic coupling
- E-field probes: electric coupling
- Spectrum analyzer: frequency domain
- Hot spot identification
```

#### Conducted emissions
```
LISN (Line Impedance Stabilization Network):
- Standard impedance: 50Ω
- Frequency range: 150kHz-30MHz
- Common/differential mode separation
- Reproducible test conditions

Measurement considerations:
- Cable length: 1-3m typical
- Load conditions: rated power
- Switching frequency: worst case
- Modulation effects: spread spectrum
```

### Design margins

#### Regulatory headroom
```
Design targets (below regulatory limits):
- Radiated: -6dB margin minimum
- Conducted: -6dB margin minimum  
- Immunity: +6dB above requirements
- Safety margin: account dla production variation
```

## 🎯 Frequency-specific techniques

### Low frequency (<1MHz)

#### Conducted emission control
```
Differential mode:
- Input filtering: L-C networks
- X-capacitors: line-to-line
- Series inductance: current limiting

Common mode:
- Y-capacitors: line-to-ground
- Common mode chokes
- Isolated supplies
```

### Medium frequency (1-100MHz)

#### PCB layout critical
```
Current loop minimization:
- Ground plane utilization
- Component placement optimization
- Via stitching: ground connection
- Power distribution: low inductance

Critical nets:
- Clock distribution: shielding
- Reset signals: proper termination
- Power switching: local filtering
```

### High frequency (>100MHz)

#### Advanced techniques
```
Microstrip/stripline design:
- Controlled impedance
- Coplanar waveguides
- Guard traces
- Via fence shielding

Material considerations:
- Low-loss dielectrics
- Copper roughness effects
- Skin effect: conductor sizing
```

## 🔧 Design verification

### Simulation tools

#### Field solvers
```
3D electromagnetic analysis:
- HFSS (Ansys): full-wave solver
- CST Studio: time/frequency domain
- Momentum (ADS): planar structures
- SIwave: power integrity focus

Applications:
- Via modeling: impedance discontinuities  
- Plane resonance: cavity modes
- Coupling analysis: crosstalk prediction
- Antenna modeling: radiation patterns
```

### Measurement techniques

#### Spectrum analysis
```
Equipment needed:
- Spectrum analyzer: wide frequency range
- Near-field probes: H-field, E-field
- Current probes: conducted measurements
- Antennas: far-field measurements

Measurement practices:
- Baseline measurement: reference
- Step-by-step analysis: isolate sources
- Fix verification: measure improvement
- Documentation: before/after comparison
```

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_plane_masy|Płaszczyzny Masy]] - grounding strategies
- [[pcb_plane_zasilania|Płaszczyzny Zasilania]] - power distribution
- [[pcb_routing_sciezki|Routing Ścieżek]] - layout techniques
- [[pcb_impedancja_kontrolowana|Impedancja Kontrolowana]] - high-speed considerations
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - general EMC guidelines
- [[pcb_testowanie_debug|Testowanie i Debug]] - EMC troubleshooting

---

**🎯 Co dalej?**
Po zrozumieniu podstaw EMI/EMC, przejdź do [[pcb_impedancja_kontrolowana|Impedancji Kontrolowanej]] dla zaawansowanych aplikacji high-speed, lub [[pcb_testowanie_debug|Testowania i Debug]] aby nauczyć się rozwiązywać problemy EMC.