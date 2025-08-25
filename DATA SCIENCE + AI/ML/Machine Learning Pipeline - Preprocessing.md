## 🏭 Machine Learning Pipeline - Preprocessing

_Budowa efektywnych pipeline'ów ML z preprocessing_

---

### 📝 Wprowadzenie do ML Pipelines

**ML Pipeline** to zautomatyzowany workflow, który:

1. **Standardyzuje** proces przygotowania danych
2. **Zapobiega** data leakage
3. **Zapewnia** reproductibility  
4. **Ułatwia** deployment modeli
5. **Przyspiesza** eksperymentowanie

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')
```

---

### 🏗️ Podstawowy Pipeline

```python
# Przykładowe dane
from sklearn.datasets import make_classification
from sklearn.datasets import load_titanic

# Tworzenie syntetycznego datasetu
X, y = make_classification(
    n_samples=1000, 
    n_features=10, 
    n_informative=8,
    n_redundant=2,
    n_classes=2,
    random_state=42
)

# Konwersja na DataFrame
feature_names = [f'feature_{i}' for i in range(X.shape[1])]
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y

# Dodanie niektórych realistic features
np.random.seed(42)
df['age'] = np.random.randint(18, 80, len(df))
df['income'] = np.random.lognormal(10, 1, len(df))
df['category'] = np.random.choice(['A', 'B', 'C'], len(df))

# Wprowadzenie missing values
missing_idx = np.random.choice(df.index, size=int(0.1 * len(df)), replace=False)
df.loc[missing_idx, 'age'] = np.nan
df.loc[missing_idx[:50], 'income'] = np.nan

print("=== DANE DO PIPELINE ===")
print(f"Kształt: {df.shape}")
print(f"Brakujące dane:\n{df.isnull().sum()}")
print(f"Typy danych:\n{df.dtypes.value_counts()}")
```

---

### 🔧 Preprocessing Transformers

```python
print("=== PREPROCESSING TRANSFORMERS ===")

# Podział danych
X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Identyfikacja typów kolumn
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = X.select_dtypes(include=['object']).columns.tolist()

print(f"Cechy numeryczne: {numeric_features}")
print(f"Cechy kategoryczne: {categorical_features}")

# 1. Numeric preprocessing pipeline
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# 2. Categorical preprocessing pipeline  
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
])

# 3. Combined preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Test preprocessor
print("\n=== TEST PREPROCESSORA ===")
X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

print(f"Kształt przed preprocessing: {X_train.shape}")
print(f"Kształt po preprocessing: {X_train_transformed.shape}")
print(f"Brakujące dane po preprocessing: {pd.isna(X_train_transformed).sum()}")

# Wizualizacja transformacji
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Przed preprocessing - numeric feature
feature_to_plot = 'income'
axes[0, 0].hist(X_train[feature_to_plot].dropna(), bins=50, alpha=0.7)
axes[0, 0].set_title(f'{feature_to_plot} - Before Preprocessing')

# Po preprocessing - ta sama cecha (scaled)
income_idx = numeric_features.index(feature_to_plot)
axes[0, 1].hist(X_train_transformed[:, income_idx], bins=50, alpha=0.7)
axes[0, 1].set_title(f'{feature_to_plot} - After Preprocessing')

# Korelacje przed i po
corr_before = X_train[numeric_features].corr()
# Korelacje po preprocessing (tylko numeric part)
n_numeric = len(numeric_features)
corr_after = pd.DataFrame(X_train_transformed[:, :n_numeric]).corr()

im1 = axes[1, 0].imshow(corr_before, cmap='coolwarm', vmin=-1, vmax=1)
axes[1, 0].set_title('Korelacje - Before')
plt.colorbar(im1, ax=axes[1, 0])

im2 = axes[1, 1].imshow(corr_after, cmap='coolwarm', vmin=-1, vmax=1)
axes[1, 1].set_title('Korelacje - After')
plt.colorbar(im2, ax=axes[1, 1])

plt.tight_layout()
plt.show()
```

---

### 🎯 Complete ML Pipeline

```python
print("=== COMPLETE ML PIPELINE ===")

# Definicja różnych modeli
models = {
    'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
    'random_forest': RandomForestClassifier(random_state=42, n_estimators=100)
}

# Tworzenie pipeline'ów dla każdego modelu
pipelines = {}
for name, model in models.items():
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])
    pipelines[name] = pipeline

# Cross-validation dla każdego pipeline'a
cv_results = {}
for name, pipeline in pipelines.items():
    scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='accuracy')
    cv_results[name] = {
        'mean_score': scores.mean(),
        'std_score': scores.std(),
        'scores': scores
    }
    
    print(f"\n{name.upper()} CV Results:")
    print(f"Mean Accuracy: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

# Trenowanie najlepszego modelu
best_model = max(cv_results.items(), key=lambda x: x[1]['mean_score'])
best_pipeline_name = best_model[0]
best_pipeline = pipelines[best_pipeline_name]

print(f"\n🏆 Najlepszy model: {best_pipeline_name}")

# Fit i evaluation
best_pipeline.fit(X_train, y_train)
y_pred = best_pipeline.predict(X_test)

print(f"\nTest Accuracy: {best_pipeline.score(X_test, y_test):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance (jeśli model to wspiera)
if hasattr(best_pipeline.named_steps['classifier'], 'feature_importances_'):
    # Pobieranie nazw cech po preprocessing
    feature_names_after = (
        numeric_features + 
        list(preprocessor.named_transformers_['cat']
             .named_steps['onehot']
             .get_feature_names_out(categorical_features))
    )
    
    importances = best_pipeline.named_steps['classifier'].feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': feature_names_after,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    print(f"\nTop 10 najważniejszych cech:")
    print(feature_importance_df.head(10))
    
    # Wizualizacja feature importance
    plt.figure(figsize=(10, 6))
    top_features = feature_importance_df.head(15)
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Feature Importance')
    plt.title('Top 15 Feature Importances')
    plt.tight_layout()
    plt.show()
```

---

### 🔍 Hyperparameter Tuning Pipeline

```python
print("=== HYPERPARAMETER TUNING PIPELINE ===")

# Pipeline z Random Forest
rf_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Grid search parameters
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [5, 10, 15, None],
    'classifier__min_samples_split': [2, 5, 10],
    'classifier__min_samples_leaf': [1, 2, 4]
}

# Grid Search z Cross-Validation
print("Rozpoczynam Grid Search...")
grid_search = GridSearchCV(
    rf_pipeline, 
    param_grid, 
    cv=3,  # 3-fold CV dla szybkości
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

print(f"\nNajlepsze parametry:")
for param, value in grid_search.best_params_.items():
    print(f"  {param}: {value}")

print(f"\nNajlepszy CV score: {grid_search.best_score_:.4f}")

# Evaluation na test set
best_model = grid_search.best_estimator_
test_score = best_model.score(X_test, y_test)
print(f"Test score najlepszego modelu: {test_score:.4f}")

# Analiza wyników grid search
results_df = pd.DataFrame(grid_search.cv_results_)
print(f"\nTop 5 kombinacji parametrów:")
top_results = results_df.nlargest(5, 'mean_test_score')[
    ['params', 'mean_test_score', 'std_test_score']
]
for idx, row in top_results.iterrows():
    print(f"Score: {row['mean_test_score']:.4f} (+/-{row['std_test_score']:.4f}) - {row['params']}")
```

---

### 🏪 Custom Transformers

```python
print("=== CUSTOM TRANSFORMERS ===")

from sklearn.base import BaseEstimator, TransformerMixin

class OutlierRemover(BaseEstimator, TransformerMixin):
    """Custom transformer do usuwania outlierów"""
    
    def __init__(self, factor=1.5):
        self.factor = factor
        
    def fit(self, X, y=None):
        # Oblicz IQR bounds dla każdej kolumny
        self.bounds_ = {}
        for col in range(X.shape[1]):
            Q1 = np.percentile(X[:, col], 25)
            Q3 = np.percentile(X[:, col], 75)
            IQR = Q3 - Q1
            self.bounds_[col] = {
                'lower': Q1 - self.factor * IQR,
                'upper': Q3 + self.factor * IQR
            }
        return self
    
    def transform(self, X):
        # Zastąp outliers przez granice IQR
        X_clean = X.copy()
        for col in range(X.shape[1]):
            bounds = self.bounds_[col]
            X_clean[:, col] = np.clip(X_clean[:, col], 
                                    bounds['lower'], 
                                    bounds['upper'])
        return X_clean

class LogTransformer(BaseEstimator, TransformerMixin):
    """Custom transformer do transformacji logarytmicznej"""
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Log1p transformation (log(1+x))
        return np.log1p(np.abs(X))

# Pipeline z custom transformers
custom_numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('outlier_remover', OutlierRemover(factor=1.5)),
    ('log_transform', LogTransformer()),
    ('scaler', StandardScaler())
])

custom_preprocessor = ColumnTransformer(
    transformers=[
        ('num', custom_numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Test custom pipeline
custom_pipeline = Pipeline([
    ('preprocessor', custom_preprocessor),
    ('classifier', RandomForestClassifier(random_state=42, n_estimators=100))
])

# Cross-validation custom pipeline
custom_scores = cross_val_score(custom_pipeline, X_train, y_train, cv=5, scoring='accuracy')
print(f"Custom Pipeline CV Accuracy: {custom_scores.mean():.4f} (+/- {custom_scores.std() * 2:.4f})")

# Porównanie z podstawowym pipeline
basic_scores = cross_val_score(pipelines['random_forest'], X_train, y_train, cv=5, scoring='accuracy')
print(f"Basic Pipeline CV Accuracy: {basic_scores.mean():.4f} (+/- {basic_scores.std() * 2:.4f})")

improvement = custom_scores.mean() - basic_scores.mean()
print(f"Improvement: {improvement:.4f}")
```

---

### 💾 Pipeline Serialization

```python
print("=== PIPELINE SERIALIZATION ===")

import joblib
from datetime import datetime

# Trenowanie finalnego modelu
final_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    ))
])

final_pipeline.fit(X_train, y_train)

# Zapisanie modelu
model_filename = f"ml_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
joblib.dump(final_pipeline, model_filename)
print(f"Model zapisany jako: {model_filename}")

# Zapisanie metadanych
metadata = {
    'model_type': 'RandomForestClassifier',
    'preprocessing_steps': [
        'SimpleImputer (median for numeric)',
        'StandardScaler',
        'SimpleImputer (constant for categorical)',
        'OneHotEncoder'
    ],
    'feature_columns': {
        'numeric': numeric_features,
        'categorical': categorical_features
    },
    'train_score': final_pipeline.score(X_train, y_train),
    'test_score': final_pipeline.score(X_test, y_test),
    'training_date': datetime.now().isoformat(),
    'train_size': len(X_train),
    'test_size': len(X_test)
}

metadata_filename = f"model_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
import json
with open(metadata_filename, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"Metadata zapisane jako: {metadata_filename}")

# Test wczytania modelu
loaded_pipeline = joblib.load(model_filename)
loaded_predictions = loaded_pipeline.predict(X_test)

# Sprawdzenie czy model działa identycznie
original_predictions = final_pipeline.predict(X_test)
identical_predictions = np.array_equal(original_predictions, loaded_predictions)

print(f"Wczytany model działa identycznie: {identical_predictions}")
print(f"Accuracy wczytanego modelu: {loaded_pipeline.score(X_test, y_test):.4f}")
```

---

### 🔄 Pipeline Validation Strategies

```python
def pipeline_validation_strategies():
    """Różne strategie walidacji pipeline'ów"""
    
    print("=== STRATEGIE WALIDACJI PIPELINE ===")
    
    from sklearn.model_selection import (
        cross_val_score, 
        StratifiedKFold, 
        TimeSeriesSplit,
        validation_curve,
        learning_curve
    )
    
    # 1. Cross-Validation Strategies
    cv_strategies = {
        'Standard 5-Fold': 5,
        'Stratified 5-Fold': StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
        'Time Series Split': TimeSeriesSplit(n_splits=5)  # Dla danych czasowych
    }
    
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=42, n_estimators=50))
    ])
    
    print("\n🔄 Cross-Validation Results:")
    for name, cv_strategy in cv_strategies.items():
        if name != 'Time Series Split':  # Skip time series dla tego przykładu
            scores = cross_val_score(pipeline, X_train, y_train, cv=cv_strategy, scoring='accuracy')
            print(f"{name}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
    
    # 2. Learning Curves
    print("\n📈 Learning Curves:")
    train_sizes, train_scores, val_scores = learning_curve(
        pipeline, X_train, y_train, cv=3,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='accuracy', n_jobs=-1
    )
    
    # Wizualizacja learning curves
    plt.figure(figsize=(10, 6))
    
    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)
    
    plt.plot(train_sizes, train_mean, 'o-', color='blue', label='Training Score')
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    
    plt.plot(train_sizes, val_mean, 'o-', color='red', label='Validation Score')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color='red')
    
    plt.xlabel('Training Set Size')
    plt.ylabel('Accuracy Score')
    plt.title('Learning Curves')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # 3. Validation Curves (dla hyperparameters)
    param_range = [10, 50, 100, 200, 500]
    train_scores, test_scores = validation_curve(
        pipeline, X_train, y_train, 
        param_name='classifier__n_estimators',
        param_range=param_range,
        cv=3, scoring='accuracy', n_jobs=-1
    )
    
    # Wizualizacja validation curves
    plt.figure(figsize=(10, 6))
    
    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    test_mean = test_scores.mean(axis=1)
    test_std = test_scores.std(axis=1)
    
    plt.plot(param_range, train_mean, 'o-', color='blue', label='Training Score')
    plt.fill_between(param_range, train_mean - train_std, train_mean + train_std, alpha=0.1, color='blue')
    
    plt.plot(param_range, test_mean, 'o-', color='red', label='Validation Score')
    plt.fill_between(param_range, test_mean - test_std, test_mean + test_std, alpha=0.1, color='red')
    
    plt.xlabel('Number of Estimators')
    plt.ylabel('Accuracy Score')
    plt.title('Validation Curve - n_estimators')
    plt.legend()
    plt.grid(True)
    plt.show()

# Uruchomienie walidacji
pipeline_validation_strategies()
```

---

### 💡 Best Practices

```python
def ml_pipeline_best_practices():
    """Najlepsze praktyki ML Pipeline"""
    
    practices = """
    ✅ ML PIPELINE BEST PRACTICES
    
    🏗️ CONSTRUCTION:
    1. Zawsze używaj Pipeline dla preprocessing + model
    2. Unikaj data leakage - fit tylko na train data
    3. Używaj ColumnTransformer dla różnych typów cech
    4. Twórz reusable custom transformers
    5. Dokumentuj każdy krok preprocessing
    
    🔧 PREPROCESSING:
    1. Handle missing values przed innymi transformacjami
    2. Standardizuj/skaluj cechy numeryczne
    3. Encode categorical variables properly
    4. Feature engineering w pipeline
    5. Validate transformations
    
    🎯 MODEL SELECTION:
    1. Cross-validation dla model selection
    2. Grid/Random search dla hyperparameters
    3. Zapisuj i ładuj kompletne pipeline
    4. Version control dla modeli
    5. A/B test w produkcji
    
    📊 VALIDATION:
    1. Stratified CV dla niezbalansowane dane
    2. Time-based split dla danych czasowych
    3. Learning curves dla diagnozy
    4. Feature importance analysis
    5. Model interpretability
    
    🚀 DEPLOYMENT:
    1. Serialize cały pipeline (nie tylko model)
    2. Zapisuj metadata i versioning
    3. Monitoring model performance
    4. Automated retraining
    5. Rollback capability
    
    ⚠️  CZĘSTE BŁĘDY:
    • Data leakage przez preprocessing przed split
    • Brak validation strategy
    • Overfitting przez złożone pipeline
    • Ignorowanie feature importance
    • Brak monitoring w produkcji
    """
    
    print(practices)

ml_pipeline_best_practices()
```

---

### 🎯 Następny krok

Poznasz **Cross Validation Techniques**:

- Advanced CV strategies
- Time series cross-validation
- Nested cross-validation
- Model selection best practices
- Bias-variance tradeoff analysis