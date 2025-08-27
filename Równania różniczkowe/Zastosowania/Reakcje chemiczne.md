# Reakcje chemiczne

## ⚗️ Wprowadzenie

**Kinetyka chemiczna** wykorzystuje równania różniczkowe do opisu szybkości reakcji chemicznych. Równania te pozwalają na:
- Przewidywanie przebiegu reakcji w czasie
- Projektowanie reaktorów chemicznych
- Optymalizację procesów przemysłowych
- Zrozumienie mechanizmów reakcji

## 🧪 Podstawy kinetyki chemicznej

### Szybkość reakcji:
**Definicja:** Zmiana stężenia reagenta lub produktu w jednostce czasu.

Dla reakcji: $aA + bB \rightarrow cC + dD$

$$r = -\frac{1}{a}\frac{d[A]}{dt} = -\frac{1}{b}\frac{d[B]}{dt} = \frac{1}{c}\frac{d[C]}{dt} = \frac{1}{d}\frac{d[D]}{dt}$$

### Prawo działania mas:
$$r = k[A]^{\alpha}[B]^{\beta}$$

gdzie:
- $k$ - **stała szybkości reakcji** [zależy od jednostek]
- $\alpha, \beta$ - **rzędy reakcji** (empiryczne, nie zawsze = współczynnikom stechiometrycznym)

## 📊 Klasyfikacja reakcji według rzędu

### Reakcja zerowego rzędu:
$$\frac{d[A]}{dt} = -k_0$$

**Rozwiązanie:**
$$[A](t) = [A]_0 - k_0 t$$

**Czas połowicznego rozpadu:**
$$t_{1/2} = \frac{[A]_0}{2k_0}$$

**Przykłady:** Kataliza heterogeniczna przy nasyceniu powierzchni

### Reakcja pierwszego rzędu:
$$\frac{d[A]}{dt} = -k_1[A]$$

**Rozwiązanie:**
$$[A](t) = [A]_0 e^{-k_1 t}$$

**Czas połowicznego rozpadu:**
$$t_{1/2} = \frac{\ln 2}{k_1} = \frac{0.693}{k_1}$$

**Przykłady:** Rozpad radioaktywny, hydroliza w nadmiarze wody

### Reakcja drugiego rzędu:

#### Przypadek A: $2A \rightarrow \text{produkty}$
$$\frac{d[A]}{dt} = -k_2[A]^2$$

**Rozwiązanie:**
$$\frac{1}{[A](t)} = \frac{1}{[A]_0} + k_2 t$$

**Czas połowicznego rozpadu:**
$$t_{1/2} = \frac{1}{k_2[A]_0}$$

#### Przypadek B: $A + B \rightarrow \text{produkty}$ (stężenia różne)
$$\frac{d[A]}{dt} = -k_2[A][B]$$

Z bilansu masy: $[B] = [B]_0 - ([A]_0 - [A])$

**Rozwiązanie** (gdy $[A]_0 \neq [B]_0$):
$$\ln\frac{[A][B]_0}{[A]_0[B]} = ([B]_0 - [A]_0)k_2 t$$

## 🔄 Reakcje odwracalne

### Model prostej reakcji odwracalnej:
$$A \underset{k_{-1}}{\overset{k_1}{\rightleftharpoons}} B$$

**Równanie kinetyczne:**
$$\frac{d[A]}{dt} = -k_1[A] + k_{-1}[B]$$

Z bilansu masy: $[A] + [B] = [A]_0 + [B]_0 = C_{\text{total}}$

**Podstawiając:** $[B] = C_{\text{total}} - [A]$
$$\frac{d[A]}{dt} = -k_1[A] + k_{-1}(C_{\text{total}} - [A]) = -(k_1 + k_{-1})[A] + k_{-1}C_{\text{total}}$$

### Rozwiązanie:
$$[A](t) = \frac{k_{-1}C_{\text{total}}}{k_1 + k_{-1}} + \left([A]_0 - \frac{k_{-1}C_{\text{total}}}{k_1 + k_{-1}}\right)e^{-(k_1 + k_{-1})t}$$

### Stan równowagi:
$$[A]_{\text{eq}} = \frac{k_{-1}C_{\text{total}}}{k_1 + k_{-1}}$$

**Stała równowagi:** $K = \frac{k_1}{k_{-1}} = \frac{[B]_{\text{eq}}}{[A]_{\text{eq}}}$

## ⚡ Reakcje następcze (szeregowe)

### Model: $A \overset{k_1}{\rightarrow} B \overset{k_2}{\rightarrow} C$

**Układ równań:**
$$\begin{cases}
\frac{d[A]}{dt} = -k_1[A] \\
\frac{d[B]}{dt} = k_1[A] - k_2[B] \\
\frac{d[C]}{dt} = k_2[B]
\end{cases}$$

### Rozwiązanie:
1. **Dla A:** $[A](t) = [A]_0 e^{-k_1 t}$

2. **Dla B:** 
   $$[B](t) = \frac{k_1[A]_0}{k_2 - k_1}(e^{-k_1 t} - e^{-k_2 t})$$

3. **Dla C:** $[C](t) = [A]_0 - [A](t) - [B](t)$

### Maksimum stężenia B:
$$t_{\max} = \frac{\ln(k_2/k_1)}{k_2 - k_1}$$

## 🌡️ Wpływ temperatury - równanie Arrheniusa

### Zależność stałej szybkości od temperatury:
$$k = A e^{-E_a/(RT)}$$

gdzie:
- $A$ - **czynnik przedwykładniczy** [te same jednostki co $k$]
- $E_a$ - **energia aktywacji** [J/mol]
- $R$ - stała gazowa [8.314 J/(mol·K)]
- $T$ - temperatura bezwzględna [K]

### Postać logarytmiczna:
$$\ln k = \ln A - \frac{E_a}{RT}$$

**Wykres $\ln k$ vs $1/T$ daje prostę o nachyleniu $-E_a/R$**

### Wpływ temperatury na szybkość:
Przybliżona reguła: **wzrost temperatury o 10°C podwaja szybkość reakcji**

## 🏭 Reaktory chemiczne

### Reaktor okresowy (batch):
**Bilans masy:** Akumulacja = Produkcja - Zużycie
$$\frac{d[A]}{dt} = -r_A$$

### Reaktor przepływowy z mieszaniem (CSTR):
**Stan ustalony:**
$$0 = \frac{F_{A0} - F_A}{V} - r_A$$

gdzie:
- $F_{A0}, F_A$ - strumienie molowe na wlocie i wylocie
- $V$ - objętość reaktora
- $r_A$ - szybkość reakcji A

### Reaktor rurowy (PFR):
**Bilans na element długości:**
$$\frac{d[A]}{dz} = -\frac{r_A}{v}$$

gdzie $v$ - prędkość liniowa przepływu.

## 📝 Przykłady liczbowe

### Przykład 1: Reakcja pierwszego rzędu
**Problem:** $A \rightarrow B$, $k = 0.1$ min⁻¹, $[A]_0 = 2$ mol/L
**Pytanie:** Ile zostanie A po 10 minutach?

**Rozwiązanie:**
$$[A](10) = 2 \cdot e^{-0.1 \times 10} = 2 \cdot e^{-1} = 2 \times 0.368 = 0.736 \text{ mol/L}$$

### Przykład 2: Czas połowiczego rozpadu
**Problem:** Reakcja pierwszego rzędu, 25% reagenta przereagowało w 50 min.
**Pytanie:** Jaki jest czas połowiczego rozpadu?

**Rozwiązanie:**
$$[A] = 0.75[A]_0 = [A]_0 e^{-k \times 50}$$
$$0.75 = e^{-50k} \Rightarrow k = \frac{-\ln(0.75)}{50} = 0.00575 \text{ min}^{-1}$$
$$t_{1/2} = \frac{\ln 2}{k} = \frac{0.693}{0.00575} = 120.5 \text{ min}$$

## 🧬 Kinetyka enzymatyczna - równanie Michaelisa-Menten

### Mechanizm:
$$E + S \underset{k_{-1}}{\overset{k_1}{\rightleftharpoons}} ES \overset{k_2}{\rightarrow} E + P$$

### Przybliżenie stanu quasi-ustalonego:
$$\frac{d[ES]}{dt} \approx 0$$

### Równanie Michaelisa-Menten:
$$v = \frac{V_{\max}[S]}{K_M + [S]}$$

gdzie:
- $V_{\max} = k_2[E]_0$ - maksymalna szybkość
- $K_M = \frac{k_{-1} + k_2}{k_1}$ - stała Michaelisa

**Interpretacja $K_M$:** Stężenie substratu przy którym $v = V_{\max}/2$

## 🔗 Powiązane tematy

- [[Równania o zmiennych rozdzielonych]]
- [[Układy liniowe jednorodne]]
- [[Modele wzrostu populacji]]
- [[Równania liniowe pierwszego rzędu]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Kinetyka chemiczna | Chemical kinetics |
| Stała szybkości | Rate constant |
| Rząd reakcji | Order of reaction |
| Czas połowiczego rozpadu | Half-life |
| Energia aktywacji | Activation energy |
| Równanie Arrheniusa | Arrhenius equation |
| Stan quasi-ustalony | Quasi-steady state |
| Reaktor okresowy | Batch reactor |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*