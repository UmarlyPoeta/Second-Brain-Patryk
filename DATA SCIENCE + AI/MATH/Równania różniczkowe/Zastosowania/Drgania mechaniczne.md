# Drgania mechaniczne

## 🎯 Wprowadzenie

**Drgania mechaniczne** to powtarzające się ruchy ciał wokół położenia równowagi. Są opisywane równaniami różniczkowymi i występują powszechnie w:
- **Mechanice** - wahadła, sprężyny, membrany
- **Inżynierii** - konstrukcje, maszyny, mosty  
- **Akustyce** - instrumenty muzyczne, głośniki
- **Sejsmologii** - trzęsienia ziemi

## 🏗️ Oscylator harmoniczny prosty

### Model fizyczny:
- Masa $m$ zawieszona na sprężynie o stałej $k$
- Brak tarcia i oporów
- Małe wychylenia (prawo Hooke'a)

### Równanie ruchu:
**II zasada dynamiki:** $F = ma$
$$m\frac{d^2x}{dt^2} = -kx$$

**Postać standardowa:**
$$\frac{d^2x}{dt^2} + \omega_0^2 x = 0$$

gdzie $\omega_0 = \sqrt{\frac{k}{m}}$ - **częstość własna**

### Rozwiązanie:
$$x(t) = A\cos(\omega_0 t + \phi)$$

**Parametry:**
- $A$ - **amplituda** (maksymalne wychylenie)
- $\omega_0$ - **częstość kątowa** [rad/s]
- $\phi$ - **faza początkowa** [rad]
- $T = \frac{2\pi}{\omega_0}$ - **okres** drgań [s]

## 🌊 Oscylator tłumiony

### Model z tarciem:
- Siła tarcia proporcjonalna do prędkości: $F_{tarcia} = -c\dot{x}$
- Współczynnik tłumienia: $c > 0$

### Równanie ruchu:
$$m\ddot{x} + c\dot{x} + kx = 0$$

**Postać standardowa:**
$$\ddot{x} + 2\gamma\dot{x} + \omega_0^2 x = 0$$

gdzie:
- $\gamma = \frac{c}{2m}$ - **współczynnik tłumienia**
- $\omega_0 = \sqrt{\frac{k}{m}}$ - **częstość własna**

### Równanie charakterystyczne:
$$r^2 + 2\gamma r + \omega_0^2 = 0$$

**Wyznacznik:** $\Delta = 4\gamma^2 - 4\omega_0^2 = 4(\gamma^2 - \omega_0^2)$

## 📊 Przypadki tłumienia

### 1. Słabe tłumienie (podkrytyczne): $\gamma < \omega_0$
**Pierwiastki zespolone:** $r = -\gamma \pm i\omega_d$

gdzie $\omega_d = \sqrt{\omega_0^2 - \gamma^2}$ - **częstość drgań tłumionych**

**Rozwiązanie:**
$$x(t) = Ae^{-\gamma t}\cos(\omega_d t + \phi)$$

**Charakterystyka:**
- Oscylacje z wykładniczo malejącą amplitudą
- Częstość niższa niż bez tłumienia: $\omega_d < \omega_0$
- **Logarytmiczny dekrement tłumienia:** $\delta = \gamma T_d = \frac{2\pi\gamma}{\omega_d}$

### 2. Tłumienie krytyczne: $\gamma = \omega_0$
**Pierwiastek podwójny:** $r = -\gamma$

**Rozwiązanie:**
$$x(t) = (A + Bt)e^{-\gamma t}$$

**Charakterystyka:**
- Najszybszy powrót do równowagi bez oscylacji
- Graniczny przypadek - zastosowanie w systemach sterowania

### 3. Silne tłumienie (nadkrytyczne): $\gamma > \omega_0$
**Pierwiastki rzeczywiste różne:** $r_1, r_2 < 0$

**Rozwiązanie:**
$$x(t) = Ae^{r_1 t} + Be^{r_2 t}$$

**Charakterystyka:**
- Powolny powrót bez oscylacji
- Oba wykładniki ujemne → stabilność asymptotyczna

## ⚡ Drgania wymuszone

### Model z siłą zewnętrzną:
$$m\ddot{x} + c\dot{x} + kx = F_0\cos(\Omega t)$$

**Postać standardowa:**
$$\ddot{x} + 2\gamma\dot{x} + \omega_0^2 x = f_0\cos(\Omega t)$$

gdzie $f_0 = \frac{F_0}{m}$, $\Omega$ - **częstość wymuszenia**

### Rozwiązanie ustalone (po zaniku przejściowego):
$$x_p(t) = A(\Omega)\cos(\Omega t - \phi(\Omega))$$

**Amplituda:**
$$A(\Omega) = \frac{f_0}{\sqrt{(\omega_0^2 - \Omega^2)^2 + (2\gamma\Omega)^2}}$$

**Przesunięcie fazowe:**
$$\phi(\Omega) = \arctan\left(\frac{2\gamma\Omega}{\omega_0^2 - \Omega^2}\right)$$

## 🎵 Rezonans

### Warunki rezonansu:
**Częstość rezonansowa:** $\Omega_{rez} = \sqrt{\omega_0^2 - 2\gamma^2}$

**Dla słabego tłumienia:** $\Omega_{rez} \approx \omega_0$

### Amplituda w rezonansie:
$$A_{max} = \frac{f_0}{2\gamma\sqrt{\omega_0^2 - \gamma^2}} \approx \frac{f_0}{2\gamma\omega_0}$$

### Współczynnik jakości:
$$Q = \frac{\omega_0}{2\gamma}$$

**Interpretacja:**
- $Q >> 1$ - rezonans ostry, małe tłumienie
- $Q \approx 1$ - rezonans szerokie, duże tłumienie

## 📝 Przykłady fizyczne

### 1. Wahadło matematyczne
**Równanie dla małych kątów:**
$$\frac{d^2\theta}{dt^2} + \frac{g}{L}\theta = 0$$

**Częstość:** $\omega_0 = \sqrt{\frac{g}{L}}$

**Period:** $T = 2\pi\sqrt{\frac{L}{g}}$

### 2. Wahadło torsyjne
**Równanie:**
$$I\frac{d^2\theta}{dt^2} + c\frac{d\theta}{dt} + k\theta = 0$$

gdzie:
- $I$ - moment bezwładności
- $c$ - współczynnik tłumienia torsyjnego
- $k$ - stała torsyjna

### 3. Drgania struny
**Równanie falowe (1D):**
$$\frac{\partial^2 y}{\partial t^2} = \frac{T}{\rho}\frac{\partial^2 y}{\partial x^2}$$

gdzie:
- $T$ - naprężenie struny
- $\rho$ - gęstość liniowa
- $c = \sqrt{\frac{T}{\rho}}$ - prędkość fali

## 🌍 Zastosowania inżynierskie

### 1. Tłumiki drgań
**Cel:** Redukcja amplitudy drgań w konstrukcjach
**Metody:**
- Zwiększenie tłumienia ($\gamma$)
- Detuning (zmiana częstości własnej)
- Tłumiki dynamiczne

### 2. Izolacja drgań
**Transmitancja:** $T = \frac{1}{\sqrt{(1-r^2)^2 + (2\zeta r)^2}}$

gdzie $r = \frac{\Omega}{\omega_0}$, $\zeta = \frac{\gamma}{\omega_0}$

**Warunki izolacji:** $r > \sqrt{2}$ (częstość wymuszenia wyższa od $\sqrt{2}\omega_0$)

### 3. Pomiary drgań
- **Akcelerometry** - pomiar przyspieszeń
- **Sejsmometry** - detekcja trzęsień ziemi
- **Wibrometry** - analiza drgań maszyn

## 📊 Analiza widmowa

### Transformata Fourier:
$$X(\omega) = \int_{-\infty}^{\infty} x(t)e^{-i\omega t}dt$$

**Zastosowania:**
- Identyfikacja częstości dominujących
- Diagnoza stanu technicznego
- Projektowanie filtrów

### Funkcja odpowiedzi częstotliwościowej:
$$H(\omega) = \frac{1}{-\omega^2 + 2i\gamma\omega + \omega_0^2}$$

## ⚠️ Skutki rezonansu

### Przykłady historyczne:
1. **Most w Tacoma Narrows (1940)** - rezonans wywołany wiatrem
2. **Budynki podczas trzęsień ziemi** - rezonans z falami sejsmicznymi
3. **Maszyny wirujące** - rezonans przy krytycznych obrotach

### Zapobieganie:
- Projektowanie z odpowiednim marginesem bezpieczeństwa
- Tłumienie aktywne i pasywne
- Detuning konstrukcji

## 🔗 Powiązane tematy

- [[Oscylator harmoniczny]]
- [[Równania z tłumieniem]]
- [[Obwody elektryczne RLC]]
- [[Równania liniowe niejednorodne - metoda współczynników nieoznaczonych]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Drgania mechaniczne | Mechanical vibrations |
| Częstość własna | Natural frequency |
| Tłumienie krytyczne | Critical damping |
| Rezonans | Resonance |
| Współczynnik jakości | Quality factor |
| Logarytmiczny dekrement | Logarithmic decrement |
| Izolacja drgań | Vibration isolation |
| Transmitancja | Transmissibility |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*