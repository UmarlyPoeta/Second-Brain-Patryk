![[rc_obwod.pdf]]

**Obwód RC – notatki na egzamin z fizyki**

---

**Obwód RC**  
Obwód RC to układ elektryczny złożony z rezystora (R) i kondensatora (C) połączonych szeregowo lub równolegle. Najczęściej analizuje się obwód szeregowy RC, w którym rezystor i kondensator są połączone jeden za drugim.

---

**Zachowanie obwodu RC przy ładowaniu kondensatora**  
Gdy podłączymy źródło napięcia do obwodu RC, kondensator zaczyna się ładować. Prąd w obwodzie oraz napięcie na kondensatorze zmieniają się w czasie.

- Napięcie na kondensatorze podczas ładowania: 
Uc(t) = U0 (1 – e^(–t/RC)) 
- gdzie Uc(t) to napięcie na kondensatorze w chwili t, U0 to napięcie źródła, e to liczba Eulera.
    
- Prąd w obwodzie podczas ładowania: I(t) = (U0/R) · e^(–t/RC) gdzie I(t) to prąd w chwili t.
    

---

**Zachowanie obwodu RC przy rozładowywaniu kondensatora**  
Gdy kondensator jest naładowany i odłączymy źródło napięcia, kondensator zaczyna się rozładowywać przez rezystor.

- Napięcie na kondensatorze podczas rozładowania: Uc(t) = U0 · e^(–t/RC)
    
- Prąd w obwodzie podczas rozładowania: I(t) = –(U0/R) · e^(–t/RC)
    

---

**Stała czasowa obwodu RC (τ)**  
Stała czasowa obwodu RC oznaczana jest jako τ (tau) i wyraża się wzorem: τ = R · C gdzie R to opór rezystora, C to pojemność kondensatora.

- Stała czasowa τ określa, jak szybko kondensator ładuje się lub rozładowuje.
- Po czasie równym τ napięcie na kondensatorze podczas ładowania osiąga około 63% wartości końcowej, a podczas rozładowania spada do około 37% wartości początkowej.
- Po czasie około 5τ kondensator jest praktycznie całkowicie naładowany lub rozładowany.

---

**Podsumowanie najważniejszych wzorów**

- τ = R · C
- Uc(t) = U0 (1 – e^(–t/RC)) – ładowanie
- Uc(t) = U0 · e^(–t/RC) – rozładowanie
- I(t) = (U0/R) · e^(–t/RC) – prąd przy ładowaniu
- I(t) = –(U0/R) · e^(–t/RC) – prąd przy rozładowaniu

---

**Zastosowania obwodu RC**

- Filtry sygnałów (np. filtr dolnoprzepustowy)
- Układy czasowe (np. generatory, opóźnienia)
- Kształtowanie przebiegów napięcia i prądu

---

**Wskazówki na egzamin**

- Zwróć uwagę na jednostki: R w omach (Ω), C w faradach (F), τ w sekundach (s).
- Umiej wyprowadzić wzory i obliczyć napięcie, prąd oraz stałą czasową dla podanych wartości.
- Pamiętaj, że proces ładowania i rozładowania kondensatora jest wykładniczy, a nie liniowy.