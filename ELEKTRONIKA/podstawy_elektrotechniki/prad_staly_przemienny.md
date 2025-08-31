# Prąd Stały vs Prąd Przemienny

## ⚡ Prąd stały (DC - Direct Current)

### Definicja
**Prąd stały** to prąd o stałym kierunku i (zazwyczaj) stałej wartości natężenia.

### Charakterystyka
- **Kierunek**: Nie zmienia się w czasie
- **Wartość**: Stała lub powoli zmienna
- **Symbol**: DC lub ⎓
- **Źródła**: Baterie, akumulatory, zasilacze DC

### Przebieg czasowy
```
Prąd [A]
  ↑
  |  ┌─────────────────────
  |  │
  |  │
  └──┴─────────────────→ Czas [s]
     0
```

### Zastosowania DC
- **Elektronika**: Wszystkie układy cyfrowe, mikrokontrolery
- **Motoryzacja**: Instalacje 12V/24V w pojazdach
- **Telekomunikacja**: Sieci telefoniczne, Internet
- **Oświetlenie LED**: Diody wymagają prądu stałego
- **Baterie**: Ładowanie i rozładowanie

## 🌊 Prąd przemienny (AC - Alternating Current)

### Definicja
**Prąd przemienny** to prąd zmieniający kierunek i wartość w sposób okresowy, najczęściej sinusoidalnie.

### Charakterystyka
- **Kierunek**: Zmienia się okresowo
- **Wartość**: Zmienia się sinusoidalnie
- **Symbol**: AC lub ~
- **Częstotliwość**: 50 Hz (Europa), 60 Hz (USA/Kanada)

### Przebieg czasowy (sinusoida)
```
Prąd [A]
  ↑
  |    ╭─╮       ╭─╮
  |   ╱   ╲     ╱   ╲
  ├──╱─────╲───╱─────╲──→ Czas [s]
  | ╱       ╲ ╱       ╲
  |╱         ╲╱         ╲
  ↓           ╲╱
              
Okres T = 20ms (50Hz)
```

### Parametry AC

#### Częstotliwość (f)
```
f = 1/T
```
- **50 Hz** - Europa, Azja, Afryka
- **60 Hz** - Ameryka Północna i Południowa

#### Wartości napięcia AC

##### Wartość chwilowa
```
u(t) = Um × sin(2πft + φ)
```

##### Wartość skuteczna (RMS)
```
U = Um / √2 ≈ 0,707 × Um
```

**Przykład dla sieci 230V:**
- U = 230V (wartość skuteczna)
- Um = 230V × √2 ≈ 325V (wartość szczytowa)

## ⚖️ Porównanie DC vs AC

| Parametr | Prąd stały (DC) | Prąd przemienny (AC) |
|----------|-----------------|---------------------|
| **Kierunek** | Stały | Zmienny |
| **Transformacja** | Trudna (konwertery) | Łatwa (transformatory) |
| **Przesyłanie energii** | Straty w przewodach | Efektywne na długie odległości |
| **Bezpieczeństwo** | Mniej niebezpieczny | Bardziej niebezpieczny |
| **Magazynowanie** | Możliwe (baterie) | Niemożliwe bezpośrednio |
| **Silniki** | Prostsza regulacja | Większa moc |

## 🔄 Konwersja DC ↔ AC

### Prostowniki (AC → DC)
Przekształcają prąd przemienny na stały:

#### Prostownik jednopołówkowy
```
AC ──┤ D ├── DC
```
- Przepuszcza tylko jedną połówkę sinusoidy
- Niska sprawność (~40%)

#### Prostownik dwupołówkowy (mostek)
```
    D1   D2
AC ──┤├───┤├── DC+
  │        │
  └─┤├───┤├── DC-
    D4   D3
```
- Wykorzystuje obie połówki sinusoidy  
- Wysoka sprawność (~90%)

### Falowniki (DC → AC)
Przekształcają prąd stały na przemienny:
- **Falownik sinusoidalny** - czysty AC (drogi)
- **Falownik prostokątny** - prosty AC (tańszy)
- **Falownik PWM** - modulacja szerokości impulsów

## 🏠 Zastosowania praktyczne

### Instalacje domowe (230V AC)
- **Oświetlenie** - żarówki, świetlówki, halogeny
- **AGD** - pralki, lodówki, kuchenki
- **Grzanie** - grzejniki, bojlery
- **Silniki** - pompy, wentylatory

### Elektronika (różne napięcia DC)
- **5V** - USB, Arduino, Raspberry Pi
- **12V** - LED, wentylatory komputerowe, motoryzacja
- **3.3V** - mikrokontrolery, czujniki
- **1.5V** - baterie AA/AAA

## ⚠️ Bezpieczeństwo

### Prąd stały
- **Skurcz mięśni** - łatwiej puścić przewód
- **Oparzenia** - lokalnie w miejscu kontaktu
- **Elektroliza** - rozkład tkanek

### Prąd przemienny  
- **Skurcz mięśni** - trudniej puścić przewód (50Hz)
- **Migotanie serca** - bardzo niebezpieczne
- **Porażenie** - bardziej odczuwalne

### Pierwsze pomoc
1. **Przerwij dopływ prądu** - wyłącz bezpiecznik
2. **Nie dotykaj** poszkodowanego gdy jest pod napięciem
3. **Wezwij pomoc** - 112 lub 999
4. **RKO** - jeśli nie oddycha

## 🧮 Obliczenia praktyczne

### Przykład 1: Moc w obwodzie DC
**Dane:** U = 12V, I = 2A
```
P = U × I = 12V × 2A = 24W
```

### Przykład 2: Moc w obwodzie AC
**Dane:** U = 230V (skuteczne), I = 1A, cos φ = 0.8
```
P = U × I × cos φ = 230V × 1A × 0.8 = 184W
```

## 📚 Powiązane tematy

- [[napiecie_prad_opor|Napięcie, Prąd i Opór]]
- [[moc_elektryczna|Moc Elektryczna]]
- [[transformatory|Transformatory]]
- [[diody|Diody i Prostowniki]]
- [[zasilacze|Zasilacze Elektroniczne]]
- [[bezpieczenstwo_elektryczne|Bezpieczeństwo Elektryczne]]

---

#elektrotechnika #prąd-stały #prąd-przemienny #AC #DC #bezpieczeństwo