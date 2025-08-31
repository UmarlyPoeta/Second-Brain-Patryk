# 85. Klasyfikacja ciał ze względu na własności magnetyczne

## Podstawowe pojęcia

### Magnetyzacja (M)
**Definicja:** Magnetyczny moment dipolowy na jednostkę objętości
$$\vec{M} = \frac{\sum \vec{μ}}{V}$$

### Podatność magnetyczna (χ)
$$\vec{M} = χ\vec{H}$$

gdzie H - natężenie pola magnetycznego

### Przenikalność magnetyczna
$$μ = μ_0(1 + χ)$$

**Przenikalność względna:**
$$μ_r = 1 + χ$$

## Klasyfikacja materiałów magnetycznych

### 1. Diamagnetyki (χ < 0)

**Właściwości:**
- **χ ≈ -10⁻⁶ do -10⁻⁴**
- **Słabe odpychanie** przez magnes
- **Temperatura nie wpływa** na χ
- **Wszystkie substancje** mają składową diamagnetyczną

**Mechanizm:** Indukowane prądy orbitalny (prawo Lenza)

**Przykłady:** Cu, Ag, Au, Bi, woda, szkło, większość organicznych

### 2. Paramagnetyki (χ > 0)

**Właściwości:**
- **χ ≈ 10⁻⁶ do 10⁻²**
- **Słabe przyciąganie** przez magnes  
- **Podatność maleje z temperaturą** (prawo Curie)

**Prawo Curie:**
$$χ = \frac{C}{T}$$

gdzie C - stała Curie

**Mechanizm:** Orientacja stałych momentów magnetycznych atomów

**Przykłady:** Al, Pt, Mn, O₂, sole metali przejściowych

### 3. Ferromagnetyki (χ >> 0)

**Właściwości:**
- **χ ≈ 10² do 10⁶** 
- **Silne przyciąganie** przez magnes
- **Spontaniczna magnetyzacja** poniżej temperatury Curie
- **Histerea magnetyczna**

**Prawo Curie-Weissa (T > Tc):**
$$χ = \frac{C}{T - T_C}$$

**Przykłady:** Fe (TC = 1043 K), Ni (TC = 627 K), Co (TC = 1388 K)

### 4. Antyferromagnetyki

**Właściwości:**
- **Momenty sąsiednich atomów** ustawione antyrównolegle
- **Brak wypadkowej magnetyzacji** w T = 0
- **Maksimum χ** przy temperaturze Néela (TN)

**Przykłady:** MnO (TN = 122 K), Cr (TN = 311 K)

### 5. Ferrimagnetyki

**Właściwości:**
- **Dwie podsieci** z różnymi momentami magnetycznymi
- **Niekompensowane momenty** → wypadkowa magnetyzacja
- **Podobne do ferromagnetyków**, ale słabsze

**Przykłady:** Ferryty (Fe₃O₄, γ-Fe₂O₃)

## Teoria wymian

**Całka wymiany (J):**
- **J > 0:** sprzężenie ferromagnetyczne
- **J < 0:** sprzężenie antyferromagnetyczne

**Hamiltonian Heisenberga:**
$$H = -2J \sum_{i,j} \vec{S_i} \cdot \vec{S_j}$$

## Domeny magnetyczne

**Domeny Weissa:**
- Obszary jednolitej magnetyzacji
- Minimalizacja energii magnetostatycznej
- Ściany domenowe - obszary przejściowe

**Proces magnesowania:**
1. **Odwracalne przemieszczenia** ścian domenowych
2. **Nieodwracalne skoki** ścian (skutek Barkhausena)
3. **Rotacja magnetyzacji** domen

## Histereza magnetyczna

**Charakterystyczne punkty:**
- **Magnetyzacja nasycenia (Ms)** - maksymalna magnetyzacja
- **Magnetyzacja szczątkowa (Mr)** - po usunięciu pola
- **Pole koercji (Hc)** - pole zerujące magnetyzację

**Energia histerezy:**
$$W = \oint H \, dM$$

## Przykłady liczbowe

**Żelazo (300K):**
- **χ ≈ 5000** (w słabych polach)
- **Ms = 1,7×10⁶ A/m**
- **TC = 1043 K**

**Porównanie podatności:**
- **Bi (diamagnetyk):** χ = -1,66×10⁻⁴
- **Al (paramagnetyk):** χ = 2,2×10⁻⁵  
- **Fe (ferromagnetyk):** χ ≈ 5000

## Materiały magnetyczne w technice

### Magnesy trwałe
**Wysokie:** Mr, Hc, (BH)max
**Materiały:** SmCo₅, Nd₂Fe₁₄B, Alnico

### Materiały magnetycznie miękkie  
**Niskie:** Hc, straty na histerezę
**Zastosowania:** Rdzenie transformatorów, silników
**Materiały:** Fe-Si, permalloy, ferryty

### Materiały magnetycznie twarde
**Wysokie:** Hc, Mr
**Zastosowania:** Magnesy trwałe, pamięci magnetyczne

## Zastosowania

**Pamięci magnetyczne:**
- Dyski twarde (HDD)
- Taśmy magnetyczne
- Karty magnetyczne

**Czujniki:**
- Czujniki Hall'a
- Magnetometry
- Kompasy elektroniczne

**Energetyka:**
- Transformatory
- Silniki elektryczne  
- Generatory

![[Wlasnosci magnetyczne.pdf]]
