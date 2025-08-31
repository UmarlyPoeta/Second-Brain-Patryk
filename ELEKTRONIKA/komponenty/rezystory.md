# Rezystory

## 🔧 Definicja

**Rezystor** to element elektroniczny o określonym oporze elektrycznym, służący do ograniczania prądu lub tworzenia spadku napięcia w obwodzie.

## 📊 Podstawowe parametry

### Opór nominalny (R)
- **Jednostka**: Ohm [Ω], kΩ, MΩ
- **Standardowe wartości**: Seria E12, E24, E96
- **Tolerancja**: ±1%, ±5%, ±10%

### Moc nominalna (P)
- **Typowe wartości**: 0.125W, 0.25W, 0.5W, 1W, 2W, 5W
- **Wzór**: P = I²R = U²/R
- **Bezpieczeństwo**: Używać rezystor o 2x większej mocy niż obliczona

### Napięcie maksymalne
- **Wzór**: Umax = √(P × R)
- **Przykład**: Rezystor 1MΩ/0.25W → Umax = 500V

## 🎨 Kod kolorów rezystorów

### Rezystory 4-pasmowe
| Kolor | 1. pasek | 2. pasek | 3. pasek (mnożnik) | 4. pasek (tolerancja) |
|-------|----------|----------|-------------------|----------------------|
| **Czarny** | 0 | 0 | ×1 | - |
| **Brązowy** | 1 | 1 | ×10 | ±1% |
| **Czerwony** | 2 | 2 | ×100 | ±2% |
| **Pomarańczowy** | 3 | 3 | ×1k | - |
| **Żółty** | 4 | 4 | ×10k | - |
| **Zielony** | 5 | 5 | ×100k | ±0.5% |
| **Niebieski** | 6 | 6 | ×1M | ±0.25% |
| **Fioletowy** | 7 | 7 | ×10M | ±0.1% |
| **Szary** | 8 | 8 | - | ±0.05% |
| **Biały** | 9 | 9 | - | - |
| **Złoty** | - | - | ×0.1 | ±5% |
| **Srebrny** | - | - | ×0.01 | ±10% |

### Przykład odczytu
**Rezystor**: Czerwony-Fioletowy-Brązowy-Złoty
- Czerwony = 2
- Fioletowy = 7  
- Brązowy = ×10
- Złoty = ±5%
- **Wynik**: 27 × 10 = 270Ω ±5%

## 🏗️ Rodzaje rezystorów

### Ze względu na materiał

#### Rezystory węglowe
- **Materiał**: Węgiel + spoiwo
- **Moc**: 0.125W - 2W
- **Tolerancja**: ±5% - ±10%
- **Zastosowania**: Ogólne, tanie aplikacje

#### Rezystory metalowe
- **Materiał**: Cienka warstwa metalu
- **Moc**: 0.125W - 1W  
- **Tolerancja**: ±1% - ±5%
- **Cechy**: Stabilne temperaturowo, dokładne

#### Rezystory drutowe
- **Materiał**: Drut oporowy na rdzeniu ceramicznym
- **Moc**: 1W - 100W i więcej
- **Zastosowania**: Duże prądy, precision shunts

### Ze względu na charakterystykę

#### Rezystory liniowe (stałe)
- **Charakterystyka**: R = const
- **Najczęstsze**: 90% wszystkich rezystorów

#### Rezystory nieliniowe

##### Termistory
- **NTC** - opór maleje z temperaturą
- **PTC** - opór rośnie z temperaturą
- **Zastosowania**: Pomiary temperatury, ograniczanie prądu rozruchowego

##### Warystory (VDR)
- **Charakterystyka**: Opór maleje z napięciem
- **Zastosowania**: Zabezpieczenia przepięciowe

##### Fotoreziory (LDR)
- **Charakterystyka**: Opór maleje z oświetleniem
- **Zastosowania**: Czujniki światła, automat oświetleniowy

#### Rezystory zmienne

##### Potencjometry
- **Budowa**: 3 wyprowadzenia
- **Zastosowania**: Regulatory głośności, brightness
- **Charakterystyka**: Liniowa (A), logarytmiczna (B), wykładnicza (C)

##### Trymer/preset
- **Budowa**: Małe potencjometry do PCB
- **Zastosowania**: Kalibracja, dostrójka układów

## 🔌 Połączenia rezystorów

### Połączenie szeregowe
```
R₁ ── R₂ ── R₃
```
**Wzór**: Rcałk = R₁ + R₂ + R₃
**Prąd**: Taki sam przez wszystkie
**Napięcie**: Dzieli się proporcjonalnie do oporów

### Połączenie równoległe
```
R₁ ──┐
     ├── Rcałk
R₂ ──┘
```
**Wzór**: 1/Rcałk = 1/R₁ + 1/R₂ + 1/R₃
**Napięcie**: Takie samo na wszystkich
**Prąd**: Dzieli się odwrotnie proporcjonalnie do oporów

### Wzory praktyczne
**Dwa rezystory równolegle**:
```
Rcałk = (R₁ × R₂)/(R₁ + R₂)
```

## 💡 Zastosowania praktyczne

### Ograniczanie prądu LED
```
RLED = (Uzasilania - ULED) / ILED
```
**Przykład**: LED 2V/20mA, zasilanie 5V
```
R = (5V - 2V) / 0.02A = 150Ω
```

### Dzielnik napięcia
```
      R₁
Uin ──────┬── Uout = Uin × R₂/(R₁+R₂)
      R₂  │
         ═══ GND
```

### Pull-up / Pull-down
- **Pull-up**: Rezystor 10kΩ między pinem a VCC
- **Pull-down**: Rezystor 10kΩ między pinem a GND
- **Zastosowania**: Przyciski, linie komunikacyjne (I²C)

## 🔥 Moc i nagrzewanie

### Obliczanie mocy
```
P = I²R = U²/R = U × I
```

### Wybór mocy rezystora
**Zasada bezpieczeństwa**: Pmaksymalna ≥ 2 × Pobliczona

**Przykład**: Rezystor 100Ω przy 12V
```
P = U²/R = 144/100 = 1.44W
Wybieramy: Rezystor 2W lub więcej
```

### Temperatura pracy
- **Maksymalna temperatura**: 70°C (rezystory standardowe)
- **Derating**: Obniżenie mocy przy wysokich temperaturach
- **Chłodzenie**: Radiatory dla rezystorów mocowych

## ⚠️ Częste błędy

1. **Za mała moc** → przepalenie rezystora
2. **Zła tolerancja** → nieprawidłowe działanie układu
3. **Odczyt kolorów** → pomylenie brązowego z czerwonym
4. **Połączenia** → pomylenie szeregowego z równoległym

## 🧮 Ćwiczenia

### Zadanie 1
Oblicz opór zastępczy:
- Trzy rezystory 1kΩ połączone szeregowo
- Trzy rezystory 1kΩ połączone równolegle

### Zadanie 2  
Zaprojektuj dzielnik napięcia 12V → 5V przy obciążeniu 100mA.

### Zadanie 3
Dobierz rezystor dla LED: 3.3V/20mA z zasilaniem 9V.

## 📚 Powiązane tematy

- [[prawo_ohma|Prawo Ohma]]
- [[obwody_szeregowe_rownoleg|Obwody Szeregowe i Równoległe]]
- [[moc_elektryczna|Moc Elektryczna]]
- [[kondensatory|Kondensatory]]
- [[multimetr|Multimetr - Pomiar Oporu]]
- [[lutowanie|Lutowanie Elementów]]

---

#elektronika #rezystory #komponenty #kod-kolorów #moc #opór