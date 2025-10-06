# Routing Ścieżek - Techniki Prowadzenia

## 🎯 Wprowadzenie

Routing ścieżek to proces tworzenia fizycznych połączeń elektrycznych między komponentami na PCB. To jeden z najważniejszych i najbardziej wymagających etapów projektowania PCB, który bezpośrednio wpływa na wydajność, niezawodność i EMI układu.

## 🛤️ Podstawy routingu

### Co to jest routing?

#### Definicja
- **Routing**: tworzenie ścieżek miedzianych (traces) łączących komponenty
- **Net**: logiczne połączenie między pinami
- **Track/Trace**: fizyczna ścieżka miedziana na PCB
- **Via**: połączenie między warstwami

#### Cele routingu
- **Connectivity**: wszystkie nets połączone
- **Signal integrity**: zachowanie jakości sygnałów
- **EMI compliance**: minimalizacja zakłóceń
- **Manufacturing**: zgodność z zasadami produkcji

### Typy połączeń

#### Point-to-point
```
Component A ────────────► Component B
```
- **Zastosowanie**: pojedyncze sygnały
- **Optymalizacja**: minimalna długość

#### Multi-point (Star)
```
        Component A
             │
Component B ─┼─ Component C
             │
        Component D
```
- **Zastosowanie**: sygnały zasilania, clock
- **Kontrola**: impedancja, timing

#### Daisy chain
```
Comp A ──► Comp B ──► Comp C ──► Comp D
```
- **Zastosowanie**: magistrale danych
- **Uwaga**: propagation delay

## 📏 Szerokości ścieżek

### Obliczanie szerokości

#### Wzór podstawowy (IPC-2221)
```
Area [mil²] = (Current [A] / (k × ΔT[°C]^b))^(1/c)

gdzie:
k = 0.048 (external), 0.024 (internal)
b = 0.44
c = 0.725
ΔT = przyrost temperatury
```

#### Przykładowe szerokości
```
Prąd [A]  External [mm]  Internal [mm]  Uwagi
0.1       0.08           0.11           Sygnały cyfrowe
0.5       0.20           0.30           GPIO, I/O
1.0       0.40           0.65           Zasilanie lokalne
2.0       0.80           1.30           Zasilanie główne
5.0       2.0            3.0            High power
```

### Praktyczne guidelines

#### Minimalne szerokości
- **Signal traces**: 0.1mm (4 mil) minimum
- **Power traces**: calculate based on current
- **Ground**: use plane when possible
- **High-frequency**: impedance controlled

#### Standardowe wartości
```
0.1mm (4 mil)   - minimum, light signals
0.15mm (6 mil)  - safe minimum, general I/O  
0.2mm (8 mil)   - preferred minimum
0.25mm (10 mil) - comfortable for hand routing
0.3mm (12 mil)  - power distribution
0.5mm+ (20 mil) - high current paths
```

## 🎯 Strategie routingu

### Hierarchia routingu

#### 1. Critical nets first
```
Priority 1: Power, Ground
Priority 2: Clocks, Reset
Priority 3: High-speed signals  
Priority 4: Analog signals
Priority 5: General I/O
```

#### 2. Routing order
1. **Power distribution**: planes and heavy traces
2. **Ground connections**: return paths
3. **Clock signals**: timing-critical
4. **High-speed digital**: fast edges
5. **Analog signals**: sensitive to noise
6. **Low-speed digital**: remaining connections

### Routing techniques

#### Manual routing
- **Full control**: designer controls every trace
- **Optimization**: optimal for critical signals
- **Time**: labor-intensive
- **Skill**: requires experience

#### Auto-routing
- **Speed**: fast completion
- **Consistency**: uniform approach
- **Limitations**: may not be optimal
- **Post-processing**: usually needs cleanup

#### Interactive routing
- **Balance**: human guidance + tool assistance
- **Modern approach**: current best practice
- **Flexibility**: adjust strategy as needed

## 📐 Design rules dla routingu

### Spacing rules

#### Minimum clearances
```
Feature              Minimum [mm]
Trace to trace       0.1
Trace to pad         0.1  
Via to via          0.2
Via to trace        0.1
Pad to board edge   0.2
```

#### High-voltage clearances
```
Voltage [V]    Air Gap [mm]    PCB Surface [mm]
12             0.1             0.1
24             0.2             0.2
48             0.4             0.4
110            1.0             1.6
230            2.0             3.2
```

### Via rules

#### Standard vias
- **Drill size**: 0.15mm minimum, 0.2mm preferred
- **Pad size**: drill + 0.1mm minimum annular ring
- **Aspect ratio**: depth:diameter < 8:1

#### Via placement
- **Via in pad**: avoid for THT components
- **Via tenting**: cover with solder mask
- **Via fill**: filled vias for high-frequency

## ⚡ High-speed routing

### Signal integrity considerations

#### Trace impedance
```
Z₀ = 87/√(εᵣ+1.41) × ln(5.98h/(0.8w+t))

dla microstrip na zewnętrznej warstwie
```

#### Critical parameters
- **Rise time**: faster edges more sensitive
- **Trace length**: electrical length matters
- **Impedance**: maintain characteristic impedance
- **Termination**: proper line termination

### Length matching

#### When needed
- **Clock distribution**: minimize skew
- **High-speed data**: synchronous interfaces
- **Differential pairs**: maintain pair matching
- **Memory interfaces**: DDR, QDR signals

#### Techniques
```
Serpentine routing:
═════╗     ╔═════
     ║     ║
     ╚═════╝

Trombone routing:
═══╗ ╔═╗ ╔═══
   ╚═╝ ╚═╝
```

#### Tolerances
```
Application         Tolerance
Audio              ±25%
Low-speed digital  ±10%
High-speed digital ±5%
DDR memory         ±0.05mm
RF/microwave       ±0.01mm
```

## 🔄 Differential pairs

### Basics
- **Differential signaling**: sygnał przesyłany jako różnica
- **Common mode rejection**: odporność na zakłócenia
- **Applications**: USB, Ethernet, HDMI, SATA

### Routing rules

#### Trace parameters
```
Differential impedance: typically 90Ω, 100Ω
Single trace impedance: ~45Ω, 50Ω
Trace spacing: 3× trace width minimum
```

#### Layout guidelines
- **Keep pairs together**: minimize separation
- **Equal lengths**: match within 0.1mm
- **Avoid vias**: minimize via usage
- **Reference plane**: continuous ground beneath

#### Via handling
```
Good: Symmetric via placement
P ○─────────○ P
N ○─────────○ N

Bad: Asymmetric vias  
P ○───────── P
N ○────○──── N
```

## 🌐 Power routing

### Power distribution strategies

#### Power planes
- **Dedicated layers**: most efficient for high current
- **Uniform distribution**: even voltage across board
- **Low impedance**: minimized voltage drop
- **Thermal**: heat spreading

#### Power traces
- **Point-to-point**: specific power delivery
- **Star distribution**: from central point
- **Tree structure**: branching distribution
- **Mesh**: redundant paths

### Current calculations

#### Voltage drop
```
V_drop = I × R × L / A

gdzie:
I = current [A]
R = resistivity [Ω⋅mm²/m]
L = length [mm]  
A = cross-sectional area [mm²]
```

#### Temperature rise
```
Copper resistivity increases ~0.4%/°C
Account for temperature in calculations
Use derating factors for safety
```

### Decoupling strategy

#### Capacitor placement
- **Close to IC**: minimize inductance
- **Multiple values**: different frequency ranges
- **Via placement**: direct connection to planes

```
Decoupling hierarchy:
10μF - bulk decoupling (low frequency)
1μF - intermediate frequency
100nF - high frequency (close to IC)
10nF - very high frequency  
1nF - ultra high frequency
```

## 📡 Analog routing

### Analog-specific considerations

#### Sensitive signals
- **Keep short**: minimize noise pickup
- **Shield**: ground planes or guard traces
- **Separate**: from digital switching signals
- **Layout**: star ground configuration

#### Ground separation
```
Digital Ground ≠ Analog Ground

Connection strategy:
- Single point connection
- Ferrite bead isolation
- Separate planes with bridge
```

### Noise reduction

#### Shielding techniques
```
Guard traces:
Signal ─────────────
GND   ═════════════  ← Guard trace
GND   ═════════════
```

#### Filtering
- **RC filters**: simple noise reduction
- **Ferrite beads**: high-frequency suppression
- **Common mode chokes**: differential filtering

## 🛠️ Routing tools i techniques

### CAD tool features

#### Modern routing engines
- **Push and shove**: dynamic obstacle avoidance
- **Length tuning**: automatic serpentine
- **Differential pairs**: paired routing
- **Interactive**: real-time feedback

#### Routing strategies
```
Settings example:
- Via cost: high (minimize usage)
- Layer changes: medium cost  
- Direction preference: horizontal/vertical
- Trace width: optimize for current
```

### Manual optimization

#### Post-routing cleanup
- **Minimize vias**: reduce layer changes
- **Smooth traces**: remove unnecessary bends
- **Optimize length**: shortest practical routes
- **Check clearances**: verify design rules

#### Visual inspection
- **45° angles**: avoid 90° bends where possible
- **Trace consistency**: uniform appearance
- **Symmetry**: balanced layouts
- **Accessibility**: test points, debug access

## 🔍 Verification i testing

### Design Rule Check (DRC)

#### Electrical verification
- **Connectivity**: all nets connected
- **Clearances**: minimum spacings maintained
- **Via rules**: proper via specifications
- **Current capacity**: adequate trace widths

#### Manufacturing verification
- **Minimum features**: achievable by fab
- **Drill sizes**: available tooling
- **Aspect ratios**: manufacturable vias
- **Registration**: alignment tolerances

### Signal integrity analysis

#### Pre-layout planning
- **Stackup design**: impedance targets
- **Critical nets**: identify sensitive signals
- **Constraints**: timing, length, impedance

#### Post-layout verification
- **Impedance**: verify controlled impedance
- **Crosstalk**: check coupling between traces
- **Timing**: signal arrival times
- **EMI**: potential radiation issues

## 🎯 Best practices

### General guidelines

#### Planning
- **Start with constraints**: define rules first
- **Critical nets first**: route important signals early
- **Layer assignment**: plan signal layers
- **Power first**: establish power distribution

#### Execution
- **Grid alignment**: use design grid
- **45° routing**: prefer over 90° angles
- **Via minimization**: reduce layer changes
- **Symmetry**: balanced layouts

#### Optimization
- **Length optimization**: minimize trace length
- **Via optimization**: consolidate layer changes
- **Clearance maximization**: exceed minimums where possible
- **Test accessibility**: provide test points

### Common mistakes

#### Electrical
- **Inadequate trace width**: voltage drop, heating
- **Poor grounding**: noise, EMI issues
- **Missing termination**: signal integrity problems
- **Crosstalk**: insufficient spacing

#### Manufacturing
- **Acid traps**: acute angles in copper
- **Via in pad**: assembly issues
- **Minimum features**: unmanufacturable designs
- **Poor registration**: overlay misalignment

## 🔗 Powiązane tematy
- [[pcb_projekt_layoutu|Projekt Layoutu]] - ogólny proces layoutu
- [[pcb_warstwy_pcb|Warstwy PCB]] - struktura wielowarstwowa
- [[pcb_via_i_drillholes|Via i Otwory]] - połączenia między warstwami
- [[pcb_plane_zasilania|Płaszczyzny Zasilania]] - power distribution
- [[pcb_plane_masy|Płaszczyzny Masy]] - ground distribution
- [[pcb_impedancja_kontrolowana|Impedancja Kontrolowana]] - kontrola impedancji
- [[pcb_emi_emc|EMI/EMC]] - zagadnienia elektromagnetyczne
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - sprawdzone metody

---

**🎯 Co dalej?**
Po opanowaniu routingu, przejdź do [[pcb_via_i_drillholes|Via i Otworów]] aby zrozumieć połączenia między warstwami, lub [[pcb_impedancja_kontrolowana|Impedancji Kontrolowanej]] dla zaawansowanych aplikacji.