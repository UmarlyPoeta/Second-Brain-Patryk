# Układy liniowe jednorodne

## 🎯 Definicja i postać macierzowa

**Układ liniowy jednorodny** pierwszego rzędu ma postać:
$$\frac{d\vec{y}}{dt} = A\vec{y}$$

gdzie:
- $\vec{y}(t) = \begin{pmatrix} y_1(t) \\ y_2(t) \\ \vdots \\ y_n(t) \end{pmatrix}$ - wektor funkcji szukanych
- $A = \begin{pmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{n1} & a_{n2} & \cdots & a_{nn} \end{pmatrix}$ - macierz stałych współczynników

## 📝 Postać rozwinięta (przykład 2×2)

$$\begin{cases}
\frac{dy_1}{dt} = a_{11}y_1 + a_{12}y_2 \\
\frac{dy_2}{dt} = a_{21}y_1 + a_{22}y_2
\end{cases}$$

**Warunki początkowe:** $\vec{y}(t_0) = \vec{y_0} = \begin{pmatrix} y_{10} \\ y_{20} \end{pmatrix}$

## 🔧 Metoda wartości własnych i wektorów własnych

### Krok 1: Znajdź wartości własne
Rozwiąż równanie charakterystyczne:
$$\det(A - \lambda I) = 0$$

### Krok 2: Znajdź wektory własne
Dla każdej wartości własnej $\lambda_i$ rozwiąż:
$$(A - \lambda_i I)\vec{v_i} = \vec{0}$$

### Przypadki rozwiązań:

## 📊 Przypadek 1: Wartości własne rzeczywiste różne

**Jeśli:** $\lambda_1 \neq \lambda_2$ (oba rzeczywiste)

**Rozwiązanie ogólne:**
$$\vec{y}(t) = C_1 e^{\lambda_1 t}\vec{v_1} + C_2 e^{\lambda_2 t}\vec{v_2}$$

### Przykład:
$$A = \begin{pmatrix} 1 & 2 \\ 3 & 2 \end{pmatrix}$$

#### Rozwiązanie:
1. **Równanie charakterystyczne:**
   $$\det\begin{pmatrix} 1-\lambda & 2 \\ 3 & 2-\lambda \end{pmatrix} = (1-\lambda)(2-\lambda) - 6 = \lambda^2 - 3\lambda - 4 = 0$$

2. **Wartości własne:** $\lambda_1 = 4, \lambda_2 = -1$

3. **Wektory własne:**
   - Dla $\lambda_1 = 4$: $(A - 4I)\vec{v_1} = \vec{0}$ → $\vec{v_1} = \begin{pmatrix} 2 \\ 3 \end{pmatrix}$
   - Dla $\lambda_2 = -1$: $(A + I)\vec{v_2} = \vec{0}$ → $\vec{v_2} = \begin{pmatrix} 1 \\ -1 \end{pmatrix}$

4. **Rozwiązanie:**
   $$\vec{y}(t) = C_1 e^{4t}\begin{pmatrix} 2 \\ 3 \end{pmatrix} + C_2 e^{-t}\begin{pmatrix} 1 \\ -1 \end{pmatrix}$$

## 🔄 Przypadek 2: Wartości własne zespolone

**Jeśli:** $\lambda = \alpha \pm i\beta$ (para zespolona)

**Rozwiązanie ogólne:**
$$\vec{y}(t) = e^{\alpha t}[C_1(\vec{u}\cos(\beta t) - \vec{v}\sin(\beta t)) + C_2(\vec{v}\cos(\beta t) + \vec{u}\sin(\beta t))]$$

gdzie wektor własny zespolony $\vec{w} = \vec{u} + i\vec{v}$.

### Przykład:
$$A = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$$

#### Rozwiązanie:
1. **Równanie charakterystyczne:** $\lambda^2 + 1 = 0$ → $\lambda = \pm i$

2. **Wartości własne:** $\alpha = 0, \beta = 1$

3. **Wektor własny dla $\lambda = i$:**
   $$(A - iI)\vec{w} = \vec{0} \Rightarrow \vec{w} = \begin{pmatrix} 1 \\ -i \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \end{pmatrix} + i\begin{pmatrix} 0 \\ -1 \end{pmatrix}$$
   
   Więc $\vec{u} = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \vec{v} = \begin{pmatrix} 0 \\ -1 \end{pmatrix}$

4. **Rozwiązanie:**
   $$\vec{y}(t) = C_1\begin{pmatrix} \cos(t) \\ \sin(t) \end{pmatrix} + C_2\begin{pmatrix} \sin(t) \\ -\cos(t) \end{pmatrix}$$

## ⚡ Przypadek 3: Wartość własna podwójna

**Jeśli:** $\lambda$ jest wartością własną podwójną

### Przypadek 3a: Dwa liniowo niezależne wektory własne
**Rozwiązanie:** Jak w przypadku 1, ale $\lambda_1 = \lambda_2 = \lambda$

### Przypadek 3b: Jeden wektor własny (blok Jordana)
**Rozwiązanie:** 
$$\vec{y}(t) = C_1 e^{\lambda t}\vec{v} + C_2 e^{\lambda t}(t\vec{v} + \vec{w})$$

gdzie $\vec{w}$ to **wektor własny uogólniony**: $(A - \lambda I)\vec{w} = \vec{v}$

## 🌟 Rozwiązanie macierzowe - eksponencjał macierzy

**Rozwiązanie ogólne:**
$$\vec{y}(t) = e^{At}\vec{C}$$

gdzie $e^{At}$ to **eksponencjał macierzy**:
$$e^{At} = I + At + \frac{(At)^2}{2!} + \frac{(At)^3}{3!} + \cdots$$

### Obliczanie przez diagonalizację:
Jeśli $A = PDP^{-1}$, to:
$$e^{At} = Pe^{Dt}P^{-1}$$

gdzie $e^{Dt} = \begin{pmatrix} e^{\lambda_1 t} & 0 & \cdots \\ 0 & e^{\lambda_2 t} & \cdots \\ \vdots & \vdots & \ddots \end{pmatrix}$

## 📈 Analiza stabilności

### Punkty równowagi:
**Punkt równowagi** układu $\frac{d\vec{y}}{dt} = A\vec{y}$ to $\vec{y} = \vec{0}$.

### Klasyfikacja stabilności (dla układów 2×2):

| Wartości własne | Typ punktu | Stabilność |
|----------------|------------|------------|
| $\lambda_1, \lambda_2 < 0$ | Węzeł stabilny | Asymptotycznie stabilny |
| $\lambda_1, \lambda_2 > 0$ | Węzeł niestabilny | Niestabilny |
| $\lambda_1 < 0 < \lambda_2$ | Punkt siodłowy | Niestabilny |
| $\lambda = \alpha \pm i\beta, \alpha < 0$ | Ognisko stabilne | Asymptotycznie stabilny |
| $\lambda = \alpha \pm i\beta, \alpha > 0$ | Ognisko niestabilne | Niestabilny |
| $\lambda = \pm i\beta$ | Środek | Stabilny (Ljapunow) |

## 🎯 Portret fazowy

**Portret fazowy** to zbiór trajektorii w przestrzeni $(y_1, y_2)$ dla różnych warunków początkowych.

### Charakterystyczne kształty:
- **Węzeł:** trajektorie dążą/oddalają się radijalnie
- **Ognisko:** trajektorie spiralne
- **Punkt siodłowy:** hiperbole
- **Środek:** elipsy zamknięte

## 📝 Przykład z warunkami początkowymi

### Problem:
$$\frac{d\vec{y}}{dt} = \begin{pmatrix} -2 & 1 \\ 1 & -2 \end{pmatrix}\vec{y}, \quad \vec{y}(0) = \begin{pmatrix} 1 \\ 2 \end{pmatrix}$$

#### Rozwiązanie:
1. **Wartości własne:** $\lambda_1 = -1, \lambda_2 = -3$
2. **Wektory własne:** $\vec{v_1} = \begin{pmatrix} 1 \\ 1 \end{pmatrix}, \vec{v_2} = \begin{pmatrix} 1 \\ -1 \end{pmatrix}$
3. **Rozwiązanie ogólne:** $\vec{y}(t) = C_1 e^{-t}\begin{pmatrix} 1 \\ 1 \end{pmatrix} + C_2 e^{-3t}\begin{pmatrix} 1 \\ -1 \end{pmatrix}$
4. **Warunki początkowe:** $C_1 + C_2 = 1, C_1 - C_2 = 2$ → $C_1 = \frac{3}{2}, C_2 = -\frac{1}{2}$
5. **Rozwiązanie szczególne:** $\vec{y}(t) = \frac{3}{2}e^{-t}\begin{pmatrix} 1 \\ 1 \end{pmatrix} - \frac{1}{2}e^{-3t}\begin{pmatrix} 1 \\ -1 \end{pmatrix}$

## 🔗 Powiązane tematy

- [[Wartości własne i wektory własne w układach]]
- [[Stabilność rozwiązań układów]]
- [[Macierz fundamentalna rozwiązań]]
- [[Równania liniowe jednorodne o stałych współczynnikach]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Układ liniowy | Linear system |
| Wartości własne | Eigenvalues |
| Wektory własne | Eigenvectors |
| Eksponencjał macierzy | Matrix exponential |
| Portret fazowy | Phase portrait |
| Punkt siodłowy | Saddle point |
| Węzeł stabilny | Stable node |
| Ognisko | Focus/Spiral |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*