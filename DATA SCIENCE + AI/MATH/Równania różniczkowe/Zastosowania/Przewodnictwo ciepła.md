# Przewodnictwo ciepła

## 🌡️ Wprowadzenie

**Przewodnictwo ciepła** to proces transportu energii cieplnej w substancji bez przemieszczania się materii. Jest opisywane równaniami różniczkowymi cząstkowymi i znajdzie zastosowania w:
- **Inżynierii** - projektowanie radiatorów, izolacji
- **Metalurgii** - procesy krzepnięcia i hartowania
- **Geofizyce** - temperatura wnętrza Ziemi
- **Medycynie** - hipertermia, kriochirurgia

## 🔥 Prawo Fouriera

### Prawo podstawowe:
**Gęstość strumienia ciepła** jest proporcjonalna do gradientu temperatury:
$$\vec{q} = -k\nabla T$$

gdzie:
- $\vec{q}$ - wektor gęstości strumienia ciepła [W/m²]
- $k$ - **współczynnik przewodności cieplnej** [W/(m·K)]
- $T$ - temperatura [K lub °C]
- Znak "-" oznacza przepływ od wyższej do niższej temperatury

### W jednym wymiarze:
$$q = -k\frac{\partial T}{\partial x}$$

## 🧮 Równanie przewodnictwa ciepła

### Wyprowadzenie z zasady zachowania energii:

**Bilans energii w elemencie objętości:**
$$\text{Przyrost} = \text{Wpływ} - \text{Wypływ} + \text{Źródła}$$

### Równanie ogólne (3D):
$$\rho c \frac{\partial T}{\partial t} = k\nabla^2T + Q$$

gdzie:
- $\rho$ - gęstość [kg/m³]
- $c$ - ciepło właściwe [J/(kg·K)]
- $Q$ - moc źródeł ciepła na jednostkę objętości [W/m³]

### Dyfuzyjność cieplna:
$$\alpha = \frac{k}{\rho c} \quad [\text{m}^2/\text{s}]$$

**Równanie w postaci standardowej:**
$$\frac{\partial T}{\partial t} = \alpha\nabla^2T + \frac{Q}{\rho c}$$

## 📐 Równanie jednowymiarowe

### Postać ogólna:
$$\frac{\partial T}{\partial t} = \alpha\frac{\partial^2T}{\partial x^2} + \frac{Q(x,t)}{\rho c}$$

### Przypadki szczególne:

#### 1. Przewodnictwo stacjonarne (bez zmian w czasie):
$$\frac{\partial T}{\partial t} = 0 \Rightarrow \frac{d^2T}{dx^2} = -\frac{Q}{\alpha\rho c}$$

#### 2. Bez źródeł wewnętrznych:
$$\frac{\partial T}{\partial t} = \alpha\frac{\partial^2T}{\partial x^2}$$

#### 3. Stacjonarne bez źródeł:
$$\frac{d^2T}{dx^2} = 0 \Rightarrow T(x) = ax + b$$

## 🧱 Przewodnictwo przez ścianę płaską

### Model:
- Ściana grubości $L$
- Temperatura powierzchni: $T_1$ i $T_2$
- Stan ustalony (stacjonarny)

### Rozwiązanie:
$$\frac{d^2T}{dx^2} = 0$$

**Warunki brzegowe:** $T(0) = T_1$, $T(L) = T_2$

**Rozwiązanie:**
$$T(x) = T_1 + \frac{T_2 - T_1}{L}x$$

**Strumień ciepła:**
$$q = -k\frac{dT}{dx} = -k\frac{T_2 - T_1}{L} = \frac{k(T_1 - T_2)}{L}$$

### Opór cieplny:
$$R_{th} = \frac{L}{k} \quad \text{[K/W na jednostkę powierzchni]}$$

**Prawo Ohma dla ciepła:**
$$q = \frac{\Delta T}{R_{th}}$$

## 🔄 Przewodnictwo przez ścianę cylindryczną

### Model:
- Cylinder o promieniach wewnętrznym $r_1$ i zewnętrznym $r_2$
- Temperatury powierzchni: $T_1$ i $T_2$
- Stan stacjonarny

### Równanie w współrzędnych cylindrycznych:
$$\frac{1}{r}\frac{d}{dr}\left(r\frac{dT}{dr}\right) = 0$$

### Rozwiązanie:
$$T(r) = A\ln(r) + B$$

**Z warunkami brzegowymi:**
$$T(r) = T_1 + \frac{T_2 - T_1}{\ln(r_2/r_1)}\ln\left(\frac{r}{r_1}\right)$$

**Strumień ciepła (na jednostkę długości):**
$$q_L = \frac{2\pi k(T_1 - T_2)}{\ln(r_2/r_1)}$$

## ⏱️ Przewodnictwo niestacjonarne

### Ściana nieskończona z warunkiem początkowym:
$$\frac{\partial T}{\partial t} = \alpha\frac{\partial^2T}{\partial x^2}$$

**Warunki:**
- $T(x,0) = f(x)$ - rozkład początkowy
- Warunki brzegowe w $\pm\infty$

### Rozwiązanie fundamentalne (funkcja Greena):
$$G(x,t) = \frac{1}{\sqrt{4\pi\alpha t}}e^{-x^2/(4\alpha t)}$$

**Interpretacja:** Rozkład temperatury od źródła punktowego w $t=0$.

## 🏠 Praktyczne zastosowania

### 1. Izolacja termiczna
**Współczynnik przenikania ciepła:**
$$U = \frac{1}{\sum R_i} = \frac{1}{\sum \frac{L_i}{k_i}}$$

**Strumień przez ścianę wielowarstwową:**
$$q = U \cdot \Delta T$$

### 2. Czas stygnięcia małego ciała
**Prawo chłodzenia Newtona:**
$$\frac{dT}{dt} = -h\frac{A}{mc}(T - T_{\text{otoczenia}})$$

gdzie $h$ - współczynnik przejmowania ciepła.

**Rozwiązanie:**
$$T(t) = T_{\text{otoczenia}} + (T_0 - T_{\text{otoczenia}})e^{-t/\tau}$$

gdzie $\tau = \frac{mc}{hA}$ - stała czasowa chłodzenia.

### 3. Pręt z chłodzeniem powierzchni
**Równanie:**
$$\frac{d^2T}{dx^2} - \frac{hP}{kA}(T - T_{\text{otoczenia}}) = 0$$

gdzie:
- $P$ - obwód przekroju
- $A$ - pole przekroju

**Charakterystyczna długość:**
$$l_c = \sqrt{\frac{kA}{hP}}$$

## 📊 Metody numeryczne

### 1. Różnice skończone (1D):
$$\frac{T_i^{n+1} - T_i^n}{\Delta t} = \alpha\frac{T_{i+1}^n - 2T_i^n + T_{i-1}^n}{(\Delta x)^2}$$

### 2. Warunek stabilności (Courant):
$$\frac{\alpha \Delta t}{(\Delta x)^2} \leq \frac{1}{2}$$

### 3. Schemat niejawny (bezwarunkowo stabilny):
$$\frac{T_i^{n+1} - T_i^n}{\Delta t} = \alpha\frac{T_{i+1}^{n+1} - 2T_i^{n+1} + T_{i-1}^{n+1}}{(\Delta x)^2}$$

## 🌡️ Właściwości materiałów

### Przewodniki ciepła:
- **Miedź:** $k = 400$ W/(m·K)
- **Aluminium:** $k = 200$ W/(m·K)  
- **Stal:** $k = 50$ W/(m·K)

### Izolatory:
- **Powietrze:** $k = 0.025$ W/(m·K)
- **Styropian:** $k = 0.04$ W/(m·K)
- **Wełna mineralna:** $k = 0.04$ W/(m·K)

### Dyfuzyjność cieplna:
$$\alpha = \frac{k}{\rho c}$$

**Typowe wartości:**
- Metale: $10^{-4} - 10^{-5}$ m²/s
- Woda: $1.4 \times 10^{-7}$ m²/s
- Izolatory: $10^{-7} - 10^{-8}$ m²/s

## ⚠️ Analogie i podobieństwa

### Analogia elektryczna:
| Przewodnictwo ciepła | Obwody elektryczne |
|---------------------|-------------------|
| Temperatura $T$ | Potencjał $V$ |
| Strumień ciepła $q$ | Prąd $I$ |
| Opór cieplny $R_{th}$ | Opór elektryczny $R$ |
| Przewodność cieplna $k$ | Przewodność $\sigma$ |

### Równanie dyfuzji:
Równanie przewodnictwa ciepła ma tę samą postać co:
- **Dyfuzja materii:** $\frac{\partial c}{\partial t} = D\frac{\partial^2 c}{\partial x^2}$
- **Dyfuzja w finansach** (model Black-Scholes)
- **Przewodnictwo elektryczne w dielektrykach**

## 🔗 Powiązane tematy

- [[Równania cząstkowe]] 
- [[Metody numeryczne]]
- [[Warunki początkowe i brzegowe]]
- [[Równania o zmiennych rozdzielonych]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Przewodnictwo ciepła | Heat conduction |
| Prawo Fouriera | Fourier's law |
| Dyfuzyjność cieplna | Thermal diffusivity |
| Opór cieplny | Thermal resistance |
| Stała czasowa | Time constant |
| Współczynnik przenikania | Heat transfer coefficient |
| Równanie dyfuzji | Diffusion equation |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*