# Rozwiązania ogólne i szczególne

## 🎯 Definicje podstawowe

### Rozwiązanie równania różniczkowego
Funkcja $y = \phi(x)$ jest **rozwiązaniem** równania różniczkowego, jeśli po podstawieniu tej funkcji i jej pochodnych równanie staje się tożsamością.

### Krzywa całkowa
Wykres rozwiązania równania różniczkowego nazywamy **krzywą całkową**.

## 🔍 Typy rozwiązań

### 1. Rozwiązanie ogólne (General Solution)
**Rozwiązanie ogólne** zawiera wszystkie możliwe rozwiązania równania różniczkowego.

**Dla równania rzędu $n$:**
$$y = \phi(x, C_1, C_2, \ldots, C_n)$$

gdzie $C_1, C_2, \ldots, C_n$ to **dowolne stałe całkowania**.

#### Przykład - równanie I rzędu:
$$\frac{dy}{dx} = 2x$$

**Rozwiązanie ogólne:**
$$y = x^2 + C$$

### 2. Rozwiązanie szczególne (Particular Solution)  
**Rozwiązanie szczególne** otrzymujemy przez nadanie konkretnych wartości stałym całkowania.

#### Przykład kontynuacji:
Jeśli $C = 3$, to rozwiązanie szczególne: $y = x^2 + 3$

### 3. Rozwiązanie osobliwe (Singular Solution)
**Rozwiązanie osobliwe** nie może być otrzymane z rozwiązania ogólnego dla żadnych wartości stałych.

## 📊 Równanie drugiego rzędu - przykład

### Równanie:
$$\frac{d^2y}{dx^2} + y = 0$$

### Rozwiązanie ogólne:
$$y = C_1 \cos(x) + C_2 \sin(x)$$

### Rozwiązania szczególne:
- Jeśli $C_1 = 1, C_2 = 0$: $y = \cos(x)$
- Jeśli $C_1 = 0, C_2 = 1$: $y = \sin(x)$  
- Jeśli $C_1 = 2, C_2 = -3$: $y = 2\cos(x) - 3\sin(x)$

## 🎛️ Warunki określające rozwiązanie

### Warunki początkowe (Initial Conditions)
Wartości funkcji i jej pochodnych w jednym punkcie.

**Dla równania II rzędu:**
- $y(x_0) = y_0$
- $y'(x_0) = y'_0$

### Warunki brzegowe (Boundary Conditions)  
Wartości funkcji w różnych punktach.

**Przykład:**
- $y(0) = 1$
- $y(1) = 2$

## 📝 Przykład kompletny

### Zadanie:
Rozwiąż równanie $y'' - 4y = 0$ z warunkami początkowymi $y(0) = 1$, $y'(0) = 2$.

### Rozwiązanie:

#### Krok 1: Znajdź rozwiązanie ogólne
Równanie charakterystyczne: $r^2 - 4 = 0$
$$r = \pm 2$$

**Rozwiązanie ogólne:**
$$y = C_1 e^{2x} + C_2 e^{-2x}$$

#### Krok 2: Zastosuj warunki początkowe
$$y(0) = C_1 + C_2 = 1$$
$$y'(x) = 2C_1 e^{2x} - 2C_2 e^{-2x}$$
$$y'(0) = 2C_1 - 2C_2 = 2$$

#### Krok 3: Rozwiąż układ równań
$\begin{cases} C_1 + C_2 = 1 \\ 2C_1 - 2C_2 = 2 \end{cases}$

Z drugiego równania: $C_1 - C_2 = 1$

Rozwiązując: $C_1 = 1$, $C_2 = 0$

**Rozwiązanie szczególne:**
$$y = e^{2x}$$

## 🔢 Liczba stałych całkowania

| Rząd równania | Liczba stałych | Liczba warunków |
|---------------|----------------|-----------------|
| I | 1 | 1 |
| II | 2 | 2 |
| III | 3 | 3 |
| n | n | n |

## ⚠️ Zagadnienia graniczne

### Twierdzenie Cauchy'ego-Lipschitza
Dla równania $y' = f(x,y)$ z warunkiem $y(x_0) = y_0$:

**Jeśli** $f$ i $\frac{\partial f}{\partial y}$ są ciągłe w otoczeniu punktu $(x_0, y_0)$,
**to** istnieje dokładnie jedno rozwiązanie.

### Istnienie i jednoznaczność
- **Istnienie** - czy rozwiązanie w ogóle istnieje?
- **Jednoznaczność** - czy rozwiązanie jest tylko jedno?

## 🔗 Powiązane tematy

- [[Definicja równania różniczkowego]]
- [[Warunki początkowe i brzegowe]]
- [[Równania liniowe pierwszego rzędu]]
- [[Równania liniowe jednorodne o stałych współczynnikach]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Rozwiązanie ogólne | General solution |
| Rozwiązanie szczególne | Particular solution |
| Rozwiązanie osobliwe | Singular solution |
| Stała całkowania | Integration constant |
| Krzywa całkowa | Integral curve |
| Warunki początkowe | Initial conditions |
| Warunki brzegowe | Boundary conditions |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*