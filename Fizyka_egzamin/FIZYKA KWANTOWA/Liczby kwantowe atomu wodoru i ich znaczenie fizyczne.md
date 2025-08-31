# 80. Liczby kwantowe atomu wodoru i ich znaczenie fizyczne

## System liczb kwantowych

Atom wodoru opisują **cztery liczby kwantowe**:

### 1. Główna liczba kwantowa (n)

**Wartości:** n = 1, 2, 3, 4, ... 

**Znaczenie fizyczne:**
- Określa **energię** stanu elektronowego
- Określa **średni promień** orbity
- Związana z **powłokami elektronowymi** (K, L, M, N, ...)

**Energia:**
$$E_n = -\frac{13,6 \text{ eV}}{n^2}$$

**Średni promień:**
$$⟨r⟩_n ≈ \frac{3n^2 - l(l+1)}{2} a_0$$

### 2. Orbitalna liczba kwantowa (l)

**Wartości:** l = 0, 1, 2, ..., (n-1)

**Znaczenie fizyczne:**
- Określa **moment pędu orbitalnego**
- Określa **kształt** orbitalu
- Związana z **podpowłokami** (s, p, d, f, ...)

**Moment pędu:**
$$|L| = \hbar\sqrt{l(l+1)}$$

**Oznaczenia:**
- l = 0 → s (sharp)
- l = 1 → p (principal) 
- l = 2 → d (diffuse)
- l = 3 → f (fundamental)

### 3. Magnetyczna liczba kwantowa (mₗ)

**Wartości:** mₗ = -l, -l+1, ..., 0, ..., l-1, l

**Znaczenie fizyczne:**
- Określa **składową z momentu pędu** orbitalnego
- Określa **orientację** orbitalu w przestrzeni
- **Degeneracja** poziomów energetycznych

**Składowa z momentu pędu:**
$$L_z = m_l \hbar$$

**Liczba stanów:** 2l + 1 dla każdego l

### 4. Spinowa liczba kwantowa (mₛ)

**Wartości:** mₛ = ±1/2

**Znaczenie fizyczne:**
- **Wewnętrzny moment pędu** elektronu
- **Orientacja spinu** w polu magnetycznym
- Nie ma klasycznego odpowiednika

**Moment magnetyczny spinu:**
$$μ_s = -g_s μ_B m_s$$

gdzie gₛ ≈ 2 (żyromagnetyczny stosunek spinu)

## Orbitale atomu wodoru

### Orbital 1s (n=1, l=0, mₗ=0)
- **Kształt:** sferyczny
- **Energia:** E₁ = -13,6 eV
- **Rozmiar:** najwyższe prawdopodobieństwo przy r = a₀

### Orbitale 2s, 2p (n=2)
**2s (l=0):** sferyczny, większy od 1s
**2p (l=1):** hantelkowy, 3 orientacje (mₗ = -1, 0, +1)
- 2pₓ, 2pᵧ, 2pᵧ

### Orbitale 3d (n=3, l=2)
- **5 orientacji** (mₗ = -2, -1, 0, +1, +2)
- Bardziej skomplikowane kształty
- dₓᵧ, dₓz, dᵧz, dx²-y², dz²

## Degeneracja poziomów

**W atomie wodoru** (bez pola zewnętrznego):
- Energie zależą tylko od n
- Degeneracja poziomu n: n²

**Przykłady:**
- n=1: 1 stan (1s)
- n=2: 4 stany (1×2s + 3×2p)  
- n=3: 9 stanów (1×3s + 3×3p + 5×3d)

## Efekt Zeemana

**W polu magnetycznym B:**
- Degeneracja zostaje zniesiona
- Każdy orbital rozszczepia się zgodnie z mₗ

**Zmiana energii:**
$$\Delta E = μ_B g m_l B$$

gdzie μ_B - magneton Bohra

## Zasady wyboru dla przejść

**Reguły dla emisji/absorpcji:**
- Δn = dowolne
- Δl = ±1
- Δmₗ = 0, ±1

**Przykłady dozwolonych przejść:**
- 2p → 1s ✓
- 3d → 2p ✓  
- 3s → 1s ✗ (Δl = 0)

## Notacja spektroskopowa

**Format:** n²ˢ⁺¹Lⱼ

gdzie:
- n - główna liczba kwantowa
- s - całkowity spin
- L - całkowity moment orbitalny (S, P, D, F, ...)
- J - całkowity moment pędu

**Przykłady:**
- Stan podstawowy H: 1²S₁/₂
- Pierwszy stan wzbudzony: 2²S₁/₂, 2²P₁/₂, 2²P₃/₂

## Przykład: Linie widma wodoru

**Seria Balmera (n→2):**
- 3p → 2s: Hα (656 nm, czerwony)
- 4p → 2s: Hβ (486 nm, niebieski)
- 5p → 2s: Hγ (434 nm, fioletowy)

## Moment magnetyczny atomu

**Całkowity moment magnetyczny:**
$$μ = -μ_B \sqrt{J(J+1)} g_J$$

**Żyromagnetyczny stosunek Landé:**
$$g_J = 1 + \frac{J(J+1) + S(S+1) - L(L+1)}{2J(J+1)}$$

## Zastosowania

- **Spektroskopia atomowa** - identyfikacja pierwiastków
- **Rezonans magnetyczny** (NMR, ESR)
- **Lasery atomowe** - projektowanie przejść
- **Chemia kwantowa** - struktura elektronowa

![[wodor.pdf]]
