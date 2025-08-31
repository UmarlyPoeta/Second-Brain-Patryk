# Montaż Komponentów PCB

## 🎯 Wprowadzenie

Montaż komponentów to proces fizycznego umieszczania i lutowania elementów elektronicznych na PCB. Proper assembly techniques są kluczowe dla niezawodności, funkcjonalności i produkcyjności urządzeń elektronicznych. Ta notatka omawia różne technologie montażu i najlepsze praktyki.

## 📚 Technologie montażu

### THT - Through-Hole Technology

#### Charakterystyka
```
Through-Hole mounting:
- Componenty przewlekane przez otwory w PCB
- Lutowanie od strony solder side
- Mocne połączenia mechaniczne  
- Większe rozmiary komponentów
- Łatwiejszy ręczny montaż
```

#### Zastosowania THT
```
Ideal dla:
- Prototypowanie i development
- Komponenty dużej mocy
- Mechanical connectors
- Components wymagające wytrzymałości
- Educational projects
- Repair i maintenance

Examples:
- Power transformers
- Large electrolytic capacitors
- Power MOSFETs w TO-220
- Connectors i headers
- Switches i potentiometers
```

#### Process THT assembly
```
Manual assembly steps:
1. Component insertion
2. Bending/clinching leads
3. Hand soldering (iron/wave)
4. Lead trimming
5. Cleaning (if required)
6. Inspection i testing

Wave soldering process:
1. Flux application
2. Preheating
3. Wave soldering
4. Cooling
5. Cleaning
6. Inspection
```

### SMT - Surface Mount Technology

#### Charakterystyka
```
Surface Mount benefits:
- Smaller component sizes
- Higher component density
- Better high-frequency performance
- Automated assembly compatible
- Lower manufacturing cost (volume)
- Both sides utilization possible
```

#### SMT process overview
```
Pick and place assembly:
1. Solder paste printing
2. Component placement
3. Reflow soldering
4. Inspection (AOI/AXI)
5. Testing
6. Cleaning (if required)

Key advantages:
- Fully automated process
- High throughput capability
- Consistent quality
- Statistical process control
```

## 🏭 Assembly processes

### Solder paste printing

#### Stencil design
```
Stencil parameters:
- Thickness: 0.1-0.2mm typical
- Aperture size: 90-100% of pad size
- Aperture shape: rectangle, rounded
- Registration: ±25μm typical

Paste release factors:
- Area ratio: >0.66 preferred
- Surface finish: electropolished
- Aperture walls: smooth, vertical
- Cleaning: regular stencil cleaning
```

#### Solder paste properties
```
Paste composition:
- Solder alloy: SAC305 (lead-free standard)
- Flux: rosin-based or water-soluble
- Particle size: Type 3, 4, or 5
- Metal content: 88-92% by weight

Storage i handling:
- Refrigerated storage (2-8°C)
- Working time: 4-8 hours @ room temp
- Stir before use
- Avoid contamination
```

### Component placement

#### Pick and place equipment
```
Machine capabilities:
- Placement speed: 10,000-100,000+ CPH
- Placement accuracy: ±25-50μm
- Component range: 0201 to large BGAs
- Vision systems: component verification
- Feeders: tape, tray, bulk

Placement sequence:
- Fine pitch components first
- Heat-sensitive components last
- Optimize machine efficiency
- Minimize component placement errors
```

#### Placement accuracy
```
Factors affecting accuracy:
- Machine calibration
- Component package type
- Feeder setup i maintenance
- Vision system quality
- PCB warpage i flatness

Typical accuracies:
- Standard SMT: ±75μm
- Fine pitch: ±25μm  
- Flip chip: ±10μm
- BGA: ±50μm
```

### Reflow soldering

#### Reflow profile
```
Profile stages:
1. Ramp-up: 1-3°C/s rise rate
2. Preheat: 150-180°C, 60-120s
3. Reflow: Above liquidus, 20-40s
4. Cool down: <6°C/s initial rate

Critical parameters:
- Peak temperature: 240-250°C (SAC305)
- Time above liquidus: 60-150s
- Time above 217°C: <4 minutes total
- ΔT across PCB: <5°C/cm
```

#### Profile optimization
```
Considerations:
- Component heat sensitivity
- PCB thermal mass
- Solder paste requirements
- Throughput requirements

Profile development:
- Use thermal profiler
- Measure multiple points on PCB
- Adjust conveyor speed i zone temps
- Validate with different PCB sizes
- Document approved profiles
```

## 🔧 Assembly equipment

### Manual assembly tools

#### Basic hand tools
```
Essential tools:
- Temperature-controlled soldering iron
- Solder (rosin core, appropriate alloy)
- Flux (liquid or paste)
- Desoldering braid/pump
- Tweezers (fine tip, anti-static)
- Magnification (2-10×)
```

#### Specialized hand tools
```
Advanced manual tools:
- Hot air rework station
- Preheating plate
- Vacuum pickup tools
- Precision dispensing syringes
- ESD-safe workstation
- Fume extraction system
```

### Production equipment

#### SMT line configuration
```
Complete SMT line:
1. Solder paste printer
2. Pick and place machine(s)
3. Reflow oven
4. Automated optical inspection (AOI)
5. In-circuit test (optional)
6. Functional test

Line balancing:
- Match throughput capabilities
- Minimize bottlenecks
- Buffer between operations
- Quality checkpoints
```

#### Supporting equipment
```
Auxiliary equipment:
- Stencil cleaner
- Component storage (dry cabinets)
- Feeder preparation station
- Traceability systems
- Material handling equipment
- ESD protection systems
```

## 🎯 Design for Assembly (DFA)

### Component placement rules

#### Spacing requirements
```
Minimum spacings:
- Component to component: 0.5mm
- Component to board edge: 1.0mm
- Keep-out around connectors
- Access dla rework/repair
- Tooling i fixture clearances

Height considerations:  
- Avoid shadowing w reflow
- Consider mechanical constraints
- Plan dla heat sink attachment
- PCB warpage effects
```

#### Orientation guidelines
```
Component orientation:
- Polarized components: consistent direction
- Fine pitch ICs: same orientation
- Connectors: accessible placement
- Test points: probe accessibility

Benefits:
- Simplified programming
- Reduced placement errors
- Easier visual inspection
- Consistent rework procedures
```

### Thermal considerations

#### Thermal balance
```
Reflow considerations:
- Component thermal mass matching
- Avoid large thermal imbalances
- Group similar components together
- Consider PCB thermal design

Thermal shadowing:
- Large components create shadows
- Smaller components may not reflow
- Use stepped reflow profiles
- Consider component placement order
```

#### Heat-sensitive components
```
Temperature-sensitive parts:
- Electrolytic capacitors
- Crystal oscillators  
- Plastic connectors
- Some LEDs i displays

Protection strategies:
- Place away from high-temp areas
- Use heat sinks dla protection
- Lower temperature profiles
- Manual placement after reflow
```

## 🧪 Quality control

### Inspection methods

#### Visual inspection
```
Manual inspection points:
- Solder joint quality
- Component orientation
- Missing/wrong components
- Solder bridges
- Insufficient solder

Inspection aids:
- Magnification (5-20×)
- Good lighting (daylight balanced)
- Inspection standards (IPC-A-610)
- Training i certification
```

#### Automated Optical Inspection (AOI)
```
AOI capabilities:
- Component presence/absence
- Component orientation
- Solder joint quality
- Bridge detection
- Coplanarity measurement

Limitations:
- Cannot detect internal defects
- Hidden solder joints
- Electrical functionality
- Requires good programming
```

#### X-ray inspection
```
AXI applications:
- BGA solder joint inspection
- Hidden solder joints
- Void detection in solder
- Component internal structure
- Counterfeit component detection

Advanced features:
- 3D X-ray capability
- CT (computed tomography)
- Real-time inspection
- Automated defect classification
```

### Testing methods

#### In-Circuit Test (ICT)
```
ICT capabilities:
- Component value verification
- Short/open detection
- Basic digital IC testing
- Analog measurements
- Boundary scan testing

Limitations:
- Requires test fixture
- Access to nodes required
- Limited fault coverage dla complex ICs
- High setup costs
```

#### Functional testing
```
Functional test benefits:
- Tests actual product functionality
- High fault coverage
- Real operating conditions
- User interface validation
- Software integration testing

Implementation:
- Custom test fixtures
- Test software development
- Pass/fail criteria definition
- Data logging i traceability
```

## 🔍 Common assembly defects

### Solder joint defects

#### Insufficient solder
```
Causes:
- Inadequate paste volume
- Poor wetting
- Component placement errors
- Reflow profile issues

Detection:
- Visual inspection
- X-ray dla hidden joints
- Electrical testing
- Pull testing (destructive)
```

#### Solder bridges
```
Prevention:
- Proper stencil design
- Accurate component placement  
- Optimized reflow profile
- Good solder mask design

Repair:
- Desoldering braid removal
- Hot air rework
- Flux application
- Component replacement
```

### Placement defects

#### Component misalignment
```
Causes:
- Pick and place accuracy
- Component package tolerances
- PCB warpage
- Vision system calibration

Acceptance criteria:
- IPC standards (IPC-A-610)
- Customer specifications
- Electrical functionality
- Mechanical requirements
```

#### Tombstoning
```
Tombstoning causes:
- Unbalanced thermal mass
- Paste volume imbalance
- Component placement pressure
- Reflow profile issues

Prevention:
- Balanced pad design
- Proper paste printing
- Thermal design optimization
- Component placement verification
```

## 🌡️ Environmental considerations

### Lead-free assembly

#### RoHS compliance
```
Lead-free requirements:
- Solder alloys: SAC305, SAC387
- Component terminations: lead-free
- Process temperatures: higher than leaded
- Reliability considerations

Implementation:
- Equipment upgrades
- Process optimization
- Staff training
- Documentation updates
```

#### Process changes
```
Lead-free impacts:
- Higher reflow temperatures
- Different flux chemistry
- Component reliability
- Rework procedures

Validation requirements:
- Thermal cycling testing
- Mechanical shock testing
- Long-term reliability
- Process capability studies
```

### ESD protection

#### ESD control program
```
ESD protection requirements:
- Grounded workstations
- Wrist straps i heel grounders
- ESD-safe tools i equipment
- Component handling procedures
- Training i auditing

Standards compliance:
- ANSI/ESD S20.20
- IEC 61340 series
- JEDEC standards
- Customer specifications
```

## 📊 Assembly documentation

### Work instructions

#### Assembly procedures
```
Documentation requirements:
- Bill of materials (BOM)
- Assembly drawings
- Pick and place files
- Reflow profiles
- Test procedures
- Quality standards

Version control:
- Document revision tracking
- Change approval process
- Training on updates
- Archive management
```

### Traceability

#### Manufacturing records
```
Traceability data:
- PCB lot/serial numbers
- Component lot codes
- Process parameters
- Operator identification
- Test results
- Rework records

Benefits:
- Quality control
- Problem investigation
- Regulatory compliance
- Customer requirements
- Field failure analysis
```

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_komponenty_elektroniczne|Komponenty Elektroniczne]] - component knowledge
- [[pcb_produkcja_wytwarzanie|Produkcja PCB]] - PCB manufacturing
- [[pcb_testowanie_debug|Testowanie i Debug]] - testing assembled PCBs
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - DFA guidelines
- [[pcb_bledy_czestie|Częste Błędy]] - assembly-related mistakes
- [[pcb_thermal_management|Zarządzanie Cieplne]] - thermal considerations

---

**🎯 Co dalej?**
Po zrozumieniu montażu komponentów, przejdź do [[pcb_testowanie_debug|Testowania i Debug]] aby nauczyć się weryfikować zmontowane PCB, lub [[pcb_thermal_management|Zarządzania Cieplnego]] dla thermal design considerations.