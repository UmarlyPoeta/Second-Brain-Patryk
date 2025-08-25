## 📊 Matplotlib - Podstawy wizualizacji

_Główna biblioteka do tworzenia wykresów w Python_

---

### 📝 Wprowadzenie do Matplotlib

**Matplotlib** to najważniejsza biblioteka do tworzenia wykresów w Python:

1. **Elastyczność** - pełna kontrola nad każdym elementem wykresu
2. **Kompatybilność** - integracja z NumPy i Pandas
3. **Różne style** - od prostych do publikacyjnych wykresów
4. **Eksport** - PNG, PDF, SVG, PostScript

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Sprawdzenie wersji
print(f"Matplotlib version: {plt.__version__}")

# Konfiguracja dla Jupyter
%matplotlib inline
```

---

### 🏗️ Podstawowa anatomia wykresu

```python
# Podstawowy wykres
fig, ax = plt.subplots(figsize=(8, 6))

x = np.linspace(0, 10, 100)
y = np.sin(x)

ax.plot(x, y, color='blue', linewidth=2, label='sin(x)')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis') 
ax.set_title('Podstawowy wykres sin(x)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Alternatywna składnia (pyplot)
plt.figure(figsize=(8, 6))
plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Wykres sin(x) - pyplot style')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

### 🎨 Style i formatowanie

```python
# Dostępne style
print("Dostępne style:", plt.style.available[:10])

# Użycie stylu
plt.style.use('seaborn-v0_8')  # lub 'ggplot', 'bmh', 'classic'

# Kolory - różne sposoby definicji
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

x = np.linspace(0, 2*np.pi, 100)

# Subplot 1: Named colors
axes[0,0].plot(x, np.sin(x), color='red', label='sin')
axes[0,0].plot(x, np.cos(x), color='blue', label='cos')
axes[0,0].set_title('Named colors')
axes[0,0].legend()

# Subplot 2: Hex colors
axes[0,1].plot(x, np.sin(x), color='#FF6B6B', label='sin')
axes[0,1].plot(x, np.cos(x), color='#4ECDC4', label='cos')
axes[0,1].set_title('Hex colors')
axes[0,1].legend()

# Subplot 3: RGB tuples
axes[1,0].plot(x, np.sin(x), color=(0.8, 0.2, 0.2), label='sin')
axes[1,0].plot(x, np.cos(x), color=(0.2, 0.8, 0.6), label='cos')
axes[1,0].set_title('RGB tuples')
axes[1,0].legend()

# Subplot 4: Colormap
colors = plt.cm.viridis(np.linspace(0, 1, 4))
for i, func in enumerate([np.sin, np.cos, np.tan, lambda x: np.sin(2*x)]):
    axes[1,1].plot(x, func(x), color=colors[i], 
                   label=f'function {i+1}')
axes[1,1].set_title('Colormap colors')
axes[1,1].legend()
axes[1,1].set_ylim(-2, 2)

plt.tight_layout()
plt.show()
```

---

### 📈 Typy wykresów liniowych

```python
# Dane testowe
x = np.linspace(0, 10, 20)
y1 = x + np.random.normal(0, 1, 20)
y2 = x**0.5 + np.random.normal(0, 0.5, 20)
y3 = np.log(x + 1) * 3

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Różne style linii
axes[0,0].plot(x, y1, '-', label='Solid line')
axes[0,0].plot(x, y2, '--', label='Dashed line')  
axes[0,0].plot(x, y3, '-.', label='Dash-dot line')
axes[0,0].plot(x, y1*0.5, ':', label='Dotted line')
axes[0,0].set_title('Style linii')
axes[0,0].legend()

# Markery
axes[0,1].plot(x, y1, 'o-', markersize=6, label='Circles')
axes[0,1].plot(x, y2, 's--', markersize=6, label='Squares')
axes[0,1].plot(x, y3, '^:', markersize=6, label='Triangles')
axes[0,1].set_title('Markery')
axes[0,1].legend()

# Grubość linii i przezroczystość
axes[0,2].plot(x, y1, linewidth=1, alpha=0.7, label='thin')
axes[0,2].plot(x, y2, linewidth=3, alpha=0.7, label='thick')
axes[0,2].plot(x, y3, linewidth=5, alpha=0.4, label='very thick')
axes[0,2].set_title('Grubość i alpha')
axes[0,2].legend()

# Error bars
axes[1,0].errorbar(x, y1, yerr=0.5, capsize=5, capthick=2, 
                   fmt='o-', label='Z error bars')
axes[1,0].set_title('Error bars')
axes[1,0].legend()

# Wypełnienie między liniami
axes[1,1].plot(x, y1, 'b-', label='Upper')
axes[1,1].plot(x, y1-1, 'r-', label='Lower')
axes[1,1].fill_between(x, y1, y1-1, alpha=0.3, color='green')
axes[1,1].set_title('Fill between')
axes[1,1].legend()

# Subplots with shared axis
axes[1,2].plot(x, y1, 'b-', label='Primary')
ax2 = axes[1,2].twinx()
ax2.plot(x, y3*10, 'r-', label='Secondary')
axes[1,2].set_title('Dual Y-axis')
axes[1,2].legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()
```

---

### 🎯 Customizacja wykresów

```python
# Zaawansowana customizacja
fig, ax = plt.subplots(figsize=(10, 6))

x = np.linspace(0, 4*np.pi, 1000)
y1 = np.sin(x)
y2 = np.cos(x)

# Wykres z customizacją
line1, = ax.plot(x, y1, color='#2E8B57', linewidth=2.5, label='sin(x)')
line2, = ax.plot(x, y2, color='#FF6347', linewidth=2.5, label='cos(x)')

# Osie
ax.set_xlim(0, 4*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Angle (radians)', fontsize=12, fontweight='bold')
ax.set_ylabel('Amplitude', fontsize=12, fontweight='bold')

# Ticks
ax.set_xticks([0, np.pi, 2*np.pi, 3*np.pi, 4*np.pi])
ax.set_xticklabels(['0', 'π', '2π', '3π', '4π'], fontsize=11)
ax.set_yticks([-1, -0.5, 0, 0.5, 1])

# Grid
ax.grid(True, linestyle='--', alpha=0.7, color='gray')
ax.set_axisbelow(True)  # Grid pod wykresem

# Tytuł i legend
ax.set_title('Funkcje trygonometryczne', fontsize=14, fontweight='bold', pad=20)
ax.legend(frameon=True, fancybox=True, shadow=True, fontsize=11)

# Ramki
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(0.5)
ax.spines['bottom'].set_linewidth(0.5)

# Annotations
ax.annotate('Maksimum sin', xy=(np.pi/2, 1), xytext=(np.pi/2, 1.3),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            fontsize=10, ha='center')

plt.tight_layout()
plt.show()
```

---

### 📊 Wykresy z Pandas

```python
# Tworzenie danych testowych
dates = pd.date_range('2023-01-01', periods=365)
df = pd.DataFrame({
    'sprzedaz': np.cumsum(np.random.randn(365)) + 1000,
    'zysk': np.cumsum(np.random.randn(365)) + 200,
    'klienci': np.cumsum(np.random.randint(-5, 15, 365)) + 500
}, index=dates)

# Pandas plotting
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Line plot
df['sprzedaz'].plot(ax=axes[0,0], title='Sprzedaż w czasie', color='blue')
axes[0,0].set_ylabel('Wartość')

# Multiple lines
df[['zysk', 'klienci']].plot(ax=axes[0,1], title='Zysk i Klienci')

# Rolling average
df['sprzedaz'].rolling(30).mean().plot(ax=axes[1,0], 
                                      title='30-dniowa średnia sprzedaży',
                                      color='red', linewidth=2)

# Resample and plot
df.resample('M').mean().plot(ax=axes[1,1], 
                            title='Średnie miesięczne',
                            marker='o')

plt.tight_layout()
plt.show()

# Pandas plot methods
print("Dostępne metody pandas plot:")
print([method for method in dir(df.plot) if not method.startswith('_')])
```

---

### 💾 Zapisywanie wykresów

```python
# Tworzenie wykresu do zapisu
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x), 'b-', linewidth=2)
ax.set_title('Wykres do zapisu')
ax.grid(True, alpha=0.3)

# Różne formaty zapisu
# PNG - dobry dla web, prezentacji
plt.savefig('wykres.png', dpi=300, bbox_inches='tight')

# PDF - dobry dla dokumentów, publikacji
plt.savefig('wykres.pdf', bbox_inches='tight')

# SVG - wektor, dobry dla web
plt.savefig('wykres.svg', bbox_inches='tight')

# Z custom parametrami
plt.savefig('wykres_custom.png', 
           dpi=300,                    # Rozdzielczość
           bbox_inches='tight',        # Obcinanie białych brzegów
           facecolor='white',          # Kolor tła
           edgecolor='none',           # Kolor ramki
           transparent=False)          # Przezroczyste tło

plt.close()  # Zamknięcie figury z pamięci

# Kontekst manager dla automatycznego zamykania
with plt.style.context('seaborn-v0_8'):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 2])
    ax.set_title('Wykres w kontekście')
    plt.savefig('context_plot.png', dpi=150)
```

---

### 🔧 Praktyczne wskazówki

```python
# 1. Memory management dla wielu wykresów
def create_and_save_plot(data, filename):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(data)
    ax.set_title('Sample Plot')
    plt.savefig(filename)
    plt.close(fig)  # Ważne! Zwolnienie pamięci

# 2. Batch plotting
data_sets = [np.random.randn(100) for _ in range(5)]
for i, data in enumerate(data_sets):
    create_and_save_plot(data, f'plot_{i}.png')

# 3. Interactive mode
plt.ion()  # Włączenie trybu interaktywnego
plt.plot([1, 2, 3], [1, 4, 2])
plt.show(block=False)  # Non-blocking show
# plt.ioff()  # Wyłączenie trybu interaktywnego

# 4. Figure i axes reuse
fig, ax = plt.subplots()
for i in range(3):
    ax.clear()  # Czyszczenie axes
    ax.plot(np.random.randn(50))
    ax.set_title(f'Dataset {i+1}')
    plt.pause(0.5)  # Pauza 0.5s
plt.close(fig)

# 5. Custom color cycles
custom_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=custom_colors)

# Test custom colors
fig, ax = plt.subplots()
for i in range(5):
    ax.plot(np.random.randn(50).cumsum(), label=f'Series {i+1}')
ax.legend()
ax.set_title('Custom color cycle')
plt.show()

# Reset do domyślnych
plt.rcdefaults()
```

---

### 🎯 Następny krok

Poznasz **Matplotlib - Wykresy liniowe i punktowe**:

- Scatter plots i customizacja
- Line plots zaawansowane
- Multiple datasets
- Trend lines
- 3D plotting basics