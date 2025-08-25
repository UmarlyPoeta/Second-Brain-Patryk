# 🎲 NumPy - numpy.random - Generowanie liczb losowych

## 📚 Co to jest numpy.random?

`numpy.random` to moduł do generowania liczb losowych i próbkowania. To jak cyfrowa kostka do gry - daje losowość, ale kontrolowaną! 🎲

## 🔧 Podstawowe funkcje

```python
import numpy as np

# Ustawienie seed dla reprodukowalności
np.random.seed(42)

# Podstawowe funkcje
np.random.rand()        # liczba losowa 0-1
np.random.randn()       # rozkład normalny (0,1)  
np.random.randint()     # liczby całkowite
np.random.choice()      # wybór z tablicy
np.random.shuffle()     # przemieszanie
```

## 💻 Podstawowe przykłady

```python
import numpy as np

# Ustawmy seed dla powtarzalności
np.random.seed(42)

print("=== PODSTAWOWE GENEROWANIE ===")

# Liczba losowa 0-1
losowa = np.random.rand()
print(f"Losowa 0-1: {losowa:.4f}")

# Tablica losowych liczb
losowe_tablice = np.random.rand(3, 4)
print(f"Tablica 3x4:\n{losowe_tablice}")

# Rozkład normalny (średnia=0, odchylenie=1)
normalne = np.random.randn(5)
print(f"Rozkład normalny: {normalne}")

# Liczby całkowite z zakresu
calkowite = np.random.randint(1, 11, size=10)  # 1-10
print(f"Całkowite 1-10: {calkowite}")

# Wybór z listy
kolory = ['czerwony', 'niebieski', 'zielony', 'żółty']
wybrany_kolor = np.random.choice(kolory)
print(f"Wybrany kolor: {wybrany_kolor}")

# Wiele wyborów z prawdopodobieństwami
wybory = np.random.choice(kolory, size=10, 
                         p=[0.1, 0.3, 0.4, 0.2])  # prawdopodobieństwa
print(f"Wybory z wagami: {wybory}")
```

## 🎯 Praktyczne zastosowania

### 📊 Symulacja eksperymentów

```python
# Symulacja rzutów monetą
def rzuty_moneta(n_rzutow=1000):
    np.random.seed(123)
    rzuty = np.random.choice(['Orzeł', 'Reszka'], size=n_rzutow)
    
    orly = np.sum(rzuty == 'Orzeł')
    reszki = n_rzutow - orly
    
    print(f"=== SYMULACJA {n_rzutow} RZUTÓW MONETĄ ===")
    print(f"Orły: {orly} ({orly/n_rzutow:.1%})")
    print(f"Reszki: {reszki} ({reszki/n_rzutow:.1%})")
    
    # Sprawdź zbieżność do 50%
    proporcje_orlow = []
    for i in range(10, n_rzutow, 50):
        prop = np.sum(rzuty[:i] == 'Orzeł') / i
        proporcje_orlow.append(prop)
    
    return rzuty, proporcje_orlow

rzuty, proporcje = rzuty_moneta(1000)
print(f"Końcowa proporcja orłów: {proporcje[-1]:.3f}")

# Symulacja rzutów kostką
def rzuty_kostka(n_rzutow=6000):
    np.random.seed(456)
    rzuty = np.random.randint(1, 7, size=n_rzutow)
    
    print(f"\n=== SYMULACJA {n_rzutow} RZUTÓW KOSTKĄ ===")
    
    unique, counts = np.unique(rzuty, return_counts=True)
    for wartość, liczba in zip(unique, counts):
        procent = liczba / n_rzutow * 100
        print(f"Liczba {wartość}: {liczba:4} razy ({procent:5.1f}%)")
    
    # Chi-kwadrat test (uproszczony)
    expected = n_rzutow / 6  # oczekiwana częstość
    chi2 = np.sum((counts - expected)**2 / expected)
    print(f"\nChi-kwadrat: {chi2:.2f} (im mniej, tym bardziej uczciwa)")
    
    return rzuty

kostka_rzuty = rzuty_kostka(6000)
```

### 🎮 Generowanie danych testowych

```python
# Symulacja danych klientów e-commerce
def generuj_klientow(n=1000):
    np.random.seed(789)
    
    # Różne grupy wiekowe z różnymi charakterystykami
    grupy_wiekowe = ['18-25', '26-35', '36-45', '46-60', '60+']
    wiek_grupa = np.random.choice(grupy_wiekowe, n, 
                                 p=[0.2, 0.3, 0.25, 0.2, 0.05])
    
    # Dochód zależy od wieku (starsi = więcej)
    dochody = []
    for grupa in wiek_grupa:
        if grupa == '18-25':
            dochod = np.random.normal(3000, 1000)
        elif grupa == '26-35':
            dochod = np.random.normal(5000, 1500)
        elif grupa == '36-45':
            dochod = np.random.normal(7000, 2000)
        elif grupa == '46-60':
            dochod = np.random.normal(8000, 2500)
        else:  # 60+
            dochod = np.random.normal(4000, 1500)  # emerytura
        
        dochody.append(max(1500, dochod))  # minimum 1500
    
    # Wydatki zależą od dochodu (z losowością)
    wydatki = []
    for dochod in dochody:
        # Ludzie wydają 20-80% dochodu na zakupy online
        procent_wydatkow = np.random.uniform(0.2, 0.8)
        wydatek = dochod * procent_wydatkow * np.random.uniform(0.5, 1.5)
        wydatki.append(max(100, wydatek))
    
    # Kategorie produktów z wagami
    kategorie = ['Elektronika', 'Odzież', 'Dom', 'Sport', 'Książki']
    # Młodzi kupują więcej elektroniki, starsi więcej dla domu
    kategoria_preferencje = []
    for grupa in wiek_grupa:
        if grupa in ['18-25', '26-35']:
            kat = np.random.choice(kategorie, p=[0.4, 0.3, 0.1, 0.15, 0.05])
        elif grupa in ['36-45', '46-60']:
            kat = np.random.choice(kategorie, p=[0.2, 0.2, 0.4, 0.1, 0.1])
        else:  # 60+
            kat = np.random.choice(kategorie, p=[0.1, 0.1, 0.5, 0.05, 0.25])
        kategoria_preferencje.append(kat)
    
    klienci = pd.DataFrame({
        'wiek_grupa': wiek_grupa,
        'dochod': np.array(dochody).round(0),
        'wydatki': np.array(wydatki).round(0),
        'kategoria': kategoria_preferencje
    })
    
    return klienci

# Wygeneruj i przeanalizuj
import pandas as pd
klienci_df = generuj_klientow(1000)

print("=== ANALIZA WYGENEROWANYCH KLIENTÓW ===")
print(f"Liczba klientów: {len(klienci_df)}")
print(f"\nRozkład grup wiekowych:")
print(klienci_df['wiek_grupa'].value_counts().sort_index())

print(f"\nŚrednie dochody według grup:")
dochody_grupa = klienci_df.groupby('wiek_grupa')['dochod'].mean().sort_index()
for grupa, sredni_dochod in dochody_grupa.items():
    print(f"{grupa}: {sredni_dochod:,.0f} PLN")

print(f"\nNajpopularniejsze kategorie według wieku:")
for grupa in ['18-25', '36-45', '60+']:
    if grupa in klienci_df['wiek_grupa'].values:
        top_kat = klienci_df[klienci_df['wiek_grupa'] == grupa]['kategoria'].mode()[0]
        print(f"{grupa}: {top_kat}")
```

### 🧪 Próbkowanie i bootstrap

```python
# Bootstrap - metoda resamplingowa
def bootstrap_analiza(dane, n_bootstrap=1000):
    np.random.seed(999)
    
    # Oryginalna średnia
    orig_mean = np.mean(dane)
    
    # Bootstrap samples
    bootstrap_means = []
    for _ in range(n_bootstrap):
        # Losuj z powrotami (with replacement)
        bootstrap_sample = np.random.choice(dane, size=len(dane), replace=True)
        bootstrap_means.append(np.mean(bootstrap_sample))
    
    bootstrap_means = np.array(bootstrap_means)
    
    print(f"=== BOOTSTRAP ANALIZA ===")
    print(f"Oryginalna średnia: {orig_mean:.2f}")
    print(f"Bootstrap średnia: {np.mean(bootstrap_means):.2f}")
    print(f"Bootstrap std: {np.std(bootstrap_means):.2f}")
    
    # Przedział ufności 95%
    ci_lower = np.percentile(bootstrap_means, 2.5)
    ci_upper = np.percentile(bootstrap_means, 97.5)
    print(f"95% przedział ufności: [{ci_lower:.2f}, {ci_upper:.2f}]")
    
    return bootstrap_means

# Test na przykładowych danych
test_data = np.random.normal(100, 15, 50)  # 50 obserwacji
bootstrap_results = bootstrap_analiza(test_data)

# Monte Carlo - symulacja złożonych procesów
def monte_carlo_pi(n_points=100000):
    """Oblicz π metodą Monte Carlo"""
    np.random.seed(42)
    
    # Losowe punkty w kwadracie (-1,1) x (-1,1)
    x = np.random.uniform(-1, 1, n_points)
    y = np.random.uniform(-1, 1, n_points)
    
    # Sprawdź które punkty są w kole (odległość od środka <= 1)
    distances = np.sqrt(x**2 + y**2)
    points_in_circle = np.sum(distances <= 1)
    
    # π ≈ 4 * (punkty w kole / wszystkie punkty)
    pi_estimate = 4 * points_in_circle / n_points
    
    print(f"\n=== MONTE CARLO ESTYMACJA π ===")
    print(f"Punkty w kole: {points_in_circle:,}")
    print(f"Wszystkie punkty: {n_points:,}")
    print(f"Estymacja π: {pi_estimate:.6f}")
    print(f"Prawdziwa π: {np.pi:.6f}")
    print(f"Błąd: {abs(pi_estimate - np.pi):.6f}")
    
    return pi_estimate

pi_estimate = monte_carlo_pi(1000000)
```

## 🔍 Zaawansowane rozkłady

```python
# Różne rozkłady prawdopodobieństwa
np.random.seed(555)

print("=== RÓŻNE ROZKŁADY ===")

# Rozkład wykładniczy (czas między zdarzeniami)
exponential = np.random.exponential(scale=2, size=1000)
print(f"Wykładniczy: średnia={np.mean(exponential):.2f}, mediana={np.median(exponential):.2f}")

# Rozkład gamma (czas obsługi klientów)
gamma = np.random.gamma(shape=2, scale=3, size=1000)
print(f"Gamma: średnia={np.mean(gamma):.2f}, mediana={np.median(gamma):.2f}")

# Rozkład beta (procenty, prawdopodobieństwa)
beta = np.random.beta(a=2, b=5, size=1000)
print(f"Beta (0-1): średnia={np.mean(beta):.3f}, mediana={np.median(beta):.3f}")

# Rozkład Poissona (liczba zdarzeń w czasie)
poisson = np.random.poisson(lam=3, size=1000)  # średnio 3 zdarzenia
print(f"Poisson: średnia={np.mean(poisson):.2f}, moda={np.bincount(poisson).argmax()}")

# Rozkład dwumianowy (liczba sukcesów w n próbach)
binomial = np.random.binomial(n=10, p=0.3, size=1000)  # 10 prób, 30% sukcesu
print(f"Dwumianowy: średnia={np.mean(binomial):.2f}, teoretyczna={10*0.3}")
```

## ⚠️ Ważne uwagi

```python
# Kontrola reprodukowalności
print("=== KONTROLA LOSOWOŚCI ===")

# Bez seed - różne wyniki za każdym razem
random1 = np.random.rand(5)
random2 = np.random.rand(5) 
print(f"Bez seed - różne: {not np.array_equal(random1, random2)}")

# Z seed - identyczne wyniki
np.random.seed(123)
seeded1 = np.random.rand(5)
np.random.seed(123)
seeded2 = np.random.rand(5)
print(f"Z seed - identyczne: {np.array_equal(seeded1, seeded2)}")

# Generator state - zaawansowana kontrola
state = np.random.get_state()
val1 = np.random.rand()
np.random.set_state(state)
val2 = np.random.rand()
print(f"State control - identyczne: {val1 == val2}")
```

## 📝 Podsumowanie

`numpy.random` to potężne narzędzie do:

- 🎲 Generowania liczb losowych (`rand`, `randn`, `randint`)
- 🎯 Próbkowania z rozkładów (`choice`, `shuffle`)  
- 📊 Symulacji Monte Carlo i bootstrap
- 🧪 Generowania danych testowych
- 🔬 Eksperymentów statystycznych
- ⚡ `seed()` dla reprodukowalności wyników
- 📈 Różnych rozkładów prawdopodobieństwa

To jak cyfrowa kostka - daje kontrolowaną losowość! 🎲✨