# Metoda Runge-Kutta

## 🎯 Wprowadzenie

**Metody Runge-Kutta** to rodzina metod numerycznych do rozwiązywania równań różniczkowych pierwszego rzędu, opracowanych przez matematyków C. Runge i M.W. Kutta na początku XX wieku.

**Główna idea:** Uzyskać wyższą dokładność niż metoda Eulera przez oszacowanie nachylenia w kilku punktach pomocniczych.

## 🔧 Metoda Runge-Kutta drugiego rzędu (RK2)

### Algorytm:
$$\begin{cases}
k_1 = h \cdot f(x_n, y_n) \\
k_2 = h \cdot f(x_n + h, y_n + k_1) \\
y_{n+1} = y_n + \frac{1}{2}(k_1 + k_2)
\end{cases}$$

**Interpretacja geometryczna:**
- $k_1$ - nachylenie w punkcie początkowym
- $k_2$ - nachylenie w punkcie końcowym (oszacowanym metodą Eulera)
- Wynik - średnia z obu nachyleń

**Rząd dokładności:** $O(h^2)$

## 🌟 Metoda Runge-Kutta czwartego rzędu (RK4)

### Algorytm klasyczny:
$$\begin{cases}
k_1 = h \cdot f(x_n, y_n) \\
k_2 = h \cdot f(x_n + \frac{h}{2}, y_n + \frac{k_1}{2}) \\
k_3 = h \cdot f(x_n + \frac{h}{2}, y_n + \frac{k_2}{2}) \\
k_4 = h \cdot f(x_n + h, y_n + k_3) \\
y_{n+1} = y_n + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)
\end{cases}$$

**Interpretacja współczynników $k_i$:**
- $k_1$ - nachylenie na początku przedziału
- $k_2$ - nachylenie w środku (używając $k_1$)
- $k_3$ - nachylenie w środku (używając $k_2$) 
- $k_4$ - nachylenie na końcu (używając $k_3$)

**Wagi w średniej ważonej:**
$$\frac{k_1 + 2k_2 + 2k_3 + k_4}{6}$$

- Początek i koniec: waga 1
- Środek: waga 2 (podwójnie ważny)

## 📝 Przykład szczegółowy - RK4

### Problem:
$$\frac{dy}{dx} = x + y, \quad y(0) = 1$$

**Znajdź $y(0.2)$ używając jednego kroku RK4.**

### Rozwiązanie:
**Dane:** $x_0 = 0$, $y_0 = 1$, $h = 0.2$, $f(x,y) = x + y$

**Krok 1:** $k_1 = h \cdot f(x_0, y_0) = 0.2 \cdot f(0, 1) = 0.2 \cdot 1 = 0.2$

**Krok 2:** 
- $k_2 = h \cdot f(x_0 + \frac{h}{2}, y_0 + \frac{k_1}{2})$
- $k_2 = 0.2 \cdot f(0.1, 1.1) = 0.2 \cdot 1.2 = 0.24$

**Krok 3:**
- $k_3 = h \cdot f(x_0 + \frac{h}{2}, y_0 + \frac{k_2}{2})$
- $k_3 = 0.2 \cdot f(0.1, 1.12) = 0.2 \cdot 1.22 = 0.244$

**Krok 4:**
- $k_4 = h \cdot f(x_0 + h, y_0 + k_3)$
- $k_4 = 0.2 \cdot f(0.2, 1.244) = 0.2 \cdot 1.444 = 0.2888$

**Wynik:**
$$y_1 = y_0 + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$
$$y_1 = 1 + \frac{1}{6}(0.2 + 2 \cdot 0.24 + 2 \cdot 0.244 + 0.2888)$$
$$y_1 = 1 + \frac{1.4568}{6} = 1 + 0.2428 = 1.2428$$

**Porównanie z rozwiązaniem dokładnym:**
- Dokładne: $y(0.2) = 2e^{0.2} - 0.2 - 1 \approx 1.2428$
- RK4: $y(0.2) \approx 1.2428$
- **Błąd praktycznie zerowy!**

## 📊 Porównanie metod

### Ten sam problem z $h = 0.2$:

| Metoda | Wynik | Błąd | Rząd dokładności |
|--------|-------|------|------------------|
| **Euler** | 1.2 | 0.0428 | $O(h)$ |
| **RK2** | 1.232 | 0.0108 | $O(h^2)$ |
| **RK4** | 1.2428 | ≈0 | $O(h^4)$ |
| **Dokładny** | 1.2428 | 0 | - |

## 💻 Implementacja RK4

### Pseudokod:
```
ALGORYTM RK4(f, x0, y0, h, n)
WEJŚCIE: f - funkcja prawej strony
         x0, y0 - warunki początkowe
         h - krok
         n - liczba kroków

x = x0
y = y0

DLA i = 1 DO n:
    k1 = h * f(x, y)
    k2 = h * f(x + h/2, y + k1/2)
    k3 = h * f(x + h/2, y + k2/2)
    k4 = h * f(x + h, y + k3)
    
    y = y + (k1 + 2*k2 + 2*k3 + k4)/6
    x = x + h
    
    WYPISZ x, y
KONIEC
```

### Implementacja w Pythonie:
```python
import numpy as np
import matplotlib.pyplot as plt

def rk4_step(f, x, y, h):
    """Jeden krok RK4"""
    k1 = h * f(x, y)
    k2 = h * f(x + h/2, y + k1/2)
    k3 = h * f(x + h/2, y + k2/2)
    k4 = h * f(x + h, y + k3)
    
    return y + (k1 + 2*k2 + 2*k3 + k4)/6

def rk4_solve(f, x0, y0, x_end, h):
    """Rozwiązanie całego przedziału"""
    x_vals = [x0]
    y_vals = [y0]
    
    x, y = x0, y0
    while x < x_end:
        if x + h > x_end:
            h = x_end - x  # Ostatni krok
        
        y = rk4_step(f, x, y, h)
        x += h
        
        x_vals.append(x)
        y_vals.append(y)
    
    return np.array(x_vals), np.array(y_vals)
```

## 🌟 Metody Runge-Kutta wyższych rzędów

### Metody adaptacyjne:
- **RK45** (Dormand-Prince) - automatyczny wybór kroku
- **RK23** - metoda z kontrolą błędu
- **Fehlberg** - para metod różnych rzędów

### Kontrola błędu:
1. Oblicz rozwiązanie metodami rzędu $p$ i $p+1$
2. Porównaj wyniki - różnica to oszacowanie błędu
3. Jeśli błąd za duży - zmniejsz krok
4. Jeśli błąd za mały - zwiększ krok

## ⚖️ Zalety i wady RK4

### ✅ Zalety:
- **Wysoka dokładność** - błąd $O(h^4)$
- **Stabilność numeryczna** - dobra dla większości problemów
- **Prostota implementacji** - algorytm jednokrokowy
- **Szeroka stosowalność** - działa dla różnorodnych równań

### ❌ Wady:
- **Koszt obliczeniowy** - 4 wywołania funkcji $f$ na krok
- **Brak adaptacji kroku** - krok stały może być nieefektywny
- **Problemy z równaniami sztywnymi** - może wymagać bardzo małego kroku

## 🎯 Zastosowania praktyczne

### 1. Mechanika:
- Trajektorie ciał niebieskich
- Dynamika molekularna
- Symulacje ruchu

### 2. Inżynieria:
- Analiza obwodów elektronicznych
- Systemy sterowania
- Dynamika płynów

### 3. Biologia:
- Modele populacyjne
- Farmakokinetyka
- Modele epidemiologiczne

## 🔄 Rozszerzenia na układy równań

### Układ równań:
$$\begin{cases}
\frac{dy_1}{dx} = f_1(x, y_1, y_2) \\
\frac{dy_2}{dx} = f_2(x, y_1, y_2)
\end{cases}$$

### RK4 dla układów:
```python
def rk4_system(f, x0, y0, h):
    """RK4 dla układu równań"""
    k1 = h * f(x0, y0)
    k2 = h * f(x0 + h/2, y0 + k1/2)
    k3 = h * f(x0 + h/2, y0 + k2/2)
    k4 = h * f(x0 + h, y0 + k3)
    
    return y0 + (k1 + 2*k2 + 2*k3 + k4)/6
```

## 🔗 Powiązane tematy

- [[Metoda Eulera]]
- [[Stabilność metod numerycznych]]
- [[Układy liniowe jednorodne]]
- [[Oscylator harmoniczny]]
- [[Modele wzrostu populacji]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Metoda Runge-Kutta | Runge-Kutta method |
| Rząd dokładności | Order of accuracy |
| Krok adaptacyjny | Adaptive step size |
| Kontrola błędu | Error control |
| Równania sztywne | Stiff equations |
| Nachylenie | Slope |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*