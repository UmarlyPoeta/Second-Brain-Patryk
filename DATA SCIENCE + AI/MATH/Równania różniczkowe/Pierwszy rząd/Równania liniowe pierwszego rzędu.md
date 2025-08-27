# Równania liniowe pierwszego rzędu

## 🎯 Definicja i postać standardowa

**Równanie liniowe pierwszego rzędu** ma postać:
$$\frac{dy}{dx} + P(x)y = Q(x)$$

gdzie $P(x)$ i $Q(x)$ to dane funkcje zmiennej $x$.

### Klasyfikacja:
- **Jednorodne:** gdy $Q(x) = 0$ → $\frac{dy}{dx} + P(x)y = 0$
- **Niejednorodne:** gdy $Q(x) \neq 0$ → $\frac{dy}{dx} + P(x)y = Q(x)$

## 🔧 Metoda czynnika całkującego

### Krok 1: Znajdź czynnik całkujący
$$\mu(x) = e^{\int P(x) dx}$$

### Krok 2: Pomnoż równanie przez $\mu(x)$
$$\mu(x)\frac{dy}{dx} + \mu(x)P(x)y = \mu(x)Q(x)$$

### Krok 3: Rozpoznaj pochodną iloczynu
Lewa strona to $\frac{d}{dx}[\mu(x)y]$:
$$\frac{d}{dx}[\mu(x)y] = \mu(x)Q(x)$$

### Krok 4: Całkuj
$$\mu(x)y = \int \mu(x)Q(x) dx + C$$

### Krok 5: Rozwiąż względem $y$
$$y = \frac{1}{\mu(x)}\left[\int \mu(x)Q(x) dx + C\right]$$

## 📝 Przykłady rozwiązane

### Przykład 1: Równanie jednorodne
**Równanie:** $\frac{dy}{dx} + 2y = 0$

#### Rozwiązanie:
1. **Identyfikacja:** $P(x) = 2$, $Q(x) = 0$
2. **Czynnik całkujący:** $\mu(x) = e^{\int 2 dx} = e^{2x}$
3. **Mnożenie:** $e^{2x}\frac{dy}{dx} + 2e^{2x}y = 0$
4. **Rozpoznanie:** $\frac{d}{dx}[e^{2x}y] = 0$
5. **Całkowanie:** $e^{2x}y = C$
6. **Rozwiązanie:** $y = Ce^{-2x}$

### Przykład 2: Równanie niejednorodne
**Równanie:** $\frac{dy}{dx} + y = e^x$

#### Rozwiązanie:
1. **Identyfikacja:** $P(x) = 1$, $Q(x) = e^x$
2. **Czynnik całkujący:** $\mu(x) = e^{\int 1 dx} = e^x$
3. **Mnożenie:** $e^x\frac{dy}{dx} + e^x y = e^{2x}$
4. **Rozpoznanie:** $\frac{d}{dx}[e^x y] = e^{2x}$
5. **Całkowanie:** $e^x y = \int e^{2x} dx = \frac{1}{2}e^{2x} + C$
6. **Rozwiązanie:** $y = \frac{1}{2}e^x + Ce^{-x}$

### Przykład 3: Ze współczynnikami zmiennymi
**Równanie:** $x\frac{dy}{dx} + y = x^2$, $x > 0$

#### Rozwiązanie:
1. **Postać standardowa:** $\frac{dy}{dx} + \frac{1}{x}y = x$
2. **Identyfikacja:** $P(x) = \frac{1}{x}$, $Q(x) = x$
3. **Czynnik całkujący:** $\mu(x) = e^{\int \frac{1}{x} dx} = e^{\ln|x|} = x$
4. **Mnożenie:** $x\frac{dy}{dx} + y = x^2$
5. **Rozpoznanie:** $\frac{d}{dx}[xy] = x^2$
6. **Całkowanie:** $xy = \int x^2 dx = \frac{x^3}{3} + C$
7. **Rozwiązanie:** $y = \frac{x^2}{3} + \frac{C}{x}$

## 🏗️ Struktura rozwiązania

Rozwiązanie równania niejednorodnego składa się z dwóch części:
$$y = y_h + y_p$$

gdzie:
- $y_h$ - **rozwiązanie jednorodne** (rozwiązanie równania $\frac{dy}{dx} + P(x)y = 0$)
- $y_p$ - **rozwiązanie szczególne** równania niejednorodnego

### Przykład struktury:
Dla równania $\frac{dy}{dx} + y = e^x$:
- $y_h = Ce^{-x}$ (rozwiązanie jednorodne)
- $y_p = \frac{1}{2}e^x$ (rozwiązanie szczególne)
- $y = Ce^{-x} + \frac{1}{2}e^x$ (rozwiązanie pełne)

## 🌟 Zastosowania praktyczne

### 1. Obwody RC
**Równanie:** $RC\frac{dq}{dt} + q = V(t)$

gdzie $q$ - ładunek, $V(t)$ - napięcie wymuszające

### 2. Mieszanki i rozcieńczanie
**Równanie:** $\frac{dx}{dt} + \frac{F}{V}x = \frac{F \cdot c_{in}}{V}$

gdzie $x$ - ilość substancji, $F$ - przepływ, $V$ - objętość

### 3. Wzrost populacji z ograniczeniami
**Równanie:** $\frac{dN}{dt} + aN = b$

gdzie $N$ - populacja, $a, b$ - parametry modelu

## 📊 Algorytm rozwiązywania

```mermaid
graph TD
    A[dy/dx + P(x)y = Q(x)] --> B[Znajdź μ(x) = e^∫P(x)dx]
    B --> C[Pomnoż równanie przez μ(x)]
    C --> D[Rozpoznaj d/dx[μ(x)y]]
    D --> E[Całkuj: μ(x)y = ∫μ(x)Q(x)dx + C]
    E --> F[Rozwiąż: y = (∫μ(x)Q(x)dx + C)/μ(x)]
```

## ⚠️ Ważne uwagi

1. **Postać standardowa** - zawsze sprowadź do postaci $\frac{dy}{dx} + P(x)y = Q(x)$
2. **Czynnik całkujący** - nie dodawaj stałej przy obliczaniu $\mu(x)$
3. **Całkowanie** - pamiętaj o stałej $C$ przy ostatecznym całkowaniu
4. **Dziedzina** - sprawdź gdzie $P(x)$ i $Q(x)$ są określone

## 🔢 Sprawdzenie rozwiązania

Zawsze sprawdź przez podstawienie do oryginalnego równania:
$$\frac{d}{dx}[rozwiązanie] + P(x) \cdot [rozwiązanie] = Q(x)$$

## 🔗 Powiązane tematy

- [[Równania o zmiennych rozdzielonych]]
- [[Równania Bernoulliego]]
- [[Czynnik całkujący]]
- [[Obwody elektryczne RLC]]
- [[Modele wzrostu populacji]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Równanie liniowe | Linear equation |
| Czynnik całkujący | Integrating factor |
| Równanie jednorodne | Homogeneous equation |
| Równanie niejednorodne | Non-homogeneous equation |
| Rozwiązanie szczególne | Particular solution |
| Postać standardowa | Standard form |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*