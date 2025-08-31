# Fizyka - Elektryczność 🔌⚡

*Kompleksowe notatki do egzaminu z fizyki - dziedzina elektryczności*

---

## 📚 Spis treści

1. [Podstawowe pojęcia](#podstawowe-pojęcia)
2. [Prawo Coulomba](#prawo-coulomba)
3. [Pole elektryczne](#pole-elektryczne)
4. [Prawo Gaussa](#prawo-gaussa)
5. [Potencjał elektryczny](#potencjał-elektryczny)
6. [Pojemność elektryczna i kondensatory](#pojemność-elektryczna-i-kondensatory)
7. [Prąd elektryczny](#prąd-elektryczny)
8. [Opór i prawo Ohma](#opór-i-prawo-ohma)
9. [Obwody elektryczne](#obwody-elektryczne)
10. [Moc elektryczna](#moc-elektryczna)
11. [Elektroliza](#elektroliza)
12. [Wzory do zapamiętania](#wzory-do-zapamiętania)

---

## Podstawowe pojęcia

### Ładunek elektryczny
- **Ładunek elektryczny (q)** - podstawowa właściwość materii
- Jednostka: **Coulomb [C]**
- Ładunek elementarny: $e = 1{,}602 \times 10^{-19}$ C
- **Zasada zachowania ładunku**: suma ładunków w układzie izolowanym pozostaje stała

### Rodzaje ładunków
- **Dodatni (+)**: niedobór elektronów
- **Ujemny (-)**: nadmiar elektronów
- **Zasada**: ładunki jednoimienne się odpychają, różnoimienne się przyciągają

### Kwantowanie ładunku
- Każdy ładunek jest wielokrotnością ładunku elementarnego:
$$q = n \cdot e$$
gdzie $n$ to liczba całkowita

---

## Prawo Coulomba

### Definicja
Prawo opisujące **siłę elektrostatyczną** między dwoma punktowymi ładunkami:

$$F = k \cdot \frac{|q_1 \cdot q_2|}{r^2}$$

gdzie:
- $F$ – siła elektrostatyczna [N]
- $q_1, q_2$ – ładunki elektryczne [C]
- $r$ – odległość między ładunkami [m]
- $k$ – stała Coulomba: $k = \frac{1}{4\pi\varepsilon_0} \approx 8{,}99 \times 10^9 \frac{N \cdot m^2}{C^2}$

### Postać wektorowa
$$\vec{F}_{12} = k \cdot \frac{q_1 q_2}{r^2} \cdot \hat{r}_{12}$$

### Właściwości
- **Odpychanie**: ładunki tego samego znaku
- **Przyciąganie**: ładunki przeciwnych znaków
- Działa na linii łączącej ładunki
- Spełnia trzecią zasadę dynamiki Newtona: $\vec{F}_{12} = -\vec{F}_{21}$

**📖 Szczegóły:** [[Prawa Coulomba i Gaussa]]

---

## Pole elektryczne

### Definicja
**Pole elektryczne** to przestrzeń wokół ładunków, w której działa siła elektryczna na inne ładunki.

**Natężenie pola elektrycznego**:
$$\vec{E} = \frac{\vec{F}}{q_0}$$

gdzie:
- $\vec{E}$ – natężenie pola elektrycznego [N/C] lub [V/m]
- $\vec{F}$ – siła działająca na ładunek próbny
- $q_0$ – ładunek próbny (dodatni)

### Pole ładunku punktowego
$$\vec{E} = k \cdot \frac{q}{r^2} \cdot \hat{r}$$

### Zasada superpozycji
Pole wypadkowe jest sumą wektorową pól od wszystkich ładunków:
$$\vec{E}_{wyp} = \sum_{i=1}^{n} \vec{E}_i$$

### Linie sił pola
- Wychodzą z ładunków dodatnich
- Wchodzą do ładunków ujemnych
- Nigdy się nie przecinają
- Gęstość linii ~ natężenie pola

---

## Prawo Gaussa

### Definicja
Prawo łączące **strumień pola elektrycznego** przez zamkniętą powierzchnię z ładunkiem wewnątrz:

$$\oint_S \vec{E} \cdot d\vec{S} = \frac{Q_{wew}}{\varepsilon_0}$$

### Interpretacja
- **Źródłem pola** są ładunki elektryczne
- Strumień zależy tylko od ładunków wewnątrz powierzchni
- Niezależny od rozkładu ładunków

### Zastosowania
Szczególnie użyteczne przy symetriach:
- **Sferyczna**: ładunek punktowy, kula naładowana
- **Cylindryczna**: nieskończony przewód
- **Płaska**: nieskończona naładowana płaszczyzna

**📖 Szczegóły:** [[Prawa Coulomba i Gaussa]]

---

## Potencjał elektryczny

### Definicja potencjału
**Potencjał elektryczny** to energia potencjalna jednostkowego ładunku dodatniego:

$$V = \frac{U}{q_0}$$

Jednostka: **Volt [V]**

### Potencjał ładunku punktowego
$$V = k \cdot \frac{q}{r}$$

### Różnica potencjałów (napięcie)
$$U = V_A - V_B = -\int_A^B \vec{E} \cdot d\vec{l}$$

### Związek między polem a potencjałem
**Pole jest gradientem potencjału**:
$$\vec{E} = -\nabla V = -\frac{\partial V}{\partial x}\hat{i} - \frac{\partial V}{\partial y}\hat{j} - \frac{\partial V}{\partial z}\hat{k}$$

W przypadku jednowymiarowym:
$$E = -\frac{dV}{dx}$$

### Praca w polu elektrycznym
$$W = q(V_A - V_B) = qU$$

**📖 Szczegóły:** [[Związek między potencjałem a natężeniem pola elektrycznego + dowod]]

---

## Pojemność elektryczna i kondensatory

### Pojemność elektryczna
**Pojemność** określa zdolność przewodnika do gromadzenia ładunku:

$$C = \frac{Q}{U}$$

gdzie:
- $C$ – pojemność [F] (farad)
- $Q$ – ładunek [C]
- $U$ – napięcie [V]

### Kondensator płaski
Składa się z dwóch równoległych płytek:

$$C = \varepsilon_0 \varepsilon_r \frac{S}{d}$$

gdzie:
- $\varepsilon_0 = 8{,}854 \times 10^{-12} \frac{F}{m}$ – przenikalność próżni
- $\varepsilon_r$ – względna przenikalność dielektryka
- $S$ – powierzchnia okładki
- $d$ – odległość między okładkami

### Energia kondensatora
$$U = \frac{1}{2}CV^2 = \frac{1}{2}QV = \frac{Q^2}{2C}$$

### Łączenie kondensatorów

#### Równolegle
$$C_{wyp} = C_1 + C_2 + C_3 + ...$$

#### Szeregowo
$$\frac{1}{C_{wyp}} = \frac{1}{C_1} + \frac{1}{C_2} + \frac{1}{C_3} + ...$$

**📖 Szczegóły:** [[Definicja pojemności elektrycznej, kondensator płaski, łączenie kondensatorów]]

---

## Prąd elektryczny

### Definicja natężenia prądu
**Natężenie prądu** to ładunek przepływający przez przekrój przewodnika w jednostce czasu:

$$I = \frac{Q}{t} = \frac{dQ}{dt}$$

Jednostka: **Amper [A]**

### Gęstość prądu
$$\vec{j} = n \cdot e \cdot \vec{v}$$

gdzie:
- $n$ – koncentracja nośników ładunku
- $e$ – ładunek elementarny  
- $\vec{v}$ – prędkość unoszenia

### Związek z natężeniem prądu
$$I = \int_S \vec{j} \cdot d\vec{S}$$

Dla przewodnika jednorodnego:
$$I = j \cdot S$$

---

## Opór i prawo Ohma

### Opór elektryczny
**Opór** charakteryzuje przeciwdziałanie przepływowi prądu:

$$R = \frac{U}{I}$$

Jednostka: **Om [Ω]**

### Oporność właściwa
$$R = \rho \frac{l}{S}$$

gdzie:
- $\rho$ – oporność właściwa [Ω⋅m]
- $l$ – długość przewodnika
- $S$ – pole przekroju

### Prawo Ohma

#### Postać makroskopowa
$$U = I \cdot R$$

#### Postać mikroskopowa
$$\vec{j} = \sigma \vec{E}$$

gdzie $\sigma = \frac{1}{\rho}$ – przewodność właściwa

### Zależność oporu od temperatury
$$R(T) = R_0[1 + \alpha(T - T_0)]$$

gdzie $\alpha$ – współczynnik temperaturowy oporu

### Łączenie oporników

#### Szeregowo
$$R_{wyp} = R_1 + R_2 + R_3 + ...$$

#### Równolegle
$$\frac{1}{R_{wyp}} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3} + ...$$

**📖 Szczegóły:** [[Opór (R) i oporność właściwa (), prawo Ohma (w postaci mikro- i makroskopowej), zależność oporu od temperatury]]

---

## Obwody elektryczne

### Prawa Kirchhoffa

#### I prawo (prawo węzłowe)
**Suma prądów wpływających do węzła = suma prądów wypływających**
$$\sum I_{wply} = \sum I_{wyply}$$

lub w ogólnej postaci:
$$\sum_{i} I_i = 0$$

#### II prawo (prawo oczek)
**Suma spadków napięć w zamkniętej pętli = suma siły elektromotorycznych**
$$\sum U_R = \sum \varepsilon$$

lub:
$$\sum_{i} U_i = 0$$

### Siła elektromotoryczna (SEM)
$$\varepsilon = \frac{W_{stronnych}}{q}$$

### Prawo Ohma dla obwodu z SEM
$$\varepsilon = I(R + r)$$

gdzie $r$ – opór wewnętrzny źródła

**📖 Szczegóły:** [[Natężenie, napięcie i moc prądu, analiza obwodów elektrycznych]]

---

## Moc elektryczna

### Moc w obwodzie elektrycznym
$$P = U \cdot I$$

### Inne postacie
- $P = I^2 R$ (z prawa Ohma)
- $P = \frac{U^2}{R}$ (z prawa Ohma)

### Jednostka
**Wat [W]**

### Energia elektryczna
$$E = P \cdot t = UIt$$

Jednostka: **Wat-sekunda [Ws]** lub **kilowatogodzina [kWh]**

### Sprawność
$$\eta = \frac{P_{użyteczna}}{P_{całkowita}} \times 100\%$$

---

## Elektroliza

### Definicja
**Elektroliza** to proces rozkładu związków chemicznych pod wpływem prądu elektrycznego.

### I prawo Faradaya
**Masa wydzielonej substancji jest proporcjonalna do ładunku**:
$$m = k \cdot Q = k \cdot I \cdot t$$

gdzie $k$ – równoważnik elektrochemiczny

### II prawo Faradaya  
**Równoważnik elektrochemiczny jest proporcjonalny do masy molowej**:
$$k = \frac{M}{n \cdot F}$$

gdzie:
- $M$ – masa molowa
- $n$ – wartościowość  
- $F$ – stała Faradaya ($F = 96485$ C/mol)

### Łączne równanie elektrolizy
$$m = \frac{M \cdot I \cdot t}{n \cdot F}$$

**📖 Szczegóły:** [[Przepływ prądu w elektrolitach; prawa elektrolizy]]

---

## Wzory do zapamiętania

### Podstawowe stałe
- Ładunek elementarny: $e = 1{,}602 \times 10^{-19}$ C
- Stała Coulomba: $k = 8{,}99 \times 10^9 \frac{N \cdot m^2}{C^2}$
- Przenikalność próżni: $\varepsilon_0 = 8{,}854 \times 10^{-12} \frac{F}{m}$
- Stała Faradaya: $F = 96485$ C/mol

### Kluczowe wzory

| Wielkość | Wzór | Jednostka |
|----------|------|-----------|
| Prawo Coulomba | $F = k \frac{q_1 q_2}{r^2}$ | N |
| Natężenie pola | $E = \frac{F}{q}$ | N/C |
| Potencjał | $V = k \frac{q}{r}$ | V |
| Pojemność | $C = \frac{Q}{U}$ | F |
| Prawo Ohma | $U = IR$ | V |
| Moc elektryczna | $P = UI$ | W |
| I prawo Faradaya | $m = kIt$ | kg |

### Łączenie elementów

| Element | Szeregowo | Równolegle |
|---------|-----------|------------|
| Oporniki | $R = R_1 + R_2 + ...$ | $\frac{1}{R} = \frac{1}{R_1} + \frac{1}{R_2} + ...$ |
| Kondensatory | $\frac{1}{C} = \frac{1}{C_1} + \frac{1}{C_2} + ...$ | $C = C_1 + C_2 + ...$ |

---

## 🔗 Powiązane notatki

### Elektryczność i magnetyzm
- [[Prawa Coulomba i Gaussa]] - szczegółowe wyprowadzenia
- [[Związek między potencjałem a natężeniem pola elektrycznego + dowod]] - matematyczne podstawy
- [[Definicja pojemności elektrycznej, kondensator płaski, łączenie kondensatorów]] - kondensatory
- [[Opór (R) i oporność właściwa (), prawo Ohma (w postaci mikro- i makroskopowej), zależność oporu od temperatury]] - opór elektryczny
- [[Natężenie, napięcie i moc prądu, analiza obwodów elektrycznych]] - analiza obwodów
- [[Przepływ prądu w elektrolitach; prawa elektrolizy]] - elektroliza

### Hub główny
[[ELEKRYCZNOŚĆ I MAGNETYZM]] - wszystkie tematy z elektryczności i magnetyzmu

---

*📚 Notatka utworzona dla kompleksowego przygotowania do egzaminu z fizyki*
*🔧 Ostatnia aktualizacja: Styczeń 2025*