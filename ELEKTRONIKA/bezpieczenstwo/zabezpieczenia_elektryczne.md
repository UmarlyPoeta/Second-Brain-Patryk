# Zabezpieczenia Elektryczne

## ⚡ Wprowadzenie

**Zabezpieczenia elektryczne** to systemy i urządzenia mające na celu ochronę instalacji elektrycznych, urządzeń i ludzi przed skutkami awarii elektrycznych takich jak zwarcia, przeciążenia i przepięcia.

## 🔧 Zabezpieczenia nadprądowe

### Bezpieczniki topikowe

#### Zasada działania
- **Element topliwy**: Drut lub blaszka z metalu o niskiej temperaturze topnienia
- **Przy przeciążeniu**: Element się topi i przerywa obwód
- **Jednorazowe**: Po zadziałaniu trzeba wymienić

#### Charakterystyki czasowo-prądowe
```
Czas [s]
   ↑
1000├─────╲
  100├──────╲ Wolne (gL/gG)
   10├───────╲
    1├────────╲
  0.1├─────────╲── Szybkie (aM)
 0.01├──────────╲
    └─┬──┬──┬──┬─→ Prąd/In
      1  2  5  10
```

#### Rodzaje bezpieczników

##### Charakterystyka gG/gL (wolne)
- **Zastosowanie**: Ochrona przewodów, odbiorniki ohmiczne
- **Czas zadziałania**: Długi przy małych przeciążeniach
- **Przykłady**: Oświetlenie, gniazdka, grzejniki

##### Charakterystyka aM (szybkie)
- **Zastosowanie**: Ochrona silników, półprzewodników
- **Prąd rozruchowy**: Wytrzymują krótkotrwałe przeciążenia
- **Zadziałanie**: Szybkie przy dużych prądach zwarciowych

##### Charakterystyka gR (ultra-szybkie)
- **Zastosowanie**: Półprzewodniki (tyrystory, diody)
- **Czas**: < 10ms przy dużych prądach
- **Napięcie**: Do 1000V AC/DC

#### Rozmiary standardowe
- **D01** (10×38): 2A-25A, 400V/500V
- **D02** (22×58): 16A-80A, 400V/500V  
- **NH00** (69×108): 50A-160A, 500V
- **NH1** (78×125): 80A-200A, 500V

### Wyłączniki nadprądowe (MCB)

#### Zasada działania
- **Element bimetaliczny**: Przeciążenia (I = 1.1-1.45 × In)
- **Wyzwalacz elektromagnetyczny**: Zwarcia (I > 5-20 × In)
- **Wielokrotność**: Można resetować po zadziałaniu

#### Charakterystyki wyzwalania

##### Typ B (domowe)
```
Wyzwalacz magnetyczny: 3-5 × In
Zastosowanie: Instalacje mieszkalne
Przykład: Oświetlenie, gniazdka domowe
```

##### Typ C (uniwersalne)
```
Wyzwalacz magnetyczny: 5-10 × In  
Zastosowanie: Instalacje mieszane
Przykład: Oświetlenie biurowe, gniazdka
```

##### Typ D (indukcyjne)
```
Wyzwalacz magnetyczny: 10-20 × In
Zastosowanie: Odbiorniki indukcyjne  
Przykład: Transformatory, silniki
```

#### Klasy wyłączalności
- **Klasa 1**: 1.5kA (instalacje domowe)
- **Klasa 2**: 3kA (budynki mieszkalne)
- **Klasa 3**: 4.5kA-6kA (budynki biurowe)
- **Klasa 4**: 10kA+ (przemysł)

## ⚡ Zabezpieczenia różnicowoprądowe (RCD)

### Zasada działania
```
   L ──→ IL
      ┌───┐
      │ T │ ← Transformator różnicowy
      └───┘
   N ←── IN

Gdy IL ≠ IN → prąd różnicowy → wyzwalacz
```

### Prądy znamionowe różnicowe (IΔn)
- **10 mA**: Ochrona specjalna (łazienki, dzieci)
- **30 mA**: Ochrona przeciwporażeniowa (standardowa)
- **100 mA**: Ochrona przeciwpożarowa
- **300 mA**: Ochrona mienia, selektywność

### Typy RCD według rodzaju prądu

#### Typ AC
- **Prądy**: Tylko sinusoidalne AC
- **Zastosowanie**: Podstawowe, tanie
- **Ograniczenia**: Nie wykrywa prądów DC

#### Typ A  
- **Prądy**: AC + pulsujące DC
- **Zastosowanie**: Pralki, ściemniacze, UPS
- **Standard**: Wymagany w nowoczesnych instalacjach

#### Typ B
- **Prądy**: AC + DC + złożone kształty
- **Zastosowanie**: Falowniki, ładowarki EV, zasilacze impulsowe
- **Koszt**: Najdroższe

#### Typ F
- **Prądy**: Jak typ A + wysokie częstotliwości
- **Zastosowanie**: Falowniki jednofazowe
- **Alternatywa**: Dla typu B w niektórych przypadkach

### Wyłączniki różnicowoprądowe z nadprądem (RCBO)
```
RCD + MCB w jednej obudowie
Zalety: Oszczędność miejsca, selektywność
Wady: Droższe, trudniejsza diagnostyka
```

## ⚠️ Zabezpieczenia przepięciowe (SPD)

### Klasy SPD

#### Klasa I (T1) - grubeochronne
- **Lokalizacja**: Złącze budynku, rozdzielnica główna
- **Prąd udarowy**: 25kA-100kA (10/350μs)
- **Zagrożenie**: Bezpośrednie uderzenie pioruna
- **Technologia**: Iskiernik, gazowy

#### Klasa II (T2) - podstawowe  
- **Lokalizacja**: Rozdzielnice podrzędne, tablice mieszkań
- **Prąd udarowy**: 5kA-40kA (8/20μs)
- **Zagrożenie**: Przepięcia indukowane, przełączeniowe
- **Technologia**: Warystor (MOV), dioda lawiny

#### Klasa III (T3) - dokładne
- **Lokalizacja**: Przy urządzeniach wrażliwych
- **Prąd udarowy**: < 5kA (8/20μs)  
- **Zagrożenie**: Pozostałe przepięcia
- **Technologia**: Diody Zenera, gas discharge tube

### Napięcie zadziałania (Up)
```
Napięcie sieciowe → Up maksymalne
230V → 1.5kV
400V → 2.5kV  
```

### Schemat połączenia
```
L1 ──┬─── SPD ───┬─── Instalacja
L2 ──┼─── SPD ───┤
L3 ──┼─── SPD ───┤
N  ──┼─── SPD ───┤
PE ──┴───────────┘
```

## 🔧 Zabezpieczenia silników

### Wyłączniki silnikowe (motor circuit breaker)
- **Zakres**: 0.1A-80A (regulowany)
- **Funkcje**: Nadprąd + brak fazy + niezrównoważenie
- **Typ**: Magnetotermiczne
- **Reset**: Ręczny lub automatyczny

### Przekaźniki termiczne
```
Schemat:
L1 ──[T1]── Silnik
L2 ──[T2]── 
L3 ──[T3]──

T1,T2,T3 - elementy bimetaliczne
Przy asymetrii lub przeciążeniu → rozwarcie styku pomocniczego
```

### Zabezpieczenia fazowe
- **Monitor faz**: Wykrywa brak fazy, kolejność, asymetrię
- **Przekaźnik**: Wyłącza stycznik silnika
- **Parametry**: Asymetria >15%, napięcie <85%

### Transformatory prądowe (CT)
```
Pierwotny: 100A/1000A (przewód silowy)
Wtórny: 5A/1A → przekaźniki zabezpieczeniowe

Przekładnia: np. 100/5 = 20:1
```

## 🏠 Dobór zabezpieczeń

### Obliczanie prądów

#### Prąd obliczeniowy (Ib)
```
Jednofazowy: Ib = P / (U × cos φ)
Trójfazowy: Ib = P / (√3 × U × cos φ)
```

#### Prąd znamionowy zabezpieczenia (In)
```
Warunek: Ib ≤ In ≤ Iz

gdzie Iz - obciążalność przewodu
```

#### Sprawdzenie selektywności
```
In(niższy) < In(wyższy) × 0.4
```
**Przykład**: MCB 16A + MCB 32A = OK (16 < 32×0.4=12.8) ❌
Poprawnie: MCB 16A + MCB 50A = OK (16 < 50×0.4=20) ✅

### Koordynacja zabezpieczeń

#### Selektywność prądowa
```
    50A ──┬── 32A ──┬── 16A ── Odbiornik
          │         │
       Awaria      │
     tu: 50A       │
     się nie       │
     wyzwoli      Awaria tu:  
                  tylko 16A
                  się wyzwoli
```

#### Selektywność czasowa
- **RCD**: 100mA (1s) → 30mA (natychmiast)
- **MCB**: Wyłączniki selektywne (oznaczenie S)

## ⚡ Zabezpieczenia różnicowe specjalne

### AFDD (Arc Fault Detection Device)
- **Funkcja**: Wykrywa łuki elektryczne
- **Zastosowanie**: Ochrona przeciwpożarowa
- **Lokalizacja**: Sypialnie, pokoje dziecięce
- **Technologia**: Analiza spektrum sygnału

### RCMU (RCD Monitoring Unit)
- **Funkcja**: Monitoruje sprawność RCD
- **Zastosowanie**: Systemy IT, miejsca niebezpieczne
- **Test**: Automatyczny, cykliczny

## 🧮 Obliczenia praktyczne

### Przykład 1: Dobór MCB dla gniazdek
**Dane**: 5 gniazdek × 16A, przewód 2.5mm²
```
Obciążalność przewodu: Iz = 25A (2.5mm² w rurze)
Prąd obliczeniowy: Ib = 16A (zgodnie z normą)
Dobór: MCB 16A typ C (16A ≤ 25A) ✓
```

### Przykład 2: Dobór bezpiecznika dla transformatora
**Dane**: Transformator 230V/24V, 100VA
```
Prąd pierwotny: I1 = 100VA/230V = 0.43A
Prąd rozruchowy: Ir = 10 × I1 = 4.3A (przez 0.1s)
Dobór: Bezpiecznik 1A gG lub 0.5A aM
```

### Przykład 3: RCD dla łazienki
**Dane**: Łazienka z wanną
```
Wymaganie: IΔn ≤ 30mA (ochrona przeciwporażeniowa)
Typ A: obowiązkowy (pralka, suszarka)
Dodatkowe: 10mA dla gniazdka przy umywalce
```

## ⚠️ Konserwacja zabezpieczeń

### Testy RCD
- **Częstotliwość**: Miesięcznie (przycisk TEST)
- **Pomiar**: Rocznie (tester RCD)
- **Parametry**: Czas zadziałania, prąd wyzwalania

### Przeglądy MCB
- **Czyszczenie**: Kontaktów i mechanizmu
- **Test**: Działania przy przeciążeniu (symulator)
- **Wymiana**: Po liczbie zadziałań (20-30 × In)

### Dokumentacja
- **Protokoły**: Pomiarów i testów
- **Schemat**: Selektywności zabezpieczeń
- **Instrukcje**: Obsługi i konserwacji

## 📚 Powiązane tematy

- [[bezpieczenstwo_elektryczne|Bezpieczeństwo Elektryczne]]
- [[instalacje_elektryczne|Instalacje Elektryczne w Budynkach]]
- [[silniki_elektryczne|Silniki Elektryczne - Zabezpieczenia]]
- [[moc_elektryczna|Moc Elektryczna - Obliczenia Obciążeń]]
- [[multimetr|Multimetr - Pomiary Zabezpieczeń]]
- [[transformatory|Transformatory - Zabezpieczenia]]

---

#zabezpieczenia #MCB #RCD #bezpieczniki #SPD #selektywność #ochrona