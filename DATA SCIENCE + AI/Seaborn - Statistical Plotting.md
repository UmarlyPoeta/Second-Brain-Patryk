## 📈 Seaborn - Statistical Plotting

_Biblioteka do zaawansowanych wizualizacji statystycznych_

---

### 📝 Wprowadzenie do Seaborn

**Seaborn** to biblioteka zbudowana na Matplotlib, która oferuje:

1. **Gotowe style** - ładne wykresy od razu
2. **Statystyczne funkcje** - automatyczne obliczenia
3. **Integrację z Pandas** - bezpośrednia praca z DataFrame
4. **Wykresy wielowymiarowe** - łatwe grupowanie danych

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Konfiguracja
sns.set_style("whitegrid")  # whitegrid, darkgrid, white, dark, ticks
sns.set_palette("husl")     # husl, Set1, viridis, etc.
```

---

### 📊 Distribution Plots

```python
# Dane testowe
np.random.seed(42)
data = pd.DataFrame({
    'wartość': np.concatenate([
        np.random.normal(0, 1, 300),
        np.random.normal(3, 1.5, 200)
    ]),
    'grupa': ['A'] * 300 + ['B'] * 200,
    'kategoria': np.random.choice(['X', 'Y', 'Z'], 500)
})

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Histogram z KDE
sns.histplot(data=data, x='wartość', kde=True, ax=axes[0,0])
axes[0,0].set_title('Histogram z KDE')

# Histogram z grupowaniem
sns.histplot(data=data, x='wartość', hue='grupa', 
             bins=30, alpha=0.7, ax=axes[0,1])
axes[0,1].set_title('Histogram pogrupowany')

# KDE plot
sns.kdeplot(data=data, x='wartość', hue='grupa', 
            fill=True, alpha=0.6, ax=axes[0,2])
axes[0,2].set_title('Kernel Density Plot')

# Box plot
sns.boxplot(data=data, x='grupa', y='wartość', ax=axes[1,0])
axes[1,0].set_title('Box Plot')

# Violin plot
sns.violinplot(data=data, x='grupa', y='wartość', ax=axes[1,1])
axes[1,1].set_title('Violin Plot')

# Strip plot with swarm
sns.swarmplot(data=data, x='grupa', y='wartość', ax=axes[1,2])
axes[1,2].set_title('Swarm Plot')

plt.tight_layout()
plt.show()
```

---

### 🎯 Categorical Plots

```python
# Dane kategoryczne
tips = sns.load_dataset("tips")
print(tips.head())

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Bar plot
sns.barplot(data=tips, x='day', y='total_bill', ax=axes[0,0])
axes[0,0].set_title('Bar Plot')

# Count plot
sns.countplot(data=tips, x='day', hue='sex', ax=axes[0,1])
axes[0,1].set_title('Count Plot')

# Point plot
sns.pointplot(data=tips, x='day', y='total_bill', hue='sex', ax=axes[0,2])
axes[0,2].set_title('Point Plot')

# Cat plot (factor plot)
g = sns.catplot(data=tips, x='day', y='total_bill', 
                hue='sex', kind='bar', height=4, aspect=1.2)
g.fig.suptitle('Cat Plot (Bar)')
plt.show()

# Box plot with categories
sns.boxplot(data=tips, x='day', y='total_bill', hue='time', ax=axes[1,0])
axes[1,0].set_title('Box Plot z grupowaniem')

# Violin plot with split
sns.violinplot(data=tips, x='day', y='total_bill', 
               hue='sex', split=True, ax=axes[1,1])
axes[1,1].set_title('Split Violin Plot')

# Strip plot with dodge
sns.stripplot(data=tips, x='day', y='total_bill', 
              hue='sex', dodge=True, ax=axes[1,2])
axes[1,2].set_title('Strip Plot z dodge')

plt.tight_layout()
plt.show()
```

---

### 🔗 Relationship Plots

```python
# Scatter plot
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Basic scatter
sns.scatterplot(data=tips, x='total_bill', y='tip', ax=axes[0,0])
axes[0,0].set_title('Basic Scatter')

# Scatter z grupowaniem
sns.scatterplot(data=tips, x='total_bill', y='tip', 
                hue='time', style='sex', ax=axes[0,1])
axes[0,1].set_title('Grouped Scatter')

# Regression plot
sns.regplot(data=tips, x='total_bill', y='tip', ax=axes[1,0])
axes[1,0].set_title('Regression Plot')

# LM plot z grupami
sns.scatterplot(data=tips, x='total_bill', y='tip', hue='smoker', ax=axes[1,1])
# Dodanie linii regresji dla każdej grupy
for smoker in tips['smoker'].unique():
    subset = tips[tips['smoker'] == smoker]
    sns.regplot(data=subset, x='total_bill', y='tip', 
                scatter=False, ax=axes[1,1])
axes[1,1].set_title('Regression by Group')

plt.tight_layout()
plt.show()

# Pair plot - macierz scatter plotów
pair_cols = ['total_bill', 'tip', 'size']
g = sns.pairplot(tips[pair_cols + ['time']], hue='time')
g.fig.suptitle('Pair Plot', y=1.02)
plt.show()
```

---

### 🌡️ Heatmaps

```python
# Correlation heatmap
numeric_tips = tips.select_dtypes(include=[np.number])
corr_matrix = numeric_tips.corr()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Basic heatmap
sns.heatmap(corr_matrix, ax=axes[0])
axes[0].set_title('Basic Heatmap')

# Annotated heatmap
sns.heatmap(corr_matrix, annot=True, fmt='.2f', 
            cmap='coolwarm', center=0, ax=axes[1])
axes[1].set_title('Annotated Heatmap')

# Custom heatmap
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
            cmap='RdYlBu_r', vmin=-1, vmax=1,
            square=True, cbar_kws={"shrink": .8}, ax=axes[2])
axes[2].set_title('Triangular Heatmap')

plt.tight_layout()
plt.show()

# Pivot table heatmap
pivot_tips = tips.pivot_table(values='tip', index='day', 
                             columns='time', aggfunc='mean')
plt.figure(figsize=(8, 6))
sns.heatmap(pivot_tips, annot=True, fmt='.2f', cmap='YlOrRd')
plt.title('Średnia napiwku według dnia i pory')
plt.show()
```

---

### 📋 FacetGrid i PairGrid

```python
# FacetGrid - subplots based on categories
g = sns.FacetGrid(tips, col='time', row='smoker', margin_titles=True)
g.map(sns.scatterplot, 'total_bill', 'tip', alpha=0.7)
g.add_legend()
plt.show()

# FacetGrid z różnymi wykresami
g = sns.FacetGrid(tips, col='day', col_wrap=2, height=4)
g.map(sns.histplot, 'total_bill', bins=15)
plt.show()

# PairGrid - custom pair plot
g = sns.PairGrid(tips, vars=['total_bill', 'tip', 'size'], 
                 hue='time', diag_sharey=False)
g.map_upper(sns.scatterplot)
g.map_lower(sns.regplot)
g.map_diag(sns.histplot)
g.add_legend()
plt.show()

# Custom diagonal
g = sns.PairGrid(tips[['total_bill', 'tip', 'size']])
g.map_upper(plt.scatter)
g.map_diag(sns.histplot, kde=False)
g.map_lower(sns.regplot)
plt.show()
```

---

### 🎨 Style i palety kolorów

```python
# Różne style
styles = ['darkgrid', 'whitegrid', 'dark', 'white', 'ticks']
fig, axes = plt.subplots(1, len(styles), figsize=(20, 4))

for i, style in enumerate(styles):
    with sns.axes_style(style):
        sns.scatterplot(data=tips, x='total_bill', y='tip', ax=axes[i])
        axes[i].set_title(f'Style: {style}')

plt.tight_layout()
plt.show()

# Palety kolorów
palettes = ['deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind']
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, palette in enumerate(palettes):
    with sns.color_palette(palette):
        sns.boxplot(data=tips, x='day', y='total_bill', ax=axes[i])
        axes[i].set_title(f'Palette: {palette}')

plt.tight_layout()
plt.show()

# Custom palette
custom_palette = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
sns.set_palette(custom_palette)

plt.figure(figsize=(8, 6))
sns.boxplot(data=tips, x='day', y='total_bill')
plt.title('Custom Color Palette')
plt.show()

# Continuous color palette
plt.figure(figsize=(10, 6))
sns.scatterplot(data=tips, x='total_bill', y='tip', 
                hue='size', size='size', sizes=(50, 200),
                palette='viridis')
plt.title('Continuous Color Mapping')
plt.show()
```

---

### 💻 Praktyczne zastosowania

```python
# 1. Eksploracja dataset'u
iris = sns.load_dataset('iris')

# Quick overview
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Distribution by species
sns.boxplot(data=iris, x='species', y='sepal_length', ax=axes[0,0])
axes[0,0].set_title('Długość działki kielicha')

# Correlation within species
sns.scatterplot(data=iris, x='sepal_length', y='sepal_width', 
                hue='species', ax=axes[0,1])
axes[0,1].set_title('Długość vs Szerokość działki')

# Distribution comparison
sns.histplot(data=iris, x='petal_length', hue='species', 
             multiple='stack', ax=axes[1,0])
axes[1,0].set_title('Rozkład długości płatka')

# Pair relationships
iris_numeric = iris.select_dtypes(include=[np.number])
corr = iris_numeric.corr()
sns.heatmap(corr, annot=True, fmt='.2f', ax=axes[1,1])
axes[1,1].set_title('Macierz korelacji')

plt.tight_layout()
plt.show()

# 2. Business dashboard style
flights = sns.load_dataset('flights')
flights_pivot = flights.pivot(index='month', columns='year', values='passengers')

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Trend over time
sns.lineplot(data=flights, x='year', y='passengers', ax=axes[0,0])
axes[0,0].set_title('Trend pasażerów w czasie')

# Seasonality
sns.boxplot(data=flights, x='month', y='passengers', ax=axes[0,1])
axes[0,1].tick_params(axis='x', rotation=45)
axes[0,1].set_title('Sezonowość')

# Heatmap year-month
sns.heatmap(flights_pivot, cmap='YlOrRd', ax=axes[1,0])
axes[1,0].set_title('Mapa cieplna: rok vs miesiąc')

# Growth by decade
flights['decade'] = (flights['year'] // 10) * 10
sns.barplot(data=flights, x='decade', y='passengers', ax=axes[1,1])
axes[1,1].set_title('Średnia według dekad')

plt.tight_layout()
plt.show()
```

---

### 🔧 Konfiguracja i customization

```python
# Globalne ustawienia
sns.set(
    style="whitegrid",
    palette="muted",
    font_scale=1.2,
    rc={"figure.figsize": (10, 6)}
)

# Context dla różnych zastosowań
contexts = ['paper', 'notebook', 'talk', 'poster']
fig, axes = plt.subplots(1, 4, figsize=(20, 5))

for i, context in enumerate(contexts):
    with sns.plotting_context(context):
        sns.scatterplot(data=tips, x='total_bill', y='tip', ax=axes[i])
        axes[i].set_title(f'Context: {context}')

plt.tight_layout()
plt.show()

# Custom theme
def custom_theme():
    # Custom color palette
    custom_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    sns.set_palette(custom_colors)
    
    # Custom style
    sns.set_style("whitegrid", {
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.bottom": True,
        "ytick.left": True,
    })
    
    # Font settings
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 11
    })

# Aplikacja custom theme
custom_theme()
plt.figure(figsize=(10, 6))
sns.boxplot(data=tips, x='day', y='total_bill', hue='time')
plt.title('Custom Theme Example')
plt.show()

# Reset do defaults
sns.reset_defaults()
```

---

### 🎯 Następny krok

Poznasz **EDA - Exploratory Data Analysis**:

- Systematic data exploration
- Univariate analysis
- Bivariate relationships  
- Missing data patterns
- Outlier detection methods