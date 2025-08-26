# Rząd i stopień równania różniczkowego

## 🎯 Definicje podstawowe

### Rząd równania (Order)
**Rząd** równania różniczkowego to najwyższa pochodna występująca w równaniu.

#### Przykłady:
- $y' + 2y = x$ → **I rząd** (najwyższa pochodna: $y'$)
- $y'' + 3y' - 4y = 0$ → **II rząd** (najwyższa pochodna: $y''$)
- $y''' + 2y'' + y' = \sin(x)$ → **III rząd** (najwyższa pochodna: $y'''$)

### Stopień równania (Degree)
**Stopień** to najwyższa potęga najwyższej pochodnej w równaniu (po sprowadzeniu do postaci wielomianowej).

#### Przykłady:
- $y' + y = 0$ → **I stopień** (potęga $y'$ = 1)
- $(y')^2 + y = x$ → **II stopień** (potęga $y'$ = 2)
- $(y'')^3 + (y')^2 = 1$ → **III stopień** (potęga najwyższej pochodnej $y''$ = 3)

## 📊 Klasyfikacja według rzędu

### Równania I rzędu
$$F(x, y, y') = 0$$

**Postać standardowa:** $y' = f(x, y)$

**Przykłady:**
- $y' = 2x + 3$
- $y' + xy = e^x$
- $\frac{dy}{dx} = \frac{y}{x}$

### Równania II rzędu  
$$F(x, y, y', y'') = 0$$

**Postać standardowa:** $y'' = f(x, y, y')$

**Przykłady:**
- $y'' + y = 0$ (oscylator harmoniczny)
- $y'' - 4y' + 4y = 0$
- $x^2y'' + xy' + y = 0$

### Równania wyższych rzędów
$$F(x, y, y', y'', \ldots, y^{(n)}) = 0$$

**Przykład III rzędu:**
$$y''' + 6y'' + 11y' + 6y = 0$$

## 🔍 Określanie stopnia

### Krok 1: Sprawdź czy równanie jest wielomianowe
Czy równanie można zapisać jako wielomian względem pochodnych?

### Krok 2: Znajdź najwyższą pochodną
Zidentyfikuj najwyższą pochodną występującą w równaniu.

### Krok 3: Określ potęgę
Sprawdź w jakiej potędze występuje najwyższa pochodna.

## 📝 Przykłady szczegółowe

### Przykład 1
$$\sqrt{1 + (y')^2} = y$$

**Analiza:**
- Podnosimy do kwadratu: $1 + (y')^2 = y^2$
- Przekształcamy: $(y')^2 = y^2 - 1$
- **Rząd:** I (najwyższa pochodna $y'$)
- **Stopień:** II (potęga $(y')^2$)

### Przykład 2
$$\left(\frac{d^2y}{dx^2}\right)^3 + \left(\frac{dy}{dx}\right)^2 = x$$

**Analiza:**
- **Rząd:** II (najwyższa pochodna $y''$)
- **Stopień:** III (potęga $(y'')^3$)

### Przykład 3
$$y' + e^{y''} = 0$$

**Analiza:**
- **Rząd:** II
- **Stopień:** nieokreślony (nie można sprowadzić do postaci wielomianowej)

## ⚠️ Uwagi ważne

1. **Stopień nie zawsze istnieje** - tylko dla równań wielomianowych względem pochodnych
2. **Równania transcendentne** mogą nie mieć określonego stopnia
3. **Transformacje** mogą zmieniać rząd i stopień równania

## 📊 Tabela przykładów

| Równanie | Rząd | Stopień | Uwagi |
|----------|------|---------|--------|
| $y' = x$ | I | I | Podstawowe |
| $(y')^3 = x$ | I | III | Nieliniowe |
| $y'' + y = 0$ | II | I | Liniowe |
| $(y'')^2 + y' = 1$ | II | II | Nieliniowe |
| $y' + \sin(y'') = 0$ | II | - | Transcendentne |

## 🔗 Powiązane tematy

- [[Definicja równania różniczkowego]]
- [[Klasyfikacja równań różniczkowych]]
- [[Rozwiązania ogólne i szczególne]]
- [[Równania liniowe pierwszego rzędu]]
- [[Równania liniowe jednorodne o stałych współczynnikach]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Rząd równania | Order of equation |
| Stopień równania | Degree of equation |
| Najwyższa pochodna | Highest derivative |
| Postać wielomianowa | Polynomial form |
| Równanie transcendentne | Transcendental equation |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*