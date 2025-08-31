# 82. Przewodniki, izolatory, półprzewodniki

## Teoria pasmowa ciała stałego

**Pasma energetyczne** powstają przez nakładanie się orbitali atomowych w krysztale.

### Pasmo walencyjne (VB - Valence Band)
- Zawiera elektrony walencyjne atomów
- W T = 0 K całkowicie zapełnione

### Pasmo przewodnictwa (CB - Conduction Band)  
- W T = 0 K całkowicie puste
- Elektrony w tym paśmie mogą przewodzić prąd

### Przerwa energetyczna (Eg)
**Przerwa zabroniona** - energia między VB a CB
$$E_g = E_{CB} - E_{VB}$$

## Klasyfikacja materiałów

### Przewodniki (metale)
- **Eg = 0** - pasma VB i CB nakładają się
- **Wysoka przewodność** σ > 10⁶ S/m
- **Opór maleje z temperaturą** (więcej kolizji)

**Przykłady:** Cu, Ag, Au, Al

**Mechanizm przewodzenia:**
- Elektrony swobodne w paśmie przewodnictwa
- Ruch w polu elektrycznym

### Izolatory (dielektryki)
- **Eg > 3 eV** - duża przerwa energetyczna
- **Bardzo niska przewodność** σ < 10⁻⁸ S/m
- Brak elektronów w paśmie przewodnictwa w temperaturze pokojowej

**Przykłady:** Szkło (Eg ≈ 9 eV), Guma (Eg ≈ 7 eV)

### Półprzewodniki
- **0,1 eV < Eg < 3 eV** - umiarkowana przerwa
- **Przewodność rośnie z temperaturą**
- Możliwość kontroli przewodności przez domieszkowanie

## Półprzewodniki samoistne (intrinsic)

**Koncentracja nośników:**
$$n = p = n_i = \sqrt{N_C N_V} e^{-E_g/2kT}$$

gdzie:
- NC, NV - efektywne gęstości stanów
- ni - koncentracja samoistna

**Przykłady (300K):**
- **Si:** Eg = 1,12 eV, ni = 1,5×10¹⁰ cm⁻³
- **Ge:** Eg = 0,67 eV, ni = 2,4×10¹³ cm⁻³  
- **GaAs:** Eg = 1,42 eV, ni = 1,8×10⁶ cm⁻³

## Półprzewodniki domieszne (extrinsic)

### Typ n (donorowy)
**Domieszka:** Atomy 5-walencyjne (P, As, Sb) w Si lub Ge
- **4 elektrony** tworzą wiązania
- **1 elektron** słabo związany → łatwo przechodzi do CB
- **Nośniki większościowe:** elektrony
- **Nośniki mniejszościowe:** dziury

**Energia jonizacji donora:** ED ≈ 0,01-0,05 eV

### Typ p (akceptorowy)  
**Domieszka:** Atomy 3-walencyjne (B, Al, Ga) w Si lub Ge
- **3 elektrony** tworzą wiązania  
- **Brak 1 elektronu** → dziura w VB
- **Nośniki większościowe:** dziury
- **Nośniki mniejszościowe:** elektrony

**Energia jonizacji akceptora:** EA ≈ 0,01-0,05 eV

## Przewodnictwo elektryczne

**Prawo Ohma w skali mikroskopowej:**
$$\vec{J} = σ\vec{E}$$

**Przewodność:**
$$σ = neμ_e + peμ_h$$

gdzie:
- n, p - koncentracje elektronów i dziur
- μe, μh - ruchliwości elektronów i dziur

**Ruchliwość:** μ = vd/E (prędkość unoszenia/pole elektryczne)

## Przykład liczbowy

**Krzem domieszkowany (300K):**
- **Koncentracja domieszki:** ND = 10¹⁶ cm⁻³
- **Ruchliwość elektronów:** μe = 1350 cm²/(V·s)
- **Przewodność:**
$$σ = eN_Dμ_e = 1,6 \times 10^{-19} \times 10^{16} \times 1350 = 2,16 \text{ S/cm}$$

## Temperatura a przewodność

**Metale:** σ(T) ~ T⁻¹ (wzrost kolizji)

**Półprzewodniki samoistne:** 
$$σ(T) ~ e^{-E_g/2kT}$$ (więcej nośników)

**Półprzewodniki domieszne:**
- **Niskie T:** jonizacja domieszek (σ rośnie)
- **Wysokie T:** generacja samoistna (σ rośnie szybko)

![[przewodniki_izolatory_polprzewod.pdf]]