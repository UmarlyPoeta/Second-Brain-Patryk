# Równania dokładne

## 🎯 Definicja

**Równanie dokładne** (exact equation) ma postać:
$$M(x,y)dx + N(x,y)dy = 0$$

gdzie istnieje funkcja $F(x,y)$ taka, że:
- $\frac{\partial F}{\partial x} = M(x,y)$
- $\frac{\partial F}{\partial y} = N(x,y)$

Rozwiązaniem jest wówczas: $F(x,y) = C$

## 🔍 Kryterium dokładności

Równanie $M(x,y)dx + N(x,y)dy = 0$ jest **dokładne** wtedy i tylko wtedy, gdy:
$$\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}$$

**Uzasadnienie:** Z twierdzenia Schwarza o równości pochodnych mieszanych.

## 🔧 Metoda rozwiązywania

### Krok 1: Sprawdź kryterium dokładności
Oblicz $\frac{\partial M}{\partial y}$ i $\frac{\partial N}{\partial x}$

### Krok 2: Znajdź funkcję $F(x,y)$
**Metoda A:** Całkuj $M$ względem $x$:
$$F(x,y) = \int M(x,y) dx + g(y)$$

gdzie $g(y)$ to nieznana funkcja $y$.

**Metoda B:** Całkuj $N$ względem $y$:
$$F(x,y) = \int N(x,y) dy + h(x)$$

gdzie $h(x)$ to nieznana funkcja $x$.

### Krok 3: Znajdź nieznaną funkcję
Użyj warunku $\frac{\partial F}{\partial y} = N$ lub $\frac{\partial F}{\partial x} = M$

### Krok 4: Zapisz rozwiązanie
$$F(x,y) = C$$

## 📝 Przykłady rozwiązane

### Przykład 1: Podstawowy
**Równanie:** $(2xy + 3)dx + (x^2 - 1)dy = 0$

#### Rozwiązanie:
1. **Identyfikacja:** $M = 2xy + 3$, $N = x^2 - 1$

2. **Sprawdzenie dokładności:**
   - $\frac{\partial M}{\partial y} = \frac{\partial}{\partial y}(2xy + 3) = 2x$
   - $\frac{\partial N}{\partial x} = \frac{\partial}{\partial x}(x^2 - 1) = 2x$
   - $\frac{\partial M}{\partial y} = \frac{\partial N}{\partial x}$ ✓ (równanie jest dokładne)

3. **Znajdowanie $F$:** Całkujemy $M$ względem $x$:
   $$F(x,y) = \int (2xy + 3) dx = x^2y + 3x + g(y)$$

4. **Znajdowanie $g(y)$:** Używamy warunku $\frac{\partial F}{\partial y} = N$:
   $$\frac{\partial F}{\partial y} = x^2 + g'(y) = x^2 - 1$$
   $$g'(y) = -1$$
   $$g(y) = -y + C_1$$

5. **Rozwiązanie:**
   $$F(x,y) = x^2y + 3x - y = C$$

### Przykład 2: Z funkcjami trygonometrycznymi
**Równanie:** $(\cos(x)\cos(y) - y\sin(x))dx - (\sin(x)\sin(y) + \cos(x))dy = 0$

#### Rozwiązanie:
1. **Identyfikacja:**
   - $M = \cos(x)\cos(y) - y\sin(x)$
   - $N = -(\sin(x)\sin(y) + \cos(x))$

2. **Sprawdzenie dokładności:**
   - $\frac{\partial M}{\partial y} = -\cos(x)\sin(y) - \sin(x)$
   - $\frac{\partial N}{\partial x} = -(\cos(x)\sin(y) + (-\sin(x))) = -\cos(x)\sin(y) + \sin(x)$
   - $\frac{\partial M}{\partial y} \neq \frac{\partial N}{\partial x}$ ❌

*To równanie nie jest dokładne i wymaga czynnika całkującego.*

### Przykład 3: Sprawdzenie przez całkowanie $N$
**Równanie:** $(3x^2 + 2xy)dx + (x^2 + 2y)dy = 0$

#### Rozwiązanie:
1. **Sprawdzenie:** $\frac{\partial M}{\partial y} = 2x$, $\frac{\partial N}{\partial x} = 2x$ ✓

2. **Całkowanie $N$ względem $y$:**
   $$F(x,y) = \int (x^2 + 2y) dy = x^2y + y^2 + h(x)$$

3. **Znajdowanie $h(x)$:**
   $$\frac{\partial F}{\partial x} = 2xy + h'(x) = 3x^2 + 2xy$$
   $$h'(x) = 3x^2$$
   $$h(x) = x^3 + C_1$$

4. **Rozwiązanie:** $x^3 + x^2y + y^2 = C$

## 🌟 Interpretacja geometryczna

Równanie dokładne reprezentuje **linie poziomicowe** (level curves) funkcji $F(x,y)$.

Rozwiązanie $F(x,y) = C$ to rodzina krzywych, z których każda odpowiada stałej wartości funkcji $F$.

## ⚠️ Gdy równanie nie jest dokładne

Jeśli $\frac{\partial M}{\partial y} \neq \frac{\partial N}{\partial x}$, równanie nie jest dokładne, ale można:

1. **Znaleźć czynnik całkujący** $\mu(x,y)$
2. **Pomnożyć równanie przez $\mu$:**
   $$\mu M dx + \mu N dy = 0$$
3. **Nowe równanie może być dokładne**

## 🔍 Sprawdzenie rozwiązania

Po znalezieniu $F(x,y) = C$, sprawdź przez różniczkowanie zupełne:
$$dF = \frac{\partial F}{\partial x}dx + \frac{\partial F}{\partial y}dy = M dx + N dy$$

## 📊 Algorytm rozwiązywania

```mermaid
graph TD
    A[M dx + N dy = 0] --> B[Sprawdź: ∂M/∂y = ∂N/∂x?]
    B -->|Tak| C[Równanie dokładne]
    B -->|Nie| D[Znajdź czynnik całkujący]
    C --> E[F = ∫M dx + g(y)]
    E --> F[Znajdź g(y) z ∂F/∂y = N]
    F --> G[Rozwiązanie: F(x,y) = C]
    D --> H[μM dx + μN dy = 0]
    H --> B
```

## 🎯 Wskazówki praktyczne

1. **Kolejność całkowania** - wybierz prostszą funkcję do całkowania
2. **Sprawdź obliczenia** - pochodne mieszane muszą się zgadzać
3. **Stałe całkowania** - możesz pominąć przy znajdowaniu $F$
4. **Weryfikacja** - zawsze sprawdź rozwiązanie

## 🔗 Powiązane tematy

- [[Czynnik całkujący]]
- [[Równania o zmiennych rozdzielonych]]
- [[Równania liniowe pierwszego rzędu]]
- [[Zastosowania geometryczne równań pierwszego rzędu]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Równanie dokładne | Exact equation |
| Kryterium dokładności | Exactness condition |
| Różniczka zupełna | Total differential |
| Pochodna mieszana | Mixed partial derivative |
| Linie poziomicowe | Level curves |
| Czynnik całkujący | Integrating factor |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*