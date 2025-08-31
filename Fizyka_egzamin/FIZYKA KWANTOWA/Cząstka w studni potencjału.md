# 79. Cząstka w studni potencjału

## Model nieskończonej studni potencjału

**Potencjał:**
$$V(x) = \begin{cases} 
0 & \text{dla } 0 < x < L \\
∞ & \text{dla } x ≤ 0 \text{ lub } x ≥ L
\end{cases}$$

**Warunki brzegowe:**
$$ψ(0) = 0 \quad \text{i} \quad ψ(L) = 0$$

## Rozwiązanie równania Schrödingera

**Wewnątrz studni (V = 0):**
$$-\frac{\hbar^2}{2m}\frac{d^2ψ}{dx^2} = Eψ$$

**Ogólne rozwiązanie:**
$$ψ(x) = A\sin(kx) + B\cos(kx)$$

gdzie $k = \sqrt{2mE}/\hbar$

**Zastosowanie warunków brzegowych:**
- ψ(0) = 0 → B = 0
- ψ(L) = 0 → sin(kL) = 0 → kL = nπ

## Funkcje falowe i energie

**Skwantowane wartości k:**
$$k_n = \frac{nπ}{L}, \quad n = 1, 2, 3, ...$$

**Poziomy energetyczne:**
$$E_n = \frac{\hbar^2k_n^2}{2m} = \frac{n^2π^2\hbar^2}{2mL^2}$$

**Znormalizowane funkcje falowe:**
$$ψ_n(x) = \sqrt{\frac{2}{L}}\sin\left(\frac{nπx}{L}\right)$$

## Właściwości rozwiązań

### Energia punktu zerowego
$$E_1 = \frac{π^2\hbar^2}{2mL^2} > 0$$

**Cząstka nie może mieć zerowej energii!** (następstwo zasady nieoznaczoności)

### Degeneracja
**Każdy poziom jest niezdegenerowany** - jedna funkcja falowa dla każdej energii.

### Parzystość
- **n nieparzyste**: ψ_n(-x) = -ψ_n(x) (nieparzyste)
- **n parzyste**: ψ_n(-x) = ψ_n(x) (parzyste)

## Przykład liczbowy

**Dane:**
- Elektron w studni L = 1 nm
- m = 9,1×10⁻³¹ kg

**Energia stanu podstawowego:**
$$E_1 = \frac{π^2 \times (1,05 \times 10^{-34})^2}{2 \times 9,1 \times 10^{-31} \times (10^{-9})^2}$$
$$E_1 = 6,0 \times 10^{-20} \text{ J} = 0,38 \text{ eV}$$

**Energia pierwszego stanu wzbudzonego:**
$$E_2 = 4E_1 = 1,52 \text{ eV}$$

## Studnia skończona

**Potencjał:**
$$V(x) = \begin{cases} 
V_0 & \text{dla } x < 0 \text{ lub } x > L \\
0 & \text{dla } 0 < x < L
\end{cases}$$

**Właściwości:**
- Funkcja falowa "przecieka" do obszarów zabronionych
- Skończona liczba stanów związanych
- Energie wyższe niż w studni nieskończonej

## Zastosowania

**Kwantowe kropki (quantum dots):**
- Półprzewodnikowe nanostruktury
- Kontrolowane właściwości optyczne
- Zastosowania w LED i laserach

**Studnie kwantowe:**
- Heterostruktury półprzewodnikowe
- Lasery kwantowe
- Efekt Hall'a kwantowy

**Molekuły:**
- Przybliżenie delokalizacji elektronów
- Przewodnictwo w łańcuchach węglowych

## Analogie klasyczne

**Fala stojąca na strunie:**
- Podobne warunki brzegowe
- Skwantowane częstotliwości drgań
- λ = 2L/n

**Różnica**: W mechanice kwantowej energia jest skwantowana, nie tylko częstotliwość.

![[studnia_potencjału.pdf]]
