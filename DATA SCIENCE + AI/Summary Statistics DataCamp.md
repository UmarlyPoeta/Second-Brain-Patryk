## 📊 Summary Statistics – Chapter 1

_Introduction to Statistics in Python_

**Powiązane notatki:**

- [[Random Numbers and Probability]]
    
- [[Summary Statistics DataCamp]]
    

---

### 📝 Zakres materiału

W tym rozdziale poznałeś podstawowe pojęcia **statystyk opisowych** dotyczące **miar tendencji centralnej**:

1. **Mean (średnia arytmetyczna)**
    
    - Wzór: suma wartości / liczba obserwacji
        
    - Python: `np.mean(data)`
        
    - **Wrażliwa na wartości odstające**
        
2. **Median (mediana)**
    
    - Wartość środkowa po posortowaniu danych
        
    - Przy parzystej liczbie obserwacji: średnia z dwóch środkowych wartości
        
    - Python: `np.median(data)`
        
    - **Odporniejsza na dane odstające**
        
3. **Mode (dominanta)**
    
    - Najczęściej występująca wartość
        
    - Szczególnie przydatna dla danych kategorycznych
        
    - Python: `statistics.mode(data)`
        

---

### ⚖️ Wpływ rozkładu danych

- **Rozkład skośny** → średnia przesuwa się w stronę ogona rozkładu
    
- **Mediana** jest stabilniejszym miernikiem w przypadku danych z wartościami odstającymi
    

---

### 💻 Ćwiczenia praktyczne

- Biblioteki: `pandas`, `numpy`
    
- Dane: konsumpcja żywności + ślad węglowy
    
- Cel: zastosowanie miar tendencji centralnej w analizie rzeczywistych zbiorów danych
    

---

### 🎯 Następny krok

Poznasz **miary rozproszenia**:

- Wariancja
    
- Odchylenie standardowe
    
- Wykrywanie wartości odstających
    
- Praktyczne przykłady w analizie danych