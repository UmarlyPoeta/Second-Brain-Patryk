# 🌊 Seaborn - heatmap() - Mapy ciepła i korelacje

## 📚 Co to jest seaborn.heatmap()?

`seaborn.heatmap()` to funkcja do tworzenia map ciepła - wizualizacji gdzie kolory pokazują intensywność wartości. To jak termowizja dla danych! 🌡️

## 🔧 Podstawowa składnia

```python
import seaborn as sns

sns.heatmap(data, annot=False, fmt='.2g', cmap='viridis', cbar=True, **kwargs)
```

## 💻 Podstawowy przykład

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Przykładowe dane
np.random.seed(42)
data = np.random.rand(5, 5)

plt.figure(figsize=(8, 6))
sns.heatmap(data, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Podstawowa mapa ciepła')
plt.show()
```

## 🎯 Praktyczne przypadki

### 📊 Macierz korelacji

```python
# Dane finansowe
stocks = pd.DataFrame({
    'AAPL': np.random.randn(100).cumsum(),
    'GOOGL': np.random.randn(100).cumsum(), 
    'MSFT': np.random.randn(100).cumsum(),
    'TSLA': np.random.randn(100).cumsum(),
    'NVDA': np.random.randn(100).cumsum()
})

# Macierz korelacji
corr_matrix = stocks.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, 
           annot=True,           # pokaż wartości
           cmap='RdYlBu',        # kolorowanie
           center=0,             # centrum na 0
           square=True,          # kwadratowe komórki
           fmt='.3f')            # format liczb
plt.title('Macierz korelacji akcji technologicznych')
plt.show()

print("Najsilniejsze korelacje:")
corr_pairs = corr_matrix.unstack().sort_values(ascending=False)
# Usuń autokorelacje (1.0) i duplikaty
corr_pairs = corr_pairs[corr_pairs != 1.0]
print(corr_pairs.head(3))
```

### 🏢 Dane sprzedażowe

```python
# Sprzedaż produktów w regionach
regions = ['Północ', 'Południe', 'Wschód', 'Zachód', 'Centrum']
products = ['Laptop', 'Telefon', 'Tablet', 'Monitor', 'Słuchawki']

# Symulacja danych sprzedaży
np.random.seed(123)
sales_data = np.random.randint(100, 1000, (len(regions), len(products)))

# Dodaj trendy (niektóre regiony lepsze w niektórych produktach)
sales_data[0] *= [1.2, 0.8, 1.0, 1.1, 0.9]  # Północ lubi laptopy
sales_data[1] *= [0.9, 1.3, 1.1, 0.8, 1.2]  # Południe lubi telefony

sales_df = pd.DataFrame(sales_data, index=regions, columns=products)

plt.figure(figsize=(12, 8))
sns.heatmap(sales_df,
           annot=True,
           fmt='d',              # liczby całkowite
           cmap='YlOrRd',
           cbar_kws={'label': 'Sprzedaż (sztuki)'})
plt.title('Sprzedaż produktów według regionów')
plt.ylabel('Region')
plt.xlabel('Produkt') 
plt.show()

print("Najlepiej sprzedające się kombinacje:")
best_sales = sales_df.unstack().sort_values(ascending=False).head(5)
for (product, region), sales in best_sales.items():
    print(f"{region} - {product}: {sales} sztuk")
```

### 🎓 Oceny studentów

```python
# Macierz ocen studentów z przedmiotów
students = [f'Student_{i}' for i in range(1, 16)]
subjects = ['Matematyka', 'Fizyka', 'Chemia', 'Biologia', 'Geografia']

# Generuj oceny z pewną logiką
np.random.seed(456)
grades = []

for student in students:
    student_grades = []
    # Każdy student ma "profil" - lepszy w niektórych przedmiotach
    ability = np.random.uniform(0.3, 1.0)  # ogólne zdolności
    science_bonus = np.random.uniform(-0.2, 0.3)  # bonus do nauk ścisłych
    
    for subject in subjects:
        base_grade = ability * 5
        if subject in ['Matematyka', 'Fizyka', 'Chemia']:
            base_grade += science_bonus * 2
        
        # Dodaj losowość i zaokrąglij do skali 2-5
        grade = np.clip(base_grade + np.random.normal(0, 0.5), 2, 5)
        student_grades.append(round(grade, 1))
    
    grades.append(student_grades)

grades_df = pd.DataFrame(grades, index=students, columns=subjects)

# Dwie mapy ciepła obok siebie
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))

# Mapa ocen
sns.heatmap(grades_df, annot=True, fmt='.1f', cmap='RdYlGn', 
           vmin=2, vmax=5, ax=ax1, cbar_kws={'label': 'Ocena'})
ax1.set_title('Oceny studentów z przedmiotów')

# Mapa z ranking studentów (normalizacja po wierszach)
grades_normalized = grades_df.div(grades_df.sum(axis=1), axis=0)
sns.heatmap(grades_normalized, annot=False, cmap='viridis', ax=ax2,
           cbar_kws={'label': 'Udział w sumie ocen'})
ax2.set_title('Względne mocne strony studentów')

plt.tight_layout()
plt.show()

# Statystyki
print("Średnie oceny z przedmiotów:")
subject_means = grades_df.mean().sort_values(ascending=False)
for subject, mean_grade in subject_means.items():
    print(f"{subject:12}: {mean_grade:.2f}")

print(f"\nNajlepsi studenci (średnia):")
student_means = grades_df.mean(axis=1).sort_values(ascending=False)
for student, mean_grade in student_means.head(5).items():
    print(f"{student}: {mean_grade:.2f}")
```

## 🔍 Zaawansowane opcje

### 1️⃣ Różne mapy kolorów i formatowanie

```python
# Demonstracja różnych opcji
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Różne dane do pokazania opcji
confusion_matrix = np.array([[85, 3, 2], [4, 88, 1], [2, 1, 92]])
correlation_data = np.random.rand(6, 6)
np.fill_diagonal(correlation_data, 1)

# 1. Confusion matrix
sns.heatmap(confusion_matrix, annot=True, fmt='d', 
           cmap='Blues', ax=axes[0,0])
axes[0,0].set_title('Confusion Matrix')
axes[0,0].set_xlabel('Predykcja')
axes[0,0].set_ylabel('Rzeczywistość')

# 2. Korelacje z maskowaniem
mask = np.triu(correlation_data, k=1)
sns.heatmap(correlation_data, mask=mask, annot=True, fmt='.2f',
           cmap='coolwarm', center=0, ax=axes[0,1])
axes[0,1].set_title('Macierz korelacji (połowa)')

# 3. Bez colorbar i z kustomowymi kolorami
sns.heatmap(np.random.rand(4, 6), cbar=False, 
           linewidths=1, linecolor='white',
           cmap='Spectral', ax=axes[1,0])
axes[1,0].set_title('Bez colorbar, z liniami')

# 4. Z kustomowymi etykietkami
custom_data = np.random.rand(3, 4)
row_labels = ['Małe', 'Średnie', 'Duże']  
col_labels = ['Q1', 'Q2', 'Q3', 'Q4']
sns.heatmap(custom_data, 
           xticklabels=col_labels,
           yticklabels=row_labels,
           annot=True, fmt='.1%',  # procenty
           cmap='viridis', ax=axes[1,1])
axes[1,1].set_title('Kustomowe etykiety, procenty')

plt.tight_layout()
plt.show()
```

### 2️⃣ Interaktywna analiza

```python
# Analiza wydajności zespołu w czasie
months = ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze']
metrics = ['Sprzedaż', 'Satysfakcja', 'Produktywność', 'Jakość']

# Symulacja danych zespołu
performance_data = []
for month in months:
    month_data = []
    # Trend wzrostowy w roku
    trend = (months.index(month) + 1) / 6 * 0.2
    for metric in metrics:
        base = np.random.uniform(0.6, 0.9)
        score = base + trend + np.random.normal(0, 0.1)
        month_data.append(max(0, min(1, score)))  # 0-1 range
    performance_data.append(month_data)

perf_df = pd.DataFrame(performance_data, index=months, columns=metrics)

# Zaawansowana heatmapa z adnotacjami
plt.figure(figsize=(10, 6))
sns.heatmap(perf_df,
           annot=True,
           fmt='.1%',
           cmap='RdYlGn',
           linewidths=0.5,
           cbar_kws={'label': 'Wynik (%)', 'shrink': 0.8},
           annot_kws={'size': 12})

plt.title('Wydajność zespołu w czasie', fontsize=16, pad=20)
plt.xlabel('Metryki', fontsize=12)
plt.ylabel('Miesiąc', fontsize=12)

# Dodaj średnie na marginesach (ręcznie)
# Średnie kolumn (metryki)
col_means = perf_df.mean(axis=0)
for i, mean in enumerate(col_means):
    plt.text(i + 0.5, len(months) + 0.1, f'{mean:.1%}', 
            ha='center', va='bottom', fontweight='bold', color='blue')

# Średnie wierszy (miesiące)  
row_means = perf_df.mean(axis=1)
for i, mean in enumerate(row_means):
    plt.text(len(metrics) + 0.1, i + 0.5, f'{mean:.1%}',
            ha='left', va='center', fontweight='bold', color='red')

plt.tight_layout()
plt.show()

print("=== ANALIZA WYDAJNOŚCI ===")
print("Najlepsze miesiące:")
best_months = row_means.sort_values(ascending=False)
for month, score in best_months.items():
    print(f"{month}: {score:.1%}")

print(f"\nNajlepsze metryki:")
best_metrics = col_means.sort_values(ascending=False)
for metric, score in best_metrics.items():
    print(f"{metric}: {score:.1%}")
```

## ⚠️ Uwagi praktyczne

```python
# Problemy i rozwiązania
print("=== CZĘSTE PROBLEMY I ROZWIĄZANIA ===")

# 1. Za dużo danych
big_data = np.random.rand(50, 50)
print("1. Za dużo danych - użyj mniejszych fontów i bez annotacji:")
plt.figure(figsize=(8, 6))
sns.heatmap(big_data, cmap='viridis', 
           annot=False,  # bez liczb
           cbar_kws={'shrink': 0.8})
plt.title('Duża mapa bez annotacji')
plt.show()

# 2. Różne zakresy wartości - normalizacja
mixed_data = pd.DataFrame({
    'Małe_liczby': np.random.rand(5),
    'Duże_liczby': np.random.rand(5) * 1000,
    'Średnie_liczby': np.random.rand(5) * 100
})

# Bez normalizacji - źle!
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
sns.heatmap(mixed_data.T, annot=True, fmt='.1f', ax=ax1)
ax1.set_title('Bez normalizacji (źle)')

# Z normalizacją - dobrze!
normalized_data = (mixed_data - mixed_data.mean()) / mixed_data.std()
sns.heatmap(normalized_data.T, annot=True, fmt='.2f', 
           center=0, cmap='coolwarm', ax=ax2)
ax2.set_title('Z normalizacją (dobrze)')
plt.show()
```

## 📝 Podsumowanie

`seaborn.heatmap()` to potężne narzędzie wizualizacji:

- 🌡️ Pokazuje intensywność wartości kolorami
- 📊 Idealne do macierzy korelacji
- 🎨 `cmap=` dla różnych palet kolorów
- 📝 `annot=True` żeby pokazać wartości
- 🎯 `center=0` dla danych z zerem jako neutralną wartością
- 📐 `square=True` dla kwadratowych komórek
- 🔍 Świetne do znajdowania wzorców w danych tabularycznych

To jak termowizja dla danych - od razu widać co jest gorące! 🔥📊