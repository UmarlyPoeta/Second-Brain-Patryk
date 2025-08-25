# 📊 Matplotlib - pyplot.plot() - Podstawowe wykresy liniowe

## 📚 Co to jest pyplot.plot()?

`matplotlib.pyplot.plot()` to podstawowa funkcja do tworzenia wykresów liniowych w Pythonie. To jak ołówek dla matematyka - najprostsze i najważniejsze narzędzie do rysowania danych! ✏️📈

## 🔧 Podstawowa składnia

```python
import matplotlib.pyplot as plt

# Podstawowa składnia
plt.plot(x, y, format_string, **kwargs)
plt.plot(y)  # x będzie automatycznie 0,1,2,3...
```

## 💻 Praktyczne przykłady

### 1️⃣ Pierwszy prosty wykres

```python
import matplotlib.pyplot as plt
import numpy as np

# Dane
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Prosty wykres
plt.plot(x, y)
plt.title('Mój pierwszy wykres')
plt.xlabel('Oś X')
plt.ylabel('Oś Y')
plt.show()

print("Wykres liniowy został wyświetlony!")
```

### 2️⃣ Różne style linii i kolory

```python
# Dane przykładowe
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.cos(x)

# Różne style
plt.figure(figsize=(10, 6))

# Linia ciągła, niebieska, grube
plt.plot(x, y1, 'b-', linewidth=2, label='sin(x)')

# Linia przerywana, czerwona, kropki
plt.plot(x, y2, 'r--', linewidth=2, label='cos(x)')

# Linia kropkowana, zielona, cienka
plt.plot(x, y3, 'g:', linewidth=1, label='sin(x)*cos(x)')

plt.title('Różne style linii')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()  # pokaż legendę
plt.grid(True)  # dodaj siatkę
plt.show()

print("Wykres z różnymi stylami został wyświetlony!")
```

### 3️⃣ Markery i punkty

```python
# Dane
x = range(10)
y = [i**2 for i in x]

plt.figure(figsize=(8, 6))

# Tylko punkty
plt.plot(x, y, 'o', markersize=8, label='Punkty')

# Linia z punktami
plt.plot(x, [i**1.5 for i in x], 'ro-', linewidth=2, 
         markersize=6, label='Linia z punktami')

# Różne markery
markery = ['s', '^', 'v', '<', '>', 'D', 'p', '*']
for i, marker in enumerate(markery[:8]):
    plt.plot(i, i**2.5, marker, markersize=10, 
             color=plt.cm.tab10(i), label=f'Marker {marker}')

plt.title('Różne markery')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

print("Wykres z markerami został wyświetlony!")
```

## 🎯 Praktyczne przypadki użycia

### 📈 Wykres sprzedaży w czasie

```python
# Dane sprzedażowe
miesiace = ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze',
            'Lip', 'Sie', 'Wrz', 'Paź', 'Lis', 'Gru']

sprzedaz_2022 = [15000, 18000, 22000, 19000, 25000, 28000,
                 32000, 30000, 26000, 24000, 20000, 35000]

sprzedaz_2023 = [18000, 21000, 25000, 22000, 28000, 32000,
                 36000, 35000, 31000, 29000, 26000, 40000]

plt.figure(figsize=(12, 7))

# Wykresy dla dwóch lat
plt.plot(miesiace, sprzedaz_2022, 'b-o', linewidth=3, 
         markersize=8, label='2022')
plt.plot(miesiace, sprzedaz_2023, 'r-s', linewidth=3, 
         markersize=8, label='2023')

# Wyróżnij najlepszy miesiąc
best_month_2023 = max(sprzedaz_2023)
best_idx = sprzedaz_2023.index(best_month_2023)
plt.plot(miesiace[best_idx], best_month_2023, 'go', 
         markersize=15, markerfacecolor='yellow', 
         markeredgecolor='green', markeredgewidth=3)

plt.title('Sprzedaż miesięczna - porównanie 2022 vs 2023', fontsize=16)
plt.xlabel('Miesiąc', fontsize=12)
plt.ylabel('Sprzedaż (PLN)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

# Dodaj adnotację
plt.annotate(f'Najlepszy miesiąc\n{best_month_2023:,} PLN', 
             xy=(miesiace[best_idx], best_month_2023),
             xytext=(miesiace[best_idx], best_month_2023 + 3000),
             ha='center', fontsize=10,
             arrowprops=dict(arrowstyle='->', color='green'))

plt.tight_layout()
plt.show()

print(f"Najlepszy miesiąc 2023: {miesiace[best_idx]} ({best_month_2023:,} PLN)")
```

### 🌡️ Temperatura w ciągu dnia

```python
# Symulacja temperatury
godziny = list(range(24))
temperatura = [12, 10, 9, 8, 7, 8, 10, 15, 18, 22, 
               25, 28, 30, 32, 31, 29, 27, 24, 20, 18, 
               16, 15, 14, 13]

plt.figure(figsize=(12, 6))

# Wykres temperatury
plt.plot(godziny, temperatura, 'orange', linewidth=3, 
         marker='o', markersize=6)

# Wyróżnij dzień i noc
dzien = [6, 18]  # wschód i zachód słońca
plt.axvspan(0, dzien[0], alpha=0.2, color='navy', label='Noc')
plt.axvspan(dzien[0], dzien[1], alpha=0.2, color='yellow', label='Dzień') 
plt.axvspan(dzien[1], 24, alpha=0.2, color='navy')

# Najwyższa i najniższa temperatura
max_temp = max(temperatura)
min_temp = min(temperatura)
max_idx = temperatura.index(max_temp)
min_idx = temperatura.index(min_temp)

plt.plot(max_idx, max_temp, 'ro', markersize=12, label=f'Max: {max_temp}°C')
plt.plot(min_idx, min_temp, 'bo', markersize=12, label=f'Min: {min_temp}°C')

plt.title('Temperatura w ciągu dnia', fontsize=16)
plt.xlabel('Godzina', fontsize=12)
plt.ylabel('Temperatura (°C)', fontsize=12)
plt.xticks(range(0, 25, 3))  # co 3 godziny
plt.grid(True, alpha=0.3)
plt.legend()

# Średnia temperatura
avg_temp = np.mean(temperatura)
plt.axhline(y=avg_temp, color='red', linestyle='--', 
            label=f'Średnia: {avg_temp:.1f}°C')

plt.tight_layout()
plt.show()

print(f"Temperatura: Min {min_temp}°C o {min_idx}:00, Max {max_temp}°C o {max_idx}:00")
```

### 💰 Wzrost inwestycji

```python
# Symulacja wzrostu inwestycji
lata = list(range(2010, 2024))
inwestycja_A = [1000]  # start z 1000 PLN
inwestycja_B = [1000]

# Symulacja wzrostu (różne stopy zwrotu)
np.random.seed(42)
for i in range(1, len(lata)):
    # Inwestycja A - stabilna (5-8% rocznie)
    zwrot_A = np.random.uniform(0.05, 0.08)
    inwestycja_A.append(inwestycja_A[-1] * (1 + zwrot_A))
    
    # Inwestycja B - ryzykowna (-10% do +20%)
    zwrot_B = np.random.uniform(-0.10, 0.20)
    inwestycja_B.append(inwestycja_B[-1] * (1 + zwrot_B))

plt.figure(figsize=(12, 8))

# Wykresy inwestycji
plt.plot(lata, inwestycja_A, 'g-o', linewidth=3, 
         markersize=6, label='Inwestycja A (Stabilna)')
plt.plot(lata, inwestycja_B, 'r-s', linewidth=3, 
         markersize=6, label='Inwestycja B (Ryzykowna)')

# Linia bazowa (początkowa wartość)
plt.axhline(y=1000, color='black', linestyle='-', 
            alpha=0.5, label='Wartość początkowa')

# Wypełnij obszar zysku/straty
plt.fill_between(lata, inwestycja_A, 1000, 
                 where=(np.array(inwestycja_A) >= 1000), 
                 color='green', alpha=0.2, interpolate=True)
plt.fill_between(lata, inwestycja_B, 1000, 
                 where=(np.array(inwestycja_B) >= 1000), 
                 color='red', alpha=0.2, interpolate=True)

plt.title('Porównanie wzrostu inwestycji (2010-2023)', fontsize=16)
plt.xlabel('Rok', fontsize=12)
plt.ylabel('Wartość inwestycji (PLN)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

# Formatuj oś Y jako waluta
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f} PLN'))

plt.tight_layout()
plt.show()

final_A = inwestycja_A[-1]
final_B = inwestycja_B[-1]
print(f"Końcowa wartość A: {final_A:,.2f} PLN (+{((final_A/1000)-1)*100:.1f}%)")
print(f"Końcowa wartość B: {final_B:,.2f} PLN (+{((final_B/1000)-1)*100:.1f}%)")
```

## 🔍 Zaawansowane opcje

### 1️⃣ Wiele wykresów w jednym

```python
# Subplot - kilka wykresów razem
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Wykres 1 - sin
x = np.linspace(0, 2*np.pi, 100)
axes[0,0].plot(x, np.sin(x), 'b-', linewidth=2)
axes[0,0].set_title('sin(x)')
axes[0,0].grid(True)

# Wykres 2 - cos  
axes[0,1].plot(x, np.cos(x), 'r-', linewidth=2)
axes[0,1].set_title('cos(x)')
axes[0,1].grid(True)

# Wykres 3 - tan
axes[1,0].plot(x, np.tan(x), 'g-', linewidth=2)
axes[1,0].set_title('tan(x)')
axes[1,0].set_ylim(-5, 5)  # ograniczenie osi Y
axes[1,0].grid(True)

# Wykres 4 - wszystkie razem
axes[1,1].plot(x, np.sin(x), 'b-', label='sin(x)')
axes[1,1].plot(x, np.cos(x), 'r-', label='cos(x)')
axes[1,1].set_title('sin(x) i cos(x)')
axes[1,1].legend()
axes[1,1].grid(True)

plt.suptitle('Funkcje trygonometryczne', fontsize=16)
plt.tight_layout()
plt.show()
```

### 2️⃣ Interaktywne elementy

```python
# Wykres z adnotacjami i strzałkami
x = np.linspace(0, 4*np.pi, 200)
y = np.sin(x) * np.exp(-x/4)

plt.figure(figsize=(12, 6))
plt.plot(x, y, 'purple', linewidth=3, label='sin(x) * exp(-x/4)')

# Znajdź maksima lokalne (uproszczony sposób)
peaks = []
for i in range(1, len(y)-1):
    if y[i-1] < y[i] > y[i+1] and y[i] > 0.1:  # próg 0.1
        peaks.append((x[i], y[i]))

# Dodaj adnotacje do pików
for i, (px, py) in enumerate(peaks[:3]):  # pierwsze 3 piki
    plt.plot(px, py, 'ro', markersize=10)
    plt.annotate(f'Pik {i+1}\n({px:.2f}, {py:.2f})', 
                 xy=(px, py), xytext=(px+1, py+0.2),
                 arrowprops=dict(arrowstyle='->', color='red'),
                 fontsize=10, ha='center')

plt.title('Funkcja tłumiona z zaznaczonymi pikami')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Zawsze dodawaj tytuły i etykiety
plt.plot([1,2,3], [1,4,9])
plt.title('Tytuł wykresu')
plt.xlabel('Oś X')
plt.ylabel('Oś Y')

# 2. Używaj kolorów i legendy dla wielu serii
plt.plot([1,2,3], [1,4,9], label='Seria 1')
plt.plot([1,2,3], [2,3,5], label='Seria 2')
plt.legend()

# 3. Dostosuj rozmiar dla czytelności
plt.figure(figsize=(10, 6))  # szerokość, wysokość

# 4. Używaj grid dla łatwiejszego odczytywania
plt.grid(True, alpha=0.3)

# 5. Zapisz wykresy
plt.savefig('wykres.png', dpi=300, bbox_inches='tight')
```

### ❌ Unikaj

```python
# Nie twórz wykresów bez opisów
# plt.plot([1,2,3], [1,4,9])  # Co to przedstawia?

# Nie używaj domyślnych małych rozmiarów
# plt.figure(figsize=(3, 2))  # Za małe!

# Nie mieszaj zbyt wielu kolorów
# plt.plot(x, y1, 'red')
# plt.plot(x, y2, 'blue') 
# plt.plot(x, y3, 'green')
# plt.plot(x, y4, 'orange')  # Za dużo!
```

## 📝 Podsumowanie

`pyplot.plot()` to fundamentalny building block matplotlib:

- 📈 Podstawowa funkcja do wykresów liniowych
- 🎨 Bogaty wybór stylów linii, kolorów, markerów
- 📊 Idealne do szeregów czasowych, trendów, porównań
- 🔧 Łatwe do dostosowania (tytuły, etykiety, legendy)
- 💫 Fundament dla bardziej złożonych wizualizacji
- ⚡ Szybkie i efektywne dla eksploracji danych

To jak uniwersalny ołówek - prosty, ale pozwala narysować wszystko! ✏️✨