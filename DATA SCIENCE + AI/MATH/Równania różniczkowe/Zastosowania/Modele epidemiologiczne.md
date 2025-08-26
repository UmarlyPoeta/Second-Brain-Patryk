# Modele epidemiologiczne

## 🦠 Wprowadzenie

**Modele epidemiologiczne** używają równań różniczkowych do opisania rozprzestrzeniania się chorób w populacji. Są kluczowe w:
- **Zdrowiu publicznym** - prognozowanie epidemii
- **Polityce sanitarnej** - planowanie szczepień
- **Medycynie** - ocena skuteczności terapii
- **Zarządzaniu kryzysowym** - reakcja na pandemie

## 🏥 Model SIR - podstawowy

### Podział populacji:
- **S(t)** - Susceptible (podatni na zachorowanie)
- **I(t)** - Infected (zarażeni, zakaźni)  
- **R(t)** - Recovered/Removed (ozdrowiali/usunięci z populacji)

### Założenia:
- Populacja stała: $N = S + I + R = \text{const}$
- Jednorodne mieszanie populacji
- Brak urodzin i zgonów (krótki okres)
- Odporność po przejściu choroby

### Układ równań SIR:
$$\begin{cases}
\frac{dS}{dt} = -\beta SI \\
\frac{dI}{dt} = \beta SI - \gamma I \\
\frac{dR}{dt} = \gamma I
\end{cases}$$

### Parametry:
- $\beta$ - **stopa transmisji** (prawdopodobieństwo zarażenia na kontakt × liczba kontaktów)
- $\gamma$ - **stopa wyzdrowienia** (= 1/czas infekcyjności)
- $R_0 = \frac{\beta S_0}{\gamma}$ - **podstawowa liczba reprodukcji**

## 📊 Analiza modelu SIR

### Punkt równowagi:
Jedyny punkt równowagi: $(S^*, I^*, R^*) = (S_{\infty}, 0, R_{\infty})$

### Zachowanie rozwiązań:
1. **$R_0 < 1$:** Epidemia nie wystąpi (I(t) maleje)
2. **$R_0 > 1$:** Epidemia wystąpi (I(t) najpierw rośnie)
3. **$R_0 = 1$:** Próg epidemiczny

### Maksimum infekcji:
**Warunek:** $\frac{dI}{dt} = 0 \Rightarrow \beta SI = \gamma I$

Przy $I > 0$: $S = \frac{\gamma}{\beta} = \frac{S_0}{R_0}$

**Czas maksimum:** Gdy liczba podatnych spadnie do $S_0/R_0$

### Wielkość końcowa epidemii:
**Całka pierwsza:** $S + I + R = N$ i $R - R_0 + \ln(S/S_0) = 0$

**Równanie na $S_{\infty}$:**
$$S_{\infty} = S_0 e^{-R_0(1 - S_{\infty}/S_0)}$$

**Frakcja zarażonych:** $R_{\infty}/N = 1 - S_{\infty}/N$

## 🔄 Rozszerzenia modelu SIR

### Model SIRS (z utratą odporności):
$$\begin{cases}
\frac{dS}{dt} = -\beta SI + \delta R \\
\frac{dI}{dt} = \beta SI - \gamma I \\
\frac{dR}{dt} = \gamma I - \delta R
\end{cases}$$

gdzie $\delta$ - stopa utraty odporności.

### Model SEIR (z okresem inkubacji):
- **E(t)** - Exposed (zarażeni, niezakaźni)

$$\begin{cases}
\frac{dS}{dt} = -\beta SI \\
\frac{dE}{dt} = \beta SI - \sigma E \\
\frac{dI}{dt} = \sigma E - \gamma I \\
\frac{dR}{dt} = \gamma I
\end{cases}$$

gdzie $\sigma$ - stopa przechodzenia z okresu inkubacji do zakaźności.

### Model SIS (bez odporności):
$$\begin{cases}
\frac{dS}{dt} = -\beta SI + \gamma I \\
\frac{dI}{dt} = \beta SI - \gamma I
\end{cases}$$

**Punkt równowagi endemicznej:**
- $I^* = \frac{N(\beta - \gamma)}{\beta}$ gdy $R_0 > 1$
- $I^* = 0$ gdy $R_0 \leq 1$

## 💉 Model z wakcynacją

### Vaccynacja ciągła (SIR + V):
$$\begin{cases}
\frac{dS}{dt} = -\beta SI - \nu S \\
\frac{dI}{dt} = \beta SI - \gamma I \\
\frac{dR}{dt} = \gamma I \\
\frac{dV}{dt} = \nu S
\end{cases}$$

gdzie $\nu$ - stopa wakcynacji.

### Próg wakcynacji:
Aby zapobiec epidemii: $R_0(1 - p) < 1$

**Minimalna pokrycie wakcynacyjne:**
$$p_c = 1 - \frac{1}{R_0}$$

## 📝 Przykład liczbowy - COVID-19

### Dane szacunkowe:
- $R_0 \approx 2.5$ (bez interwencji)
- Średni czas infekcyjności: 10 dni → $\gamma = 0.1$ dzień⁻¹
- $\beta = R_0 \cdot \gamma / S_0 \approx 2.5 \times 0.1 = 0.25$ (w pełni podatnej populacji)

### Przewidywania:
1. **Bez interwencji:** $R_{\infty} \approx 0.89N$ (89% populacji zarazi się)
2. **Próg wakcynacji:** $p_c = 1 - 1/2.5 = 0.6$ (60% populacji)
3. **Czas podwojenia** (na początku): $t_2 \approx \frac{\ln 2}{(\beta S_0 - \gamma)} \approx 3$ dni

## 🌍 Modele przestrzenne

### Model metapopulacyjny:
Populacja podzielona na podgrupy z migracją między nimi:

$$\frac{dI_i}{dt} = \beta_i S_i I_i - \gamma_i I_i + \sum_{j \neq i} m_{ji}I_j - I_i\sum_{j \neq i} m_{ij}$$

gdzie $m_{ij}$ - stopa migracji z regionu i do j.

### Model sieciowy:
Kontakty modelowane jako graf:
- Węzły = osoby
- Krawędzie = możliwe kontakty

**Równanie dla węzła i:**
$$\frac{dI_i}{dt} = \beta S_i \sum_{j \in \text{sąsiedzi}} A_{ij} I_j - \gamma I_i$$

## 🏥 Modele z demografią

### Urodziny i zgony:
$$\begin{cases}
\frac{dS}{dt} = \mu N - \beta SI - \mu S \\
\frac{dI}{dt} = \beta SI - \gamma I - \mu I \\
\frac{dR}{dt} = \gamma I - \mu R
\end{cases}$$

gdzie $\mu$ - stopa urodzeń/zgonów.

**Stan endemiczny:**
$$I^* = \frac{\mu(R_0 - 1)}{\beta}, \quad S^* = \frac{\mu + \gamma}{\beta}, \quad R^* = \frac{\gamma I^*}{\mu}$$

## 📊 Estymacja parametrów

### Z danych epidemiologicznych:
1. **Na początku epidemii:** $I(t) \approx I_0 e^{(\beta S_0 - \gamma)t}$
   - Tempo wzrostu → $r = \beta S_0 - \gamma$

2. **Ze szczytowego okresu:**
   - Maksimum I(t) → związane z $R_0$

3. **Z końcowej wielkości:**
   - $R_{\infty}$ → równanie na $S_{\infty}$

### Metoda najmniejszych kwadratów:
Minimalizacja: $\sum_i (I_{\text{dane}}(t_i) - I_{\text{model}}(t_i))^2$

## 🧮 Symulacje numeryczne

### Implementacja RK4 dla SIR:
```python
def sir_model(t, y, beta, gamma):
    S, I, R = y
    N = S + I + R
    
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    
    return [dS, dI, dR]

# Rozwiązanie numeryczne
from scipy.integrate import solve_ivp

sol = solve_ivp(sir_model, [0, 365], [S0, I0, R0], 
                args=(beta, gamma), dense_output=True)
```

## 📈 Wskaźniki epidemiologiczne

### Podstawowe liczby reprodukcji:
- **$R_0$** - w pełni podatnej populacji
- **$R_e$** - efektywna (w częściowo odpornej populacji)
- **$R_t$** - chwilowa (z interwencjami)

### Inne wskaźniki:
- **Atak rate:** $R_{\infty}/N$ (frakcja zarażonych)
- **Czas podwojenia:** na początku epidemii
- **Szczyt epidemii:** maksymalna liczba zakażeń dziennie

## ⚠️ Ograniczenia modeli

### Założenia często nierealistyczne:
1. **Jednorodne mieszanie** - w rzeczywistości struktura sieci kontaktów
2. **Stałe parametry** - zmieniają się z interwencjami
3. **Populacja zamknięta** - migracja i zmiany demograficzne
4. **Odporność trwała** - może zanikać w czasie

### Niepewność parametrów:
- Trudność pomiaru $\beta, \gamma$
- Zmiany w zachowaniach społecznych
- Mutacje patogena

## 🔗 Powiązane tematy

- [[Modele wzrostu populacji]]
- [[Układy liniowe jednorodne]]
- [[Stabilność rozwiązań układów]]
- [[Metody numeryczne]]
- [[Dynamika predator-ofiara]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Model epidemiologiczny | Epidemiological model |
| Podstawowa liczba reprodukcji | Basic reproduction number |
| Stopa transmisji | Transmission rate |
| Próg epidemiczny | Epidemic threshold |
| Odporność zbiorowiska | Herd immunity |
| Okres inkubacji | Incubation period |
| Model metapopulacyjny | Metapopulation model |

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*