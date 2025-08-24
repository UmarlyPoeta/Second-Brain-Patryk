## 🎯 Classification Algorithms - Comprehensive Guide

_Kompletny przewodnik po algorytmach klasyfikacji w Machine Learning_

---

### 📝 Wprowadzenie do klasyfikacji

**Classification** to zadanie przewidywania kategorii (klasy) dla danych wejściowych:

1. **Binary classification** - dwie klasy (0/1, tak/nie)
2. **Multiclass classification** - więcej niż dwie klasy
3. **Multilabel classification** - wiele etykiet na raz
4. **Probabilistic vs deterministic** - prawdopodobieństwa vs konkretne klasy

---

### 🏛️ Linear Classification Algorithms

#### Logistic Regression

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, load_breast_cancer, load_iris
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def demonstrate_logistic_regression():
    """Demonstracja Logistic Regression"""
    
    print("Logistic Regression:")
    print("=" * 30)
    
    # Dataset
    X, y = make_classification(
        n_samples=2000, n_features=20, n_informative=15, 
        n_redundant=3, n_clusters_per_class=2, random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 1. Basic Logistic Regression
    print("1. Basic Logistic Regression:")
    
    lr_basic = LogisticRegression(random_state=42, max_iter=1000)
    lr_basic.fit(X_train_scaled, y_train)
    
    # Predictions
    y_pred = lr_basic.predict(X_test_scaled)
    y_proba = lr_basic.predict_proba(X_test_scaled)
    
    print(f"   Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"   AUC-ROC: {roc_auc_score(y_test, y_proba[:, 1]):.4f}")
    
    # Model interpretation
    print(f"   Coefficients shape: {lr_basic.coef_.shape}")
    print(f"   Intercept: {lr_basic.intercept_[0]:.4f}")
    print(f"   Top 3 positive coefficients: {np.argsort(lr_basic.coef_[0])[-3:]}")
    print(f"   Top 3 negative coefficients: {np.argsort(lr_basic.coef_[0])[:3]}")
    
    # 2. Regularization comparison
    print(f"\n2. Regularization Comparison:")
    
    regularization_strengths = [0.01, 0.1, 1.0, 10.0, 100.0]
    penalties = ['l1', 'l2', 'elasticnet']
    
    results = {}
    
    for penalty in penalties:
        results[penalty] = []
        
        for C in regularization_strengths:
            if penalty == 'elasticnet':
                lr = LogisticRegression(
                    penalty=penalty, C=C, solver='saga', 
                    l1_ratio=0.5, random_state=42, max_iter=1000
                )
            else:
                solver = 'liblinear' if penalty == 'l1' else 'lbfgs'
                lr = LogisticRegression(
                    penalty=penalty, C=C, solver=solver, 
                    random_state=42, max_iter=1000
                )
            
            cv_scores = cross_val_score(lr, X_train_scaled, y_train, cv=5, scoring='accuracy')
            results[penalty].append(cv_scores.mean())
    
    print("   Regularization results (CV accuracy):")
    for penalty in penalties:
        print(f"   {penalty.upper()}:")
        for i, C in enumerate(regularization_strengths):
            print(f"     C={C}: {results[penalty][i]:.4f}")
    
    # Best regularization
    best_penalty = max(penalties, key=lambda p: max(results[p]))
    best_C_idx = np.argmax(results[best_penalty])
    best_C = regularization_strengths[best_C_idx]
    
    print(f"\n   Best configuration: {best_penalty} with C={best_C}")
    
    # 3. Multiclass extension
    print(f"\n3. Multiclass Classification:")
    
    # Load multiclass dataset
    iris = load_iris()
    X_iris, y_iris = iris.data, iris.target
    X_iris_train, X_iris_test, y_iris_train, y_iris_test = train_test_split(
        X_iris, y_iris, test_size=0.3, random_state=42
    )
    
    # Scale features
    X_iris_train_scaled = scaler.fit_transform(X_iris_train)
    X_iris_test_scaled = scaler.transform(X_iris_test)
    
    # Multiclass strategies
    multiclass_strategies = ['ovr', 'multinomial']
    
    for strategy in multiclass_strategies:
        lr_multi = LogisticRegression(
            multi_class=strategy, random_state=42, max_iter=1000
        )
        lr_multi.fit(X_iris_train_scaled, y_iris_train)
        
        y_iris_pred = lr_multi.predict(X_iris_test_scaled)
        y_iris_proba = lr_multi.predict_proba(X_iris_test_scaled)
        
        accuracy = accuracy_score(y_iris_test, y_iris_pred)
        
        print(f"   {strategy.upper()} strategy:")
        print(f"     Accuracy: {accuracy:.4f}")
        print(f"     Coefficient matrix shape: {lr_multi.coef_.shape}")
        print(f"     Classes: {lr_multi.classes_}")

demonstrate_logistic_regression()
```

#### Linear SVM and variations

```python
from sklearn.svm import SVC, LinearSVC
from sklearn.calibration import CalibratedClassifierCV

def demonstrate_linear_svm():
    """Demonstracja Support Vector Machines"""
    
    print("Support Vector Machines:")
    print("=" * 30)
    
    # Dataset z different separability
    datasets = {
        'linearly_separable': make_classification(
            n_samples=1000, n_features=2, n_redundant=0, n_informative=2,
            n_clusters_per_class=1, random_state=42
        ),
        'non_linearly_separable': make_classification(
            n_samples=1000, n_features=2, n_redundant=0, n_informative=2,
            n_clusters_per_class=2, random_state=42
        )
    }
    
    for dataset_name, (X, y) in datasets.items():
        print(f"\n{dataset_name.upper()}:")
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scaling (important dla SVM)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 1. Linear SVM
        print(f"  Linear SVM:")
        
        linear_svm = LinearSVC(random_state=42, max_iter=2000)
        linear_svm.fit(X_train_scaled, y_train)
        
        linear_pred = linear_svm.predict(X_test_scaled)
        linear_accuracy = accuracy_score(y_test, linear_pred)
        
        print(f"    Accuracy: {linear_accuracy:.4f}")
        print(f"    Support vectors: N/A (LinearSVC)")
        print(f"    Coefficients shape: {linear_svm.coef_.shape}")
        
        # 2. RBF Kernel SVM
        print(f"  RBF Kernel SVM:")
        
        rbf_svm = SVC(kernel='rbf', random_state=42, probability=True)
        rbf_svm.fit(X_train_scaled, y_train)
        
        rbf_pred = rbf_svm.predict(X_test_scaled)
        rbf_proba = rbf_svm.predict_proba(X_test_scaled)
        rbf_accuracy = accuracy_score(y_test, rbf_pred)
        
        print(f"    Accuracy: {rbf_accuracy:.4f}")
        print(f"    Support vectors: {rbf_svm.n_support_}")
        print(f"    Support vector ratio: {rbf_svm.n_support_.sum() / len(X_train):.3f}")
        
        # 3. Polynomial Kernel SVM
        print(f"  Polynomial Kernel SVM:")
        
        poly_svm = SVC(kernel='poly', degree=3, random_state=42, probability=True)
        poly_svm.fit(X_train_scaled, y_train)
        
        poly_pred = poly_svm.predict(X_test_scaled)
        poly_accuracy = accuracy_score(y_test, poly_pred)
        
        print(f"    Accuracy: {poly_accuracy:.4f}")
        print(f"    Support vectors: {poly_svm.n_support_}")
        
        # 4. C parameter tuning
        print(f"  C Parameter Tuning (RBF):")
        
        C_values = [0.01, 0.1, 1.0, 10.0, 100.0]
        C_results = []
        
        for C in C_values:
            svm_c = SVC(kernel='rbf', C=C, random_state=42)
            cv_scores = cross_val_score(svm_c, X_train_scaled, y_train, cv=5)
            C_results.append(cv_scores.mean())
            print(f"    C={C}: CV accuracy = {cv_scores.mean():.4f}")
        
        best_C = C_values[np.argmax(C_results)]
        print(f"    Best C: {best_C}")
        
        # 5. Gamma parameter tuning (dla RBF)
        print(f"  Gamma Parameter Tuning (RBF, C={best_C}):")
        
        gamma_values = ['scale', 'auto', 0.001, 0.01, 0.1, 1.0]
        gamma_results = []
        
        for gamma in gamma_values:
            svm_gamma = SVC(kernel='rbf', C=best_C, gamma=gamma, random_state=42)
            cv_scores = cross_val_score(svm_gamma, X_train_scaled, y_train, cv=5)
            gamma_results.append(cv_scores.mean())
            print(f"    gamma={gamma}: CV accuracy = {cv_scores.mean():.4f}")

demonstrate_linear_svm()
```

---

### 🌳 Tree-Based Algorithms

#### Decision Trees

```python
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.metrics import classification_report

def demonstrate_decision_trees():
    """Demonstracja Decision Trees"""
    
    print("Decision Trees:")
    print("=" * 20)
    
    # Use interpretable dataset
    breast_cancer = load_breast_cancer()
    X, y = breast_cancer.data, breast_cancer.target
    feature_names = breast_cancer.feature_names
    class_names = breast_cancer.target_names
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Basic Decision Tree
    print("1. Basic Decision Tree:")
    
    dt_basic = DecisionTreeClassifier(random_state=42)
    dt_basic.fit(X_train, y_train)
    
    dt_pred = dt_basic.predict(X_test)
    dt_accuracy = accuracy_score(y_test, dt_pred)
    
    print(f"   Accuracy: {dt_accuracy:.4f}")
    print(f"   Tree depth: {dt_basic.get_depth()}")
    print(f"   Number of leaves: {dt_basic.get_n_leaves()}")
    print(f"   Number of nodes: {dt_basic.tree_.node_count}")
    
    # Feature importance
    feature_importance = dt_basic.feature_importances_
    top_features = np.argsort(feature_importance)[-5:]
    
    print("   Top 5 important features:")
    for idx in reversed(top_features):
        print(f"     {feature_names[idx]}: {feature_importance[idx]:.4f}")
    
    # 2. Overfitting demonstration
    print(f"\n2. Overfitting Analysis:")
    
    # Very deep tree
    dt_overfit = DecisionTreeClassifier(random_state=42)  # No constraints
    dt_overfit.fit(X_train, y_train)
    
    train_accuracy_overfit = dt_overfit.score(X_train, y_train)
    test_accuracy_overfit = dt_overfit.score(X_test, y_test)
    
    print(f"   Unrestricted tree:")
    print(f"     Training accuracy: {train_accuracy_overfit:.4f}")
    print(f"     Test accuracy: {test_accuracy_overfit:.4f}")
    print(f"     Overfitting gap: {train_accuracy_overfit - test_accuracy_overfit:.4f}")
    
    # 3. Pruning parameters
    print(f"\n3. Pruning Parameters:")
    
    pruning_params = {
        'max_depth': [3, 5, 10, None],
        'min_samples_split': [2, 10, 50],
        'min_samples_leaf': [1, 5, 20],
        'max_features': [None, 'sqrt', 'log2']
    }
    
    best_params = {}
    best_score = 0
    
    # Grid search (simplified)
    for max_depth in pruning_params['max_depth']:
        for min_samples_split in pruning_params['min_samples_split']:
            for min_samples_leaf in pruning_params['min_samples_leaf']:
                dt = DecisionTreeClassifier(
                    max_depth=max_depth,
                    min_samples_split=min_samples_split,
                    min_samples_leaf=min_samples_leaf,
                    random_state=42
                )
                
                cv_scores = cross_val_score(dt, X_train, y_train, cv=5)
                avg_score = cv_scores.mean()
                
                if avg_score > best_score:
                    best_score = avg_score
                    best_params = {
                        'max_depth': max_depth,
                        'min_samples_split': min_samples_split,
                        'min_samples_leaf': min_samples_leaf
                    }
    
    print(f"   Best parameters: {best_params}")
    print(f"   Best CV score: {best_score:.4f}")
    
    # 4. Optimized tree
    dt_optimized = DecisionTreeClassifier(**best_params, random_state=42)
    dt_optimized.fit(X_train, y_train)
    
    train_accuracy_opt = dt_optimized.score(X_train, y_train)
    test_accuracy_opt = dt_optimized.score(X_test, y_test)
    
    print(f"\n   Optimized tree:")
    print(f"     Training accuracy: {train_accuracy_opt:.4f}")
    print(f"     Test accuracy: {test_accuracy_opt:.4f}")
    print(f"     Overfitting gap: {train_accuracy_opt - test_accuracy_opt:.4f}")
    print(f"     Tree depth: {dt_optimized.get_depth()}")
    print(f"     Number of leaves: {dt_optimized.get_n_leaves()}")
    
    # 5. Tree interpretation
    print(f"\n4. Tree Interpretation:")
    
    # Use smaller tree dla interpretability
    dt_interpretable = DecisionTreeClassifier(max_depth=3, random_state=42)
    dt_interpretable.fit(X_train, y_train)
    
    # Text representation
    tree_rules = export_text(dt_interpretable, feature_names=list(feature_names), max_depth=2)
    print("   Decision tree rules (first 2 levels):")
    print(tree_rules[:500] + "..." if len(tree_rules) > 500 else tree_rules)

demonstrate_decision_trees()
```

#### Random Forest

```python
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

def demonstrate_random_forest():
    """Demonstracja Random Forest"""
    
    print("Random Forest:")
    print("=" * 20)
    
    # Dataset
    X, y = make_classification(
        n_samples=2000, n_features=20, n_informative=15, 
        n_redundant=3, n_clusters_per_class=2, random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Basic Random Forest
    print("1. Basic Random Forest:")
    
    rf_basic = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_basic.fit(X_train, y_train)
    
    rf_pred = rf_basic.predict(X_test)
    rf_proba = rf_basic.predict_proba(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)
    
    print(f"   Accuracy: {rf_accuracy:.4f}")
    print(f"   Number of trees: {rf_basic.n_estimators}")
    print(f"   Max features per tree: {rf_basic.max_features}")
    
    # Feature importance
    feature_importance = rf_basic.feature_importances_
    print(f"   Top 5 feature importances: {np.sort(feature_importance)[-5:]}")
    
    # 2. Hyperparameter tuning
    print(f"\n2. Hyperparameter Tuning:")
    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'max_features': ['sqrt', 'log2', None]
    }
    
    rf_grid = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        rf_grid, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=0
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"   Best parameters: {grid_search.best_params_}")
    print(f"   Best CV score: {grid_search.best_score_:.4f}")
    
    # Test best model
    best_rf = grid_search.best_estimator_
    best_pred = best_rf.predict(X_test)
    best_accuracy = accuracy_score(y_test, best_pred)
    
    print(f"   Best model test accuracy: {best_accuracy:.4f}")
    
    # 3. Out-of-bag evaluation
    print(f"\n3. Out-of-Bag (OOB) Evaluation:")
    
    rf_oob = RandomForestClassifier(
        n_estimators=100, oob_score=True, random_state=42
    )
    rf_oob.fit(X_train, y_train)
    
    print(f"   OOB Score: {rf_oob.oob_score_:.4f}")
    print(f"   Test Accuracy: {rf_oob.score(X_test, y_test):.4f}")
    print(f"   OOB vs Test difference: {abs(rf_oob.oob_score_ - rf_oob.score(X_test, y_test)):.4f}")
    
    # 4. Feature importance analysis
    print(f"\n4. Feature Importance Analysis:")
    
    # Compare different importance measures
    rf_full = RandomForestClassifier(n_estimators=200, random_state=42)
    rf_full.fit(X_train, y_train)
    
    # Gini importance (default)
    gini_importance = rf_full.feature_importances_
    
    # Permutation importance
    from sklearn.inspection import permutation_importance
    perm_importance = permutation_importance(
        rf_full, X_test, y_test, n_repeats=10, random_state=42
    )
    
    print("   Feature importance comparison (top 5 features):")
    top_gini = np.argsort(gini_importance)[-5:]
    top_perm = np.argsort(perm_importance.importances_mean)[-5:]
    
    print("   Gini importance:")
    for idx in reversed(top_gini):
        print(f"     Feature {idx}: {gini_importance[idx]:.4f}")
    
    print("   Permutation importance:")  
    for idx in reversed(top_perm):
        print(f"     Feature {idx}: {perm_importance.importances_mean[idx]:.4f} ± {perm_importance.importances_std[idx]:.4f}")
    
    # 5. Comparison z Extra Trees
    print(f"\n5. Random Forest vs Extra Trees:")
    
    et = ExtraTreesClassifier(n_estimators=100, random_state=42)
    et.fit(X_train, y_train)
    
    rf_time = %timeit -o -q rf_basic.fit(X_train, y_train)
    et_time = %timeit -o -q et.fit(X_train, y_train)
    
    rf_pred = rf_basic.predict(X_test)
    et_pred = et.predict(X_test)
    
    rf_acc = accuracy_score(y_test, rf_pred)
    et_acc = accuracy_score(y_test, et_pred)
    
    print(f"   Random Forest:")
    print(f"     Accuracy: {rf_acc:.4f}")
    print(f"     Training time: Variable (depends on system)")
    
    print(f"   Extra Trees:")
    print(f"     Accuracy: {et_acc:.4f}")
    print(f"     Training time: Variable (depends on system)")
    print(f"     Speed advantage: Extra Trees typically faster")

demonstrate_random_forest()
```

---

### 🎯 Ensemble Methods

#### Gradient Boosting

```python
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.ensemble import VotingClassifier, BaggingClassifier

def demonstrate_boosting():
    """Demonstracja algorytmów boosting"""
    
    print("Boosting Algorithms:")
    print("=" * 25)
    
    # Dataset
    X, y = make_classification(
        n_samples=2000, n_features=20, n_informative=15,
        n_redundant=3, n_clusters_per_class=2, random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Gradient Boosting Classifier
    print("1. Gradient Boosting:")
    
    gb = GradientBoostingClassifier(random_state=42)
    gb.fit(X_train, y_train)
    
    gb_pred = gb.predict(X_test)
    gb_proba = gb.predict_proba(X_test)
    gb_accuracy = accuracy_score(y_test, gb_pred)
    
    print(f"   Accuracy: {gb_accuracy:.4f}")
    print(f"   Number of estimators: {gb.n_estimators}")
    print(f"   Learning rate: {gb.learning_rate}")
    print(f"   Max depth: {gb.max_depth}")
    
    # Feature importance
    gb_importance = gb.feature_importances_
    top_gb_features = np.argsort(gb_importance)[-5:]
    print("   Top 5 features:")
    for idx in reversed(top_gb_features):
        print(f"     Feature {idx}: {gb_importance[idx]:.4f}")
    
    # 2. Learning rate analysis
    print(f"\n2. Learning Rate Analysis:")
    
    learning_rates = [0.01, 0.1, 0.2, 0.5, 1.0]
    lr_results = []
    
    for lr in learning_rates:
        gb_lr = GradientBoostingClassifier(
            learning_rate=lr, n_estimators=100, random_state=42
        )
        cv_scores = cross_val_score(gb_lr, X_train, y_train, cv=5)
        lr_results.append(cv_scores.mean())
        print(f"   Learning rate {lr}: CV accuracy = {cv_scores.mean():.4f}")
    
    best_lr = learning_rates[np.argmax(lr_results)]
    print(f"   Best learning rate: {best_lr}")
    
    # 3. Number of estimators analysis
    print(f"\n3. Number of Estimators Analysis:")
    
    n_estimators_range = [50, 100, 200, 300, 500]
    estimator_results = []
    
    for n_est in n_estimators_range:
        gb_nest = GradientBoostingClassifier(
            n_estimators=n_est, learning_rate=best_lr, random_state=42
        )
        cv_scores = cross_val_score(gb_nest, X_train, y_train, cv=5)
        estimator_results.append(cv_scores.mean())
        print(f"   n_estimators {n_est}: CV accuracy = {cv_scores.mean():.4f}")
    
    best_n_est = n_estimators_range[np.argmax(estimator_results)]
    print(f"   Best n_estimators: {best_n_est}")
    
    # 4. AdaBoost Comparison
    print(f"\n4. AdaBoost Comparison:")
    
    ada = AdaBoostClassifier(n_estimators=best_n_est, learning_rate=best_lr, random_state=42)
    ada.fit(X_train, y_train)
    
    ada_pred = ada.predict(X_test)
    ada_accuracy = accuracy_score(y_test, ada_pred)
    
    print(f"   AdaBoost accuracy: {ada_accuracy:.4f}")
    print(f"   Gradient Boosting accuracy: {gb_accuracy:.4f}")
    print(f"   Difference: {abs(ada_accuracy - gb_accuracy):.4f}")
    
    # Feature importance comparison
    ada_importance = ada.feature_importances_
    
    print("   Feature importance correlation:")
    importance_corr = np.corrcoef(gb_importance, ada_importance)[0, 1]
    print(f"   GB vs AdaBoost importance correlation: {importance_corr:.4f}")
    
    # 5. Early stopping analysis
    print(f"\n5. Training Progress Analysis:")
    
    # Train z validation monitoring
    gb_monitor = GradientBoostingClassifier(
        n_estimators=200, learning_rate=0.1, random_state=42,
        validation_fraction=0.2, n_iter_no_change=10
    )
    
    gb_monitor.fit(X_train, y_train)
    
    train_scores = gb_monitor.train_score_
    
    print(f"   Final number of estimators: {len(train_scores)}")
    print(f"   Training score progression:")
    print(f"     Initial: {train_scores[0]:.4f}")
    print(f"     After 50: {train_scores[min(49, len(train_scores)-1)]:.4f}")
    print(f"     Final: {train_scores[-1]:.4f}")

demonstrate_boosting()
```

#### Ensemble Combinations

```python
def demonstrate_ensemble_combinations():
    """Demonstracja kombinowania różnych modeli"""
    
    print("Ensemble Combinations:")
    print("=" * 30)
    
    # Dataset
    X, y = make_classification(
        n_samples=2000, n_features=20, n_informative=15,
        n_redundant=3, n_clusters_per_class=2, random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Base models
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(probability=True, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42)
    }
    
    # 1. Individual model performance
    print("1. Individual Model Performance:")
    
    individual_scores = {}
    individual_predictions = {}
    
    for name, model in models.items():
        if 'SVM' in name or 'Logistic' in name:
            model.fit(X_train_scaled, y_train)
            pred = model.predict(X_test_scaled)
            proba = model.predict_proba(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            proba = model.predict_proba(X_test)
        
        accuracy = accuracy_score(y_test, pred)
        individual_scores[name] = accuracy
        individual_predictions[name] = {'pred': pred, 'proba': proba}
        
        print(f"   {name}: {accuracy:.4f}")
    
    # 2. Voting Classifier
    print(f"\n2. Voting Classifiers:")
    
    # Hard voting
    voting_hard = VotingClassifier([
        ('lr', LogisticRegression(random_state=42, max_iter=1000)),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
        ('svm', SVC(random_state=42)),
        ('gb', GradientBoostingClassifier(random_state=42))
    ], voting='hard')
    
    # Note: Mixed scaled/unscaled features - w produkcji użyj pipeline
    voting_hard.fit(X_train, y_train)  # Simplified dla demo
    hard_pred = voting_hard.predict(X_test)
    hard_accuracy = accuracy_score(y_test, hard_pred)
    
    print(f"   Hard voting accuracy: {hard_accuracy:.4f}")
    
    # Soft voting
    voting_soft = VotingClassifier([
        ('lr', LogisticRegression(random_state=42, max_iter=1000)),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
        ('svm', SVC(probability=True, random_state=42)),
        ('gb', GradientBoostingClassifier(random_state=42))
    ], voting='soft')
    
    voting_soft.fit(X_train, y_train)
    soft_pred = voting_soft.predict(X_test)
    soft_accuracy = accuracy_score(y_test, soft_pred)
    
    print(f"   Soft voting accuracy: {soft_accuracy:.4f}")
    print(f"   Best individual: {max(individual_scores.values()):.4f}")
    print(f"   Voting improvement: {max(hard_accuracy, soft_accuracy) - max(individual_scores.values()):.4f}")
    
    # 3. Bagging ensemble
    print(f"\n3. Bagging Ensemble:")
    
    # Bagging z different base estimators
    base_estimators = [
        DecisionTreeClassifier(max_depth=10, random_state=42),
        LogisticRegression(random_state=42, max_iter=1000)
    ]
    
    for i, base_estimator in enumerate(base_estimators):
        bagging = BaggingClassifier(
            estimator=base_estimator, 
            n_estimators=50, 
            random_state=42
        )
        
        if 'Logistic' in str(base_estimator):
            bagging.fit(X_train_scaled, y_train)
            bagging_pred = bagging.predict(X_test_scaled)
        else:
            bagging.fit(X_train, y_train)
            bagging_pred = bagging.predict(X_test)
        
        bagging_accuracy = accuracy_score(y_test, bagging_pred)
        estimator_name = str(base_estimator.__class__.__name__)
        
        print(f"   Bagging z {estimator_name}: {bagging_accuracy:.4f}")
    
    # 4. Stacking (simplified)
    print(f"\n4. Manual Stacking:")
    
    # Create meta-features from individual predictions
    meta_features = np.column_stack([
        pred_data['proba'][:, 1] for pred_data in individual_predictions.values()
    ])
    
    print(f"   Meta-features shape: {meta_features.shape}")
    
    # Train meta-model
    meta_model = LogisticRegression(random_state=42)
    
    # Split dla stacking (simplified - should use CV)
    X_meta_train, X_meta_test, y_meta_train, y_meta_test = train_test_split(
        meta_features, y_test, test_size=0.5, random_state=42
    )
    
    meta_model.fit(X_meta_train, y_meta_train)
    stacked_pred = meta_model.predict(X_meta_test)
    stacked_accuracy = accuracy_score(y_meta_test, stacked_pred)
    
    print(f"   Stacking accuracy: {stacked_accuracy:.4f}")
    print(f"   Meta-model coefficients: {meta_model.coef_[0]}")
    
    # 5. Diversity analysis
    print(f"\n5. Model Diversity Analysis:")
    
    # Calculate agreement between models
    model_names = list(individual_predictions.keys())
    
    print("   Pairwise agreement matrix:")
    for i, name1 in enumerate(model_names):
        for j, name2 in enumerate(model_names):
            if i <= j:
                pred1 = individual_predictions[name1]['pred']
                pred2 = individual_predictions[name2]['pred']
                agreement = np.mean(pred1 == pred2)
                print(f"   {name1[:8]} vs {name2[:8]}: {agreement:.3f}")

demonstrate_ensemble_combinations()
```

---

### 🧠 Instance-Based Learning

#### k-Nearest Neighbors

```python
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.metrics import pairwise_distances

def demonstrate_knn():
    """Demonstracja k-Nearest Neighbors"""
    
    print("k-Nearest Neighbors:")
    print("=" * 25)
    
    # Dataset
    X, y = make_classification(
        n_samples=1500, n_features=10, n_informative=8,
        n_redundant=1, n_clusters_per_class=2, random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scaling (important dla distance-based algorithms)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 1. Effect of k parameter
    print("1. Effect of k Parameter:")
    
    k_values = [1, 3, 5, 7, 11, 15, 21, 31]
    k_results = []
    
    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k)
        cv_scores = cross_val_score(knn, X_train_scaled, y_train, cv=5)
        k_results.append(cv_scores.mean())
        print(f"   k={k}: CV accuracy = {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    best_k = k_values[np.argmax(k_results)]
    print(f"   Best k: {best_k}")
    
    # 2. Distance metrics comparison
    print(f"\n2. Distance Metrics Comparison:")
    
    distance_metrics = ['euclidean', 'manhattan', 'chebyshev', 'minkowski']
    metric_results = {}
    
    for metric in distance_metrics:
        if metric == 'minkowski':
            knn = KNeighborsClassifier(
                n_neighbors=best_k, metric=metric, p=2  # p=2 dla Euclidean
            )
        else:
            knn = KNeighborsClassifier(n_neighbors=best_k, metric=metric)
        
        cv_scores = cross_val_score(knn, X_train_scaled, y_train, cv=5)
        metric_results[metric] = cv_scores.mean()
        print(f"   {metric}: CV accuracy = {cv_scores.mean():.4f}")
    
    best_metric = max(metric_results.keys(), key=lambda x: metric_results[x])
    print(f"   Best metric: {best_metric}")
    
    # 3. Weighting schemes
    print(f"\n3. Weighting Schemes:")
    
    weights = ['uniform', 'distance']
    
    for weight in weights:
        knn = KNeighborsClassifier(
            n_neighbors=best_k, metric=best_metric, weights=weight
        )
        knn.fit(X_train_scaled, y_train)
        
        test_accuracy = knn.score(X_test_scaled, y_test)
        print(f"   {weight} weights: test accuracy = {test_accuracy:.4f}")
    
    # 4. Algorithm comparison
    print(f"\n4. Algorithm Comparison:")
    
    algorithms = ['auto', 'ball_tree', 'kd_tree', 'brute']
    
    for algorithm in algorithms:
        try:
            knn = KNeighborsClassifier(
                n_neighbors=best_k, algorithm=algorithm
            )
            
            import time
            start_time = time.time()
            knn.fit(X_train_scaled, y_train)
            pred = knn.predict(X_test_scaled)
            total_time = time.time() - start_time
            
            accuracy = accuracy_score(y_test, pred)
            print(f"   {algorithm}: accuracy = {accuracy:.4f}, time = {total_time:.4f}s")
            
        except ValueError as e:
            print(f"   {algorithm}: not suitable dla this dataset")
    
    # 5. Radius-based neighbors
    print(f"\n5. Radius-based Neighbors:")
    
    # Estimate good radius based na k-NN distances
    knn_for_radius = KNeighborsClassifier(n_neighbors=best_k)
    knn_for_radius.fit(X_train_scaled, y_train)
    
    # Get distances to k-th neighbor
    distances, indices = knn_for_radius.kneighbors(X_train_scaled)
    median_kth_distance = np.median(distances[:, -1])
    
    print(f"   Median distance to {best_k}th neighbor: {median_kth_distance:.4f}")
    
    # Try radius classifier
    radii = [median_kth_distance * factor for factor in [0.5, 1.0, 1.5, 2.0]]
    
    for radius in radii:
        try:
            radius_clf = RadiusNeighborsClassifier(radius=radius)
            radius_clf.fit(X_train_scaled, y_train)
            
            # Check if all test samples have neighbors
            test_neighbors = radius_clf.radius_neighbors(X_test_scaled, return_distance=False)
            samples_with_neighbors = sum(1 for neighbors in test_neighbors if len(neighbors) > 0)
            
            if samples_with_neighbors == len(X_test_scaled):
                pred = radius_clf.predict(X_test_scaled)
                accuracy = accuracy_score(y_test, pred)
                print(f"   Radius {radius:.3f}: accuracy = {accuracy:.4f}")
            else:
                print(f"   Radius {radius:.3f}: {samples_with_neighbors}/{len(X_test_scaled)} samples have neighbors")
                
        except Exception as e:
            print(f"   Radius {radius:.3f}: failed - {str(e)[:50]}")
    
    # 6. KNN dla imbalanced data
    print(f"\n6. KNN z Imbalanced Data:")
    
    # Create imbalanced dataset
    X_imb, y_imb = make_classification(
        n_samples=1000, n_features=10, n_informative=8,
        n_clusters_per_class=1, weights=[0.9, 0.1], random_state=42
    )
    
    X_train_imb, X_test_imb, y_train_imb, y_test_imb = train_test_split(
        X_imb, y_imb, test_size=0.2, stratify=y_imb, random_state=42
    )
    
    X_train_imb_scaled = scaler.fit_transform(X_train_imb)
    X_test_imb_scaled = scaler.transform(X_test_imb)
    
    print(f"   Class distribution: {np.bincount(y_train_imb)}")
    
    # Standard KNN
    knn_standard = KNeighborsClassifier(n_neighbors=5)
    knn_standard.fit(X_train_imb_scaled, y_train_imb)
    pred_standard = knn_standard.predict(X_test_imb_scaled)
    
    # Distance-weighted KNN
    knn_weighted = KNeighborsClassifier(n_neighbors=5, weights='distance')
    knn_weighted.fit(X_train_imb_scaled, y_train_imb)
    pred_weighted = knn_weighted.predict(X_test_imb_scaled)
    
    print("   Standard KNN:")
    print(classification_report(y_test_imb, pred_standard, target_names=['Majority', 'Minority']))
    
    print("   Distance-weighted KNN:")
    print(classification_report(y_test_imb, pred_weighted, target_names=['Majority', 'Minority']))

demonstrate_knn()
```

---

### 📊 Model Evaluation i Comparison

#### Comprehensive evaluation metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve,
    confusion_matrix, classification_report, cohen_kappa_score
)
import matplotlib.pyplot as plt

def comprehensive_model_evaluation():
    """Komprehensywna ewaluacja modeli klasyfikacji"""
    
    print("Comprehensive Model Evaluation:")
    print("=" * 40)
    
    # Create diverse datasets
    datasets = {
        'Balanced': make_classification(
            n_samples=1000, n_features=20, n_informative=15, 
            weights=[0.5, 0.5], random_state=42
        ),
        'Imbalanced': make_classification(
            n_samples=1000, n_features=20, n_informative=15,
            weights=[0.9, 0.1], random_state=42
        ),
        'Multiclass': load_iris(return_X_y=True)
    }
    
    # Models to compare
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(probability=True, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5)
    }
    
    for dataset_name, (X, y) in datasets.items():
        print(f"\n{dataset_name.upper()} DATASET:")
        print("=" * 30)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, stratify=y, random_state=42
        )
        
        # Preprocessing
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        results = {}
        
        # Train and evaluate każdy model
        for model_name, model in models.items():
            # Use scaled data dla models that need it
            if model_name in ['Logistic Regression', 'SVM', 'KNN']:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                if hasattr(model, 'predict_proba'):
                    y_proba = model.predict_proba(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                if hasattr(model, 'predict_proba'):
                    y_proba = model.predict_proba(X_test)
            
            # Calculate metrics
            metrics = {}
            
            # Basic metrics
            metrics['Accuracy'] = accuracy_score(y_test, y_pred)
            
            # Handle binary vs multiclass
            if len(np.unique(y)) == 2:
                # Binary classification
                metrics['Precision'] = precision_score(y_test, y_pred)
                metrics['Recall'] = recall_score(y_test, y_pred)
                metrics['F1'] = f1_score(y_test, y_pred)
                
                if hasattr(model, 'predict_proba'):
                    metrics['AUC-ROC'] = roc_auc_score(y_test, y_proba[:, 1])
                
                metrics['Kappa'] = cohen_kappa_score(y_test, y_pred)
                
            else:
                # Multiclass classification
                metrics['Precision'] = precision_score(y_test, y_pred, average='weighted')
                metrics['Recall'] = recall_score(y_test, y_pred, average='weighted')
                metrics['F1'] = f1_score(y_test, y_pred, average='weighted')
                
                if hasattr(model, 'predict_proba'):
                    try:
                        metrics['AUC-ROC'] = roc_auc_score(y_test, y_proba, multi_class='ovr')
                    except:
                        metrics['AUC-ROC'] = 'N/A'
                
                metrics['Kappa'] = cohen_kappa_score(y_test, y_pred)
            
            results[model_name] = metrics
        
        # Display results
        metric_names = list(results[list(models.keys())[0]].keys())
        
        print(f"{'Model':<20}", end='')
        for metric in metric_names:
            print(f"{metric:<12}", end='')
        print()
        print("-" * (20 + 12 * len(metric_names)))
        
        for model_name, metrics in results.items():
            print(f"{model_name:<20}", end='')
            for metric_name in metric_names:
                value = metrics[metric_name]
                if isinstance(value, float):
                    print(f"{value:<12.4f}", end='')
                else:
                    print(f"{str(value):<12}", end='')
            print()
        
        # Best model per metric
        print(f"\nBest models per metric:")
        for metric in metric_names:
            if metric != 'AUC-ROC' or all(isinstance(results[m][metric], float) for m in models.keys()):
                if isinstance(list(results.values())[0][metric], float):
                    best_model = max(results.keys(), key=lambda x: results[x][metric])
                    best_score = results[best_model][metric]
                    print(f"  {metric}: {best_model} ({best_score:.4f})")
        
        # Confusion matrices dla binary datasets
        if len(np.unique(y)) == 2 and dataset_name != 'Multiclass':
            print(f"\nConfusion Matrices:")
            
            # Get best model by F1 score
            best_f1_model = max(results.keys(), key=lambda x: results[x]['F1'])
            best_model_obj = models[best_f1_model]
            
            # Refit and predict
            if best_f1_model in ['Logistic Regression', 'SVM', 'KNN']:
                best_model_obj.fit(X_train_scaled, y_train)
                best_pred = best_model_obj.predict(X_test_scaled)
            else:
                best_model_obj.fit(X_train, y_train)
                best_pred = best_model_obj.predict(X_test)
            
            cm = confusion_matrix(y_test, best_pred)
            print(f"  Best model ({best_f1_model}):")
            print(f"    {cm}")
            
            # Calculate additional metrics from confusion matrix
            tn, fp, fn, tp = cm.ravel()
            specificity = tn / (tn + fp)
            sensitivity = tp / (tp + fn)
            
            print(f"    Sensitivity (Recall): {sensitivity:.4f}")
            print(f"    Specificity: {specificity:.4f}")

comprehensive_model_evaluation()
```

---

### 💡 Best Practices

#### Classification best practices summary

```python
def classification_best_practices():
    """Best practices dla classification problems"""
    
    best_practices = """
    ✅ DATA PREPARATION:
    - Handle missing values appropriately
    - Scale features dla distance-based algorithms (KNN, SVM, Logistic Regression)
    - Encode categorical variables properly
    - Check for class imbalance
    - Split data properly (stratified dla imbalanced datasets)
    
    ✅ ALGORITHM SELECTION:
    - Logistic Regression: Good baseline, interpretable, fast
    - Random Forest: Robust, handles mixed data types, feature importance
    - SVM: Good dla high-dimensional data, kernel trick dla non-linearity
    - Gradient Boosting: Often best performance, careful tuning needed
    - KNN: Simple, good dla local patterns, can be slow
    
    ✅ MODEL EVALUATION:
    - Use appropriate metrics dla problem type (accuracy, precision, recall, F1, AUC)
    - Consider business context (is false positive or false negative worse?)
    - Use cross-validation dla robust evaluation
    - Check confusion matrix dla detailed error analysis
    - Test on truly unseen data
    
    ✅ HYPERPARAMETER TUNING:
    - Use GridSearchCV or RandomizedSearchCV
    - Be aware of computational cost
    - Use nested CV dla unbiased evaluation
    - Consider Bayesian optimization dla expensive tuning
    
    ✅ ENSEMBLE METHODS:
    - Combine diverse models dla better performance
    - Voting classifiers dla simple combination
    - Stacking dla meta-learning
    - Bagging dla variance reduction
    - Boosting dla bias reduction
    
    ✅ COMMON PITFALLS:
    - Data leakage (information from future in training)
    - Overfitting (too complex model)
    - Ignoring class imbalance
    - Not scaling features when needed
    - Using accuracy dla imbalanced datasets
    - Not validating on unseen data
    """
    
    print("Classification Best Practices:")
    print("=" * 40)
    print(best_practices)

classification_best_practices()

# Practical checklist class
class ClassificationPipeline:
    """Template dla comprehensive classification pipeline"""
    
    def __init__(self, problem_type='binary'):
        self.problem_type = problem_type
        self.preprocessing_steps = []
        self.models = {}
        self.results = {}
    
    def add_preprocessing_step(self, step_name, step_object):
        """Add preprocessing step"""
        self.preprocessing_steps.append((step_name, step_object))
    
    def add_model(self, model_name, model_object):
        """Add model to pipeline"""
        self.models[model_name] = model_object
    
    def evaluate_models(self, X, y, test_size=0.2):
        """Evaluate all models z comprehensive metrics"""
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=42
        )
        
        # Apply preprocessing
        X_train_processed = X_train.copy()
        X_test_processed = X_test.copy()
        
        preprocessing_pipeline = Pipeline(self.preprocessing_steps)
        X_train_processed = preprocessing_pipeline.fit_transform(X_train_processed)
        X_test_processed = preprocessing_pipeline.transform(X_test_processed)
        
        # Evaluate każdy model
        for model_name, model in self.models.items():
            model.fit(X_train_processed, y_train)
            y_pred = model.predict(X_test_processed)
            
            # Calculate metrics
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted'),
                'recall': recall_score(y_test, y_pred, average='weighted'),
                'f1': f1_score(y_test, y_pred, average='weighted')
            }
            
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(X_test_processed)
                if self.problem_type == 'binary' and len(np.unique(y)) == 2:
                    metrics['auc'] = roc_auc_score(y_test, y_proba[:, 1])
            
            self.results[model_name] = metrics
        
        return self.results
    
    def get_best_model(self, metric='f1'):
        """Get best model based na specified metric"""
        if not self.results:
            raise ValueError("No results available. Run evaluate_models first.")
        
        best_model = max(self.results.keys(), key=lambda x: self.results[x][metric])
        return best_model, self.results[best_model][metric]

# Example usage
def demonstrate_pipeline_class():
    """Demonstracja ClassificationPipeline class"""
    
    print("Classification Pipeline Class:")
    print("=" * 35)
    
    # Create pipeline
    pipeline = ClassificationPipeline(problem_type='binary')
    
    # Add preprocessing steps
    pipeline.add_preprocessing_step('scaler', StandardScaler())
    pipeline.add_preprocessing_step('selector', SelectKBest(k=10))
    
    # Add models
    pipeline.add_model('Logistic Regression', LogisticRegression(random_state=42))
    pipeline.add_model('Random Forest', RandomForestClassifier(n_estimators=100, random_state=42))
    pipeline.add_model('SVM', SVC(probability=True, random_state=42))
    
    # Test data
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    
    # Evaluate
    results = pipeline.evaluate_models(X, y)
    
    print("Pipeline Results:")
    for model_name, metrics in results.items():
        print(f"  {model_name}:")
        for metric_name, value in metrics.items():
            print(f"    {metric_name}: {value:.4f}")
    
    # Get best model
    best_model, best_score = pipeline.get_best_model('f1')
    print(f"\nBest model: {best_model} (F1: {best_score:.4f})")

demonstrate_pipeline_class()
```

---

### 🔗 Powiązane tematy

- [[Scikit-learn - Podstawy i Pipeline]] - Podstawy scikit-learn
- [[Regression Algorithms - Comprehensive Guide]] - Algorytmy regresji
- [[Model Evaluation i Metrics]] - Ewaluacja modeli
- [[Feature Engineering - Podstawy]] - Inżynieria cech
- [[Cross Validation Techniques]] - Techniki walidacji krzyżowej