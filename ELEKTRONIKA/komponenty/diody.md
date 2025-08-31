# Diody

## 💎 Definicja

**Dioda** to element półprzewodnikowy o dwóch wyprowadzeniach (anoda i katoda), który przewodzi prąd tylko w jednym kierunku.

## 🔬 Budowa i zasada działania

### Złącze p-n
```
     p      n
  ┌─────┬─────┐
  │ ⊕ ⊕ │ ⊖ ⊖ │
  │ ⊕ ⊕ │ ⊖ ⊖ │ ← Strefa zubożona
  └─────┴─────┘
  Anoda  Katoda
    A      K
```

### Kierunki przewodzenia
- **Przewodzenie (kierunek prosty)**: Anoda (+) → Katoda (-)
- **Zaporowy (kierunek wsteczny)**: Katoda (+) → Anoda (-)

### Symbol diody
```
     A    K
      │    │
   ──►│  ──┤
      │    │
```
**Mnemonika**: Strzałka wskazuje kierunek przepływu prądu

## 📊 Charakterystyka prądowo-napięciowa

### Kierunek prosty
- **Napięcie przewodzenia**: ~0.7V (krzem), ~0.3V (german)
- **Opór dynamiczny**: Bardzo mały (~0.1Ω)
- **Prąd**: Rośnie wykładniczo z napięciem

### Kierunek wsteczny
- **Prąd upływu**: Bardzo mały (nA - μA)
- **Napięcie przebicia**: Zależy od typu diody
- **Przebicie**: Zniszczenie lub działanie nominalnie (Zenera)

## 🏗️ Rodzaje diod

### Diody prostownicze

#### Charakterystyka
- **Prąd nominalny**: 1A - 100A i więcej
- **Napięcie wsteczne**: 50V - 1000V i więcej
- **Spadek napięcia**: 0.7V - 1.2V
- **Częstotliwość**: Do ~1kHz (wolne)

#### Popularne typy
- **1N4001-1N4007**: 1A, 50V-1000V
- **1N5400-1N5408**: 3A, 50V-1000V  
- **BY-series**: Diody mocy

#### Zastosowania
- **Prostowniki** sieciowe 50Hz
- **Zabezpieczenia** przed odwrotną polaryzacją
- **Diody koła swobodnego** (flyback)

### Diody szybkie (fast recovery)

#### Charakterystyka
- **Czas przełączania**: < 100ns
- **Zastosowania**: Zasilacze impulsowe, invertory
- **Oznaczenia**: FR-prefix (np. FR107)

### Diody Schottky

#### Charakterystyka
- **Spadek napięcia**: 0.2V - 0.4V (niższy niż krzem)
- **Szybkość**: Bardzo szybkie przełączanie
- **Prąd wsteczny**: Wyższy niż diody krzemowe
- **Zastosowania**: Zasilacze, systemy logiczne

#### Popularne typy
- **1N5817-1N5819**: 1A, 20V-40V
- **SB-series**: Różne prądy i napięcia

### Diody Zenera (stabilizacyjne)

#### Charakterystyka
- **Napięcie stabilizacji**: 2.7V - 200V
- **Tolerancja**: ±5%, ±2%, ±1%
- **Moc**: 0.5W, 1W, 5W, 20W...
- **Działanie**: W kierunku wstecznym przy napięciu Zenera

#### Zastosowania
- **Stabilizatory napięcia**
- **Zabezpieczenia przeciwprzepięciowe**
- **Źródła napięcia odniesienia**

#### Przykład obliczenia
**Stabilizator 12V z Zenera:**
```
      R
Uin ──┴── Uzener (12V)
       │
      ┌─┤  Dioda Zenera
      │ └─┐
     RL   │
      │   │
     GND GND
```

### Diody świecące (LED)

#### Charakterystyka
- **Napięcie przewodzenia**: 1.8V-4V (zależnie od koloru)
- **Prąd nominalny**: 20mA (standardowe)
- **Moc**: 0.1W - 100W (high-power LED)
- **Kolory**: Czerwony, zielony, niebieski, biały...

#### Napięcia LED według kolorów
- **Czerwony**: 1.8V - 2.2V
- **Żółty**: 2.0V - 2.4V  
- **Zielony**: 2.0V - 3.5V
- **Niebieski**: 3.0V - 3.8V
- **Biały**: 3.0V - 4.0V

#### Obliczanie rezystora szeregowego
```
RLED = (Uzasilania - ULED) / ILED
```

**Przykład**: LED biały (3.2V, 20mA), zasilanie 5V
```
R = (5V - 3.2V) / 0.02A = 90Ω (wybieramy 100Ω)
```

### Fotodiody
- **Działanie**: Generują prąd pod wpływem światła
- **Zastosowania**: Czujniki światła, komunikacja optyczna
- **Charakterystyka**: Prąd proporcjonalny do natężenia światła

## 🔄 Układy z diodami

### Prostownik jednopołówkowy
```
         D
AC ──┬───├──┬── DC+
     │      │
    ═══    ═══ C
            │
           DC- ──┘
```
- **Sprawność**: ~40%
- **Tętnienie**: Duże
- **Zastosowania**: Proste, tanie układy małej mocy

### Prostownik dwupołówkowy (mostek Graetza)
```
      D1    D2
  ──┬──├──┬──├──┬── DC+
    │     │     │
AC ─┤    ═══    │
    │     │     │
  ──┴──├──┴──├──┴── DC-
      D4    D3
```
- **Sprawność**: ~90%
- **Tętnienie**: Mniejsze
- **Zastosowania**: Większość zasilaczy

### Zabezpieczenie przeciw odwrotnej polaryzacji
```
+Bat ──├──┬── +Circuit
       D  │
          │
-Bat ─────┴── -Circuit
```

### Koło swobodne (flyback diode)
```
+VCC ──┐
       │
      ╔═╗ Cewka (przekaźnik, silnik)
      ╚═╝
       │  ↗D (flyback)
      GND
```
**Funkcja**: Ochrana przed przepięciami od cewek

## ⚠️ Najczęstsze problemy

### Przepalona dioda
**Objawy**:
- Zwarcie (sprawdzić omomierzem)
- Przegrzanie układu
- Zapach spalenizny

**Przyczyny**:
- Przekroczenie prądu nominalnego
- Przekroczenie temperatury
- Przepięcia wsteczne

### Zła orientacja
**Objawy**:
- Brak przewodzenia
- LED nie świeci
- Prostownik nie działa

**Rozwiązanie**: Sprawdzić kierunek (anoda do +, katoda do -)

### Spadki napięcia
- **Problem**: Za duży spadek napięcia na diodzie
- **Rozwiązanie**: Użyć diody Schottky (niższy spadek)

## 🧮 Obliczenia praktyczne

### Przykład 1: Rezystor dla LED
**Dane**: LED czerwony 2V/20mA, zasilanie 12V
```
R = (12V - 2V) / 0.02A = 500Ω
Moc = I²R = 0.02² × 500 = 0.2W
```

### Przykład 2: Prostownik z filtrem
**Dane**: Transformator 15V RMS, diody 0.7V
```
Napięcie szczytowe = 15V × √2 = 21.2V
Po diodach = 21.2V - 1.4V = 19.8V (mostek)
Po filtrze ≈ 19V DC
```

### Przykład 3: Stabilizator Zenera
**Dane**: Zener 9V/1W, Uin = 15V, IL = 50mA
```
Iz(min) = 10% × Iz(max) = 10mA
Iz(max) = P/Uz = 1W/9V = 111mA
IR = IL + Iz = 50mA + 20mA = 70mA (wybieramy Iz=20mA)
R = (Uin - Uz)/IR = (15V - 9V)/0.07A = 86Ω (wybieramy 82Ω)
```

## 🔧 Testowanie diod

### Multimetrem
1. **Ustaw** funkcję testu diod lub opór
2. **Kierunek prosty**: Czerwona sonda na anodę, czarna na katodę
3. **Wskazanie**: ~0.7V lub niski opór
4. **Kierunek wsteczny**: Zamień sondy
5. **Wskazanie**: OL (otwarty obwód) lub wysoki opór

### Wizualnie
- **Pasek**: Katoda często oznaczona paskiem
- **Rozmiar wyprowadzeń**: Katoda czasem krótsza (LED)
- **Kształt**: Płaskie miejsce przy katodzie (LED)

## 📚 Powiązane tematy

- [[prostowniki|Prostowniki i Zasilacze]]
- [[tranzystory|Tranzystory]]
- [[led_oświetlenie|Oświetlenie LED]]
- [[zabezpieczenia_elektryczne|Zabezpieczenia Elektroniczne]]
- [[multimetr|Multimetr - Test Diod]]
- [[lutowanie|Lutowanie Diod]]

---

#elektronika #diody #półprzewodniki #LED #prostowniki #Zener