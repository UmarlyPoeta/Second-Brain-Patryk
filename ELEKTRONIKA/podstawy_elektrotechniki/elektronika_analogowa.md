# Elektronika Analogowa - Podstawy

## 🌊 Definicja

**Elektronika analogowa** to dziedzina elektroniki zajmująca się przetwarzaniem sygnałów, które mogą przyjmować ciągły zakres wartości w czasie i amplitudzie.

## 📊 Charakterystyka sygnałów analogowych

### Parametry podstawowe

#### Amplituda
```
     Vmax ┌─────┐
          │     │
     Vpp  │     │  ← Napięcie międzyszczytowe (peak-to-peak)
          │     │
     Vmin └─────┘

Veff = Vmax / √2 (dla sinusoidy)
```

#### Częstotliwość i okres
```
f = 1/T
ω = 2πf (pulsacja)

Sygnał: v(t) = Vmax × sin(ωt + φ)
```

#### Zniekształcenia
- **THD** (Total Harmonic Distortion): % harmonicznych
- **SNR** (Signal-to-Noise Ratio): Stosunek sygnał/szum
- **SINAD** (Signal-to-Noise-and-Distortion): Jakość ogólna

## 🔧 Wzmacniacze operacyjne (Op-Amp)

### Charakterystyki idealne
- **Wzmocnienie różnicowe**: Ad → ∞
- **Impedancja wejściowa**: Rin → ∞
- **Impedancja wyjściowa**: Rout → 0
- **Pasmo przenoszenia**: DC do ∞
- **Prądy wejściowe**: 0A

### Symbole i wyprowadzenia
```
      │ +Vcc
      │
  ────┤ +IN (nieodwracające)
     ╱│╲
    ╱ │ ╲── OUT
   ╱  │  ╲
  ────┤ -IN (odwracające)
      │
      │ -Vcc (lub GND)
```

### Podstawowe układy

#### Wzmacniacz nieodwracający
```
        R2
    ┌───┴───┐
IN ──┤+     │
     │  LM358├── OUT
  ┌──┤-     │
  │  └──────┘  
  │    R1
  └────┴────┐
            │
           GND

Au = 1 + (R2/R1)
Rin = bardzo duża
```

#### Wzmacniacz odwracający
```
     R2
  ┌──┴──┐
  │     │
  ├─────├── OUT  
  │  LM358
IN┴─┤-  │
 R1 │+  │
    ├───┘
    │
   GND

Au = -R2/R1
Rin = R1
```

#### Wtórnik napięciowy (buffer)
```
IN ──┤+
     │  LM358├── OUT = IN
  ┌──┤-     │
  │  └──────┘
  │
  └──────────── (sprzężenie 100%)

Au = 1
Rin = bardzo duża
Rout = bardzo mała
```

### Popularne wzmacniacze operacyjne

#### LM358/LM324
- **Zasilanie**: Single supply 3V-32V
- **GBW**: 1MHz
- **Slew Rate**: 0.5 V/μs
- **Zastosowanie**: Ogólne, tanie aplikacje

#### TL071/TL074  
- **Wejścia**: JFET (bardzo duża Rin)
- **GBW**: 3MHz
- **Slew Rate**: 13 V/μs
- **Zastosowanie**: Audio, precyzyjne pomiary

#### LM741
- **Klasyczny**: Pierwszy popularny Op-Amp
- **Zasilanie**: ±15V (dual supply)
- **Zastosowanie**: Nauka, laboratoria

## 🔄 Filtry analogowe

### Filtry pasywne RC

#### Filtr dolnoprzepustowy
```
Vin ── R ──┬── Vout
           │
           C
           │
          GND

fc = 1/(2πRC) - częstotliwość odcięcia
Tłumienie: 20dB/dekadę poniżej fc
```

#### Filtr górnoprzepustowy
```
Vin ── C ──┬── Vout  
           │
           R
           │
          GND

fc = 1/(2πRC)
Tłumienie: 20dB/dekadę powyżej fc
```

#### Filtr pasmowoprzepustowy
```
         C1    R2
Vin ─────┴───┬─┴──┬── Vout
         R1  │    │
         ┴   C2   │
            ┴    │
           GND   GND

f1 = 1/(2πR1C1) - dolne odcięcie
f2 = 1/(2πR2C2) - górne odcięcie
```

### Filtry aktywne (z Op-Amp)

#### Sallen-Key dolnoprzepustowy
```
       R1    R2
Vin ───┴─────┴───┬── Vout
       │         │
       C1    ┌───┤+
       │     │   │ LM358
       ├─────┤   ├── (połączone)
       │     │-  │
       C2    └───┘
       │    
      GND

Wzmocnienie: Q kontroluje ostrość
```

## ⚡ Zasilacze liniowe

### Stabilizator szeregowy
```
Uin ── R1 ──┬── Q1 ──┬── Uout
            │   │    │
           D1   │    C1
            │   │    │
           GND  │   GND
               │
            R2 ├── Uref (Zener)
               │
              GND

Uout = Uzener + UBE ≈ Uzener + 0.7V
```

### Układy scalone stabilizatorów

#### Seria 78xx (dodatnie)
- **78L05**: +5V, 100mA
- **7805**: +5V, 1A
- **7812**: +12V, 1A
- **7815**: +15V, 1A

#### Seria 79xx (ujemne)
- **79L05**: -5V, 100mA  
- **7905**: -5V, 1A
- **7912**: -12V, 1A

#### LM317 (regulowany)
```
     R1 (240Ω)
Vin ──┤LM317├── Vout
      │ ADJ │
      └──┴──┘
         R2
         ┴
        GND

Vout = 1.25V × (1 + R2/R1)
```

## 🔊 Układy audio

### Wzmacniacz mikrofonowy
```
         R2 (100kΩ)
      ┌───┴───┐
      │       │
MIC ──┤+  TL071├── OUT
   ┌──┤-      │  
   │  └───────┘
   │    R1 (1kΩ)  
   └────┴────┐
             │
            GND

Au = 1 + (R2/R1) = 101 (40dB)
```

### Wzmacniacz słuchawkowy
```
       10μF        100μF
IN ─────┤├── R ──┬─── ┤├─── Słuchawki
             1kΩ │    │
                 │    │
              TL071  GND
              buffer │
                     │
                    GND

Impedancja wyjściowa: < 10Ω
Moc: P = V²/R = 1V²/32Ω = 31mW
```

## 📶 Generatory i oscylatory

### Oscylator RC (mostek Wiena)
```
      R     C
  ┌───┴─────┤├──┐
  │             │
  ├─── R1 ──────┤+
  │             │ LM358
OUT├──────────── │-├── OUT
  │             │
  └─── R2 ──────┘

fo = 1/(2πRC)
Warunek oscylacji: R2/R1 = 2
```

### Oscylator relaksacyjny (555)
```
     +Vcc
       │
    R1 ┴
       ├── TRIG (2)
    R2 ┴     555
       ├── THRESH (6)
       │     │
       C     OUT (3)
       │
      GND

f = 1.44/((R1+2×R2)×C)
Wypełnienie = (R1+R2)/(R1+2×R2)
```

## 🔄 Modulacja i demodulacja

### Modulator AM
```
Sygnał audio ──┐
              ├─ Mixer → AM out
Nośna (RF) ────┘

MAM(t) = (1 + m×sin(ωmt))×sin(ωct)
m - współczynnik modulacji (0-1)
```

### Detektor AM (diodowy)
```
AM in ──┤D├── R ──┬── Audio out
             ┴    │
                  C (filtr)
                  │
                 GND
```

### Modulator FM (VCO)
```
Audio ── Integrator ── VCO ── FM out

f(t) = fc + kf×∫m(t)dt
kf - czułość częstotliwościowa [Hz/V]
```

## 🧮 Pomiary i analiza

### Pomiar wzmocnienia
```
Au = 20×log₁₀(Vout/Vin) [dB]

Przykłady:
Au = 2 → 6dB
Au = 10 → 20dB  
Au = 100 → 40dB
Au = 0.5 → -6dB
```

### Charakterystyka częstotliwościowa
```
|H(jω)| [dB]
  ↑
  0├─────────────
   │        ╲
-3 │         ╲ -20dB/dek
   │          ╲
-20├──────────────╲──→ ω [Hz]
                  fc
```

### Pomiar zniekształceń
```
THD = √(U₂² + U₃² + U₄² + ...) / U₁ × 100%

Gdzie:
U₁ - amplituda podstawowej
U₂,₃,₄... - amplitudy harmonicznych
```

## ⚠️ Problemy i rozwiązania

### Oscylacje pasożytnicze
**Przyczyny**:
- Za duże wzmocnienie
- Dodatnie sprzężenie zwrotne
- Złe rozmieszczenie ścieżek PCB

**Rozwiązania**:
- Kondensator kompensacyjny (pF-nF)
- Rezystor w sprzężeniu zwrotnym
- Kondensatory odsprzęgające zasilanie

### Szumy
**Źródła**:
- Szum termiczny (Johnson): 4kTRB
- Szum śrubowy (shot): 2qIB
- Szum 1/f (różowy): Niskoczęstotliwościowy

**Minimalizacja**:
- Małe rezystancje sygnałowe
- Krótkie połączenia
- Ekranowanie (klatka Faradaya)

### Zasilanie
**Problemy**:
- Tętnienia zasilania → modulacja sygnału
- Spadki napięcia → ograniczenie dynamiki
- Sprzężenia przez zasilanie → oscylacje

**Rozwiązania**:
- Kondensatory filtrujące (μF + nF)
- Stabilizatory napięcia
- Osobne zasilania analogowe/cyfrowe

## 🧮 Ćwiczenia praktyczne

### Ćwiczenie 1: Wzmacniacz audio
Zaprojektuj wzmacniacz o wzmocnieniu 20dB dla sygnału z mikrofonu (1mV → 10mV).

### Ćwiczenie 2: Filtr aktywny
Zbuduj filtr dolnoprzepustowy Sallen-Key z częstotliwością odcięcia 1kHz.

### Ćwiczenie 3: Generator sinusoidalny  
Zaprojektuj oscylator RC na 1kHz z regulacją amplitudy.

## 📚 Powiązane tematy

- [[wzmacniacze_operacyjne|Wzmacniacze Operacyjne - Zaawansowane]]
- [[elektronika_cyfrowa|Elektronika Cyfrowa]]
- [[filtry_rc_lc|Filtry RC i LC]]
- [[oscylatory|Oscylatory i Generatory]]
- [[zasilacze_liniowe|Zasilacze Liniowe]]
- [[audio_elektronika|Elektronika Audio]]

---

#elektronika-analogowa #wzmacniacze #filtry #op-amp #oscylatory #audio #pomiary