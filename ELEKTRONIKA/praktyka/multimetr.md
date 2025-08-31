# Multimetr - Podstawy Obsługi

## 📏 Definicja

**Multimetr** (multimeter, DMM - Digital Multimeter) to uniwersalny przyrząd pomiarowy służący do pomiaru podstawowych wielkości elektrycznych: napięcia, prądu i oporu.

## 🔧 Budowa multimetru

### Wyświetlacz
- **Cyfrowy**: LCD/LED z dokładnością 3-6 cyfr
- **Analogowy**: Wskazówkowy (rzadkie współcześnie)
- **Funkcje dodatkowe**: Podświetlenie, bargraf, hold

### Przełącznik zakresów/funkcji
- **Obrotowy**: Najczęściej spotykany
- **Przyciski**: W multimetrach zaawansowanych
- **Autorange**: Automatyczny wybór zakresu

### Gniazda pomiarowe
- **COM** (Common) - masa, reference, "-"
- **VΩmA** - napięcie, opór, prąd do ~200mA
- **10A** lub **20A** - duże prądy (czasem osobne gniazdo)

### Sondy pomiarowe
- **Czerwona** → VΩmA lub A (dodatni potencjał)
- **Czarna** → COM (masa, ujemny potencjał)

## ⚡ Pomiar napięcia (V)

### Przygotowanie
1. **Połączenie sond**: Czerwona do VΩmA, czarna do COM
2. **Wybór funkcji**: DC V (⎓) lub AC V (~)
3. **Wybór zakresu**: Większy niż spodziewane napięcie

### Technika pomiaru
```
    + ────┬──── -
          │     ↗ Obwód
          V
          ↓ Multimetr
         COM
```
- **Równolegle** do mierzonego elementu
- **DC**: Czerwona do +, czarna do -
- **AC**: Polaryzacja bez znaczenia

### Przykłady praktyczne
- **Bateria AA**: 1.5V DC
- **Akumulator samochodowy**: 12V DC  
- **Gniazdko domowe**: 230V AC ⚠️
- **Zasilacz komputera**: 5V, 12V DC

### Bezpieczeństwo przy pomiarze napięcia
- **Sprawdź kategorię CAT** multimetru
- **230V wymaga CAT II** minimum
- **Nie dotykaj** końcówek sond
- **Zaczynaj od najwyższego zakresu**

## 🔄 Pomiar prądu (A)

### Przygotowanie
1. **Wybór gniazda**: 
   - mA dla prądów < 200mA
   - A dla prądów > 200mA (do 10-20A)
2. **Wybór funkcji**: DC A (⎓) lub AC A (~)
3. **Wybór zakresu**: Większy niż spodziewany prąd

### Technika pomiaru
```
+Bat ──┬── R ──┬── -Bat
       │       │
       └── A ──┘
       Multimetr szeregowo
```
- **Szeregowo** z obwodem (przerywamy obwód!)
- **Prąd płynie** przez multimetr
- **Duży prąd** - uwaga na bezpiecznik!

### Praktyczne przykłady
- **LED**: 20mA → gniazdo mA
- **Żarówka 60W/12V**: 5A → gniazdo A
- **Akumulator podczas ładowania**: 0.5-2A

### ⚠️ Częste błędy
- **Pomiar równolegle** zamiast szeregowo → przepalony bezpiecznik
- **Za mały zakres** → przepalony bezpiecznik  
- **Zapomnienie o przełączeniu** z A na V → zwarcie

## 🚫 Pomiar oporu (Ω)

### Przygotowanie  
1. **Połączenie sond**: Czerwona do VΩmA, czarna do COM
2. **Wybór funkcji**: Ω (ohm)
3. **ODŁĄCZ zasilanie** z mierzonego obwodu!

### Technika pomiaru
```
    ┌─── Element ───┐
    │               │
   RED             BLK
    │               │
    └── Multimetr ──┘
```
- **Równolegle** do mierzonego elementu
- **BEZ ZASILANIA** w obwodzie
- Element może być w obwodzie (inne elementy wpłyną na pomiar)

### Interpretacja wyników
- **0Ω lub bardzo mało**: Zwarcie, przewód
- **OL (Over Limit)**: Przerwa, bardzo duży opór
- **Wartość nominalna**: Sprawność elementu

### Przykłady praktyczne
- **Przewód**: Powinien być ~0Ω
- **Rezystor 1kΩ**: 950Ω-1050Ω (tolerancja ±5%)
- **Dioda w kierunku prostym**: 0.7V (nie opór!)
- **Kondensator**: Chwilowo niski opór, potem OL

## 🔍 Dodatkowe funkcje

### Test diodowy (⊐►|)
- **Wyświetla napięcie przewodzenia** (~0.7V dla diod krzemowych)
- **Kierunek prosty**: 0.6-0.8V
- **Kierunek wsteczny**: OL
- **Zwarcie**: ~0V
- **Przerwa**: OL w obydwu kierunkach

### Test ciągłości (♪)
- **Sygnał dźwiękowy** przy niskim oporze
- **Próg**: Zazwyczaj 30-50Ω
- **Zastosowanie**: Sprawdzanie przewodów, połączeń
- **Szybsze** niż odczytywanie wartości oporu

### Pomiar pojemności (┤├)
- **Zakres**: Od pF do mF
- **Element musi być rozładowany!**
- **Dokładność**: Zazwyczaj ±2-5%
- **Ograniczenia**: Kondensatory w obwodzie, kondensatory elektrolityczne

### Pomiar częstotliwości (Hz)
- **Sygnały cyfrowe**: Impulsów, prostokątne
- **Zakres**: 10Hz - 10MHz (typowo)
- **Zastosowanie**: Sprawdzanie oscylatorów, generatorów

### Pomiar temperatury (°C)
- **Termopara typu K** (dodatkowa sonda)
- **Zakres**: -40°C do +400°C (typowo)  
- **Dokładność**: ±2-5°C
- **Zastosowanie**: Monitoring temperatury elementów

## 📊 Specyfikacje i dokładność

### Dokładność podstawowa
- **Tanie multimetry**: ±0.5% - ±3%
- **Średnie multimetry**: ±0.1% - ±0.5%  
- **Profesjonalne**: ±0.025% - ±0.1%

### Rozdzielczość
- **3½ cyfry**: 0-1999 (2000 jednostek)
- **4½ cyfry**: 0-19999 (20000 jednostek)
- **6½ cyfr**: 0-1999999 (precyzyjne)

### Kategorie pomiarowe (CAT)
- **CAT I**: Elektronika niskonapięciowa
- **CAT II**: Instalacje domowe (230V)
- **CAT III**: Rozdzielnice, silniki przemysłowe  
- **CAT IV**: Linie napowietrzne, wejścia budynków

## 🛠️ Konserwacja i kalibracja

### Konserwacja rutynowa
- **Czyść** regularnie obudowę i sondy
- **Sprawdzaj** baterie (słaby wskaźnik)
- **Przechowuj** w etui, chroń przed upadkiem
- **Wymieniaj** bezpieczniki po przepaleniu

### Kalibracja
- **Sprawdzanie dokładności** znanymi źródłami
- **Częstotliwość**: Raz w roku (użytkowanie profesjonalne)
- **Źródła wzorcowe**: 1.5V bateria, rezystor precyzyjny
- **Serwis kalibracyjny**: Dla pomiarów wymagających wysokiej dokładności

### Wymienna bezpieczników
- **Lokalizacja**: Zazwyczaj na tylnej ściance
- **Typ**: Szybki (F), ceramiczny
- **Wartości**: 200mA, 10A (sprawdź dokumentację!)
- **Wymiana**: **TYLKO** identyczne parametry

## ⚠️ Bezpieczeństwo i błędy

### Najczęstsze błędy początkujących
1. **Pomiar prądu równolegle** → przepalony bezpiecznik
2. **Nieprzełączenie z A na V** → zwarcie przy następnym pomiarze
3. **Pomiar oporu przy zasilaniu** → nieprawdiwy wynik lub uszkodzenie
4. **Przekroczenie zakresu napięciowego** → uszkodzenie multimetru

### Zasady bezpieczeństwa
- **Sprawdź kategorię CAT** przed pomiarem wysokich napięć
- **Zaczynaj od najwyższego zakresu** i schodź w dół
- **Nigdy nie mierz** oporu w obwodzie pod napięciem
- **Rozładuj kondensatory** przed pomiarem pojemności
- **Nie przekraczaj** maksymalnych wartości

## 🧮 Ćwiczenia praktyczne

### Ćwiczenie 1: Pomiar baterii
1. Zmierz napięcie baterii AA
2. Podłącz rezystor 100Ω i zmierz napięcie ponownie
3. Oblicz prąd i opór wewnętrzny baterii

### Ćwiczenie 2: Prawo Ohma
1. Zbuduj obwód: bateria 9V + rezystor 1kΩ
2. Zmierz napięcie na rezystorze
3. Zmierz prąd przez rezystor
4. Sprawdź prawo Ohma: U = I × R

### Ćwiczenie 3: Dzielnik napięcia
1. Połącz dwa rezystory 1kΩ szeregowo z baterią 9V
2. Zmierz napięcie na każdym rezystorze
3. Sprawdź czy napięcia się sumują

## 📚 Powiązane tematy

- [[prawo_ohma|Prawo Ohma]]
- [[napiecie_prad_opor|Napięcie, Prąd i Opór]]
- [[bezpieczenstwo_elektryczne|Bezpieczeństwo Elektryczne]]
- [[rezystory|Rezystory - Pomiar]]
- [[diody|Diody - Test Multimetrem]]
- [[lutowanie|Lutowanie - Kontrola Połączeń]]

---

#multimetr #pomiary #DMM #napięcie #prąd #opór #elektronika #narzędzia