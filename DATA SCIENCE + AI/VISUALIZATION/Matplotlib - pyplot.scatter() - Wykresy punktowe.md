# 🎨 Matplotlib - pyplot.scatter() - Wykresy punktowe

## 📚 Co to jest pyplot.scatter()?

`matplotlib.pyplot.scatter()` to funkcja do tworzenia wykresów punktowych (scatter plots). To jak gwiazdy na niebie - każdy punkt to jedna obserwacja, a razem pokazują wzorce! ⭐

## 🔧 Podstawowa składnia

```python
import matplotlib.pyplot as plt

# Podstawowa składnia
plt.scatter(x, y, s=None, c=None, marker='o', alpha=None, **kwargs)
```

## 💻 Podstawowe przykłady

### 1️⃣ Prosty scatter plot

```python
import matplotlib.pyplot as plt
import numpy as np

# Dane
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [2, 5, 3, 8, 7, 10, 6, 9, 11, 12]

# Prosty scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(x, y)
plt.title('Prosty wykres punktowy')
plt.xlabel('Zmienna X')
plt.ylabel('Zmienna Y')
plt.grid(True, alpha=0.3)
plt.show()

print("Podstawowy scatter plot został wyświetlony!")
```

### 2️⃣ Kolorowe punkty i różne rozmiary

```python
# Więcej danych
n_points = 100
np.random.seed(42)

x = np.random.randn(n_points)
y = np.random.randn(n_points)
colors = np.random.rand(n_points)  # kolory
sizes = 1000 * np.random.rand(n_points)  # rozmiary

plt.figure(figsize=(10, 8))
scatter = plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')

plt.colorbar(scatter, label='Wartość koloru')
plt.title('Scatter plot z kolorami i rozmiarami')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True, alpha=0.3)
plt.show()

print("Kolorowy scatter plot został wyświetlony!")
```

## 🎯 Praktyczne przypadki użycia

### 📊 Analiza korelacji wzrost-waga

```python
# Symulacja danych wzrost-waga
np.random.seed(123)
n_people = 150

# Wzrost (cm) - rozkład normalny
wzrost = np.random.normal(175, 15, n_people)
wzrost = np.clip(wzrost, 150, 200)  # ograniczenie do realistycznego zakresu

# Waga zależy od wzrostu + losowość
waga = (wzrost - 100) * 0.8 + np.random.normal(0, 10, n_people)
waga = np.clip(waga, 45, 120)

# Płeć wpływa na rozkład
plec = np.random.choice(['M', 'K'], n_people)
# Mężczyźni średnio wyżsi i ciężsi
wzrost[plec == 'M'] += 8
waga[plec == 'M'] += 5

plt.figure(figsize=(12, 8))

# Różne kolory dla płci
for p, kolor, label in [('M', 'blue', 'Mężczyźni'), ('K', 'red', 'Kobiety')]:
    mask = plec == p
    plt.scatter(wzrost[mask], waga[mask], 
               c=kolor, alpha=0.6, s=50, label=label)

plt.xlabel('Wzrost (cm)', fontsize=12)
plt.ylabel('Waga (kg)', fontsize=12)
plt.title('Relacja wzrost-waga w zależności od płci', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)

# Dodaj linię trendu
z = np.polyfit(wzrost, waga, 1)  # linia liniowa
p = np.poly1d(z)
plt.plot(wzrost, p(wzrost), "--", color='gray', alpha=0.8, 
         label=f'Trend: y = {z[0]:.2f}x + {z[1]:.1f}')
plt.legend()

plt.tight_layout()
plt.show()

# Korelacja
correlation = np.corrcoef(wzrost, waga)[0, 1]
print(f"Korelacja wzrost-waga: {correlation:.3f}")
```

### 💰 Analiza cena vs jakość produktów

```python
# Dane produktów
np.random.seed(456)
n_products = 200

# Różne kategorie produktów
kategorie = ['Elektronika', 'Odzież', 'Dom', 'Sport']
kategoria = np.random.choice(kategorie, n_products)

# Cena zależy od kategorii
cena_base = {'Elektronika': 500, 'Odzież': 100, 'Dom': 200, 'Sport': 150}
ceny = []
jakosci = []

for kat in kategoria:
    base_price = cena_base[kat]
    cena = np.random.exponential(base_price/2) + base_price/3
    # Jakość koreluje z ceną, ale z szumem
    jakosc = min(10, max(1, (cena - base_price/3) / (base_price/2) * 5 + 
                            np.random.normal(0, 1.5) + 5))
    ceny.append(cena)
    jakosci.append(jakosc)

ceny = np.array(ceny)
jakosci = np.array(jakosci)

plt.figure(figsize=(14, 10))

# Różne kolory i markery dla kategorii
colors = {'Elektronika': 'blue', 'Odzież': 'red', 'Dom': 'green', 'Sport': 'orange'}
markers = {'Elektronika': 'o', 'Odzież': 's', 'Dom': '^', 'Sport': 'D'}

for kat in kategorie:
    mask = kategoria == kat
    plt.scatter(ceny[mask], jakosci[mask], 
               c=colors[kat], marker=markers[kat], 
               alpha=0.7, s=60, label=kat)

plt.xlabel('Cena (PLN)', fontsize=12)
plt.ylabel('Ocena jakości (1-10)', fontsize=12)
plt.title('Relacja cena-jakość różnych kategorii produktów', fontsize=14)
plt.legend(title='Kategoria', fontsize=10)
plt.grid(True, alpha=0.3)

# Dodaj linie średnich dla każdej kategorii
for kat in kategorie:
    mask = kategoria == kat
    if np.sum(mask) > 1:
        z = np.polyfit(ceny[mask], jakosci[mask], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(ceny[mask].min(), ceny[mask].max(), 100)
        plt.plot(x_trend, p(x_trend), '--', color=colors[kat], alpha=0.5, linewidth=2)

plt.tight_layout()
plt.show()

# Korelacje per kategoria
print("Korelacja cena-jakość per kategoria:")
for kat in kategorie:
    mask = kategoria == kat
    if np.sum(mask) > 1:
        corr = np.corrcoef(ceny[mask], jakosci[mask])[0, 1]
        avg_price = np.mean(ceny[mask])
        avg_quality = np.mean(jakosci[mask])
        print(f"{kat:12}: r={corr:+.3f}, średnia cena: {avg_price:5.0f} PLN, średnia jakość: {avg_quality:.1f}")
```

### 🏠 Analiza rynku nieruchomości

```python
# Symulacja danych o mieszkaniach
np.random.seed(789)
n_apartments = 300

# Powierzchnia mieszkań
powierzchnia = np.random.gamma(2, 25)  # rozkład gamma - realistyczny dla mieszkań
powierzchnia = np.clip(powierzchnia, 25, 150)

# Cena zależy od powierzchni, lokalizacji, wieku
lokalizacja = np.random.choice(['Centrum', 'Śródmieście', 'Przedmieścia', 'Peryferie'], n_apartments,
                               p=[0.15, 0.25, 0.35, 0.25])
wiek_budynku = np.random.randint(0, 50, n_apartments)

# Cena za m2 zależy od lokalizacji
cena_m2_base = {'Centrum': 12000, 'Śródmieście': 8000, 'Przedmieścia': 6000, 'Peryferie': 4000}

ceny = []
for i in range(n_apartments):
    lok = lokalizacja[i]
    base = cena_m2_base[lok]
    # Cena maleje z wiekiem budynku
    age_factor = 1 - (wiek_budynku[i] / 100)  # max -50%
    # Dodaj losowość
    noise_factor = np.random.normal(1, 0.2)
    cena_m2 = base * age_factor * noise_factor
    cena_total = cena_m2 * powierzchnia[i]
    ceny.append(cena_total)

ceny = np.array(ceny)

plt.figure(figsize=(15, 10))

# Subplot dla różnych analiz
plt.subplot(2, 2, 1)
# Powierzchnia vs Cena, kolorowane według lokalizacji
loc_colors = {'Centrum': 'red', 'Śródmieście': 'orange', 'Przedmieścia': 'green', 'Peryferie': 'blue'}
for lok in np.unique(lokalizacja):
    mask = lokalizacja == lok
    plt.scatter(powierzchnia[mask], ceny[mask], 
               c=loc_colors[lok], alpha=0.6, s=30, label=lok)
plt.xlabel('Powierzchnia (m²)')
plt.ylabel('Cena (PLN)')
plt.title('Powierzchnia vs Cena')
plt.legend(title='Lokalizacja', fontsize=8)
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 2)
# Wiek vs Cena za m2, rozmiar = powierzchnia
cena_m2 = ceny / powierzchnia
plt.scatter(wiek_budynku, cena_m2, s=powierzchnia*2, alpha=0.5, c='purple')
plt.xlabel('Wiek budynku (lata)')
plt.ylabel('Cena za m² (PLN)')
plt.title('Wiek vs Cena/m² (rozmiar = powierzchnia)')
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 3)
# Histogram cen według lokalizacji
for lok in np.unique(lokalizacja):
    mask = lokalizacja == lok
    plt.scatter(np.random.normal(0, 0.1, np.sum(mask)), ceny[mask]/1000, 
               c=loc_colors[lok], alpha=0.6, s=20, label=lok)
plt.ylabel('Cena (tys. PLN)')
plt.title('Rozkład cen według lokalizacji')
plt.xticks([])
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 4)
# Cena vs powierzchnia z regresją
plt.scatter(powierzchnia, ceny/1000, alpha=0.5, c='gray', s=20)
# Linia trendu
z = np.polyfit(powierzchnia, ceny/1000, 1)
p = np.poly1d(z)
plt.plot(powierzchnia, p(powierzchnia), "r--", alpha=0.8, linewidth=2)
plt.xlabel('Powierzchnia (m²)')
plt.ylabel('Cena (tys. PLN)')
plt.title(f'Trend: {z[0]:.1f} tys.PLN/m² + {z[1]:.0f} tys.PLN')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Statystyki
print("=== ANALIZA RYNKU MIESZKAŃ ===")
print(f"Liczba mieszkań: {n_apartments}")
print(f"Średnia powierzchnia: {np.mean(powierzchnia):.1f} m²")
print(f"Średnia cena: {np.mean(ceny):,.0f} PLN")
print(f"Średnia cena za m²: {np.mean(cena_m2):,.0f} PLN/m²")

print(f"\nStatystyki według lokalizacji:")
for lok in np.unique(lokalizacja):
    mask = lokalizacja == lok
    avg_price = np.mean(ceny[mask])
    avg_m2 = np.mean(powierzchnia[mask])
    avg_price_m2 = np.mean(cena_m2[mask])
    count = np.sum(mask)
    print(f"{lok:15}: {count:3} mieszkań, {avg_m2:4.1f}m², {avg_price:7.0f} PLN ({avg_price_m2:5.0f} PLN/m²)")
```

## 🔍 Zaawansowane opcje

### 1️⃣ Różne markery i style

```python
# Demonstracja różnych markerów
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Różne markery
markery = ['o', 's', '^', 'v', '<', '>', 'D', 'p', '*', 'h', '+', 'x']
x_demo = range(len(markery))
y_demo = np.random.rand(len(markery)) * 10

axes[0,0].scatter(x_demo, y_demo, s=100, c=y_demo, cmap='viridis')
for i, marker in enumerate(markery):
    axes[0,0].scatter(i, y_demo[i], s=200, marker=marker, c='red', alpha=0.7)
axes[0,0].set_title('Różne markery')
axes[0,0].set_xticks(x_demo)
axes[0,0].set_xticklabels(markery)

# Różne rozmiary
sizes = [20, 50, 100, 200, 500, 1000]
axes[0,1].scatter(range(len(sizes)), [5]*len(sizes), s=sizes, alpha=0.6)
axes[0,1].set_title('Różne rozmiary')
axes[0,1].set_ylim(0, 10)

# Różne alpha (przezroczystość)
alphas = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
for i, alpha in enumerate(alphas):
    axes[1,0].scatter([i], [5], s=200, alpha=alpha, c='blue')
axes[1,0].set_title('Różne alpha (przezroczystość)')
axes[1,0].set_ylim(0, 10)

# Edgecolors i facecolors
axes[1,1].scatter([0, 1, 2], [5, 5, 5], s=200, 
                 facecolors=['red', 'none', 'blue'],
                 edgecolors=['black', 'red', 'black'],
                 linewidth=3)
axes[1,1].set_title('Edge colors i face colors')
axes[1,1].set_ylim(0, 10)

plt.tight_layout()
plt.show()
```

## ⚠️ Uwagi i best practices

### ✅ Dobre praktyki

```python
# 1. Zawsze dodawaj opisy
plt.scatter(x, y)
plt.xlabel('Zmienna X')
plt.ylabel('Zmienna Y')
plt.title('Opisowy tytuł')

# 2. Użyj alpha dla nakładających się punktów
plt.scatter(x, y, alpha=0.6)

# 3. Colorbar dla kolorowych danych
scatter = plt.scatter(x, y, c=colors, s=sizes)
plt.colorbar(scatter, label='Opis koloru')

# 4. Grid dla łatwiejszego odczytywania
plt.grid(True, alpha=0.3)
```

### ❌ Unikaj

```python
# Nie rób za dużo punktów bez alpha
# plt.scatter(huge_x, huge_y, s=100)  # Nieczytelne!

# Nie używaj za małych punktów
# plt.scatter(x, y, s=1)  # Niewidoczne!

# Nie zapominaj o opisach
# plt.scatter(x, y)  # Co to przedstawia?
```

## 📝 Podsumowanie

`pyplot.scatter()` to idealne narzędzie do analizy relacji:

- 🎯 Pokazuje korelacje między zmiennymi
- 🎨 Kolory (`c=`) dla trzeciego wymiaru
- 📏 Rozmiary (`s=`) dla czwartego wymiaru  
- 🔍 `alpha=` dla przezroczystości nakładających się punktów
- 📊 Idealne do eksploracji danych i znajdowania wzorców
- 🌈 `cmap=` dla map kolorów
- ✨ Podstawa dla wielu analiz statystycznych

To jak gwiazdy na niebie danych - razem tworzą konstelacje znaczeń! ⭐🌌