# 75. Model atomu Bohra (*)

## Postulaty Bohra (1913)

### Postulat I - Orbity stacjonarne
Elektron porusza się po określonych orbitach kołowych, na których nie promieniuje energii.

**Warunek kwantowania momentu pędu:**
$$L = mvr = n\hbar$$

gdzie:
- n = 1, 2, 3, ... (główna liczba kwantowa)
- ℏ = h/2π - zredukowana stała Plancka

### Postulat II - Emisja i absorpcja
Atom emituje lub absorbuje energię tylko przy przejściach między orbitami stacjonarnymi.

**Warunek częstotliwości:**
$$hf = E_n - E_m$$

## Wyprowadzenie promieni orbit (*)

**Siła Coulomba = Siła dośrodkowa:**
$$\frac{ke^2}{r^2} = \frac{mv^2}{r}$$

**Z warunku kwantowania:**
$$v = \frac{n\hbar}{mr}$$

Podstawiając do równania sił:
$$\frac{ke^2}{r^2} = \frac{m}{r} \cdot \frac{n^2\hbar^2}{m^2r^2}$$

$$\frac{ke^2}{r^2} = \frac{n^2\hbar^2}{mr^3}$$

**Promienie orbit Bohra:**
$$r_n = \frac{n^2\hbar^2}{mke^2} = n^2 a_0$$

gdzie $a_0 = \frac{\hbar^2}{mke^2} = 0,529$ Å - promień Bohra

## Wyprowadzenie poziomów energetycznych (*)

**Energia kinetyczna:**
$$E_k = \frac{1}{2}mv^2 = \frac{ke^2}{2r}$$

**Energia potencjalna:**
$$E_p = -\frac{ke^2}{r}$$

**Energia całkowita:**
$$E_n = E_k + E_p = \frac{ke^2}{2r} - \frac{ke^2}{r} = -\frac{ke^2}{2r}$$

Podstawiając r_n:
$$E_n = -\frac{mk^2e^4}{2n^2\hbar^2} = -\frac{13,6 \text{ eV}}{n^2}$$

## Widmo atomu wodoru

**Seria Lymana** (n → 1, UV):
$$\frac{1}{λ} = R_H \left(\frac{1}{1^2} - \frac{1}{n^2}\right)$$

**Seria Balmera** (n → 2, widzialne):
$$\frac{1}{λ} = R_H \left(\frac{1}{2^2} - \frac{1}{n^2}\right)$$

**Seria Paschena** (n → 3, IR):
$$\frac{1}{λ} = R_H \left(\frac{1}{3^2} - \frac{1}{n^2}\right)$$

**Stała Rydberga:**
$$R_H = \frac{mk^2e^4}{4π c \hbar^3} = 1,097 \times 10^7 \text{ m}^{-1}$$

## Przykłady liczbowe

**Energia poziomów:**
- E₁ = -13,6 eV (stan podstawowy)
- E₂ = -3,4 eV
- E₃ = -1,51 eV
- E₄ = -0,85 eV

**Linia Hα (n=3→2):**
$$E = E_3 - E_2 = -1,51 - (-3,4) = 1,89 \text{ eV}$$
$$λ = \frac{hc}{E} = \frac{1240 \text{ eV·nm}}{1,89 \text{ eV}} = 656 \text{ nm}$$ (czerwony)

## Ograniczenia modelu Bohra

**Sukcesy:**
- Wyjaśnił widmo wodoru
- Przewidział stałą Rydberga
- Wprowadził kwantowanie

**Problemy:**
- Nie wyjaśnia atomów wieloelektronowych
- Nie przewiduje intensywności linii
- Nie uwzględnia spinu elektronu
- Niezgodny z zasadą nieoznaczoności

## Uogólnienia

**Wzór Bohra-Sommerfelda:**
$$\oint p \, dq = nh$$

**Atomy wodoropodobne (Z > 1):**
$$r_n = \frac{n^2 a_0}{Z}$$
$$E_n = -\frac{13,6 Z^2}{n^2} \text{ eV}$$
