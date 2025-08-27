# Oscylator harmoniczny

## 🎯 Definicja i równanie podstawowe

**Oscylator harmoniczny** jest opisany równaniem:
$$\frac{d^2x}{dt^2} + \omega^2 x = 0$$

gdzie:
- $x(t)$ - położenie w funkcji czasu
- $\omega$ - częstość kątowa [rad/s]
- $\omega^2 > 0$ - warunek oscylacji

**Alternatywne zapisy:**
- $\ddot{x} + \omega^2 x = 0$
- $m\ddot{x} + kx = 0$ (gdzie $\omega^2 = \frac{k}{m}$)

## 🔧 Rozwiązanie ogólne

### Metoda równania charakterystycznego:
1. **Równanie charakterystyczne:** $r^2 + \omega^2 = 0$
2. **Pierwiastki:** $r = \pm i\omega$ (zespolone)
3. **Rozwiązanie ogólne:**
$$x(t) = C_1 \cos(\omega t) + C_2 \sin(\omega t)$$

### Postaci alternatywne:
$$x(t) = A \cos(\omega t + \phi)$$

gdzie:
- $A = \sqrt{C_1^2 + C_2^2}$ - **amplituda**
- $\phi = -\arctan\left(\frac{C_2}{C_1}\right)$ - **faza początkowa**

**Związki między postaciami:**
- $C_1 = A \cos(\phi)$
- $C_2 = -A \sin(\phi)$

## 📊 Charakterystyki ruchu

### Wielkości podstawowe:
- **Period:** $T = \frac{2\pi}{\omega}$
- **Częstotliwość:** $f = \frac{1}{T} = \frac{\omega}{2\pi}$ [Hz]
- **Częstość kątowa:** $\omega = 2\pi f$ [rad/s]

### Prędkość i przyspieszenie:
- **Prędkość:** $v(t) = \dot{x}(t) = -A\omega \sin(\omega t + \phi)$
- **Przyspieszenie:** $a(t) = \ddot{x}(t) = -A\omega^2 \cos(\omega t + \phi) = -\omega^2 x(t)$

## 📝 Przykłady rozwiązane

### Przykład 1: Z warunkami początkowymi
**Problem:** Rozwiąż $\ddot{x} + 4x = 0$ z warunkami $x(0) = 3$, $\dot{x}(0) = -8$.

#### Rozwiązanie:
1. **Identyfikacja:** $\omega^2 = 4$ → $\omega = 2$
2. **Rozwiązanie ogólne:** $x(t) = C_1 \cos(2t) + C_2 \sin(2t)$
3. **Prędkość:** $\dot{x}(t) = -2C_1 \sin(2t) + 2C_2 \cos(2t)$
4. **Warunki początkowe:**
   - $x(0) = C_1 = 3$
   - $\dot{x}(0) = 2C_2 = -8$ → $C_2 = -4$
5. **Rozwiązanie:** $x(t) = 3\cos(2t) - 4\sin(2t)$

**Postać amplitudowo-fazowa:**
- $A = \sqrt{3^2 + (-4)^2} = 5$
- $\phi = -\arctan\left(\frac{-4}{3}\right) = \arctan\left(\frac{4}{3}\right)$
- **Wynik:** $x(t) = 5\cos(2t + \arctan(4/3))$

### Przykład 2: Sprężyna
**Problem:** Masa $m = 2$ kg zawieszona na sprężynie o stałej $k = 8$ N/m. Początkowe wychylenie 0.5 m, początkowa prędkość 2 m/s.

#### Rozwiązanie:
1. **Częstość kątowa:** $\omega = \sqrt{\frac{k}{m}} = \sqrt{\frac{8}{2}} = 2$ rad/s
2. **Równanie:** $\ddot{x} + 4x = 0$
3. **Warunki:** $x(0) = 0.5$ m, $\dot{x}(0) = 2$ m/s
4. **Stałe:** $C_1 = 0.5$, $C_2 = 1$
5. **Rozwiązanie:** $x(t) = 0.5\cos(2t) + \sin(2t)$ [m]

## 🌟 Energia w oscylatorze harmonicznym

### Energia kinetyczna:
$$E_k = \frac{1}{2}m\dot{x}^2 = \frac{1}{2}mA^2\omega^2\sin^2(\omega t + \phi)$$

### Energia potencjalna:
$$E_p = \frac{1}{2}kx^2 = \frac{1}{2}kA^2\cos^2(\omega t + \phi)$$

### Energia całkowita:
$$E = E_k + E_p = \frac{1}{2}kA^2 = \frac{1}{2}mA^2\omega^2 = \text{const}$$

**Właściwość:** Energia całkowita jest stała (zasada zachowania energii).

## 🔄 Przestrzeń fazowa

**Wykres $(\dot{x}, x)$** dla oscylatora harmonicznego to **elipsa**:
$$\frac{x^2}{A^2} + \frac{\dot{x}^2}{A^2\omega^2} = 1$$

**Interpretacja:**
- Punkt reprezentuje stan układu
- Trajektoria to orbita zamknięta
- Kierunek ruchu zgodny z ruchem wskazówek zegara

## 🎯 Zastosowania fizyczne

### 1. **Drgania mechaniczne**
- Sprężyna z masą: $m\ddot{x} + kx = 0$
- Wahadło matematyczne (małe kąty): $\ddot{\theta} + \frac{g}{L}\theta = 0$

### 2. **Obwody elektryczne LC**
- Równanie: $L\frac{d^2q}{dt^2} + \frac{1}{C}q = 0$
- Częstość: $\omega = \frac{1}{\sqrt{LC}}$

### 3. **Drgania molekularne**
- Model oscylatora dla wiązań chemicznych
- Spektroskopia w podczerwieni

### 4. **Kwantowy oscylator harmoniczny**
- Podstawowy model w mechanice kwantowej
- Poziomy energetyczne: $E_n = \hbar\omega(n + \frac{1}{2})$

## 📊 Porównanie z innymi typami drgań

| Typ | Równanie | Rozwiązanie | Charakterystyka |
|-----|----------|-------------|-----------------|
| **Harmoniczny** | $\ddot{x} + \omega^2x = 0$ | $A\cos(\omega t + \phi)$ | Stała amplituda |
| **Tłumiony** | $\ddot{x} + 2\gamma\dot{x} + \omega^2x = 0$ | $Ae^{-\gamma t}\cos(\omega't + \phi)$ | Malejąca amplituda |
| **Wymuszony** | $\ddot{x} + \omega^2x = F\cos(\Omega t)$ | Oscylacje + rezonans | Zewnętrzne wymuszenie |

## 🧮 Metody numeryczne

### Dyskretyzacja dla metody Eulera:
$$x_{n+1} = x_n + h \cdot v_n$$
$$v_{n+1} = v_n + h \cdot (-\omega^2 x_n)$$

gdzie $h$ to krok czasowy.

## 🔗 Powiązane tematy

- [[Równania liniowe jednorodne o stałych współczynnikach]]
- [[Równania z tłumieniem]]
- [[Układy liniowe jednorodne]]
- [[Drgania mechaniczne]]
- [[Obwody elektryczne RLC]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Oscylator harmoniczny | Harmonic oscillator |
| Częstość kątowa | Angular frequency |
| Amplituda | Amplitude |
| Faza początkowa | Initial phase |
| Przestrzeń fazowa | Phase space |
| Energia kinetyczna | Kinetic energy |
| Energia potencjalna | Potential energy |

## 🎵 Ciekawostka muzyczna

Częstość drgań określa wysokość dźwięku:
- **A4** (la) = 440 Hz
- **C4** (do) ≈ 261.6 Hz
- Oktawa wyżej = 2× częstość

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*