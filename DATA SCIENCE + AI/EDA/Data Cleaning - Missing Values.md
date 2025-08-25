## 🧹 Data Cleaning - Missing Values

_Strategie radzenia z brakującymi danymi_

---

### 📝 Wprowadzenie do Missing Values

**Brakujące dane** to jeden z najczęstszych problemów w Data Science. Nieprawidłowe podejście może:

1. **Zmniejszyć dokładność** modeli
2. **Wprowadzić bias** w analizie
3. **Ograniczyć** wielkość datasetu
4. **Wpłynąć na interpretację** wyników

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import warnings
warnings.filterwarnings('ignore')
```

---

### 🔍 Typy brakujących danych

```python
# Generowanie przykładowych danych z różnymi typami missing values
np.random.seed(42)
n_samples = 1000

# Podstawowe dane
data = {
    'age': np.random.normal(35, 10, n_samples),
    'income': np.random.lognormal(10, 0.5, n_samples),
    'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples),
    'experience': np.random.normal(10, 5, n_samples)
}

df = pd.DataFrame(data)
df['experience'] = np.maximum(0, df['experience'])  # Doświadczenie >= 0

print("=== TYPY BRAKUJĄCYCH DANYCH ===")

# 1. MCAR (Missing Completely At Random)
# Losowe 5% brakujących wartości
mcar_indices = np.random.choice(df.index, size=int(0.05 * len(df)), replace=False)
df.loc[mcar_indices, 'age'] = np.nan
print(f"MCAR: {df['age'].isnull().sum()} brakujących wartości wieku (losowo)")

# 2. MAR (Missing At Random)
# Starsi ludzie rzadziej podają dochód
prob_missing = 1 / (1 + np.exp(-(df['age'] - 40) / 5))
mar_mask = np.random.random(len(df)) < prob_missing * 0.3
df.loc[mar_mask, 'income'] = np.nan
print(f"MAR: {df['income'].isnull().sum()} brakujących dochodów (zależy od wieku)")

# 3. MNAR (Missing Not At Random)
# Ludzie z niskim wykształceniem nie podają lat doświadczenia
mnar_mask = (df['education'] == 'High School') & (np.random.random(len(df)) < 0.4)
df.loc[mnar_mask, 'experience'] = np.nan
print(f"MNAR: {df['experience'].isnull().sum()} brakującego doświadczenia (związane z wykształceniem)")

# Analiza wzorców
def analyze_missing_patterns(df):
    missing_data = df.isnull()
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. Missing data heatmap
    sns.heatmap(missing_data, cbar=True, ax=axes[0], cmap='viridis')
    axes[0].set_title('Mapa brakujących danych')
    
    # 2. Missing data bar plot
    missing_counts = missing_data.sum()
    missing_counts.plot(kind='bar', ax=axes[1])
    axes[1].set_title('Liczba brakujących wartości')
    axes[1].tick_params(axis='x', rotation=45)
    
    # 3. Missing combinations
    missing_combinations = missing_data.sum(axis=1).value_counts().sort_index()
    missing_combinations.plot(kind='bar', ax=axes[2])
    axes[2].set_title('Kombinacje brakujących wartości')
    axes[2].set_xlabel('Liczba brakujących kolumn na wiersz')
    
    plt.tight_layout()
    plt.show()

analyze_missing_patterns(df)
```

---

### 🗑️ Strategia 1: Usuwanie danych

```python
def deletion_strategies(df):
    """Różne strategie usuwania brakujących danych"""
    
    print("=== STRATEGIE USUWANIA ===")
    print(f"Rozmiar oryginalny: {df.shape}")
    
    # 1. Listwise deletion (complete case analysis)
    df_listwise = df.dropna()
    print(f"Listwise deletion: {df_listwise.shape} (utracono {len(df) - len(df_listwise)} wierszy)")
    
    # 2. Pairwise deletion - analiza korelacji
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"\nKorelacje z pairwise deletion:")
    corr_pairwise = df[numeric_cols].corr()  # Automatycznie ignoruje NaN pairwise
    print(corr_pairwise.round(3))
    
    # 3. Threshold-based deletion
    # Usuń kolumny z >50% missing values
    missing_threshold = 0.5
    cols_to_keep = df.columns[df.isnull().mean() < missing_threshold]
    df_col_filtered = df[cols_to_keep]
    print(f"\nPo usunięciu kolumn >50% missing: {df_col_filtered.shape}")
    
    # Usuń wiersze z >50% missing values
    row_missing_pct = df.isnull().sum(axis=1) / df.shape[1]
    df_row_filtered = df[row_missing_pct < missing_threshold]
    print(f"Po usunięciu wierszy >50% missing: {df_row_filtered.shape}")
    
    # 4. Conditional deletion
    # Usuń tylko jeśli konkretna kolumna ma missing value
    df_conditional = df.dropna(subset=['income'])  # Usuń tylko jeśli brak dochodu
    print(f"Conditional deletion (income): {df_conditional.shape}")
    
    return {
        'listwise': df_listwise,
        'column_filtered': df_col_filtered, 
        'row_filtered': df_row_filtered,
        'conditional': df_conditional
    }

deletion_results = deletion_strategies(df)

# Porównanie rozkładów po deletion
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for i, (name, data) in enumerate(deletion_results.items()):
    ax = axes[i//2, i%2]
    if 'age' in data.columns and not data['age'].empty:
        data['age'].hist(bins=20, alpha=0.7, ax=ax)
        ax.set_title(f'Rozkład wieku - {name}')
        ax.set_xlabel('Wiek')

plt.tight_layout()
plt.show()
```

---

### 🔄 Strategia 2: Imputacja podstawowa

```python
def basic_imputation(df):
    """Podstawowe metody imputacji"""
    
    print("=== IMPUTACJA PODSTAWOWA ===")
    
    # Kopia danych do testów
    df_test = df.copy()
    
    # 1. Mean/Median/Mode imputation
    numeric_cols = df_test.select_dtypes(include=[np.number]).columns
    categorical_cols = df_test.select_dtypes(include=['object']).columns
    
    # Numeryczne - median (odporny na outliers)
    median_imputer = SimpleImputer(strategy='median')
    df_test[numeric_cols] = median_imputer.fit_transform(df_test[numeric_cols])
    
    # Kategoryczne - most frequent
    mode_imputer = SimpleImputer(strategy='most_frequent')
    df_test[categorical_cols] = mode_imputer.fit_transform(df_test[categorical_cols])
    
    print(f"Po imputacji podstawowej: {df_test.isnull().sum().sum()} brakujących wartości")
    
    # 2. Forward/Backward fill (dla danych czasowych)
    df_ffill = df.fillna(method='ffill')  # Forward fill
    df_bfill = df.fillna(method='bfill')  # Backward fill
    
    # 3. Interpolacja
    df_interpolated = df.copy()
    for col in numeric_cols:
        df_interpolated[col] = df_interpolated[col].interpolate()
    
    # 4. Custom values
    df_custom = df.copy()
    custom_values = {
        'age': df['age'].median(),
        'income': 0,  # Założenie: brak dochodu = 0
        'experience': df['experience'].mean(),
        'education': 'Unknown'
    }
    
    df_custom = df_custom.fillna(value=custom_values)
    
    # Porównanie wyników
    imputation_comparison = pd.DataFrame({
        'Original': df.isnull().sum(),
        'Basic': df_test.isnull().sum(),
        'Forward Fill': df_ffill.isnull().sum(),
        'Interpolated': df_interpolated.isnull().sum(),
        'Custom': df_custom.isnull().sum()
    })
    
    print("\nPorównanie metod imputacji:")
    print(imputation_comparison)
    
    return {
        'basic': df_test,
        'ffill': df_ffill,
        'interpolated': df_interpolated,
        'custom': df_custom
    }

basic_results = basic_imputation(df)
```

---

### 🤖 Strategia 3: Imputacja zaawansowana

```python
def advanced_imputation(df):
    """Zaawansowane metody imputacji"""
    
    print("=== IMPUTACJA ZAAWANSOWANA ===")
    
    # Przygotowanie danych - kodowanie kategorycznych
    df_encoded = df.copy()
    df_encoded['education'] = pd.Categorical(df_encoded['education']).codes
    
    # 1. KNN Imputation
    knn_imputer = KNNImputer(n_neighbors=5)
    df_knn = pd.DataFrame(
        knn_imputer.fit_transform(df_encoded),
        columns=df_encoded.columns,
        index=df_encoded.index
    )
    
    # Dekodowanie education
    education_mapping = dict(enumerate(df['education'].astype('category').cat.categories))
    df_knn['education'] = df_knn['education'].round().astype(int).map(education_mapping)
    
    print(f"KNN Imputation: {df_knn.isnull().sum().sum()} brakujących wartości")
    
    # 2. Iterative Imputation (MICE)
    iterative_imputer = IterativeImputer(random_state=42, max_iter=10)
    df_mice = pd.DataFrame(
        iterative_imputer.fit_transform(df_encoded),
        columns=df_encoded.columns,
        index=df_encoded.index
    )
    
    df_mice['education'] = df_mice['education'].round().astype(int).map(education_mapping)
    print(f"MICE Imputation: {df_mice.isnull().sum().sum()} brakujących wartości")
    
    # 3. Group-based imputation
    df_group = df.copy()
    
    # Imputacja wieku na podstawie wykształcenia
    age_by_education = df.groupby('education')['age'].median()
    for education in age_by_education.index:
        mask = (df_group['education'] == education) & df_group['age'].isnull()
        df_group.loc[mask, 'age'] = age_by_education[education]
    
    # Imputacja dochodu na podstawie wieku i wykształcenia
    for education in df['education'].unique():
        education_data = df_group[df_group['education'] == education]
        if not education_data.empty:
            income_median = education_data['income'].median()
            mask = (df_group['education'] == education) & df_group['income'].isnull()
            df_group.loc[mask, 'income'] = income_median
    
    # Imputacja doświadczenia na podstawie wieku
    mask = df_group['experience'].isnull()
    df_group.loc[mask, 'experience'] = np.maximum(0, df_group.loc[mask, 'age'] - 25)
    
    print(f"Group-based Imputation: {df_group.isnull().sum().sum()} brakujących wartości")
    
    return {
        'knn': df_knn,
        'mice': df_mice,
        'group': df_group
    }

advanced_results = advanced_imputation(df)

# Porównanie rozkładów
def compare_distributions(original, imputed_dict, column):
    """Porównanie rozkładów przed i po imputacji"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    
    # Oryginalny rozkład (bez NaN)
    original_clean = original[column].dropna()
    original_clean.hist(bins=30, alpha=0.7, ax=axes[0], color='blue')
    axes[0].set_title(f'Oryginalny {column}')
    axes[0].axvline(original_clean.mean(), color='red', linestyle='--', label='Mean')
    axes[0].legend()
    
    # Imputowane rozkłady
    for i, (name, data) in enumerate(imputed_dict.items(), 1):
        if i < len(axes):
            data[column].hist(bins=30, alpha=0.7, ax=axes[i])
            axes[i].set_title(f'{name.upper()} - {column}')
            axes[i].axvline(data[column].mean(), color='red', linestyle='--', label='Mean')
            axes[i].legend()
    
    plt.tight_layout()
    plt.show()

# Porównanie dla wieku
all_methods = {**basic_results, **advanced_results}
compare_distributions(df, all_methods, 'age')
```

---

### 📊 Walidacja imputacji

```python
def validate_imputation(original, imputed_dict):
    """Walidacja jakości imputacji"""
    
    print("=== WALIDACJA IMPUTACJI ===")
    
    validation_results = []
    
    for method_name, imputed_df in imputed_dict.items():
        for column in original.columns:
            if original[column].dtype in [np.number]:
                # Porównanie statystyk
                original_stats = original[column].describe()
                imputed_stats = imputed_df[column].describe()
                
                # Obliczenie różnic
                mean_diff = abs(imputed_stats['mean'] - original_stats['mean'])
                std_diff = abs(imputed_stats['std'] - original_stats['std'])
                
                # Test Kolmogorov-Smirnov
                from scipy.stats import ks_2samp
                original_clean = original[column].dropna()
                ks_stat, ks_pvalue = ks_2samp(original_clean, imputed_df[column])
                
                validation_results.append({
                    'Method': method_name,
                    'Column': column,
                    'Mean_Diff': mean_diff,
                    'Std_Diff': std_diff,
                    'KS_Statistic': ks_stat,
                    'KS_P_Value': ks_pvalue,
                    'Distribution_Similar': ks_pvalue > 0.05
                })
    
    validation_df = pd.DataFrame(validation_results)
    
    print("\nStatystyki walidacji:")
    print(validation_df.round(4))
    
    # Wizualizacja
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Mean differences
    pivot_mean = validation_df.pivot(index='Method', columns='Column', values='Mean_Diff')
    sns.heatmap(pivot_mean, annot=True, ax=axes[0], cmap='Reds')
    axes[0].set_title('Różnica średnich')
    
    # Std differences  
    pivot_std = validation_df.pivot(index='Method', columns='Column', values='Std_Diff')
    sns.heatmap(pivot_std, annot=True, ax=axes[1], cmap='Reds')
    axes[1].set_title('Różnica odchyleń standardowych')
    
    # KS test p-values
    pivot_ks = validation_df.pivot(index='Method', columns='Column', values='KS_P_Value')
    sns.heatmap(pivot_ks, annot=True, ax=axes[2], cmap='RdYlGn', vmin=0, vmax=1)
    axes[2].set_title('K-S Test P-Values (>0.05 = good)')
    
    plt.tight_layout()
    plt.show()
    
    return validation_df

# Walidacja wszystkich metod
validation_results = validate_imputation(df, all_methods)
```

---

### 🎯 Strategia wyboru metody

```python
def imputation_strategy_guide():
    """Przewodnik wyboru strategii imputacji"""
    
    strategy_guide = """
    🎯 PRZEWODNIK WYBORU STRATEGII IMPUTACJI
    
    📊 WEDŁUG TYPU DANYCH:
    ┌─────────────────┬──────────────────────────────────────┐
    │ Typ danych      │ Zalecana metoda                      │
    ├─────────────────┼──────────────────────────────────────┤
    │ Numeryczne      │ Median, KNN, MICE                    │
    │ Kategoryczne    │ Mode, KNN z encoding                 │
    │ Czasowe         │ Forward/Backward fill, interpolacja  │
    │ Tekstowe        │ Mode, "Unknown", domain-specific     │
    └─────────────────┴──────────────────────────────────────┘
    
    📈 WEDŁUG PROCENTU MISSING:
    ┌─────────────────┬──────────────────────────────────────┐
    │ Procent missing │ Strategia                            │
    ├─────────────────┼──────────────────────────────────────┤
    │ < 5%            │ Listwise deletion, Mean/Median       │
    │ 5-15%           │ KNN, MICE, Group-based               │
    │ 15-40%          │ Advanced methods, Domain knowledge   │
    │ > 40%           │ Consider dropping, Create indicator  │
    └─────────────────┴──────────────────────────────────────┘
    
    🔍 WEDŁUG WZORCA MISSING:
    ┌─────────────────┬──────────────────────────────────────┐
    │ Typ missing     │ Podejście                            │
    ├─────────────────┼──────────────────────────────────────┤
    │ MCAR            │ Any imputation method                │
    │ MAR             │ Model-based (KNN, MICE)              │
    │ MNAR            │ Domain knowledge, Create indicators  │
    └─────────────────┴──────────────────────────────────────┘
    
    ⚠️  UWAGI:
    • Zawsze zachowaj oryginalny dataset
    • Dokumentuj wszystkie transformacje
    • Waliduj wpływ na model
    • Rozważ utworzenie wskaźnika missing
    • Testuj stabilność imputacji
    """
    
    print(strategy_guide)
    
    # Przykład decision tree dla wyboru metody
    def suggest_imputation_method(column_data, missing_pct):
        """Sugestia metody imputacji na podstawie danych"""
        
        if missing_pct > 40:
            return "Consider dropping or creating missing indicator"
        elif missing_pct < 5:
            return "Simple deletion or mean/median imputation"
        elif column_data.dtype in [np.number]:
            if missing_pct < 15:
                return "KNN or MICE imputation"
            else:
                return "Group-based or domain-specific imputation"
        else:  # categorical
            return "Mode or group-based imputation"
    
    # Sugestie dla naszego datasetu
    print("\n🔧 SUGESTIE DLA OBECNEGO DATASETU:")
    for column in df.columns:
        missing_pct = (df[column].isnull().sum() / len(df)) * 100
        suggestion = suggest_imputation_method(df[column], missing_pct)
        print(f"• {column} ({missing_pct:.1f}% missing): {suggestion}")

imputation_strategy_guide()
```

---

### 💡 Best Practices

```python
def imputation_best_practices():
    """Najlepsze praktyki w imputacji"""
    
    best_practices = """
    ✅ NAJLEPSZE PRAKTYKI IMPUTACJI
    
    📋 PRZED IMPUTACJĄ:
    1. Zrozum przyczyny brakujących danych
    2. Przeanalizuj wzorce missing data
    3. Określ typ missing data (MCAR/MAR/MNAR)
    4. Zachowaj kopię oryginalnych danych
    5. Udokumentuj wszystkie założenia
    
    🔄 PODCZAS IMPUTACJI:
    1. Testuj różne metody
    2. Waliduj zachowanie rozkładów
    3. Sprawdź wpływ na korelacje
    4. Używaj cross-validation
    5. Monitoruj performance modelu
    
    📊 PO IMPUTACJI:
    1. Porównaj statystyki przed/po
    2. Sprawdź rozkłady zmiennych
    3. Testuj stabilność wyników
    4. Dokumentuj wpływ na model
    5. Rozważ sensitivity analysis
    
    ⚠️  CZĘSTE BŁĘDY:
    • Imputacja przed train/test split
    • Używanie target variable w imputacji
    • Ignorowanie typu missing data
    • Brak walidacji wyników
    • Over-imputation (>40% missing)
    """
    
    print(best_practices)

imputation_best_practices()
```

---

### 🎯 Następny krok

Poznasz **Data Cleaning - Duplicate Handling**:

- Identyfikacja duplikatów
- Różne typy duplikatów
- Strategie usuwania
- Fuzzy matching
- Validation after deduplication