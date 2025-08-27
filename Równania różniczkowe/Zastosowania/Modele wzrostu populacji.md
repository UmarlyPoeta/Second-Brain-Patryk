# Modele wzrostu populacji

## 🎯 Wprowadzenie

**Modele wzrostu populacji** używają równań różniczkowych do opisania zmian liczebności populacji w czasie. Są fundamentalne w:
- **Biologii** - dynamika populacji zwierząt i roślin
- **Demografii** - wzrost populacji ludzkiej
- **Epidemiologii** - rozprzestrzenianie się chorób
- **Ekonomii** - wzrost gospodarczy

## 📈 Model Malthusa (wzrost wykładniczy)

### Założenia:
- Nieograniczone zasoby
- Stała stopa wzrostu
- Brak konkurencji wewnątrzgatunkowej

### Równanie różniczkowe:
$$\frac{dN}{dt} = rN$$

gdzie:
- $N(t)$ - liczebność populacji w czasie $t$
- $r$ - stopa wzrostu (współczynnik Malthusa)

### Rozwiązanie:
$$N(t) = N_0 e^{rt}$$

gdzie $N_0 = N(0)$ - liczebność początkowa.

#### Interpretacja parametru $r$:
- $r > 0$ - populacja rośnie
- $r = 0$ - populacja stała  
- $r < 0$ - populacja maleje (wymieranie)

### Przykład liczbowy:
**Problem:** Populacja bakterii podwaja się co 20 minut. Ile bakterii będzie po 2 godzinach, jeśli początkowo było 1000?

#### Rozwiązanie:
1. **Warunek podwojenia:** $N(20) = 2N_0$
2. **Z wzoru:** $2N_0 = N_0 e^{20r}$ → $e^{20r} = 2$
3. **Stopa wzrostu:** $r = \frac{\ln(2)}{20} \approx 0.0347$ min⁻¹
4. **Po 120 minutach:** $N(120) = 1000 \cdot e^{120 \cdot 0.0347} = 1000 \cdot e^{4.164} = 1000 \cdot 64 = 64000$ bakterii

## 🔄 Model logistyczny (Verhulst)

### Założenia:
- Ograniczona pojemność środowiska
- Konkurencja wewnątrzgatunkowa
- Spadek tempa wzrostu przy dużych populacjach

### Równanie różniczkowe:
$$\frac{dN}{dt} = rN\left(1 - \frac{N}{K}\right)$$

gdzie:
- $K$ - **pojemność środowiska** (carrying capacity)
- $r$ - **wewnętrzna stopa wzrostu**

### Rozwiązanie:
$$N(t) = \frac{K}{1 + \left(\frac{K-N_0}{N_0}\right)e^{-rt}}$$

### Właściwości krzywej logistycznej:
- **Punkt przegięcia:** przy $N = \frac{K}{2}$
- **Asymptota pozioma:** $\lim_{t \to \infty} N(t) = K$
- **Kształt sigmoid** (krzywa S)

### Przykład:
**Problem:** Populacja ryb w jeziorze. $K = 10000$, $r = 0.1$ dzień⁻¹, $N_0 = 100$.

#### Analiza:
1. **Początek:** wzrost prawie wykładniczy (mała populacja)
2. **Środek:** najszybszy wzrost przy $N = 5000$
3. **Koniec:** wzrost zwalnia, dąży do $K = 10000$

## 🦌 Model drapieżnik-ofiara (Lotka-Volterra)

### Układ równań:
$$\begin{cases}
\frac{dx}{dt} = ax - bxy \\
\frac{dy}{dt} = -cy + dxy
\end{cases}$$

gdzie:
- $x(t)$ - liczebność ofiar
- $y(t)$ - liczebność drapieżników
- $a, b, c, d > 0$ - parametry modelu

### Interpretacja parametrów:
- $a$ - stopa wzrostu ofiar (bez drapieżników)
- $b$ - skuteczność polowania drapieżników
- $c$ - stopa śmiertelności drapieżników (bez ofiar)
- $d$ - efektywność konwersji ofiar w potomstwo drapieżników

### Punkty równowagi:
1. **Wymarcie:** $(0, 0)$ - niestabilne
2. **Koegzystencja:** $\left(\frac{c}{d}, \frac{a}{b}\right)$ - centrum (orbity zamknięte)

### Właściwości:
- **Oscylacje okresowe** populacji
- **Przesunięcie fazowe** - maksima drapieżników opóźnione względem ofiar
- **Zachowanie się energii** - trajektorie zamknięte w przestrzeni fazowej

## 🦠 Model epidemiologiczny SIR

### Podział populacji:
- **S(t)** - Susceptible (podatni)
- **I(t)** - Infected (zarażeni)  
- **R(t)** - Recovered (ozdrowiali/odporni)

### Układ równań:
$$\begin{cases}
\frac{dS}{dt} = -\beta SI \\
\frac{dI}{dt} = \beta SI - \gamma I \\
\frac{dR}{dt} = \gamma I
\end{cases}$$

### Parametry:
- $\beta$ - stopa infekcji (transmisji)
- $\gamma$ - stopa wyzdrowienia
- $R_0 = \frac{\beta S_0}{\gamma}$ - **podstawowa liczba reprodukcji**

### Warunki epidemii:
- $R_0 > 1$ - epidemia się rozprzestrzenia
- $R_0 < 1$ - epidemia wygasa
- $R_0 = 1$ - punkt progowy

## 📊 Porównanie modeli

| Model | Równanie | Rozwiązanie | Zastosowanie |
|-------|----------|-------------|--------------|
| **Malthus** | $\frac{dN}{dt} = rN$ | $N_0 e^{rt}$ | Wzrost nieograniczony |
| **Logistyczny** | $\frac{dN}{dt} = rN(1-\frac{N}{K})$ | Krzywa sigmoid | Ograniczone środowisko |
| **Lotka-Volterra** | System 2×2 | Orbity zamknięte | Interakcje międzygatunkowe |
| **SIR** | System 3×3 | Numeryczne | Epidemiologia |

## 🧮 Metody analizy

### 1. Analityczne:
- Rozdzielenie zmiennych
- Podstawienia
- Analiza stabilności

### 2. Geometryczne:
- Pola kierunkowe
- Przestrzeń fazowa
- Punkty równowagi

### 3. Numeryczne:
- Metoda Eulera
- Runge-Kutta
- Symulacje komputerowe

## 🌍 Dane rzeczywiste

### Populacja światowa (1800-2000):
Dobrze opisana modelem logistycznym z:
- $K \approx 10-12$ miliardów
- $r \approx 0.02$ rok⁻¹
- Punkt przegięcia ok. 1970 roku

### Bakterie w hodowli:
Model Malthusa dla pierwszych faz, logistyczny po wyczerpaniu składników odżywczych.

## ⚠️ Ograniczenia modeli

### Model Malthusa:
- Ignoruje ograniczone zasoby
- Przewiduje nierealistyczny wzrost nieskończony

### Model logistyczny:
- Stałe parametry $r$ i $K$
- Brak fluktuacji środowiskowych
- Jedna populacja izolowana

### Lotka-Volterra:
- Brak konkurencji wewnątrzgatunkowej
- Oscylacje bez tłumienia (nierealistyczne)
- Tylko dwa gatunki

## 🔗 Powiązane tematy

- [[Równania o zmiennych rozdzielonych]]
- [[Układy liniowe jednorodne]]
- [[Stabilność rozwiązań układów]]
- [[Metody numeryczne]]
- [[Modele epidemiologiczne]]
- [[Dynamika predator-ofiara]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Model wzrostu | Growth model |
| Pojemność środowiska | Carrying capacity |
| Punkt przegięcia | Inflection point |
| Krzywa sigmoid | Sigmoid curve |
| Drapieżnik-ofiara | Predator-prey |
| Podstawowa liczba reprodukcji | Basic reproduction number |
| Przestrzeń fazowa | Phase space |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*