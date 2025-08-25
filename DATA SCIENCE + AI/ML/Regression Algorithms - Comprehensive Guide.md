## 📈 Regression Algorithms - Comprehensive Guide

_Kompletny przewodnik po algorytmach regresji w Machine Learning_

---

### 📝 Wprowadzenie do regresji

**Regression** to zadanie przewidywania wartości ciągłych (numerycznych):

1. **Linear regression** - modelowanie związków liniowych
2. **Polynomial regression** - związki nieliniowe przez wielomiany
3. **Regularized regression** - Ridge, Lasso, Elastic Net
4. **Tree-based regression** - Random Forest, Gradient Boosting
5. **Advanced methods** - SVR, KNN regression, Neural Networks

---

### 📏 Linear Regression Family

#### Simple and Multiple Linear Regression

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_regression, load_diabetes, fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def demonstrate_linear_regression():
    """Demonstracja Linear Regression"""
    
    print("Linear Regression:")
    print("=" * 25)
    
    # Generate synthetic dataset
    X, y = make_regression(
        n_samples=1000, n_features=10, n_informative=8, 
        noise=0.1, random_state=42
    )
    
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Simple Linear Regression (1 feature)
    print("1. Simple Linear Regression:")
    
    # Use most informative feature
    X_simple = X[:, 0].reshape(-1, 1)  # First feature
    X_train_simple, X_test_simple, y_train_simple, y_test_simple = train_test_split(
        X_simple, y, test_size=0.2, random_state=42
    )
    
    lr_simple = LinearRegression()
    lr_simple.fit(X_train_simple, y_train_simple)
    
    y_pred_simple = lr_simple.predict(X_test_simple)
    
    print(f"   R² Score: {r2_score(y_test_simple, y_pred_simple):.4f}")
    print(f"   MSE: {mean_squared_error(y_test_simple, y_pred_simple):.4f}")
    print(f"   MAE: {mean_absolute_error(y_test_simple, y_pred_simple):.4f}")
    print(f"   Coefficient: {lr_simple.coef_[0]:.4f}")
    print(f"   Intercept: {lr_simple.intercept_:.4f}")
    
    # 2. Multiple Linear Regression
    print(f"\n2. Multiple Linear Regression:")
    
    lr_multiple = LinearRegression()
    lr_multiple.fit(X_train, y_train)
    
    y_pred_multiple = lr_multiple.predict(X_test)
    
    print(f"   R² Score: {r2_score(y_test, y_pred_multiple):.4f}")
    print(f"   MSE: {mean_squared_error(y_test, y_pred_multiple):.4f}")
    print(f"   MAE: {mean_absolute_error(y_test, y_pred_multiple):.4f}")
    
    # Feature importance (coefficient magnitude)
    feature_importance = np.abs(lr_multiple.coef_)
    top_features = np.argsort(feature_importance)[-5:]
    
    print("   Top 5 features by coefficient magnitude:")
    for idx in reversed(top_features):
        print(f"     {feature_names[idx]}: {lr_multiple.coef_[idx]:.4f}")
    
    # 3. Regression assumptions checking
    print(f"\n3. Regression Assumptions:")
    
    residuals = y_test - y_pred_multiple
    
    # Linearity check (residuals vs fitted)
    fitted_values = y_pred_multiple
    
    print("   Assumption checks:")
    print(f"   Mean of residuals: {np.mean(residuals):.6f} (should be ~0)")
    print(f"   Std of residuals: {np.std(residuals):.4f}")
    
    # Homoscedasticity check (Breusch-Pagan test simplified)
    from scipy import stats
    
    # Test if residual variance is constant
    _, p_value = stats.pearsonr(np.abs(residuals), fitted_values)
    print(f"   Homoscedasticity p-value: {p_value:.4f} (>0.05 is good)")
    
    # Normality of residuals
    _, p_value_norm = stats.normaltest(residuals)
    print(f"   Residuals normality p-value: {p_value_norm:.4f} (>0.05 is good)")
    
    # 4. Confidence intervals for coefficients
    print(f"\n4. Coefficient Confidence Intervals:")
    
    # Calculate standard errors (simplified)
    from sklearn.metrics import mean_squared_error
    
    mse = mean_squared_error(y_train, lr_multiple.predict(X_train))
    var_beta = mse * np.linalg.inv(X_train.T @ X_train).diagonal()
    std_error = np.sqrt(var_beta)
    
    # 95% confidence intervals
    t_value = stats.t.ppf(0.975, df=len(X_train) - X_train.shape[1] - 1)
    
    print("   95% Confidence intervals for coefficients:")
    for i, (coef, se) in enumerate(zip(lr_multiple.coef_, std_error)):
        lower = coef - t_value * se
        upper = coef + t_value * se
        print(f"     {feature_names[i]}: {coef:.4f} [{lower:.4f}, {upper:.4f}]")

demonstrate_linear_regression()
```

#### Polynomial Regression

```python
def demonstrate_polynomial_regression():
    """Demonstracja Polynomial Regression"""
    
    print("Polynomial Regression:")
    print("=" * 25)
    
    # Generate non-linear data
    np.random.seed(42)
    X_nonlinear = np.random.uniform(-3, 3, 200).reshape(-1, 1)
    y_nonlinear = 0.5 * X_nonlinear.ravel()**3 - 2 * X_nonlinear.ravel()**2 + X_nonlinear.ravel() + np.random.normal(0, 2, 200)
    
    X_train_nl, X_test_nl, y_train_nl, y_test_nl = train_test_split(
        X_nonlinear, y_nonlinear, test_size=0.2, random_state=42
    )
    
    # 1. Compare different polynomial degrees
    print("1. Polynomial Degree Comparison:")
    
    degrees = [1, 2, 3, 4, 5, 8, 10]
    results = {}
    
    for degree in degrees:
        # Create polynomial features
        poly_reg = Pipeline([
            ('poly', PolynomialFeatures(degree=degree)),
            ('linear', LinearRegression())
        ])
        
        poly_reg.fit(X_train_nl, y_train_nl)
        y_pred_poly = poly_reg.predict(X_test_nl)
        
        # Calculate metrics
        r2 = r2_score(y_test_nl, y_pred_poly)
        mse = mean_squared_error(y_test_nl, y_pred_poly)
        
        # Cross-validation score
        cv_scores = cross_val_score(poly_reg, X_train_nl, y_train_nl, cv=5, scoring='r2')
        
        results[degree] = {
            'test_r2': r2,
            'test_mse': mse,
            'cv_r2_mean': cv_scores.mean(),
            'cv_r2_std': cv_scores.std()
        }
        
        print(f"   Degree {degree:2d}: R² = {r2:.4f}, MSE = {mse:.4f}, CV R² = {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    # Find optimal degree
    best_degree = max(results.keys(), key=lambda k: results[k]['cv_r2_mean'])
    print(f"\n   Best degree by CV: {best_degree}")
    
    # 2. Overfitting demonstration
    print(f"\n2. Overfitting Analysis:")
    
    high_degrees = [1, 5, 10, 15]
    
    for degree in high_degrees:
        poly_reg = Pipeline([
            ('poly', PolynomialFeatures(degree=degree)),
            ('linear', LinearRegression())
        ])
        
        poly_reg.fit(X_train_nl, y_train_nl)
        
        train_score = poly_reg.score(X_train_nl, y_train_nl)
        test_score = poly_reg.score(X_test_nl, y_test_nl)
        overfitting_gap = train_score - test_score
        
        print(f"   Degree {degree:2d}: Train R² = {train_score:.4f}, Test R² = {test_score:.4f}, Gap = {overfitting_gap:.4f}")
    
    # 3. Feature interaction analysis
    print(f"\n3. Feature Interactions (Multiple Features):")
    
    # Create multi-feature dataset
    X_multi, y_multi = make_regression(n_samples=500, n_features=3, noise=0.1, random_state=42)
    
    # Add interaction terms
    X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(
        X_multi, y_multi, test_size=0.2, random_state=42
    )
    
    interaction_options = [
        {'degree': 1, 'interaction_only': False},  # Linear only
        {'degree': 2, 'interaction_only': True},   # Interactions only
        {'degree': 2, 'interaction_only': False},  # Polynomial + interactions
    ]
    
    for i, options in enumerate(interaction_options):
        poly_multi = Pipeline([
            ('poly', PolynomialFeatures(**options)),
            ('linear', LinearRegression())
        ])
        
        poly_multi.fit(X_train_multi, y_train_multi)
        
        # Get feature names
        feature_names = poly_multi.named_steps['poly'].get_feature_names_out(
            input_features=[f'x{i}' for i in range(3)]
        )
        
        coefficients = poly_multi.named_steps['linear'].coef_
        
        test_score = poly_multi.score(X_test_multi, y_test_multi)
        
        option_name = "Linear" if options['degree'] == 1 else ("Interactions" if options['interaction_only'] else "Polynomial+Interactions")
        
        print(f"   {option_name}: R² = {test_score:.4f}, Features = {len(feature_names)}")
        
        # Show most important features
        if len(coefficients) <= 10:  # Only for manageable number of features
            feature_importance = np.abs(coefficients)
            top_features = np.argsort(feature_importance)[-5:]
            print(f"     Top features: {[feature_names[idx] for idx in reversed(top_features)]}")

demonstrate_polynomial_regression()
```

---

### 🎯 Regularized Regression

#### Ridge, Lasso, and Elastic Net

```python
from sklearn.linear_model import RidgeCV, LassoCV, ElasticNetCV

def demonstrate_regularized_regression():
    """Demonstracja regularized regression techniques"""
    
    print("Regularized Regression:")
    print("=" * 30)
    
    # Create dataset z multicollinearity
    np.random.seed(42)
    n_samples, n_features = 500, 50
    
    # Generate correlated features
    X_base = np.random.randn(n_samples, 10)
    
    # Add correlated features
    X_corr = np.column_stack([
        X_base,
        X_base[:, :5] + np.random.randn(n_samples, 5) * 0.1,  # Highly correlated
        X_base[:, 5:] * 2 + np.random.randn(n_samples, 5) * 0.2,  # Scaled versions
        np.random.randn(n_samples, 30)  # Random noise features
    ])
    
    # True relationship (only first 10 features matter)
    true_coef = np.zeros(X_corr.shape[1])
    true_coef[:10] = np.random.randn(10) * 2
    
    y = X_corr @ true_coef + np.random.randn(n_samples) * 0.5
    
    X_train, X_test, y_train, y_test = train_test_split(X_corr, y, test_size=0.2, random_state=42)
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 1. Regular Linear Regression baseline
    print("1. Regular Linear Regression (Baseline):")
    
    lr_regular = LinearRegression()
    lr_regular.fit(X_train_scaled, y_train)
    
    lr_pred = lr_regular.predict(X_test_scaled)
    lr_r2 = r2_score(y_test, lr_pred)
    lr_mse = mean_squared_error(y_test, lr_pred)
    
    print(f"   R² Score: {lr_r2:.4f}")
    print(f"   MSE: {lr_mse:.4f}")
    print(f"   Non-zero coefficients: {np.sum(np.abs(lr_regular.coef_) > 0.01)}/{len(lr_regular.coef_)}")
    
    # 2. Ridge Regression (L2 regularization)
    print(f"\n2. Ridge Regression (L2 Regularization):")
    
    # Cross-validation dla optimal alpha
    ridge_cv = RidgeCV(alphas=np.logspace(-3, 3, 20), cv=5)
    ridge_cv.fit(X_train_scaled, y_train)
    
    ridge_pred = ridge_cv.predict(X_test_scaled)
    ridge_r2 = r2_score(y_test, ridge_pred)
    ridge_mse = mean_squared_error(y_test, ridge_pred)
    
    print(f"   Best alpha: {ridge_cv.alpha_:.4f}")
    print(f"   R² Score: {ridge_r2:.4f}")
    print(f"   MSE: {ridge_mse:.4f}")
    print(f"   Non-zero coefficients: {np.sum(np.abs(ridge_cv.coef_) > 0.01)}/{len(ridge_cv.coef_)}")
    
    # 3. Lasso Regression (L1 regularization)
    print(f"\n3. Lasso Regression (L1 Regularization):")
    
    lasso_cv = LassoCV(alphas=np.logspace(-3, 1, 20), cv=5, random_state=42)
    lasso_cv.fit(X_train_scaled, y_train)
    
    lasso_pred = lasso_cv.predict(X_test_scaled)
    lasso_r2 = r2_score(y_test, lasso_pred)
    lasso_mse = mean_squared_error(y_test, lasso_pred)
    
    print(f"   Best alpha: {lasso_cv.alpha_:.4f}")
    print(f"   R² Score: {lasso_r2:.4f}")
    print(f"   MSE: {lasso_mse:.4f}")
    print(f"   Non-zero coefficients: {np.sum(np.abs(lasso_cv.coef_) > 0.01)}/{len(lasso_cv.coef_)}")
    print(f"   Selected features: {np.sum(lasso_cv.coef_ != 0)}")
    
    # Show selected features
    selected_features = np.where(lasso_cv.coef_ != 0)[0]
    print(f"   Selected feature indices: {selected_features[:10]}...")  # Show first 10
    
    # 4. Elastic Net (L1 + L2 regularization)
    print(f"\n4. Elastic Net (L1 + L2 Regularization):")
    
    elastic_cv = ElasticNetCV(
        alphas=np.logspace(-3, 1, 20), 
        l1_ratio=[0.1, 0.3, 0.5, 0.7, 0.9],
        cv=5, random_state=42
    )
    elastic_cv.fit(X_train_scaled, y_train)
    
    elastic_pred = elastic_cv.predict(X_test_scaled)
    elastic_r2 = r2_score(y_test, elastic_pred)
    elastic_mse = mean_squared_error(y_test, elastic_pred)
    
    print(f"   Best alpha: {elastic_cv.alpha_:.4f}")
    print(f"   Best l1_ratio: {elastic_cv.l1_ratio_:.2f}")
    print(f"   R² Score: {elastic_r2:.4f}")
    print(f"   MSE: {elastic_mse:.4f}")
    print(f"   Non-zero coefficients: {np.sum(np.abs(elastic_cv.coef_) > 0.01)}/{len(elastic_cv.coef_)}")
    
    # 5. Regularization path analysis
    print(f"\n5. Regularization Path Analysis:")
    
    # Ridge path
    alphas = np.logspace(-3, 3, 50)
    ridge_coefs = []
    
    for alpha in alphas:
        ridge = Ridge(alpha=alpha)
        ridge.fit(X_train_scaled, y_train)
        ridge_coefs.append(ridge.coef_)
    
    ridge_coefs = np.array(ridge_coefs)
    
    # Lasso path
    from sklearn.linear_model import lasso_path
    lasso_alphas, lasso_coefs, _ = lasso_path(X_train_scaled, y_train, alphas=alphas)
    
    print("   Regularization path computed")
    print(f"   Ridge: coefficients shrink gradually")
    print(f"   Lasso: coefficients become exactly zero")
    
    # Compare coefficient stability
    ridge_std = np.std(ridge_coefs, axis=0)
    lasso_std = np.std(lasso_coefs.T, axis=0)
    
    print(f"   Average coefficient std - Ridge: {np.mean(ridge_std):.4f}")
    print(f"   Average coefficient std - Lasso: {np.mean(lasso_std):.4f}")
    
    # 6. Model comparison summary
    print(f"\n6. Model Comparison Summary:")
    
    models = {
        'Linear Regression': {'r2': lr_r2, 'mse': lr_mse, 'n_features': len(lr_regular.coef_)},
        'Ridge': {'r2': ridge_r2, 'mse': ridge_mse, 'n_features': np.sum(np.abs(ridge_cv.coef_) > 0.01)},
        'Lasso': {'r2': lasso_r2, 'mse': lasso_mse, 'n_features': np.sum(lasso_cv.coef_ != 0)},
        'Elastic Net': {'r2': elastic_r2, 'mse': elastic_mse, 'n_features': np.sum(np.abs(elastic_cv.coef_) > 0.01)}
    }
    
    print(f"   {'Model':<15} {'R²':<8} {'MSE':<8} {'Features':<10}")
    print("   " + "-" * 45)
    
    for model_name, metrics in models.items():
        print(f"   {model_name:<15} {metrics['r2']:<8.4f} {metrics['mse']:<8.4f} {metrics['n_features']:<10d}")
    
    # Best model
    best_model = max(models.keys(), key=lambda k: models[k]['r2'])
    print(f"\n   Best model by R²: {best_model}")

demonstrate_regularized_regression()
```

---

### 🌳 Tree-Based Regression

#### Decision Tree and Random Forest Regression

```python
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.inspection import permutation_importance

def demonstrate_tree_regression():
    """Demonstracja tree-based regression"""
    
    print("Tree-Based Regression:")
    print("=" * 28)
    
    # Use California housing dataset
    california = fetch_california_housing()
    X, y = california.data, california.target
    feature_names = california.feature_names
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Decision Tree Regression
    print("1. Decision Tree Regression:")
    
    # Basic decision tree
    dt_basic = DecisionTreeRegressor(random_state=42)
    dt_basic.fit(X_train, y_train)
    
    dt_pred = dt_basic.predict(X_test)
    dt_r2 = r2_score(y_test, dt_pred)
    dt_mse = mean_squared_error(y_test, dt_pred)
    
    print(f"   R² Score: {dt_r2:.4f}")
    print(f"   MSE: {dt_mse:.4f}")
    print(f"   Tree depth: {dt_basic.get_depth()}")
    print(f"   Number of leaves: {dt_basic.get_n_leaves()}")
    
    # Feature importance
    dt_importance = dt_basic.feature_importances_
    top_dt_features = np.argsort(dt_importance)[-5:]
    
    print("   Top 5 important features:")
    for idx in reversed(top_dt_features):
        print(f"     {feature_names[idx]}: {dt_importance[idx]:.4f}")
    
    # 2. Pruned Decision Tree
    print(f"\n2. Pruned Decision Tree:")
    
    # Grid search dla optimal parameters
    dt_param_grid = {
        'max_depth': [5, 10, 15, None],
        'min_samples_split': [2, 10, 20],
        'min_samples_leaf': [1, 5, 10]
    }
    
    dt_grid = GridSearchCV(
        DecisionTreeRegressor(random_state=42),
        dt_param_grid, cv=5, scoring='r2', n_jobs=-1
    )
    
    dt_grid.fit(X_train, y_train)
    
    dt_best = dt_grid.best_estimator_
    dt_best_pred = dt_best.predict(X_test)
    dt_best_r2 = r2_score(y_test, dt_best_pred)
    dt_best_mse = mean_squared_error(y_test, dt_best_pred)
    
    print(f"   Best parameters: {dt_grid.best_params_}")
    print(f"   R² Score: {dt_best_r2:.4f}")
    print(f"   MSE: {dt_best_mse:.4f}")
    print(f"   Tree depth: {dt_best.get_depth()}")
    print(f"   Improvement over basic: {dt_best_r2 - dt_r2:.4f}")
    
    # 3. Random Forest Regression
    print(f"\n3. Random Forest Regression:")
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    
    rf_pred = rf.predict(X_test)
    rf_r2 = r2_score(y_test, rf_pred)
    rf_mse = mean_squared_error(y_test, rf_pred)
    
    print(f"   R² Score: {rf_r2:.4f}")
    print(f"   MSE: {rf_mse:.4f}")
    print(f"   Number of trees: {rf.n_estimators}")
    
    # Feature importance comparison
    rf_importance = rf.feature_importances_
    
    print("\n   Feature Importance Comparison (RF vs DT):")
    print(f"   {'Feature':<20} {'RF Importance':<15} {'DT Importance':<15}")
    print("   " + "-" * 50)
    
    for i, feature in enumerate(feature_names):
        print(f"   {feature:<20} {rf_importance[i]:<15.4f} {dt_importance[i]:<15.4f}")
    
    # 4. Gradient Boosting Regression
    print(f"\n4. Gradient Boosting Regression:")
    
    gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb.fit(X_train, y_train)
    
    gb_pred = gb.predict(X_test)
    gb_r2 = r2_score(y_test, gb_pred)
    gb_mse = mean_squared_error(y_test, gb_pred)
    
    print(f"   R² Score: {gb_r2:.4f}")
    print(f"   MSE: {gb_mse:.4f}")
    print(f"   Learning rate: {gb.learning_rate}")
    
    # Training progress
    test_scores = np.zeros(gb.n_estimators)
    for i, pred in enumerate(gb.staged_predict(X_test)):
        test_scores[i] = r2_score(y_test, pred)
    
    print(f"   Initial R² (1 tree): {test_scores[0]:.4f}")
    print(f"   Final R² ({gb.n_estimators} trees): {test_scores[-1]:.4f}")
    print(f"   Best iteration: {np.argmax(test_scores) + 1}")
    
    # 5. Hyperparameter tuning comparison
    print(f"\n5. Hyperparameter Tuning:")
    
    # Random Forest tuning
    rf_param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5]
    }
    
    rf_grid = GridSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=-1),
        rf_param_grid, cv=3, scoring='r2', n_jobs=-1
    )
    
    rf_grid.fit(X_train, y_train)
    
    rf_best_pred = rf_grid.predict(X_test)
    rf_best_r2 = r2_score(y_test, rf_best_pred)
    
    print(f"   Best RF parameters: {rf_grid.best_params_}")
    print(f"   Best RF R²: {rf_best_r2:.4f}")
    
    # Gradient Boosting tuning
    gb_param_grid = {
        'n_estimators': [100, 200],
        'learning_rate': [0.05, 0.1, 0.2],
        'max_depth': [3, 5]
    }
    
    gb_grid = GridSearchCV(
        GradientBoostingRegressor(random_state=42),
        gb_param_grid, cv=3, scoring='r2', n_jobs=-1
    )
    
    gb_grid.fit(X_train, y_train)
    
    gb_best_pred = gb_grid.predict(X_test)
    gb_best_r2 = r2_score(y_test, gb_best_pred)
    
    print(f"   Best GB parameters: {gb_grid.best_params_}")
    print(f"   Best GB R²: {gb_best_r2:.4f}")
    
    # 6. Model comparison summary
    print(f"\n6. Tree-Based Model Summary:")
    
    models_results = {
        'Decision Tree (Basic)': dt_r2,
        'Decision Tree (Tuned)': dt_best_r2,
        'Random Forest (Basic)': rf_r2,
        'Random Forest (Tuned)': rf_best_r2,
        'Gradient Boosting (Basic)': gb_r2,
        'Gradient Boosting (Tuned)': gb_best_r2
    }
    
    print(f"   {'Model':<25} {'R² Score':<10}")
    print("   " + "-" * 35)
    
    for model_name, r2_score_val in models_results.items():
        print(f"   {model_name:<25} {r2_score_val:<10.4f}")
    
    best_tree_model = max(models_results.keys(), key=lambda k: models_results[k])
    print(f"\n   Best tree-based model: {best_tree_model}")

demonstrate_tree_regression()
```

---

### 🎯 Advanced Regression Methods

#### Support Vector Regression and KNN Regression

```python
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

def demonstrate_advanced_regression():
    """Demonstracja advanced regression methods"""
    
    print("Advanced Regression Methods:")
    print("=" * 35)
    
    # Generate complex dataset
    np.random.seed(42)
    X_complex = np.random.uniform(-3, 3, 400).reshape(-1, 1)
    y_complex = np.sin(X_complex.ravel()) + 0.5 * X_complex.ravel() + np.random.normal(0, 0.2, 400)
    
    X_train_adv, X_test_adv, y_train_adv, y_test_adv = train_test_split(
        X_complex, y_complex, test_size=0.2, random_state=42
    )
    
    # Scaling
    scaler = StandardScaler()
    X_train_adv_scaled = scaler.fit_transform(X_train_adv)
    X_test_adv_scaled = scaler.transform(X_test_adv)
    
    # 1. Support Vector Regression
    print("1. Support Vector Regression:")
    
    # Different kernels
    svr_kernels = ['linear', 'poly', 'rbf', 'sigmoid']
    svr_results = {}
    
    for kernel in svr_kernels:
        if kernel == 'poly':
            svr = SVR(kernel=kernel, degree=3, C=1.0)
        else:
            svr = SVR(kernel=kernel, C=1.0)
        
        svr.fit(X_train_adv_scaled, y_train_adv)
        svr_pred = svr.predict(X_test_adv_scaled)
        
        svr_r2 = r2_score(y_test_adv, svr_pred)
        svr_mse = mean_squared_error(y_test_adv, svr_pred)
        
        svr_results[kernel] = {'r2': svr_r2, 'mse': svr_mse, 'n_support': len(svr.support_)}
        
        print(f"   {kernel.upper():>8} kernel: R² = {svr_r2:.4f}, MSE = {svr_mse:.4f}, Support vectors = {len(svr.support_)}")
    
    best_svr_kernel = max(svr_results.keys(), key=lambda k: svr_results[k]['r2'])
    print(f"   Best SVR kernel: {best_svr_kernel}")
    
    # 2. SVR Hyperparameter tuning
    print(f"\n2. SVR Hyperparameter Tuning (RBF kernel):")
    
    svr_param_grid = {
        'C': [0.1, 1, 10, 100],
        'gamma': ['scale', 'auto', 0.01, 0.1, 1],
        'epsilon': [0.01, 0.1, 0.2]
    }
    
    svr_grid = GridSearchCV(
        SVR(kernel='rbf'),
        svr_param_grid, cv=5, scoring='r2', n_jobs=-1
    )
    
    svr_grid.fit(X_train_adv_scaled, y_train_adv)
    
    svr_best_pred = svr_grid.predict(X_test_adv_scaled)
    svr_best_r2 = r2_score(y_test_adv, svr_best_pred)
    
    print(f"   Best parameters: {svr_grid.best_params_}")
    print(f"   Best SVR R²: {svr_best_r2:.4f}")
    print(f"   Improvement: {svr_best_r2 - svr_results['rbf']['r2']:.4f}")
    
    # 3. k-Nearest Neighbors Regression
    print(f"\n3. k-Nearest Neighbors Regression:")
    
    # Different k values
    k_values = [1, 3, 5, 7, 11, 15, 21]
    knn_results = {}
    
    for k in k_values:
        knn = KNeighborsRegressor(n_neighbors=k)
        knn.fit(X_train_adv_scaled, y_train_adv)
        
        knn_pred = knn.predict(X_test_adv_scaled)
        knn_r2 = r2_score(y_test_adv, knn_pred)
        knn_mse = mean_squared_error(y_test_adv, knn_pred)
        
        knn_results[k] = {'r2': knn_r2, 'mse': knn_mse}
        
        print(f"   k = {k:2d}: R² = {knn_r2:.4f}, MSE = {knn_mse:.4f}")
    
    best_k = max(knn_results.keys(), key=lambda k: knn_results[k]['r2'])
    print(f"   Best k: {best_k}")
    
    # 4. KNN distance metrics and weights
    print(f"\n4. KNN Distance Metrics and Weights:")
    
    distance_metrics = ['euclidean', 'manhattan', 'chebyshev']
    weights = ['uniform', 'distance']
    
    knn_advanced_results = {}
    
    for metric in distance_metrics:
        for weight in weights:
            knn_adv = KNeighborsRegressor(
                n_neighbors=best_k, metric=metric, weights=weight
            )
            knn_adv.fit(X_train_adv_scaled, y_train_adv)
            
            knn_adv_pred = knn_adv.predict(X_test_adv_scaled)
            knn_adv_r2 = r2_score(y_test_adv, knn_adv_pred)
            
            config = f"{metric}_{weight}"
            knn_advanced_results[config] = knn_adv_r2
            
            print(f"   {metric:>12} + {weight:>8}: R² = {knn_adv_r2:.4f}")
    
    best_knn_config = max(knn_advanced_results.keys(), key=lambda k: knn_advanced_results[k])
    print(f"   Best KNN config: {best_knn_config}")
    
    # 5. Ensemble of advanced methods
    print(f"\n5. Ensemble of Advanced Methods:")
    
    # Train best models
    svr_final = SVR(kernel='rbf', **svr_grid.best_params_)
    svr_final.fit(X_train_adv_scaled, y_train_adv)
    
    metric, weight = best_knn_config.split('_')
    knn_final = KNeighborsRegressor(
        n_neighbors=best_k, metric=metric, weights=weight
    )
    knn_final.fit(X_train_adv_scaled, y_train_adv)
    
    # Also include a tree-based model
    rf_final = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_final.fit(X_train_adv, y_train_adv)  # RF doesn't need scaling
    
    # Individual predictions
    svr_pred_final = svr_final.predict(X_test_adv_scaled)
    knn_pred_final = knn_final.predict(X_test_adv_scaled)
    rf_pred_final = rf_final.predict(X_test_adv)
    
    # Ensemble predictions (simple averaging)
    ensemble_pred = (svr_pred_final + knn_pred_final + rf_pred_final) / 3
    
    # Results
    svr_final_r2 = r2_score(y_test_adv, svr_pred_final)
    knn_final_r2 = r2_score(y_test_adv, knn_pred_final)
    rf_final_r2 = r2_score(y_test_adv, rf_pred_final)
    ensemble_r2 = r2_score(y_test_adv, ensemble_pred)
    
    print(f"   SVR R²: {svr_final_r2:.4f}")
    print(f"   KNN R²: {knn_final_r2:.4f}")
    print(f"   RF R²: {rf_final_r2:.4f}")
    print(f"   Ensemble R²: {ensemble_r2:.4f}")
    
    best_individual = max([svr_final_r2, knn_final_r2, rf_final_r2])
    ensemble_improvement = ensemble_r2 - best_individual
    
    print(f"   Ensemble improvement: {ensemble_improvement:.4f}")

demonstrate_advanced_regression()
```

---

### 📊 Model Evaluation i Diagnostics

#### Comprehensive regression evaluation

```python
from scipy import stats
import matplotlib.pyplot as plt

def comprehensive_regression_evaluation():
    """Komprehensywna ewaluacja modeli regresji"""
    
    print("Comprehensive Regression Evaluation:")
    print("=" * 45)
    
    # Use California housing dataset dla realistic evaluation
    california = fetch_california_housing()
    X, y = california.data, california.target
    feature_names = california.feature_names
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train multiple models
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge': Ridge(alpha=1.0),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'SVR': SVR(kernel='rbf', C=1.0)
    }
    
    model_results = {}
    
    # 1. Train and evaluate models
    print("1. Model Performance Metrics:")
    
    for name, model in models.items():
        # Use scaled data dla models that need it
        if name in ['Linear Regression', 'Ridge', 'SVR']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_train_pred = model.predict(X_train_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_train_pred = model.predict(X_train)
        
        # Calculate comprehensive metrics
        metrics = {
            'r2_test': r2_score(y_test, y_pred),
            'r2_train': r2_score(y_train, y_train_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'mape': np.mean(np.abs((y_test - y_pred) / y_test)) * 100,
            'predictions': y_pred
        }
        
        # Additional metrics
        residuals = y_test - y_pred
        metrics['residual_std'] = np.std(residuals)
        metrics['max_error'] = np.max(np.abs(residuals))
        
        model_results[name] = metrics
        
        print(f"\n   {name}:")
        print(f"     R² (test): {metrics['r2_test']:.4f}")
        print(f"     R² (train): {metrics['r2_train']:.4f}")
        print(f"     Overfitting gap: {metrics['r2_train'] - metrics['r2_test']:.4f}")
        print(f"     RMSE: {metrics['rmse']:.4f}")
        print(f"     MAE: {metrics['mae']:.4f}")
        print(f"     MAPE: {metrics['mape']:.2f}%")
    
    # 2. Residual analysis
    print(f"\n2. Residual Analysis:")
    
    for name, results in model_results.items():
        predictions = results['predictions']
        residuals = y_test - predictions
        
        # Normality test
        _, p_value_norm = stats.normaltest(residuals)
        
        # Homoscedasticity test (simplified)
        _, p_value_homo = stats.pearsonr(np.abs(residuals), predictions)
        
        # Durbin-Watson test dla independence (simplified)
        residuals_sorted = residuals[np.argsort(predictions)]
        dw_stat = np.sum(np.diff(residuals_sorted)**2) / np.sum(residuals_sorted**2)
        
        print(f"\n   {name}:")
        print(f"     Residuals normality p-value: {p_value_norm:.4f}")
        print(f"     Homoscedasticity p-value: {abs(p_value_homo):.4f}")
        print(f"     Durbin-Watson statistic: {dw_stat:.4f}")
        
        # Interpretation
        if p_value_norm > 0.05:
            print(f"     ✓ Residuals appear normally distributed")
        else:
            print(f"     ⚠ Residuals may not be normally distributed")
        
        if abs(p_value_homo) > 0.05:
            print(f"     ✓ Residuals appear homoscedastic")
        else:
            print(f"     ⚠ Potential heteroscedasticity detected")
    
    # 3. Cross-validation analysis
    print(f"\n3. Cross-Validation Analysis:")
    
    cv_results = {}
    
    for name, model in models.items():
        if name in ['Linear Regression', 'Ridge', 'SVR']:
            pipeline = Pipeline([('scaler', StandardScaler()), ('model', model)])
            cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='r2')
        else:
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        
        cv_results[name] = cv_scores
        
        print(f"   {name}:")
        print(f"     CV R² mean: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        print(f"     CV Range: [{cv_scores.min():.4f}, {cv_scores.max():.4f}]")
    
    # 4. Learning curves
    print(f"\n4. Learning Curve Analysis:")
    
    from sklearn.model_selection import learning_curve
    
    for name, model in models.items():
        if name in ['Random Forest']:  # Focus on one model dla demo
            train_sizes = np.linspace(0.1, 1.0, 10)
            
            train_sizes_abs, train_scores, val_scores = learning_curve(
                model, X_train, y_train, train_sizes=train_sizes, cv=3, scoring='r2'
            )
            
            train_mean = train_scores.mean(axis=1)
            train_std = train_scores.std(axis=1)
            val_mean = val_scores.mean(axis=1)
            val_std = val_scores.std(axis=1)
            
            print(f"   {name} Learning Curve:")
            print(f"     Final train score: {train_mean[-1]:.4f} ± {train_std[-1]:.4f}")
            print(f"     Final validation score: {val_mean[-1]:.4f} ± {val_std[-1]:.4f}")
            print(f"     Learning gap: {train_mean[-1] - val_mean[-1]:.4f}")
    
    # 5. Feature importance analysis (dla applicable models)
    print(f"\n5. Feature Importance Analysis:")
    
    for name, model in models.items():
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            top_features = np.argsort(importance)[-5:]
            
            print(f"   {name} - Top 5 features:")
            for idx in reversed(top_features):
                print(f"     {feature_names[idx]}: {importance[idx]:.4f}")
        
        elif hasattr(model, 'coef_'):
            # Dla linear models, use coefficient magnitude
            coef_magnitude = np.abs(model.coef_)
            top_features = np.argsort(coef_magnitude)[-5:]
            
            print(f"   {name} - Top 5 features (by |coefficient|):")
            for idx in reversed(top_features):
                print(f"     {feature_names[idx]}: {model.coef_[idx]:.4f}")
    
    # 6. Prediction intervals (dla applicable models)
    print(f"\n6. Prediction Confidence:")
    
    # For linear models, calculate prediction intervals
    for name, model in models.items():
        if name in ['Linear Regression', 'Ridge']:
            predictions = model_results[name]['predictions']
            residuals = y_test - predictions
            mse = mean_squared_error(y_test, predictions)
            
            # Simplified prediction intervals
            prediction_std = np.sqrt(mse)
            lower_bound = predictions - 1.96 * prediction_std
            upper_bound = predictions + 1.96 * prediction_std
            
            # Coverage calculation
            coverage = np.mean((y_test >= lower_bound) & (y_test <= upper_bound))
            
            print(f"   {name}:")
            print(f"     95% prediction interval coverage: {coverage:.2%}")
            print(f"     Average interval width: {np.mean(upper_bound - lower_bound):.4f}")
    
    # 7. Model ranking
    print(f"\n7. Model Ranking:")
    
    # Rank by different metrics
    metrics_to_rank = ['r2_test', 'rmse', 'mae']
    
    for metric in metrics_to_rank:
        print(f"\n   Ranking by {metric}:")
        
        if metric == 'r2_test':
            # Higher is better dla R²
            sorted_models = sorted(model_results.items(), key=lambda x: x[1][metric], reverse=True)
        else:
            # Lower is better dla error metrics
            sorted_models = sorted(model_results.items(), key=lambda x: x[1][metric])
        
        for i, (model_name, results) in enumerate(sorted_models, 1):
            print(f"     {i}. {model_name}: {results[metric]:.4f}")

comprehensive_regression_evaluation()
```

---

### 💡 Best Practices Summary

#### Regression best practices

```python
def regression_best_practices():
    """Best practices dla regression problems"""
    
    best_practices = """
    ✅ DATA PREPARATION:
    - Check dla outliers i handle appropriately
    - Examine feature distributions i transform if needed
    - Handle missing values properly
    - Check dla multicollinearity (VIF > 10)
    - Scale features dla regularized i distance-based methods
    
    ✅ MODEL SELECTION:
    - Linear Regression: Start here, interpretable baseline
    - Ridge: When multicollinearity exists
    - Lasso: When feature selection is needed
    - Elastic Net: Combines Ridge + Lasso benefits
    - Random Forest: Robust, handles non-linearity, less interpretable
    - Gradient Boosting: Often best performance, requires tuning
    - SVR: Good dla non-linear patterns, expensive dla large data
    
    ✅ EVALUATION METRICS:
    - R²: Proportion of variance explained (0-1, higher better)
    - MSE/RMSE: Penalizes large errors more (lower better)
    - MAE: Robust to outliers (lower better)  
    - MAPE: Percentage error, easy to interpret
    - Consider business context (cost of prediction errors)
    
    ✅ VALIDATION TECHNIQUES:
    - Train/validation/test splits
    - Cross-validation dla robust evaluation
    - Time series: temporal splits, no shuffling
    - Learning curves to detect over/underfitting
    
    ✅ DIAGNOSTICS:
    - Residual plots (vs fitted values)
    - QQ plots dla normality
    - Leverage i influence points
    - Cook's distance dla outliers
    - Durbin-Watson dla independence
    
    ✅ HYPERPARAMETER TUNING:
    - Grid search dla systematic exploration
    - Random search dla high-dimensional spaces
    - Bayesian optimization dla expensive models
    - Early stopping dla iterative algorithms
    
    ✅ COMMON PITFALLS:
    - Extrapolation beyond training data range
    - Ignoring residual patterns
    - Over-interpreting R² (can be misleading)
    - Not checking assumptions
    - Data leakage (future information in features)
    - Not handling categorical variables properly
    """
    
    print("Regression Best Practices:")
    print("=" * 35)
    print(best_practices)

regression_best_practices()

# Comprehensive regression workflow template
class RegressionAnalysisPipeline:
    """Complete regression analysis pipeline"""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        self.best_model = None
        self.scaler = StandardScaler()
    
    def add_model(self, name, model, needs_scaling=False):
        """Add model to pipeline"""
        self.models[name] = {'model': model, 'needs_scaling': needs_scaling}
    
    def fit_and_evaluate(self, X, y, test_size=0.2):
        """Fit all models and evaluate comprehensively"""
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Fit scaler
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        for name, model_info in self.models.items():
            model = model_info['model']
            needs_scaling = model_info['needs_scaling']
            
            # Select appropriate data
            if needs_scaling:
                X_tr, X_te = X_train_scaled, X_test_scaled
            else:
                X_tr, X_te = X_train, X_test
            
            # Fit model
            model.fit(X_tr, y_train)
            
            # Predictions
            y_pred = model.predict(X_te)
            y_train_pred = model.predict(X_tr)
            
            # Metrics
            metrics = {
                'r2_test': r2_score(y_test, y_pred),
                'r2_train': r2_score(y_train, y_train_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'mae': mean_absolute_error(y_test, y_pred),
                'residuals': y_test - y_pred
            }
            
            # Cross-validation
            if needs_scaling:
                pipeline = Pipeline([('scaler', StandardScaler()), ('model', model)])
                cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='r2')
            else:
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
            
            metrics['cv_r2_mean'] = cv_scores.mean()
            metrics['cv_r2_std'] = cv_scores.std()
            
            self.results[name] = metrics
        
        # Find best model
        self.best_model = max(self.results.keys(), key=lambda k: self.results[k]['cv_r2_mean'])
        
        return self.results
    
    def generate_report(self):
        """Generate comprehensive report"""
        
        print("REGRESSION ANALYSIS REPORT")
        print("=" * 50)
        
        # Model comparison
        print("\n1. MODEL COMPARISON:")
        print(f"{'Model':<20} {'R² Test':<10} {'RMSE':<10} {'CV R²':<15}")
        print("-" * 60)
        
        for name, results in self.results.items():
            cv_score = f"{results['cv_r2_mean']:.3f}±{results['cv_r2_std']:.3f}"
            print(f"{name:<20} {results['r2_test']:<10.4f} {results['rmse']:<10.4f} {cv_score:<15}")
        
        print(f"\nBest model: {self.best_model}")
        
        # Residual analysis
        print(f"\n2. RESIDUAL ANALYSIS ({self.best_model}):")
        best_residuals = self.results[self.best_model]['residuals']
        
        # Basic statistics
        print(f"   Residual mean: {np.mean(best_residuals):.6f}")
        print(f"   Residual std: {np.std(best_residuals):.4f}")
        
        # Normality test
        _, p_norm = stats.normaltest(best_residuals)
        print(f"   Normality test p-value: {p_norm:.4f}")
        
        if p_norm > 0.05:
            print("   ✓ Residuals appear normally distributed")
        else:
            print("   ⚠ Residuals may not be normally distributed")
    
    def predict_with_uncertainty(self, X_new, confidence_level=0.95):
        """Make predictions z uncertainty estimates"""
        
        best_model_info = self.models[self.best_model]
        model = best_model_info['model']
        
        # Prepare data
        if best_model_info['needs_scaling']:
            X_new_processed = self.scaler.transform(X_new)
        else:
            X_new_processed = X_new
        
        # Point predictions
        predictions = model.predict(X_new_processed)
        
        # Uncertainty estimate (simplified)
        best_results = self.results[self.best_model]
        residual_std = np.std(best_results['residuals'])
        
        # Confidence intervals
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        margin_of_error = z_score * residual_std
        
        lower_bound = predictions - margin_of_error
        upper_bound = predictions + margin_of_error
        
        return {
            'predictions': predictions,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'margin_of_error': margin_of_error
        }

# Example usage
def demonstrate_pipeline():
    """Demonstracja RegressionAnalysisPipeline"""
    
    print("Regression Analysis Pipeline Demo:")
    print("=" * 40)
    
    # Create pipeline
    pipeline = RegressionAnalysisPipeline()
    
    # Add models
    pipeline.add_model('Linear Regression', LinearRegression(), needs_scaling=True)
    pipeline.add_model('Ridge', Ridge(alpha=1.0), needs_scaling=True)
    pipeline.add_model('Random Forest', RandomForestRegressor(n_estimators=100, random_state=42), needs_scaling=False)
    pipeline.add_model('SVR', SVR(kernel='rbf'), needs_scaling=True)
    
    # Generate test data
    X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)
    
    # Fit and evaluate
    results = pipeline.fit_and_evaluate(X, y)
    
    # Generate report
    pipeline.generate_report()
    
    # Make predictions z uncertainty
    X_new = np.random.randn(5, 10)
    predictions = pipeline.predict_with_uncertainty(X_new)
    
    print(f"\n3. PREDICTIONS WITH UNCERTAINTY:")
    for i in range(len(predictions['predictions'])):
        pred = predictions['predictions'][i]
        lower = predictions['lower_bound'][i]  
        upper = predictions['upper_bound'][i]
        print(f"   Sample {i+1}: {pred:.2f} [{lower:.2f}, {upper:.2f}]")

demonstrate_pipeline()
```

---

### 🔗 Powiązane tematy

- [[Classification Algorithms - Comprehensive Guide]] - Algorytmy klasyfikacji
- [[Scikit-learn - Podstawy i Pipeline]] - Podstawy scikit-learn
- [[Feature Engineering - Podstawy]] - Inżynieria cech
- [[Model Evaluation i Metrics]] - Ewaluacja modeli
- [[Statistical Testing - Podstawy]] - Testy statystyczne