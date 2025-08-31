# Kondensatory

## ⚡ Definicja

**Kondensator** to element elektroniczny zdolny do gromadzenia energii elektrycznej w postaci pola elektrycznego między dwiema okładkami oddzielonymi dielektrykiem.

## 📊 Podstawowe parametry

### Pojemność (C)
- **Jednostka**: Farad [F], μF, nF, pF
- **Wzór**: C = Q/U (ładunek/napięcie)
- **Typowe wartości**: 1pF - 100000μF

### Napięcie robocze (Umax)
- **Oznaczenia**: 6.3V, 16V, 25V, 50V, 100V, 450V...
- **Bezpieczeństwo**: Urobocze < 0.8 × Umax
- **Przekroczenie**: Przebicie dielektryka → zniszczenie

### Tolerancja
- **Ceramiczne**: ±5%, ±10%, ±20%
- **Foliowe**: ±1%, ±2%, ±5%
- **Elektrolityczne**: +20% / -10%

## 🔋 Zasada działania

### Ładowanie kondensatora
```
     +Q ┃ -Q
    ────┃────
    +   ┃   -
       U
```
- **Prąd ładowania**: I = C × (dU/dt)
- **Energia**: W = ½CU²

### Wykładnicza charakterystyka ładowania
```
U(t) = Uzasilania × (1 - e^(-t/RC))
```
- **Stała czasowa**: τ = RC
- **99% naładowania**: t ≈ 5τ

## 🏗️ Rodzaje kondensatorów

### Kondensatory ceramiczne

#### Charakterystyka
- **Pojemność**: 1pF - 10μF
- **Napięcie**: 6.3V - 3kV
- **Tolerancja**: ±5% do ±80%
- **Temperatura**: Stabilne lub zmienne z temperaturą

#### Zastosowania
- **Filtrowanie wysokich częstotliwości**
- **Sprzęganie AC**
- **Rezonatory** (w oscylatorach)

#### Klasy ceramiki
- **Klasa 1 (NP0/C0G)**: Bardzo stabilne, ±30ppm/°C
- **Klasa 2 (X7R, Y5V)**: Większe pojemności, mniej stabilne

### Kondensatory foliowe

#### Charakterystyka
- **Pojemność**: 1nF - 100μF
- **Napięcie**: 63V - 2kV
- **Tolerancja**: ±1% - ±10%
- **Temperatura**: Bardzo stabilne

#### Rodzaje folii
- **Polipropylenowe (PP)**: Audio, filtry
- **Poliestrowe (PET)**: Ogólne zastosowania
- **Polystyrenkowe (PS)**: Precyzyjne pomiary

### Kondensatory elektrolityczne

#### Charakterystyka
- **Pojemność**: 1μF - 100000μF
- **Napięcie**: 6.3V - 450V
- **Polaryzacja**: TAK! (+ i -)
- **Tolerancja**: +20%/-10%

#### Zastosowania
- **Filtrowanie zasilania**
- **Kondensatory buforowe**
- **Sprzęganie mocy**

⚠️ **UWAGA**: Połączenie z odwrotną polaryzacją → WYBUCH!

### Kondensatory tantalowe
- **Pojemność**: 0.1μF - 1000μF
- **Napięcie**: 2V - 50V
- **Cechy**: Małe rozmiary, niska ESR, drogie
- **Zastosowania**: Elektronika cyfrowa, filtry

## 🔌 Połączenia kondensatorów

### Połączenie równoległe
```
C₁ ──┐
     ├── Ccałk = C₁ + C₂ + C₃
C₂ ──┘
```
- **Pojemność się dodaje**
- **Napięcie**: Takie samo na wszystkich

### Połączenie szeregowe
```
C₁ ── C₂ ── C₃
```
**Wzór**: 1/Ccałk = 1/C₁ + 1/C₂ + 1/C₃

**Dla dwóch kondensatorów**:
```
Ccałk = (C₁ × C₂)/(C₁ + C₂)
```

## ⚡ Zastosowania praktyczne

### Filtrowanie zasilania

#### Filtr dolnoprzepustowy
```
Uin ── R ──┬── Uout
           │
           C
           │
          GND
```
**Częstotliwość odcięcia**: f = 1/(2πRC)

#### Filtr w zasilaczach
- **C1 (duży)**: 1000μF - głowny filtr
- **C2 (mały)**: 100nF - filtr HF
- **Montaż równolegle**: Lepsze filtrowanie

### Sprzęganie AC
```
Sygnał ──┤├── R ──┬── Wzmacniacz
         C        │
                 GND
```
- **Przepuszcza AC, blokuje DC**
- **Częstotliwość dolna**: f = 1/(2πRC)

### Kondensator rozruchowy (silniki)
- **Funkcja**: Start silników jednofazowych
- **Pojemność**: Obliczana z mocy silnika
- **Napięcie**: 1.5 × Usieć

### Timer 555
```
     R
Vcc ─┴─┬─ Trigger
       │
       C
       │
      GND
```
**Okres**: T = 1.1 × RC

## 🧮 Obliczenia praktyczne

### Przykład 1: Filtr RC
**Dane**: R = 1kΩ, potrzeba f = 1.6kHz
```
C = 1/(2π × f × R) = 1/(2π × 1600 × 1000) = 100nF
```

### Przykład 2: Energia w kondensatorze
**Dane**: C = 1000μF, U = 25V
```
W = ½CU² = ½ × 0.001 × 625 = 0.31J
```

### Przykład 3: Połączenie szeregowe
**Dane**: C₁ = 10μF, C₂ = 20μF
```
Ccałk = (10 × 20)/(10 + 20) = 200/30 = 6.67μF
```

## ⚠️ Bezpieczeństwo

### Ładunki resztkowe
- **Kondensatory dużej pojemności** mogą być niebezpieczne
- **Rozładowanie**: Rezystorem 1kΩ przez izolowaną rączkę
- **Nie dotykać** wyprowadzeń kondensatorów HV

### Przepięcia
- **Sprawdzaj napięcie robocze**
- **Derating**: 20-30% zapasu
- **Przyczyną uszkodzeń**: 80% przypadków w elektronice

### Temperatura
- **Kondensatory elektrolityczne**: Wysychają w wysokich temperaturach
- **Ceramiczne**: Mogą pękać przy szokach termicznych

## 🔍 Testowanie kondensatorów

### Multimetrem
1. **Rozładuj** kondensator
2. **Ustaw** pomiar pojemności
3. **Podłącz** sondy (polarność dla elektrolitycznych)
4. **Odczytaj** wartość

### Oscyloskopem
- **Test ładowania**: Sprawdzenie stałej czasowej RC
- **Test ESR**: Pomiar oporu zastępczego
- **Test przecieków**: Pomiar prądu upływu

## 🧰 Markowanie kondensatorów

### Kondensatory małe (ceramiczne)
**Przykład**: 104
- 10 × 10⁴ pF = 100000pF = 100nF

### Kondensatory elektrolityczne
**Bezpośrednie oznaczenie**: 1000μF / 25V

### Kod literowy
- **p** = pF (pikofarad)
- **n** = nF (nanofarad) 
- **u lub μ** = μF (mikrofarad)

## 📚 Powiązane tematy

- [[cewki_induktory|Cewki (Induktory)]]
- [[filtry_rc_lc|Filtry RC i LC]]
- [[zasilacze|Zasilacze - Filtrowanie]]
- [[oscylator_555|Timer 555]]
- [[silniki_elektryczne|Silniki - Kondensatory Rozruchowe]]
- [[multimetr|Multimetr - Pomiar Pojemności]]

---

#elektronika #kondensatory #pojemność #filtrowanie #energia #bezpieczeństwo