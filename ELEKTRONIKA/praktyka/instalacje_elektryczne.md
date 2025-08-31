# Instalacje Elektryczne w Budynkach

## 🏠 Podstawy instalacji elektrycznych

### Definicja
**Instalacja elektryczna** to zespół przewodów, urządzeń i aparatów elektrycznych służących do przesyłania, rozdziału i używania energii elektrycznej w budynku.

### Podstawowe funkcje
- **Zasilanie** odbiorników energii elektrycznej
- **Bezpieczne** używanie energii
- **Ochrona** przed porażeniem i pożarem
- **Wygodna eksploatacja** i konserwacja

## ⚡ Sieć elektroenergetyczna

### System TN-C-S (najczęściej w Polsce)
```
Transformator 15/0.4kV:
┌─── L1 (faza 1) ──── 230V ────┐
├─── L2 (faza 2) ──── 230V ────┤
├─── L3 (faza 3) ──── 230V ────┤ → Dom
├─── N (neutralny) ── 0V ──────┤
└─── PE (ochronny) ── ziemia ──┘

Napięcia fazowe: L1-N, L2-N, L3-N = 230V
Napięcia międzyfazowe: L1-L2, L2-L3, L3-L1 = 400V
```

### Rodzaje sieci

#### Sieć TN-C
- **PEN**: Połączony przewód ochronny i neutralny
- **Zastosowanie**: Instalacje starsze, przemysł
- **Wady**: Brak galwanicznej separacji N-PE

#### Sieć TN-S  
- **Oddzielne**: N i PE przez całą trasę
- **Zastosowanie**: Nowoczesne budynki mieszkalne
- **Zalety**: Lepsza ochrona przeciwporażeniowa

#### Sieć TT
- **Uziemienie lokalne**: Odbiornika
- **RCD obowiązkowy**: 30mA lub 100mA
- **Zastosowanie**: Budynki jednorodzinne na wsiach

## 🔧 Elementy instalacji

### Rozdzielnica główna

#### Budowa
```
    Licznik energii
         │
    ── WLZ ──  (wyłącznik główny)
         │
    ┌─── RCD 40A/30mA ────┐
    │                    │
MCB 16A │  MCB 10A       │  MCB 20A
gniazdka │  oświetlenie   │  kuchnia
```

#### Elementy obowiązkowe
- **Wyłącznik główny** (WLZ) - odłączenie całego budynku
- **Wyłączniki różnicowoprądowe** (RCD) - ochrona przeciwporażeniowa  
- **Wyłączniki nadprądowe** (MCB) - ochrona obwodów
- **Ogranicznik przepięć** (SPD) - ochrona przed przepięciami

### Wyłączniki różnicowoprądowe (RCD)

#### Prądy wyzwalania
- **10 mA**: Łazienki (specjalne wymagania)
- **30 mA**: Ochrona przeciwporażeniowa (obowiązkowa)
- **100 mA**: Ochrona przeciwpożarowa
- **300 mA**: Ochrona majątku

#### Typy RCD
- **AC**: Tylko prądy przemienne sinusoidalne
- **A**: AC + prądy pulsujące DC (pralki, ściemniacze)
- **B**: AC + DC (falowniki, UPS)

### Wyłączniki nadprądowe (MCB)

#### Charakterystyki wyzwalania
- **Typ B**: 3-5 × In (instalacje mieszkalne)
- **Typ C**: 5-10 × In (oświetlenie, gniazdka ogólne)
- **Typ D**: 10-20 × In (transformatory, silniki)

#### Prądy znamionowe
- **6A**: Oświetlenie mieszkalne
- **10A**: Oświetlenie rozszerzone
- **16A**: Gniazdka standardowe  
- **20A**: Gniazdka kuchnia, łazienka
- **25A**: Płyta elektryczna, bojler
- **32A**: Duże odbiorniki (piece, ładowarki EV)

## 🔌 Przewody i okablowanie

### Przekroje przewodów

#### Dobór według obciążenia
| Prąd [A] | Przekrój Cu [mm²] | MCB [A] | Zastosowanie |
|----------|-------------------|---------|---------------|
| **10** | 1.5 | 10 | Oświetlenie |
| **16** | 2.5 | 16 | Gniazdka standardowe |
| **25** | 4.0 | 20 | Gniazdka kuchnia |
| **32** | 6.0 | 25 | Bojler, piec |
| **40** | 10.0 | 32 | Kuchnia elektryczna |

#### Spadki napięć
**Maksymalne dozwolone**:
- **Oświetlenie**: 3%
- **Inne odbiorniki**: 5%

**Obliczanie spadku**:
```
ΔU = (2 × l × I × ρ) / S
```
Gdzie:
- l - długość przewodu [m]
- I - prąd [A]  
- ρ - oporność Cu = 0.0175 Ω×mm²/m
- S - przekrój [mm²]

### Rodzaje przewodów

#### YDY (mieszkalne)
- **Budowa**: Jednożyłowe, miedziane, izolacja PVC
- **Kolory**: L-brązowy, N-niebieski, PE-żółto-zielony
- **Zastosowanie**: Instalacje podtynkowe

#### YKY (rozdzielcze)
- **Budowa**: Wielo-żyłowe, miedziane
- **Przekroje**: 3×1.5, 5×2.5, 5×4.0
- **Zastosowanie**: Połączenia rozdzielnic

#### H05VV-F (łączeniowe)
- **Budowa**: Elastyczne, PVC
- **Zastosowanie**: Przedłużacze, przewody sieciowe

## 🏠 Rozmieszczenie w pomieszczeniach

### Wysokości montażu
- **Wyłączniki**: 140cm od podłogi
- **Gniazdka standardowe**: 30cm od podłogi  
- **Gniazdka blat kuchenny**: 110cm od podłogi
- **Gniazdka łazienka**: > 60cm od brodzika/wanny

### Strefy w łazience

#### Strefa 0
- **Lokalizacja**: Wewnątrz wanny/brodzika
- **Ochrona**: IPX7, napięcie < 12V AC
- **Urządzenia**: Brak (poza specjalnymi)

#### Strefa 1  
- **Lokalizacja**: Nad wanną do 225cm wysokości
- **Ochrona**: IPX4, napięcie < 25V AC
- **Urządzenia**: Grzałki, bojlery (klasa I)

#### Strefa 2
- **Lokalizacja**: 60cm od strefy 1
- **Ochrona**: IPX4
- **Urządzenia**: Oświetlenie, gniazdka z RCD 30mA

### Liczba punktów

#### Oświetlenie
- **Minimium**: 1 punkt na pomieszczenie
- **Salon**: 1 punkt na 20m²
- **Kuchnia**: Oświetlenie ogólne + blat roboczy

#### Gniazdka
- **Salon/sypialnia**: 1 gniazdko na 6m²
- **Kuchnia**: Minimum 6 gniazdek
- **Łazienka**: Minimum 1 gniazdko (strefa 2)
- **Korytarz**: 1 gniazdko na 10m biegu

## ⚠️ Ochrony i zabezpieczenia

### Ochrona przeciwporażeniowa

#### Ochrona podstawowa
- **Izolacja**: Przewodów i urządzeń
- **Obudowy**: IP stopień ochrony
- **Odległości**: Bezpieczne od części czynnych

#### Ochrona dodatkowa  
- **Uziemienie ochronne**: Połączenie PE
- **Wyrównanie potencjałów**: Instalacje metalowe
- **RCD**: Wyłączniki różnicowoprądowe

### Ochrona przeciwpożarowa

#### Ograniczniki przepięć (SPD)
```
L ──┬─── SPD ───┬─── Instalacja
    │           │
    └─── SPD ───┤
    │           │
N ──┴───────────┤
                │
PE ─────────────┘
```

#### Wyłączniki łukowe (AFDD)
- **Funkcja**: Wykrywanie łuków elektrycznych
- **Zastosowanie**: Sypialnie, pokoje dziecięce
- **Technologia**: Analiza widma częstotliwościowego

## 🔧 Montaż i wykonanie

### Instalacje podtynkowe

#### Bruzdy w ścianach
- **Kierunek**: Poziomo/pionowo (nie ukośnie)
- **Głębokość**: 2× średnica rury
- **Odległość od krawędzi**: > 5cm

#### Puszki instalacyjne  
- **Średnica**: fi 60mm (standardowa)
- **Głębokość**: 40mm (minimum)
- **Mocowanie**: Gips, alabaster (nie cement)

### Instalacje natynkowe

#### Korytka instalacyjne
- **Rodzaje**: PVC, aluminium
- **Rozmiary**: 25×16, 40×25, 60×40mm
- **Pokrywy**: Zdejmowane dla konserwacji

#### Przepusty
- **Ściany**: Tuleje ochronne
- **Stropy**: Przepusty ognioodporne
- **Uszczelnienie**: Pianka, masa ognioodporna

## 🧮 Obliczenia projektowe

### Bilans mocy
```
Pmoc = Σ(Pi × ki × kj)
```
Gdzie:
- Pi - moc odbiornika
- ki - współczynnik jednoczesności  
- kj - współczynnik zapotrzebowania

#### Typowe współczynniki
- **Oświetlenie**: ki = 1.0, kj = 0.9
- **Gniazdka**: ki = 0.2, kj = 1.0  
- **Grzanie**: ki = 0.8, kj = 1.0

### Prąd obliczeniowy
**Jednofazowy**:
```
Ib = P / (U × cos φ)
```

**Trójfazowy**:  
```
Ib = P / (√3 × U × cos φ)
```

### Dobór zabezpieczeń
```
Ib ≤ In ≤ Iz
```
Gdzie:
- Ib - prąd obliczeniowy
- In - prąd znamionowy zabezpieczenia
- Iz - obciążalność przewodu

## ⚠️ Odbiory i legalizacja

### Przeglądy instalacji

#### Odbiór pierwotny
- **Pomiary**: Izolacja, ciągłość PE, RCD
- **Protokół**: Przez uprawnionego elektryka
- **Częstotliwość**: Przed pierwszym użyciem

#### Przeglądy okresowe
- **Mieszkania**: Co 10 lat
- **Biura**: Co 5 lat  
- **Przemysł**: Co 1 rok
- **Miejsca szczególnie zagrożone**: Co 1 rok

### Podstawowe pomiary

#### Test izolacji
- **Napięcie**: 500V DC (instalacje do 500V)
- **Wymaganie**: > 0.5 MΩ (nowe), > 0.25 MΩ (ekspl.)
- **Pomiar**: Między fazami a PE, N-PE

#### Test RCD
- **Prąd testowy**: 1× IN (nie zadziała)
- **Prąd testowy**: 5× IN (zadziała < 300ms)
- **Prąd testowy**: 0.5× IN (może zadziałać)

#### Test ciągłości PE
- **Prąd**: > 200mA
- **Wymaganie**: < 0.05Ω + 0.02Ω/m

## 📚 Powiązane tematy

- [[bezpieczenstwo_elektryczne|Bezpieczeństwo Elektryczne]]
- [[zabezpieczenia_elektryczne|Zabezpieczenia Elektryczne]]
- [[uziemienie|Systemy Uziemieniowe]]
- [[moc_elektryczna|Moc Elektryczna - Bilanse]]
- [[multimetr|Multimetr - Pomiary Instalacji]]
- [[transformatory|Transformatory - Stacje Trafo]]

---

#instalacje-elektryczne #BHP #RCD #MCB #przewody #rozdzielnice #budynki