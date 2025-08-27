# Definicja równania różniczkowego

## 📚 Definicja podstawowa

**Równanie różniczkowe** to równanie zawierające funkcję nieznaną i jej pochodne. 

W przypadku funkcji jednej zmiennej $y = f(x)$, ogólna postać równania różniczkowego to:
$$F(x, y, y', y'', \ldots, y^{(n)}) = 0$$

gdzie:
- $x$ - zmienna niezależna
- $y$ - funkcja szukana (zmienna zależna) 
- $y', y'', \ldots, y^{(n)}$ - pochodne funkcji $y$ względem $x$

## 🔍 Przykłady

### Przykład 1 - Równanie pierwszego rzędu
$$\frac{dy}{dx} = 2x + 1$$

**Rozwiązanie:**
$$y = \int (2x + 1) dx = x^2 + x + C$$

### Przykład 2 - Równanie drugiego rzędu  
$$\frac{d^2y}{dx^2} + y = 0$$

**Rozwiązanie:**
$$y = C_1 \cos(x) + C_2 \sin(x)$$

### Przykład 3 - Równanie nieliniowe
$$\left(\frac{dy}{dx}\right)^2 + y^2 = 1$$

## 🎯 Kluczowe pojęcia

- **Funkcja szukana** - nieznana funkcja $y(x)$ którą chcemy znaleźć
- **Pochodne** - reprezentują szybkość zmian funkcji
- **Stałe całkowania** - parametry w rozwiązaniu ogólnym (np. $C, C_1, C_2$)

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Równanie różniczkowe | Differential equation |
| Funkcja szukana | Unknown function |
| Pochodna | Derivative |
| Zmienna niezależna | Independent variable |
| Zmienna zależna | Dependent variable |

## 🔗 Powiązane tematy

- [[Klasyfikacja równań różniczkowych]]
- [[Rząd i stopień równania różniczkowego]]  
- [[Rozwiązania ogólne i szczególne]]
- [[Warunki początkowe i brzegowe]]

## 💡 Zastosowania praktyczne

Równania różniczkowe opisują wiele zjawisk naturalnych:
- 🌡️ **Fizyka** - przewodnictwo ciepła, drgania, ruch planet
- 🧬 **Biologia** - wzrost populacji, modele epidemii
- 💰 **Ekonomia** - modele wzrostu gospodarczego
- ⚡ **Inżynieria** - obwody elektryczne, sterowanie

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*