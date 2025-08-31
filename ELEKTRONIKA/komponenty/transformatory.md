# Transformatory

## 🔄 Definicja

**Transformator** to urządzenie elektryczne służące do zmiany wartości napięcia przemiennego przy zachowaniu mocy, składające się z dwóch lub więcej cewek (uzwojeń) sprzężonych magnetycznie przez wspólny rdzeń.

## ⚡ Zasada działania

### Prawa transformatora (idealnego)

#### Przekładnia napięciowa
```
U₂/U₁ = N₂/N₁ = n
```
Gdzie:
- **U₁** - napięcie pierwotne
- **U₂** - napięcie wtórne  
- **N₁** - liczba zwojów uzwojenia pierwotnego
- **N₂** - liczba zwojów uzwojenia wtórnego
- **n** - przekładnia transformatora

#### Przekładnia prądowa
```
I₂/I₁ = N₁/N₂ = 1/n
```

#### Zachowanie mocy
```
P₁ = P₂  →  U₁ × I₁ = U₂ × I₂
```

### Indukcja elektromagnetyczna
1. **Prąd przemienny** w uzwojeniu pierwotnym
2. **Zmienna indukcja magnetyczna** w rdzeniu  
3. **Indukowanie napięcia** w uzwojeniu wtórnym (prawo Faradaya)
4. **Przekształcenie** napięcia zgodnie z przekładnią

## 🏗️ Budowa transformatora

### Rdzeń magnetyczny

#### Transformatory rdzeniowe (50Hz)
- **Materiał**: Stal transformatorowa (blachy izolowane)
- **Kształty**: E-I, C, toroidal, R
- **Grubość blach**: 0.3-0.5mm (redukcja prądów wirowych)
- **Zastosowania**: Zasilacze sieciowe, audio

#### Transformatory bezrdzeniowe
- **Rdzeń**: Powietrze
- **Indukcyjność**: Mała
- **Zastosowania**: VHF/UHF, impedancja charakterystyczna

#### Transformatory ferrytowe
- **Materiał**: Ferryty (tlenki żelaza)
- **Częstotliwość**: 1kHz - 1MHz+
- **Zastosowania**: Zasilacze impulsowe, transformatory IF

### Uzwojenia

#### Uzwojenie pierwotne (primary)
- **Podłączane** do źródła napięcia AC
- **Pobiera** moc ze źródła
- **Przewody**: Grubość według prądu pierwotnego

#### Uzwojenie wtórne (secondary)  
- **Dostarcza** moc do obciążenia
- **Może być** jedno lub więcej uzwojeń
- **Izolacja**: Galwaniczna od pierwotnego

#### Uzwojenia dodatkowe
- **Bias**: Małe napięcia pomocnicze
- **Feedback**: Sprzężenie zwrotne
- **Screen**: Ekranowanie (uziemione)

## 🔧 Rodzaje transformatorów

### Transformatory sieciowe (50Hz)

#### Transformatory obniżające
- **Zastosowania**: Zasilacze elektroniczne
- **Typowe**: 230V → 12V, 9V, 6V
- **Moc**: 3VA - 1000VA
- **Przykład**: Ładowarka telefonu

#### Transformatory podwyższające  
- **Zastosowania**: Neon, lasery, spawarki
- **Typowe**: 230V → 2000V-15000V
- **Niebezpieczeństwo**: Wysokie napięcie!

#### Autotransformatory
```
     ┌─── 250V
230V ├─── 230V (wejście)
     ├─── 200V  
     └─── 110V
```
- **Jedna cewka** z odpustami
- **Brak izolacji** galwanicznej
- **Zastosowania**: Regulatory napięcia

### Transformatory impulsowe

#### Flyback (zwrotne)
- **Energia magazynowana** w pauzie
- **Zastosowania**: Zasilacze TV, LED
- **Izolacja**: Pierwotne/wtórne oddzielone

#### Forward (przepustowe)
- **Energia przekazywana** bezpośrednio  
- **Sprawność**: Wyższa niż flyback
- **Zastosowania**: Zasilacze komputerowe

### Transformatory audio

#### Transformatory wyjściowe
- **Dopasowanie impedancji**: Lampa → głośnik
- **Częstotliwość**: 20Hz - 20kHz
- **Zniekształcenia**: Minimalne

#### Transformatory mikrofonowe
- **Symetrizacja**: Balansowanie sygnału
- **Tłumienie**: Szumów i zakłóceń
- **Impedancja**: 600Ω ↔ 600Ω

### Transformatory prądowe (CT)

#### Pomiarowe
- **Przekładnia**: 1000A/5A, 100A/1A
- **Zastosowania**: Pomiary dużych prądów
- **Dokładność**: Klasa 0.5, 1.0

#### Zabezpieczeniowe
- **Funkcja**: Wykrywanie zwarć, przeciążeń
- **Szybkość**: Bardzo szybka odpowiedź
- **Zastosowania**: Automatyka energetyczna

## ⚡ Parametry transformatorów

### Podstawowe parametry

#### Moc znamionowa (VA)
```
S = U₁ × I₁ = U₂ × I₂
```
- **Jednostka**: VA (Volt-Amper)
- **Różnica od Watt**: Uwzględnia reaktancję

#### Napięcia znamionowe
- **Pierwotne**: 230V, 400V (Europa)
- **Wtórne**: 6V, 9V, 12V, 15V, 24V...
- **Tolerancja**: ±5% (biegu jałowym)

#### Prądy znamionowe
```
I₁ = S/U₁
I₂ = S/U₂
```

### Parametry eksploatacyjne

#### Spadek napięcia
- **Przyczyna**: Opór uzwojeń, rozproszenie
- **Wartość**: 3-8% przy obciążeniu znamionowym
- **Regulacja**: (U₀ - Un)/Un × 100%

#### Sprawność
```
η = P₂/P₁ × 100%
```
- **Małe**: 80-90%
- **Średnie**: 90-95%
- **Duże**: 95-98%

#### Straty
- **W rdzeniu**: Histereza, prądy wirowe
- **W uzwojeniach**: I²R (straty ohmowe)
- **Rozproszenie**: Pola magnetyczne

## 🔌 Pomiary i testy

### Test biegu jałowego
- **Wtórne**: Rozłączone (bez obciążenia)
- **Pomiar**: U₁, I₀, P₀
- **Ocena**: Sprawność rdzenia, prąd magnesowania

### Test zwarcia
- **Wtórne**: Zwarte  
- **Pierwotne**: Obniżone napięcie do In
- **Pomiar**: Uk, Ik, Pk
- **Ocena**: Opór uzwojeń, spadek napięcia

### Pomiar przekładni
```
n = U₁/U₂ (w biegu jałowym)
```

### Test izolacji
- **Megger**: 500V lub 1000V
- **Pomiar**: Opór między uzwojeniami
- **Norma**: > 2MΩ (nowe), > 1MΩ (używane)

## ⚠️ Bezpieczeństwo

### Niebezpieczeństwa

#### Wysokie napięcia
- **Uzwojenia**: Mogą mieć kV
- **Rdzeń**: Może być pod napięciem
- **Zawsze sprawdź** przed dotknięciem

#### Prądy wirowe
- **Metalowe przedmioty**: Nagrzewają się w polu
- **Narzędzia**: Mogą się magnetyzować
- **Bransoletki**: Usuń przed pracą

#### Pola magnetyczne
- **Rozruszniki serca**: Minimalna odległość 30cm
- **Karty magnetyczne**: Mogą zostać skasowane
- **Zegarki**: Mogą się zmagnesować

### Środki ochrony

#### Uziemienie rdzenia
- **Ekranowanie**: Rdzeń połączony z PE
- **Ochrona**: Przed napięciami indukowanymi
- **Norma**: Obowiązkowe w urządzeniach klasy I

#### Zabezpieczenia pierwotne
- **Bezpiecznik**: Pierwotny obwód
- **Wyłącznik**: Odłączenie od sieci
- **RCD**: Ochrona przeciwporażeniowa

#### Oznaczenia
- **Fazy uzwojeń**: Kropki, kolory
- **Napięcia**: Wyraźne oznaczenia
- **Ostrzeżenia**: "WYSOKIE NAPIĘCIE"

## 🧮 Obliczenia praktyczne

### Przykład 1: Podstawowy transformator
**Dane**: 230V/12V, 50VA

```
Przekładnia: n = U₁/U₂ = 230V/12V = 19.17
Prąd wtórny: I₂ = S/U₂ = 50VA/12V = 4.17A  
Prąd pierwotny: I₁ = S/U₁ = 50VA/230V = 0.217A
```

### Przykład 2: Dobór bezpiecznika
**Dane**: Transformator 230V/24V, 100VA

```
I₁ = 100VA/230V = 0.43A
Bezpiecznik pierwotny: 0.5A lub 1A (wolny)
Bezpiecznik wtórny: I₂ = 100VA/24V = 4.17A → 5A
```

### Przykład 3: Sprawność
**Dane**: P₁ = 120W, P₂ = 100W

```
η = P₂/P₁ = 100W/120W = 0.833 = 83.3%
Straty = P₁ - P₂ = 120W - 100W = 20W
```

## 🔧 Testowanie i diagnozowanie

### Objawy uszkodzeń

#### Przepalenie uzwojenia
- **Objaw**: Brak napięcia, zapach spalenizny
- **Test**: Pomiar oporu (powinien być ciągły)
- **Przyczyna**: Przeciążenie, zwarcie

#### Zwarcie międzyzwojowe  
- **Objaw**: Niskie napięcie, nagrzewanie
- **Test**: Pomiar przekładni, prąd biegu jałowego
- **Skutek**: Zmniejszona sprawność

#### Uszkodzenie izolacji
- **Objaw**: Wyłączanie RCD, "bije prądem"
- **Test**: Megger (pomiar izolacji)
- **Niebezpieczeństwo**: Porażenie elektryczne

### Diagnostyka praktyczna
1. **Pomiar napięć**: Bez obciążenia i z obciążeniem
2. **Pomiar temperatury**: Po 30 min pracy
3. **Test dźwięku**: Bzyczenie może wskazywać problemy
4. **Inspekcja wizualna**: Ślady przegrzania, korozji

## 📚 Powiązane tematy

- [[cewki_induktory|Cewki (Induktory)]]
- [[prad_staly_przemienny|Prąd Stały vs Przemienny]]
- [[zasilacze|Zasilacze Elektroniczne]]
- [[silniki_elektryczne|Silniki Elektryczne]]
- [[bezpieczenstwo_elektryczne|Bezpieczeństwo Elektryczne]]
- [[multimetr|Multimetr - Pomiary Transformatorów]]

---

#transformatory #elektrotechnika #napięcie #przekładnia #zasilacze #bezpieczeństwo