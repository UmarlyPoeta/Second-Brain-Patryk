## 🔬 Scikit-learn - Podstawy i Pipeline

_Wprowadzenie do biblioteki Scikit-learn i konstrukcja pipeline'ów ML_

---

### 📝 Wprowadzenie do Scikit-learn

**Scikit-learn** to najważniejsza biblioteka uczenia maszynowego w Python:

1. **Unified API** - spójny interfejs dla wszystkich algorytmów
2. **Rich ecosystem** - preprocessing, model selection, evaluation
3. **Production ready** - stabilne, optimized implementations
4. **Extensible** - łatwe tworzenie custom transformers
5. **Well documented** - excellent documentation i examples

---

### 🏗️ Scikit-learn API Overview

#### Core components understanding

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

def demonstrate_sklearn_api():
    """Demonstracja podstawowego API Scikit-learn"""
    
    print("Scikit-learn API Overview:")
    print("=" * 40)
    
    # 1. Dataset creation
    print("1. Dataset Creation:")
    
    # Classification dataset
    X_class, y_class = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=10,
        n_redundant=5,
        n_clusters_per_class=1,
        random_state=42
    )
    
    print(f"   Classification dataset: {X_class.shape}, {np.unique(y_class, return_counts=True)}")
    
    # Regression dataset
    X_reg, y_reg = make_regression(
        n_samples=1000,
        n_features=15,
        n_informative=10,
        noise=0.1,
        random_state=42
    )
    
    print(f"   Regression dataset: {X_reg.shape}, y range: [{y_reg.min():.2f}, {y_reg.max():.2f}]")
    
    # 2. Train-test split
    print(f"\n2. Train-Test Split:")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_class, y_class, 
        test_size=0.2, 
        stratify=y_class,  # Maintain class balance
        random_state=42
    )
    
    print(f"   Training set: {X_train.shape}")
    print(f"   Test set: {X_test.shape}")
    print(f"   Train classes: {np.bincount(y_train)}")
    print(f"   Test classes: {np.bincount(y_test)}")
    
    # 3. Preprocessing
    print(f"\n3. Preprocessing (Standardization):")
    
    scaler = StandardScaler()
    
    # Fit scaler na training data
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Transform test data (bez refitting!)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"   Original feature means: {X_train.mean(axis=0)[:3]}")
    print(f"   Scaled feature means: {X_train_scaled.mean(axis=0)[:3]}")
    print(f"   Original feature stds: {X_train.std(axis=0)[:3]}")
    print(f"   Scaled feature stds: {X_train_scaled.std(axis=0)[:3]}")
    
    # 4. Model training i prediction
    print(f"\n4. Model Training & Prediction:")
    
    # Logistic Regression
    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train_scaled, y_train)
    lr_predictions = lr_model.predict(X_test_scaled)
    lr_probabilities = lr_model.predict_proba(X_test_scaled)
    
    print(f"   Logistic Regression accuracy: {accuracy_score(y_test, lr_predictions):.4f}")
    print(f"   Probability shape: {lr_probabilities.shape}")
    print(f"   Sample probabilities: {lr_probabilities[:3]}")
    
    # Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)  # RF nie wymaga scaling, ale dla consistency
    rf_predictions = rf_model.predict(X_test_scaled)
    
    print(f"   Random Forest accuracy: {accuracy_score(y_test, rf_predictions):.4f}")
    
    # 5. Model evaluation
    print(f"\n5. Model Evaluation:")
    
    print("   Logistic Regression Report:")
    print(classification_report(y_test, lr_predictions, target_names=['Class 0', 'Class 1']))
    
    # 6. Model inspection
    print(f"\n6. Model Inspection:")
    
    # Logistic Regression coefficients
    print(f"   LR coefficients shape: {lr_model.coef_.shape}")
    print(f"   LR intercept: {lr_model.intercept_}")
    
    # Random Forest feature importance
    feature_importance = rf_model.feature_importances_
    print(f"   RF feature importance (top 5): {np.argsort(feature_importance)[-5:]}")
    print(f"   RF importance values (top 5): {np.sort(feature_importance)[-5:]}")

demonstrate_sklearn_api()
```

#### Estimator types understanding

```python
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def demonstrate_estimator_types():
    """Demonstracja różnych typów estimators"""
    
    print("Scikit-learn Estimator Types:")
    print("=" * 40)
    
    # Test data
    np.random.seed(42)
    X_numeric = np.random.randn(100, 5)
    X_categorical = np.random.choice(['A', 'B', 'C'], size=(100, 2))
    y_binary = np.random.choice([0, 1], size=100)
    y_multiclass = np.random.choice([0, 1, 2], size=100)
    
    # 1. Transformers (fit + transform)
    print("1. Transformers:")
    
    # Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_numeric)
    print(f"   StandardScaler: {X_numeric.shape} -> {X_scaled.shape}")
    
    # PCA
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_numeric)
    print(f"   PCA: {X_numeric.shape} -> {X_pca.shape}")
    print(f"   Explained variance ratio: {pca.explained_variance_ratio_}")
    
    # OneHotEncoder
    ohe = OneHotEncoder(sparse_output=False)
    X_encoded = ohe.fit_transform(X_categorical)
    print(f"   OneHotEncoder: {X_categorical.shape} -> {X_encoded.shape}")
    print(f"   Categories: {ohe.categories_}")
    
    # 2. Predictors (fit + predict)
    print(f"\n2. Predictors:")
    
    # Classifier
    classifier = LogisticRegression(random_state=42)
    classifier.fit(X_scaled, y_binary)
    y_pred_class = classifier.predict(X_scaled)
    y_proba = classifier.predict_proba(X_scaled)
    
    print(f"   Classifier predictions shape: {y_pred_class.shape}")
    print(f"   Classifier probabilities shape: {y_proba.shape}")
    print(f"   Classifier accuracy: {accuracy_score(y_binary, y_pred_class):.4f}")
    
    # Regressor
    from sklearn.linear_model import LinearRegression
    y_continuous = X_numeric[:, 0] * 2 + X_numeric[:, 1] + np.random.randn(100) * 0.1
    
    regressor = LinearRegression()
    regressor.fit(X_scaled, y_continuous)
    y_pred_reg = regressor.predict(X_scaled)
    
    print(f"   Regressor predictions shape: {y_pred_reg.shape}")
    print(f"   Regressor R²: {regressor.score(X_scaled, y_continuous):.4f}")
    
    # 3. Clustering (fit + predict/transform)
    print(f"\n3. Clustering:")
    
    clustering = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = clustering.fit_predict(X_scaled)
    
    print(f"   Clustering labels: {np.bincount(cluster_labels)}")
    print(f"   Cluster centers shape: {clustering.cluster_centers_.shape}")
    print(f"   Inertia: {clustering.inertia_:.2f}")
    
    # 4. Meta-estimators
    print(f"\n4. Meta-estimators:")
    
    from sklearn.ensemble import VotingClassifier
    from sklearn.svm import SVC
    
    # Voting classifier - combines multiple estimators
    voting_clf = VotingClassifier([
        ('lr', LogisticRegression(random_state=42)),
        ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
        ('svc', SVC(probability=True, random_state=42))
    ], voting='soft')  # soft voting uses probabilities
    
    voting_clf.fit(X_scaled, y_multiclass)
    voting_pred = voting_clf.predict(X_scaled)
    
    print(f"   Voting classifier accuracy: {accuracy_score(y_multiclass, voting_pred):.4f}")
    print(f"   Individual estimators: {len(voting_clf.estimators_)}")

demonstrate_estimator_types()
```

---

### 🔄 Building ML Pipelines

#### Basic pipeline construction

```python
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import GridSearchCV, cross_val_score

def demonstrate_basic_pipelines():
    """Demonstracja podstawowej konstrukcji pipelines"""
    
    print("Basic Pipeline Construction:")
    print("=" * 40)
    
    # Generate dataset
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=10,
        n_redundant=5,
        n_clusters_per_class=2,
        random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Manual workflow (bez pipeline)
    print("1. Manual Workflow (without Pipeline):")
    
    # Step by step
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    selector = SelectKBest(score_func=f_classif, k=10)
    X_train_selected = selector.fit_transform(X_train_scaled, y_train)
    X_test_selected = selector.transform(X_test_scaled)
    
    classifier = LogisticRegression(random_state=42)
    classifier.fit(X_train_selected, y_train)
    
    manual_predictions = classifier.predict(X_test_selected)
    manual_accuracy = accuracy_score(y_test, manual_predictions)
    
    print(f"   Manual workflow accuracy: {manual_accuracy:.4f}")
    print(f"   Steps: Scale -> Select -> Classify")
    print(f"   Final feature count: {X_train_selected.shape[1]}")
    
    # 2. Pipeline workflow
    print(f"\n2. Pipeline Workflow:")
    
    # Create pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('selector', SelectKBest(score_func=f_classif, k=10)),
        ('classifier', LogisticRegression(random_state=42))
    ])
    
    # Fit entire pipeline
    pipeline.fit(X_train, y_train)
    
    # Predict
    pipeline_predictions = pipeline.predict(X_test)
    pipeline_accuracy = accuracy_score(y_test, pipeline_predictions)
    
    print(f"   Pipeline accuracy: {pipeline_accuracy:.4f}")
    print(f"   Pipeline steps: {[step for step, _ in pipeline.steps]}")
    print(f"   Results match manual: {manual_accuracy == pipeline_accuracy}")
    
    # 3. make_pipeline shorthand
    print(f"\n3. make_pipeline Shorthand:")
    
    auto_pipeline = make_pipeline(
        StandardScaler(),
        SelectKBest(score_func=f_classif, k=10),
        LogisticRegression(random_state=42)
    )
    
    auto_pipeline.fit(X_train, y_train)
    auto_predictions = auto_pipeline.predict(X_test)
    auto_accuracy = accuracy_score(y_test, auto_predictions)
    
    print(f"   Auto-pipeline accuracy: {auto_accuracy:.4f}")
    print(f"   Auto-generated step names: {[step for step, _ in auto_pipeline.steps]}")
    
    # 4. Pipeline introspection
    print(f"\n4. Pipeline Introspection:")
    
    # Access individual steps
    scaler_step = pipeline.named_steps['scaler']
    selector_step = pipeline.named_steps['selector']
    classifier_step = pipeline.named_steps['classifier']
    
    print(f"   Scaler mean: {scaler_step.mean_[:5]}")
    print(f"   Selected features: {selector_step.get_support().sum()}")
    print(f"   Classifier coefficients shape: {classifier_step.coef_.shape}")
    
    # Transform intermediate steps
    X_train_intermediate = pipeline[:-1].transform(X_train)  # All steps except last
    print(f"   Intermediate transformation shape: {X_train_intermediate.shape}")
    
    # 5. Pipeline with cross-validation
    print(f"\n5. Pipeline Cross-validation:")
    
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='accuracy')
    
    print(f"   CV scores: {cv_scores}")
    print(f"   CV mean ± std: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

demonstrate_basic_pipelines()
```

#### Advanced pipeline patterns

```python
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def demonstrate_advanced_pipelines():
    """Zaawansowane wzorce pipelines"""
    
    print("Advanced Pipeline Patterns:")
    print("=" * 40)
    
    # Create mixed-type dataset
    np.random.seed(42)
    n_samples = 1000
    
    df = pd.DataFrame({
        # Numeric features
        'age': np.random.randint(18, 80, n_samples),
        'income': np.random.exponential(50000, n_samples),
        'score': np.random.normal(100, 15, n_samples),
        
        # Categorical features
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_samples),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
        
        # Ordinal features
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples),
        
        # Target
        'target': np.random.choice([0, 1], n_samples)
    })
    
    # Introduce some missing values
    missing_mask = np.random.random((n_samples, 6)) < 0.05
    for i, col in enumerate(['age', 'income', 'score', 'category', 'region', 'education']):
        df.loc[missing_mask[:, i], col] = np.nan
    
    print(f"1. Dataset Overview:")
    print(f"   Shape: {df.shape}")
    print(f"   Missing values per column:")
    print(f"   {df.isnull().sum()}")
    
    # Separate features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. ColumnTransformer dla different feature types
    print(f"\n2. ColumnTransformer for Mixed Types:")
    
    # Define feature groups
    numeric_features = ['age', 'income', 'score']
    categorical_features = ['category', 'region']
    ordinal_features = ['education']
    
    # Create transformers dla each type
    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(drop='first', sparse_output=False))
    ])
    
    ordinal_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='High School')),
        ('ordinal', OrdinalEncoder(categories=[['High School', 'Bachelor', 'Master', 'PhD']]))
    ])
    
    # Combine transformers
    preprocessor = ColumnTransformer([
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features),
        ('ord', ordinal_transformer, ordinal_features)
    ])
    
    # Full pipeline
    full_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Fit and evaluate
    full_pipeline.fit(X_train, y_train)
    pipeline_predictions = full_pipeline.predict(X_test)
    pipeline_accuracy = accuracy_score(y_test, pipeline_predictions)
    
    print(f"   Full pipeline accuracy: {pipeline_accuracy:.4f}")
    
    # Inspect transformed features
    X_transformed = preprocessor.fit_transform(X_train)
    print(f"   Original features: {X_train.shape[1]}")
    print(f"   Transformed features: {X_transformed.shape[1]}")
    
    # 3. Pipeline z hyperparameter tuning
    print(f"\n3. Pipeline Hyperparameter Tuning:")
    
    # Define parameter grid
    param_grid = {
        'preprocessor__num__imputer__strategy': ['mean', 'median'],
        'classifier__n_estimators': [50, 100, 200],
        'classifier__max_depth': [None, 5, 10],
        'classifier__min_samples_split': [2, 5, 10]
    }
    
    # Grid search
    grid_search = GridSearchCV(
        full_pipeline, 
        param_grid, 
        cv=5, 
        scoring='accuracy',
        n_jobs=-1,
        verbose=0
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"   Best CV score: {grid_search.best_score_:.4f}")
    print(f"   Best parameters:")
    for param, value in grid_search.best_params_.items():
        print(f"     {param}: {value}")
    
    # Evaluate best model
    best_predictions = grid_search.predict(X_test)
    best_accuracy = accuracy_score(y_test, best_predictions)
    print(f"   Best model test accuracy: {best_accuracy:.4f}")
    
    # 4. Custom transformer w pipeline
    print(f"\n4. Custom Transformer in Pipeline:")
    
    class FeatureEngineer(BaseEstimator, TransformerMixin):
        """Custom feature engineering transformer"""
        
        def __init__(self, create_interactions=True):
            self.create_interactions = create_interactions
        
        def fit(self, X, y=None):
            return self
        
        def transform(self, X):
            X_transformed = X.copy()
            
            if self.create_interactions:
                # Create age-income interaction
                if 'age' in X_transformed.columns and 'income' in X_transformed.columns:
                    X_transformed['age_income_interaction'] = X_transformed['age'] * X_transformed['income']
                
                # Create income per age (experience factor)
                if 'age' in X_transformed.columns and 'income' in X_transformed.columns:
                    X_transformed['income_per_age'] = X_transformed['income'] / (X_transformed['age'] + 1)
            
            return X_transformed
    
    # Pipeline z custom transformer
    custom_pipeline = Pipeline([
        ('feature_engineer', FeatureEngineer(create_interactions=True)),
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    custom_pipeline.fit(X_train, y_train)
    custom_predictions = custom_pipeline.predict(X_test)
    custom_accuracy = accuracy_score(y_test, custom_predictions)
    
    print(f"   Custom pipeline accuracy: {custom_accuracy:.4f}")
    
    # Feature importance z custom features
    feature_names = (
        numeric_features + 
        list(custom_pipeline.named_steps['preprocessor']
             .named_transformers_['cat']
             .named_steps['onehot'].get_feature_names_out(categorical_features)) +
        ordinal_features +
        ['age_income_interaction', 'income_per_age']
    )
    
    feature_importance = custom_pipeline.named_steps['classifier'].feature_importances_
    print(f"   Number of final features: {len(feature_importance)}")
    
    # Top 5 most important features
    top_features_idx = np.argsort(feature_importance)[-5:]
    print(f"   Top 5 feature importances:")
    for idx in reversed(top_features_idx):
        if idx < len(feature_names):
            print(f"     {feature_names[idx]}: {feature_importance[idx]:.4f}")

demonstrate_advanced_pipelines()
```

---

### 🎛️ Model Selection i Validation

#### Cross-validation strategies

```python
from sklearn.model_selection import (
    cross_val_score, cross_validate, 
    StratifiedKFold, TimeSeriesSplit, 
    ShuffleSplit, LeaveOneOut
)
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score

def demonstrate_cross_validation():
    """Demonstracja różnych strategii cross-validation"""
    
    print("Cross-Validation Strategies:")
    print("=" * 40)
    
    # Generate datasets
    X_class, y_class = make_classification(
        n_samples=1000, n_features=20, n_informative=15, 
        n_redundant=3, n_clusters_per_class=2, random_state=42
    )
    
    # Time series data
    np.random.seed(42)
    n_time_samples = 200
    time_index = pd.date_range('2020-01-01', periods=n_time_samples, freq='D')
    X_time = np.random.randn(n_time_samples, 10)
    # Add trend i seasonality
    trend = np.linspace(0, 1, n_time_samples)
    seasonal = np.sin(2 * np.pi * np.arange(n_time_samples) / 30)
    y_time = trend + seasonal + np.random.randn(n_time_samples) * 0.1
    
    # Create pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(n_estimators=50, random_state=42))
    ])
    
    # 1. Basic K-Fold Cross-Validation
    print("1. K-Fold Cross-Validation:")
    
    cv_scores = cross_val_score(pipeline, X_class, y_class, cv=5, scoring='accuracy')
    
    print(f"   5-Fold CV scores: {cv_scores}")
    print(f"   Mean ± Std: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    # 2. Stratified K-Fold (maintains class balance)
    print(f"\n2. Stratified K-Fold:")
    
    stratified_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    stratified_scores = cross_val_score(
        pipeline, X_class, y_class, cv=stratified_cv, scoring='accuracy'
    )
    
    print(f"   Stratified CV scores: {stratified_scores}")
    print(f"   Mean ± Std: {stratified_scores.mean():.4f} ± {stratified_scores.std():.4f}")
    
    # Check class distribution w folds
    print("   Class distribution per fold:")
    for fold, (train_idx, val_idx) in enumerate(stratified_cv.split(X_class, y_class)):
        train_dist = np.bincount(y_class[train_idx])
        val_dist = np.bincount(y_class[val_idx])
        print(f"     Fold {fold+1}: Train {train_dist}, Val {val_dist}")
    
    # 3. Time Series Cross-Validation
    print(f"\n3. Time Series Cross-Validation:")
    
    from sklearn.ensemble import RandomForestRegressor
    ts_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor(n_estimators=50, random_state=42))
    ])
    
    # Time series split (no shuffling, maintains temporal order)
    ts_cv = TimeSeriesSplit(n_splits=5)
    ts_scores = cross_val_score(
        ts_pipeline, X_time, y_time, cv=ts_cv, scoring='neg_mean_squared_error'
    )
    
    print(f"   Time Series CV scores (neg MSE): {ts_scores}")
    print(f"   Mean ± Std: {ts_scores.mean():.4f} ± {ts_scores.std():.4f}")
    
    # Visualize time series splits
    print("   Time series split sizes:")
    for fold, (train_idx, val_idx) in enumerate(ts_cv.split(X_time)):
        print(f"     Fold {fold+1}: Train [{train_idx[0]}:{train_idx[-1]}], Val [{val_idx[0]}:{val_idx[-1]}]")
    
    # 4. Custom scoring i multiple metrics
    print(f"\n4. Multiple Metrics Cross-Validation:")
    
    # Define multiple scoring metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': make_scorer(precision_score, average='weighted'),
        'recall': make_scorer(recall_score, average='weighted'),
        'f1': make_scorer(f1_score, average='weighted')
    }
    
    cv_results = cross_validate(
        pipeline, X_class, y_class, 
        cv=5, scoring=scoring, return_train_score=True
    )
    
    print("   Cross-validation results:")
    for metric in ['accuracy', 'precision', 'recall', 'f1']:
        test_scores = cv_results[f'test_{metric}']
        train_scores = cv_results[f'train_{metric}']
        print(f"   {metric.capitalize()}:")
        print(f"     Test:  {test_scores.mean():.4f} ± {test_scores.std():.4f}")
        print(f"     Train: {train_scores.mean():.4f} ± {train_scores.std():.4f}")
    
    # 5. Monte Carlo Cross-Validation
    print(f"\n5. Monte Carlo Cross-Validation:")
    
    mc_cv = ShuffleSplit(n_splits=10, test_size=0.2, random_state=42)
    mc_scores = cross_val_score(pipeline, X_class, y_class, cv=mc_cv, scoring='accuracy')
    
    print(f"   Monte Carlo CV scores: {mc_scores}")
    print(f"   Mean ± Std: {mc_scores.mean():.4f} ± {mc_scores.std():.4f}")
    
    # 6. Leave-One-Out (dla small datasets)
    print(f"\n6. Leave-One-Out (small sample):")
    
    # Use small subset dla LOOCV demonstration
    X_small = X_class[:50]
    y_small = y_class[:50]
    
    loo_cv = LeaveOneOut()
    loo_scores = cross_val_score(pipeline, X_small, y_small, cv=loo_cv, scoring='accuracy')
    
    print(f"   LOOCV mean accuracy: {loo_scores.mean():.4f}")
    print(f"   LOOCV std: {loo_scores.std():.4f}")
    print(f"   Number of iterations: {len(loo_scores)}")

demonstrate_cross_validation()
```

#### Model comparison and selection

```python
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import validation_curve, learning_curve
import matplotlib.pyplot as plt

def demonstrate_model_selection():
    """Demonstracja model selection i comparison"""
    
    print("Model Selection and Comparison:")
    print("=" * 40)
    
    # Generate dataset
    X, y = make_classification(
        n_samples=2000, n_features=20, n_informative=15, 
        n_redundant=3, n_clusters_per_class=2, random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 1. Multiple model comparison
    print("1. Multiple Model Comparison:")
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'SVM': SVC(random_state=42),
        'Naive Bayes': GaussianNB(),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5)
    }
    
    model_results = {}
    
    for name, model in models.items():
        # Create pipeline z preprocessing
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', model)
        ])
        
        # Cross-validation
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='accuracy')
        
        # Fit and test
        pipeline.fit(X_train, y_train)
        test_score = pipeline.score(X_test, y_test)
        
        model_results[name] = {
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'test_score': test_score
        }
        
        print(f"   {name}:")
        print(f"     CV: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        print(f"     Test: {test_score:.4f}")
    
    # Find best model
    best_model = max(model_results.keys(), key=lambda k: model_results[k]['cv_mean'])
    print(f"\n   Best model by CV: {best_model}")
    
    # 2. Validation curves (hyperparameter tuning)
    print(f"\n2. Validation Curves:")
    
    # Example: Random Forest n_estimators
    param_range = [10, 30, 50, 100, 200, 500]
    
    train_scores, val_scores = validation_curve(
        RandomForestClassifier(random_state=42),
        X_train, y_train,
        param_name='n_estimators',
        param_range=param_range,
        cv=5, scoring='accuracy'
    )
    
    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)
    
    print("   Random Forest n_estimators validation:")
    for i, n_est in enumerate(param_range):
        print(f"     {n_est}: Train {train_mean[i]:.4f}±{train_std[i]:.4f}, "
              f"Val {val_mean[i]:.4f}±{val_std[i]:.4f}")
    
    # Find optimal parameter
    best_n_estimators = param_range[np.argmax(val_mean)]
    print(f"   Optimal n_estimators: {best_n_estimators}")
    
    # 3. Learning curves (bias-variance analysis)
    print(f"\n3. Learning Curves:")
    
    train_sizes = np.linspace(0.1, 1.0, 10)
    train_sizes_abs, train_scores_lc, val_scores_lc = learning_curve(
        RandomForestClassifier(n_estimators=100, random_state=42),
        X_train, y_train,
        train_sizes=train_sizes,
        cv=5, scoring='accuracy'
    )
    
    print("   Learning curve analysis:")
    for i, size in enumerate(train_sizes_abs):
        train_mean_lc = train_scores_lc[i].mean()
        val_mean_lc = val_scores_lc[i].mean()
        gap = train_mean_lc - val_mean_lc
        
        print(f"     Size {size:4d}: Train {train_mean_lc:.4f}, "
              f"Val {val_mean_lc:.4f}, Gap {gap:.4f}")
    
    # Analyze bias-variance
    final_train_score = train_scores_lc[-1].mean()
    final_val_score = val_scores_lc[-1].mean()
    
    if final_train_score - final_val_score > 0.05:
        print("   → Model shows signs of overfitting (high variance)")
    elif final_val_score < 0.8:  # Assuming 0.8 is desired performance
        print("   → Model shows signs of underfitting (high bias)")
    else:
        print("   → Model shows good bias-variance tradeoff")
    
    # 4. Statistical significance testing
    print(f"\n4. Statistical Significance Testing:")
    
    # Compare top 2 models
    sorted_models = sorted(model_results.items(), key=lambda x: x[1]['cv_mean'], reverse=True)
    model1_name, model1_results = sorted_models[0]
    model2_name, model2_results = sorted_models[1]
    
    # Detailed CV comparison
    model1 = Pipeline([
        ('scaler', StandardScaler()),
        ('model', models[model1_name])
    ])
    model2 = Pipeline([
        ('scaler', StandardScaler()),
        ('model', models[model2_name])
    ])
    
    cv_scores1 = cross_val_score(model1, X_train, y_train, cv=10, scoring='accuracy')
    cv_scores2 = cross_val_score(model2, X_train, y_train, cv=10, scoring='accuracy')
    
    # Paired t-test
    from scipy import stats
    t_stat, p_value = stats.ttest_rel(cv_scores1, cv_scores2)
    
    print(f"   Comparing {model1_name} vs {model2_name}:")
    print(f"   {model1_name}: {cv_scores1.mean():.4f} ± {cv_scores1.std():.4f}")
    print(f"   {model2_name}: {cv_scores2.mean():.4f} ± {cv_scores2.std():.4f}")
    print(f"   Paired t-test: t-stat = {t_stat:.4f}, p-value = {p_value:.4f}")
    
    if p_value < 0.05:
        print(f"   → {model1_name} is significantly better than {model2_name}")
    else:
        print(f"   → No significant difference between models")

demonstrate_model_selection()
```

---

### 🛠️ Custom Components

#### Creating custom transformers

```python
class OutlierRemover(BaseEstimator, TransformerMixin):
    """Custom transformer do usuwania outliers"""
    
    def __init__(self, method='iqr', factor=1.5):
        self.method = method
        self.factor = factor
        self.outlier_bounds_ = {}
    
    def fit(self, X, y=None):
        X_df = pd.DataFrame(X) if not isinstance(X, pd.DataFrame) else X
        
        for col in X_df.select_dtypes(include=[np.number]).columns:
            if self.method == 'iqr':
                Q1 = X_df[col].quantile(0.25)
                Q3 = X_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - self.factor * IQR
                upper_bound = Q3 + self.factor * IQR
            elif self.method == 'zscore':
                mean = X_df[col].mean()
                std = X_df[col].std()
                lower_bound = mean - self.factor * std
                upper_bound = mean + self.factor * std
            
            self.outlier_bounds_[col] = (lower_bound, upper_bound)
        
        return self
    
    def transform(self, X):
        X_df = pd.DataFrame(X) if not isinstance(X, pd.DataFrame) else X.copy()
        
        for col, (lower, upper) in self.outlier_bounds_.items():
            if col in X_df.columns:
                # Cap outliers instead of removing rows
                X_df[col] = X_df[col].clip(lower=lower, upper=upper)
        
        return X_df.values if not isinstance(X, pd.DataFrame) else X_df

class PolynomialInteractionFeatures(BaseEstimator, TransformerMixin):
    """Custom transformer tworzący polynomial i interaction features"""
    
    def __init__(self, degree=2, include_bias=False, interaction_only=False):
        self.degree = degree
        self.include_bias = include_bias
        self.interaction_only = interaction_only
        self.feature_names_in_ = None
        self.n_features_in_ = None
    
    def fit(self, X, y=None):
        self.n_features_in_ = X.shape[1]
        if hasattr(X, 'columns'):
            self.feature_names_in_ = X.columns.tolist()
        else:
            self.feature_names_in_ = [f'feature_{i}' for i in range(self.n_features_in_)]
        
        return self
    
    def transform(self, X):
        X_array = X.values if hasattr(X, 'values') else X
        
        # Start z original features
        features = [X_array]
        feature_names = self.feature_names_in_.copy()
        
        # Add polynomial features
        if not self.interaction_only:
            for d in range(2, self.degree + 1):
                poly_features = X_array ** d
                features.append(poly_features)
                feature_names.extend([f"{name}^{d}" for name in self.feature_names_in_])
        
        # Add interaction features
        for i in range(self.n_features_in_):
            for j in range(i + 1, self.n_features_in_):
                interaction = X_array[:, i] * X_array[:, j]
                features.append(interaction.reshape(-1, 1))
                feature_names.append(f"{self.feature_names_in_[i]} * {self.feature_names_in_[j]}")
        
        # Add bias term
        if self.include_bias:
            bias = np.ones((X_array.shape[0], 1))
            features.append(bias)
            feature_names.append('bias')
        
        result = np.hstack(features)
        return result

def demonstrate_custom_transformers():
    """Demonstracja custom transformers"""
    
    print("Custom Transformers:")
    print("=" * 25)
    
    # Create test data z outliers
    np.random.seed(42)
    n_samples = 1000
    
    # Normal data
    X_normal = np.random.randn(n_samples, 3)
    
    # Add outliers
    outlier_indices = np.random.choice(n_samples, size=50, replace=False)
    X_normal[outlier_indices, :] += np.random.choice([-1, 1], size=(50, 3)) * np.random.exponential(5, (50, 3))
    
    X_df = pd.DataFrame(X_normal, columns=['feature_1', 'feature_2', 'feature_3'])
    
    print("1. Outlier Removal Transformer:")
    
    # Before outlier removal
    print("   Before outlier removal:")
    for col in X_df.columns:
        print(f"     {col}: min={X_df[col].min():.2f}, max={X_df[col].max():.2f}, "
              f"mean={X_df[col].mean():.2f}, std={X_df[col].std():.2f}")
    
    # Apply outlier removal
    outlier_remover = OutlierRemover(method='iqr', factor=2.0)
    X_cleaned = outlier_remover.fit_transform(X_df)
    X_cleaned_df = pd.DataFrame(X_cleaned, columns=['feature_1', 'feature_2', 'feature_3'])
    
    print("\n   After outlier removal (IQR method):")
    for col in X_cleaned_df.columns:
        print(f"     {col}: min={X_cleaned_df[col].min():.2f}, max={X_cleaned_df[col].max():.2f}, "
              f"mean={X_cleaned_df[col].mean():.2f}, std={X_cleaned_df[col].std():.2f}")
    
    # 2. Polynomial interaction features
    print(f"\n2. Polynomial Interaction Features:")
    
    # Smaller dataset dla demo
    X_small = X_df.iloc[:100, :2]  # First 100 rows, 2 features
    
    print(f"   Original features: {X_small.shape}")
    
    poly_transformer = PolynomialInteractionFeatures(degree=2, include_bias=True, interaction_only=False)
    X_poly = poly_transformer.fit_transform(X_small)
    
    print(f"   After polynomial transformation: {X_poly.shape}")
    print("   Feature breakdown:")
    print(f"     Original features: {X_small.shape[1]}")
    print(f"     Squared features: {X_small.shape[1]}")
    print(f"     Interaction features: {X_small.shape[1] * (X_small.shape[1] - 1) // 2}")
    print(f"     Bias term: 1")
    print(f"     Total: {X_poly.shape[1]}")
    
    # 3. Custom transformer w pipeline
    print(f"\n3. Custom Transformers in Pipeline:")
    
    # Create target variable
    y = (X_df['feature_1'] + X_df['feature_2'] * X_df['feature_3'] + np.random.randn(len(X_df)) * 0.1) > 0
    
    # Pipeline z custom transformers
    custom_pipeline = Pipeline([
        ('outlier_removal', OutlierRemover(method='iqr', factor=1.5)),
        ('poly_features', PolynomialInteractionFeatures(degree=2, interaction_only=True)),
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(random_state=42, max_iter=1000))
    ])
    
    # Train and evaluate
    X_train, X_test, y_train, y_test = train_test_split(X_df, y, test_size=0.2, random_state=42)
    
    custom_pipeline.fit(X_train, y_train)
    custom_predictions = custom_pipeline.predict(X_test)
    custom_accuracy = accuracy_score(y_test, custom_predictions)
    
    print(f"   Custom pipeline accuracy: {custom_accuracy:.4f}")
    
    # Compare z simple pipeline
    simple_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(random_state=42, max_iter=1000))
    ])
    
    simple_pipeline.fit(X_train, y_train)
    simple_predictions = simple_pipeline.predict(X_test)
    simple_accuracy = accuracy_score(y_test, simple_predictions)
    
    print(f"   Simple pipeline accuracy: {simple_accuracy:.4f}")
    print(f"   Improvement: {custom_accuracy - simple_accuracy:.4f}")
    
    # Pipeline introspection
    print(f"\n   Pipeline introspection:")
    print(f"   Original features: {X_train.shape[1]}")
    
    # After outlier removal
    step1_output = custom_pipeline.named_steps['outlier_removal'].transform(X_train)
    print(f"   After outlier removal: {step1_output.shape}")
    
    # After polynomial features
    step2_output = custom_pipeline.named_steps['poly_features'].transform(step1_output)
    print(f"   After polynomial features: {step2_output.shape}")

demonstrate_custom_transformers()
```

---

### 💡 Production Tips

#### Pipeline serialization and deployment

```python
import joblib
import pickle
from sklearn.base import clone

def demonstrate_production_tips():
    """Production tips dla sklearn pipelines"""
    
    print("Production Tips:")
    print("=" * 20)
    
    # Create and train pipeline
    X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    production_pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('selector', SelectKBest(score_func=f_classif, k=5)),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    production_pipeline.fit(X_train, y_train)
    
    # 1. Model serialization
    print("1. Model Serialization:")
    
    # Using joblib (recommended dla sklearn)
    joblib_file = tempfile.NamedTemporaryFile(delete=False, suffix='.joblib')
    joblib.dump(production_pipeline, joblib_file.name)
    joblib_size = os.path.getsize(joblib_file.name) / 1024  # KB
    
    # Using pickle
    pickle_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pkl')
    with open(pickle_file.name, 'wb') as f:
        pickle.dump(production_pipeline, f)
    pickle_size = os.path.getsize(pickle_file.name) / 1024  # KB
    
    print(f"   Joblib file size: {joblib_size:.2f} KB")
    print(f"   Pickle file size: {pickle_size:.2f} KB")
    
    # Load and verify
    loaded_pipeline = joblib.load(joblib_file.name)
    loaded_predictions = loaded_pipeline.predict(X_test)
    original_predictions = production_pipeline.predict(X_test)
    
    print(f"   Predictions match: {np.array_equal(loaded_predictions, original_predictions)}")
    
    # 2. Model versioning
    print(f"\n2. Model Versioning:")
    
    class VersionedModel:
        def __init__(self, model, version, metadata=None):
            self.model = model
            self.version = version
            self.metadata = metadata or {}
            self.created_at = pd.Timestamp.now()
        
        def predict(self, X):
            return self.model.predict(X)
        
        def predict_proba(self, X):
            if hasattr(self.model, 'predict_proba'):
                return self.model.predict_proba(X)
            raise AttributeError("Model doesn't support probability predictions")
    
    # Create versioned model
    versioned_model = VersionedModel(
        model=production_pipeline,
        version="1.0.0",
        metadata={
            'algorithm': 'RandomForest',
            'n_features': X_train.shape[1],
            'training_samples': X_train.shape[0],
            'accuracy': accuracy_score(y_test, original_predictions)
        }
    )
    
    print(f"   Model version: {versioned_model.version}")
    print(f"   Created at: {versioned_model.created_at}")
    print(f"   Metadata: {versioned_model.metadata}")
    
    # 3. Model monitoring utilities
    print(f"\n3. Model Monitoring:")
    
    class ModelMonitor:
        def __init__(self, model, feature_names=None):
            self.model = model
            self.feature_names = feature_names or [f'feature_{i}' for i in range(X_train.shape[1])]
            self.prediction_log = []
        
        def predict_and_log(self, X):
            predictions = self.model.predict(X)
            probabilities = self.model.predict_proba(X) if hasattr(self.model, 'predict_proba') else None
            
            # Log predictions
            for i, (pred, prob) in enumerate(zip(predictions, probabilities or [None]*len(predictions))):
                log_entry = {
                    'timestamp': pd.Timestamp.now(),
                    'prediction': pred,
                    'probability': prob.max() if prob is not None else None,
                    'features': X[i] if X.ndim > 1 else [X[i]]
                }
                self.prediction_log.append(log_entry)
            
            return predictions
        
        def get_prediction_summary(self):
            if not self.prediction_log:
                return "No predictions logged"
            
            df_log = pd.DataFrame(self.prediction_log)
            
            summary = {
                'total_predictions': len(df_log),
                'prediction_distribution': df_log['prediction'].value_counts().to_dict(),
                'avg_confidence': df_log['probability'].mean() if df_log['probability'].notna().any() else None,
                'latest_prediction': df_log.iloc[-1]['timestamp']
            }
            
            return summary
        
        def detect_drift(self, X_reference, X_current, threshold=0.1):
            """Simple feature drift detection"""
            reference_means = np.mean(X_reference, axis=0)
            current_means = np.mean(X_current, axis=0)
            
            drift_scores = np.abs(reference_means - current_means) / (np.std(X_reference, axis=0) + 1e-8)
            
            drift_detected = drift_scores > threshold
            
            return {
                'drift_detected': drift_detected.any(),
                'drift_features': [self.feature_names[i] for i in np.where(drift_detected)[0]],
                'drift_scores': drift_scores
            }
    
    # Create monitor
    monitor = ModelMonitor(production_pipeline, feature_names=[f'feature_{i}' for i in range(10)])
    
    # Make monitored predictions
    monitored_predictions = monitor.predict_and_log(X_test[:10])
    
    print("   Prediction monitoring:")
    print(f"   Monitored predictions: {monitored_predictions}")
    print(f"   Summary: {monitor.get_prediction_summary()}")
    
    # Test drift detection
    X_drifted = X_test + np.random.normal(0, 0.5, X_test.shape)  # Simulate drift
    drift_results = monitor.detect_drift(X_train, X_drifted, threshold=0.2)
    
    print(f"\n   Drift detection:")
    print(f"   Drift detected: {drift_results['drift_detected']}")
    if drift_results['drift_detected']:
        print(f"   Drifted features: {drift_results['drift_features']}")
    
    # 4. Pipeline reproducibility
    print(f"\n4. Pipeline Reproducibility:")
    
    # Extract pipeline configuration
    pipeline_config = {
        'steps': [],
        'sklearn_version': '1.3.0',  # Should be actual version
        'random_seeds': []
    }
    
    for step_name, step_estimator in production_pipeline.steps:
        step_config = {
            'name': step_name,
            'class': step_estimator.__class__.__name__,
            'parameters': step_estimator.get_params()
        }
        pipeline_config['steps'].append(step_config)
    
    print("   Pipeline configuration:")
    for step in pipeline_config['steps']:
        print(f"     {step['name']}: {step['class']}")
        if 'random_state' in step['parameters']:
            print(f"       Random state: {step['parameters']['random_state']}")
    
    # Clone pipeline dla testing
    cloned_pipeline = clone(production_pipeline)
    print(f"   Pipeline cloned successfully: {type(cloned_pipeline) == type(production_pipeline)}")
    
    # Cleanup temp files
    try:
        os.unlink(joblib_file.name)
        os.unlink(pickle_file.name)
    except:
        pass

demonstrate_production_tips()
```

---

### 🔗 Powiązane tematy

- [[Classification Algorithms - Comprehensive Guide]] - Algorytmy klasyfikacji
- [[Regression Algorithms - Comprehensive Guide]] - Algorytmy regresji  
- [[Model Evaluation i Metrics]] - Ewaluacja modeli
- [[Machine Learning Pipeline - Preprocessing]] - Pipeline preprocessing