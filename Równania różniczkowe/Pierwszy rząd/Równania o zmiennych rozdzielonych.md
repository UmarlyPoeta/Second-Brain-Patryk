# Równania o zmiennych rozdzielonych

## 🎯 Definicja i postać

**Równanie o zmiennych rozdzielonych** to równanie, które można zapisać w postaci:
$$\frac{dy}{dx} = f(x) \cdot g(y)$$

gdzie $f(x)$ zależy tylko od $x$, a $g(y)$ zależy tylko od $y$.

### Alternatywne postacie:
- $M(x)dx + N(y)dy = 0$
- $\frac{dy}{dx} = \frac{f(x)}{h(y)}$

## 🔧 Metoda rozwiązywania

### Krok 1: Rozdziel zmienne
$$\frac{dy}{g(y)} = f(x)dx$$

### Krok 2: Scałkuj obie strony
$$\int \frac{dy}{g(y)} = \int f(x)dx + C$$

### Krok 3: Rozwiąż względem $y$ (jeśli możliwe)

## 📝 Przykłady rozwiązane

### Przykład 1: Podstawowy
**Równanie:** $\frac{dy}{dx} = xy$

#### Rozwiązanie:
1. **Rozdzielenie:** $\frac{dy}{y} = x dx$
2. **Całkowanie:** $\ln|y| = \frac{x^2}{2} + C_1$
3. **Rozwiązanie:** $y = \pm e^{C_1} \cdot e^{x^2/2} = Ce^{x^2/2}$

gdzie $C = \pm e^{C_1}$ to dowolna stała różna od zera.

⚠️ **Uwaga:** Rozwiązanie $y = 0$ jest również rozwiązaniem!

### Przykład 2: Z funkcjami trygonometrycznymi
**Równanie:** $\frac{dy}{dx} = y \tan(x)$

#### Rozwiązanie:
1. **Rozdzielenie:** $\frac{dy}{y} = \tan(x) dx$
2. **Całkowanie:** $\ln|y| = \int \tan(x) dx = -\ln|\cos(x)| + C_1$
3. **Przekształcenie:** $\ln|y| = \ln|\sec(x)| + C_1$
4. **Rozwiązanie:** $y = \frac{C}{\cos(x)}$

### Przykład 3: Z warunkiem początkowym
**Równanie:** $(1 + x^2)dy = xy dx$, $y(0) = 2$

#### Rozwiązanie:
1. **Przepisanie:** $\frac{dy}{dx} = \frac{xy}{1 + x^2}$
2. **Rozdzielenie:** $\frac{dy}{y} = \frac{x dx}{1 + x^2}$
3. **Całkowanie:** $\ln|y| = \frac{1}{2}\ln(1 + x^2) + C_1$
4. **Rozwiązanie ogólne:** $y = C\sqrt{1 + x^2}$
5. **Warunek początkowy:** $y(0) = C\sqrt{1} = C = 2$
6. **Rozwiązanie szczególne:** $y = 2\sqrt{1 + x^2}$

## 🔍 Przypadki szczególne

### 1. Gdy $g(y) = 0$ w niektórych punktach
**Przykład:** $\frac{dy}{dx} = y^2$

- Rozwiązanie ogólne: $y = -\frac{1}{x + C}$
- **Rozwiązanie osobliwe:** $y = 0$

### 2. Równania w postaci różniczkowej
**Postać:** $M(x)dx + N(y)dy = 0$

**Przykład:** $x dx + y dy = 0$
- Całkowanie: $\frac{x^2}{2} + \frac{y^2}{2} = C$
- Rozwiązanie: $x^2 + y^2 = C$ (rodzina okręgów)

## 📊 Algorytm rozpoznawania

## 🌟 Zastosowania praktyczne

### 1. Wzrost populacji
$$\frac{dN}{dt} = kN$$
**Rozwiązanie:** $N(t) = N_0 e^{kt}$ (wzrost wykładniczy)

### 2. Rozpad radioaktywny
$$\frac{dm}{dt} = -\lambda m$$
**Rozwiązanie:** $m(t) = m_0 e^{-\lambda t}$

### 3. Prawo chłodzenia Newtona
$$\frac{dT}{dt} = -k(T - T_{\text{otoczenia}})$$

### 4. Opadanie z oporem powietrza
$$m\frac{dv}{dt} = mg - bv$$

## ⚠️ Ważne uwagi

1. **Rozwiązania osobliwe** - sprawdź punkty gdzie $g(y) = 0$
2. **Dziedzina rozwiązania** - uwaga na singularności
3. **Stała całkowania** może być zespolona
4. **Warunki początkowe** mogą nie mieć rozwiązania

## 🔢 Sprawdzenie rozwiązania

Zawsze sprawdź przez różniczkowanie:
$$\frac{d}{dx}[rozwiązanie] = \text{prawa strona równania}$$

## 🔗 Powiązane tematy

- [[Równania jednorodne pierwszego rzędu]]
- [[Równania liniowe pierwszego rzędu]]
- [[Równania dokładne]]
- [[Modele wzrostu populacji]]
- [[Rozpad radioaktywny]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Zmienne rozdzielone | Separable variables |
| Rozdzielenie zmiennych | Separation of variables |
| Całkowanie | Integration |
| Rozwiązanie osobliwe | Singular solution |
| Warunek początkowy | Initial condition |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*