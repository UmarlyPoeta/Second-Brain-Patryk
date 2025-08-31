# Obwody Szeregowe i Równoległe

## 🔗 Obwody szeregowe

### Definicja
**Obwód szeregowy** to obwód, w którym wszystkie elementy są połączone w jednej "pętli" - prąd ma tylko jedną drogę przepływu.

### Schemat podstawowy
```
+Bat ──┬── R1 ── R2 ── R3 ──┬── -Bat
       │                    │
       ├────── Rtotal ──────┤
```

### Podstawowe prawa

#### Prąd
**Ten sam przez wszystkie elementy**
```
I = I1 = I2 = I3 = ... = In
```

#### Napięcie  
**Suma napięć = napięcie źródła**
```
Utotal = U1 + U2 + U3 + ... + Un
```

#### Opór
**Opory się dodają**
```
Rtotal = R1 + R2 + R3 + ... + Rn
```

### Dzielnik napięcia
```
      R1          U1 = Utotal × R1/(R1+R2)
Uin ──┴───┬──── 
      R2  │      U2 = Utotal × R2/(R1+R2)
      ┴   │
         GND
```

**Wzór ogólny**:
```
Un = Utotal × Rn / Rtotal
```

### Przykład obliczeniowy
**Dane**: Bateria 12V, R1 = 2kΩ, R2 = 3kΩ

```
Rtotal = R1 + R2 = 2kΩ + 3kΩ = 5kΩ
I = U/R = 12V/5kΩ = 2.4mA
U1 = I × R1 = 2.4mA × 2kΩ = 4.8V
U2 = I × R2 = 2.4mA × 3kΩ = 7.2V
Sprawdzenie: U1 + U2 = 4.8V + 7.2V = 12V ✓
```

## ⚡ Obwody równoległe

### Definicja
**Obwód równoległy** to obwód, w którym elementy mają wspólne punkty połączenia - napięcie na wszystkich elementach jest takie samo.

### Schemat podstawowy
```
        R1 ──┐
+Bat ──┬────┬┤
        R2 ──┤├── -Bat
        R3 ──┘
```

### Podstawowe prawa

#### Napięcie
**Takie samo na wszystkich elementach**
```
U = U1 = U2 = U3 = ... = Un
```

#### Prąd
**Suma prądów = prąd całkowity**
```
Itotal = I1 + I2 + I3 + ... + In
```

#### Opór
**Odwrotności się dodają**
```
1/Rtotal = 1/R1 + 1/R2 + 1/R3 + ... + 1/Rn
```

**Dla dwóch rezystorów**:
```
Rtotal = (R1 × R2)/(R1 + R2)
```

### Prąd przez gałęzie
```
In = Utotal / Rn
```
Prąd jest **odwrotnie proporcjonalny** do oporu

### Przykład obliczeniowy
**Dane**: Bateria 12V, R1 = 4kΩ, R2 = 6kΩ

```
1/Rtotal = 1/4kΩ + 1/6kΩ = 3/12kΩ + 2/12kΩ = 5/12kΩ
Rtotal = 12kΩ/5 = 2.4kΩ

lub: Rtotal = (4kΩ × 6kΩ)/(4kΩ + 6kΩ) = 24kΩ/10kΩ = 2.4kΩ

Itotal = 12V/2.4kΩ = 5mA
I1 = 12V/4kΩ = 3mA  
I2 = 12V/6kΩ = 2mA
Sprawdzenie: I1 + I2 = 3mA + 2mA = 5mA ✓
```

## 🔄 Obwody mieszane (szeregowo-równoległe)

### Strategia rozwiązywania
1. **Znajdź** najprostsze połączenia równoległe/szeregowe
2. **Oblicz** opory zastępcze tych fragmentów
3. **Uprość** obwód stopniowo
4. **Oblicz** prądy i napięcia wstecz

### Przykład obwodu mieszanego
```
       R1
+Bat ──┴───┬── R2 ──┐
           │        ├── -Bat
           └── R3 ──┘
```

**Rozwiązanie**:
1. R2 i R3 są równolegle: R23 = (R2×R3)/(R2+R3)
2. R1 i R23 są szeregowo: Rtotal = R1 + R23
3. Prąd główny: I = Ubat/Rtotal
4. Napięcie na R23: U23 = I × R23
5. Prądy przez R2 i R3: I2 = U23/R2, I3 = U23/R3

## ⚡ Charakterystyki specjalne

### Zwarcie (short circuit)
- **Opór = 0Ω**
- **W obwodzie szeregowym**: Całkowity opór = 0Ω, bardzo duży prąd
- **W obwodzie równoległym**: Wszystkie prądy idą przez zwarcie

### Przerwa (open circuit)  
- **Opór = ∞Ω**
- **W obwodzie szeregowym**: Prąd = 0A przez cały obwód
- **W obwodzie równoległym**: Brak wpływu na inne gałęzie

## 🏠 Zastosowania praktyczne

### Oświetlenie domowe (równoległe)
```
230V AC ──┬── Żarówka 1
          ├── Żarówka 2  
          ├── Żarówka 3
          └── Żarówka 4
```
**Zalety**:
- Każda żarówka ma pełne 230V
- Wyłączenie jednej nie wpływa na inne
- Możliwość różnych mocy żarówek

### Lampki choinkowe (szeregowe)
```
230V AC ── LED1 ── LED2 ── ... ── LED50
```
**Cechy**:
- Każda LED dostaje 230V/50 = 4.6V
- Przepalenie jednej = wyłączenie całego łańcucha
- Mała moc każdej diody

### Dzielniki napięcia
**Arduino 5V → 3.3V**:
```
      1kΩ
5V ──┴───┬── 3.3V (do urządzenia 3.3V)
     2kΩ │
     ┴   │
        GND
```

### Ładowanie kondensatorów
**Szeregowe** (dzielenie napięcia):
```
Ładowarka ── C1 ── C2 ── GND
12V        6V   6V
```

**Równoległe** (większa pojemność):
```
        C1 ──┐
12V ──┬────┬┤  Ctotal = C1 + C2
        C2 ──┘
```

## 🧮 Wzory pomocnicze

### Dwa rezystory równolegle
```
R = (R1 × R2)/(R1 + R2)
```

### Dwa identyczne rezystory
- **Szeregowo**: Rtotal = 2R
- **Równolegle**: Rtotal = R/2

### Trzy identyczne rezystory
- **Szeregowo**: Rtotal = 3R  
- **Równolegle**: Rtotal = R/3

### Dzielnik 1:1 (połowa napięcia)
```
R1 = R2  →  Uout = Uin/2
```

### Dzielnik 2:1 (jedna trzecia napięcia)
```
R1 = 2×R2  →  Uout = Uin/3
```

## ⚠️ Częste błędy

### Mylenie połączeń
- **Szeregowe**: Jeden koniec jednego elementu z początkiem drugiego
- **Równoległe**: Wszystkie początki razem, wszystkie końce razem

### Błędne stosowanie wzorów
- **Napięcie**: Dzieli się w szeregowych, identyczne w równoległych
- **Prąd**: Identyczny w szeregowych, dzieli się w równoległych
- **Opór**: Dodaje się w szeregowych, odwrotności w równoległych

### Pomijanie wpływu na inne elementy
- Dodanie/usunięcie elementu równoległego zmienia prądy
- Zmiana jednego elementu szeregowego wpływa na cały obwód

## 🧮 Ćwiczenia praktyczne

### Ćwiczenie 1: Dzielnik napięcia
Zaprojektuj dzielnik 12V → 5V przy obciążeniu 10mA.

### Ćwiczenie 2: Obwód mieszany
```
       2kΩ
12V ──┴───┬── 3kΩ ──┐
          │         ├── GND
          └── 6kΩ ──┘
```
Oblicz wszystkie prądy i napięcia.

### Ćwiczenie 3: Optymalizacja mocy
Jakie połączenie dwóch rezystorów 100Ω/1W pozwoli na największą moc całkowitą?

## 📚 Powiązane tematy

- [[prawo_ohma|Prawo Ohma]]
- [[napiecie_prad_opor|Napięcie, Prąd i Opór]]
- [[rezystory|Rezystory]]
- [[kondensatory|Kondensatory - Połączenia]]
- [[moc_elektryczna|Moc Elektryczna]]
- [[multimetr|Multimetr - Pomiary w Obwodach]]

---

#elektronika #obwody #szeregowe #równoległe #dzielnik-napięcia #prawo-ohma