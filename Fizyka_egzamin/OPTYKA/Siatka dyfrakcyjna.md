# 68. Siatka dyfrakcyjna

## Definicja i budowa

**Siatka dyfrakcyjna** - układ wielu równoległych szczelin o równych szerokościach i odstępach.

**Parametry siatki:**
- **Stała siatki (d)** - odległość między środkami sąsiednich szczelin
- **Liczba rysek na jednostkę długości (N)**: d = 1/N
- Typowo: 100-1000 rysek/mm

## Warunek głównych maksimów

**Równanie siatki dyfrakcyjnej:**
$$d \sin θ = m\lambda$$

gdzie:
- m = 0, ±1, ±2, ±3, ... (rząd widma)
- θ - kąt pod którym obserwujemy maksimum

## Charakterystyka widma

**Rząd zerowy (m = 0):**
- θ = 0° (kierunek prostoliniowy)
- Wszystkie długości fal się nakładają
- Światło białe → obraz biały

**Rzędy wyższe (m ≠ 0):**
- Różne długości fal pod różnymi kątami
- Światło białe → widmo ciągłe
- Fiolet najbliżej centrum, czerwień najdalej

## Zdolność rozdzielcza siatki

**Zdolność rozdzielcza:**
$$R = \frac{\lambda}{\Delta\lambda} = mN_{tot}$$

gdzie:
- N_{tot} - całkowita liczba rysek siatki
- m - rząd widma

**Im więcej rysek, tym lepsza rozdzielczość!**

## Natężenie dla siatki N szczelin

**Wzór na natężenie:**
$$I(θ) = I_0 \left(\frac{\sin β}{\β}\right)^2 \left(\frac{\sin(N\gamma)}{\sin \gamma}\right)^2$$

gdzie:
- $β = \frac{\pi a \sin θ}{\lambda}$ (a - szerokość szczeliny)
- $γ = \frac{\pi d \sin θ}{\lambda}$

## Właściwości maksimów głównych

- **Ostrość maksimów** rośnie z liczbą szczelin N
- **Jasność maksimów** jest proporcjonalna do N²
- **Szerokość kątowa maksimum** ~ 1/N

## Przykład liczbowy

**Dane:**
- Siatka: 500 rysek/mm → d = 2×10⁻⁶ m
- λ = 589 nm (linia D sodium)
- Szukane: kąt pierwszego maksimum

**Rozwiązanie:**
$$\sin θ_1 = \frac{\lambda}{d} = \frac{589 \times 10^{-9}}{2 \times 10^{-6}} = 0,295$$
$$θ_1 = 17,2°$$

## Zastosowania

- **Spektrometry** - analiza widm
- **Monochromatory** - wydzielanie określonych długości fal
- **Lasery** - elementy rezonatorów
- **Astronomia** - analiza światła gwiazd

![[siatka_dyfrakcyjna.pdf]]
