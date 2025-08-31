# Bezpieczeństwo Elektryczne

## ⚠️ Podstawy bezpieczeństwa elektrycznego

### Dlaczego prąd jest niebezpieczny?

#### Wpływ na organizm
Prąd elektryczny może:
- **Paraliżować mięśnie** (niemożność puszczenia przewodu)
- **Zakłócać pracę serca** (migotanie komór)
- **Powodować oparzenia** (cieplne i elektrolityczne)
- **Uszkadzać układ nerwowy**

#### Czynniki wpływające na niebezpieczeństwo
1. **Natężenie prądu** - najważniejsze
2. **Czas trwania** - dłuższy = groźniejszy  
3. **Droga przepływu** - przez serce najniebezpieczniej
4. **Częstotliwość** - 50/60Hz najgroźniejsze
5. **Stan skóry** - mokra/uszkodzona = mniejszy opór

## ⚡ Progi odczuwalności i niebezpieczeństwa

### Prąd przemienny (50Hz)
| Natężenie prądu | Skutek |
|----------------|--------|
| **0.5-1 mA** | Próg odczuwalności |
| **1-5 mA** | Lekkie mrowienie |
| **5-10 mA** | Bolesne mrowienie |
| **10-20 mA** | Skurcz mięśni, trudność z puszczeniem |
| **20-50 mA** | Silny skurcz, utrudnione oddychanie |
| **50-100 mA** | **Migotanie komór serca** |
| **100-200 mA** | Pewna śmierć po 1-3 sekundach |

### Prąd stały (DC)
**Mniej niebezpieczny** niż AC przy tych samych wartościach:
- Próg odczuwalności: ~2mA
- Progi niebezpieczeństwa są 2-3x wyższe
- Łatwiej puścić przewód (brak skurczów)

## 🏠 Bezpieczne napięcia

### Klasyfikacja napięć (norma)
- **ELV** (Extra Low Voltage): < 50V AC / < 120V DC - **BEZPIECZNE**
- **LV** (Low Voltage): 50V-1000V AC / 120V-1500V DC  
- **MV** (Medium Voltage): 1kV-35kV
- **HV** (High Voltage): > 35kV

### Praktyczne bezpieczne napięcia
- **12V DC**: Motoryzacja - praktycznie bezpieczne
- **24V DC/AC**: Automatyka - bezpieczne w suchych warunkach
- **48V DC**: Telekomunikacja - ostatnie "bezpieczne" napięcie
- **230V AC**: **NIEBEZPIECZNE** - instalacje domowe

## 🏡 Ochrona w instalacjach domowych

### Wyłączniki różnicowoprądowe (RCD)

#### Zasada działania
```
   L ──┐  ┌── L
       │30mA│
   N ──┴──┴── N
       │
    RCD│
       ↓ GND
```
**Gdy IL ≠ IN → zadziała przy różnicy ≥ 30mA**

#### Rodzaje RCD
- **30 mA**: Ochrona przeciwporażeniowa (ludzie)
- **100 mA**: Ochrona przeciwpożarowa  
- **300 mA**: Ochrona majątku

#### Typy RCD
- **AC**: Tylko prąd przemienny
- **A**: AC + prąd pulsujący DC
- **B**: AC + DC (przemysł)

### Wyłączniki nadprądowe (MCB)

#### Charakterystyki wyzwalania
- **Typ B**: 3-5 × In (instalacje mieszkalne)
- **Typ C**: 5-10 × In (oświetlenie, gniazdka)  
- **Typ D**: 10-20 × In (silniki)

#### Dobór prądu nominalnego
**Zasada**: In(MCB) ≤ Imax(przewód)

**Przykłady**:
- Przewód 1.5mm² → max 10A → MCB 10A
- Przewód 2.5mm² → max 16A → MCB 16A  
- Przewód 4.0mm² → max 25A → MCB 20A lub 25A

### Uziemienie ochronne

#### System TN (most popular)
```
Transformator:  Rozdzielnica:  Odbiornik:
     N ──────────── N ──────────── N
     │              │              │
    ═══            PE ────────────═══ Obudowa
   ZIEMIA                        ZIEMIA
```

#### Zasada działania
1. **Zwarcie** faza-obudowa
2. **Duży prąd** przez PE i N
3. **Zadziała MCB** lub bezpiecznik
4. **Szybkie wyłączenie** niebezpiecznego napięcia

## ⚠️ Pierwsza pomoc przy porażeniu prądem

### Natychmiastowe działania
1. **WYŁĄCZ PRĄD** - bezpiecznik, wyłącznik główny
2. **NIE DOTYKAJ** poszkodowanego gdy jest pod napięciem
3. **Odłącz** poszkodowanego (drewniana deszczułka, gumowe rękawice)
4. **Sprawdź** oddech i tętno
5. **Wezwij pomoć** - 112 lub 999

### Resuscytacja krążeniowo-oddechowa (RKO)
Jeśli **brak oddechu** lub **brak tętna**:
1. **30 uciśnięć** klatki piersiowej (5-6cm głębokość)
2. **2 oddechy** ratownicze (usta-usta)
3. **Kontynuuj** do przyjazdu pomocy

### Po porażeniu
**ZAWSZE** skonsultuj z lekarzem, nawet gdy czujesz się dobrze:
- Skutki mogą pojawić się później
- Możliwe uszkodzenia serca
- Ryzyko powikłań

## 🔧 Bezpieczeństwo podczas pracy

### Przed rozpoczęciem pracy
1. **WYŁĄCZ zasilanie** - bezpiecznik/główny wyłącznik
2. **Sprawdź brak napięcia** - multimetrem lub wskaźnikiem
3. **Zabezpiecz** przed przypadkowym włączeniem
4. **Użyj EPG** (środki ochrony indywidualnej)

### Środki ochrony osobistej (EPG)
- **Rękawice dielektryczne** - klasa 00 (500V) do klasy 4 (40kV)
- **Obuwie dielektryczne** - bez metalowych elementów
- **Odzież ochronna** - nieprzewodząca, bez sztucznych włókien
- **Okulary ochronne** - przy spawaniu, łuku elektrycznym

### Narzędzia bezpieczne
- **Izolowane do 1000V** - znormalizowane narzędzia
- **Wskaźniki napięcia** - bezstykowe i kontaktowe  
- **Multimetry CAT III/IV** - odporne na przepięcia
- **Latarki bezpieczne** - unikaj metalowych

## ⚡ Niebezpieczeństwa specjalne

### Kondensatory wysokich napięć
- **Magazynują energię** nawet po wyłączeniu zasilania
- **Rozładowanie**: Rezystor izolowany 1-10kΩ
- **Nigdy** nie dotykaj wyprowadzeń
- **Sprawdź napięcie** przed pracą

### Transformatory wysokich napięć
- **Transformatory neonowe**: 9-15kV
- **Transformatory mikrofalowe**: 2-4kV + wysokoprądowe
- **Transformatory spawalnicze**: Niskie napięcie, wysoki prąd

### Baterie
- **Kwas siarkowy** (olowiowe): Żrący, toksyczne gazy
- **Litowo-jonowe**: Ryzyko pożaru/eksplozji przy uszkodzeniu
- **Wysokie prądy**: Zwarcie akumulatora samochodowego

### Linie napowietrzne
- **Nigdy** nie zbliżaj się do przewodów wysokich napięć
- **Minimalne odległości**:
  - 1kV: 1m
  - 15kV: 3m  
  - 110kV: 5m
  - 400kV: 8m

## 🏥 Skutki porażenia długoterminowe

### Natychmiastowe
- Oparzenia elektryczne i termiczne
- Złamania (skurcz mięśni)
- Wstrząs i utrata przytomności

### Późne (po godzinach/dniach)
- Zaburzenia rytmu serca
- Uszkodzenia neurologiczne  
- Problemy z pamięcią i koncentracją
- Depresja i stany lękowe

## 📋 Lista kontrolna bezpieczeństwa

### Przed każdą pracą elektryczną:
- [ ] Czy wyłączyłem zasilanie?
- [ ] Czy sprawdziłem brak napięcia?  
- [ ] Czy mam odpowiednie narzędzia?
- [ ] Czy ktoś wie gdzie pracuję?
- [ ] Czy znam lokalizację wyłącznika głównego?
- [ ] Czy mam kontakt z pomocą medyczną?

### Podczas pracy:
- [ ] Czy pracuję jedną ręką gdy to możliwe?
- [ ] Czy unikam dotykania uziemionych powierzchni?
- [ ] Czy mam suche ręce i obuwie?
- [ ] Czy zachowuję ostrożność?

## 📚 Powiązane tematy

- [[instalacje_elektryczne|Instalacje Elektryczne w Budynkach]]
- [[zabezpieczenia_elektryczne|Zabezpieczenia Elektryczne]]
- [[multimetr|Multimetr - Bezpieczny Pomiar]]
- [[uziemienie|Systemy Uziemieniowe]]
- [[pierwsza_pomoc|Pierwsza Pomoc - Elektryczna]]

---

#bezpieczeństwo #BHP #porażenie #pierwsza-pomoc #instalacje #ochrona