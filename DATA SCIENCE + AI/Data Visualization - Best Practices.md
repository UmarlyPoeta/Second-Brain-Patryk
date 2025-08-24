## 📊 Data Visualization - Best Practices

_Zasady efektywnej wizualizacji danych_

---

### 📝 Wprowadzenie do Data Visualization

**Dobra wizualizacja danych** powinna:

1. **Przekazywać** jasny przekaz
2. **Minimalizować** cognitive load
3. **Maksymalizować** data-to-ink ratio
4. **Wybierać** odpowiedni typ wykresu
5. **Używać** konsystentnego stylu

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Konfiguracja
plt.style.use('default')
sns.set_palette("husl")
```

---

### 🎨 Wybór typu wykresu

```python
# Przykładowe dane
np.random.seed(42)
sales_data = pd.DataFrame({
    'month': pd.date_range('2023-01-01', periods=12, freq='M'),
    'sales': [100, 120, 115, 140, 155, 180, 175, 165, 185, 200, 210, 220],
    'category': ['Electronics', 'Clothing', 'Books', 'Home', 'Electronics', 
                'Clothing', 'Books', 'Home', 'Electronics', 'Clothing', 'Books', 'Home'],
    'region': ['North', 'South', 'East', 'West'] * 3,
    'profit_margin': np.random.uniform(0.1, 0.3, 12)
})

customer_data = pd.DataFrame({
    'age': np.random.normal(40, 12, 1000),
    'income': np.random.lognormal(10, 0.5, 1000),
    'satisfaction': np.random.randint(1, 6, 1000),
    'segment': np.random.choice(['A', 'B', 'C'], 1000, p=[0.3, 0.5, 0.2])
})

print("=== WYBÓR TYPU WYKRESU ===")

# Guide dla wyboru wykresu
chart_selection_guide = """
🎯 PRZEWODNIK WYBORU WYKRESU

📈 TRENDS OVER TIME:
• Line Chart → continuous time series
• Area Chart → cumulative values
• Bar Chart → discrete time periods

📊 COMPARISONS:
• Bar Chart → categorical comparisons
• Horizontal Bar → many categories/long names
• Grouped Bar → multiple series comparison

🥧 COMPOSITION:
• Pie Chart → parts of whole (< 6 categories)
• Stacked Bar → composition + comparison
• Treemap → hierarchical composition

📉 DISTRIBUTION:
• Histogram → single variable distribution
• Box Plot → distribution with outliers
• Violin Plot → distribution shape

🔗 RELATIONSHIPS:
• Scatter Plot → correlation between variables
• Bubble Chart → 3+ dimensions
• Heatmap → correlation matrix

🗺️ SPATIAL DATA:
• Maps → geographical data
• Choropleth → regional comparisons
"""

print(chart_selection_guide)

# Demonstracja różnych typów wykresów
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Line Chart - trends over time
axes[0, 0].plot(sales_data['month'], sales_data['sales'], marker='o', linewidth=2)
axes[0, 0].set_title('Trend sprzedaży w czasie')
axes[0, 0].set_xlabel('Miesiąc')
axes[0, 0].set_ylabel('Sprzedaż')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Bar Chart - categorical comparison
category_sales = sales_data.groupby('category')['sales'].sum()
axes[0, 1].bar(category_sales.index, category_sales.values, color=sns.color_palette("husl", len(category_sales)))
axes[0, 1].set_title('Sprzedaż według kategorii')
axes[0, 1].set_xlabel('Kategoria')
axes[0, 1].set_ylabel('Sprzedaż')

# 3. Scatter Plot - relationships
axes[0, 2].scatter(customer_data['age'], customer_data['income'], alpha=0.6, s=30)
axes[0, 2].set_title('Wiek vs Dochód')
axes[0, 2].set_xlabel('Wiek')
axes[0, 2].set_ylabel('Dochód')

# 4. Histogram - distribution
axes[1, 0].hist(customer_data['age'], bins=30, alpha=0.7, edgecolor='black')
axes[1, 0].set_title('Rozkład wieku klientów')
axes[1, 0].set_xlabel('Wiek')
axes[1, 0].set_ylabel('Częstość')

# 5. Box Plot - distribution comparison
segment_satisfaction = [customer_data[customer_data['segment'] == seg]['satisfaction'] 
                       for seg in ['A', 'B', 'C']]
axes[1, 1].boxplot(segment_satisfaction, labels=['A', 'B', 'C'])
axes[1, 1].set_title('Satysfakcja według segmentu')
axes[1, 1].set_xlabel('Segment')
axes[1, 1].set_ylabel('Satysfakcja')

# 6. Heatmap - correlation matrix
numeric_cols = customer_data.select_dtypes(include=[np.number])
corr_matrix = numeric_cols.corr()
im = axes[1, 2].imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
axes[1, 2].set_title('Macierz korelacji')
axes[1, 2].set_xticks(range(len(corr_matrix.columns)))
axes[1, 2].set_yticks(range(len(corr_matrix.columns)))
axes[1, 2].set_xticklabels(corr_matrix.columns, rotation=45)
axes[1, 2].set_yticklabels(corr_matrix.columns)

# Dodanie colorbar
plt.colorbar(im, ax=axes[1, 2])

plt.tight_layout()
plt.show()
```

---

### 🎨 Teoria kolorów

```python
print("=== TEORIA KOLORÓW W DATA SCIENCE ===")

# Demonstracja różnych palet kolorów
color_theory = """
🌈 TEORIA KOLORÓW

🎯 TYPY PALET:
• Sequential → uporządkowane dane (light → dark)
• Diverging → dane z punktem centralnym (-/+ od zera)
• Qualitative → kategorie nominalne (distinct colors)

🔍 DOSTĘPNOŚĆ:
• Colorblind-friendly palettes
• High contrast ratios
• Avoid red/green combinations only

💡 PSYCHOLOGIA KOLORÓW:
• Czerwony → uwaga, niebezpieczeństwo, spadek
• Zielony → pozytyw, wzrost, sukces
• Niebieski → spokój, zaufanie, stabilność
• Pomarańczowy → energia, ostrzeżenie
"""

print(color_theory)

# Porównanie palet kolorów
fig, axes = plt.subplots(3, 2, figsize=(15, 12))

# Dane testowe
x = np.linspace(0, 10, 100)
data_matrix = np.random.rand(10, 10)
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

# Sequential palette
cmap_seq = plt.cm.Blues
axes[0, 0].imshow(data_matrix, cmap=cmap_seq)
axes[0, 0].set_title('Sequential Palette (Blues)')

# Diverging palette  
data_diverging = np.random.randn(10, 10)
axes[0, 1].imshow(data_diverging, cmap='RdBu_r', vmin=-2, vmax=2)
axes[0, 1].set_title('Diverging Palette (RdBu)')

# Qualitative palette - good
colors_good = plt.cm.Set2(np.linspace(0, 1, len(categories)))
axes[1, 0].bar(categories, values, color=colors_good)
axes[1, 0].set_title('✅ Good Qualitative (Set2)')

# Qualitative palette - bad (rainbow)
colors_bad = plt.cm.rainbow(np.linspace(0, 1, len(categories)))
axes[1, 1].bar(categories, values, color=colors_bad)
axes[1, 1].set_title('❌ Bad Qualitative (Rainbow)')

# Colorblind-friendly
colors_cb = sns.color_palette("colorblind", len(categories))
axes[2, 0].bar(categories, values, color=colors_cb)
axes[2, 0].set_title('✅ Colorblind-friendly')

# Accessibility test - contrast
# Symulacja protanopia (red-blind)
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
original_colors = plt.cm.Set1(np.linspace(0, 1, len(categories)))

axes[2, 1].bar(categories, values, color=original_colors)
axes[2, 1].set_title('Original vs Protanopia View')

plt.tight_layout()
plt.show()

# Demonstracja wpływu kolorów na percepcję
print("\n📊 WPŁYW KOLORÓW NA PERCEPCJĘ:")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Te same dane, różne kolory
profit_data = [15, 25, -10, 30, -5]
quarters = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']

# Neutralne kolory
axes[0].bar(quarters, profit_data, color='steelblue')
axes[0].set_title('Neutralne kolory')
axes[0].set_ylabel('Zysk (%)')
axes[0].axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# Semantyczne kolory (green = pozytywne, red = negatywne)
bar_colors = ['green' if x > 0 else 'red' for x in profit_data]
axes[1].bar(quarters, profit_data, color=bar_colors)
axes[1].set_title('Semantyczne kolory')
axes[1].set_ylabel('Zysk (%)')
axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# Gradient based on value
norm = plt.Normalize(vmin=min(profit_data), vmax=max(profit_data))
colors = plt.cm.RdYlGn(norm(profit_data))
axes[2].bar(quarters, profit_data, color=colors)
axes[2].set_title('Gradient kolorów')
axes[2].set_ylabel('Zysk (%)')
axes[2].axhline(y=0, color='black', linestyle='-', linewidth=0.5)

plt.tight_layout()
plt.show()
```

---

### 📏 Zasady designu

```python
print("=== ZASADY DESIGNU WYKRESÓW ===")

design_principles = """
📏 ZASADY DESIGNU

✨ CLARITY (Przejrzystość):
• Jeden główny message per wykres
• Usuń chart junk (zbędne elementy)
• Użyj white space effectively
• Clear and descriptive titles

📐 DATA-INK RATIO:
• Maximize data, minimize ink
• Remove unnecessary grid lines
• Simplify axes and legends
• Focus on the data story

🎯 ACCESSIBILITY:
• Readable font sizes (min 10pt)
• High contrast colors
• Alternative text descriptions
• Colorblind considerations

📱 RESPONSIVE DESIGN:
• Scale appropriately
• Consider mobile viewing
• Maintain readability at all sizes
"""

print(design_principles)

# Demonstracja good vs bad design
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Bad design example
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
sales = [100, 120, 115, 140, 155, 180]

# BAD: Chart junk, poor colors, cluttered
axes[0, 0].bar(months, sales, color='red', edgecolor='blue', linewidth=3)
axes[0, 0].grid(True, linestyle='-', linewidth=2, alpha=0.8)
axes[0, 0].set_title('!!!SALES DATA!!! VERY IMPORTANT!!!', fontsize=16, color='red')
axes[0, 0].set_ylabel('Sales ($$$)', fontsize=14, color='purple')
axes[0, 0].set_xlabel('Month (2023)', fontsize=14, color='orange')
# Dodanie zbędnych elementów
for i, v in enumerate(sales):
    axes[0, 0].text(i, v + 5, f'${v}K', ha='center', fontsize=12, color='green', fontweight='bold')
axes[0, 0].set_facecolor('lightgray')

# GOOD: Clean, clear, focused
axes[0, 1].bar(months, sales, color='steelblue', alpha=0.8)
axes[0, 1].grid(True, linestyle='-', alpha=0.3, axis='y')
axes[0, 1].set_title('Monthly Sales Growth', fontsize=12, pad=20)
axes[0, 1].set_ylabel('Sales (thousands $)')
axes[0, 1].spines['top'].set_visible(False)
axes[0, 1].spines['right'].set_visible(False)

# Subplot titles
axes[0, 0].text(0.5, -0.15, '❌ BAD DESIGN', transform=axes[0, 0].transAxes, 
                ha='center', va='top', fontsize=14, color='red', fontweight='bold')
axes[0, 1].text(0.5, -0.15, '✅ GOOD DESIGN', transform=axes[0, 1].transAxes,
                ha='center', va='top', fontsize=14, color='green', fontweight='bold')

# Font size demonstration
text_sizes = [8, 10, 12, 14, 16, 18]
y_positions = np.arange(len(text_sizes))

axes[1, 0].barh(y_positions, [1]*len(text_sizes), color='lightblue')
for i, size in enumerate(text_sizes):
    axes[1, 0].text(0.5, i, f'Font size {size}pt', fontsize=size, 
                    ha='center', va='center')
axes[1, 0].set_title('Font Size Readability')
axes[1, 0].set_yticks(y_positions)
axes[1, 0].set_yticklabels([f'{s}pt' for s in text_sizes])
axes[1, 0].set_xlim(0, 1)

# Aspect ratio demonstration
x_data = np.linspace(0, 10, 100)
y_data = np.sin(x_data) * 2 + 5

axes[1, 1].plot(x_data, y_data, linewidth=2)
axes[1, 1].set_title('Proper Aspect Ratio')
axes[1, 1].set_xlabel('Time')
axes[1, 1].set_ylabel('Value')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Przykład progressive disclosure
print("\n📊 PROGRESSIVE DISCLOSURE:")

# Overview → Details on Demand
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Level 1: High-level overview
quarterly_sales = [500, 650, 720, 800]
quarters = ['Q1', 'Q2', 'Q3', 'Q4']

axes[0].plot(quarters, quarterly_sales, marker='o', linewidth=3, markersize=8)
axes[0].set_title('Level 1: Quarterly Overview', fontsize=14)
axes[0].set_ylabel('Sales (thousands $)')
axes[0].grid(True, alpha=0.3)

# Level 2: Monthly breakdown
months_q3 = ['Jul', 'Aug', 'Sep']
monthly_q3 = [220, 250, 250]

axes[1].bar(months_q3, monthly_q3, color='orange', alpha=0.7)
axes[1].set_title('Level 2: Q3 Monthly Detail', fontsize=14)
axes[1].set_ylabel('Sales (thousands $)')

# Level 3: Daily detail for August
days_aug = list(range(1, 31))
daily_aug = np.random.normal(250/30, 5, 30).cumsum()

axes[2].plot(days_aug, daily_aug, alpha=0.7)
axes[2].set_title('Level 3: August Daily Detail', fontsize=14)
axes[2].set_xlabel('Day of Month')
axes[2].set_ylabel('Cumulative Sales')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

### 📱 Interactive Visualizations

```python
print("=== INTERACTIVE VISUALIZATIONS ===")

# Przykłady z Plotly (interactive)
interactive_benefits = """
📱 KORZYŚCI Z INTERAKTYWNYCH WIZUALIZACJI

🔍 EXPLORABILITY:
• Zoom in/out dla szczegółów
• Pan across data ranges
• Filter i hover informacje
• Drill-down capabilities

👤 USER ENGAGEMENT:
• Higher attention time
• Better data comprehension
• Self-service analytics
• Personalized views

📊 COMPLEX DATA:
• Multiple dimensions
• Large datasets
• Real-time updates
• Cross-filtering
"""

print(interactive_benefits)

# Plotly examples (kod do uruchomienia w Jupyter)
plotly_examples = '''
# 1. Interactive Scatter Plot
fig = px.scatter(customer_data, x='age', y='income', 
                color='segment', size='satisfaction',
                hover_data=['satisfaction'],
                title='Interactive Customer Analysis')
fig.show()

# 2. Interactive Time Series
time_series_data = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=365),
    'value': np.cumsum(np.random.randn(365)) + 100
})

fig = px.line(time_series_data, x='date', y='value',
             title='Interactive Time Series')
fig.add_hline(y=100, line_dash="dash", line_color="red")
fig.show()

# 3. Interactive Dashboard
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Sales Trend', 'Category Distribution', 
                   'Regional Performance', 'Correlation Matrix'),
    specs=[[{"secondary_y": False}, {"type": "pie"}],
           [{"colspan": 2}, None]]
)

# Sales trend
fig.add_trace(go.Scatter(x=sales_data['month'], y=sales_data['sales'],
                        mode='lines+markers', name='Sales'),
              row=1, col=1)

# Pie chart
fig.add_trace(go.Pie(labels=category_sales.index, values=category_sales.values,
                    name="Categories"), row=1, col=2)

# Regional heatmap
region_category = sales_data.pivot_table(values='sales', 
                                        index='region', columns='category')
fig.add_trace(go.Heatmap(z=region_category.values,
                        x=region_category.columns,
                        y=region_category.index,
                        colorscale='Viridis'),
              row=2, col=1)

fig.update_layout(height=800, showlegend=False,
                 title_text="Sales Dashboard")
fig.show()
'''

print("💻 PLOTLY EXAMPLES (run in Jupyter):")
print(plotly_examples)

# Alternatywa: matplotlib z widgets (basic interactivity)
print("\n🎮 MATPLOTLIB INTERACTIVE EXAMPLE:")

# Prosty przykład z suwakami (wymaga widget backend)
matplotlib_interactive = '''
%matplotlib widget
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# Create figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

# Initial parameters
freq = 1.0
amp = 1.0

# Data
t = np.linspace(0, 2*np.pi, 1000)
s = amp * np.sin(freq * t)
line, = ax.plot(t, s)

ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-2, 2)

# Sliders
ax_freq = plt.axes([0.25, 0.1, 0.5, 0.03])
ax_amp = plt.axes([0.25, 0.05, 0.5, 0.03])

slider_freq = Slider(ax_freq, 'Frequency', 0.1, 5.0, valinit=freq)
slider_amp = Slider(ax_amp, 'Amplitude', 0.1, 2.0, valinit=amp)

def update(val):
    freq = slider_freq.val
    amp = slider_amp.val
    line.set_ydata(amp * np.sin(freq * t))
    fig.canvas.draw()

slider_freq.on_changed(update)
slider_amp.on_changed(update)

plt.show()
'''

print(matplotlib_interactive)
```

---

### 📊 Dashboard Design

```python
print("=== DASHBOARD DESIGN PRINCIPLES ===")

dashboard_principles = """
🎯 DASHBOARD DESIGN PRINCIPLES

📐 LAYOUT HIERARCHY:
• Most important metrics at top-left
• Group related information together
• Use consistent spacing and alignment
• Progressive disclosure for details

🏷️ INFORMATION DENSITY:
• Avoid cognitive overload
• 5±2 rule for main metrics
• White space is your friend
• Prioritize key insights

🎨 VISUAL CONSISTENCY:
• Consistent color scheme
• Uniform chart types for similar data
• Standard fonts and sizes
• Aligned elements

⚡ PERFORMANCE:
• Fast loading times (< 3 seconds)
• Real-time updates when needed
• Responsive design
• Progressive loading for large datasets

👤 USER EXPERIENCE:
• Clear navigation
• Intuitive interactions
• Mobile-friendly design
• Accessible to all users
"""

print(dashboard_principles)

# Dashboard mockup using matplotlib
fig = plt.figure(figsize=(16, 12))

# Define grid for dashboard layout
gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)

# Title
fig.suptitle('Sales Performance Dashboard', fontsize=20, fontweight='bold', y=0.95)

# KPI Cards (top row)
kpis = [
    ('Total Revenue', '$1.2M', '+15%', 'green'),
    ('Active Customers', '15.2K', '+8%', 'blue'),
    ('Avg Order Value', '$185', '-2%', 'red'),
    ('Conversion Rate', '3.2%', '+12%', 'green')
]

for i, (title, value, change, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.text(0.5, 0.7, value, ha='center', va='center', fontsize=24, fontweight='bold')
    ax.text(0.5, 0.4, title, ha='center', va='center', fontsize=12)
    ax.text(0.5, 0.2, change, ha='center', va='center', fontsize=14, 
            color=color, fontweight='bold')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    # Add subtle border
    ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, fill=False, edgecolor='lightgray'))

# Main chart - Sales trend (spans 2 columns)
ax_main = fig.add_subplot(gs[1:3, 0:2])
months = pd.date_range('2023-01-01', periods=12, freq='M')
sales_trend = [100, 120, 115, 140, 155, 180, 175, 165, 185, 200, 210, 220]
ax_main.plot(months, sales_trend, linewidth=3, marker='o', markersize=6, color='steelblue')
ax_main.set_title('Sales Trend (2023)', fontsize=14, fontweight='bold', pad=20)
ax_main.grid(True, alpha=0.3)
ax_main.spines['top'].set_visible(False)
ax_main.spines['right'].set_visible(False)

# Category breakdown (pie chart)
ax_pie = fig.add_subplot(gs[1, 2:4])
categories = ['Electronics', 'Clothing', 'Books', 'Home']
sizes = [35, 30, 20, 15]
colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
ax_pie.pie(sizes, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
ax_pie.set_title('Sales by Category', fontsize=14, fontweight='bold')

# Regional performance (bar chart)
ax_bar = fig.add_subplot(gs[2, 2:4])
regions = ['North', 'South', 'East', 'West']
performance = [85, 92, 78, 88]
bars = ax_bar.bar(regions, performance, color='lightcoral', alpha=0.7)
ax_bar.set_title('Regional Performance Score', fontsize=14, fontweight='bold')
ax_bar.set_ylim(0, 100)
ax_bar.spines['top'].set_visible(False)
ax_bar.spines['right'].set_visible(False)
# Add value labels on bars
for bar, value in zip(bars, performance):
    ax_bar.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{value}%', ha='center', va='bottom')

# Recent transactions table (mockup)
ax_table = fig.add_subplot(gs[3, :])
ax_table.axis('tight')
ax_table.axis('off')

table_data = [
    ['Order ID', 'Customer', 'Amount', 'Status'],
    ['#12345', 'John Doe', '$234.50', 'Completed'],
    ['#12346', 'Jane Smith', '$156.30', 'Processing'],
    ['#12347', 'Bob Johnson', '$89.99', 'Shipped'],
    ['#12348', 'Alice Brown', '$445.20', 'Completed']
]

table = ax_table.table(cellText=table_data, cellLoc='center', loc='center',
                      colWidths=[0.2, 0.3, 0.2, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Style table header
for i in range(len(table_data[0])):
    table[(0, i)].set_facecolor('#4CAF50')
    table[(0, i)].set_text_props(weight='bold', color='white')

ax_table.set_title('Recent Transactions', fontsize=14, fontweight='bold', pad=20)

plt.show()

# Dashboard checklist
dashboard_checklist = """
✅ DASHBOARD CHECKLIST

📊 CONTENT:
□ Key metrics clearly visible
□ Logical information hierarchy  
□ Relevant time periods shown
□ Actionable insights highlighted

🎨 DESIGN:
□ Consistent color scheme
□ Appropriate chart types
□ Clean, uncluttered layout
□ Professional appearance

🔧 FUNCTIONALITY:
□ Fast loading performance
□ Mobile responsive
□ Interactive elements work
□ Data refreshes properly

👤 USER TESTING:
□ Intuitive navigation
□ Clear call-to-actions
□ Accessible to all users
□ Feedback incorporated
"""

print(dashboard_checklist)
```

---

### 💡 Best Practices Summary

```python
def visualization_best_practices_summary():
    """Podsumowanie najlepszych praktyk wizualizacji"""
    
    summary = """
    ✅ DATA VISUALIZATION BEST PRACTICES
    
    🎯 STRATEGIA:
    1. Zdefiniuj cel wizualizacji
    2. Poznaj swoją publiczność
    3. Wybierz odpowiedni typ wykresu
    4. Skoncentruj się na głównym przekazie
    5. Testuj z prawdziwymi użytkownikami
    
    🎨 DESIGN:
    1. Używaj consistent color schemes
    2. Maksymalizuj data-to-ink ratio
    3. Zapewnij accessibility (colorblind, contrast)
    4. Stosuj progressive disclosure
    5. Maintain visual hierarchy
    
    📊 TECHNICAL:
    1. Choose appropriate scales and axes
    2. Label everything clearly
    3. Provide context and baselines
    4. Handle missing data transparently
    5. Optimize for performance
    
    📱 USER EXPERIENCE:
    1. Make it interactive when beneficial
    2. Ensure mobile compatibility
    3. Provide clear navigation
    4. Enable data export/sharing
    5. Include help/documentation
    
    ⚠️  UNIKAJ:
    • Chart junk i zbędnych elementów
    • Misleading scales (truncated axes)
    • Too many colors or patterns
    • 3D effects bez potrzeby
    • Rainbow color schemes
    • Pie charts z >6 kategoriami
    • Dual y-axes bez jasnego powodu
    """
    
    print(summary)

visualization_best_practices_summary()
```

---

### 🎯 Następny krok

Poznasz **Pandas - Time Series Analysis**:

- Working with datetime data
- Resampling and frequency conversion
- Rolling windows and seasonal decomposition
- Time zone handling
- Advanced time series operations