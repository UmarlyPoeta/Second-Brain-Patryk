# Równania Bernoulliego

## 🎯 Definicja

**Równanie Bernoulliego** ma postać:
$$\frac{dy}{dx} + P(x)y = Q(x)y^n$$

gdzie:
- $P(x)$ i $Q(x)$ to dane funkcje zmiennej $x$
- $n$ to rzeczywista stała, $n \neq 0, 1$

**Nazwa:** Od matematyka Jakoba Bernoulliego (1654-1705)

## 🔄 Przypadki szczególne

- **Gdy $n = 0$:** $\frac{dy}{dx} + P(x)y = Q(x)$ (równanie liniowe)
- **Gdy $n = 1$:** $\frac{dy}{dx} + P(x)y = Q(x)y$ → $\frac{dy}{dx} = [Q(x) - P(x)]y$ (zmienne rozdzielone)

## 🔧 Metoda rozwiązywania - podstawienie Bernoulliego

### Krok 1: Podstawienie
$$v = y^{1-n}$$

### Krok 2: Oblicz pochodną
$$\frac{dv}{dx} = (1-n)y^{-n}\frac{dy}{dx}$$
$$\frac{dy}{dx} = \frac{y^n}{1-n}\frac{dv}{dx}$$

### Krok 3: Podstaw do równania
$$\frac{y^n}{1-n}\frac{dv}{dx} + P(x)y = Q(x)y^n$$

### Krok 4: Podziel przez $y^n$
$$\frac{1}{1-n}\frac{dv}{dx} + P(x)y^{1-n} = Q(x)$$

### Krok 5: Podstaw $v = y^{1-n}$
$$\frac{1}{1-n}\frac{dv}{dx} + P(x)v = Q(x)$$

### Krok 6: Przekształć do postaci liniowej
$$\frac{dv}{dx} + (1-n)P(x)v = (1-n)Q(x)$$

## 📝 Przykłady rozwiązane

### Przykład 1: Podstawowy
**Równanie:** $\frac{dy}{dx} + \frac{y}{x} = y^2$

#### Rozwiązanie:
1. **Identyfikacja:** $P(x) = \frac{1}{x}$, $Q(x) = 1$, $n = 2$
2. **Podstawienie:** $v = y^{1-2} = y^{-1} = \frac{1}{y}$
3. **Pochodna:** $\frac{dv}{dx} = -y^{-2}\frac{dy}{dx}$, więc $\frac{dy}{dx} = -y^2\frac{dv}{dx}$
4. **Podstawienie:** $-y^2\frac{dv}{dx} + \frac{y}{x} = y^2$
5. **Dzielenie przez $y^2$:** $-\frac{dv}{dx} + \frac{1}{xy} = 1$
6. **Podstawienie $v = \frac{1}{y}$:** $-\frac{dv}{dx} + \frac{v}{x} = 1$
7. **Przekształcenie:** $\frac{dv}{dx} - \frac{v}{x} = -1$
8. **Równanie liniowe:** $\frac{dv}{dx} + \left(-\frac{1}{x}\right)v = -1$
9. **Czynnik całkujący:** $\mu(x) = e^{-\int \frac{1}{x}dx} = \frac{1}{x}$
10. **Rozwiązanie:** $\frac{v}{x} = \int \frac{-1}{x}dx = -\ln|x| + C$
11. **Więc:** $v = x(-\ln|x| + C) = -x\ln|x| + Cx$
12. **Powrót:** $\frac{1}{y} = -x\ln|x| + Cx$
13. **Rozwiązanie:** $y = \frac{1}{-x\ln|x| + Cx}$

### Przykład 2: Z wykładnikiem ułamkowym
**Równanie:** $\frac{dy}{dx} + y = y^{1/2}$

#### Rozwiązanie:
1. **Identyfikacja:** $P(x) = 1$, $Q(x) = 1$, $n = \frac{1}{2}$
2. **Podstawienie:** $v = y^{1-1/2} = y^{1/2} = \sqrt{y}$
3. **Pochodna:** $\frac{dv}{dx} = \frac{1}{2\sqrt{y}}\frac{dy}{dx}$, więc $\frac{dy}{dx} = 2\sqrt{y}\frac{dv}{dx}$
4. **Podstawienie:** $2\sqrt{y}\frac{dv}{dx} + y = y^{1/2}$
5. **Dzielenie przez $y^{1/2}$:** $2\frac{dv}{dx} + \sqrt{y} = 1$
6. **Podstawienie $v = \sqrt{y}$:** $2\frac{dv}{dx} + v = 1$
7. **Równanie liniowe:** $\frac{dv}{dx} + \frac{1}{2}v = \frac{1}{2}$
8. **Rozwiązanie:** $v = 1 + Ce^{-x/2}$
9. **Powrót:** $\sqrt{y} = 1 + Ce^{-x/2}$
10. **Rozwiązanie:** $y = (1 + Ce^{-x/2})^2$

## 🌟 Zastosowania praktyczne

### 1. Dynamika populacji z nasyceniem
$$\frac{dN}{dt} = aN - bN^2$$
gdzie $a$ - tempo wzrostu, $b$ - współczynnik konkurencji

### 2. Reakcje chemiczne drugiego rzędu
$$\frac{dc}{dt} + kc = c^2$$
gdzie $c$ - stężenie, $k$ - stała reakcji

### 3. Przepływ w kanałach otwartych
Równania hydrauliczne często przyjmują postać Bernoulliego

## 📊 Algorytm rozwiązywania

```mermaid
graph TD
    A[dy/dx + P(x)y = Q(x)y^n] --> B{n = 0 lub n = 1?}
    B -->|Tak| C[Użyj prostszych metod]
    B -->|Nie| D[Podstawienie v = y^(1-n)]
    D --> E[Oblicz dv/dx]
    E --> F[Podstaw do równania]
    F --> G[Otrzymaj równanie liniowe względem v]
    G --> H[Rozwiąż równanie liniowe]
    H --> I[Podstaw z powrotem y]
```

## ⚠️ Ważne uwagi

1. **Sprawdzenie $n$:** Metoda działa tylko gdy $n \neq 0, 1$
2. **Rozwiązania osobliwe:** Sprawdź $y = 0$ (może być rozwiązaniem)
3. **Dziedzina:** Uważaj na punkty gdzie $y = 0$ lub $y^n$ może być nieokreślone
4. **Znak podstawienia:** Dla $n < 0$ podstawienie może być skomplikowane

## 🔢 Sprawdzenie rozwiązania

Po znalezieniu rozwiązania $y(x)$, sprawdź czy:
$$\frac{dy}{dx} + P(x)y = Q(x)y^n$$

## 🎯 Przykłady do ćwiczeń

1. $\frac{dy}{dx} + 2y = y^3$
2. $x\frac{dy}{dx} - y = xy^2$  
3. $\frac{dy}{dx} - y = e^x y^{1/3}$

## 🔗 Powiązane tematy

- [[Równania liniowe pierwszego rzędu]]
- [[Równania o zmiennych rozdzielonych]]
- [[Równania Riccatiego]]
- [[Modele wzrostu populacji]]
- [[Reakcje chemiczne]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Równanie Bernoulliego | Bernoulli equation |
| Podstawienie Bernoulliego | Bernoulli substitution |
| Równanie liniowe | Linear equation |
| Wykładnik | Exponent |
| Stała reakcji | Reaction constant |
| Dynamika populacji | Population dynamics |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*