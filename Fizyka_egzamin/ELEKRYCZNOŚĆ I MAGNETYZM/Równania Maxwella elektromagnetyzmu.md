
![[maxwell.pdf]]

**1. Prawo Gaussa dla pola elektrycznego**

- Całkowity strumień pola elektrycznego przez zamkniętą powierzchnię jest proporcjonalny do ładunku wewnątrz tej powierzchni. $$ \oint_{S} \vec{E} \cdot d\vec{S} = \frac{Q_{wew}}{\varepsilon_0} $$ lub w postaci różniczkowej: $$ \nabla \cdot \vec{E} = \frac{\rho}{\varepsilon_0} $$ gdzie:
    - $$ \vec{E} $$ – natężenie pola elektrycznego (V/m)
    - $$ d\vec{S} $$ – element powierzchni (m²)
    - $$ Q_{wew} $$ – ładunek wewnątrz powierzchni (C)
    - $$ \varepsilon_0 $$ – przenikalność elektryczna próżni
    - $$ \rho $$ – gęstość ładunku (C/m³)

---

**2. Prawo Gaussa dla pola magnetycznego**

- Całkowity strumień pola magnetycznego przez zamkniętą powierzchnię jest zawsze równy zero (nie istnieją monopole magnetyczne). $$ \oint_{S} \vec{B} \cdot d\vec{S} = 0 $$ lub w postaci różniczkowej: $$ \nabla \cdot \vec{B} = 0 $$ gdzie:
    - $$ \vec{B} $$ – indukcja magnetyczna (T)

---

**3. Prawo Faradaya (indukcji elektromagnetycznej)**

- Zmiana strumienia magnetycznego przez powierzchnię powoduje powstanie wiru pola elektrycznego (indukuje SEM). $$ \oint_{C} \vec{E} \cdot d\vec{l} = -\frac{d}{dt} \int_{S} \vec{B} \cdot d\vec{S} $$ lub w postaci różniczkowej: $$ \nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t} $$

---

**4. Prawo Ampera-Maxwella**

- Wir pola magnetycznego jest związany z prądem elektrycznym oraz ze zmianą pola elektrycznego w czasie. $$ \oint_{C} \vec{B} \cdot d\vec{l} = \mu_0 I_{wew} + \mu_0 \varepsilon_0 \frac{d}{dt} \int_{S} \vec{E} \cdot d\vec{S} $$ lub w postaci różniczkowej: $$ \nabla \times \vec{B} = \mu_0 \vec{J} + \mu_0 \varepsilon_0 \frac{\partial \vec{E}}{\partial t} $$ gdzie:
    - $$ \vec{J} $$ – gęstość prądu (A/m²)
    - $$ \mu_0 $$ – przenikalność magnetyczna próżni

---

**Podsumowanie najważniejszych wzorów**

1. $$ \nabla \cdot \vec{E} = \frac{\rho}{\varepsilon_0} $$
2. $$ \nabla \cdot \vec{B} = 0 $$
3. $$ \nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t} $$
4. $$ \nabla \times \vec{B} = \mu_0 \vec{J} + \mu_0 \varepsilon_0 \frac{\partial \vec{E}}{\partial t} $$

---

**Wskazówki na egzamin**

- Umiej rozpoznać i opisać fizyczne znaczenie każdego równania.
- Pamiętaj o jednostkach: V/m, T, C, A, m².
- Równania Maxwella opisują powstawanie fal elektromagnetycznych, związek prądu i pola, oraz zachowanie ładunków i pól w przestrzeni.