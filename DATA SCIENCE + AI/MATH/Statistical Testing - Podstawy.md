## 📊 Statistical Testing - Podstawy

_Testy hipotez statystycznych w Data Science_

---

### 📝 Wprowadzenie do testowania hipotez

**Testy statystyczne** pozwalają na podejmowanie decyzji opartych na danych:

1. **Sprawdzenie różnic** między grupami
2. **Walidacja założeń** modelowych
3. **A/B testing** w biznesie
4. **Quality assurance** danych

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_1samp, ttest_ind, chi2_contingency
from scipy.stats import shapiro, normaltest, kstest
from scipy.stats import mannwhitneyu, kruskal, wilcoxon
import warnings
warnings.filterwarnings('ignore')

# Konfiguracja
np.random.seed(42)
plt.style.use('seaborn-v0_8')
```

---

### 🎯 Framework testowania hipotez

```python
def hypothesis_test_framework():
    """Framework dla testowania hipotez"""
    
    framework = """
    🎯 FRAMEWORK TESTOWANIA HIPOTEZ
    
    1️⃣ SFORMUŁOWANIE HIPOTEZ:
    • H₀ (hipoteza zerowa): Brak efektu/różnicy
    • H₁ (hipoteza alternatywna): Istnienie efektu/różnicy
    
    2️⃣ WYBÓR POZIOMU ISTOTNOŚCI:
    • α = 0.05 (standardowy)
    • α = 0.01 (bardziej rygorystyczny)
    • α = 0.10 (mniej rygorystyczny)
    
    3️⃣ WYBÓR TESTU:
    • Typ danych (numeryczne, kategoryczne)
    • Liczba grup
    • Założenia o rozkładzie
    • Wielkość próby
    
    4️⃣ OBLICZENIE STATYSTYKI:
    • Test statistic
    • P-value
    • Confidence interval
    
    5️⃣ DECYZJA:
    • p < α → Odrzuć H₀
    • p ≥ α → Nie ma podstaw do odrzucenia H₀
    
    6️⃣ INTERPRETACJA:
    • Znaczenie praktyczne vs statystyczne
    • Effect size
    • Ograniczenia i założenia
    """
    
    print(framework)

hypothesis_test_framework()
```

---

### 🔍 Testy normalności

```python
# Generowanie danych testowych
np.random.seed(42)
data_normal = np.random.normal(100, 15, 1000)
data_uniform = np.random.uniform(50, 150, 1000)  
data_exponential = np.random.exponential(2, 1000)
data_skewed = np.random.gamma(2, 2, 1000)

datasets = {
    'Normal': data_normal,
    'Uniform': data_uniform, 
    'Exponential': data_exponential,
    'Skewed (Gamma)': data_skewed
}

print("=== TESTY NORMALNOŚCI ===")

# Funkcja do testowania normalności
def test_normality(data, name):
    """Kompleksowe testowanie normalności"""
    
    results = {}
    
    # 1. Shapiro-Wilk test (dla n < 5000)
    if len(data) <= 5000:
        stat, p_value = shapiro(data)
        results['Shapiro-Wilk'] = {'statistic': stat, 'p_value': p_value}
    
    # 2. D'Agostino's normality test
    stat, p_value = normaltest(data)
    results["D'Agostino"] = {'statistic': stat, 'p_value': p_value}
    
    # 3. Kolmogorov-Smirnov test
    stat, p_value = kstest(data, 'norm', args=(np.mean(data), np.std(data)))
    results['Kolmogorov-Smirnov'] = {'statistic': stat, 'p_value': p_value}
    
    # 4. Opisowe statystyki
    results['Skewness'] = stats.skew(data)
    results['Kurtosis'] = stats.kurtosis(data)
    
    print(f"\n--- {name} ---")
    for test_name, result in results.items():
        if isinstance(result, dict):
            p_val = result['p_value']
            interpretation = "Normalny" if p_val > 0.05 else "Nie-normalny"
            print(f"{test_name}: p-value = {p_val:.6f} ({interpretation})")
        else:
            print(f"{test_name}: {result:.4f}")
    
    return results

# Testowanie wszystkich rozkładów
normality_results = {}
for name, data in datasets.items():
    normality_results[name] = test_normality(data, name)

# Wizualizacja rozkładów
fig, axes = plt.subplots(2, 4, figsize=(16, 8))

for i, (name, data) in enumerate(datasets.items()):
    # Histogram z krzywą normalną
    axes[0, i].hist(data, bins=50, density=True, alpha=0.7)
    mu, sigma = np.mean(data), np.std(data)
    x = np.linspace(data.min(), data.max(), 100)
    axes[0, i].plot(x, stats.norm.pdf(x, mu, sigma), 'r-', lw=2)
    axes[0, i].set_title(f'{name}')
    
    # Q-Q plot
    stats.probplot(data, dist="norm", plot=axes[1, i])
    axes[1, i].set_title(f'Q-Q Plot: {name}')

plt.tight_layout()
plt.show()
```

---

### 📈 Testy dla jednej próby

```python
print("\n=== TESTY DLA JEDNEJ PRÓBY ===")

# Dane: wyniki testów studentów
test_scores = np.random.normal(75, 12, 100)

# 1. One-sample t-test
# H0: średnia = 70, H1: średnia ≠ 70
target_mean = 70
t_stat, p_value = ttest_1samp(test_scores, target_mean)

print(f"One-sample t-test:")
print(f"H₀: μ = {target_mean}")
print(f"t-statistic = {t_stat:.4f}")
print(f"p-value = {p_value:.6f}")
print(f"Decyzja: {'Odrzuć H₀' if p_value < 0.05 else 'Nie ma podstaw do odrzucenia H₀'}")

# Confidence interval
confidence_level = 0.95
alpha = 1 - confidence_level
degrees_of_freedom = len(test_scores) - 1
t_critical = stats.t.ppf(1 - alpha/2, degrees_of_freedom)

mean_score = np.mean(test_scores)
std_err = stats.sem(test_scores)
margin_of_error = t_critical * std_err

ci_lower = mean_score - margin_of_error
ci_upper = mean_score + margin_of_error

print(f"\n95% Confidence Interval: [{ci_lower:.2f}, {ci_upper:.2f}]")

# 2. Wilcoxon signed-rank test (non-parametric alternative)
differences = test_scores - target_mean
wilcoxon_stat, wilcoxon_p = wilcoxon(differences)

print(f"\nWilcoxon signed-rank test (non-parametric):")
print(f"W-statistic = {wilcoxon_stat:.4f}")
print(f"p-value = {wilcoxon_p:.6f}")

# Effect size (Cohen's d)
cohens_d = (mean_score - target_mean) / np.std(test_scores, ddof=1)
print(f"\nEffect size (Cohen's d) = {cohens_d:.4f}")

effect_interpretation = ""
if abs(cohens_d) < 0.2:
    effect_interpretation = "Małe"
elif abs(cohens_d) < 0.5:
    effect_interpretation = "Średnie"  
elif abs(cohens_d) < 0.8:
    effect_interpretation = "Duże"
else:
    effect_interpretation = "Bardzo duże"

print(f"Interpretacja effect size: {effect_interpretation}")
```

---

### 👥 Testy dla dwóch prób

```python
print("\n=== TESTY DLA DWÓCH PRÓB ===")

# Generowanie danych: wyniki przed i po treningu
before_training = np.random.normal(70, 10, 50)
after_training = np.random.normal(75, 10, 50)

# Dane niezależne
group_a = np.random.normal(100, 15, 100)  # Grupa kontrolna
group_b = np.random.normal(105, 15, 100)  # Grupa testowa

def two_sample_tests(data1, data2, paired=False, names=('Group 1', 'Group 2')):
    """Kompleksowe testy dla dwóch prób"""
    
    print(f"\n--- Porównanie {names[0]} vs {names[1]} ---")
    
    # Podstawowe statystyki
    mean1, mean2 = np.mean(data1), np.mean(data2)
    std1, std2 = np.std(data1, ddof=1), np.std(data2, ddof=1)
    
    print(f"{names[0]}: Mean = {mean1:.2f}, SD = {std1:.2f}")
    print(f"{names[1]}: Mean = {mean2:.2f}, SD = {std2:.2f}")
    print(f"Różnica średnich: {mean2 - mean1:.2f}")
    
    # Test równości wariancji (Levene's test)
    levene_stat, levene_p = stats.levene(data1, data2)
    equal_var = levene_p > 0.05
    print(f"\nLevene's test (równość wariancji): p = {levene_p:.4f}")
    print(f"Równe wariancje: {'Tak' if equal_var else 'Nie'}")
    
    if paired:
        # Paired t-test
        t_stat, p_value = ttest_1samp(data2 - data1, 0)
        print(f"\nPaired t-test:")
        test_name = "Paired t-test"
        
        # Wilcoxon signed-rank (non-parametric)
        wilcoxon_stat, wilcoxon_p = wilcoxon(data1, data2)
        print(f"Wilcoxon signed-rank: p = {wilcoxon_p:.6f}")
        
    else:
        # Independent t-test
        t_stat, p_value = ttest_ind(data1, data2, equal_var=equal_var)
        test_name = f"Independent t-test (equal_var={equal_var})"
        
        # Mann-Whitney U (non-parametric)
        u_stat, mann_p = mannwhitneyu(data1, data2, alternative='two-sided')
        print(f"Mann-Whitney U test: p = {mann_p:.6f}")
    
    print(f"\n{test_name}:")
    print(f"t-statistic = {t_stat:.4f}")
    print(f"p-value = {p_value:.6f}")
    print(f"Decyzja: {'Odrzuć H₀' if p_value < 0.05 else 'Nie ma podstaw do odrzucenia H₀'}")
    
    # Effect size (Cohen's d)
    if paired:
        cohens_d = np.mean(data2 - data1) / np.std(data2 - data1, ddof=1)
    else:
        pooled_std = np.sqrt(((len(data1)-1)*std1**2 + (len(data2)-1)*std2**2) / 
                            (len(data1) + len(data2) - 2))
        cohens_d = (mean2 - mean1) / pooled_std
    
    print(f"Cohen's d = {cohens_d:.4f}")
    
    return {
        'test_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'equal_var': equal_var
    }

# Testy dla różnych przypadków
results_independent = two_sample_tests(group_a, group_b, 
                                     names=('Kontrolna', 'Testowa'))

results_paired = two_sample_tests(before_training, after_training, paired=True,
                                names=('Przed', 'Po treningu'))
```

---

### 🔢 Testy dla zmiennych kategorycznych

```python
print("\n=== TESTY DLA ZMIENNYCH KATEGORYCZNYCH ===")

# Przykład: skuteczność dwóch leków
np.random.seed(42)
drug_data = pd.DataFrame({
    'drug': ['A'] * 100 + ['B'] * 100,
    'outcome': np.concatenate([
        np.random.choice(['Success', 'Failure'], 100, p=[0.7, 0.3]),
        np.random.choice(['Success', 'Failure'], 100, p=[0.8, 0.2])
    ])
})

# 1. Chi-square test of independence
contingency_table = pd.crosstab(drug_data['drug'], drug_data['outcome'])
print("Tabela kontyngencji:")
print(contingency_table)

chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"\nChi-square test of independence:")
print(f"Chi² = {chi2_stat:.4f}")
print(f"p-value = {p_value:.6f}")
print(f"Degrees of freedom = {dof}")
print(f"Decyzja: {'Istnieje związek' if p_value < 0.05 else 'Brak związku'}")

print("\nOczekiwane częstości:")
print(pd.DataFrame(expected, 
                   index=contingency_table.index, 
                   columns=contingency_table.columns))

# Effect size (Cramér's V)
n = contingency_table.sum().sum()
cramers_v = np.sqrt(chi2_stat / (n * (min(contingency_table.shape) - 1)))
print(f"\nCramér's V = {cramers_v:.4f}")

# 2. Fisher's exact test (dla małych prób)
from scipy.stats import fisher_exact

# Tylko dla tabel 2x2
if contingency_table.shape == (2, 2):
    odds_ratio, fisher_p = fisher_exact(contingency_table)
    print(f"\nFisher's exact test:")
    print(f"Odds ratio = {odds_ratio:.4f}")
    print(f"p-value = {fisher_p:.6f}")

# 3. Test proporcji
success_a = contingency_table.loc['A', 'Success']
success_b = contingency_table.loc['B', 'Success']
total_a = contingency_table.loc['A'].sum()
total_b = contingency_table.loc['B'].sum()

prop_a = success_a / total_a
prop_b = success_b / total_b

print(f"\nProporcje sukcesu:")
print(f"Lek A: {prop_a:.3f} ({success_a}/{total_a})")
print(f"Lek B: {prop_b:.3f} ({success_b}/{total_b})")
print(f"Różnica proporcji: {prop_b - prop_a:.3f}")

# Two-proportion z-test
from statsmodels.stats.proportion import proportions_ztest

counts = np.array([success_a, success_b])
nobs = np.array([total_a, total_b])
z_stat, z_p = proportions_ztest(counts, nobs)

print(f"\nTwo-proportion z-test:")
print(f"z = {z_stat:.4f}")
print(f"p-value = {z_p:.6f}")
```

---

### 📊 A/B Testing Framework

```python
print("\n=== A/B TESTING FRAMEWORK ===")

def ab_test_analysis(control_data, treatment_data, metric_name="Metric"):
    """Kompleksowa analiza A/B testu"""
    
    print(f"🧪 A/B TEST ANALYSIS - {metric_name}")
    print("=" * 50)
    
    # 1. Sample sizes and basic stats
    n_control = len(control_data)
    n_treatment = len(treatment_data)
    
    mean_control = np.mean(control_data)
    mean_treatment = np.mean(treatment_data)
    
    std_control = np.std(control_data, ddof=1)
    std_treatment = np.std(treatment_data, ddof=1)
    
    print(f"📊 BASIC STATISTICS:")
    print(f"Control Group:   n={n_control:,}, Mean={mean_control:.3f}, SD={std_control:.3f}")
    print(f"Treatment Group: n={n_treatment:,}, Mean={mean_treatment:.3f}, SD={std_treatment:.3f}")
    
    # 2. Effect size
    absolute_lift = mean_treatment - mean_control
    relative_lift = (absolute_lift / mean_control) * 100
    
    pooled_std = np.sqrt(((n_control-1)*std_control**2 + (n_treatment-1)*std_treatment**2) / 
                        (n_control + n_treatment - 2))
    cohens_d = absolute_lift / pooled_std
    
    print(f"\n📈 EFFECT SIZE:")
    print(f"Absolute Lift: {absolute_lift:.4f}")
    print(f"Relative Lift: {relative_lift:.2f}%")
    print(f"Cohen's d: {cohens_d:.4f}")
    
    # 3. Statistical test
    t_stat, p_value = ttest_ind(control_data, treatment_data)
    
    print(f"\n🔬 STATISTICAL TEST:")
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.6f}")
    
    # 4. Confidence interval for difference
    se_diff = np.sqrt(std_control**2/n_control + std_treatment**2/n_treatment)
    dof = n_control + n_treatment - 2
    t_critical = stats.t.ppf(0.975, dof)  # 95% CI
    
    ci_lower = absolute_lift - t_critical * se_diff
    ci_upper = absolute_lift + t_critical * se_diff
    
    print(f"95% CI for difference: [{ci_lower:.4f}, {ci_upper:.4f}]")
    
    # 5. Power analysis
    from scipy.stats import power
    
    # Calculate observed power
    effect_size = cohens_d
    alpha = 0.05
    
    # Approximate power calculation
    power_approx = stats.ttest_ind_from_stats(
        mean_control, std_control, n_control,
        mean_treatment, std_treatment, n_treatment
    )[1]
    
    print(f"\n⚡ POWER ANALYSIS:")
    print(f"Effect Size (Cohen's d): {effect_size:.4f}")
    print(f"Alpha level: {alpha}")
    
    # 6. Business interpretation
    print(f"\n💼 BUSINESS INTERPRETATION:")
    if p_value < 0.05:
        significance = "STATISTICALLY SIGNIFICANT"
        if abs(relative_lift) > 5:  # Arbitrary business threshold
            business_significance = "PRACTICALLY SIGNIFICANT"
        else:
            business_significance = "NOT PRACTICALLY SIGNIFICANT"
    else:
        significance = "NOT STATISTICALLY SIGNIFICANT"
        business_significance = "NOT SIGNIFICANT"
    
    print(f"Statistical Significance: {significance}")
    print(f"Business Significance: {business_significance}")
    
    # 7. Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if p_value < 0.05 and abs(relative_lift) > 5:
        if relative_lift > 0:
            print("✅ IMPLEMENT: Treatment shows significant positive impact")
        else:
            print("❌ DO NOT IMPLEMENT: Treatment shows significant negative impact")
    elif p_value < 0.05 and abs(relative_lift) <= 5:
        print("⚠️  CONSIDER: Statistically significant but small practical impact")
    else:
        print("🔄 CONTINUE TESTING: No significant difference detected")
    
    return {
        'absolute_lift': absolute_lift,
        'relative_lift': relative_lift,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper
    }

# Przykład A/B testu - conversion rate
np.random.seed(42)

# Symulacja danych conversion (1 = conversion, 0 = no conversion)
control_conversions = np.random.binomial(1, 0.10, 1000)  # 10% baseline
treatment_conversions = np.random.binomial(1, 0.12, 1000)  # 12% treatment

# Analiza A/B testu
ab_results = ab_test_analysis(control_conversions, treatment_conversions, "Conversion Rate")

# Wizualizacja wyników
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Distribution comparison
conversion_data = pd.DataFrame({
    'Group': ['Control'] * len(control_conversions) + ['Treatment'] * len(treatment_conversions),
    'Conversion': np.concatenate([control_conversions, treatment_conversions])
})

sns.barplot(data=conversion_data, x='Group', y='Conversion', ax=axes[0])
axes[0].set_title('Conversion Rate by Group')
axes[0].set_ylabel('Conversion Rate')

# Confidence intervals
groups = ['Control', 'Treatment']
means = [np.mean(control_conversions), np.mean(treatment_conversions)]
errors = [stats.sem(control_conversions), stats.sem(treatment_conversions)]

axes[1].bar(groups, means, yerr=errors, capsize=10, alpha=0.7)
axes[1].set_title('Conversion Rates with 95% CI')
axes[1].set_ylabel('Conversion Rate')

plt.tight_layout()
plt.show()
```

---

### 🎯 Power Analysis i Sample Size

```python
def power_analysis_guide():
    """Przewodnik power analysis"""
    
    print("=== POWER ANALYSIS ===")
    
    # Symulacja różnych scenariuszy
    effect_sizes = np.arange(0.1, 1.0, 0.1)
    sample_sizes = [50, 100, 200, 500, 1000]
    alpha = 0.05
    
    # Obliczenie mocy dla różnych kombinacji
    from scipy.stats import ttest_ind
    
    powers = []
    for effect_size in effect_sizes:
        power_row = []
        for n in sample_sizes:
            # Symulacja power przez Monte Carlo
            significant_tests = 0
            n_simulations = 1000
            
            for _ in range(n_simulations):
                control = np.random.normal(0, 1, n)
                treatment = np.random.normal(effect_size, 1, n)
                _, p_val = ttest_ind(control, treatment)
                if p_val < alpha:
                    significant_tests += 1
            
            power = significant_tests / n_simulations
            power_row.append(power)
        powers.append(power_row)
    
    # Vizualizacja power curves
    plt.figure(figsize=(10, 6))
    
    for i, n in enumerate(sample_sizes):
        power_values = [powers[j][i] for j in range(len(effect_sizes))]
        plt.plot(effect_sizes, power_values, marker='o', label=f'n={n}')
    
    plt.axhline(y=0.8, color='red', linestyle='--', label='Power = 0.8')
    plt.xlabel('Effect Size (Cohen\'s d)')
    plt.ylabel('Statistical Power')
    plt.title('Power Curves for Different Sample Sizes')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Sample size calculation
    print("\n📏 SAMPLE SIZE RECOMMENDATIONS:")
    target_power = 0.8
    
    for effect_size in [0.2, 0.5, 0.8]:  # Small, medium, large effects
        for n in sample_sizes:
            idx_effect = min(range(len(effect_sizes)), 
                           key=lambda i: abs(effect_sizes[i] - effect_size))
            idx_sample = sample_sizes.index(n)
            power = powers[idx_effect][idx_sample]
            
            if power >= target_power:
                print(f"Effect size {effect_size}: Minimum n ≈ {n} (Power = {power:.3f})")
                break

power_analysis_guide()
```

---

### 💡 Best Practices

```python
def statistical_testing_best_practices():
    """Najlepsze praktyki testowania statystycznego"""
    
    practices = """
    ✅ NAJLEPSZE PRAKTYKI TESTOWANIA STATYSTYCZNEGO
    
    📋 PRZED TESTEM:
    1. Określ hipotezy przed analizą danych
    2. Wybierz poziom istotności (α) z wyprzedzeniem
    3. Oblicz wymaganą wielkość próby (power analysis)
    4. Sprawdź założenia testu
    5. Plan pre-registration (dla ważnych badań)
    
    🔬 PODCZAS ANALIZY:
    1. Sprawdź jakość i kompletność danych
    2. Testuj założenia (normalność, równość wariancji)
    3. Użyj odpowiednich testów dla typu danych
    4. Rozważ multiple testing corrections
    5. Oblicz effect sizes
    
    📊 INTERPRETACJA:
    1. Rozróżnij significance statystyczne od praktycznego
    2. Raportuj confidence intervals
    3. Dyskutuj limitations i assumptions
    4. Unikaj p-hackingu
    5. Waliduj wyniki na nowych danych
    
    ⚠️  CZĘSTE BŁĘDY:
    • Multiple testing bez korekty
    • Ignorowanie założeń testów
    • Koncentracja tylko na p-values
    • Brak effect size analysis
    • Post-hoc hypotheses (HARKing)
    • Niewłaściwy wybór testu
    """
    
    print(practices)

statistical_testing_best_practices()
```

---

### 🎯 Następny krok

Poznasz **Machine Learning Pipeline - Preprocessing**:

- Data preprocessing workflows
- Feature scaling and selection
- Pipeline construction with sklearn
- Cross-validation strategies  
- Model evaluation metrics