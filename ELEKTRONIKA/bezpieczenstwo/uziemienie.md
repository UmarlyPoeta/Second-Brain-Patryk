# Uziemienie i Systemy Ochronne

## 🌍 Definicja uziemienia

**Uziemienie** to połączenie przewodzące między instalacją elektryczną a ziemią, mające na celu zapewnienie bezpiecznego odprowadzenia prądów awarii i wyrównanie potencjałów.

## ⚡ Rodzaje uziemień

### Uziemienie robocze (funkcjonalne)
- **Cel**: Prawidłowe funkcjonowanie instalacji
- **Przykłady**: Punkt zerowy transformatora, filtry EMC
- **Oznaczenie**: Często brak oznaczenia lub "FE"

### Uziemienie ochronne
- **Cel**: Bezpieczeństwo ludzi i zwierząt
- **Zastosowanie**: Obudowy urządzeń elektrycznych
- **Oznaczenie**: PE (Protective Earth) - żółto-zielony

### Uziemienie piorunochronne
- **Cel**: Odprowadzenie prądów pioruna
- **Składniki**: Zwodniki, przewody odprowadzające
- **Oznaczenie**: Czerwone tabliczki "UZIEMIENIE"

## 🔧 Systemy uziemieniowe (wg IEC)

### System TN (Terra-Neutral)

#### TN-C (combined)
```
Transformator:    Instalacja:
   N ────────────── PEN ── Odbiorniki
   │               │
  ╧ Uziem        ╧ Uziem  
```
**Cechy**:
- **PEN**: Jeden przewód jako N i PE  
- **Zastosowania**: Przemysł, starsze instalacje
- **Wady**: Brak separacji N-PE, zagrożenia

#### TN-S (separated)  
```
Transformator:    Instalacja:
   N ────────────── N ── Odbiorniki
   │               │
   PE ───────────── PE ── Obudowy
   │               │
  ╧ Uziem        ╧ Uziem
```
**Cechy**:
- **Oddzielne**: N i PE przez całą trasę
- **Zastosowania**: Nowoczesne budynki mieszkalne
- **Zalety**: Bezpieczniejsze, lepsze EMC

#### TN-C-S (combined-separated)
```
Transformator:    Rozdzielnica:    Instalacja:
   PEN ──────────── PEN ──┬── N ── Odbiorniki  
   │                │     │
  ╧ Uziem          │     PE ── Obudowy
                    │     │
                   ╧ Uziem ╧ Uziem
```
**Cechy**:
- **PEN do rozdzielnicy**, następnie podział N/PE
- **Najczęściej**: Stosowane w Polsce
- **Kompromis**: Między TN-C a TN-S

### System TT (Terra-Terra)
```
Transformator:    Instalacja:
   N ────────────── N ── Odbiorniki
   │               │
  ╧ Uziem Trafo   PE ── Obudowy
                   │
                  ╧ Uziem lokalne
```
**Cechy**:
- **Lokalne uziemienie**: Niezależne od trafo
- **RCD obowiązkowy**: Jedyny sposób ochrony
- **Zastosowania**: Budynki wiejskie, mobilne

### System IT (Isolated-Terra)
```
Transformator:    Instalacja:  
   Izolowany ────── L1,L2,L3 ── Odbiorniki
   od ziemi        │
                   PE ── Obudowy  
                   │
                  ╧ Uziem lokalne
```
**Cechy**:
- **Pierwotne**: Izolowane od ziemi
- **Monitor izolacji**: Sygnalizuje pierwsze zwarcie
- **Zastosowania**: Szpitale, kopalnie (ciągłość zasilania)

## 🔧 Budowa uziemiania

### Elektrody uziemiające

#### Elektrody poziome
```
    ╔══ Przewód Cu 25mm² ══╗
    ║                     ║ 0.8m głębokość
    ║  ←── 20m długość ──→ ║
    ╚═════════════════════╝
```
**Materiał**: Pasek stalowy 30×4mm, taśma miedziana
**Zalety**: Łatwość układania, duża powierzchnia
**Wady**: Większy opór niż pręty

#### Elektrody pionowe (pręty)
```
        │← Pręt stalowy
        │  lub miedziany
        │  ⌀16-20mm
        │
    ────┼──── poziom gruntu
        │
        │  2.5-3m głębokość
        │
        ●
```
**Materiał**: Stal ocynkowana, miedź
**Zalety**: Mały opór, sięgają wilgotnych warstw
**Wady**: Trudniejsze wbijanie

#### Uziomy taśmowe
```
Fundament żelbetowy:
┌─────────────────────────┐
│ ←──── Taśma Fe 30×4 ────│ Beton
│                         │
└─────────────────────────┘
           │
    Wyprowadzenie Cu
```
**Zalety**: Wykorzystanie fundamentów, trwałość
**Zastosowanie**: Nowe budynki, duże obiekty

### Przewody uziemiające

#### Przekroje minimalne
- **Miedź**: 16mm² (ochronne), 10mm² (funkcjonalne)
- **Stal**: 50mm² (ochronne)
- **Aluminium**: 25mm² (nie zalecane w ziemi)

#### Ochrona przed korozją
- **Powłoki**: Ocynk, miedź
- **Głębokość**: Min. 0.8m (poniżej przemarzania)
- **Kontakty**: Lutowane, spawane, zaciskane

## ⚡ Opór uziemienia

### Wzór podstawowy
```
R = ρ / (2πl)  [Ω]
```
Gdzie:
- **ρ** - oporność właściwa gruntu [Ω×m]
- **l** - długość elektrody [m]

### Oporność gruntów
| Rodzaj gruntu | Oporność [Ω×m] |
|---------------|----------------|
| **Woda morska** | 0.2 |
| **Glina wilgotna** | 10-50 |
| **Ziemia uprawna** | 50-200 |  
| **Piasek wilgotny** | 200-1000 |
| **Piasek suchy** | 1000-5000 |
| **Skała** | 10000+ |

### Wymagane wartości oporu

#### System TN
- **Ra < 50V / Ia**: Gdzie Ia - prąd zadziałania zabezpieczenia
- **Typowo**: Ra < 10Ω (dla MCB 25A)
- **Obliczenie**: 50V / 5A = 10Ω

#### System TT  
- **Ra < 50V / IΔn**: Gdzie IΔn - prąd RCD
- **Przykład**: Ra < 50V / 0.03A = 1667Ω
- **Praktycznie**: Ra < 30-100Ω (zapas bezpieczeństwa)

#### Specjalne wymagania
- **Stacje trafo**: Ra < 1Ω
- **Telekomunikacja**: Ra < 4Ω  
- **Piorunochrony**: Ra < 10Ω

## 🔧 Pomiary uziemienia

### Metody pomiarowe

#### Metoda trzyelektrodowa (Wenner)
```
      20m        20m
   E ──────── S ──────── H
   │         │         │
Elektroda  Sonda    Elektroda
 badana   napięć.   prądowa
```

**Procedura**:
1. **Pomiar**: Miernik uziemienia 3-klemmowy
2. **Odległości**: E-S = S-H = 20-50m  
3. **Kierunek**: Pod kątem prostym do E
4. **Wynik**: Bezpośredni odczyt Ra

#### Metoda dwuelektrodowa (uproszczona)
```
Ra(zmierzona) = Ra(badana) + Ra(pomocnicza)

Warunek: Ra(pomocnicza) << Ra(badana)
```

#### Metoda pętli zwarciowej
```
Za pomocą miernika pętli zwarciowej:
Zs = Ztrafo + Zprzevodów + Ra

Do określenia Ra przy znanym Zs
```

### Przyrządy pomiarowe

#### Miernik uziemienia cyfrowy
- **Zakres**: 0.01Ω - 20kΩ
- **Dokładność**: ±2-5%
- **Częstotliwość**: 128Hz (unikanie 50Hz)
- **Funkcje**: Auto-range, pamięć wyników

#### Miernik kleszczowy (clamp-on)
- **Zasada**: Transformator Rogosky
- **Zalety**: Bez rozłączania uziemienia
- **Ograniczenia**: Wymaga pętli powrotu
- **Zastosowanie**: Systemy TN-C, pomiary kontrolne

## ⚡ Wyrównanie potencjałów

### Główne wyrównanie potencjałów (GWP)
```
Rozdzielnica główna (PE/PEN):
    │
    ├─── Instalacja wodna (metalowa)
    ├─── Instalacja gazowa  
    ├─── Instalacja c.o.
    ├─── Konstrukcja budynku (żelbet)
    ├─── Inne instalacje metalowe
    └─── Szyna wyrównania potencjałów
```

**Przekrój przewodów**: Min. 10mm² Cu (do 16mm² PE)

### Dodatkowe wyrównanie potencjałów (DWP)  
```
Łazienka:
PE ──┬─── Wanna metalowa
     ├─── Rury wodne  
     ├─── Rury grzewcze
     ├─── Odpływ prysznica
     └─── Inne części przewodzące
```

**Zastosowanie**: Łazienki, baseny, miejsca mokre
**Przekrój**: Min. 4mm² Cu

### Funkcjonalne wyrównanie potencjałów
- **Cel**: EMC, redukcja zakłóceń
- **Zastosowanie**: Serwerownie, laboratoria
- **Siatka**: Miedziana, 60cm × 60cm
- **Połączenie**: Każde urządzenie elektroniczne

## ⚠️ Błędy i zagrożenia

### Błędy montażowe

#### Złe połączenia
- **Skrętki**: Zamiast połączeń lutowanych/zaciskanych
- **Korozja**: Różne metale w kontakcie
- **Luzy**: Zmienne opory połączeń

#### Błędne trasy
- **Długie**: Przewody PE (zwiększona impedancja)
- **Równoległe**: Do przewodów fazowych (indukcyjność)
- **Przerwanie**: Ciągłości w złączach

### Zagrożenia eksploatacyjne

#### Korozja elektrolytyczna
```
Anoda (+): Fe → Fe²⁺ + 2e⁻ (rozpuszczanie)
Katoda (-): O₂ + 4H⁺ + 4e⁻ → 2H₂O

Ochrona: Powłoki, inhibitory korozji
```

#### Prądy błądzące
- **Źródło**: Instalacje DC (tramwaje, elektroliza)
- **Skutek**: Przyspieszona korozja uziomów
- **Ochrona**: Izolacja, uziomy galwaniczne

#### Przepięcia krokowe i dotykowe
```
Napięcie krokowe: Uk = I × ρ / (2π) × (1/r1 - 1/r2)
Napięcie dotykowe: Ud = I × ρ / (2πr) 

Bezpieczne: Uk < 65V, Ud < 50V
```

## 🧮 Obliczenia praktyczne

### Przykład 1: Wymiar pręta uziemiącego
**Dane**: System TT, RCD 30mA, grunt - glina (ρ=100 Ω×m)
```
Ra(wymagane) = 50V / 0.03A = 1667Ω
Ra(praktyczne) < 100Ω (zapas)

l = ρ / (2π × Ra) = 100 / (2π × 100) = 0.16m

Pręt minimum: 2.5m (ze względów praktycznych)
```

### Przykład 2: System TN, MCB 25A
**Dane**: ρ = 200 Ω×m, wymagane Ra < 2Ω
```
l = ρ / (2π × Ra) = 200 / (2π × 2) = 16m

Rozwiązanie: 8 prętów po 2.5m lub taśma 20m
```

### Przykład 3: Opór zastępczy elektrod równoległych
```
1/Ra = 1/R1 + 1/R2 + ... + 1/Rn

Przykład: 4 pręty po 10Ω każdy
Ra = 10Ω / 4 = 2.5Ω (przy dużych odległościach)

Praktycznie: Ra = 10Ω / 2.5 = 4Ω (wzajemne oddziaływanie)
```

## 📋 Dokumentacja i normy

### Pomiary obowiązkowe
- **Odbiór**: Przed pierwszym użyciem
- **Okresowe**: Co 5 lat (budynki), co 1 rok (przemysł)
- **Kontrolne**: Po każdej modyfikacji
- **Sezonowe**: Przed i po zimie (zmiany wilgotności)

### Protokoły pomiarów
**Zawartość**:
- Data, warunki atmosferyczne
- Metoda i przyrząd pomiarowy
- Schemat rozmieszczenia elektrod
- Wyniki Ra dla każdej elektrody
- Ocena zgodności z normami

### Normy polskie
- **PN-HD 60364**: Instalacje elektryczne w obiektach budowlanych
- **PN-E-05204**: Ochrona przed porażeniem elektrycznym
- **PN-89/E-05003**: Ochrona odgromowa obiektów budowlanych

## 📚 Powiązane tematy

- [[bezpieczenstwo_elektryczne|Bezpieczeństwo Elektryczne]]
- [[zabezpieczenia_elektryczne|Zabezpieczenia Elektryczne]]
- [[instalacje_elektryczne|Instalacje Elektryczne w Budynkach]]
- [[multimetr|Multimetr - Pomiary Uziemienia]]
- [[transformatory|Transformatory - Uziemienie]]
- [[silniki_elektryczne|Silniki - Uziemienie Ochronne]]

---

#uziemienie #PE #TN #TT #IT #ochrona #bezpieczeństwo #pomiary #opór-uziemienia