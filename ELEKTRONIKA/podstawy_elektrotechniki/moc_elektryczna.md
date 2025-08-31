# Moc Elektryczna

## ⚡ Definicja

**Moc elektryczna** to szybkość przekształcania energii elektrycznej w inne formy energii (ciepło, światło, ruch).

## 📊 Wzory podstawowe

### Moc w obwodach DC
```
P = U × I
P = I² × R  
P = U² / R
```

Gdzie:
- **P** - moc [W - Wat]
- **U** - napięcie [V]
- **I** - prąd [A]
- **R** - opór [Ω]

### Jednostki mocy
- **Watt [W]** - podstawowa jednostka
- **Kilowatt [kW]** = 1000 W
- **Megawatt [MW]** = 1 000 000 W
- **Koń mechaniczny [KM]** = 736 W

## 🔋 Energia elektryczna

### Wzór na energię
```
E = P × t
```

Gdzie:
- **E** - energia [Wh - Watogodzina]
- **P** - moc [W]
- **t** - czas [h]

### Jednostki energii
- **Watogodzina [Wh]**
- **Kilowatogodzina [kWh]** - jednostka rozliczeniowa energii
- **Dżul [J]** - 1 Wh = 3600 J

## 🏠 Moc w gospodarstwie domowym

### Typowe moce urządzeń

| Urządzenie | Moc |
|-----------|-----|
| **Żarówka LED** | 5-15 W |
| **Żarówka tradycyjna** | 60-100 W |
| **Telewizor LCD** | 100-200 W |
| **Lodówka** | 150-300 W |
| **Pralka** | 2000-2500 W |
| **Czajnik elektryczny** | 1500-2500 W |
| **Mikrofalówka** | 800-1200 W |
| **Grzejnik elektryczny** | 1000-2000 W |

### Obliczanie kosztów energii
```
Koszt = Moc [kW] × Czas [h] × Cena [zł/kWh]
```

**Przykład:** Żarówka 60W przez 5h dziennie
- Energia dziennie: 0.06 kW × 5h = 0.3 kWh
- Koszt miesięczny: 0.3 × 30 × 0.6 zł/kWh = 5.4 zł

## 🌊 Moc w obwodach AC

### Moc rzeczywista (aktywna)
```
P = U × I × cos φ [W]
```

### Moc pozorna
```
S = U × I [VA - Woltamper]
```

### Moc bierna
```
Q = U × I × sin φ [VAR - Woltamper reaktancyjny]
```

### Współczynnik mocy (cos φ)
- **cos φ = 1** - obwód czysto ohmiczny (najlepiej)
- **cos φ = 0.8** - typowy dla silników indukcyjnych
- **cos φ = 0** - obwód czysto reaktancyjny

## 🔧 Przykłady obliczeniowe

### Przykład 1: Moc żarówki
**Dane:** U = 230V, R = 529Ω (żarówka 100W)

```
P = U² / R = 230² / 529 = 100W ✓
I = U / R = 230 / 529 = 0.43A
```

### Przykład 2: Moc silnika AC
**Dane:** U = 400V, I = 10A, cos φ = 0.8

```
P = U × I × cos φ = 400 × 10 × 0.8 = 3200W = 3.2kW
```

### Przykład 3: Koszt pralki
**Dane:** Pralka 2kW, 3 prania tygodniowo po 2h, cena 0.6 zł/kWh

```
Energia miesięczna = 2kW × 2h × 3 × 4 = 48 kWh
Koszt miesięczny = 48 × 0.6 = 28.8 zł
```

## ⚡ Strata mocy

### Straty w przewodach
```
Pstraty = I² × Rprzewodu
```

**Dlaczego przesyła się energię wysokim napięciem?**
- Przy stałej mocy: P = U × I
- Wyższe U → niższe I → mniejsze straty I²R

### Sprawność
```
η = Pużyteczna / Pdostarczana × 100%
```

**Przykłady sprawności:**
- **Silniki elektryczne**: 85-95%
- **Zasilacze impulsowe**: 80-90%
- **Żarówki LED**: 80-90%
- **Żarówki tradycyjne**: 5-10%

## 🏭 Klasyfikacja odbiorników

### Odbiorniki ohmiczne
- **Charakterystyka**: Moc zamienia się w ciepło
- **Przykłady**: Grzejniki, żarówki, czajniki
- **cos φ = 1** (najlepsze dla sieci)

### Odbiorniki indukcyjne  
- **Charakterystyka**: Zawierają cewki
- **Przykłady**: Silniki, transformatory, świetlówki
- **cos φ < 1** (obciążają sieć mocą bierną)

### Odbiorniki pojemnościowe
- **Charakterystyka**: Zawierają kondensatory
- **Przykłady**: Zasilacze impulsowe, oświetlenie LED
- **cos φ** - może być niski (zniekształcenia)

## ⚠️ Bezpieczeństwo i praktyka

### Zabezpieczenia przeciążeniowe
- **Bezpieczniki** - topikowe lub automatyczne
- **Wyłączniki nadprądowe** - typ B, C, D
- **Wyłączniki różnicowoprądowe** - ochrona przed porażeniem

### Dobór przekroju przewodów
**Przykład:** Obwód 16A (3680W przy 230V)
- Przewód miedziane: 2.5 mm²
- Zabezpieczenie: 16A (typ B lub C)
- Maksymalna moc: 16A × 230V = 3680W

### Przeciążenia
**Objawy przeciążenia:**
- Nagrzewanie się przewodów/gniazdek
- Migotanie światła przy włączaniu urządzeń
- Zadziałanie zabezpieczeń

## 🧮 Ćwiczenia praktyczne

### Zadanie 1
Oblicz miesięczny koszt świecenia LED 10W przez 8h dziennie przy cenie 0.65 zł/kWh.

### Zadanie 2
Jaki prąd pobiera czajnik 2200W z sieci 230V? Czy można go podłączyć do gniazdka 10A?

### Zadanie 3
Silnik o mocy 5kW i cos φ = 0.8 jest zasilany napięciem 400V. Oblicz prąd i moc pozorną.

## 📚 Powiązane tematy

- [[prawo_ohma|Prawo Ohma]]
- [[napiecie_prad_opor|Napięcie, Prąd i Opór]]
- [[prad_staly_przemienny|Prąd Stały vs Przemienny]]
- [[zabezpieczenia_elektryczne|Zabezpieczenia Elektryczne]]
- [[instalacje_elektryczne|Instalacje Elektryczne]]
- [[silniki_elektryczne|Silniki Elektryczne]]

---

#elektrotechnika #moc-elektryczna #energia #koszty #sprawność #bezpieczeństwo