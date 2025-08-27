# Metoda Eulera

## 🎯 Wprowadzenie

**Metoda Eulera** to najprostsza metoda numeryczna rozwiązywania równań różniczkowych pierwszego rzędu. Opracowana przez Leonharda Eulera (1707-1783), stanowi podstawę dla bardziej zaawansowanych metod numerycznych.

## 📝 Problem początkowy

**Zagadnienie Cauchy'ego:**
$$\frac{dy}{dx} = f(x, y), \quad y(x_0) = y_0$$

**Cel:** Znaleźć przybliżone wartości $y(x)$ w punktach $x_1, x_2, \ldots, x_n$.

## 🔧 Wyprowadzenie metody

### Idea geometryczna:
1. W punkcie $(x_0, y_0)$ rysujemy styczną o nachyleniu $f(x_0, y_0)$
2. Przechodzimy wzdłuż stycznej o krok $h$
3. W nowym punkcie powtarzamy procedurę

### Matematyczne wyprowadzenie:
**Wzór Taylora:** 
$$y(x + h) = y(x) + hy'(x) + \frac{h^2}{2}y''(x) + \cdots$$

**Przybliżenie liniowe (pomijamy składniki wyższych rzędów):**
$$y(x + h) \approx y(x) + hy'(x) = y(x) + hf(x, y(x))$$

### Algorytm Eulera:
$$\begin{cases}
x_{n+1} = x_n + h \\
y_{n+1} = y_n + h \cdot f(x_n, y_n)
\end{cases}$$

gdzie:
- $h = \frac{x_{końcowy} - x_0}{N}$ - **krok całkowania**
- $N$ - liczba kroków

## 📝 Przykład krok po kroku

### Problem:
$$\frac{dy}{dx} = x + y, \quad y(0) = 1$$

**Znajdź $y(1)$ używając $h = 0.2$.**

### Rozwiązanie:
**Punkty:** $x_0 = 0, x_1 = 0.2, x_2 = 0.4, x_3 = 0.6, x_4 = 0.8, x_5 = 1.0$

**Krok 0:** $x_0 = 0, y_0 = 1$

**Krok 1:** 
- $f(x_0, y_0) = f(0, 1) = 0 + 1 = 1$
- $y_1 = y_0 + h \cdot f(x_0, y_0) = 1 + 0.2 \cdot 1 = 1.2$

**Krok 2:**
- $f(x_1, y_1) = f(0.2, 1.2) = 0.2 + 1.2 = 1.4$ 
- $y_2 = 1.2 + 0.2 \cdot 1.4 = 1.48$

**Krok 3:**
- $f(x_2, y_2) = f(0.4, 1.48) = 0.4 + 1.48 = 1.88$
- $y_3 = 1.48 + 0.2 \cdot 1.88 = 1.856$

**Krok 4:**
- $f(x_3, y_3) = f(0.6, 1.856) = 0.6 + 1.856 = 2.456$
- $y_4 = 1.856 + 0.2 \cdot 2.456 = 2.3472$

**Krok 5:**
- $f(x_4, y_4) = f(0.8, 2.3472) = 0.8 + 2.3472 = 3.1472$
- $y_5 = 2.3472 + 0.2 \cdot 3.1472 = 2.9766$

**Wynik:** $y(1) \approx 2.9766$

### Porównanie z rozwiązaniem dokładnym:
**Rozwiązanie analityczne:** $y = 2e^x - x - 1$
**Wartość dokładna:** $y(1) = 2e - 2 \approx 3.4366$
**Błąd:** $|3.4366 - 2.9766| = 0.46$ (13% błędu)

## 📊 Analiza błędów

### Błąd lokalny (w jednym kroku):
$$\text{Błąd lokalny} = O(h^2)$$

Wynika z pominięcia składników wyższych rzędów w rozwinięciu Taylora.

### Błąd globalny (skumulowany):
$$\text{Błąd globalny} = O(h)$$

**Wniosek:** Metoda Eulera ma **pierwszy rząd dokładności**.

### Wpływ kroku $h$:
- **Mniejszy $h$** → większa dokładność, ale więcej obliczeń
- **Większy $h$** → mniejsza dokładność, ale szybsze obliczenia

## 🔄 Modyfikacje metody Eulera

### Metoda Eulera wsteczna (implicit):
$$y_{n+1} = y_n + h \cdot f(x_{n+1}, y_{n+1})$$

**Właściwości:**
- Równanie należy rozwiązać względem $y_{n+1}$ 
- Lepsza stabilność numeryczna
- Trudniejsza do implementacji

### Metoda Eulera ulepszona (Heun):
$$\begin{cases}
k_1 = h \cdot f(x_n, y_n) \\
k_2 = h \cdot f(x_n + h, y_n + k_1) \\
y_{n+1} = y_n + \frac{1}{2}(k_1 + k_2)
\end{cases}$$

**Rząd dokładności:** $O(h^2)$

## 💻 Implementacja w pseudokodzie

```
ALGORYTM EULER(f, x0, y0, h, n)
WEJŚCIE: f - funkcja prawej strony
         x0, y0 - warunki początkowe  
         h - krok
         n - liczba kroków
         
x = x0
y = y0

DLA i = 1 DO n:
    slope = f(x, y)
    y = y + h * slope
    x = x + h
    WYPISZ x, y
KONIEC
```

## ⚠️ Ograniczenia i problemy

### 1. Stabilność numeryczna:
- Dla niektórych równań metoda może być **niestabilna**
- Problem szczególnie dotyczy **sztywnych równań** (stiff equations)

### 2. Dokładność:
- **Niska dokładność** w porównaniu z metodami wyższych rzędów
- Wymaga **bardzo małych kroków** dla dobrej dokładności

### 3. Błąd skumulowany:
- Błędy narastają z każdym krokiem
- Długie przedziały całkowania mogą dawać bardzo niedokładne wyniki

## 🌟 Zastosowania praktyczne

### 1. Pierwszy krok w analizie:
- Szybkie oszacowanie rozwiązania
- Test poprawności implementacji

### 2. Równania proste:
- Gdy dokładność nie jest kluczowa
- Demonstracje edukacyjne

### 3. Punkt odniesienia:
- Porównanie z bardziej zaawansowanymi metodami

## 📈 Porównanie z innymi metodami

| Metoda | Rząd dokładności | Złożoność obliczeniowa | Stabilność |
|--------|-----------------|------------------------|------------|
| **Euler** | $O(h)$ | Niska | Słaba |
| **Heun** | $O(h^2)$ | Średnia | Średnia |
| **Runge-Kutta 4** | $O(h^4)$ | Wysoka | Dobra |
| **Adams** | $O(h^p)$ | Średnia | Dobra |

## 🎯 Wskazówki praktyczne

1. **Wybór kroku:** Zacznij od większego, zmniejszaj aż do stabilności wyników
2. **Kontrola błędu:** Porównaj wyniki dla $h$ i $h/2$
3. **Wizualizacja:** Narysuj pole kierunkowe aby zrozumieć zachowanie rozwiązania
4. **Upgrade:** Przejdź na RK4 gdy potrzebna większa dokładność

## 🔗 Powiązane tematy

- [[Metoda Runge-Kutta]]
- [[Stabilność metod numerycznych]]  
- [[Równania o zmiennych rozdzielonych]]
- [[Warunki początkowe i brzegowe]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Metoda Eulera | Euler's method |
| Krok całkowania | Step size |
| Błąd lokalny | Local error |
| Błąd globalny | Global error |
| Stabilność numeryczna | Numerical stability |
| Równania sztywne | Stiff equations |
| Rząd dokładności | Order of accuracy |

## 🧮 Ćwiczenie

**Zadanie:** Rozwiąż $\frac{dy}{dx} = y$, $y(0) = 1$ na przedziale $[0, 1]$ z krokiem $h = 0.1$.

**Porównaj z rozwiązaniem dokładnym:** $y = e^x$

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*