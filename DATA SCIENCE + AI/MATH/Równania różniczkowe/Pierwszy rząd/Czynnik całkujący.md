# Czynnik całkujący

## 🎯 Definicja i cel

**Czynnik całkujący** (integrating factor) $\mu(x,y)$ to funkcja, przez którą mnożymy równanie różniczkowe:
$$M(x,y)dx + N(x,y)dy = 0$$

aby otrzymać równanie dokładne:
$$\mu M dx + \mu N dy = 0$$

**Cel:** Przekształcić równanie niedokładne w dokładne.

## 🔍 Warunek dokładności po zastosowaniu $\mu$

Po pomnożeniu przez $\mu$, równanie jest dokładne gdy:
$$\frac{\partial(\mu M)}{\partial y} = \frac{\partial(\mu N)}{\partial x}$$

Rozwijając:
$$\mu \frac{\partial M}{\partial y} + M \frac{\partial \mu}{\partial y} = \mu \frac{\partial N}{\partial x} + N \frac{\partial \mu}{\partial x}$$

## 🔧 Przypadki szczególne - łatwiejsze do rozwiązania

### Przypadek 1: $\mu = \mu(x)$ (zależy tylko od $x$)

**Warunek:**
$$\frac{1}{\mu}\frac{d\mu}{dx} = \frac{\frac{\partial M}{\partial y} - \frac{\partial N}{\partial x}}{N}$$

**Jeśli prawa strona zależy tylko od $x$**, to:
$$\mu(x) = e^{\int \frac{\frac{\partial M}{\partial y} - \frac{\partial N}{\partial x}}{N} dx}$$

### Przypadek 2: $\mu = \mu(y)$ (zależy tylko od $y$)

**Warunek:**
$$\frac{1}{\mu}\frac{d\mu}{dy} = \frac{\frac{\partial N}{\partial x} - \frac{\partial M}{\partial y}}{M}$$

**Jeśli prawa strona zależy tylko od $y$**, to:
$$\mu(y) = e^{\int \frac{\frac{\partial N}{\partial x} - \frac{\partial M}{\partial y}}{M} dy}$$

## 📝 Przykłady rozwiązane

### Przykład 1: Czynnik zależny od $x$
**Równanie:** $(2y - 6x)dx + (3x - 4x^2/y)dy = 0$

#### Rozwiązanie:
1. **Sprawdzenie dokładności:**
   - $M = 2y - 6x$, $N = 3x - 4x^2/y$
   - $\frac{\partial M}{\partial y} = 2$
   - $\frac{\partial N}{\partial x} = 3 - 8x/y$
   - $\frac{\partial M}{\partial y} \neq \frac{\partial N}{\partial x}$ (nie jest dokładne)

2. **Próba czynnika $\mu(x)$:**
   $$\frac{\frac{\partial M}{\partial y} - \frac{\partial N}{\partial x}}{N} = \frac{2 - (3 - 8x/y)}{3x - 4x^2/y} = \frac{-1 + 8x/y}{3x - 4x^2/y}$$

   To nie zależy tylko od $x$.

3. **Próba czynnika $\mu(y)$:**
   $$\frac{\frac{\partial N}{\partial x} - \frac{\partial M}{\partial y}}{M} = \frac{(3 - 8x/y) - 2}{2y - 6x} = \frac{1 - 8x/y}{2y - 6x}$$

   To też nie jest proste.

*Ten przykład wymaga bardziej zaawansowanych technik.*

### Przykład 2: Prosty przypadek
**Równanie:** $y dx + (x^2 - x)dy = 0$

#### Rozwiązanie:
1. **Sprawdzenie dokładności:**
   - $M = y$, $N = x^2 - x$
   - $\frac{\partial M}{\partial y} = 1$, $\frac{\partial N}{\partial x} = 2x - 1$
   - Nie jest dokładne

2. **Próba czynnika $\mu(x)$:**
   $$\frac{\frac{\partial M}{\partial y} - \frac{\partial N}{\partial x}}{N} = \frac{1 - (2x - 1)}{x^2 - x} = \frac{2 - 2x}{x(x-1)} = \frac{-2}{x}$$

   To zależy tylko od $x$!

3. **Obliczenie $\mu(x)$:**
   $$\mu(x) = e^{\int \frac{-2}{x} dx} = e^{-2\ln|x|} = \frac{1}{x^2}$$

4. **Nowe równanie:**
   $$\frac{y}{x^2} dx + \frac{x^2 - x}{x^2} dy = 0$$
   $$\frac{y}{x^2} dx + \left(1 - \frac{1}{x}\right) dy = 0$$

5. **Sprawdzenie dokładności:**
   - $M_1 = \frac{y}{x^2}$, $N_1 = 1 - \frac{1}{x}$
   - $\frac{\partial M_1}{\partial y} = \frac{1}{x^2}$
   - $\frac{\partial N_1}{\partial x} = \frac{1}{x^2}$ ✓

6. **Rozwiązanie równania dokładnego:**
   $$F = \int \frac{y}{x^2} dx = -\frac{y}{x} + g(y)$$
   
   Z $\frac{\partial F}{\partial y} = N_1$:
   $$-\frac{1}{x} + g'(y) = 1 - \frac{1}{x}$$
   $$g'(y) = 1$$
   $$g(y) = y$$

7. **Rozwiązanie:** $-\frac{y}{x} + y = C$ → $y\left(1 - \frac{1}{x}\right) = C$

## 🌟 Szczególne typy czynników całkujących

### 1. Czynnik typu $\mu = x^n y^m$
Dla równań jednorodnych czasem można znaleźć czynnik postaci $\mu = x^n y^m$.

### 2. Czynnik typu $\mu = \mu(xy)$
Gdy równanie ma określoną strukturę, czynnik może zależeć od iloczynu $xy$.

### 3. Czynnik typu $\mu = \mu(x^2 + y^2)$
W równaniach z symetrią radialną.

## 📊 Strategia poszukiwania czynnika

```mermaid
graph TD
    A[Równanie niedokładne] --> B[Sprawdź μ(x)]
    B --> C{Czy funkcja zależy tylko od x?}
    C -->|Tak| D[Oblicz μ(x)]
    C -->|Nie| E[Sprawdź μ(y)]
    E --> F{Czy funkcja zależy tylko od y?}
    F -->|Tak| G[Oblicz μ(y)]
    F -->|Nie| H[Spróbuj szczególnych form]
    D --> I[Pomnóż równanie przez μ]
    G --> I
    H --> I
    I --> J[Rozwiąż równanie dokładne]
```

## ⚠️ Trudności i ograniczenia

1. **Nie zawsze istnieje** - czynnik całkujący może nie istnieć w prostej postaci
2. **Trudność znalezienia** - wymaga często intuicji i doświadczenia  
3. **Nieskończenie wiele** - jeśli $\mu$ jest czynnikiem, to $k\mu$ też (gdzie $k$ = const)
4. **Metody numeryczne** - czasem jedyna opcja

## 🎯 Wskazówki praktyczne

1. **Zawsze sprawdź najpierw** $\mu(x)$ i $\mu(y)$
2. **Poszukaj symetrii** w równaniu
3. **Zastanów się nad fizyczną interpretacją** problemu
4. **Sprawdź rozwiązanie** po znalezieniu czynnika

## 🔗 Powiązane tematy

- [[Równania dokładne]]
- [[Równania liniowe pierwszego rzędu]]
- [[Równania jednorodne pierwszego rzędu]]
- [[Równania o zmiennych rozdzielonych]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Czynnik całkujący | Integrating factor |
| Równanie dokładne | Exact equation |
| Równanie niedokładne | Non-exact equation |
| Symetria radialna | Radial symmetry |
| Intuicja matematyczna | Mathematical intuition |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*