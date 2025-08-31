# Elektronika Cyfrowa - Podstawy

## 💻 Definicja

**Elektronika cyfrowa** to dziedzina elektroniki zajmująca się przetwarzaniem sygnałów, które mogą przyjmować tylko dyskretne wartości (najczęściej 0 i 1).

## ⚡ Sygnały cyfrowe vs analogowe

### Sygnał analogowy
```
Napięcie [V]
     ↑
   5 |    ╭─╮
     |   ╱   ╲
   3 |  ╱     ╲
     | ╱       ╲
   1 |╱         ╲
   0 └─────────────→ Czas
```
- **Ciągły zakres** wartości
- **Podatny** na zakłócenia i szumy
- **Przykłady**: Mikrofon, termometr analogowy

### Sygnał cyfrowy
```
Napięcie [V]
     ↑
   5 |  ┌───┐     ┌───┐
     |  │   │     │   │
   3 |  │   │     │   │
     |  │   │     │   │
   1 |  │   └─────┘   │
   0 └──┘─────────────┴──→ Czas
     1   0   0   0   1
```
- **Dyskretne** wartości (0 lub 1)
- **Odporny** na zakłócenia
- **Łatwe** przetwarzanie i przechowywanie

## 🔢 System binarny

### Pozycyjny system liczbowy
```
Pozycja: 7  6  5  4  3  2  1  0
Waga:   128 64 32 16  8  4  2  1
Bit:     1  0  1  1  0  1  0  1
```

**Przykład**: 10110101₂ = 128 + 32 + 16 + 4 + 1 = 181₁₀

### Podstawowe systemy liczbowe

#### Binarny (podstawa 2)
- **Cyfry**: 0, 1
- **Zastosowanie**: Podstawa elektroniki cyfrowej

#### Ósemkowy (podstawa 8)  
- **Cyfry**: 0, 1, 2, 3, 4, 5, 6, 7
- **Zastosowanie**: Uproszczenie zapisu binarnego

#### Szesnastkowy (podstawa 16)
- **Cyfry**: 0-9, A, B, C, D, E, F
- **Przykład**: FF₁₆ = 255₁₀ = 11111111₂
- **Zastosowanie**: Adresy pamięci, kolory (RGB)

## ⚡ Poziomy logiczne

### Standard TTL (Transistor-Transistor Logic)
- **Zasilanie**: 5V
- **Log. 0**: 0V - 0.8V
- **Log. 1**: 2V - 5V
- **Strefa nieokreślona**: 0.8V - 2V
- **Prąd wyjściowy**: ±20mA

### Standard CMOS (3.3V)
- **Zasilanie**: 3.3V
- **Log. 0**: 0V - 1.0V  
- **Log. 1**: 2.3V - 3.3V
- **Pobór prądu**: Bardzo mały (statyczny)

### Kompatybilność poziomów
```
5V TTL → 3.3V CMOS: OK (1 = 5V > 2.3V)
3.3V CMOS → 5V TTL: Problem! (1 = 3.3V < 4V wymagane)

Rozwiązanie: Konwertery poziomów, pull-up do 5V
```

## 🔧 Bramki logiczne

### Bramki podstawowe

#### Bramka NOT (inwersja)
```
Tabela prawdy:
A | Y
--|--
0 | 1
1 | 0

Symbol: ──┤>○── Y = Ā
```

#### Bramka AND (iloczyn logiczny)
```
Tabela prawdy:
A B | Y
----|--
0 0 | 0
0 1 | 0  
1 0 | 0
1 1 | 1

Symbol: ──┐
         &├── Y = A · B
        ──┘
```

#### Bramka OR (suma logiczna)
```
Tabela prawdy:
A B | Y
----|--
0 0 | 0
0 1 | 1
1 0 | 1  
1 1 | 1

Symbol: ──┐
        ≥1├── Y = A + B
        ──┘
```

### Bramki pochodne

#### Bramka NAND (NOT AND)
```
A B | Y
----|--
0 0 | 1
0 1 | 1
1 0 | 1
1 1 | 0

Y = A̅ · B̅ = A·B (prawo De Morgana)
```

#### Bramka NOR (NOT OR)  
```
A B | Y
----|--
0 0 | 1
0 1 | 0
1 0 | 0
1 1 | 0

Y = A̅ + B̅ = A+B (prawo De Morgana)
```

#### Bramka XOR (exclusive OR)
```
A B | Y
----|--
0 0 | 0
0 1 | 1
1 0 | 1
1 1 | 0

Y = A ⊕ B = A·B̅ + Ā·B
```

### Uniwersalność NAND i NOR
- **NAND**: Może zrealizować wszystkie funkcje logiczne
- **NOR**: Również uniwersalna
- **Zastosowanie**: Uproszczenie projektowania układów

## 🔄 Układy kombinacyjne

### Dekoder BCD → 7-segmentowy
```
Wejście BCD:  Wyjście 7-seg:
0000 (0)   →   ╭─a─╮
0001 (1)   →  f│   │b  
0010 (2)   →   ├─g─┤
...            e│   │c
1001 (9)   →   └─d─┘ 
```

### Multiplekser (MUX)
```
     D0 ──┐
     D1 ──┤
     D2 ──┤ MUX ── Y
     D3 ──┤  8:1
     ... ──┘
      │
   A2 A1 A0 (adres)

Y = Dadres (wybór jednego z wielu wejść)
```

### Demultiplekser (DEMUX)
```
          ┌── Y0
          ├── Y1  
Din ── DEMUX ─── Y2
    1:8   ├── Y3
          └── ...
            │
         A2 A1 A0

Yadres = Din (rozesłanie na wybrane wyjście)
```

### Sumator binarny
```
Pełny sumator 1-bitowy:
A B Cin | S Cout
--------|-------
0 0  0  | 0  0
0 0  1  | 1  0  
0 1  0  | 1  0
0 1  1  | 0  1
1 0  0  | 1  0
1 0  1  | 0  1
1 1  0  | 0  1
1 1  1  | 1  1

S = A ⊕ B ⊕ Cin
Cout = A·B + Cin·(A ⊕ B)
```

## 🔄 Układy sekwencyjne

### Przerzutnik RS (Reset-Set)
```
Tabela prawdy:
R S | Q Q̅
----|-----
0 0 | Q Q̅ (pamięć)
0 1 | 1  0 (set)
1 0 | 0  1 (reset)
1 1 | ? ? (zabroniony)
```

### Przerzutnik D (Data)
```
     ┌─── Q
D ───┤D  │
     │   │
CLK ─┤>  │
     └─── Q̅

Q(n+1) = D (przy zboczu CLK)
```

### Przerzutnik JK
```
J K | Q(n+1)
----|--------
0 0 | Q (pamięć)
0 1 | 0 (reset)
1 0 | 1 (set)  
1 1 | Q̅ (toggle)
```

### Liczniki

#### Licznik asynchroniczny (ripple)
```
CLK ──┤FF0├─┤FF1├─┤FF2├─┤FF3├── (4-bitowy)
      Q0   Q1   Q2   Q3
```
- **Szybkość**: Ograniczona opóźnieniami
- **Zastosowanie**: Dzielniki częstotliwości

#### Licznik synchroniczny
```
CLK ──┬─┤FF0├─┬─┤FF1├─┬─┤FF2├─┬─┤FF3├──
      │      │      │      │
    EN0    EN1    EN2    EN3
```
- **Szybkość**: Wszystkie FF przełączają jednocześnie
- **Zastosowanie**: Szybkie liczniki

## 💾 Pamięci cyfrowe

### Klasyfikacja pamięci

#### ROM (Read-Only Memory)
- **PROM**: Programowalne jednorazowo
- **EPROM**: Kasowalne UV (okienko)
- **EEPROM**: Elektrycznie kasowalne
- **Flash**: Szybkie kasowanie blokowe

#### RAM (Random Access Memory)  
- **SRAM**: Statyczna (przerzutniki)
- **DRAM**: Dynamiczna (kondensatory)
- **NVRAM**: Nieulotna RAM (bateria backup)

### Organizacja pamięci
```
Adres: A15 A14 ... A1 A0 (16-bit)
       │                │
      MSB              LSB

Dekoder adresów → wybór komórki
Magistrala danych ↔ D7 D6 ... D1 D0
Sygnały sterujące: /CS /RD /WR
```

## ⚡ Przykłady zastosowań

### Sterownik 7-segmentowy
```
Arduino → BCD (4 bity) → Dekoder → 7-segment LED

Kod Arduino:
for (int i = 0; i < 16; i++) {
  digitalWrite(BCD0, i & 1);
  digitalWrite(BCD1, (i >> 1) & 1);
  digitalWrite(BCD2, (i >> 2) & 1);  
  digitalWrite(BCD3, (i >> 3) & 1);
  delay(1000);
}
```

### Licznik z wyświetlaczem
```
CLK → Licznik 4-bit → Dekoder BCD → 7-segment
                   ↓
              Przerzutniki D (zatrzask)
```

### Prosty kalkulator
```
Wejście A (4-bit) ─┐
                   ├─ Sumator → Wynik (5-bit)
Wejście B (4-bit) ─┘
```

## 🔧 Narzędzia projektowe

### Symulatory
- **Logisim**: Darmowy, edukacyjny
- **Proteus**: Profesjonalny, płatny
- **Tinkercad**: Online, prosty

### Języki opisu sprzętu
- **VHDL**: IEEE standard
- **Verilog**: Popularny w przemyśle
- **SystemVerilog**: Rozszerzenie Verilog

### Układy programowalne
- **PAL**: Proste bramki + przerzutniki
- **FPGA**: Field-Programmable Gate Array
- **CPLD**: Complex Programmable Logic Device

## 🧮 Ćwiczenia praktyczne

### Ćwiczenie 1: Konwersje liczbowe
1. 10110101₂ → ?₁₀
2. 173₁₀ → ?₂
3. A5₁₆ → ?₁₀ → ?₂

### Ćwiczenie 2: Projektowanie
Zaprojektuj układ sygnalizacji świetlnej (3 LED) z licznikiem:
- Stan 001: Zielony
- Stan 010: Żółty  
- Stan 100: Czerwony

### Ćwiczenie 3: Sumator
Zbuduj 4-bitowy sumator z wyświetlaniem wyniku na LED.

## 📚 Powiązane tematy

- [[arduino_podstawy|Arduino - Programowanie]]
- [[raspberry_pi|Raspberry Pi - GPIO]]
- [[mikrokontrolery|Mikrokontrolery]]
- [[elektronika_analogowa|Elektronika Analogowa]]
- [[lutowanie|Lutowanie - Układy Cyfrowe]]
- [[multimetr|Multimetr - Pomiary Cyfrowe]]

---

#elektronika-cyfrowa #bramki-logiczne #binarne #TTL #CMOS #pamięci #liczniki