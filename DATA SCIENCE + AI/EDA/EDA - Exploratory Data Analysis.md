## 🔍 EDA - Exploratory Data Analysis

_Systematyczne eksplorowanie i zrozumienie danych_

---

### 📝 Wprowadzenie do EDA

**Exploratory Data Analysis (EDA)** to proces systematycznego badania danych w celu:

1. **Zrozumienia struktury** danych
2. **Wykrycia wzorców** i anomalii  
3. **Identyfikacji problemów** z jakością danych
4. **Formułowania hipotez** do dalszej analizy
5. **Przygotowania strategii** czyszczenia danych

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Konfiguracja
plt.style.use('seaborn-v0_8')
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)
```

---

### 📊 1. Pierwszy rzut oka na dane

```python
# Wczytanie przykładowych danych
df = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')

# Podstawowe informacje
print("=== PODSTAWOWE INFORMACJE ===")
print(f"Kształt danych: {df.shape}")
print(f"Pamięć: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Podgląd danych
print("\n=== PIERWSZE 5 WIERSZY ===")
print(df.head())

print("\n=== OSTATNIE 5 WIERSZY ===")  
print(df.tail())

print("\n=== LOSOWE 5 WIERSZY ===")
print(df.sample(5))

# Info o kolumnach
print("\n=== INFORMACJE O KOLUMNACH ===")
print(df.info())

# Typy danych
print("\n=== TYPY DANYCH ===")
print(df.dtypes.value_counts())

# Nazwy kolumn
print(f"\nNazwy kolumn: {df.columns.tolist()}")
print(f"Kolumny numeryczne: {df.select_dtypes(include=[np.number]).columns.tolist()}")
print(f"Kolumny tekstowe: {df.select_dtypes(include=['object']).columns.tolist()}")
```

---

### 🔢 2. Analiza zmiennych numerycznych

```python
def analyze_numeric_variables(df):
    """Kompleksowa analiza zmiennych numerycznych"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        print("Brak zmiennych numerycznych")
        return
    
    print("=== STATYSTYKI OPISOWE ===")
    print(df[numeric_cols].describe())
    
    # Dodatkowe statystyki
    print("\n=== DODATKOWE STATYSTYKI ===")
    additional_stats = pd.DataFrame({
        'Skewness': df[numeric_cols].skew(),
        'Kurtosis': df[numeric_cols].kurtosis(),
        'Variance': df[numeric_cols].var(),
        'IQR': df[numeric_cols].quantile(0.75) - df[numeric_cols].quantile(0.25),
        'Range': df[numeric_cols].max() - df[numeric_cols].min()
    })
    print(additional_stats)
    
    # Wizualizacja rozkładów
    n_cols = min(4, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 3*n_rows))
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols):
        if i < len(axes):
            # Histogram z KDE
            df[col].hist(bins=30, alpha=0.7, ax=axes[i])
            df[col].plot(kind='kde', ax=axes[i], secondary_y=True)
            axes[i].set_title(f'Rozkład: {col}')
            axes[i].set_ylabel('Frequency')
    
    # Ukrycie pustych subplotów
    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    return additional_stats

# Analiza zmiennych numerycznych Titanica
numeric_stats = analyze_numeric_variables(df)
```

---

### 🏷️ 3. Analiza zmiennych kategorycznych

```python
def analyze_categorical_variables(df, max_categories=10):
    """Analiza zmiennych kategorycznych"""
    cat_cols = df.select_dtypes(include=['object']).columns
    
    if len(cat_cols) == 0:
        print("Brak zmiennych kategorycznych")
        return
    
    print("=== ANALIZA ZMIENNYCH KATEGORYCZNYCH ===")
    
    for col in cat_cols:
        print(f"\n--- {col.upper()} ---")
        
        # Podstawowe statystyki
        print(f"Unikalne wartości: {df[col].nunique()}")
        print(f"Najczęstsza wartość: {df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A'}")
        
        # Value counts
        value_counts = df[col].value_counts()
        print(f"\nRozkład wartości:")
        print(value_counts.head(max_categories))
        
        if len(value_counts) > max_categories:
            print(f"... i {len(value_counts) - max_categories} innych")
        
        # Procenty
        percentages = df[col].value_counts(normalize=True) * 100
        print(f"\nRozkład procentowy:")
        print(percentages.head(max_categories).round(2))
    
    # Wizualizacja
    n_cols = min(3, len(cat_cols))
    n_rows = (len(cat_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
    if len(cat_cols) == 1:
        axes = [axes]
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    axes = axes.flatten()
    
    for i, col in enumerate(cat_cols):
        if i < len(axes):
            value_counts = df[col].value_counts().head(max_categories)
            value_counts.plot(kind='bar', ax=axes[i])
            axes[i].set_title(f'Rozkład: {col}')
            axes[i].tick_params(axis='x', rotation=45)
    
    # Ukrycie pustych subplotów
    for i in range(len(cat_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()

analyze_categorical_variables(df)
```

---

### ❓ 4. Analiza brakujących danych

```python
def analyze_missing_data(df):
    """Kompleksowa analiza brakujących danych"""
    
    # Podstawowe statystyki
    missing_counts = df.isnull().sum()
    missing_percentages = (missing_counts / len(df)) * 100
    
    missing_summary = pd.DataFrame({
        'Missing_Count': missing_counts,
        'Missing_Percentage': missing_percentages
    })
    missing_summary = missing_summary[missing_summary['Missing_Count'] > 0]
    missing_summary = missing_summary.sort_values('Missing_Percentage', ascending=False)
    
    print("=== BRAKUJĄCE DANE ===")
    if len(missing_summary) == 0:
        print("Brak brakujących danych! ✅")
        return missing_summary
    
    print(missing_summary)
    
    # Wizualizacja brakujących danych
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. Bar plot
    missing_summary.plot(kind='bar', y='Missing_Percentage', ax=axes[0])
    axes[0].set_title('Procent brakujących danych')
    axes[0].set_ylabel('Procent (%)')
    axes[0].tick_params(axis='x', rotation=45)
    
    # 2. Heatmap brakujących danych
    sns.heatmap(df.isnull(), cbar=True, ax=axes[1], cmap='viridis')
    axes[1].set_title('Mapa brakujących danych')
    
    # 3. Missing data patterns
    if len(missing_summary) > 1:
        # Kombinacje brakujących danych
        missing_combinations = df[missing_summary.index].isnull()
        missing_patterns = missing_combinations.value_counts()
        
        axes[2].bar(range(len(missing_patterns)), missing_patterns.values)
        axes[2].set_title('Wzorce brakujących danych')
        axes[2].set_xlabel('Pattern')
        axes[2].set_ylabel('Count')
    else:
        axes[2].text(0.5, 0.5, 'Tylko jedna kolumna\nz brakującymi danymi', 
                    ha='center', va='center', transform=axes[2].transAxes)
        axes[2].set_title('Wzorce brakujących danych')
    
    plt.tight_layout()
    plt.show()
    
    # Analiza korelacji brakujących danych
    if len(missing_summary) > 1:
        print("\n=== KORELACJE BRAKUJĄCYCH DANYCH ===")
        missing_corr = df[missing_summary.index].isnull().corr()
        print(missing_corr)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(missing_corr, annot=True, cmap='coolwarm', center=0)
        plt.title('Korelacja brakujących danych')
        plt.show()
    
    return missing_summary

missing_analysis = analyze_missing_data(df)
```

---

### 🎯 5. Analiza outlierów

```python
def detect_outliers(df, methods=['iqr', 'zscore']):
    """Wykrywanie outlierów różnymi metodami"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outlier_summary = {}
    
    for col in numeric_cols:
        outlier_summary[col] = {}
        data = df[col].dropna()
        
        if 'iqr' in methods:
            # Metoda IQR
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            iqr_outliers = data[(data < lower_bound) | (data > upper_bound)]
            outlier_summary[col]['IQR'] = {
                'count': len(iqr_outliers),
                'percentage': len(iqr_outliers) / len(data) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
        
        if 'zscore' in methods:
            # Z-score method
            z_scores = np.abs(stats.zscore(data))
            zscore_outliers = data[z_scores > 3]
            outlier_summary[col]['Z-Score'] = {
                'count': len(zscore_outliers),
                'percentage': len(zscore_outliers) / len(data) * 100
            }
    
    # Wyświetlenie wyników
    print("=== ANALIZA OUTLIERÓW ===")
    for col in outlier_summary:
        print(f"\n--- {col.upper()} ---")
        for method in outlier_summary[col]:
            info = outlier_summary[col][method]
            print(f"{method}: {info['count']} outlierów ({info['percentage']:.2f}%)")
    
    # Wizualizacja
    n_cols = min(4, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 3*n_rows))
    if len(numeric_cols) == 1:
        axes = [axes]
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols):
        if i < len(axes):
            # Box plot dla outlierów
            df.boxplot(column=col, ax=axes[i])
            axes[i].set_title(f'Outliers: {col}')
    
    # Ukrycie pustych subplotów  
    for i in range(len(numeric_cols), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    return outlier_summary

outlier_results = detect_outliers(df)
```

---

### 🔗 6. Analiza korelacji

```python
def correlation_analysis(df):
    """Analiza korelacji między zmiennymi"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        print("Zbyt mało zmiennych numerycznych do analizy korelacji")
        return
    
    # Macierz korelacji
    corr_matrix = df[numeric_cols].corr()
    
    print("=== MACIERZ KORELACJI ===")
    print(corr_matrix.round(3))
    
    # Wysokie korelacje
    print("\n=== WYSOKIE KORELACJE (|r| > 0.7) ===")
    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) > 0.7:
                high_corr_pairs.append({
                    'Variable_1': corr_matrix.columns[i],
                    'Variable_2': corr_matrix.columns[j], 
                    'Correlation': corr_val
                })
    
    if high_corr_pairs:
        high_corr_df = pd.DataFrame(high_corr_pairs)
        print(high_corr_df)
    else:
        print("Brak wysokich korelacji")
    
    # Wizualizacja
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Heatmap
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, ax=axes[0])
    axes[0].set_title('Macierz korelacji')
    
    # Clustermap - uporządkowana heatmap
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, ax=axes[1])
    axes[1].set_title('Macierz korelacji (uporządkowana)')
    
    plt.tight_layout()
    plt.show()
    
    return corr_matrix

correlation_matrix = correlation_analysis(df)
```

---

### 📈 7. Quick EDA Report

```python
def quick_eda_report(df, target_col=None):
    """Szybki raport EDA"""
    print("="*60)
    print("           QUICK EDA REPORT")
    print("="*60)
    
    # 1. Dataset Overview
    print(f"📊 Dataset Shape: {df.shape}")
    print(f"💾 Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"🔢 Numeric Columns: {len(df.select_dtypes(include=[np.number]).columns)}")
    print(f"📝 Categorical Columns: {len(df.select_dtypes(include=['object']).columns)}")
    
    # 2. Missing Data Summary
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    missing_cols = missing_pct[missing_pct > 0]
    print(f"❓ Columns with Missing Data: {len(missing_cols)}")
    if len(missing_cols) > 0:
        print("Top missing columns:")
        for col, pct in missing_cols.head().items():
            print(f"  - {col}: {pct}%")
    
    # 3. Duplicates
    duplicates = df.duplicated().sum()
    print(f"🔄 Duplicate Rows: {duplicates} ({duplicates/len(df)*100:.2f}%)")
    
    # 4. Outliers (quick check)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    total_outliers = 0
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)][col].count()
        total_outliers += outliers
    
    print(f"⚠️  Total Outliers (IQR method): {total_outliers}")
    
    # 5. High Cardinality Columns
    cat_cols = df.select_dtypes(include=['object']).columns
    high_cardinality = []
    for col in cat_cols:
        if df[col].nunique() > 20:
            high_cardinality.append(f"{col} ({df[col].nunique()} unique)")
    
    if high_cardinality:
        print(f"🔤 High Cardinality Columns: {', '.join(high_cardinality)}")
    
    # 6. Target variable analysis (if provided)
    if target_col and target_col in df.columns:
        print(f"\n🎯 TARGET VARIABLE: {target_col}")
        if df[target_col].dtype in ['object', 'category']:
            print("Distribution:")
            print(df[target_col].value_counts(normalize=True).round(3))
        else:
            print(f"Stats: Mean={df[target_col].mean():.2f}, Std={df[target_col].std():.2f}")
            print(f"Range: [{df[target_col].min():.2f}, {df[target_col].max():.2f}]")
    
    print("="*60)

# Uruchomienie quick report
quick_eda_report(df, target_col='Survived')
```

---

### 💡 Best Practices

```python
# EDA Checklist
eda_checklist = """
✅ EDA CHECKLIST

📊 DANE PODSTAWOWE:
- [ ] Kształt i rozmiar datasetu
- [ ] Typy danych w kolumnach  
- [ ] Podgląd pierwszych/ostatnich wierszy
- [ ] Podstawowe statystyki

❓ JAKOŚĆ DANYCH:
- [ ] Analiza brakujących danych
- [ ] Wykrycie duplikatów
- [ ] Identyfikacja outlierów
- [ ] Sprawdzenie niespójności

🔍 ANALIZA ZMIENNYCH:
- [ ] Rozkłady zmiennych numerycznych
- [ ] Analiza zmiennych kategorycznych
- [ ] High cardinality columns
- [ ] Skewness i kurtoza

🔗 RELACJE:
- [ ] Macierz korelacji
- [ ] Scatter plots kluczowych par
- [ ] Analiza target variable
- [ ] Feature importance (jeśli applicable)

📈 WIZUALIZACJE:
- [ ] Histogramy i box plots
- [ ] Heatmapy
- [ ] Pair plots dla kluczowych zmiennych
- [ ] Distribution plots

📝 WNIOSKI:
- [ ] Dokumentacja anomalii
- [ ] Plan czyszczenia danych
- [ ] Hipotezy do sprawdzenia
- [ ] Strategia feature engineering
"""

print(eda_checklist)
```

---

### 🎯 Następny krok

Poznasz **Data Cleaning - Missing Values**:

- Strategie radzenia z brakującymi danymi
- Imputacja statystyczna
- Advanced imputation methods
- Walidacja po imputacji
- Impact assessment