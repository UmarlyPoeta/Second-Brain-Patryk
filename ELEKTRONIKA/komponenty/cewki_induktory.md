# Cewki (Induktory)

## 🌀 Definicja

**Cewka** (induktor) to element elektroniczny składający się z przewodu nawiniętego w spiralę, który magazynuje energię w postaci pola magnetycznego.

## ⚡ Podstawowe właściwości

### Indukcyjność (L)
- **Jednostka**: Henry [H], milihenry [mH], mikrohenry [μH]
- **Definicja**: Zdolność do magazynowania energii magnetycznej
- **Wzór podstawowy**: L = Φ/I (strumień/prąd)

### Podstawowe równanie cewki
```
u(t) = L × di/dt
```
- **Napięcie na cewce** proporcjonalne do szybkości zmian prądu
- **Stały prąd** → napięcie = 0V (cewka = zwarcie)
- **Szybkie zmiany prądu** → duże napięcie

### Energia magazynowana
```
W = ½ × L × I²
```

## 🏗️ Budowa i konstrukcja

### Parametry fizyczne wpływające na indukcyjność

#### Wzór ogólny
```
L = μ × N² × A / l
```
Gdzie:
- **μ** - przepuszczalność magnetyczna rdzenia
- **N** - liczba zwojów
- **A** - pole przekroju rdzenia [m²]
- **l** - długość rdzenia [m]

#### Wnioski praktyczne
- **Więcej zwojów** → większa indukcyjność (N²!)
- **Rdzeń ferromagnetyczny** → znacznie większa L
- **Większy przekrój** → większa L
- **Krótszy rdzeń** → większa L

### Rodzaje rdzeni

#### Rdzeń powietrzny
- **Materiał**: Tylko powietrze (μ ≈ μ₀)
- **Indukcyjność**: Mała (μH-mH)
- **Zalety**: Brak nasycenia, liniowa charakterystyka
- **Zastosowania**: VHF/UHF, filtry

#### Rdzeń ferytowy
- **Materiał**: Tlenki żelaza (ferryty)
- **Indukcyjność**: Duża (mH-H)
- **Częstotliwość**: Do ~100MHz
- **Zastosowania**: Transformatory impulsowe, filtry EMC

#### Rdzeń żelazny
- **Materiał**: Żelazo, stal transformatorowa
- **Indukcyjność**: Bardzo duża
- **Częstotliwość**: Do ~1kHz (straty wirowe)
- **Zastosowania**: Transformatory sieciowe, dławiki

## 🔄 Zachowanie w obwodach

### Prąd stały (DC)
```
Po ustaleniu: XL = 0Ω (zwarcie)
Włączenie: i(t) = (U/R) × (1 - e^(-t/τ))
τ = L/R (stała czasowa)
```

### Prąd przemienny (AC)
```
Reaktancja indukcyjna: XL = 2πfL
Impedancja: ZL = jXL = j2πfL
```

**Właściwości AC**:
- **Prąd opóźniony** o 90° względem napięcia
- **Wyższe f** → większy XL (blokuje AC)
- **Niższe f** → mniejszy XL (przepuszcza)

## 🔌 Połączenia induktorów

### Połączenie szeregowe
```
L1 ── L2 ── L3

Ltotal = L1 + L2 + L3 + ... + Ln
```
**Warunek**: Brak sprzężeń magnetycznych

### Połączenie równoległe
```
L1 ──┐
     ├── Ltotal
L2 ──┘

1/Ltotal = 1/L1 + 1/L2 + 1/L3 + ... + 1/Ln
```

### Sprzężenie magnetyczne
```
L12 = L1 + L2 ± 2M
```
Gdzie **M** = współczynnik sprzężenia wzajemnego
- **+** gdy pola się wzmacniają
- **-** gdy pola się osłabiają

## 💡 Rodzaje cewek

### Cewki małej indukcyjności (μH-mH)

#### Cewki toroidalne
- **Indukcyjność**: 1μH - 100mH
- **Zalety**: Brak promieniowania pola, kompaktowe
- **Zastosowania**: Filtry EMC, dławiki w zasilaczach

#### Cewki na rdzeniu E/I
- **Indukcyjność**: 100μH - 10mH  
- **Zastosowania**: Transformatory impulsowe
- **Szczelina powietrzna**: Kontroluje nasycenie

#### Cewki wielowarstwowe (SMD)
- **Indukcyjność**: 1nH - 100μH
- **Rozmiary**: 0603, 0805, 1206
- **Zastosowania**: Elektronika wysokich częstotliwości

### Cewki dużej indukcyjności (mH-H)

#### Dławiki sieciowe
- **Indukcyjność**: 1H - 100H
- **Zastosowania**: Ograniczanie prądów włączenia
- **Konstrukcja**: Rdzeń żelazny, szczelina

#### Cewki głośnikowe
- **Indukcyjność**: 0.1mH - 10mH
- **Opór**: Mały (~0.1Ω)
- **Zastosowania**: Crossovery audio

## ⚡ Zastosowania praktyczne

### Filtry dolnoprzepustowe (z rezystorem)
```
Uin ── R ──┬── Uout
           │
           L
           │
          GND
```
**Częstotliwość odcięcia**: f = R/(2πL)

### Filtry górnoprzepustowe (z rezystorem)  
```
Uin ── L ──┬── Uout
           │
           R
           │
          GND
```
**Częstotliwość odcięcia**: f = R/(2πL)

### Obwody rezonansowe LC
```
     L
Uin ──┴───┬── Uout
      C   │
      ┴   │
         GND
```
**Częstotliwość rezonansowa**: f₀ = 1/(2π√LC)

### Dławiki w zasilaczach
```
DC in ── L ──┬── DC out
             │
             C (filtrujący)
             │
            GND
```
**Funkcja**: Wygładzanie tętnień prądu

### Transformatory
```
Pierwotna L1 ═══╫══╫══ L2 Wtórna
                M
```
**Przekładnia napięć**: U₂/U₁ = N₂/N₁
**Przekładnia prądów**: I₂/I₁ = N₁/N₂

## 🔧 Pomiar indukcyjności

### Multimetrem z funkcją L
1. **Rozładuj** cewkę (zwarcie przez rezystor)
2. **Ustaw** funkcję pomiaru indukcyjności
3. **Podłącz** sondy do wyprowadzeń cewki
4. **Odczytaj** wartość

### Metodą rezonansową
1. **Połącz** z kondensatorem znanej pojemności
2. **Znajdź** częstotliwość rezonansową f₀
3. **Oblicz**: L = 1/(4π²f₀²C)

### Oscyloskopem (metoda czasowa)
1. **Podaj** impuls napięciowy przez rezystor
2. **Zmierz** stałą czasową τ = L/R
3. **Oblicz**: L = τ × R

## ⚠️ Zjawiska niepożądane

### Napięcie samoindukcji
```
u = -L × di/dt
```
**Przy wyłączeniu**: Bardzo wysokie napięcie!

**Zabezpieczenie - dioda koła swobodnego**:
```
+12V ──┐
       │
      ╔═╗ Cewka
      ╚═╝ (przekaźnik)
       │ ↗ Dioda
      GND
```

### Straty w rdzeniu
- **Histereza**: Energia tracona przy przemagnesowaniu
- **Prądy wirowe**: Straty w masywnym rdzeniu
- **Rozwiązania**: Rdzenie z blach, ferryty

### Pojemność pasożytnicza
- **Między zwojami**: Tworzy pojemność
- **Przy wysokich f**: Cewka staje się kondensatorem
- **Częstotliwość własna**: f = 1/(2π√LC_paraz)

## 🧮 Obliczenia praktyczne

### Przykład 1: Stała czasowa RL
**Dane**: L = 100mH, R = 10Ω
```
τ = L/R = 0.1H / 10Ω = 0.01s = 10ms
Po czasie 5τ = 50ms prąd osiągnie 99% wartości końcowej
```

### Przykład 2: Filtr LC
**Dane**: L = 10mH, C = 100nF
```
f₀ = 1/(2π√LC) = 1/(2π√(0.01 × 100×10⁻⁹)) = 5.03kHz
```

### Przykład 3: Reaktancja przy 50Hz
**Dane**: L = 1H
```
XL = 2πfL = 2π × 50 × 1 = 314Ω
```

## ⚠️ Bezpieczeństwo

### Wysokie napięcia samoindukcji
- **Wyłączanie** obwodów indukcyjnych → iskrzenie
- **Zawsze używaj** diod koła swobodnego
- **Ostrożność** przy dławikach świetlówek

### Pola magnetyczne
- **Silne cewki**: Mogą uszkodzić karty magnetyczne, pacemaker
- **Minimalna odległość**: 30cm od urządzeń elektronicznych

## 📚 Powiązane tematy

- [[kondensatory|Kondensatory]]
- [[transformatory|Transformatory]]
- [[filtry_rc_lc|Filtry RC i LC]]
- [[zasilacze_impulsowe|Zasilacze Impulsowe]]
- [[silniki_elektryczne|Silniki - Cewki Rozruchowe]]
- [[multimetr|Multimetr - Pomiar Indukcyjności]]

---

#elektronika #cewki #induktory #indukcyjność #filtry #transformatory #pola-magnetyczne