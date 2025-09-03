# 66. Dyfrakcja i interferencja światła na dwóch szczelinach. Położenie maksimów i minimów 

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


# Dyfrakcja i interferencja światła na dwóch szczelinach (Younga)

## Co się dzieje w doświadczeniu Younga?

- Światło przechodzi przez **dwie wąskie szczeliny**.
- Na ekranie za szczelinami pojawiają się **jasne i ciemne prążki** (paski).
- To efekt **interferencji** – fale światła nakładają się na siebie:
    - W niektórych miejscach się wzmacniają (jasne prążki – **maksima**)
    - W innych się wygaszają (ciemne prążki – **minima**)

---

## Najważniejsze wzory i co znaczą

### 1. **Różnica dróg optycznych**

To, o ile jedna fala "nadrobiła" względem drugiej: $$\Delta s = d \sin \theta$$

Dla małych kątów (gdy ekran jest daleko): $$\sin \theta \approx \frac{y}{L}$$

$$\Delta s = d \cdot \frac{y}{L}$$

- **d** – odległość między szczelinami
- **y** – odległość od środka ekranu do prążka
- **L** – odległość od szczelin do ekranu

---

### 2. **Gdzie są jasne prążki (maksima)?**

Fale się wzmacniają, gdy różnica dróg to całkowita liczba długości fali: $$\Delta s = m\lambda$$

$$y_m = \frac{m\lambda L}{d}$$

- **m** – numer prążka (0, 1, 2, 3...)

---

### 3. **Gdzie są ciemne prążki (minima)?**

Fale się wygaszają, gdy różnica dróg to pół długości fali więcej: $$\Delta s = (m + \frac{1}{2})\lambda$$

$$y_{min} = \frac{(m + \frac{1}{2})\lambda L}{d}$$

---

### 4. **Odległość między sąsiednimi jasnymi prążkami**

To bardzo ważny wzór! $$\Delta y = \frac{\lambda L}{d}$$

- Im większa długość fali (kolor bardziej czerwony) – prążki dalej od siebie
- Im większa odległość L – prążki dalej od siebie
- Im większa odległość między szczelinami d – prążki bliżej siebie

---

### 5. **Natężenie światła w punkcie na ekranie**

Jak jasny jest prążek w danym miejscu: $$I(\theta) = I_0 \cos^2\left(\frac{\pi d \sin \theta}{\lambda}\right)$$

---

## Przykład liczbowy

Dane:

- $$\lambda = 600,\text{nm} = 600 \times 10^{-9},\text{m}$$
- $$d = 0{,}1,\text{mm} = 10^{-4},\text{m}$$
- $$L = 2,\text{m}$$

Odległość między jasnymi prążkami: $$\Delta y = \frac{600 \times 10^{-9} \times 2}{10^{-4}} = 1{,}2,\text{cm}$$

---

## Co musisz umieć na egzamin?

- **Wyjaśnić, co to interferencja i dyfrakcja** (nakładanie się fal, powstawanie prążków)
- **Znać wzory na położenie maksimów i minimów**
- **Umieć policzyć odległość między prążkami**
- **Wiedzieć, od czego zależy rozstaw prążków** (λ, d, L)
- **Zastosowania**: pomiary długości fali, holografia, kontrola jakości optyki

---

## Proste podsumowanie

- Dwie szczeliny → prążki na ekranie
- Jasne prążki: $$y_m = \frac{m\lambda L}{d}$$
- Ciemne prążki: $$y_{min} = \frac{(m + \frac{1}{2})\lambda L}{d}$$
- Odległość między jasnymi prążkami: $$\Delta y = \frac{\lambda L}{d}$$

---

**Zapamiętaj:**  
Im większa długość fali lub odległość do ekranu, tym prążki są dalej od siebie. Im większa odległość między szczelinami, tym prążki są bliżej siebie.

To jest podstawa, którą musisz znać na egzamin!