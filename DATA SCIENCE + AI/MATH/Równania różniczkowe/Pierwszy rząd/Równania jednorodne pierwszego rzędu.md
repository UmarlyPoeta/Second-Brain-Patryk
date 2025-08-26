# Równania jednorodne pierwszego rzędu

## 🎯 Definicja

**Równanie jednorodne pierwszego rzędu** ma postać:
$$\frac{dy}{dx} = f\left(\frac{y}{x}\right)$$

gdzie funkcja $f$ zależy tylko od stosunku $\frac{y}{x}$.

### Alternatywne postacie:
- $M(x,y)dx + N(x,y)dy = 0$, gdzie $M$ i $N$ są funkcjami jednorodymi tego samego stopnia
- $\frac{dy}{dx} = \frac{ax + by + c}{dx + ey + f}$ gdy $c = f = 0$

## 🔧 Metoda rozwiązywania

### Podstawienie $v = \frac{y}{x}$

1. **Podstawienie:** $y = vx$, więc $\frac{dy}{dx} = v + x\frac{dv}{dx}$

2. **Przekształcenie równania:**
   $$v + x\frac{dv}{dx} = f(v)$$

3. **Rozdzielenie zmiennych:**
   $$x\frac{dv}{dx} = f(v) - v$$
   $$\frac{dv}{f(v) - v} = \frac{dx}{x}$$

4. **Całkowanie i powrót do zmiennej $y$**

## 📝 Przykłady rozwiązane

### Przykład 1: Podstawowy
**Równanie:** $\frac{dy}{dx} = \frac{x + y}{x}$

#### Rozwiązanie:
1. **Przepisanie:** $\frac{dy}{dx} = 1 + \frac{y}{x}$
2. **Podstawienie:** $v = \frac{y}{x}$, $y = vx$
3. **Przekształcenie:** $v + x\frac{dv}{dx} = 1 + v$
4. **Uproszczenie:** $x\frac{dv}{dx} = 1$
5. **Rozdzielenie:** $dv = \frac{dx}{x}$
6. **Całkowanie:** $v = \ln|x| + C$
7. **Powrót:** $\frac{y}{x} = \ln|x| + C$
8. **Rozwiązanie:** $y = x(\ln|x| + C)$

### Przykład 2: Z funkcjami trygonometrycznymi
**Równanie:** $\frac{dy}{dx} = \frac{y + x\sin(\frac{y}{x})}{x}$

#### Rozwiązanie:
1. **Przepisanie:** $\frac{dy}{dx} = \frac{y}{x} + \sin\left(\frac{y}{x}\right)$
2. **Podstawienie:** $v = \frac{y}{x}$
3. **Przekształcenie:** $v + x\frac{dv}{dx} = v + \sin(v)$
4. **Uproszczenie:** $x\frac{dv}{dx} = \sin(v)$
5. **Rozdzielenie:** $\frac{dv}{\sin(v)} = \frac{dx}{x}$
6. **Całkowanie:** $\ln|\tan(\frac{v}{2})| = \ln|x| + C_1$
7. **Rozwiązanie:** $\tan\left(\frac{y}{2x}\right) = Cx$

### Przykład 3: W postaci różniczkowej
**Równanie:** $(x^2 + y^2)dx - xy dy = 0$

#### Sprawdzenie jednorodności:
- $M(x,y) = x^2 + y^2$ (stopień 2)
- $N(x,y) = -xy$ (stopień 2)
- Funkcje są jednorodne stopnia 2 ✓

#### Rozwiązanie:
1. **Przepisanie:** $\frac{dy}{dx} = \frac{x^2 + y^2}{xy} = \frac{x}{y} + \frac{y}{x}$
2. **Podstawienie:** $v = \frac{y}{x}$, więc $\frac{x}{y} = \frac{1}{v}$
3. **Przekształcenie:** $v + x\frac{dv}{dx} = \frac{1}{v} + v$
4. **Uproszczenie:** $x\frac{dv}{dx} = \frac{1}{v}$
5. **Rozdzielenie:** $v dv = \frac{dx}{x}$
6. **Całkowanie:** $\frac{v^2}{2} = \ln|x| + C$
7. **Powrót:** $\frac{y^2}{2x^2} = \ln|x| + C$
8. **Rozwiązanie:** $y^2 = 2x^2(\ln|x| + C)$

## 🔍 Rozpoznawanie równań jednorodnych

### Test jednorodności funkcji:
Funkcja $f(x,y)$ jest jednorodna stopnia $n$, jeśli:
$$f(tx, ty) = t^n f(x,y)$$

### Przykłady:
- $x^2 + y^2$ jest jednorodna stopnia 2: $(tx)^2 + (ty)^2 = t^2(x^2 + y^2)$
- $\frac{x}{y}$ jest jednorodna stopnia 0: $\frac{tx}{ty} = \frac{x}{y}$
- $x + y + 1$ **nie jest jednorodna** (z powodu stałej 1)

## 📊 Algorytm rozwiązywania

```mermaid
graph TD
    A[Równanie dy/dx = f(x,y)] --> B{Sprawdź jednorodność}
    B -->|Jednorodne| C[Podstawienie v = y/x]
    B -->|Niejednorodne| D[Inne metody]
    C --> E[Przekształć do v + x(dv/dx) = f(v)]
    E --> F[Rozdziel zmienne]
    F --> G[Całkuj]
    G --> H[Podstaw z powrotem y = vx]
```

## 🌟 Interpretacja geometryczna

**Równania jednorodne** opisują pole kierunkowe, które ma tę samą właściwość wzdłuż każdej prostej przechodzącej przez początek układu współrzędnych.

**Krzywe całkowe** mają tę właściwość, że nachylenie stycznej w punkcie $(x,y)$ zależy tylko od stosunku $\frac{y}{x}$.

## ⚠️ Przypadki szczególne

### 1. Gdy $f(v) - v = 0$
Równanie $x\frac{dv}{dx} = 0$ daje $v = C$, czyli $y = Cx$ (proste przez początek).

### 2. Osobliwości
Sprawdź punkty gdzie $f(v) - v = 0$ - mogą dać rozwiązania osobliwe.

### 3. Problem w punkcie $x = 0$
Rozwiązania mogą mieć osobliwość w początku układu współrzędnych.

## 🔗 Powiązane tematy

- [[Równania o zmiennych rozdzielonych]]
- [[Równania liniowe pierwszego rzędu]]
- [[Czynnik całkujący]]
- [[Zastosowania geometryczne równań pierwszego rzędu]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Równanie jednorodne | Homogeneous equation |
| Funkcja jednorodna | Homogeneous function |
| Stopień jednorodności | Degree of homogeneity |
| Podstawienie | Substitution |
| Krzywa całkowa | Integral curve |
| Pole kierunkowe | Direction field |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*