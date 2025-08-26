# Równania liniowe jednorodne o stałych współczynnikach

## 🎯 Definicja i postać ogólna

**Równanie liniowe jednorodne o stałych współczynnikach** ma postać:
$$a_ny^{(n)} + a_{n-1}y^{(n-1)} + \cdots + a_1y' + a_0y = 0$$

gdzie $a_0, a_1, \ldots, a_n$ to **stałe rzeczywiste**, $a_n \neq 0$.

### Przypadek drugiego rzędu (najczęstszy):
$$ay'' + by' + cy = 0$$

gdzie $a, b, c$ to stałe, $a \neq 0$.

## 🔧 Równanie charakterystyczne

**Kluczowa idea:** Szukamy rozwiązań postaci $y = e^{rx}$.

Po podstawieniu $y = e^{rx}$ do równania $ay'' + by' + cy = 0$:
- $y' = re^{rx}$
- $y'' = r^2e^{rx}$

Otrzymujemy: $ar^2e^{rx} + bre^{rx} + ce^{rx} = 0$

Po wyciągnięciu $e^{rx} \neq 0$: 
$$ar^2 + br + c = 0$$

To jest **równanie charakterystyczne**.

## 📊 Przypadki rozwiązań (dla równań II rzędu)

### Przypadek 1: Dwa różne pierwiastki rzeczywiste
**Gdy:** $\Delta = b^2 - 4ac > 0$

**Pierwiastki:** $r_1, r_2$ różne

**Rozwiązanie ogólne:**
$$y = C_1e^{r_1x} + C_2e^{r_2x}$$

#### Przykład:
$y'' - 5y' + 6y = 0$

Równanie charakterystyczne: $r^2 - 5r + 6 = 0$
$(r-2)(r-3) = 0$ → $r_1 = 2, r_2 = 3$

**Rozwiązanie:** $y = C_1e^{2x} + C_2e^{3x}$

### Przypadek 2: Jeden pierwiastek rzeczywisty (podwójny)
**Gdy:** $\Delta = b^2 - 4ac = 0$

**Pierwiastek:** $r = -\frac{b}{2a}$ (podwójny)

**Rozwiązanie ogólne:**
$$y = (C_1 + C_2x)e^{rx}$$

#### Przykład:
$y'' - 4y' + 4y = 0$

Równanie charakterystyczne: $r^2 - 4r + 4 = 0$
$(r-2)^2 = 0$ → $r = 2$ (podwójny)

**Rozwiązanie:** $y = (C_1 + C_2x)e^{2x}$

### Przypadek 3: Pierwiastki zespolone
**Gdy:** $\Delta = b^2 - 4ac < 0$

**Pierwiastki:** $r = \alpha \pm i\beta$, gdzie:
- $\alpha = -\frac{b}{2a}$
- $\beta = \frac{\sqrt{4ac-b^2}}{2a}$

**Rozwiązanie ogólne:**
$$y = e^{\alpha x}(C_1\cos(\beta x) + C_2\sin(\beta x))$$

#### Przykład:
$y'' + 4y = 0$

Równanie charakterystyczne: $r^2 + 4 = 0$
$r^2 = -4$ → $r = \pm 2i$

$\alpha = 0, \beta = 2$

**Rozwiązanie:** $y = C_1\cos(2x) + C_2\sin(2x)$

## 📝 Przykłady szczegółowe

### Przykład 1: Z warunkami początkowymi
**Równanie:** $y'' + y' - 2y = 0$, $y(0) = 1$, $y'(0) = 0$

#### Rozwiązanie:
1. **Równanie charakterystyczne:** $r^2 + r - 2 = 0$
2. **Faktoryzacja:** $(r+2)(r-1) = 0$
3. **Pierwiastki:** $r_1 = -2, r_2 = 1$
4. **Rozwiązanie ogólne:** $y = C_1e^{-2x} + C_2e^x$
5. **Pochodna:** $y' = -2C_1e^{-2x} + C_2e^x$
6. **Warunki początkowe:**
   - $y(0) = C_1 + C_2 = 1$
   - $y'(0) = -2C_1 + C_2 = 0$
7. **Rozwiązanie układu:** $C_1 = \frac{1}{3}, C_2 = \frac{2}{3}$
8. **Rozwiązanie szczególne:** $y = \frac{1}{3}e^{-2x} + \frac{2}{3}e^x$

### Przykład 2: Pierwiastki zespolone
**Równanie:** $y'' + 2y' + 5y = 0$

#### Rozwiązanie:
1. **Równanie charakterystyczne:** $r^2 + 2r + 5 = 0$
2. **Wyznacznik:** $\Delta = 4 - 20 = -16 < 0$
3. **Pierwiastki:** $r = \frac{-2 \pm \sqrt{-16}}{2} = \frac{-2 \pm 4i}{2} = -1 \pm 2i$
4. **Identyfikacja:** $\alpha = -1, \beta = 2$
5. **Rozwiązanie:** $y = e^{-x}(C_1\cos(2x) + C_2\sin(2x))$

## 🌟 Rozszerzenie na równania wyższych rzędów

### Równanie III rzędu:
$ay''' + by'' + cy' + dy = 0$

**Równanie charakterystyczne:** $ar^3 + br^2 + cr + d = 0$

**Przypadki pierwiastków:**
- **Trzy różne rzeczywiste:** $y = C_1e^{r_1x} + C_2e^{r_2x} + C_3e^{r_3x}$
- **Jeden podwójny:** $y = (C_1 + C_2x)e^{r_1x} + C_3e^{r_2x}$
- **Jeden potrójny:** $y = (C_1 + C_2x + C_3x^2)e^{rx}$
- **Zespolone:** Kombinacja wykładniczych i trygonometrycznych

## 📊 Tabela przypadków dla równań II rzędu

| Dyskryminanta | Pierwiastki | Rozwiązanie |
|---------------|-------------|-------------|
| $\Delta > 0$ | $r_1 \neq r_2$ (rzeczywiste) | $C_1e^{r_1x} + C_2e^{r_2x}$ |
| $\Delta = 0$ | $r$ (podwójny rzeczywisty) | $(C_1 + C_2x)e^{rx}$ |
| $\Delta < 0$ | $\alpha \pm i\beta$ | $e^{\alpha x}(C_1\cos(\beta x) + C_2\sin(\beta x))$ |

## 🎯 Interpretacja fizyczna

### Drgania harmoniczne
Równanie $y'' + \omega^2y = 0$ opisuje drgania bez tłumienia:
- **Rozwiązanie:** $y = C_1\cos(\omega t) + C_2\sin(\omega t)$
- **Interpretacja:** Ruch harmoniczny prosty

### Drgania z tłumieniem
Równanie $y'' + 2\gamma y' + \omega_0^2y = 0$:
- **Słabe tłumienie** ($\gamma < \omega_0$): drgania tłumione
- **Tłumienie krytyczne** ($\gamma = \omega_0$): powrót bez oscylacji
- **Silne tłumienie** ($\gamma > \omega_0$): powrót aperiodyczny

## 🔗 Powiązane tematy

- [[Równania liniowe niejednorodne - metoda współczynników nieoznaczonych]]
- [[Równania liniowe niejednorodne - metoda uzmienniania stałych]]
- [[Oscylator harmoniczny]]
- [[Równania z tłumieniem]]
- [[Układy liniowe jednorodne]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Równanie charakterystyczne | Characteristic equation |
| Pierwiastek podwójny | Double root |
| Pierwiastki zespolone | Complex roots |
| Drgania harmoniczne | Harmonic oscillations |
| Tłumienie krytyczne | Critical damping |
| Stałe współczynniki | Constant coefficients |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*