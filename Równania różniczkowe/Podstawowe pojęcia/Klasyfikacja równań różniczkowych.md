# Klasyfikacja równań różniczkowych

## 📊 Kryteria klasyfikacji

Równania różniczkowe można klasyfikować według różnych kryteriów:

### 1. 🔢 Według liczby zmiennych

#### Równania zwyczajne (ODE - Ordinary Differential Equations)
- Funkcja zależy od **jednej zmiennej**
- Zawierają zwyczajne pochodne
- Przykład: $\frac{dy}{dx} = y + x$

#### Równania cząstkowe (PDE - Partial Differential Equations)  
- Funkcja zależy od **wielu zmiennych**
- Zawierają pochodne cząstkowe
- Przykład: $\frac{\partial u}{\partial t} = k\frac{\partial^2 u}{\partial x^2}$ (równanie przewodnictwa ciepła)

### 2. 📐 Według rzędu

**Rząd** = najwyższa pochodna występująca w równaniu

- **I rzędu**: $y' = f(x,y)$
- **II rzędu**: $y'' + py' + qy = 0$  
- **III rzędu**: $y''' + 2y'' - y' + y = x$

### 3. ⚖️ Według liniowości

#### Równania liniowe
Funkcja i jej pochodne występują w pierwszej potędze:
$$a_n(x)y^{(n)} + a_{n-1}(x)y^{(n-1)} + \ldots + a_1(x)y' + a_0(x)y = g(x)$$

**Właściwości:**
- ✅ Zasada superpozycji
- ✅ Metody systematyczne rozwiązywania

**Przykłady:**
- $y' + 2y = e^x$ (liniowe)
- $y'' + y = \sin(x)$ (liniowe)

#### Równania nieliniowe
Zawierają funkcję lub pochodne w potędze wyższej niż pierwsza:

**Przykłady:**
- $y' = y^2$ (nieliniowe - $y$ w drugiej potędze)
- $(y')^2 + y = x$ (nieliniowe - $(y')$ w drugiej potędze)
- $y'' + \sin(y) = 0$ (nieliniowe - funkcja nieliniowa od $y$)

### 4. 🎯 Według jednorodności

#### Równania jednorodne
$$a_n(x)y^{(n)} + a_{n-1}(x)y^{(n-1)} + \ldots + a_1(x)y' + a_0(x)y = 0$$

Prawa strona równa zero.

#### Równania niejednorodne  
$$a_n(x)y^{(n)} + a_{n-1}(x)y^{(n-1)} + \ldots + a_1(x)y' + a_0(x)y = g(x)$$

Prawa strona różna od zera (funkcja wymuszająca).

## 📋 Tabela klasyfikacji

| Typ | Cecha | Przykład |
|-----|-------|----------|
| **Zwyczajne** | Jedna zmienna | $y' = 2xy$ |
| **Cząstkowe** | Wiele zmiennych | $\frac{\partial u}{\partial t} = \frac{\partial^2 u}{\partial x^2}$ |
| **Liniowe** | Pierwsza potęga | $y'' + 3y' + 2y = x$ |
| **Nieliniowe** | Wyższe potęgi | $y' = y^2$ |
| **Jednorodne** | Prawa strona = 0 | $y'' + y = 0$ |
| **Niejednorodne** | Prawa strona ≠ 0 | $y'' + y = \cos(x)$ |

## 🔗 Powiązane tematy

- [[Definicja równania różniczkowego]]
- [[Rząd i stopień równania różniczkowego]]
- [[Równania liniowe pierwszego rzędu]]
- [[Układy liniowe jednorodne]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Równanie zwyczajne | Ordinary differential equation (ODE) |
| Równanie cząstkowe | Partial differential equation (PDE) |
| Równanie liniowe | Linear equation |
| Równanie nieliniowe | Nonlinear equation |
| Równanie jednorodne | Homogeneous equation |
| Równanie niejednorodne | Non-homogeneous equation |
| Rząd równania | Order of equation |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*