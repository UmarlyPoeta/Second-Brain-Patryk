# Płytki Drukowane (PCB)

## 🏗️ Definicja

**Płytka drukowana** (PCB - Printed Circuit Board) to płytka z materiału izolacyjnego z nadrukowanymi ścieżkami przewodzącymi, służąca do mechanicznego mocowania i elektrycznego łączenia elementów elektronicznych.

## 📋 Budowa PCB

### Materiały podstawowe

#### Substrat (rdzeń)
- **FR-4**: Fiberglass + żywica epoksydowa (standard)
- **FR-2**: Papier fenolowy (tanie, jednostronne)
- **Aluminium**: Odprowadzanie ciepła (LED)
- **Ceramika**: Wysokie częstotliwości, precyzja

#### Warstwy PCB
```
┌─ Warstwa miedzi (35μm - 105μm)
├─ Maska lutownicza (zielona)
├─ Napis (biały)
├─ Substrat FR-4
├─ Miedź wewnętrzna (wielowarstwowe)
├─ Substrat FR-4
├─ Napis (biały)
├─ Maska lutownicza (zielona)
└─ Warstwa miedzi (35μm - 105μm)
```

### Grubości standardowe
- **0.8mm**: Płytki cienkie (telefony, tablety)
- **1.0mm**: Standardowe aplikacje
- **1.6mm**: Najczęściej używana
- **2.4mm**: Grube aplikacje mocowe

## 🎨 Projektowanie PCB

### Zasady rozmieszczenia elementów

#### Podział na sekcje
- **Zasilanie**: Transformator, prostowniki, filtry
- **Analogowa**: Op-amp, filtry, czujniki
- **Cyfrowa**: Mikrokontrolery, pamięci, bramki
- **Wejścia/Wyjścia**: Złącza, LED, przyciski

#### Minimalizacja zakłóceń
```
[Analog] ←─ 10mm ─→ [Digital]
    │                   │
   GND plane         GND plane
    │                   │  
   ╰─────── GND ───────╯ (jeden punkt)
```

### Prowadzenie ścieżek

#### Szerokości ścieżek
| Prąd [A] | Szerokość [mm] | Grubość Cu [oz] | Temp. wzrost [°C] |
|----------|----------------|------------------|-------------------|
| **0.1** | 0.1 | 1 | 10 |
| **0.5** | 0.3 | 1 | 10 |
| **1.0** | 0.6 | 1 | 10 |
| **2.0** | 1.2 | 1 | 10 |
| **5.0** | 3.0 | 2 | 10 |

#### Kąty ścieżek
```
❌ Złe (90°):     ✅ Dobre (45°):
   ─────┐            ─────╲
        │                  ╲
        └─────              ╲─────

Powód: Nagromadzenie kwasu przy trawieniu
```

#### Minimalne odstępy
- **Ścieżka-ścieżka**: 0.1mm (cheap PCB), 0.05mm (precision)
- **Via-ścieżka**: 0.1mm
- **Ścieżka-pad**: 0.05mm

### Warstwy miedziowe

#### Płytki jednostronne
- **1 warstwa**: Tylko dolna (bottom)
- **Zastosowanie**: Proste układy, prototypy
- **Ograniczenia**: Mostkowanie przewodami

#### Płytki dwustronne  
- **2 warstwy**: Górna (top) + dolna (bottom)
- **Przełączenia**: Przez otwory (via)
- **90% zastosowań**: Wystarczające dla większości

#### Płytki wielowarstwowe
- **4-6-8+ warstw**: Wewnętrzne warstwy zasilania
- **Zalety**: Lepsze EMC, kompaktowość
- **Wady**: Droższe, trudniejsze naprawy

### Płaszczyzny zasilania

#### Ground plane (masa)
```
████████████████████  ← Jednolita warstwa GND
    │   │   │   │
   IC1 IC2 IC3 IC4    ← Elementy
```
**Zalety**:
- Niska impedancja powrotu prądu
- Ekranowanie elektromagnetyczne
- Odprowadzanie ciepła

#### Power plane (zasilanie)
- **VCC/VDD**: Dedykowana warstwa zasilania
- **Kondensatory odsprzęgające**: 100nF co 2-3cm
- **Minimalizacja**: Impedancji zasilania

## 🔧 Elementy PCB

### Otwory i pady

#### THT (Through-Hole Technology)
- **Średnica otworu**: 0.6-1.0mm (standardowe)
- **Średnica pada**: 1.5-2.0mm
- **Zastosowanie**: Elementy mocowe, złącza

#### SMD (Surface Mount Device)
- **Rozmiary**: 1206, 0805, 0603, 0402, 0201
- **Pady**: Prostokątne, dokładnie wymierzone
- **Zalety**: Kompaktowość, automatyczny montaż

### Via (przejścia)
- **Through via**: Przez całą płytkę
- **Blind via**: Z powierzchni do warstwy wewnętrznej
- **Buried via**: Między warstwami wewnętrznymi
- **Średnice**: 0.2-0.8mm (typowo 0.3mm)

### Złącza i wyprowadzenia

#### Wyprowadzenia krawędziowe
```
PCB edge: ═══╪═══╪═══╪═══
            1   2   3   4
```
- **Zastosowanie**: Karty rozszerzeń, moduły
- **Pozłacanie**: HASL, ENIG (trwałość)

#### Złącza pinowe
- **Pin headers**: 2.54mm (0.1″) - standard Arduino
- **Micro-pitch**: 1.27mm, 1.0mm (kompaktowe)
- **Specjalne**: USB, HDMI, RF (SMA, U.FL)

## 🏭 Produkcja PCB

### Proces produkcji

#### 1. Przygotowanie substratu
- **Oczyszczenie** płytek FR-4
- **Laminowanie** folii miedzianej
- **Kontrola** grubości i jakości

#### 2. Fotolitografia
```
Resist → UV exposure → Development → Etching
```
- **Fotoreist**: Światłoczuły polymer
- **Maska**: Film z wzorem ścieżek
- **Naświetlanie**: UV 365nm
- **Wywoływanie**: Chemiczne usunięcie

#### 3. Trawienie
- **Chlorek żelaza** (FeCl₃): Domowe laboratorium
- **Persiarczań amonu**: Regenerowalne
- **Kwas**: Profesjonalne (HCl + H₂O₂)

#### 4. Wiercenie
- **CNC**: Kontrolowane numerycznie
- **Średnice**: 0.1-6.0mm
- **Dokładność**: ±0.025mm
- **Wiertła**: Karbid wolframu

#### 5. Powlekanie
- **HASL**: Hot Air Solder Leveling (cyna)
- **OSP**: Organic Solderability Preservative
- **ENIG**: Electroless Nickel Immersion Gold
- **Silver**: Srebro (tanie, dobre lutowanie)

#### 6. Maska lutownicza
- **Kolor**: Zielony (standard), niebieski, czerwony, czarny
- **Funkcja**: Ochrona przed mostkami lutu
- **Okienka**: Nad padami do lutowania

#### 7. Nadruk (silkscreen)
- **Kolor**: Biały (standard), żółty
- **Zawartość**: Oznaczenia elementów, numery pinów
- **Czcionki**: Minimum 0.15mm wysokość

### Kontrola jakości

#### Testy elektryczne
- **In-Circuit Test (ICT)**: Sprawdzenie wszystkich połączeń
- **Flying Probe**: Przesuwne sondy testowe
- **Boundary Scan**: Test cyfrowy przez JTAG

#### Inspekcja wizualna
- **AOI** (Automated Optical Inspection): Kamery + AI
- **Lupa**: Kontrola ręczna (prototypy)
- **Kryteria**: IPC-A-610 standard

## 💻 Software do projektowania

### Programy CAD

#### KiCad (darmowy)
```
Schematic → Symbol libraries
    ↓
PCB Layout → Footprint libraries
    ↓
Gerber files → Production
```
**Zalety**: Open source, kompletny workflow
**Wady**: Stroma krzywa uczenia

#### Eagle (Fusion 360)
- **Osobisty**: Darmowy (ograniczenia rozmiaru)
- **Profesjonalny**: Płatny (Autodesk)
- **Zalety**: Duże biblioteki, Arduino support

#### Altium Designer
- **Profesjonalny**: Najbardziej zaawansowany
- **Koszt**: Bardzo drogi ($$$)
- **Zastosowanie**: Przemysł, zaawansowane PCB

#### Fritzing
- **Edukacyjny**: Graficzny interfejs breadboard
- **Prostota**: Idealne dla początkujących
- **Ograniczenia**: Tylko proste projekty

### Biblioteki elementów

#### Footprint (obudowa fizyczna)
- **Wymiary**: Dokładne rozmiary padów
- **Courtyards**: Obszary konfliktu
- **3D models**: Wizualizacja gotowej płytki

#### Symbol (schemat)
- **Wyprowadzenia**: Numeracja i nazwy pinów
- **Logika**: Bramki, zasilanie, sygnały
- **Standardy**: IEEE, ANSI conventions

## 🏠 Prototypowanie w domu

### Metody domowe

#### Metoda thermotransfer
1. **Wydruk** na papierze transferowym
2. **Transfer** żelazkiem (180°C)
3. **Trawienie** chlorkiem żelaza
4. **Czyszczenie** z restek papieru

#### Metoda UV
1. **Laminowanie** fotorezistu
2. **Naświetlanie** przez przezroczystą maskę
3. **Wywoływanie** w roztworze NaOH
4. **Trawienie** i czyszczenie

### Narzędzia domowe
- **Żelazko**: Transfer i laminowanie
- **UV box**: Naświetlanie (365nm LED)
- **Kuwety**: Trawienie i wywoływanie
- **Wiertarka** + mini wiertła
- **Zgrzewarka** do laminowania

### Ograniczenia domowe
- **Rozdzielczość**: 0.3mm minimum
- **Via**: Trzeba lutować ręcznie drutami
- **Maska lutownicza**: Trudna w domu
- **Wielowarstwowe**: Praktycznie niemożliwe

## ⚠️ Bezpieczeństwo

### Chemikalia
- **Chlorek żelaza**: Żrący, plami nieodwracalnie
- **Kwasy**: Rękawice, okulary, wentylacja
- **Rozpuszczalniki**: Aceton, izopropanol - łatwopalne

### Wiercenie
- **Wiertła**: Bardzo kruche, łamią się
- **Pył**: Włókno szklane - maska przeciwpyłowa
- **Obroty**: Wysokie (20000+ RPM)

### UV
- **Naświetlanie**: Okulary UV, nie patrzeć bezpośrednio
- **Skóra**: Może powodować oparzenia

## 🧮 Obliczenia praktyczne

### Szerokość ścieżki dla prądu
```
Wzór IPC-2221:
A = (I / (k × ΔT^b))^(1/c)

gdzie:
I - prąd [A]
ΔT - wzrost temperatury [°C]
k, b, c - stałe zależne od grubości miedzi
```

**Uproszczony**: 1A ≈ 1mm szerokości (1oz Cu, 10°C wzrost)

### Impedancja charakterystyczna
```
Z₀ = 87/√(εᵣ+1.41) × ln(5.98×h/(0.8×w+t))

gdzie:
h - wysokość dielektryka [mm]
w - szerokość ścieżki [mm]  
t - grubość miedzi [mm]
εᵣ - stała dielektryczna FR-4 ≈ 4.3
```

**Typowe**: 50Ω, 75Ω, 100Ω (different)

### Koszt prototypu
- **PCB (5×5cm, 2-layer)**: $2-10 (China)
- **Elementy**: $10-50 (zależnie od złożoności)
- **Czas**: 1-3 tygodnie (shipping z China)
- **Lokalne**: 5-10x droższe, ale szybsze

## 📚 Powiązane tematy

- [[lutowanie|Lutowanie - Montaż na PCB]]
- [[elektronika_cyfrowa|Elektronika Cyfrowa - Układy]]
- [[elektronika_analogowa|Elektronika Analogowa - PCB]]
- [[emc_interference|EMC i Zakłócenia]]
- [[arduino_podstawy|Arduino - Projektowanie Shield]]
- [[komponenty_smd|Komponenty SMD]]

---

#PCB #projektowanie #trawienie #produkcja #CAD #prototypowanie #lutowanie