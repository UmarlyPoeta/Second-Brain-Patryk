# Zarządzanie Cieplne w PCB

## 🎯 Wprowadzenie

Zarządzanie cieplne w PCB to kluczowy aspekt projektowania płytek zawierających komponenty generujące ciepło. Proper thermal management zapewnia niezawodną pracę układów, przedłuża żywotność komponentów i optimizes performance systemu elektronicznego.

## 🌡️ Podstawy termodynamiki PCB

### Heat generation sources

#### Primary heat sources
```
Komponenty generujące ciepło:
- Power semiconductors (MOSFETs, regulators)
- Microprocessors i DSPs
- Power management ICs
- LEDs wysokiej mocy
- Resistors (wysokie prądy)
- Transformers i inductors

Power dissipation calculation:
P = I²R (resistive losses)
P = V×I (semiconductor losses)
P = f×C×V² (switching losses)
```

### Heat transfer mechanisms

#### Conduction
```
Fourier's Law:
Q = k × A × (ΔT/Δx)

gdzie:
Q = heat flow [W]
k = thermal conductivity [W/mK]
A = cross-sectional area [m²]
ΔT = temperature difference [K]
Δx = distance [m]

Materials thermal conductivity:
- Copper: 400 W/mK
- Aluminum: 205 W/mK  
- FR-4: 0.3 W/mK (through-plane)
- FR-4: 0.8 W/mK (in-plane)
- Air: 0.024 W/mK
```

#### Convection
```
Natural convection:
h = 5-25 W/m²K (vertical surfaces)
h = 2-10 W/m²K (horizontal surfaces)

Forced convection:
h = 10-500 W/m²K (depending on airflow)

Heat transfer equation:
Q = h × A × ΔT
```

#### Radiation
```
Stefan-Boltzmann Law:
Q = ε × σ × A × (T₁⁴ - T₂⁴)

gdzie:
ε = emissivity (0-1)
σ = Stefan-Boltzmann constant
A = surface area
T = absolute temperature [K]

Practical note:
Radiation significant only at high temperatures
(>100°C surface temperature)
```

## 🔧 PCB thermal design techniques

### Copper spreading

#### Thermal vias
```
Via thermal resistance:
R_via = L / (k × A)

gdzie:
L = via length (board thickness)
k = copper thermal conductivity
A = via cross-sectional area

Multiple vias in parallel:
R_total = R_single / N

Practical design:
- Via size: 0.2-0.3mm adequate
- Spacing: 0.5-1.0mm centers
- Pattern: grid or honeycomb array
```

#### Heat spreading planes
```
Thermal spreading design:
- Large copper areas under hot components
- Thick copper layers (2oz, 4oz)
- Multiple layers dla heat distribution
- Thermal vias connecting layers
- Heat sink attachment areas

Effectiveness factors:
- Copper thickness
- Spreading area
- Via density
- Layer connectivity
```

### Component placement strategy

#### Thermal isolation
```
Layout guidelines:
- Heat sources: distributed across PCB
- Temperature-sensitive: away from hot spots
- Airflow consideration: cooling path planning
- Component height: clearance dla heat sinks

Critical separations:
- Power components: >5mm from sensitive analog
- Crystal oscillators: <±50ppm stability requirement
- Electrolytic capacitors: temperature derating
```

#### Thermal coupling
```
When thermal coupling desired:
- Multiple power stages sharing heat sink
- Thermal shutdown protection sharing
- Temperature monitoring centralized
- Heat distribution optimization

Design techniques:
- Shared thermal planes
- Thermal via bridges
- Common heat sink mounting
```

## 🏗️ Heat sink integration

### Heat sink types

#### PCB-mounted heat sinks
```
Common types:
- Clip-on: TO-220, TO-263 packages
- Adhesive: thermal tape mounting
- Push-pin: through-hole mounting
- Threaded: screw mounting

Selection criteria:
- Thermal resistance: °C/W rating
- Package compatibility
- Mechanical constraints
- Cost considerations
```

#### Custom heat spreaders
```
Design considerations:
- Material: aluminum, copper
- Thickness: thermal mass vs weight
- Fin design: surface area optimization
- Mounting: mechanical attachment
- Interface: thermal pad/paste

Thermal interface materials:
- Thermal pads: 1-8 W/mK typical
- Thermal paste: 1-15 W/mK
- Phase change materials
- Graphite sheets: high lateral conductivity
```

### Thermal interface design

#### Component thermal pads
```
Exposed pad packages:
- QFN thermal pads
- Power MOSFETs with tab
- BGA thermal balls
- Custom thermal slugs

Design requirements:
- Direct via connection to planes
- Solder mask opening
- Thermal via array
- Heat sink mounting provisions
```

## 📊 Thermal analysis

### Simulation tools

#### FEA thermal analysis
```
Popular tools:
- ANSYS Icepak: dedicated electronics cooling
- Altium Designer: integrated thermal analysis
- FloTHERM: specialist thermal simulation
- COMSOL: multi-physics simulation
- SolidWorks Simulation: mechanical CAD integrated

Analysis types:
- Steady-state thermal
- Transient thermal
- Conjugate heat transfer (fluid+solid)
- Coupled electro-thermal
```

#### Simulation setup
```
Model requirements:
- Accurate geometry (PCB, components, enclosure)
- Material properties (thermal conductivity, specific heat)
- Power dissipation values
- Boundary conditions (ambient, cooling)
- Mesh quality dla accuracy

Results analysis:
- Temperature distribution
- Heat flux vectors  
- Hot spot identification
- Thermal resistance paths
- Design optimization guidance
```

### Thermal measurement

#### Temperature measurement methods
```
Contact methods:
- Thermocouples: wide range, good accuracy
- RTDs: high accuracy, linear
- Thermistors: high sensitivity, limited range
- IC temperature sensors: digital output

Non-contact methods:
- Infrared cameras: surface temperature mapping
- Infrared thermometers: spot measurements
- Liquid crystal sheets: temperature indication
- Thermal test paints: irreversible indicators
```

#### Thermal testing procedures
```
Test conditions:
- Ambient temperature control
- Airflow standardization
- Power dissipation levels
- Steady-state vs transient
- Worst-case conditions

Data collection:
- Temperature vs time
- Spatial temperature distribution  
- Power vs temperature curves
- Thermal resistance measurements
- Reliability stress testing
```

## ⚡ High-power applications

### Power density considerations

#### Safe power density limits
```
General guidelines:
- Standard PCB: <2W/cm² without special cooling
- Enhanced cooling: up to 10W/cm²
- Specialized thermal design: >10W/cm²

Factors affecting limits:
- Cooling method (natural vs forced)
- PCB thermal design
- Component package types
- Operating environment
- Reliability requirements
```

#### Power management strategies
```
Techniques dla high power:
- Power staging: distribute power conversion
- Thermal load sharing: parallel power paths
- Dynamic thermal management: power limiting
- Phase interleaving: reduce ripple current heating
- Synchronous operation: minimize conduction losses
```

### Specialized PCB technologies

#### Metal core PCBs
```
MCPCB characteristics:
- Aluminum/copper substrate
- Thermal conductivity: 1-8 W/mK
- Electrical isolation: thermal interface layer
- Applications: LED, power electronics

Design considerations:
- Layer stackup: typically 1-2 layer
- Via limitations: no thermal vias through metal
- Component placement: direct thermal coupling
- Cost: higher than standard FR-4
```

#### Thick copper PCBs
```
Heavy copper applications:
- Current carrying: reduced resistance
- Thermal spreading: better heat conduction
- Mechanical strength: improved durability

Copper weights available:
- Standard: 1oz (35μm)
- Heavy: 2-3oz (70-105μm)  
- Extreme: 4-20oz (140-700μm)

Manufacturing impacts:
- Minimum trace/space increase
- Via aspect ratio limitations
- Etching process modifications
- Cost increase with copper weight
```

## 🌬️ Cooling strategies

### Natural convection optimization

#### PCB orientation effects
```
Optimal orientations:
- Vertical: best natural convection
- Horizontal (component up): moderate cooling
- Horizontal (component down): poor cooling

Design considerations:
- Component placement dla airflow
- Board spacing in systems
- Ventilation openings
- Chimney effect utilization
```

#### Surface area enhancement
```
Techniques:
- Heat sink fins: increase surface area
- Component standoffs: improve airflow under components
- PCB cutouts: airflow paths through board
- Surface texturing: enhanced heat transfer coefficient

Effectiveness factors:
- Fin spacing: optimize dla airflow
- Fin height: balance area vs flow restriction
- Surface finish: emissivity dla radiation
```

### Forced convection systems

#### Fan cooling design
```
Fan selection criteria:
- Airflow rate [CFM, m³/h]
- Static pressure capability
- Power consumption
- Noise level
- Reliability (bearing type)
- Operating temperature range

Airflow optimization:
- Duct design: minimize pressure drops
- Component arrangement: minimize flow blockage
- Hot spot targeting: direct cooling
- System level design: intake/exhaust balance
```

#### Liquid cooling considerations
```
When liquid cooling needed:
- Power density >50W/cm²
- Space constraints
- Noise requirements
- Precise temperature control

Implementation:
- Cold plates: direct component contact
- Heat pipes: passive transport
- Thermosiphon systems: natural circulation
- Pumped systems: forced circulation
```

## 🧪 Reliability considerations

### Temperature effects on components

#### Arrhenius equation
```
Reliability temperature dependence:
AF = exp[(Ea/k) × (1/T₁ - 1/T₂)]

gdzie:
AF = acceleration factor
Ea = activation energy [eV]
k = Boltzmann constant
T = absolute temperature [K]

Rule of thumb:
Component lifetime halves dla każde 10°C increase
(varies by component type and failure mechanism)
```

#### Component derating
```
Temperature derating guidelines:
- Junction temperature: 70-80% of maximum
- Ambient operating: 20°C margin minimum
- Storage temperature: consider worst case
- Thermal cycling: stress reduction

Critical components:
- Electrolytic capacitors: 10°C reduces lifetime by 50%
- Semiconductors: junction temperature critical
- Crystals: frequency stability vs temperature
- Batteries: capacity i lifetime degradation
```

### Thermal design validation

#### Design verification tests
```
Test protocols:
- Steady-state thermal mapping
- Transient thermal response
- Power cycling tests
- Environmental cycling
- Accelerated life testing

Acceptance criteria:
- No component exceeds maximum ratings
- Temperature rise within specifications
- Thermal gradients acceptable
- Long-term reliability projections
```

#### Field reliability correlation
```
Validation approach:
- Laboratory test correlation
- Field failure analysis
- Environmental stress screening
- Qualification testing
- Continuous monitoring

Data collection:
- Operating temperature profiles
- Failure modes i rates
- Environmental conditions
- Usage patterns
- Component lot variations
```

## 🔗 Thermal design guidelines

### Design rules summary

#### Component placement
```
Thermal placement rules:
☐ Distribute heat sources across PCB
☐ Orient hot components dla best cooling
☐ Separate temperature-sensitive components
☐ Consider airflow paths in placement
☐ Plan heat sink mounting areas
☐ Provide thermal via arrays under hot components
```

#### Copper utilization
```
Thermal copper guidelines:
☐ Use copper pours dla heat spreading
☐ Implement thermal via arrays
☐ Connect heat sources to planes
☐ Consider thick copper dla high power
☐ Optimize copper distribution dla evenness
☐ Connect thermal planes between layers
```

#### System integration
```
System thermal design:
☐ Plan system-level cooling strategy
☐ Consider enclosure thermal design
☐ Integrate with mechanical constraints
☐ Plan dla manufacturing i service access
☐ Document thermal requirements clearly
☐ Validate design with testing
```

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_plane_zasilania|Płaszczyzny Zasilania]] - power distribution thermal aspects
- [[pcb_via_i_drillholes|Via i Otwory]] - thermal via design
- [[pcb_komponenty_elektroniczne|Komponenty Elektroniczne]] - thermal characteristics
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - thermal design guidelines
- [[pcb_produkcja_wytwarzanie|Produkcja PCB]] - thermal manufacturing considerations
- [[pcb_testowanie_debug|Testowanie i Debug]] - thermal testing methods

---

**🎯 Co dalej?**
Po zrozumieniu zarządzania cieplnego, wróć do [[pcb_najlepsze_praktyki|Najlepszych Praktyk]] aby zintegrować thermal considerations z overall design methodology, lub przejdź do [[pcb_projekty_praktyczne|Projektów Praktycznych]] aby zastosować thermal design w real projects.