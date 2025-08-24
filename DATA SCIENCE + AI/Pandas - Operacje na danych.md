## 🐼 Pandas - Operacje na danych

_Zaawansowane operacje i transformacje danych_

---

### 📊 Funkcje agregujące

```python
import pandas as pd
import numpy as np

# Przykładowe dane
df = pd.DataFrame({
    'Produkt': ['A', 'B', 'A', 'C', 'B', 'C'],
    'Kategoria': ['Electronics', 'Clothing', 'Electronics', 'Books', 'Clothing', 'Books'],
    'Sprzedaż': [100, 150, 120, 80, 200, 90],
    'Zysk': [20, 45, 25, 15, 60, 20],
    'Data': pd.date_range('2023-01-01', periods=6)
})

# Podstawowe agregacje
print(f"Suma sprzedaży: {df['Sprzedaż'].sum()}")
print(f"Średnia zysku: {df['Zysk'].mean():.2f}")
print(f"Mediana sprzedaży: {df['Sprzedaż'].median()}")
print(f"Odchylenie standardowe: {df['Zysk'].std():.2f}")

# Wiele statystyk jednocześnie
print(df[['Sprzedaż', 'Zysk']].agg(['min', 'max', 'mean', 'std']))

# Różne funkcje dla różnych kolumn
multi_agg = df.agg({
    'Sprzedaż': ['sum', 'mean'],
    'Zysk': ['min', 'max'],
    'Produkt': 'count'
})
print(multi_agg)
```

---

### 🎯 Grupowanie danych (GroupBy)

```python
# Grupowanie po jednej kolumnie
grouped_by_category = df.groupby('Kategoria')

# Agregacja po grupowaniu
category_stats = grouped_by_category.agg({
    'Sprzedaż': ['sum', 'mean'],
    'Zysk': 'sum'
})
print(category_stats)

# Grupowanie po wielu kolumnach
multi_group = df.groupby(['Kategoria', 'Produkt']).sum()
print(multi_group)

# Iteracja przez grupy
for name, group in df.groupby('Kategoria'):
    print(f"\nKategoria: {name}")
    print(group)

# Zastosowanie własnej funkcji
def profit_margin(group):
    return group['Zysk'].sum() / group['Sprzedaż'].sum() * 100

margin_by_category = df.groupby('Kategoria').apply(profit_margin)
print(f"Marża zysku wg kategorii:\n{margin_by_category}")
```

---

### 📝 Operacje na tekstach

```python
# Dane tekstowe
text_df = pd.DataFrame({
    'Nazwisko': ['kowalski', 'NOWAK', 'Wiśniewski', 'wójcik'],
    'Email': ['jan.kowalski@email.com', 'anna.nowak@GMAIL.COM', 
              'piotr.wisniewski@wp.pl', 'maria.wojcik@onet.pl'],
    'Telefon': ['123-456-789', '987.654.321', '555 123 456', '(48) 111-222-333']
})

# Zmiana wielkości liter
text_df['Nazwisko_proper'] = text_df['Nazwisko'].str.title()  # Pierwsza wielka
text_df['Nazwisko_upper'] = text_df['Nazwisko'].str.upper()   # Wszystkie wielkie
text_df['Email_lower'] = text_df['Email'].str.lower()         # Wszystkie małe

# Wyodrębnianie części tekstu
text_df['Domena'] = text_df['Email'].str.split('@').str[1]
text_df['Provider'] = text_df['Domena'].str.split('.').str[0]

# Wyszukiwanie wzorców
gmail_users = text_df[text_df['Email'].str.contains('gmail', case=False)]
print("Użytkownicy Gmail:")
print(gmail_users)

# Zastępowanie tekstu
text_df['Telefon_clean'] = text_df['Telefon'].str.replace(r'[^\d]', '', regex=True)

# Długość tekstu
text_df['Email_length'] = text_df['Email'].str.len()

print(text_df)
```

---

### 📅 Operacje na datach

```python
# Tworzenie dat
date_df = pd.DataFrame({
    'Data_str': ['2023-01-15', '2023-02-20', '2023-03-10', '2023-04-05'],
    'Sprzedaż': [1000, 1500, 1200, 1800]
})

# Konwersja na datetime
date_df['Data'] = pd.to_datetime(date_df['Data_str'])

# Wyodrębnianie komponentów daty
date_df['Rok'] = date_df['Data'].dt.year
date_df['Miesiąc'] = date_df['Data'].dt.month
date_df['Dzień_tygodnia'] = date_df['Data'].dt.day_name()
date_df['Kwartal'] = date_df['Data'].dt.quarter

# Obliczenia na datach
date_df['Dni_od_dzisiaj'] = (pd.Timestamp.now() - date_df['Data']).dt.days

# Resampling (dla szeregów czasowych)
date_df = date_df.set_index('Data')
monthly_sum = date_df['Sprzedaż'].resample('M').sum()  # Suma miesięczna
print(f"Miesięczne sumy:\n{monthly_sum}")
```

---

### 🔄 Transformacje danych

```python
# Apply - zastosowanie funkcji do każdego elementu/wiersza
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [10, 20, 30, 40],
    'C': [100, 200, 300, 400]
})

# Apply do kolumny (Series)
df['A_squared'] = df['A'].apply(lambda x: x**2)

# Apply do DataFrame (kolumnami)
df_normalized = df[['A', 'B', 'C']].apply(lambda col: (col - col.mean()) / col.std())

# Apply wierszami (axis=1)
df['Sum_ABC'] = df[['A', 'B', 'C']].apply(lambda row: row.sum(), axis=1)

# Map - mapowanie wartości
grade_map = {1: 'F', 2: 'D', 3: 'C', 4: 'B', 5: 'A'}
grades = pd.Series([3, 4, 2, 5, 1])
letter_grades = grades.map(grade_map)
print(f"Oceny liczbowe: {grades.tolist()}")
print(f"Oceny literowe: {letter_grades.tolist()}")

# Transform - zachowuje kształt DataFrame
df_transformed = df[['A', 'B', 'C']].transform(lambda x: x / x.max())
```

---

### 🔢 Pivot Tables

```python
# Dane sprzedażowe
sales_data = pd.DataFrame({
    'Miesiąc': ['Styczeń', 'Styczeń', 'Luty', 'Luty', 'Marzec', 'Marzec'],
    'Produkt': ['A', 'B', 'A', 'B', 'A', 'B'],
    'Region': ['Północ', 'Południe', 'Północ', 'Południe', 'Północ', 'Południe'],
    'Sprzedaż': [100, 150, 120, 180, 140, 160]
})

# Podstawowa pivot table
pivot_basic = sales_data.pivot_table(
    values='Sprzedaż',
    index='Miesiąc',
    columns='Produkt',
    aggfunc='sum'
)
print("Podstawowa pivot table:")
print(pivot_basic)

# Zaawansowana pivot table
pivot_advanced = sales_data.pivot_table(
    values='Sprzedaż',
    index=['Miesiąc', 'Region'],
    columns='Produkt',
    aggfunc='sum',
    fill_value=0,
    margins=True  # Dodaje sumy totalne
)
print("\nZaawansowana pivot table:")
print(pivot_advanced)

# Cross-tabulation (tabulacja krzyżowa)
crosstab = pd.crosstab(sales_data['Miesiąc'], sales_data['Produkt'], 
                      values=sales_data['Sprzedaż'], aggfunc='sum')
print("\nCross-tabulation:")
print(crosstab)
```

---

### 🔍 Wyszukiwanie i filtrowanie

```python
# Dane do filtrowania
filter_df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'Age': [25, 30, 35, 40, 45],
    'Salary': [50000, 60000, 70000, 80000, 90000],
    'Department': ['IT', 'HR', 'IT', 'Finance', 'IT']
})

# Query method - SQL-like filtering
it_employees = filter_df.query('Department == "IT" and Salary > 50000')
print("Pracownicy IT z pensją > 50000:")
print(it_employees)

# isin() - filtrowanie przez listę wartości
young_or_old = filter_df[filter_df['Age'].isin([25, 45])]

# between() - wartości w przedziale
middle_aged = filter_df[filter_df['Age'].between(30, 40, inclusive='both')]

# Wyszukiwanie najbliższych wartości
target_salary = 65000
closest_salary = filter_df.iloc[(filter_df['Salary'] - target_salary).abs().argsort()[:2]]
print(f"\n2 najbliższe pensje do {target_salary}:")
print(closest_salary)
```

---

### 📊 Window functions (rolling, expanding)

```python
# Szereg czasowy
ts_data = pd.DataFrame({
    'Date': pd.date_range('2023-01-01', periods=10),
    'Value': [10, 12, 8, 15, 20, 18, 22, 25, 19, 30]
})
ts_data = ts_data.set_index('Date')

# Rolling window (okno ruchome)
ts_data['Rolling_Mean_3'] = ts_data['Value'].rolling(window=3).mean()
ts_data['Rolling_Sum_3'] = ts_data['Value'].rolling(window=3).sum()
ts_data['Rolling_Std_3'] = ts_data['Value'].rolling(window=3).std()

# Expanding window (okno rozszerzające się)
ts_data['Expanding_Mean'] = ts_data['Value'].expanding().mean()
ts_data['Expanding_Max'] = ts_data['Value'].expanding().max()

# Shift - przesunięcie wartości
ts_data['Previous_Value'] = ts_data['Value'].shift(1)
ts_data['Next_Value'] = ts_data['Value'].shift(-1)
ts_data['Diff'] = ts_data['Value'] - ts_data['Previous_Value']

print(ts_data)
```

---

### 💻 Praktyczne zastosowania

```python
# 1. Analiza sprzedaży - trend i sezonowość
def analyze_sales_trend(data):
    return {
        'total_sales': data['Sprzedaż'].sum(),
        'avg_growth': data['Sprzedaż'].pct_change().mean() * 100,
        'best_month': data.loc[data['Sprzedaż'].idxmax(), 'Miesiąc']
    }

# 2. Segmentacja klientów
def customer_segment(row):
    if row['Salary'] > 70000:
        return 'Premium'
    elif row['Salary'] > 50000:
        return 'Standard'
    else:
        return 'Basic'

filter_df['Segment'] = filter_df.apply(customer_segment, axis=1)

# 3. Obliczanie wskaźników biznesowych
def calculate_kpis(df):
    return pd.Series({
        'Revenue': df['Sprzedaż'].sum(),
        'Profit_Margin': (df['Zysk'].sum() / df['Sprzedaż'].sum()) * 100,
        'Avg_Transaction': df['Sprzedaż'].mean(),
        'Transaction_Count': len(df)
    })

# 4. Rankowanie i percentyle
filter_df['Salary_Rank'] = filter_df['Salary'].rank(ascending=False)
filter_df['Salary_Percentile'] = filter_df['Salary'].rank(pct=True) * 100
```

---

### 🎯 Następny krok

Poznasz **GroupBy operations w Pandas**:

- Zaawansowane grupowanie
- Split-Apply-Combine
- Własne funkcje agregujące
- Multi-level grouping
- Czasowe grupowanie