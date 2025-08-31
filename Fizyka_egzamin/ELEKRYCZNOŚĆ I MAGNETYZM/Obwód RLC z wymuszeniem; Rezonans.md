![[rlc.pdf]]


**Obwód RLC z wymuszeniem**

- Obwód RLC to układ elektryczny złożony z rezystora (R), cewki (L) i kondensatora (C) połączonych szeregowo lub równolegle.
- W obwodzie z wymuszeniem analizujemy zachowanie układu, gdy podłączone jest źródło napięcia zmiennego (najczęściej sinusoidalnego).

---

**Równanie różniczkowe obwodu RLC szeregowego**

- Dla napięcia wymuszającego $$ U(t) = U_0 \sin(\omega t) $$, równanie obwodu: $$ U_0 \sin(\omega t) = R I(t) + L \frac{dI(t)}{dt} + \frac{1}{C} \int I(t) dt $$

---

**Impedancja obwodu RLC**

- Impedancja $$ Z $$ to "całkowity opór" dla prądu zmiennego: $$ Z = \sqrt{R^2 + \left( \omega L - \frac{1}{\omega C} \right)^2} $$ gdzie:
    - $$ R $$ – rezystancja (Ω)
    - $$ L $$ – indukcyjność cewki (H)
    - $$ C $$ – pojemność kondensatora (F)
    - $$ \omega $$ – pulsacja (częstość kołowa, $$ \omega = 2\pi f $$)

---

**Natężenie prądu w obwodzie**

- Maksymalne natężenie prądu: $$ I_0 = \frac{U_0}{Z} $$
- Prąd w obwodzie: $$ I(t) = I_0 \sin(\omega t + \varphi) $$ gdzie $$ \varphi $$ to przesunięcie fazowe.

---

**Przesunięcie fazowe**

- Prąd i napięcie nie są w fazie, przesunięcie fazowe: $$ \tan \varphi = \frac{\omega L - \frac{1}{\omega C}}{R} $$

---

**Rezonans w obwodzie RLC**

- Rezonans występuje, gdy $$ \omega L = \frac{1}{\omega C} $$, czyli: $$ \omega_0 = \frac{1}{\sqrt{LC}} $$
- Przy rezonansie impedancja jest minimalna ($$ Z = R $$), a prąd maksymalny.

---

**Podsumowanie najważniejszych wzorów**

- Impedancja: $$ Z = \sqrt{R^2 + \left( \omega L - \frac{1}{\omega C} \right)^2} $$
- Prąd maksymalny: $$ I_0 = \frac{U_0}{Z} $$
- Przesunięcie fazowe: $$ \tan \varphi = \frac{\omega L - \frac{1}{\omega C}}{R} $$
- Częstotliwość rezonansowa: $$ \omega_0 = \frac{1}{\sqrt{LC}} $$

---

**Wskazówki na egzamin**

- Umiej obliczyć impedancję, prąd i przesunięcie fazowe dla podanych wartości.
- Pamiętaj, że przy rezonansie prąd jest największy, a napięcie na cewce i kondensatorze może być dużo większe niż napięcie źródła.
- Zwróć uwagę na jednostki: Ω, H, F, Hz, A, V.