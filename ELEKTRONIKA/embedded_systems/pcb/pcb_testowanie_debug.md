# Testowanie i Debug PCB

## 🎯 Wprowadzenie

Testowanie i debugowanie PCB to krytyczny proces weryfikacji, czy zaprojektowana płytka działa zgodnie ze specyfikacją. Właściwe zaplanowanie testów na etapie projektowania i systematyczne podejście do rozwiązywania problemów może znacznie skrócić czas rozwoju produktu.

## 🔍 Strategia testowania

### Test-driven design

#### Projektowanie z myślą o testowaniu
```
Design for Test (DFT) principles:
☐ Test points na critical nets
☐ Debug connectors (UART, JTAG)
☐ Status indicators (LEDs)
☐ Probe access to power rails
☐ Isolation jumpers dla modules
☐ Test modes i factory settings
```

#### Hierarchical testing approach
```
Level 1: Component level
- Individual IC functionality
- Power supply rails
- Clock signals
- Reset circuits

Level 2: Module level  
- Functional blocks
- Interface testing
- Communication protocols
- Timing verification

Level 3: System level
- End-to-end functionality
- Performance testing
- Environmental testing
- Compliance verification
```

### Test planning

#### Test specification
```
Test categories:
1. Bring-up tests: basic functionality
2. Functional tests: specification compliance
3. Performance tests: timing, accuracy
4. Stress tests: limits i margins
5. Environmental tests: temperature, humidity
6. Compliance tests: EMC, safety
```

## ⚡ Electrical testing

### Power system verification

#### Voltage measurements
```
Power rail testing:
☐ Input voltage ranges
☐ Regulator output voltages
☐ Load regulation (no-load to full-load)
☐ Line regulation (input voltage variation)
☐ Ripple i noise measurements
☐ Transient response
☐ Efficiency measurements

Test points requirements:
- Accessible with probe
- Adequate spacing (2.54mm minimum)
- Ground references nearby
- Labeled clearly on PCB
```

#### Current consumption
```
Current measurement points:
- Total system current
- Individual supply rails
- Sleep/standby currents
- Peak current during operation

Tools needed:
- DMM z current ranges
- Current probes for non-invasive
- Electronic load for testing
- Oscilloscope dla transients
```

### Signal integrity testing

#### Digital signals
```
Critical parameters:
- Logic levels: VIH, VIL, VOH, VOL
- Rise/fall times
- Setup i hold times
- Clock jitter i skew
- Eye diagrams dla high-speed

Test equipment:
- Digital oscilloscope: >200MHz BW
- Logic analyzer: dla bus analysis
- TDR: transmission line testing
- Spectrum analyzer: EMI assessment
```

#### Analog signals
```
AC characteristics:
- Frequency response
- THD (Total Harmonic Distortion)
- SNR (Signal-to-Noise Ratio)
- Input/output impedances
- Offset voltages i bias currents

DC characteristics:
- Transfer functions
- Linearity
- Temperature coefficients
- Power supply rejection
```

### Communication interfaces

#### Serial protocols
```
UART testing:
- Baud rate accuracy
- Start/stop bit timing
- Parity error handling
- Flow control (RTS/CTS)

SPI testing:
- Clock polarity i phase
- Data setup i hold times
- Chip select timing
- Multi-slave operation

I2C testing:
- Clock stretching
- Address acknowledgment
- Bus arbitration
- Pull-up resistor values
```

## 🛠️ Debug infrastructure

### Hardware debug features

#### Debug connectors
```
JTAG/SWD interface:
- Standard pinout (ARM 10-pin)
- Accessible placement
- Proper pull-ups/pull-downs
- Target power sensing

UART debug:
- TX/RX pins broken out
- Ground reference
- Optional flow control
- Logic level compatibility (3.3V/5V)
```

#### Test points
```
Essential test points:
☐ All power rails (VCC, VDD, analog supplies)
☐ Ground references
☐ Clock signals (main oscillator, PLL outputs)
☐ Reset signals (power-on, watchdog)
☐ Critical control signals
☐ Analog references

Physical requirements:
- Minimum 1.0mm diameter dla probing
- 2.54mm spacing dla test clips
- Via or pad accessible from top
- Clear labeling on silkscreen
```

### Software debug capabilities

#### Embedded debug features
```
Debug output:
- Printf-style debug messages
- Variable monitoring
- Function call tracing
- Performance profiling
- Error logging

Debug commands:
- Memory read/write
- Register access
- Peripheral control
- Test mode activation
- Calibration routines
```

#### Built-in self-test (BIST)
```
Test categories:
- Memory tests (RAM, Flash)
- Peripheral loopback tests
- A/D converter linearity
- Clock frequency verification
- Communication interface tests

Implementation:
- Factory test mode
- Power-on self-test
- Periodic health checks
- Error reporting mechanisms
```

## 🔧 Test equipment

### Basic instruments

#### Multimeter (DMM)
```
Required specifications:
- Voltage: 0.1mV resolution
- Current: µA to A ranges
- Resistance: 0.1Ω to 100MΩ
- Frequency: kHz range
- True RMS dla AC measurements

Applications:
- DC voltage/current measurements
- Continuity testing
- Component value verification
- Basic AC measurements
```

#### Oscilloscope
```
Minimum requirements:
- Bandwidth: 100MHz (preferably 200MHz+)
- Sample rate: 1GSa/s minimum
- Channels: 4 channels recommended
- Memory depth: 10Mpts minimum
- Trigger options: edge, pulse width, protocol

Advanced features:
- Serial protocol decoding (UART, SPI, I2C)
- Math functions (FFT, filtering)
- Automated measurements
- Reference waveform storage
```

### Advanced instruments

#### Logic analyzer
```
Applications:
- Digital bus analysis
- Protocol decoding  
- Timing diagram generation
- State machine debugging
- Multi-channel correlation

Specifications:
- Channels: 16+ for complex systems
- Sample rate: 100MSa/s minimum
- Memory depth: protocol dependent
- Trigger capabilities: pattern, state
```

#### Spectrum analyzer
```
EMI/EMC testing:
- Frequency range: 9kHz to 1GHz minimum
- Dynamic range: >70dB
- RBW: 9kHz to 1MHz
- Noise floor: -120dBm typical

Applications:
- Conducted emission testing
- Clock harmonic analysis
- Spurious signal detection
- Filter response verification
```

### Specialized tools

#### Network analyzer
```
RF applications:
- S-parameter measurements
- Impedance measurements  
- Filter characterization
- Antenna testing
- Cable testing (TDR/TDT)

Frequency coverage:
- Low frequency: 1Hz to 110MHz
- High frequency: up to 67GHz
```

#### Power analyzer
```
Switching supply testing:
- Efficiency measurements
- Power factor analysis
- Harmonic analysis
- Transient response
- Thermal analysis
```

## 🐛 Systematic debugging

### Problem isolation

#### Divide and conquer
```
Systematic approach:
1. Identify symptoms clearly
2. List possible causes
3. Test hypotheses systematically
4. Isolate problem area
5. Implement fix
6. Verify solution

Documentation:
- Problem description
- Test results
- Root cause analysis
- Fix implementation
- Verification data
```

#### Signal tracing
```
Debug methodology:
- Start from known good point
- Trace signal path step by step
- Compare expected vs actual
- Identify first failure point
- Focus debugging effort there

Tools:
- Oscilloscope dla analog/digital
- Logic analyzer dla digital buses
- DMM dla DC measurements
- Current probes dla power analysis
```

### Common failure modes

#### Power system issues
```
Symptoms i causes:
No power:
- Input voltage absent
- Fuse blown
- Regulator failure
- Short circuit

Wrong voltage:
- Incorrect feedback network
- Regulator oscillation
- Load regulation problems
- Thermal shutdown

Excessive ripple:
- Insufficient filtering
- ESR too high
- Layout issues (ground loops)
- Switching noise coupling
```

#### Digital circuit problems
```
Logic level issues:
- Voltage levels outside specs
- Loading problems (fan-out)
- Pull-up/pull-down missing
- Level shifting required

Timing problems:
- Setup/hold violations
- Clock skew
- Propagation delays
- Metastability

Communication failures:
- Protocol timing violations
- Incorrect termination
- Noise coupling
- Ground potential differences
```

## 📊 Test automation

### Automated test equipment

#### In-circuit test (ICT)
```
Capabilities:
- Component value verification
- Short/open testing
- Digital IC functional tests
- Analog circuit measurements

Limitations:
- Test fixture cost
- Access requirements
- Limited fault coverage dla complex ICs
- Programming time dla complex tests
```

#### Functional test
```
System-level testing:
- End-to-end functionality
- Performance verification
- Calibration procedures
- Quality assurance

Advantages:
- High fault coverage
- Real operating conditions
- User interface testing
- Software integration
```

### Test data management

#### Test documentation
```
Test records should include:
☐ Test procedure followed
☐ Equipment used (model, calibration date)
☐ Test conditions (temperature, humidity)
☐ Pass/fail results
☐ Measurement data
☐ Operator identification
☐ Date i time

Statistical analysis:
- Yield tracking
- Failure mode analysis
- Process capability (Cpk)
- Trend analysis
```

#### Failure analysis
```
Documentation requirements:
- Failure symptoms
- Test conditions when failed
- Root cause investigation
- Corrective actions taken
- Prevention measures
- Lessons learned

Database management:
- Searchable failure records
- Statistical trending
- Corrective action tracking
- Knowledge base building
```

## 🎯 Troubleshooting techniques

### Root cause analysis

#### 5 Whys methodology
```
Example:
Problem: LED doesn't light up
Why 1: No current through LED
Why 2: Voltage too low at LED
Why 3: Excessive voltage drop in resistor
Why 4: Wrong resistor value installed  
Why 5: BOM error in component specification

Root cause: Incorrect BOM specification
Solution: Update BOM and procurement process
```

#### Fishbone analysis
```
Categories dla PCB problems:
- Design: schematic errors, layout issues
- Components: wrong values, defective parts
- Manufacturing: assembly errors, process issues
- Testing: inadequate procedures, equipment
- Environment: temperature, humidity, vibration
```

### Debug strategies

#### Incremental testing
```
Build-up approach:
1. Power supply only
2. Add MCU and basic clocking
3. Add communication interfaces
4. Add peripheral functions
5. Add software functionality

Benefits:
- Easier problem isolation
- Faster debugging
- Reduced variables
- Systematic verification
```

#### Substitution testing
```
Component swapping:
- Replace suspect components
- Use known good boards
- Swap modules between systems
- Use external signal sources

Advantages:
- Quick fault isolation
- Definitive component testing
- Cross-reference verification
```

## 📋 Documentation i reporting

### Test reports

#### Standard format
```
Test report sections:
1. Executive summary
2. Test objectives
3. Test setup i equipment
4. Test procedures
5. Results i analysis
6. Conclusions i recommendations
7. Appendices (raw data)

Compliance requirements:
- IPC standards references
- Regulatory requirements
- Customer specifications
- Internal quality standards
```

### Design review feedback

#### Lessons learned
```
Design improvements:
- Test point additions
- Debug connector improvements
- Component placement optimization
- Signal routing changes

Process improvements:
- Design rule updates
- Review checklist additions
- Tool/equipment upgrades
- Training needs identification
```

## 🔗 Powiązane tematy
- [[pcb_design|Projektowanie PCB]] - główny indeks
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - DFT considerations
- [[pcb_bledy_czestie|Częste Błędy]] - common failure modes
- [[pcb_produkcja_wytwarzanie|Produkcja PCB]] - manufacturing test
- [[pcb_emi_emc|EMI/EMC]] - compliance testing
- [[pcb_projekty_praktyczne|Projekty Praktyczne]] - praktyczne testing
- [[embedded_systems_index|Systemy Wbudowane]] - software debug integration

---

**🎯 Co dalej?**
Po opanowaniu testowania i debugowania, wróć do [[pcb_projekty_praktyczne|Projektów Praktycznych]] aby zastosować zdobytą wiedzę, lub przejdź do zaawansowanych tematów jak [[pcb_emi_emc|EMI/EMC]] czy [[pcb_impedancja_kontrolowana|Impedancja Kontrolowana]].