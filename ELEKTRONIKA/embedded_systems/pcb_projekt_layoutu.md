# Projekt Layoutu PCB

## 🎯 Wprowadzenie

Layout PCB to proces przekształcania schematu elektrycznego w fizyczną płytkę drukowaną. To kluczowy etap, w którym projektant określa fizyczne rozmieszczenie komponentów i prowadzenie ścieżek przewodzących. Dobry layout wpływa na wydajność, niezawodność i koszt produkcji układu.

## 🎨 Proces projektowania layoutu

### Etapy projektowania

#### 1. Przygotowanie
- **Import schematu**: netlist z narzędzia schematic
- **Weryfikacja**: sprawdzenie kompletności schematu
- **Założenia**: rozmiar PCB, liczba warstw, technologia
- **Constrains**: ograniczenia mechaniczne i elektryczne

#### 2. Planowanie układu
- **Board outline**: kształt i rozmiar płytki
- **Mounting holes**: otwory montażowe
- **Connector placement**: umiejscowienie złączy
- **Critical components**: komponenty krytyczne położenie

#### 3. Rozmieszczenie komponentów (Placement)
- **Functional blocks**: grupowanie funkcjonalne
- **Thermal considerations**: zarządzanie ciepłem
- **Signal flow**: kierunek przepływu sygnałów
- **Manufacturing**: dostępność do montażu i testowania

#### 4. Routing ścieżek
- **Power planes**: płaszczyzny zasilania i masy
- **Critical signals**: sygnały wysokiej częstotliwości
- **General routing**: pozostałe połączenia
- **Optimization**: optymalizacja długości i impedancji

#### 5. Weryfikacja i finalizacja
- **DRC**: Design Rules Check
- **ERC**: Electrical Rules Check
- **Manufacturing files**: Gerber, drill files
- **Assembly drawings**: dokumentacja montażu

## 📏 Planowanie rozmiaru PCB

### Standardowe rozmiary

#### Popularne formaty
- **Euro Card**: 100mm × 160mm
- **Half Euro Card**: 100mm × 80mm
- **Credit Card**: 85.6mm × 53.98mm
- **Arduino Uno**: 68.6mm × 53.4mm
- **Custom sizes**: dopasowane do aplikacji

### Ograniczenia rozmiarów

#### Koszty produkcji
- **Standard panels**: 100×100mm często najtańsze
- **Panel utilization**: optymalne wykorzystanie panelu
- **Tooling costs**: specjalne rozmiary = dodatkowy koszt

#### Mechaniczne ograniczenia
- **Enclosure**: dopasowanie do obudowy
- **Mounting**: otwory montażowe
- **Connector positions**: położenie złączy
- **Heat sinks**: miejsce na radiatory

## 🏗️ Rozmieszczenie komponentów

### Zasady placement

#### Grupowanie funkcjonalne
```
[Power Supply] ──→ [MCU] ──→ [Peripherals]
      ↓            ↓           ↓
   [Analog]    [Digital]   [Interface]
```

#### Kierunek przepływu sygnału
- **Left to right**: wejście → przetwarzanie → wyjście  
- **Top to bottom**: zasilanie → sygnały → masa
- **Minimize crossings**: unikaj krzyżowania się sygnałów

### Considerations dla placement

#### Elektryczne
- **High-speed signals**: krótkie połączenia
- **Analog/Digital separation**: fizyczna separacja
- **Power distribution**: równomierne rozmieszczenie
- **Ground connections**: minimalne impedancje

#### Termalne
- **Heat generating**: komponenty grzejące się z dala od wrażliwych
- **Thermal vias**: odprowadzanie ciepła przez warstwy
- **Air flow**: kierunek przepływu powietrza
- **Heat sinks**: miejsce na radiatory

#### Mechaniczne
- **Component height**: wysokość komponentów
- **Keepout zones**: obszary niedostępne
- **Connector accessibility**: dostęp do złączy
- **Test points**: punkty testowe dostępne

### Orientacja komponentów

#### Jednolita orientacja
- **IC orientation**: wszystkie w tym samym kierunku
- **Polarized components**: konsystentny kierunek
- **Text readability**: etykiety czytelne z jednego kierunku

#### Exceptions
- **Optimal routing**: czasem ważniejszy od jednolitości
- **Mechanical constraints**: ograniczenia fizyczne
- **Thermal**: optymalne odprowadzanie ciepła

## 🛤️ Podstawy routingu

### Hierarchia routingu

#### 1. Power i Ground
- **Power planes**: płaszczyzny zasilania
- **Ground planes**: płaszczyzny masy  
- **Power routing**: szerokie ścieżki zasilania
- **Decoupling**: kondensatory odsprzęgające

#### 2. Clock signals
- **Clock distribution**: równomierne rozprowadzenie
- **Length matching**: dopasowanie długości
- **Shielding**: ekranowanie od zakłóceń
- **Termination**: zakończenie linii transmisyjnych

#### 3. High-speed signals
- **Differential pairs**: sygnały różnicowe
- **Impedance control**: kontrola impedancji
- **Via minimization**: minimalna liczba via
- **Crosstalk**: redukcja przesłuchów

#### 4. General I/O
- **Remaining connections**: pozostałe połączenia
- **Optimization**: optymalizacja długości
- **Via usage**: wykorzystanie via
- **DRC compliance**: zgodność z zasadami

### Track width guidelines

#### Określanie szerokości ścieżek
```
Wzór na szerokość ścieżki (IPC-2221):
A = (I / (k × (T_rise)^b))^(1/c)

gdzie:
I = prąd [A]
A = area [mil²]  
k, b, c = stałe zależne od warstwy
T_rise = przyrost temperatury [°C]
```

#### Praktyczne wartości
```
Moc [A]     Min Width [mm]    Recommended [mm]
0.1         0.1               0.15
0.5         0.2               0.3
1.0         0.4               0.6
2.0         0.8               1.0
5.0         2.0               2.5
```

#### Via current capacity
```
Via Size    Current [A]
0.2mm       0.5A
0.3mm       1.0A
0.5mm       2.0A
0.8mm       4.0A
```

### Clearances i spacings

#### Minimum clearances
- **Track to track**: 0.1mm (budget), 0.15mm (safe)
- **Track to pad**: 0.1mm minimum
- **Via to via**: 0.2mm minimum  
- **Pad to board edge**: 0.2mm minimum

#### High voltage clearances
```
Voltage [V]    Clearance [mm]
50             0.25
100            0.5
250            1.0
500            2.0
1000           4.0
```

## 🔄 Strategie routingu

### Manual routing
- **Full control**: pełna kontrola nad każdą ścieżką
- **Optimal results**: najlepsze wyniki dla critical signals
- **Time consuming**: czasochłonne dla dużych projektów
- **Experience required**: wymaga doświadczenia

### Auto-routing
- **Speed**: szybkie dla prostych projektów
- **Consistency**: jednolite podejście
- **Limited optimization**: ograniczone możliwości
- **Post-processing**: wymaga ręcznych poprawek

### Interactive routing
- **Balanced approach**: połączenie manual + auto
- **Guidance**: narzędzie proponuje rozwiązania
- **User control**: użytkownik ma ostateczną kontrolę
- **Modern tools**: obecne w nowoczesnych CAD

### Push and shove routing
- **Dynamic adjustment**: automatyczne przesuwanie ścieżek
- **Conflict resolution**: rozwiązywanie kolizji
- **Real-time feedback**: natychmiastowa informacja zwrotna
- **Professional tools**: dostępne w zaawansowanych narzędziach

## 📐 Zasady projektowe (Design Rules)

### Electrical rules

#### Minimum track width
- **Signal traces**: 0.1mm (4 mil) budget, 0.15mm (6 mil) safe
- **Power traces**: calculate based on current
- **High-frequency**: impedance-controlled

#### Minimum spacing
- **Same net**: touching allowed
- **Different nets**: minimum clearance
- **High voltage**: increased clearance
- **AC vs DC**: różne wymagania

### Mechanical rules

#### Via rules
- **Minimum size**: 0.15mm drill, 0.25mm pad
- **Annular ring**: minimum 0.05mm
- **Via in pad**: avoid for THT components
- **Tenting**: covered with solder mask

#### Drilling rules
- **Minimum drill**: 0.1mm possible, 0.15mm recommended
- **Drill tolerance**: ±0.05mm typical
- **Aspect ratio**: hole depth to diameter <8:1
- **Tool wear**: smaller holes wear tools faster

### Manufacturing rules

#### Solder mask
- **Minimum opening**: 0.1mm larger than pad
- **Bridge width**: minimum 0.1mm between openings
- **Registration**: alignment tolerance ±0.05mm

#### Silk screen
- **Minimum line width**: 0.15mm
- **Minimum text height**: 1.0mm
- **Color contrast**: white on green, black on white
- **Overlap**: avoid over pads or vias

## 📊 Layer stackup

### 2-layer PCB
```
Layer 1: Components + Signals (Top)
Core: FR-4 substrate (1.6mm)
Layer 2: Signals + Ground (Bottom)
```
- **Cost**: lowest
- **Complexity**: suitable for simple designs
- **Routing**: limited routing resources

### 4-layer PCB  
```
Layer 1: Components + Signals (Top)
Layer 2: Ground Plane
Core: FR-4 substrate
Layer 3: Power Plane  
Layer 4: Signals (Bottom)
```
- **Benefits**: improved EMI, better power distribution
- **Cost**: moderate increase
- **Complexity**: suitable for most designs

### 6+ layer PCB
```
L1: Components + Signals
L2: Ground Plane
L3: Signals
L4: Power Plane
L5: Signals  
L6: Signals + Solder Mask
```
- **Applications**: high-speed, complex designs
- **Cost**: higher
- **Performance**: excellent EMI and signal integrity

## 🔧 Via technology

### Via types

#### Through-hole vias
- **Span**: all layers
- **Manufacturing**: standard drilling
- **Cost**: lowest
- **Usage**: general connections

#### Blind vias
- **Span**: outer to inner layer
- **Manufacturing**: controlled depth drilling
- **Cost**: moderate increase
- **Usage**: high-density designs

#### Buried vias
- **Span**: internal layers only
- **Manufacturing**: sequential lamination
- **Cost**: highest
- **Usage**: ultra-high density

### Via placement strategy

#### Power distribution
- **Multiple vias**: parallel for high current
- **Distributed**: even power distribution
- **Thermal**: heat dissipation path
- **Decoupling**: direct connections

#### Signal routing
- **Minimize usage**: each via adds inductance
- **Layer changes**: necessary for routing
- **Impedance**: consider via impedance
- **Return path**: ground vias for signals

## 🌡️ Thermal considerations

### Heat dissipation strategies

#### Component placement
- **Heat sources**: identify power-dissipating components
- **Isolation**: separate from temperature-sensitive
- **Air flow**: position for cooling airflow
- **Heat sinks**: space for thermal management

#### PCB techniques
- **Thermal vias**: conduct heat through layers
- **Copper pours**: heat spreading
- **Thick copper**: higher current and thermal capacity
- **Thermal pads**: large copper areas under hot components

### Thermal modeling
- **Simulation**: FEA thermal analysis
- **Hot spot identification**: locate temperature peaks
- **Design iteration**: modify based on results
- **Measurement**: validation with thermal camera

## 🔗 Powiązane tematy
- [[pcb_podstawy|Podstawy PCB]] - podstawowe pojęcia PCB
- [[pcb_schemat_elektryczny|Schemat Elektryczny]] - punkt startowy layoutu
- [[pcb_warstwy_pcb|Warstwy PCB]] - struktura wielowarstwowa
- [[pcb_routing_sciezki|Routing Ścieżek]] - szczegółowe techniki routingu
- [[pcb_plane_zasilania|Płaszczyzny Zasilania]] - power distribution
- [[pcb_plane_masy|Płaszczyzny Masy]] - ground distribution
- [[pcb_thermal_management|Zarządzanie Cieplne]] - termiczne aspekty
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - sprawdzone metody

---

**🎯 Co dalej?**
Po opanowaniu podstaw layoutu, przejdź do [[pcb_warstwy_pcb|Warstw PCB]] aby zrozumieć strukturę wielowarstwową, lub [[pcb_routing_sciezki|Routing Ścieżek]] dla szczegółowych technik prowadzenia połączeń.