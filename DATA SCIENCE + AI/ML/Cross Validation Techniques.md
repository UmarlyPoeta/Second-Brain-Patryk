## 🎲 Cross Validation Techniques

_Zaawansowane strategie walidacji modeli ML_

---

### 📝 Wprowadzenie do Cross Validation

**Cross Validation** to technika oceny modeli, która:

1. **Maksimalizuje** wykorzystanie danych
2. **Redukuje** overfitting w ocenie modelu
3. **Zapewnia** niezawodne estymacje performance
4. **Umożliwia** porównywanie modeli
5. **Identyfikuje** stabilność modelu

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import (
    cross_val_score, cross_validate,
    KFold, StratifiedKFold, RepeatedKFold,
    TimeSeriesSplit, GroupKFold,
    LeaveOneOut, LeavePOut,
    train_test_split
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')
```

---

### 🔀 Podstawowe strategie CV

```python
# Przygotowanie danych testowych
from sklearn.datasets import make_classification, make_regression

# Classification dataset
X_clf, y_clf = make_classification(
    n_samples=1000, n_features=20, n_informative=15, 
    n_redundant=5, n_classes=3, random_state=42
)

# Regression dataset  
X_reg, y_reg = make_regression(
    n_samples=1000, n_features=20, noise=0.1, random_state=42
)

print("=== PODSTAWOWE STRATEGIE CV ===")

# Modele do testowania
clf_model = RandomForestClassifier(n_estimators=100, random_state=42)
reg_model = RandomForestRegressor(n_estimators=100, random_state=42)

# 1. K-Fold Cross Validation
cv_strategies = {
    'KFold (5)': KFold(n_splits=5, shuffle=True, random_state=42),
    'KFold (10)': KFold(n_splits=10, shuffle=True, random_state=42),
    'StratifiedKFold (5)': StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    'RepeatedKFold (3x5)': RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)
}

print("🎯 CLASSIFICATION CV RESULTS:")
clf_results = {}
for name, cv_strategy in cv_strategies.items():
    if 'Stratified' in name:
        scores = cross_val_score(clf_model, X_clf, y_clf, cv=cv_strategy, scoring='accuracy')
    elif 'Repeated' in name:
        scores = cross_val_score(clf_model, X_clf, y_clf, cv=cv_strategy, scoring='accuracy')
    else:
        scores = cross_val_score(clf_model, X_clf, y_clf, cv=cv_strategy, scoring='accuracy')
    
    clf_results[name] = scores
    print(f"{name}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

print("\n📊 REGRESSION CV RESULTS:")
reg_results = {}
reg_cv_strategies = {k: v for k, v in cv_strategies.items() if 'Stratified' not in k}

for name, cv_strategy in reg_cv_strategies.items():
    scores = cross_val_score(reg_model, X_reg, y_reg, cv=cv_strategy, scoring='r2')
    reg_results[name] = scores
    print(f"{name}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")

# Wizualizacja wyników CV
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Classification results
clf_data = []
for strategy, scores in clf_results.items():
    for score in scores:
        clf_data.append({'Strategy': strategy, 'Score': score})

clf_df = pd.DataFrame(clf_data)
sns.boxplot(data=clf_df, x='Strategy', y='Score', ax=axes[0])
axes[0].set_title('Classification CV Scores Distribution')
axes[0].tick_params(axis='x', rotation=45)

# Regression results
reg_data = []
for strategy, scores in reg_results.items():
    for score in scores:
        reg_data.append({'Strategy': strategy, 'Score': score})

reg_df = pd.DataFrame(reg_data)
sns.boxplot(data=reg_df, x='Strategy', y='Score', ax=axes[1])
axes[1].set_title('Regression CV Scores Distribution')
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
```

---

### ⏰ Time Series Cross Validation

```python
print("=== TIME SERIES CROSS VALIDATION ===")

# Generowanie szeregu czasowego
np.random.seed(42)
n_samples = 1000
dates = pd.date_range('2020-01-01', periods=n_samples, freq='D')

# Trend + sezonowość + szum
trend = np.linspace(100, 200, n_samples)
seasonality = 10 * np.sin(2 * np.pi * np.arange(n_samples) / 365.25)
noise = np.random.normal(0, 5, n_samples)
time_series = trend + seasonality + noise

# Dodanie lagged features
ts_data = pd.DataFrame({
    'date': dates,
    'value': time_series
})

# Tworzenie lag features
for lag in [1, 7, 30]:
    ts_data[f'lag_{lag}'] = ts_data['value'].shift(lag)

# Rolling features
for window in [7, 30]:
    ts_data[f'rolling_mean_{window}'] = ts_data['value'].rolling(window).mean()
    ts_data[f'rolling_std_{window}'] = ts_data['value'].rolling(window).std()

# Usuwanie NaN
ts_data = ts_data.dropna()

X_ts = ts_data.drop(['date', 'value'], axis=1)
y_ts = ts_data['value']

print(f"Time series data shape: {X_ts.shape}")

# Time Series CV strategies
ts_cv_strategies = {
    'TimeSeriesSplit (5)': TimeSeriesSplit(n_splits=5),
    'TimeSeriesSplit (10)': TimeSeriesSplit(n_splits=10),
    'Regular KFold (WRONG!)': KFold(n_splits=5, shuffle=True, random_state=42)  # Dla porównania
}

print("\n⏰ TIME SERIES CV RESULTS:")
ts_model = RandomForestRegressor(n_estimators=50, random_state=42)

for name, cv_strategy in ts_cv_strategies.items():
    scores = cross_val_score(ts_model, X_ts, y_ts, cv=cv_strategy, scoring='r2')
    print(f"{name}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
    
    if name == 'Regular KFold (WRONG!)':
        print("  ⚠️  WARNING: Regular KFold for time series causes data leakage!")

# Wizualizacja Time Series Split
fig, axes = plt.subplots(3, 2, figsize=(15, 12))

tscv = TimeSeriesSplit(n_splits=5)
for i, (train_idx, test_idx) in enumerate(tscv.split(X_ts)):
    if i < 6:  # Plot first 6 splits
        ax = axes[i//2, i%2]
        
        # Plot całego szeregu
        ax.plot(range(len(y_ts)), y_ts.values, 'lightgray', alpha=0.5, label='Full Series')
        
        # Plot train/test splits
        ax.plot(train_idx, y_ts.iloc[train_idx], 'blue', alpha=0.7, label='Train')
        ax.plot(test_idx, y_ts.iloc[test_idx], 'red', alpha=0.7, label='Test')
        
        ax.set_title(f'Time Series Split {i+1}')
        ax.legend()
        ax.set_xlabel('Time Index')
        ax.set_ylabel('Value')

plt.tight_layout()
plt.show()

# Walk-Forward Validation
def walk_forward_validation(X, y, model, min_train_size=100):
    """Custom walk-forward validation"""
    scores = []
    
    for i in range(min_train_size, len(X) - 30, 30):  # Co 30 próbek
        # Training set: od początku do i
        X_train = X.iloc[:i]
        y_train = y.iloc[:i]
        
        # Test set: następne 30 próbek
        X_test = X.iloc[i:i+30]
        y_test = y.iloc[i:i+30]
        
        # Fit i predict
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Oblicz R²
        from sklearn.metrics import r2_score
        score = r2_score(y_test, y_pred)
        scores.append(score)
    
    return np.array(scores)

print(f"\n🚶 WALK-FORWARD VALIDATION:")
wf_scores = walk_forward_validation(X_ts, y_ts, ts_model)
print(f"Walk-Forward R²: {wf_scores.mean():.4f} (+/- {wf_scores.std() * 2:.4f})")
print(f"Number of validation windows: {len(wf_scores)}")
```

---

### 👥 Group-based Cross Validation

```python
print("=== GROUP-BASED CROSS VALIDATION ===")

# Generowanie danych z grupami (np. pacjenci, klienci, eksperyment)
np.random.seed(42)
n_groups = 50
n_samples_per_group = np.random.randint(10, 30, n_groups)

group_data = []
for group_id in range(n_groups):
    n_samples = n_samples_per_group[group_id]
    
    # Każda grupa ma swoją charakterystykę
    group_effect = np.random.normal(0, 2)
    
    X_group = np.random.normal(group_effect, 1, (n_samples, 5))
    y_group = (X_group.sum(axis=1) + group_effect + 
               np.random.normal(0, 0.5, n_samples))
    
    for i in range(n_samples):
        group_data.append({
            'group_id': group_id,
            'feature_0': X_group[i, 0],
            'feature_1': X_group[i, 1], 
            'feature_2': X_group[i, 2],
            'feature_3': X_group[i, 3],
            'feature_4': X_group[i, 4],
            'target': y_group[i]
        })

group_df = pd.DataFrame(group_data)
print(f"Group data shape: {group_df.shape}")
print(f"Number of groups: {group_df['group_id'].nunique()}")
print(f"Samples per group: {group_df.groupby('group_id').size().describe()}")

X_group = group_df.drop(['group_id', 'target'], axis=1)
y_group = group_df['target']
groups = group_df['group_id']

# Group CV strategies
group_cv_strategies = {
    'GroupKFold (5)': GroupKFold(n_splits=5),
    'Regular KFold (WRONG!)': KFold(n_splits=5, shuffle=True, random_state=42),
    'StratifiedKFold (WRONG!)': StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
}

print("\n👥 GROUP CV RESULTS:")
group_model = RandomForestRegressor(n_estimators=50, random_state=42)

for name, cv_strategy in group_cv_strategies.items():
    if 'Group' in name:
        scores = cross_val_score(group_model, X_group, y_group, cv=cv_strategy, 
                               groups=groups, scoring='r2')
    else:
        # Regular CV dla porównania (błędne podejście)
        y_binned = pd.qcut(y_group, q=5, labels=False)  # Dla stratified
        if 'Stratified' in name:
            scores = cross_val_score(group_model, X_group, y_binned, cv=cv_strategy, scoring='accuracy')
        else:
            scores = cross_val_score(group_model, X_group, y_group, cv=cv_strategy, scoring='r2')
    
    print(f"{name}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")
    
    if 'WRONG!' in name:
        print("  ⚠️  WARNING: Może powodować data leakage przez grupy!")

# Analiza grup w folds
print(f"\n🔍 ANALIZA GRUP W FOLDACH:")
gkf = GroupKFold(n_splits=5)
for fold, (train_idx, test_idx) in enumerate(gkf.split(X_group, y_group, groups)):
    train_groups = set(groups.iloc[train_idx])
    test_groups = set(groups.iloc[test_idx])
    overlap = train_groups.intersection(test_groups)
    
    print(f"Fold {fold+1}: Train groups: {len(train_groups)}, "
          f"Test groups: {len(test_groups)}, Overlap: {len(overlap)}")
    
    if len(overlap) > 0:
        print(f"  ⚠️  WARNING: Groups {overlap} appear in both train and test!")
```

---

### 🎯 Leave-One-Out i Leave-P-Out

```python
print("=== LEAVE-ONE-OUT / LEAVE-P-OUT CV ===")

# Mniejszy dataset dla LOO (LOO jest kosztowny obliczeniowo)
X_small, y_small = make_classification(
    n_samples=100, n_features=10, n_informative=8,
    n_classes=2, random_state=42
)

print(f"Small dataset shape: {X_small.shape}")

# LOO i LPO strategies
loo_strategies = {
    'LeaveOneOut': LeaveOneOut(),
    'LeavePOut (p=2)': LeavePOut(p=2),
    'LeavePOut (p=5)': LeavePOut(p=5),
    'KFold (5)': KFold(n_splits=5, shuffle=True, random_state=42)  # Dla porównania
}

print("\n🎯 LOO/LPO CV RESULTS:")
small_model = LogisticRegression(random_state=42, max_iter=1000)

loo_results = {}
for name, cv_strategy in loo_strategies.items():
    if 'LeavePOut (p=5)' in name:
        # LPO z p=5 na 100 próbek jest bardzo kosztowny - ograniczamy
        # Tylko dla demonstracji - normalnie unikamy wysokich p
        print(f"{name}: Skipped (too computationally expensive)")
        continue
        
    scores = cross_val_score(small_model, X_small, y_small, cv=cv_strategy, scoring='accuracy')
    loo_results[name] = scores
    
    # Statystyki
    n_folds = len(scores)
    print(f"{name}: {scores.mean():.4f} (+/- {scores.std() * 2:.4f}) "
          f"[{n_folds} folds]")

# Porównanie wariancji estymacji
print(f"\n📊 PORÓWNANIE WARIANCJI ESTYMACJI:")
for name, scores in loo_results.items():
    variance = scores.var()
    print(f"{name}: Variance = {variance:.6f}")

# Teoretyczne właściwości
theory_comparison = """
🎓 TEORETYCZNE PORÓWNANIA:

LeaveOneOut (LOO):
✅ Maksymalne wykorzystanie danych
✅ Niemal unbiased estimate
❌ Wysoka wariancja
❌ Kosztowny obliczeniowo
❌ Może być niestabilny

LeavePOut (LPO):  
✅ Kompromis między bias a variance
✅ Mniej wrażliwy na outliers niż LOO
❌ Bardzo kosztowny dla dużego p
❌ Liczba kombinacji rośnie wykładniczo

K-Fold CV:
✅ Dobry balance bias-variance
✅ Obliczeniowo efektywny
✅ Stabilne wyniki
❌ Większy bias niż LOO
❌ Może tracić informację przy małych k
"""

print(theory_comparison)
```

---

### 🔄 Nested Cross Validation

```python
print("=== NESTED CROSS VALIDATION ===")

from sklearn.model_selection import GridSearchCV

# Nested CV - właściwy sposób model selection + evaluation
def nested_cross_validation(X, y, model, param_grid, outer_cv=5, inner_cv=3):
    """
    Nested CV dla unbiased model evaluation
    - Outer loop: model evaluation 
    - Inner loop: hyperparameter tuning
    """
    
    outer_cv_strategy = StratifiedKFold(n_splits=outer_cv, shuffle=True, random_state=42)
    inner_cv_strategy = StratifiedKFold(n_splits=inner_cv, shuffle=True, random_state=42)
    
    nested_scores = []
    best_params_list = []
    
    print(f"🔄 Running Nested CV (Outer: {outer_cv}, Inner: {inner_cv})...")
    
    for fold, (train_idx, test_idx) in enumerate(outer_cv_strategy.split(X, y)):
        print(f"  Outer Fold {fold+1}/{outer_cv}")
        
        # Outer split
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        # Inner CV dla hyperparameter tuning
        grid_search = GridSearchCV(
            model, param_grid, cv=inner_cv_strategy,
            scoring='accuracy', n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        
        # Best model na outer test set
        best_score = grid_search.score(X_test, y_test)
        nested_scores.append(best_score)
        best_params_list.append(grid_search.best_params_)
        
        print(f"    Fold {fold+1} score: {best_score:.4f}")
        print(f"    Best params: {grid_search.best_params_}")
    
    return np.array(nested_scores), best_params_list

# Porównanie z regular CV (biased!)
print("📊 COMPARISON: Nested CV vs Regular CV")

# Model i hyperparameters
rf_model = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10]
}

# 1. Nested CV (unbiased)
nested_scores, nested_params = nested_cross_validation(
    X_clf, y_clf, rf_model, param_grid, outer_cv=5, inner_cv=3
)

print(f"\n🎯 NESTED CV RESULTS:")
print(f"Mean Score: {nested_scores.mean():.4f} (+/- {nested_scores.std() * 2:.4f})")
print(f"Individual Scores: {nested_scores}")

# 2. Regular CV (biased - model selection leakage)
print(f"\n⚠️  REGULAR CV (BIASED) RESULTS:")
regular_grid_search = GridSearchCV(
    rf_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1
)
regular_scores = cross_val_score(regular_grid_search, X_clf, y_clf, cv=5, scoring='accuracy')

print(f"Mean Score: {regular_scores.mean():.4f} (+/- {regular_scores.std() * 2:.4f})")
print(f"Individual Scores: {regular_scores}")

# Porównanie
bias_estimate = regular_scores.mean() - nested_scores.mean()
print(f"\n📈 BIAS ESTIMATE:")
print(f"Regular CV - Nested CV = {bias_estimate:.4f}")
if bias_estimate > 0.01:
    print("⚠️  Significant optimistic bias detected!")
else:
    print("✅ Bias appears minimal")

# Stabilność parametrów
print(f"\n🔧 PARAMETER STABILITY:")
param_counts = {}
for params in nested_params:
    for key, value in params.items():
        if key not in param_counts:
            param_counts[key] = {}
        if value not in param_counts[key]:
            param_counts[key][value] = 0
        param_counts[key][value] += 1

for param, counts in param_counts.items():
    print(f"{param}:")
    for value, count in counts.items():
        percentage = (count / len(nested_params)) * 100
        print(f"  {value}: {count}/{len(nested_params)} ({percentage:.1f}%)")
```

---

### 📊 Cross Validation Diagnostics

```python
def cv_diagnostics(X, y, model, cv_strategy, scoring='accuracy'):
    """Szczegółowa diagnostyka Cross Validation"""
    
    print("=== CV DIAGNOSTICS ===")
    
    # Multiple metrics
    scoring_metrics = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
    
    cv_results = cross_validate(
        model, X, y, cv=cv_strategy, 
        scoring=scoring_metrics,
        return_train_score=True,
        return_estimator=True
    )
    
    # Analiza wyników
    print(f"📊 CROSS VALIDATION RESULTS:")
    for metric in scoring_metrics:
        test_scores = cv_results[f'test_{metric}']
        train_scores = cv_results[f'train_{metric}']
        
        print(f"\n{metric.upper()}:")
        print(f"  Test:  {test_scores.mean():.4f} (+/- {test_scores.std() * 2:.4f})")
        print(f"  Train: {train_scores.mean():.4f} (+/- {train_scores.std() * 2:.4f})")
        
        # Overfitting check
        overfitting = train_scores.mean() - test_scores.mean()
        if overfitting > 0.1:
            print(f"  ⚠️  Possible overfitting: {overfitting:.4f}")
        elif overfitting < -0.05:
            print(f"  ⚠️  Possible underfitting: {overfitting:.4f}")
        else:
            print(f"  ✅ Good fit: {overfitting:.4f}")
    
    # Stabilność między folds
    print(f"\n📈 FOLD STABILITY:")
    test_acc = cv_results['test_accuracy']
    stability = test_acc.std()
    
    if stability < 0.02:
        print(f"✅ Very stable: std = {stability:.4f}")
    elif stability < 0.05:
        print(f"✅ Stable: std = {stability:.4f}")
    else:
        print(f"⚠️  Unstable: std = {stability:.4f}")
    
    # Feature importance stability (jeśli model wspiera)
    if hasattr(model, 'feature_importances_') or hasattr(model, 'coef_'):
        print(f"\n🎯 FEATURE IMPORTANCE STABILITY:")
        
        importances_per_fold = []
        for estimator in cv_results['estimator']:
            if hasattr(estimator, 'feature_importances_'):
                importances_per_fold.append(estimator.feature_importances_)
            elif hasattr(estimator, 'coef_'):
                importances_per_fold.append(np.abs(estimator.coef_[0]))
        
        if importances_per_fold:
            importances_array = np.array(importances_per_fold)
            importance_std = importances_array.std(axis=0)
            importance_mean = importances_array.mean(axis=0)
            
            # CV of feature importances
            cv_importance = importance_std / importance_mean
            unstable_features = np.where(cv_importance > 0.5)[0]
            
            print(f"Features with high importance variability: {list(unstable_features)}")
            if len(unstable_features) > 0:
                print("⚠️  Some features have unstable importance across folds")
            else:
                print("✅ Feature importances are stable across folds")
    
    return cv_results

# Diagnostyka dla różnych modeli
models_to_test = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000)
}

cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for name, model in models_to_test.items():
    print(f"\n{'='*50}")
    print(f"DIAGNOSTICS FOR: {name}")
    print(f"{'='*50}")
    
    results = cv_diagnostics(X_clf, y_clf, model, cv_strategy)
    
    # Vizualizacja train vs test scores
    plt.figure(figsize=(10, 6))
    folds = range(1, len(results['test_accuracy']) + 1)
    
    plt.plot(folds, results['train_accuracy'], 'o-', label='Train Accuracy', color='blue')
    plt.plot(folds, results['test_accuracy'], 'o-', label='Test Accuracy', color='red')
    
    plt.xlabel('Fold')
    plt.ylabel('Accuracy')
    plt.title(f'{name} - Train vs Test Accuracy Across Folds')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
```

---

### 💡 Best Practices

```python
def cv_best_practices():
    """Najlepsze praktyki Cross Validation"""
    
    practices = """
    ✅ CROSS VALIDATION BEST PRACTICES
    
    🎯 WYBÓR STRATEGII:
    • Stratified CV → niezbalansowane klasy
    • Time Series CV → dane czasowe
    • Group CV → zależności grupowe
    • Repeated CV → większa stabilność
    • LOO → małe datasety (< 100 próbek)
    
    📊 OCENA MODELU:
    • Nested CV dla unbiased evaluation
    • Multiple metrics evaluation
    • Train vs test score comparison
    • Feature importance stability
    • Learning curves analysis
    
    ⚠️  UNIKAJ:
    • Data leakage w preprocessing
    • Model selection bez nested CV
    • Ignorowania grup/czasu
    • Zbyt małych fold'ów (< 5)
    • Overfitting do CV scores
    
    🔍 DIAGNOSTYKA:
    • Sprawdź stabilność między folds
    • Analizuj outlying folds
    • Monitoruj overfitting
    • Waliduj na holdout test set
    • Dokumentuj wszystkie decyzje
    
    📈 OPTYMALIZACJA:
    • Parallelize gdy możliwe
    • Cache preprocessing steps
    • Progressive validation
    • Early stopping w iterative models
    • Stratified sampling w małych klasach
    """
    
    print(practices)

cv_best_practices()
```

---

### 🎯 Następny krok

Poznasz **Data Visualization - Best Practices**:

- Zasady effective data visualization
- Color theory w data science
- Interactive visualizations
- Dashboard design principles
- Storytelling with data