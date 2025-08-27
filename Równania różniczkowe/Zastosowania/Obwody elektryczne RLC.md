# Obwody elektryczne RLC

## ⚡ Wprowadzenie

**Obwody RLC** zawierają trzy podstawowe elementy:
- **R** - Rezystor (opór)
- **L** - Cewka indukcyjna (indukcyjność)  
- **C** - Kondensator (pojemność)

Równania różniczkowe opisujące te obwody są analogiczne do równań drgań mechanicznych.

## 🔌 Podstawowe prawa i elementy

### Prawa Kirchhoffa:
1. **I prawo:** Suma prądów w węźle = 0
2. **II prawo:** Suma spadków napięć w oczku = 0

### Relacje napięcie-prąd:
- **Rezystor:** $V_R = IR$ (prawo Ohma)
- **Cewka:** $V_L = L\frac{dI}{dt}$ 
- **Kondensator:** $I = C\frac{dV_C}{dt}$ lub $V_C = \frac{1}{C}\int I dt$

### Energia w elementach:
- **Rezystor:** $P_R = I^2R$ (rozpraszana)
- **Cewka:** $E_L = \frac{1}{2}LI^2$ (magnetyczna)
- **Kondensator:** $E_C = \frac{1}{2}CV^2$ (elektryczna)

## 🔄 Obwód szeregowy RLC

### Schemat i równanie:
```
V(t) ── R ── L ── C ── GND
```

**Równanie według II prawa Kirchhoffa:**
$$V(t) = V_R + V_L + V_C = IR + L\frac{dI}{dt} + \frac{q}{C}$$

Ponieważ $I = \frac{dq}{dt}$:
$$V(t) = R\frac{dq}{dt} + L\frac{d^2q}{dt^2} + \frac{q}{C}$$

**Standardowa postać:**
$$L\frac{d^2q}{dt^2} + R\frac{dq}{dt} + \frac{1}{C}q = V(t)$$

## 🎯 Obwód LC (bez oporu)

### Równanie jednorodne:
$$L\frac{d^2q}{dt^2} + \frac{1}{C}q = 0$$

**Dzieląc przez $L$:**
$$\frac{d^2q}{dt^2} + \frac{1}{LC}q = 0$$

### Rozwiązanie:
**Częstość kątowa:** $\omega_0 = \frac{1}{\sqrt{LC}}$

**Rozwiązanie ogólne:**
$$q(t) = A\cos(\omega_0 t) + B\sin(\omega_0 t)$$

**Prąd:**
$$I(t) = \frac{dq}{dt} = -A\omega_0\sin(\omega_0 t) + B\omega_0\cos(\omega_0 t)$$

### Interpretacja fizyczna:
- **Oscylacje harmoniczne** ładunku i prądu
- **Wymiana energii** między polem elektrycznym (C) a magnetycznym (L)
- **Częstość rezonansowa:** $f_0 = \frac{1}{2\pi\sqrt{LC}}$

## 🔧 Obwód RLC z tłumieniem

### Równanie charakterystyczne:
$$Lr^2 + Rr + \frac{1}{C} = 0$$

**Wyznacznik:** $\Delta = R^2 - 4L \cdot \frac{1}{C} = R^2 - \frac{4L}{C}$

### Przypadki rozwiązań:

#### 1. Słabe tłumienie ($\Delta < 0$, $R < 2\sqrt{\frac{L}{C}}$)
**Pierwiastki zespolone:** $r = -\frac{R}{2L} \pm i\omega_d$

gdzie $\omega_d = \sqrt{\frac{1}{LC} - \frac{R^2}{4L^2}}$ - częstość tłumiona

**Rozwiązanie:**
$$q(t) = Ae^{-\frac{R}{2L}t}\cos(\omega_d t + \phi)$$

**Charakterystyka:** Oscylacje tłumione wykładniczo

#### 2. Tłumienie krytyczne ($\Delta = 0$, $R = 2\sqrt{\frac{L}{C}}$)
**Pierwiastek podwójny:** $r = -\frac{R}{2L}$

**Rozwiązanie:**
$$q(t) = (A + Bt)e^{-\frac{R}{2L}t}$$

**Charakterystyka:** Najszybszy powrót do równowagi bez oscylacji

#### 3. Silne tłumienie ($\Delta > 0$, $R > 2\sqrt{\frac{L}{C}}$)
**Pierwiastki rzeczywiste:** $r_1, r_2 < 0$ różne

**Rozwiązanie:**
$$q(t) = Ae^{r_1 t} + Be^{r_2 t}$$

**Charakterystyka:** Powolny powrót bez oscylacji

## 📝 Przykład obliczeniowy

### Dane:
- $L = 0.1$ H (henr)
- $C = 10^{-4}$ F (farad)  
- $R = 20$ Ω (om)
- Warunki początkowe: $q(0) = 10^{-3}$ C, $I(0) = 0$ A

### Rozwiązanie:
1. **Sprawdzenie typu tłumienia:**
   $$2\sqrt{\frac{L}{C}} = 2\sqrt{\frac{0.1}{10^{-4}}} = 2\sqrt{1000} = 63.2 \text{ Ω}$$
   
   Ponieważ $R = 20 < 63.2$, mamy słabe tłumienie.

2. **Parametry:**
   - $\omega_0 = \frac{1}{\sqrt{LC}} = \frac{1}{\sqrt{0.1 \times 10^{-4}}} = 316.2$ rad/s
   - $\alpha = \frac{R}{2L} = \frac{20}{0.2} = 100$ s⁻¹
   - $\omega_d = \sqrt{\omega_0^2 - \alpha^2} = \sqrt{316.2^2 - 100^2} = 300$ rad/s

3. **Rozwiązanie ogólne:**
   $$q(t) = e^{-100t}(A\cos(300t) + B\sin(300t))$$

4. **Stałe z warunków początkowych:**
   - $q(0) = A = 10^{-3}$
   - $I(0) = \frac{dq}{dt}\big|_{t=0} = -100A + 300B = 0$ → $B = \frac{100}{300}A = \frac{1}{3} \times 10^{-3}$

5. **Rozwiązanie szczególne:**
   $$q(t) = e^{-100t}\left(10^{-3}\cos(300t) + \frac{10^{-3}}{3}\sin(300t)\right)$$

## 🌊 Obwód z wymuszeniem harmonicznym

### Równanie niejednorodne:
$$L\frac{d^2q}{dt^2} + R\frac{dq}{dt} + \frac{1}{C}q = V_0\cos(\Omega t)$$

### Rozwiązanie ustalone (przy $t \to \infty$):
$$q_p(t) = A\cos(\Omega t - \phi)$$

gdzie:
- **Amplituda:** $A = \frac{V_0}{\sqrt{R^2 + (\Omega L - \frac{1}{\Omega C})^2}}$
- **Przesunięcie fazowe:** $\phi = \arctan\left(\frac{\Omega L - \frac{1}{\Omega C}}{R}\right)$

### Rezonans:
**Warunek:** $\Omega = \omega_0 = \frac{1}{\sqrt{LC}}$

**Amplituda w rezonansie:** $A_{max} = \frac{V_0}{R}$

## 🔗 Analogie z mechaniką

| Mechanika | Elektryczność |
|-----------|---------------|
| Masa $m$ | Indukcyjność $L$ |
| Tłumienie $c$ | Opór $R$ |
| Sztywność $k$ | $\frac{1}{C}$ |
| Położenie $x$ | Ładunek $q$ |
| Prędkość $v$ | Prąd $I$ |
| Siła $F$ | Napięcie $V$ |

## 🔗 Powiązane tematy

- [[Oscylator harmoniczny]]
- [[Równania z tłumieniem]]
- [[Równania liniowe niejednorodne - metoda współczynników nieoznaczonych]]
- [[Drgania mechaniczne]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Obwód RLC | RLC circuit |
| Cewka indukcyjna | Inductor |
| Kondensator | Capacitor |
| Tłumienie krytyczne | Critical damping |
| Rezonans | Resonance |
| Częstość rezonansowa | Resonant frequency |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*