# Twierdzenie Picarda-Lindelöfa (twierdzenie o istnieniu i jednoznaczności)

**Opis:**  
Twierdzenie Picarda mówi, kiedy problem Cauchy’ego dla równania różniczkowego ma dokładnie jedno rozwiązanie w pewnym otoczeniu punktu początkowego.

**Problem Cauchy’ego:** $$ y'(x) = f(x, y(x)), \quad y(x_0) = y_0 $$

**Warunki:**

- Funkcja $$ f(x, y) $$ jest ciągła w pewnym prostokącie $$ D $$ zawierającym punkt $$ (x_0, y_0) $$
- Funkcja $$ f(x, y) $$ spełnia warunek Lipschitza względem $$ y $$, tzn. istnieje stała $$ L > 0 $$ taka, że dla wszystkich $$ (x, y_1), (x, y_2) \in D $$ $$ |f(x, y_1) - f(x, y_2)| \leq L |y_1 - y_2| $$

**Wniosek:**

- Wtedy istnieje dokładnie jedno rozwiązanie $$ y(x) $$ tego problemu w pewnym otoczeniu $$ x_0 $$.

**Co to znaczy?**

- Jeśli $$ f $$ jest "ładna" (ciągła i nie zmienia się zbyt gwałtownie względem $$ y $$), to rozwiązanie jest **jednoznaczne** i **istnieje**.

---

# Twierdzenie Peano (twierdzenie o istnieniu)

**Opis:**  
Twierdzenie Peano mówi, że do istnienia rozwiązania wystarczy tylko ciągłość funkcji $$ f(x, y) $$, ale nie gwarantuje jednoznaczności.

**Problem Cauchy’ego:** $$ y'(x) = f(x, y(x)), \quad y(x_0) = y_0 $$

**Warunki:**

- Funkcja $$ f(x, y) $$ jest ciągła w pewnym prostokącie $$ D $$ zawierającym punkt $$ (x_0, y_0) $$

**Wniosek:**

- Wtedy **istnieje przynajmniej jedno rozwiązanie** $$ y(x) $$ tego problemu w pewnym otoczeniu $$ x_0 $$.

**Co to znaczy?**

- Jeśli $$ f $$ jest tylko ciągła, to rozwiązanie **na pewno istnieje**, ale może być ich więcej niż jedno (brak gwarancji jednoznaczności).

---

# Podsumowanie różnic

- **Picard:** istnienie **i jednoznaczność** (ciągłość + warunek Lipschitza)
- **Peano:** tylko istnienie (ciągłość)

---

# Przykład

1. $$ y'(x) = y(x), \quad y(0) = 1 $$
    
    - $$ f(x, y) = y $$
    - Ciągła i spełnia warunek Lipschitza
    - Rozwiązanie: $$ y(x) = e^x $$
    - Jedno rozwiązanie (Picard)
2. $$ y'(x) = \sqrt{|y(x)|}, \quad y(0) = 0 $$
    
    - $$ f(x, y) = \sqrt{|y|} $$
    - Ciągła, ale nie spełnia warunku Lipschitza w $$ y = 0 $$
    - Istnieje wiele rozwiązań (Peano, ale nie Picard)

---

# Wskazówki na egzamin

- Jeśli $$ f $$ jest ciągła i spełnia warunek Lipschitza względem $$ y $$ → jedno rozwiązanie (Picard)
- Jeśli $$ f $$ jest tylko ciągła → przynajmniej jedno rozwiązanie (Peano)
- Warunek Lipschitza to "ograniczona szybkość zmiany" względem $$ y $$

---

**Zapamiętaj:**  
Picard = istnienie + jednoznaczność  
Peano = istnienie

To podstawa teorii równań różniczkowych!