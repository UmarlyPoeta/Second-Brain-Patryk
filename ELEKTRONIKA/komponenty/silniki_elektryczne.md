# Silniki Elektryczne

## ⚡ Definicja

**Silnik elektryczny** to maszyna elektryczna przetwarzająca energię elektryczną na energię mechaniczną (ruch obrotowy lub liniowy).

## 🔄 Podstawy działania

### Zasada elektromagnetyczna
1. **Przewód z prądem** w polu magnetycznym
2. **Siła Lorentza**: F = B × I × l
3. **Moment obrotowy**: M = F × r
4. **Wzajemne oddziaływanie** pól magnetycznych

### Podstawowe wzory
```
P = M × ω = M × n × 2π/60
```
Gdzie:
- **P** - moc mechaniczna [W]
- **M** - moment obrotowy [Nm]  
- **ω** - prędkość kątowa [rad/s]
- **n** - obroty [obr/min]

## 🏗️ Silniki prądu stałego (DC)

### Silnik szczotkowy DC

#### Budowa
- **Stojan (stator)**: Magnesy stałe lub elektromagnesy
- **Wirnik (rotor)**: Uzwojenia na wirniku
- **Szczotki**: Kontakt z kolektorem
- **Kolektor**: Komutacja prądu

#### Charakterystyka
```
U = E + I × R
E = k × Φ × n (siła elektromotoryczna)
M = k × Φ × I (moment)
```

#### Rodzaje według wzbudzenia

##### Silnik z magnesami stałymi
- **Wzbudzenie**: Magnesy neodymowe/ferrytowe
- **Regulacja**: Zmiana napięcia twornika
- **Zastosowania**: Napędy małej mocy, modelarstwo

##### Silnik szeregowy
```
   +U ── Wzbudzenie ── Twornik ── -U
```
- **Charakterystyka**: M ~ I² (duży moment rozruchowy)
- **Zastosowania**: Trakcja (tramwaje), narzędzia

##### Silnik bocznikowy  
```
   +U ──┬── Wzbudzenie ──┬── -U
        │               │
        └── Twornik ─────┘
```
- **Charakterystyka**: n ≈ const (stabilne obroty)
- **Zastosowania**: Obrabiarki, wentylatory

##### Silnik mieszany
- **Kombinacja**: Szeregowe + bocznikowe
- **Charakterystyka**: Kompromis między dwoma powyższymi

### Silnik bezstrukowy (BLDC)

#### Budowa
- **Stojan**: Trójfazowe uzwojenia
- **Wirnik**: Magnesy stałe
- **Czujniki**: Hall lub enkodery
- **Sterownik**: Elektroniczna komutacja

#### Zalety
- **Brak zużycia** szczotek
- **Wysoka sprawność** (85-95%)
- **Dokładna kontrola** prędkości i pozycji
- **Długa żywotność**

#### Wady
- **Droższy** w produkcji
- **Wymaga sterownika** elektronicznego
- **Skomplikowane** sterowanie

## 🌊 Silniki prądu przemiennego (AC)

### Silnik indukcyjny (asynchroniczny)

#### Budowa
- **Stojan**: Trójfazowe uzwojenia (pole wirujące)
- **Wirnik**: Klatka wiewiórcza lub uzwojenia
- **Poślizg**: s = (n₀ - n)/n₀

#### Charakterystyki
```
n₀ = 60 × f / p (obroty synchroniczne)
```
Gdzie:
- **f** - częstotliwość sieci [Hz]
- **p** - liczba par biegunów

**Przykłady**:
- 2 bieguny: 3000 obr/min (50Hz)
- 4 bieguny: 1500 obr/min (50Hz)
- 6 biegunów: 1000 obr/min (50Hz)

#### Rozruch silników indukcyjnych

##### Rozruch bezpośredni
- **Zastosowanie**: Silniki do 5kW
- **Prąd rozruchowy**: 5-8 × In
- **Wady**: Duże obciążenie sieci

##### Rozruch gwiazda-trójkąt (Y/Δ)
```
Start: Y (obniżone napięcie)
Praca: Δ (pełne napięcie)
```
- **Redukcja**: Prąd i moment 3x mniejszy
- **Przełączenie**: Po osiągnięciu prędkości

##### Częstotliwościowe (VFD)
- **Regulacja**: f i U jednocześnie
- **Zalety**: Płynny rozruch, sterowanie prędkością
- **Zastosowania**: Pompy, dmuchawy, przenośniki

### Silnik synchroniczny

#### Charakterystyka
- **Prędkość**: Równa synchronicznej n₀
- **Wzbudzenie**: Magnesy stałe lub elektromagnes
- **Zastosowania**: Duże moce, wymagana stała prędkość

#### Silniki krokowe

##### Cechy podstawowe
- **Pozycjonowanie**: Dyskretne kroki (1.8°, 0.9°)
- **Sterowanie**: Impulsami cyfrowymi
- **Bez czujników**: Open-loop positioning

##### Rodzaje
- **Reluctancyjne**: Zmienna reluctancja
- **Z magnesami**: Hybrydowe (najczęstsze)
- **Rozdzielczość**: 200-400 kroków/obrót

## 🏡 Silniki jednofazowe

### Problem rozruchu
- **Pole pulsacyjne** zamiast wirującego
- **Brak momentu** rozruchowego przy stanie
- **Potrzeba**: Pomocnicze uzwojenie rozruchowe

### Rozwiązania rozruchowe

#### Kondensator rozruchowy
```
    R (główne)
AC ──┴───┬─── AC
     C ──┤
     ┴   │
    (pom.)
```
- **Przesunięcie fazy**: 90° między uzwojeniami
- **Wyłączanie**: Stycznik odśrodkowy lub przekaźnik
- **Zastosowania**: Sprężarki, pompy

#### Kondensator pracy
- **Ciągle**: Kondensator pozostaje włączony
- **Charakterystyka**: Lepsze właściwości robocze
- **Rozruch**: Dodatkowy kondensator rozruchowy

#### Uzwojenie bifilaryczne
- **Rozruch**: Zwiększony opór uzwojenia pomocniczego
- **Wyłączanie**: Po osiągnięciu prędkości
- **Zastosowania**: Małe silniki (wentylatory)

## ⚡ Regulatory i sterowniki

### Regulatory DC

#### Regulator liniowy
- **Tranzystor**: W obszarze aktywnym
- **Straty**: Duże (grzanie)
- **Zastosowania**: Małe moce, wymagana cisza

#### Regulator PWM
```
Uśrednie = Umax × D (wypełnienie)
```
- **Sprawność**: Wysoka (85-95%)
- **Częstotliwość**: 1-100kHz
- **Zastosowania**: Większość aplikacji DC

### Falowniki (invertery)

#### Funkcja
- **Konwersja**: DC → AC 3-fazowy
- **Sterowanie**: SVPWM, sin-PWM
- **Parametry**: f = 0-200Hz, U = 0-100%

#### Zalety VFD
- **Oszczędność energii**: Do 50%
- **Płynne sterowanie**: Przyspieszanie/hamowanie
- **Ochrony**: Przeciążenie, zwarcie, fazowanie

## 🔧 Dobór silników

### Parametry podstawowe

#### Moc mechaniczna
```
P = M × n / 9550 [kW]
```
- **Margines**: 10-20% powyżej potrzeb
- **Praca**: Ciągła (S1) vs przerywana

#### Napięcie zasilania
- **DC**: 12V, 24V, 48V, 110V, 220V
- **AC jednofazowe**: 230V
- **AC trójfazowe**: 400V (Europa), 480V (USA)

#### Obroty znamionowe
- **DC**: Płynnie regulowalne 0-nmax
- **AC**: Zależne od liczby biegunów
- **Skrzynki**: Przekładnie mechaniczne

#### Rodzaj pracy
- **S1**: Ciągła (wentylatory, pompy)
- **S2**: Krótkotrwała (podnośniki)
- **S3**: Przerywana (dźwigi, prasy)

### Dobór praktyczny

#### Pompy odśrodkowe
```
P = Q × H × ρ × g / (3600 × η)
```
Gdzie:
- **Q** - wydajność [m³/h]
- **H** - wysokość podnoszenia [m]
- **η** - sprawność pompy

#### Wentylatory
```
P = Q × Δp / (3600 × η)
```
Gdzie:
- **Q** - wydajność [m³/h]  
- **Δp** - przyrost ciśnienia [Pa]

## ⚠️ Bezpieczeństwo

### Zagrożenia elektryczne
- **Wysokie napięcia**: Falowniki do 690V
- **Kondensatory**: Pozostają naładowane
- **Wirujące części**: Zawsze odłącz zasilanie

### Zagrożenia mechaniczne
- **Wał**: Możliwość zranienia
- **Wibracje**: Poluzowane elementy
- **Hałas**: Ochrona słuchu

### Ochrony silników

#### Termiczna
- **Termik**: Bimetaliczny w uzwojeniu
- **PT100**: Rezystor platynowy  
- **Wyłączenie**: Przy przekroczeniu temperatury

#### Nadprądowa
- **Wyłącznik silnikowy**: Regulowany zakres
- **Bezpieczniki**: Szybkie, charakterystyka aM
- **VFD**: Ograniczenie prądu elektroniczne

## 🧮 Obliczenia praktyczne

### Przykład 1: Moc pompy
**Dane**: Q = 10 m³/h, H = 20m, η = 70%

```
P = 10 × 20 × 1000 × 9.81 / (3600 × 0.7) = 0.78 kW
Dobór: Silnik 1.1 kW (margines)
```

### Przykład 2: Prąd silnika trójfazowego
**Dane**: P = 5.5kW, U = 400V, η = 88%, cos φ = 0.85

```
I = P / (√3 × U × η × cos φ)
I = 5500 / (1.73 × 400 × 0.88 × 0.85) = 10.7A
```

### Przykład 3: Kondensator rozruchowy
**Dane**: Silnik 2.2kW jednofazowy

```
C = 50-70 μF/kW = 50-70 × 2.2 = 110-154 μF
Dobór: 120 μF / 400V AC
```

## 🔧 Konserwacja

### Rutynowa
- **Kontrola wizualna**: Nie rzadziej niż raz na miesiąc
- **Smarowanie**: Według instrukcji (łożyska)
- **Czyszczenie**: Usuwanie kurzu z żeber chłodzących
- **Pomiary**: Prądy, temperatury, wibracje

### Okresowa  
- **Test izolacji**: Megger, raz na rok
- **Przegląd mechaniczny**: Łożyska, sprzęgła
- **Wymiana szczotek**: Silniki DC
- **Kalibracja**: VFD, regulatory

## 📚 Powiązane tematy

- [[transformatory|Transformatory]]
- [[kondensatory|Kondensatory - Rozruchowe]]
- [[tranzystory|Tranzystory - Sterowniki Silników]]
- [[moc_elektryczna|Moc Elektryczna]]
- [[zabezpieczenia_elektryczne|Zabezpieczenia Silników]]
- [[multimetr|Multimetr - Pomiary Silników]]

---

#silniki-elektryczne #elektrotechnika #DC #AC #falowniki #sterowanie #bezpieczeństwo