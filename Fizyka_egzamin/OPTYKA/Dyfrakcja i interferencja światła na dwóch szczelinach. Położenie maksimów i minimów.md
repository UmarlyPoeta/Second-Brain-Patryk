# 66. Dyfrakcja i interferencja światła na dwóch szczelinach. Położenie maksimów i minimów (*)

## Układ dwóch szczelin Younga

**Opis doświadczenia:**
- Światło monochromatyczne (długość fali λ) pada na dwie równoległe szczeliny
- Odległość między szczelinami: d
- Odległość od szczelin do ekranu: L (L >> d)

## Wyprowadzenie wzoru na różnicę dróg (*)

**Geometria układu:**
- Punkt P na ekranie w odległości y od środka
- Kąt θ między osią układu a kierunkiem do punktu P

**Różnica dróg optycznych:**
$$\Delta = d \sin θ$$

Dla małych kątów: $\sin θ ≈ \tan θ = \frac{y}{L}$

Zatem:
$$\Delta = d \cdot \frac{y}{L}$$

## Warunki interferencji

**Interferencja konstruktywna (maksima jasne):**
$$\Delta = m\lambda$$

gdzie m = 0, ±1, ±2, ±3, ... (rząd interferencji)

**Położenie maksimów:**
$$y_m = \frac{m\lambda L}{d}$$

**Interferencja destruktywna (minima ciemne):**
$$\Delta = (m + \frac{1}{2})\lambda$$

gdzie m = 0, ±1, ±2, ±3, ...

**Położenie minimów:**
$$y_{min} = \frac{(m + \frac{1}{2})\lambda L}{d}$$

## Wyprowadzenie wzoru na odległość między prążkami (*)

**Odległość między sąsiednimi maksimami:**
$$\Delta y = y_{m+1} - y_m = \frac{(m+1)\lambda L}{d} - \frac{m\lambda L}{d}$$

$$\Delta y = \frac{\lambda L}{d}$$

## Rozkład natężenia

**Wzór na natężenie:**
$$I(θ) = I_0 \cos^2\left(\frac{\pi d \sin θ}{\lambda}\right)$$

gdzie I₀ - maksymalne natężenie

## Przykład liczbowy

**Dane:**
- λ = 600 nm (światło pomarańczowe)
- d = 0,1 mm = 10⁻⁴ m
- L = 2 m

**Odległość między prążkami:**
$$\Delta y = \frac{600 \times 10^{-9} \times 2}{10^{-4}} = 1,2 \text{ cm}$$

## Zastosowania

- Spektrometry interferometryczne
- Pomiary długości fali światła
- Kontrola jakości powierzchni optycznych
- Holografia

![[dyfrakcja_dwa.pdf]]

![[dyfrakcja_dwa_dalej.pdf]]
