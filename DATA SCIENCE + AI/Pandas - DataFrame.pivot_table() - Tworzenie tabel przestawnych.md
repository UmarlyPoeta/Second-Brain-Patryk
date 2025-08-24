# 🔄 Pandas - DataFrame.pivot_table() - Tworzenie tabel przestawnych

## 📚 Co to jest DataFrame.pivot_table()?

`DataFrame.pivot_table()` to super funkcja, która tworzy tabele przestawne - jak w Excelu! To narzędzie, które przekształca i podsumowuje dane, grupując je w intuicyjny sposób. To jak magiczny organizator danych! 📊✨

## 🔧 Podstawowa składnia

```python
import pandas as pd

# Podstawowa składnia
DataFrame.pivot_table(
    values=None,        # kolumny do agregacji
    index=None,         # wiersze tabeli
    columns=None,       # kolumny tabeli  
    aggfunc='mean',     # funkcja agregująca
    fill_value=None,    # czym wypełnić NaN
    margins=False       # czy dodać sumy
)
```

## 💻 Praktyczne przykłady

### 1️⃣ Podstawowa tabela przestawna

```python
import pandas as pd
import numpy as np

# Dane sprzedażowe
dane = {
    'Sprzedawca': ['Anna', 'Jan', 'Anna', 'Jan', 'Maria', 'Maria', 'Anna', 'Jan'],
    'Region': ['Północ', 'Południe', 'Północ', 'Południe', 'Wschód', 'Zachód', 'Wschód', 'Północ'],
    'Produkt': ['Laptop', 'Laptop', 'Telefon', 'Telefon', 'Laptop', 'Telefon', 'Laptop', 'Telefon'],
    'Sprzedaz': [15000, 12000, 8000, 9000, 18000, 7500, 16000, 8500],
    'Ilosc': [5, 4, 8, 9, 6, 15, 8, 17]
}

df = pd.DataFrame(dane)
print("Dane sprzedażowe:")
print(df)

# Podstawowa pivot table - sprzedaż per sprzedawca i region
pivot_basic = df.pivot_table(
    values='Sprzedaz',           # co agregujemy
    index='Sprzedawca',          # wiersze
    columns='Region',            # kolumny
    aggfunc='sum'                # jak agregujemy
)

print(f"\nSprzedaż per sprzedawca i region:")
print(pivot_basic)
```

### 2️⃣ Tabela z wieloma funkcjami agregacji

```python
# Tabela z różnymi statystykami
pivot_multi = df.pivot_table(
    values='Sprzedaz',
    index='Sprzedawca',
    columns='Produkt',
    aggfunc=['sum', 'mean', 'count'],    # kilka funkcji naraz
    fill_value=0                         # zastąp NaN zerami
)

print("Wielofunkcyjna tabela przestawna:")
print(pivot_multi)

# Dostęp do konkretnej funkcji
print(f"\nTylko sumy:")
print(pivot_multi['sum'])
```

### 3️⃣ Tabela z marginesami (totals)

```python
# Tabela z sumami brzegowymi
pivot_margins = df.pivot_table(
    values='Sprzedaz',
    index='Sprzedawca',
    columns='Region',
    aggfunc='sum',
    fill_value=0,
    margins=True,            # dodaj sumy brzegowe
    margins_name='TOTAL'     # nazwa dla sum brzegowych
)

print("Tabela z marginesami:")
print(pivot_margins)
```

## 🎯 Praktyczne przypadki użycia

### 📊 Analiza sprzedaży miesięcznej

```python
# Dane sprzedaży miesięcznej
np.random.seed(42)
daty = pd.date_range('2023-01-01', '2023-12-31', freq='D')
sprzedaz_data = []

produkty = ['Laptop', 'Telefon', 'Tablet', 'Słuchawki']
regiony = ['Północ', 'Południe', 'Wschód', 'Zachód']

# Generuj dane
for _ in range(1000):
    data = np.random.choice(daty)
    sprzedaz_data.append({
        'Data': data,
        'Miesiac': data.month,
        'Kwartal': f'Q{(data.month-1)//3 + 1}',
        'Produkt': np.random.choice(produkty),
        'Region': np.random.choice(regiony),
        'Sprzedaz': np.random.randint(1000, 10000)
    })

df_sales = pd.DataFrame(sprzedaz_data)
print(f"Dataset sprzedaży: {df_sales.shape}")
print(df_sales.head())

# Sprzedaż per produkt i kwartał
sprzedaz_kwartal = df_sales.pivot_table(
    values='Sprzedaz',
    index='Produkt',
    columns='Kwartal',
    aggfunc='sum',
    fill_value=0,
    margins=True
)

print(f"\nSprzedaż per produkt i kwartał:")
print(sprzedaz_kwartal)

# Najlepszy kwartał dla każdego produktu
print(f"\nNajlepszy kwartał per produkt:")
for produkt in produkty:
    if produkt in sprzedaz_kwartal.index:
        # Usuń kolumnę TOTAL z analizy
        kwartal_data = sprzedaz_kwartal.loc[produkt, ['Q1', 'Q2', 'Q3', 'Q4']]
        najlepszy = kwartal_data.idxmax()
        najlepsza_wartosc = kwartal_data.max()
        print(f"{produkt:12}: {najlepszy} ({najlepsza_wartosc:,} PLN)")
```

### 🏥 Analiza danych medycznych

```python
# Dane pacjentów
dane_medyczne = {
    'Pacjent_ID': range(1, 101),
    'Wiek_Grupa': np.random.choice(['20-30', '31-40', '41-50', '51-60'], 100),
    'Plec': np.random.choice(['M', 'K'], 100),
    'Choroba': np.random.choice(['Nadciśnienie', 'Cukrzyca', 'Migotanie', 'Zdrowy'], 100, 
                               p=[0.3, 0.25, 0.15, 0.3]),
    'Koszt_Leczenia': np.random.randint(500, 5000, 100),
    'Czas_Leczenia': np.random.randint(1, 30, 100)
}

df_med = pd.DataFrame(dane_medyczne)
print("Dane medyczne (pierwsze 10):")
print(df_med.head(10))

# Średni koszt leczenia per choroba i grupa wiekowa
koszt_pivot = df_med.pivot_table(
    values='Koszt_Leczenia',
    index='Choroba',
    columns='Wiek_Grupa',
    aggfunc='mean',
    fill_value=0
).round(0)

print(f"\nŚredni koszt leczenia per choroba i wiek:")
print(koszt_pivot)

# Ilość przypadków per płeć i choroba
ilosc_pivot = df_med.pivot_table(
    values='Pacjent_ID',
    index='Choroba',
    columns='Plec',
    aggfunc='count',
    fill_value=0,
    margins=True
)

print(f"\nIlość przypadków per płeć i choroba:")
print(ilosc_pivot)
```

### 📈 Analiza wyników finansowych

```python
# Dane finansowe firm
firmy_data = []
firmy = ['TechCorp', 'FinanceInc', 'RetailCo', 'ManufacturingLtd']
lata = [2020, 2021, 2022, 2023]
kwartaly = ['Q1', 'Q2', 'Q3', 'Q4']

for firma in firmy:
    for rok in lata:
        for kwartal in kwartaly:
            # Symuluj trend wzrostowy
            base = np.random.randint(1000000, 5000000)
            trend = (rok - 2020) * 100000  # wzrost rok do roku
            seasonal = {'Q1': -200000, 'Q2': 0, 'Q3': 100000, 'Q4': 300000}[kwartal]
            
            firmy_data.append({
                'Firma': firma,
                'Rok': rok,
                'Kwartal': kwartal,
                'Przychody': base + trend + seasonal + np.random.randint(-500000, 500000),
                'Zysk': (base + trend + seasonal) * 0.15 + np.random.randint(-100000, 100000)
            })

df_firmy = pd.DataFrame(firmy_data)
print(f"Dane finansowe firm: {df_firmy.shape}")
print(df_firmy.head())

# Przychody per firma i rok
przychody_rok = df_firmy.pivot_table(
    values='Przychody',
    index='Firma',
    columns='Rok',
    aggfunc='sum',
    margins=True
).round(0)

print(f"\nPrzychody per firma i rok (PLN):")
print(przychody_rok)

# Rentowność (Zysk/Przychody) per firma i kwartał
df_firmy['Rentownosc'] = df_firmy['Zysk'] / df_firmy['Przychody'] * 100

rentownosc_pivot = df_firmy.pivot_table(
    values='Rentownosc',
    index='Firma',
    columns='Kwartal',
    aggfunc='mean'
).round(1)

print(f"\nŚrednia rentowność per firma i kwartał (%):")
print(rentownosc_pivot)
```

## 🔍 Zaawansowane użycie

### 1️⃣ Wielopoziomowe indeksy i kolumny

```python
# Tworzenie pivot z hierarchicznymi indeksami
pivot_hierarch = df_sales.pivot_table(
    values='Sprzedaz',
    index=['Region', 'Produkt'],      # wielopoziomowy index
    columns='Kwartal',
    aggfunc=['sum', 'count'],         # wielopoziomowe kolumny
    fill_value=0
)

print("Tabela z hierarchicznymi indeksami i kolumnami:")
print(pivot_hierarch.head(10))

# Dostęp do konkretnych poziomów
print(f"\nTylko sumy:")
print(pivot_hierarch['sum'].head())

# Dane dla konkretnego regionu
print(f"\nDane dla Północy:")
polnoc_data = pivot_hierarch.loc['Północ'] if 'Północ' in pivot_hierarch.index else "Brak danych"
if isinstance(polnoc_data, pd.DataFrame):
    print(polnoc_data)
```

### 2️⃣ Custom funkcje agregacji

```python
# Definiuj własne funkcje agregacji
def cv(x):
    """Coefficient of variation (odchylenie standardowe / średnia)"""
    return x.std() / x.mean() if x.mean() != 0 else 0

def range_func(x):
    """Rozstęp (max - min)"""
    return x.max() - x.min()

# Pivot z custom funkcjami
pivot_custom = df_sales.pivot_table(
    values='Sprzedaz',
    index='Produkt',
    columns='Region',
    aggfunc=[np.mean, np.std, cv, range_func],
    fill_value=0
).round(2)

print("Tabela z custom funkcjami:")
print(pivot_custom)
```

### 3️⃣ Formatowanie i stylowanie

```python
# Pivot dla przykładu formatowania
format_pivot = df_med.pivot_table(
    values='Koszt_Leczenia',
    index='Choroba',
    columns='Plec',
    aggfunc='mean',
    fill_value=0
).round(0)

print("Tabela do formatowania:")
print(format_pivot)

# Zastosuj styling (przykład - nie będzie działać w terminalu)
# styled = format_pivot.style.format('{:,.0f} PLN').background_gradient()
```

## ⚠️ Częste błędy i pułapki

### 1️⃣ Duplikaty w indeksach

```python
# Dane z duplikatami
dane_duplikaty = pd.DataFrame({
    'A': ['X', 'X', 'Y'],  # duplikat X
    'B': ['M', 'M', 'N'],  # duplikat M dla X
    'C': [1, 2, 3]
})

print("Dane z duplikatami:")
print(dane_duplikaty)

# Pivot może dać nieoczekiwane wyniki
try:
    pivot_dup = dane_duplikaty.pivot_table(
        values='C',
        index='A', 
        columns='B',
        aggfunc='sum'  # suma rozwiąże duplikaty
    )
    print(f"Pivot z duplikatami (suma):")
    print(pivot_dup)
except Exception as e:
    print(f"Błąd: {e}")
```

### 2️⃣ Brakujące kombinacje

```python
# Nie wszystkie kombinacje istnieją
sparse_data = pd.DataFrame({
    'A': ['X', 'X', 'Y'],
    'B': ['M', 'N', 'M'],  # brak Y-N kombinacji
    'C': [1, 2, 3]
})

pivot_sparse = sparse_data.pivot_table(
    values='C',
    index='A',
    columns='B',
    fill_value='BRAK'  # wypełnij brakujące
)

print("Pivot z brakującymi kombinacjami:")
print(pivot_sparse)
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Zawsze określaj aggfunc explicite
good_pivot = df.pivot_table(
    values='Sprzedaz',
    index='Sprzedawca',
    columns='Region',
    aggfunc='sum'  # jasno określone
)

# 2. Używaj fill_value dla czytelności
clean_pivot = df.pivot_table(
    values='Sprzedaz',
    index='Sprzedawca',
    columns='Region',
    aggfunc='sum',
    fill_value=0  # zamiast NaN
)

# 3. Margins dla kontekstu
contextual_pivot = df.pivot_table(
    values='Sprzedaz',
    index='Sprzedawca',
    columns='Region',
    aggfunc='sum',
    fill_value=0,
    margins=True  # totals pomagają w analizie
)

# 4. Round dla czytelności liczb
rounded_pivot = df.pivot_table(
    values='Sprzedaz',
    index='Sprzedawca',
    columns='Region',
    aggfunc='mean'
).round(2)  # 2 miejsca po przecinku
```

### ❌ Unikaj

```python
# Nie twórz zbyt złożonych pivot tables
# complex_pivot = df.pivot_table(
#     values=['col1', 'col2', 'col3'],
#     index=['idx1', 'idx2', 'idx3'],
#     columns=['col1', 'col2'],
#     aggfunc=['sum', 'mean', 'std', 'count']
# )  # Trudne do zrozumienia!

# Nie ignoruj NaN bez przemyślenia
# bad_pivot = df.pivot_table(...)  # Gdzie są NaN?
```

## 🔗 Powiązane funkcje

- `df.pivot()` - prostszy pivot (bez agregacji)
- `df.crosstab()` - tabele krzyżowe (cross tabulation)  
- `df.groupby().agg()` - grupowanie z agregacją
- `df.unstack()` / `df.stack()` - przekształcanie indeksów
- `pd.melt()` - przeciwność pivot (wide→long)

## 📚 Porównanie z innymi metodami

```python
# Pivot table vs GroupBy
print("Porównanie metod:")

# GroupBy approach
gb_result = df.groupby(['Sprzedawca', 'Region'])['Sprzedaz'].sum().unstack(fill_value=0)
print("GroupBy + unstack:")
print(gb_result)

# Pivot table approach
pv_result = df.pivot_table(
    values='Sprzedaz',
    index='Sprzedawca', 
    columns='Region',
    aggfunc='sum',
    fill_value=0
)
print(f"\nPivot table:")
print(pv_result)

print(f"\nCzy identyczne? {gb_result.equals(pv_result)}")
```

## 📝 Podsumowanie

`DataFrame.pivot_table()` to potężne narzędzie analityczne:

- 📊 Tworzy tabele przestawne jak w Excelu
- 🔄 Przekształca długie dane w szerokie z agregacją  
- 📐 `index` (wiersze), `columns` (kolumny), `values` (co agregować)
- 🎯 `aggfunc` określa jak agregować ('sum', 'mean', 'count', etc.)
- ✨ `margins=True` dodaje sumy brzegowe
- 🎨 `fill_value` zastępuje NaN
- 📈 Idealne do raportów i analiz biznesowych

To jak Excel pivot na sterydach - więcej mocy, więcej kontroli! 💪📈