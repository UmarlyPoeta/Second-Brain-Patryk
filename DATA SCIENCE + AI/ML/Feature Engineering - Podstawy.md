## 🔍 Feature Engineering - Podstawy

_Tworzenie i transformacja cech do modelowania_

---

### 📝 Wprowadzenie do Feature Engineering

**Feature Engineering** to proces tworzenia nowych cech z istniejących danych w celu:

1. **Poprawy performance** modeli ML
2. **Uchwycenia wzorców** niewidocznych w surowych danych  
3. **Redukcji wymiarowości** przez intelligent feature selection
4. **Reprezentacji wiedzy domenowej** w danych

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
```

---

### 🔢 Transformacje numeryczne

```python
# Przykładowe dane
np.random.seed(42)
data = pd.DataFrame({
    'price': np.random.lognormal(8, 1, 1000),
    'income': np.random.normal(50000, 15000, 1000),
    'age': np.random.randint(18, 80, 1000),
    'score': np.random.beta(2, 5, 1000) * 100,
    'sales': np.random.poisson(10, 1000)
})

# Podstawowe statystyki
print("=== ORYGINALNE DANE ===")
print(data.describe())

# 1. Scaling/Normalization
scalers = {
    'StandardScaler': StandardScaler(),
    'MinMaxScaler': MinMaxScaler(), 
    'RobustScaler': RobustScaler()
}

scaled_data = {}
for name, scaler in scalers.items():
    scaled_data[name] = pd.DataFrame(
        scaler.fit_transform(data),
        columns=data.columns
    )

# Porównanie rozkładów po skalowaniu
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
axes = axes.flatten()

columns_to_plot = ['price', 'income', 'age', 'score']
for i, col in enumerate(columns_to_plot):
    # Oryginalny rozkład
    data[col].hist(bins=50, alpha=0.5, ax=axes[i], label='Original', density=True)
    
    # Skalowane rozkłady
    colors = ['red', 'green', 'orange']
    for j, (name, scaled) in enumerate(scaled_data.items()):
        scaled[col].hist(bins=50, alpha=0.3, ax=axes[i], 
                        color=colors[j], label=name, density=True)
    
    axes[i].set_title(f'Rozkład: {col}')
    axes[i].legend()

plt.tight_layout()
plt.show()

# 2. Transformacje matematyczne
print("\n=== TRANSFORMACJE MATEMATYCZNE ===")

# Log transformation (dla skewed data)
data['price_log'] = np.log1p(data['price'])  # log(1+x) - bezpieczny dla 0
data['income_log'] = np.log1p(data['income'])

# Square root transformation
data['sales_sqrt'] = np.sqrt(data['sales'])

# Box-Cox transformation
from scipy.stats import boxcox
data['price_boxcox'], lambda_price = boxcox(data['price'])

# Power transformations
data['score_squared'] = data['score'] ** 2
data['age_cube'] = data['age'] ** 3

# Reciprocal transformation
data['price_reciprocal'] = 1 / (data['price'] + 1e-8)  # +epsilon dla stabilności

print("Nowe cechy po transformacjach:")
print(data[['price_log', 'income_log', 'sales_sqrt', 'price_boxcox']].describe())
```

---

### 🏷️ Encoding zmiennych kategorycznych

```python
# Dane kategoryczne
categorical_data = pd.DataFrame({
    'city': np.random.choice(['Warszawa', 'Kraków', 'Gdańsk', 'Wrocław', 'Poznań'], 1000),
    'education': np.random.choice(['Podstawowe', 'Średnie', 'Wyższe', 'Podyplomowe'], 1000),
    'department': np.random.choice(['IT', 'HR', 'Finance', 'Marketing', 'Sales'], 1000),
    'rating': np.random.choice(['Bardzo słabe', 'Słabe', 'Średnie', 'Dobre', 'Bardzo dobre'], 1000)
})

print("=== ENCODING KATEGORYCZNYCH ===")
print(categorical_data.head())

# 1. Label Encoding (dla ordinal data)
from sklearn.preprocessing import LabelEncoder

# Dla education (ma naturalny porządek)
education_le = LabelEncoder()
categorical_data['education_encoded'] = education_le.fit_transform(categorical_data['education'])

# Manual ordinal encoding dla rating
rating_mapping = {
    'Bardzo słabe': 1, 'Słabe': 2, 'Średnie': 3, 'Dobre': 4, 'Bardzo dobre': 5
}
categorical_data['rating_ordinal'] = categorical_data['rating'].map(rating_mapping)

# 2. One-Hot Encoding (dla nominal data)
city_dummies = pd.get_dummies(categorical_data['city'], prefix='city')
department_dummies = pd.get_dummies(categorical_data['department'], prefix='dept')

# 3. Target Encoding (mean encoding)
def target_encode(df, categorical_col, target_col):
    """Target encoding z regularyzacją"""
    target_mean = df[target_col].mean()
    target_count = df.groupby(categorical_col)[target_col].count()
    target_sum = df.groupby(categorical_col)[target_col].sum()
    
    # Regularyzacja (smoothing)
    alpha = 100  # parametr regularyzacji
    encoded = (target_sum + alpha * target_mean) / (target_count + alpha)
    
    return df[categorical_col].map(encoded)

# Symulacja target variable
np.random.seed(42)
target = np.random.normal(50, 10, len(categorical_data))
categorical_data['target'] = target

categorical_data['city_target_encoded'] = target_encode(categorical_data, 'city', 'target')

# 4. Frequency Encoding
categorical_data['city_frequency'] = categorical_data['city'].map(
    categorical_data['city'].value_counts()
)

# 5. Binary Encoding (dla high cardinality)
def binary_encode(series):
    """Prosta implementacja binary encoding"""
    le = LabelEncoder()
    encoded = le.fit_transform(series)
    
    # Konwersja na reprezentację binarną
    max_val = encoded.max()
    n_bits = int(np.ceil(np.log2(max_val + 1)))
    
    binary_df = pd.DataFrame()
    for i in range(n_bits):
        binary_df[f'bit_{i}'] = (encoded >> i) & 1
    
    return binary_df

city_binary = binary_encode(categorical_data['city'])

print("\nPrzykład encodingu:")
comparison = pd.concat([
    categorical_data[['city', 'city_frequency', 'city_target_encoded']].head(),
    city_dummies.head(),
    city_binary.head()
], axis=1)
print(comparison)
```

---

### 📅 Feature Engineering dla dat

```python
# Generowanie danych czasowych
date_range = pd.date_range('2020-01-01', '2023-12-31', freq='D')
time_data = pd.DataFrame({
    'date': np.random.choice(date_range, 1000),
    'value': np.random.normal(100, 20, 1000)
})
time_data = time_data.sort_values('date').reset_index(drop=True)

print("=== FEATURE ENGINEERING DLA DAT ===")

# Podstawowe cechy czasowe
time_data['year'] = time_data['date'].dt.year
time_data['month'] = time_data['date'].dt.month
time_data['day'] = time_data['date'].dt.day
time_data['day_of_week'] = time_data['date'].dt.dayofweek
time_data['day_of_year'] = time_data['date'].dt.dayofyear
time_data['week_of_year'] = time_data['date'].dt.isocalendar().week
time_data['quarter'] = time_data['date'].dt.quarter

# Binarne cechy czasowe
time_data['is_weekend'] = time_data['day_of_week'].isin([5, 6]).astype(int)
time_data['is_month_start'] = time_data['date'].dt.is_month_start.astype(int)
time_data['is_month_end'] = time_data['date'].dt.is_month_end.astype(int)
time_data['is_quarter_start'] = time_data['date'].dt.is_quarter_start.astype(int)

# Cykliczne cechy (dla okresowości)
time_data['month_sin'] = np.sin(2 * np.pi * time_data['month'] / 12)
time_data['month_cos'] = np.cos(2 * np.pi * time_data['month'] / 12)
time_data['day_of_week_sin'] = np.sin(2 * np.pi * time_data['day_of_week'] / 7)
time_data['day_of_week_cos'] = np.cos(2 * np.pi * time_data['day_of_week'] / 7)

# Różnice czasowe
reference_date = pd.Timestamp('2020-01-01')
time_data['days_since_start'] = (time_data['date'] - reference_date).dt.days

# Lag features
time_data = time_data.sort_values('date')
for lag in [1, 7, 30]:
    time_data[f'value_lag_{lag}'] = time_data['value'].shift(lag)

# Rolling features
for window in [7, 30]:
    time_data[f'value_rolling_mean_{window}'] = time_data['value'].rolling(window).mean()
    time_data[f'value_rolling_std_{window}'] = time_data['value'].rolling(window).std()

# Seasonal features
time_data['season'] = time_data['month'].map({
    12: 'Winter', 1: 'Winter', 2: 'Winter',
    3: 'Spring', 4: 'Spring', 5: 'Spring', 
    6: 'Summer', 7: 'Summer', 8: 'Summer',
    9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
})

print("Nowe cechy czasowe:")
print(time_data.columns.tolist())

# Wizualizacja cech cyklicznych
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Cykliczność miesięcy
scatter = axes[0].scatter(time_data['month_sin'], time_data['month_cos'], 
                         c=time_data['month'], cmap='hsv')
axes[0].set_xlabel('Month Sin')
axes[0].set_ylabel('Month Cos')
axes[0].set_title('Cykliczne kodowanie miesięcy')
plt.colorbar(scatter, ax=axes[0])

# Cykliczność dni tygodnia
scatter = axes[1].scatter(time_data['day_of_week_sin'], time_data['day_of_week_cos'],
                         c=time_data['day_of_week'], cmap='Set1')
axes[1].set_xlabel('Day of Week Sin')
axes[1].set_ylabel('Day of Week Cos') 
axes[1].set_title('Cykliczne kodowanie dni tygodnia')
plt.colorbar(scatter, ax=axes[1])

plt.tight_layout()
plt.show()
```

---

### 📝 Text Feature Engineering

```python
# Przykładowe dane tekstowe
text_data = pd.DataFrame({
    'review': [
        "Produkt bardzo dobry, polecam wszystkim",
        "Słaba jakość, nie warta pieniędzy",
        "Przeciętny produkt, nic specjalnego",
        "Excellent quality, highly recommend!",
        "Poor service, would not buy again",
        "Amazing product, best purchase ever!",
        "Terrible experience, waste of money",
        "Good value for money, satisfied"
    ] * 125  # 1000 próbek
})

print("=== TEXT FEATURE ENGINEERING ===")

# Podstawowe cechy tekstowe
text_data['text_length'] = text_data['review'].str.len()
text_data['word_count'] = text_data['review'].str.split().str.len()
text_data['char_count'] = text_data['review'].apply(lambda x: len(x))
text_data['avg_word_length'] = text_data['char_count'] / text_data['word_count']

# Cechy interpunkcyjne i stylistyczne
text_data['exclamation_count'] = text_data['review'].str.count('!')
text_data['question_count'] = text_data['review'].str.count('\\?')
text_data['uppercase_count'] = text_data['review'].str.count('[A-Z]')
text_data['digit_count'] = text_data['review'].str.count('[0-9]')

# Sentiment-based features (prosty słownik)
positive_words = ['good', 'great', 'excellent', 'amazing', 'recommend', 'dobry', 'polecam']
negative_words = ['bad', 'terrible', 'poor', 'awful', 'waste', 'słaba', 'słaby']

text_data['positive_word_count'] = text_data['review'].apply(
    lambda x: sum(1 for word in positive_words if word.lower() in x.lower())
)
text_data['negative_word_count'] = text_data['review'].apply(
    lambda x: sum(1 for word in negative_words if word.lower() in x.lower())
)
text_data['sentiment_score'] = text_data['positive_word_count'] - text_data['negative_word_count']

# TF-IDF Features
tfidf = TfidfVectorizer(max_features=50, stop_words='english', lowercase=True)
tfidf_matrix = tfidf.fit_transform(text_data['review'])
tfidf_features = pd.DataFrame(tfidf_matrix.toarray(), 
                             columns=[f'tfidf_{word}' for word in tfidf.get_feature_names_out()])

# Połączenie wszystkich cech
text_features = pd.concat([text_data, tfidf_features], axis=1)

print("Podstawowe cechy tekstowe:")
print(text_data[['text_length', 'word_count', 'avg_word_length', 'sentiment_score']].describe())

print(f"\nTF-IDF cechy: {tfidf_features.shape[1]} kolumn")
print("Przykład słów TF-IDF:", list(tfidf.get_feature_names_out())[:10])
```

---

### 🔄 Interakcje i kombinacje cech

```python
# Powrót do danych numerycznych
interaction_data = data[['age', 'income', 'price', 'score']].copy()

print("=== INTERAKCJE MIĘDZY CECHAMI ===")

# 1. Interakcje multiplikatywne
interaction_data['age_income'] = interaction_data['age'] * interaction_data['income']
interaction_data['price_score'] = interaction_data['price'] * interaction_data['score']

# 2. Interakcje addytywne
interaction_data['age_plus_score'] = interaction_data['age'] + interaction_data['score']

# 3. Ratios i proporcje
interaction_data['price_income_ratio'] = interaction_data['price'] / (interaction_data['income'] + 1e-8)
interaction_data['score_per_age'] = interaction_data['score'] / (interaction_data['age'] + 1e-8)

# 4. Różnice
interaction_data['income_price_diff'] = interaction_data['income'] - interaction_data['price']

# 5. Binning i discretization
def create_bins(series, n_bins=5, labels=None):
    """Tworzenie binów z równą liczbą obserwacji"""
    if labels is None:
        labels = [f'bin_{i}' for i in range(n_bins)]
    return pd.qcut(series, n_bins, labels=labels, duplicates='drop')

interaction_data['age_binned'] = create_bins(interaction_data['age'], 5, 
                                           ['Young', 'Adult', 'Middle', 'Senior', 'Elder'])
interaction_data['income_binned'] = create_bins(interaction_data['income'], 3,
                                              ['Low', 'Medium', 'High'])

# 6. Polynomial features
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False)
base_features = interaction_data[['age', 'income', 'score']].values
poly_features = poly.fit_transform(base_features)

poly_feature_names = poly.get_feature_names_out(['age', 'income', 'score'])
poly_df = pd.DataFrame(poly_features, columns=poly_feature_names)

print("Polynomial features utworzonych:", len(poly_feature_names))
print("Przykład polynomial features:", poly_feature_names[:10])

# 7. Domain-specific combinations
interaction_data['affordability'] = interaction_data['income'] / interaction_data['price']
interaction_data['value_score'] = interaction_data['score'] / np.log1p(interaction_data['price'])
interaction_data['experience_factor'] = interaction_data['age'] * interaction_data['score'] / 100

print("\nNowe cechy interakcyjne:")
new_features = ['age_income', 'price_income_ratio', 'affordability', 'value_score']
print(interaction_data[new_features].describe())
```

---

### 🎯 Feature Selection

```python
# Generowanie target variable
np.random.seed(42)
n_samples = len(interaction_data)
target = (
    0.5 * interaction_data['age'] + 
    0.3 * np.log1p(interaction_data['income']) +
    0.2 * interaction_data['score'] +
    0.1 * interaction_data['age_income'] / 1000000 +
    np.random.normal(0, 10, n_samples)
)

print("=== FEATURE SELECTION ===")

# 1. Korelacja z target
numeric_features = interaction_data.select_dtypes(include=[np.number])
correlations = numeric_features.corrwith(target).abs().sort_values(ascending=False)

print("Top 10 cech według korelacji z target:")
print(correlations.head(10))

# 2. Mutual Information
from sklearn.feature_selection import mutual_info_regression

mi_scores = mutual_info_regression(numeric_features, target)
mi_df = pd.DataFrame({'feature': numeric_features.columns, 'mi_score': mi_scores})
mi_df = mi_df.sort_values('mi_score', ascending=False)

print("\nTop 10 cech według Mutual Information:")
print(mi_df.head(10))

# 3. Variance Threshold
from sklearn.feature_selection import VarianceThreshold

var_selector = VarianceThreshold(threshold=0.1)  # Usuń cechy z małą wariancją
selected_features = var_selector.fit_transform(numeric_features)

print(f"\nCechy po Variance Threshold: {selected_features.shape[1]} z {numeric_features.shape[1]}")

# 4. Wizualizacja ważności cech
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Korelacje
correlations.head(15).plot(kind='barh', ax=axes[0])
axes[0].set_title('Top 15 cech - Korelacja z target')

# Mutual Information
mi_df.head(15).plot(x='feature', y='mi_score', kind='barh', ax=axes[1])
axes[1].set_title('Top 15 cech - Mutual Information')

plt.tight_layout()
plt.show()
```

---

### 💡 Best Practices

```python
def feature_engineering_best_practices():
    """Najlepsze praktyki Feature Engineering"""
    
    practices = """
    ✅ NAJLEPSZE PRAKTYKI FEATURE ENGINEERING
    
    📊 PRZYGOTOWANIE:
    1. Zrozum problem biznesowy i dane
    2. Rozpocznij od eksploracyjnej analizy danych
    3. Zidentyfikuj wzorce i anomalie
    4. Określ typ zmiennych (numerical, categorical, text, time)
    
    🔧 TWORZENIE CECH:
    1. Wykorzystaj wiedzę domenową
    2. Twórz cechy na różnych poziomach agregacji
    3. Rozważ interakcje między zmiennymi
    4. Eksperymentuj z transformacjami matematycznymi
    5. Uważaj na data leakage
    
    📈 SELEKCJA CECH:
    1. Usuń cechy z niską wariancją
    2. Sprawdź korelacje między cechami
    3. Użyj statystycznych testów istotności
    4. Zastosuj algorytmy feature importance
    5. Waliduj na danych out-of-sample
    
    🎯 WALIDACJA:
    1. Cross-validation dla oceny cech
    2. Monitoruj overfitting
    3. Testuj stabilność cech w czasie
    4. Dokumentuj wszystkie transformacje
    5. A/B testuj wpływ na model
    
    ⚠️  CZĘSTE BŁĘDY:
    • Data leakage przez użycie przyszłych informacji
    • Over-engineering - zbyt wiele cech
    • Brak walidacji na unseen data
    • Ignorowanie korelacji między cechami
    • Transformacje przed train/test split
    """
    
    print(practices)
    
    # Checklist dla Feature Engineering
    checklist = """
    📋 CHECKLIST FEATURE ENGINEERING
    
    🔍 EKSPLORACJA:
    □ Analiza rozkładów zmiennych
    □ Identyfikacja outlierów
    □ Sprawdzenie brakujących danych
    □ Analiza korelacji
    
    🛠️ TRANSFORMACJE:
    □ Scaling/normalizacja zmiennych numerycznych
    □ Encoding zmiennych kategorycznych  
    □ Obsługa zmiennych tekstowych
    □ Feature extraction z dat
    
    🎨 TWORZENIE CECH:
    □ Interakcje między zmiennymi
    □ Agregacje grupowe
    □ Window functions
    □ Domain-specific features
    
    📊 SELEKCJA:
    □ Usunięcie cech z niską wariancją
    □ Kontrola multicollinearity
    □ Feature importance analysis
    □ Dimensionality reduction
    
    ✅ WALIDACJA:
    □ Cross-validation
    □ Out-of-time validation
    □ Stability tests
    □ Business validation
    """
    
    print(checklist)

feature_engineering_best_practices()
```

---

### 🎯 Następny krok

Poznasz **Statistical Testing - Podstawy**:

- Testy hipotez statystycznych
- A/B testing w Data Science
- Power analysis
- Multiple testing corrections
- Practical significance vs statistical significance