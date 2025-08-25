# 🧹 Pandas - DataFrame.fillna() - Wypełnianie brakujących wartości

## 📚 Co to jest fillna()?

`fillna()` to funkcja, która wypełnia brakujące wartości (NaN, None) w DataFrame lub Series określonymi wartościami. To jak naprawa dziur w płocie - wypełniasz puste miejsca czymś sensownym! 🔧

## 🔧 Podstawowa składnia

```python
DataFrame.fillna(
    value=None,        # czym wypełnić
    method=None,       # metoda wypełniania  
    axis=None,         # kierunek wypełniania
    inplace=False,     # czy zmienić oryginalny DataFrame
    limit=None         # maksymalna liczba wypełnień z rzędu
)
```

## 💻 Podstawowe przykłady

### 1️⃣ Wypełnianie stałą wartością

```python
import pandas as pd
import numpy as np

# DataFrame z brakującymi wartościami
dane = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': [np.nan, 20, 30, np.nan, 50],
    'C': [100, np.nan, 300, 400, np.nan],
    'D': ['x', 'y', np.nan, 'z', 'w']
})

print("Oryginalne dane:")
print(dane)
print(f"\nBrakujące wartości:\n{dane.isnull().sum()}")

# Wypełnij wszystkie NaN zerem
wypelnione_zero = dane.fillna(0)
print(f"\nWypełnione zerem:")
print(wypelnione_zero)

# Wypełnij różnymi wartościami dla różnych kolumn
wypelnione_dict = dane.fillna({
    'A': 999,           # A wypełnij przez 999
    'B': dane['B'].mean(),  # B wypełnij średnią
    'C': dane['C'].median(), # C wypełnij medianą
    'D': 'BRAK'         # D wypełnij stringiem
})

print(f"\nWypełnione różnymi wartościami:")
print(wypelnione_dict)
```

### 2️⃣ Metody forward fill i backward fill

```python
# Dane czasowe z lukami
daty = pd.date_range('2023-01-01', periods=10, freq='D')
ts_data = pd.DataFrame({
    'data': daty,
    'temperatura': [20, 22, np.nan, np.nan, 25, 23, np.nan, 21, 19, np.nan],
    'wilgotnosc': [60, np.nan, 65, 70, np.nan, np.nan, 75, 72, np.nan, 68]
})

print("Dane czasowe z lukami:")
print(ts_data)

# Forward fill - wypełnij ostatnią znaną wartością
ff_data = ts_data.fillna(method='ffill')  # lub 'pad'
print(f"\nForward fill (ffill):")
print(ff_data)

# Backward fill - wypełnij następną znaną wartością  
bf_data = ts_data.fillna(method='bfill')  # lub 'backfill'
print(f"\nBackward fill (bfill):")
print(bf_data)

# Kombinacja - najpierw ffill, potem bfill
combo_data = ts_data.fillna(method='ffill').fillna(method='bfill')
print(f"\nKombinacja ffill + bfill:")
print(combo_data)
```

### 3️⃣ Interpolacja

```python
# Dane liczbowe do interpolacji
x = np.linspace(0, 10, 11)
y = np.sin(x)

# Wprowadź luki
y_with_gaps = y.copy()
y_with_gaps[[3, 4, 7, 8]] = np.nan

interp_data = pd.DataFrame({
    'x': x,
    'y_original': y,
    'y_with_gaps': y_with_gaps
})

print("Dane do interpolacji:")
print(interp_data)

# Interpolacja liniowa
interp_data['y_linear'] = interp_data['y_with_gaps'].interpolate(method='linear')

# Interpolacja przez średnią
interp_data['y_mean'] = interp_data['y_with_gaps'].fillna(interp_data['y_with_gaps'].mean())

print(f"\nPo interpolacji:")
print(interp_data[['y_original', 'y_with_gaps', 'y_linear', 'y_mean']])
```

## 🎯 Praktyczne przypadki użycia

### 📊 Dane sprzedażowe z lukami

```python
# Dane sprzedaży z brakującymi zapisami
sprzedaz = pd.DataFrame({
    'miesiac': ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06'],
    'produkt_A': [1000, np.nan, 1200, np.nan, 1400, 1500],
    'produkt_B': [800, 850, np.nan, 950, np.nan, np.nan],
    'produkt_C': [np.nan, 600, 650, 700, 750, 800],
    'koszty': [500, 520, np.nan, 550, np.nan, 600]
})

print("Dane sprzedażowe:")
print(sprzedaz)

print(f"\nBrakujące dane per kolumna:")
for col in sprzedaz.columns[1:]:  # pomiń 'miesiac'
    missing = sprzedaz[col].isnull().sum()
    percent = missing / len(sprzedaz) * 100
    print(f"{col}: {missing} ({percent:.1f}%)")

# Strategia wypełniania dla biznesu
sprzedaz_filled = sprzedaz.copy()

# Produkty - interpolacja (trend wzrostowy)
sprzedaz_filled['produkt_A'] = sprzedaz_filled['produkt_A'].interpolate()
sprzedaz_filled['produkt_B'] = sprzedaz_filled['produkt_B'].interpolate()
sprzedaz_filled['produkt_C'] = sprzedaz_filled['produkt_C'].interpolate()

# Koszty - forward fill (ostatnia znana wartość)
sprzedaz_filled['koszty'] = sprzedaz_filled['koszty'].fillna(method='ffill')

print(f"\nPo wypełnieniu:")
print(sprzedaz_filled)

# Oblicz brakujące metryki
sprzedaz_filled['total_przychod'] = (sprzedaz_filled['produkt_A'] + 
                                    sprzedaz_filled['produkt_B'] + 
                                    sprzedaz_filled['produkt_C'])
sprzedaz_filled['zysk'] = sprzedaz_filled['total_przychod'] - sprzedaz_filled['koszty']

print(f"\nZ obliczonymi metrykami:")
print(sprzedaz_filled[['miesiac', 'total_przychod', 'koszty', 'zysk']])
```

### 🏥 Dane medyczne z brakującymi pomiarami

```python
# Dane pacjentów z brakującymi pomiarami
pacjenci = pd.DataFrame({
    'pacjent_id': range(1, 11),
    'wiek': [25, 45, np.nan, 67, 34, np.nan, 56, 23, 78, 41],
    'BMI': [22.5, np.nan, 27.8, 19.2, np.nan, 25.1, np.nan, 21.0, 28.4, 24.7],
    'cisnienie_skurczowe': [120, 140, np.nan, 135, 105, np.nan, 150, 110, np.nan, 125],
    'cisnienie_rozkurczowe': [80, 90, np.nan, 85, 70, np.nan, 95, 75, np.nan, 82],
    'cholesterol': [180, np.nan, 220, np.nan, 160, 200, np.nan, 170, 240, np.nan]
})

print("Dane medyczne z lukami:")
print(pacjenci)

# Analiza brakujących danych
print(f"\nBrakujące wartości:")
missing_summary = pacjenci.isnull().sum()
for col, missing in missing_summary.items():
    if missing > 0:
        percent = missing / len(pacjenci) * 100
        print(f"{col}: {missing} ({percent:.0f}%)")

# Strategia medyczna dla wypełniania
pacjenci_filled = pacjenci.copy()

# Wiek - wypełnij medianą (robust to outliers)
median_age = pacjenci['wiek'].median()
pacjenci_filled['wiek'] = pacjenci_filled['wiek'].fillna(median_age)

# BMI - wypełnij średnią populacyjną (WHO: ~25)
pacjenci_filled['BMI'] = pacjenci_filled['BMI'].fillna(25.0)

# Ciśnienie - wypełnij wartościami standardowymi
pacjenci_filled['cisnienie_skurczowe'] = pacjenci_filled['cisnienie_skurczowe'].fillna(120)
pacjenci_filled['cisnienie_rozkurczowe'] = pacjenci_filled['cisnienie_rozkurczowe'].fillna(80)

# Cholesterol - interpolacja na podstawie wieku
# (uproszczenie: starsi = wyższy cholesterol)
for idx in pacjenci_filled[pacjenci_filled['cholesterol'].isnull()].index:
    wiek = pacjenci_filled.loc[idx, 'wiek']
    estimated_chol = 150 + (wiek - 20) * 1.5  # uproszczony wzór
    pacjenci_filled.loc[idx, 'cholesterol'] = estimated_chol

print(f"\nPo wypełnieniu:")
print(pacjenci_filled)

# Klasyfikacja ryzyka
def klasyfikuj_ryzyko(row):
    risk_score = 0
    if row['wiek'] > 50: risk_score += 1
    if row['BMI'] > 25: risk_score += 1
    if row['cisnienie_skurczowe'] > 140: risk_score += 2
    if row['cholesterol'] > 200: risk_score += 1
    
    if risk_score >= 4: return 'Wysokie'
    elif risk_score >= 2: return 'Średnie'
    else: return 'Niskie'

pacjenci_filled['ryzyko'] = pacjenci_filled.apply(klasyfikuj_ryzyko, axis=1)
print(f"\nZ oceną ryzyka:")
print(pacjenci_filled[['pacjent_id', 'wiek', 'BMI', 'cholesterol', 'ryzyko']])
```

### 🎓 Dane studentów z brakującymi ocenami

```python
# Oceny studentów z niektórymi brakującymi
studenci = pd.DataFrame({
    'student': [f'Student_{i}' for i in range(1, 16)],
    'matematyka': [85, np.nan, 92, 78, np.nan, 88, 91, np.nan, 87, 94, 82, np.nan, 89, 86, 90],
    'fizyka': [78, 82, np.nan, 85, 80, np.nan, 88, 84, np.nan, 91, np.nan, 83, 86, 79, np.nan],
    'chemia': [np.nan, 87, 89, np.nan, 91, 85, np.nan, 92, 88, np.nan, 84, 90, np.nan, 87, 85],
    'frekwencja': [95, 87, 92, np.nan, 98, 85, np.nan, 90, 88, 94, np.nan, 89, 91, np.nan, 96]
})

print("Oceny studentów:")
print(studenci)

# Strategia dla edukacji
studenci_filled = studenci.copy()

# Oceny przedmiotów - wypełnij średnią klasy
for przedmiot in ['matematyka', 'fizyka', 'chemia']:
    srednia_klasy = studenci[przedmiot].mean()
    studenci_filled[przedmiot] = studenci_filled[przedmiot].fillna(srednia_klasy)
    print(f"Średnia klasy - {przedmiot}: {srednia_klasy:.1f}")

# Frekwencja - wypełnij medianą (mniej wrażliwa na outliers)
median_frekwencja = studenci['frekwencja'].median()
studenci_filled['frekwencja'] = studenci_filled['frekwencja'].fillna(median_frekwencja)

print(f"\nPo wypełnieniu średnimi:")
print(studenci_filled)

# Oblicz średnie ważone
studenci_filled['srednia'] = (
    studenci_filled['matematyka'] * 0.4 +  # matematyka 40%
    studenci_filled['fizyka'] * 0.3 +      # fizyka 30%  
    studenci_filled['chemia'] * 0.3        # chemia 30%
)

# Bonus za frekwencję
studenci_filled['srednia_z_bonusem'] = studenci_filled['srednia'] * (
    1 + (studenci_filled['frekwencja'] - 85) / 100 * 0.1  # bonus do 10%
)

print(f"\nWyniki finalne:")
ranking = studenci_filled[['student', 'srednia', 'frekwencja', 'srednia_z_bonusem']].sort_values('srednia_z_bonusem', ascending=False)
print(ranking)
```

## ⚠️ Uwagi i best practices

### 1️⃣ Wybór strategii wypełniania

```python
# Różne strategie dla różnych typów danych
data_types_demo = pd.DataFrame({
    'kategoria': ['A', 'B', np.nan, 'A', np.nan],           # moda
    'wiek': [25, np.nan, 45, np.nan, 67],                   # mediana  
    'dochod': [50000, np.nan, 75000, np.nan, 120000],      # średnia lub interpolacja
    'temperatura': [20.5, np.nan, np.nan, 23.1, np.nan]    # interpolacja
})

print("Różne strategie:")
print("Oryginalne dane:")
print(data_types_demo)

# Moda dla kategorii
moda_kat = data_types_demo['kategoria'].mode()[0]
# Mediana dla wieku (odporna na outliers)
mediana_wiek = data_types_demo['wiek'].median()
# Średnia dla dochodu 
srednia_dochod = data_types_demo['dochod'].mean()
# Interpolacja dla temperatury
temp_interp = data_types_demo['temperatura'].interpolate()

result = data_types_demo.copy()
result['kategoria'] = result['kategoria'].fillna(moda_kat)
result['wiek'] = result['wiek'].fillna(mediana_wiek)
result['dochod'] = result['dochod'].fillna(srednia_dochod)
result['temperatura'] = temp_interp

print(f"\nPo wypełnieniu:")
print(result)
```

## 📝 Podsumowanie

`fillna()` to kluczowe narzędzie data cleaningu:

- 🔧 Wypełnia brakujące wartości (NaN, None)
- 📊 Różne strategie: stała wartość, średnia, mediana, moda
- ⏭️ Metody: `ffill` (forward), `bfill` (backward)  
- 📈 `interpolate()` dla danych liczbowych
- 🎯 Wybór strategii zależy od typu danych i kontekstu biznesowego
- ⚠️ Uważaj na wprowadzanie bias przez nieprawidłowe wypełnianie
- 💡 Zawsze analizuj wzorce brakujących danych przed wypełnianiem

To jak naprawa dziur w danych - ważne żeby robić to mądrze! 🔧✨