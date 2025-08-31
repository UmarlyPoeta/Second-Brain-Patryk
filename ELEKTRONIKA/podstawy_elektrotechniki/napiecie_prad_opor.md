# Napięcie, Prąd i Opór - Podstawy

## ⚡ Napięcie (Voltage)

### Definicja
**Napięcie elektryczne** to różnica potencjałów między dwoma punktami w obwodzie. Jest to "siła napędowa" elektronu w obwodzie.

### Jednostka
- **Volt [V]** - podstawowa jednostka napięcia
- **Millivolt [mV]** = 0,001 V
- **Kilovolt [kV]** = 1000 V

### Analogie
- Jak ciśnienie wody w rurze
- Wysokość wodospadu (energia potencjalna)

### Pomiar napięcia
- **Voltomierz** - łączymy **równolegle** do mierzonego elementu
- **Polaryzacja** - ważne przy prądzie stałym (+ do +, - do -)

## 🔄 Prąd elektryczny (Current)

### Definicja
**Prąd elektryczny** to uporządkowany ruch ładunków elektrycznych (elektronów) w przewodniku.

### Jednostka
- **Amper [A]** - podstawowa jednostka natężenia prądu
- **Miliamper [mA]** = 0,001 A
- **Mikroamper [μA]** = 0,000001 A

### Wzór podstawowy
```
I = Q / t
```
Gdzie:
- I - natężenie prądu [A]
- Q - ładunek elektryczny [C (Coulomb)]
- t - czas [s]

### Kierunek prądu
- **Prąd konwencjonalny** - od + do -
- **Prąd elektronowy** - od - do + (rzeczywisty ruch elektronów)

### Pomiar prądu
- **Amperomierz** - łączymy **szeregowo** w obwodzie
- **Nigdy równolegle!** - może uszkodzić przyrząd

## 🚫 Opór elektryczny (Resistance)

### Definicja
**Opór elektryczny** to właściwość materiału polegająca na przeciwdziałaniu przepływowi prądu.

### Jednostka
- **Ohm [Ω]** - podstawowa jednostka oporu
- **Kiloohm [kΩ]** = 1000 Ω
- **Megaohm [MΩ]** = 1 000 000 Ω

### Czynniki wpływające na opór

#### Materiał
- **Przewodniki**: miedź, aluminium, złoto (mały opór)
- **Półprzewodniki**: krzem, german (opór średni)
- **Izolatory**: guma, porcelana, szkło (duży opór)

#### Parametry fizyczne
```
R = ρ × (l / S)
```
Gdzie:
- R - opór [Ω]
- ρ - oporność właściwa materiału [Ω×mm²/m]
- l - długość przewodnika [m]
- S - przekrój poprzeczny [mm²]

#### Temperatura
- **Metale** - opór rośnie z temperaturą
- **Półprzewodniki** - opór maleje z temperaturą

## 📊 Zależności między wielkościami

### Prawo Ohma
```
U = I × R
I = U / R
R = U / I
```

### Moc elektryczna
```
P = U × I = I²R = U²/R
```

## 🔧 Przykłady praktyczne

### Przykład 1: Przewód miedziany
**Dane:** Przewód Cu o długości 100m, przekrój 2,5mm²  
**Oporność Cu:** ρ = 0,0175 Ω×mm²/m

```
R = 0,0175 × (100 / 2,5) = 0,7 Ω
```

### Przykład 2: Prąd w obwodzie
**Dane:** Bateria 9V, żarówka o oporze 18Ω

```
I = U / R = 9V / 18Ω = 0,5A = 500mA
```

## 🎯 Zastosowania praktyczne

### W instalacjach
- **Dobór przekroju przewodów** - mniejszy przekrój = większy opór
- **Spadki napięć** - długie przewody powodują straty
- **Obliczenia obciążeń** - bezpieczne eksploatowanie instalacji

### W elektronice
- **Dzielniki napięcia** - rezystory szeregowo
- **Źródła prądowe** - duży opór szeregowo
- **Ograniczanie prądu** - rezystory w układach LED

## ⚠️ Bezpieczeństwo

### Niebezpieczne napięcia
- **< 50V** - zazwyczaj bezpieczne (w suchych warunkach)
- **50V - 1000V** - niskie napięcie (instalacje domowe 230V)
- **> 1000V** - wysokie napięcie (bardzo niebezpieczne)

### Niebezpieczne prądy
- **1-5 mA** - próg odczuwalności
- **10-20 mA** - skurcz mięśni, trudność z puszczeniem
- **50 mA** - migotanie serca
- **> 100 mA** - śmiertelne

## 📚 Powiązane tematy

- [[prawo_ohma|Prawo Ohma]]
- [[moc_elektryczna|Moc Elektryczna]]
- [[prad_staly_przemienny|Prąd Stały vs Prąd Przemienny]]
- [[bezpieczenstwo_elektryczne|Bezpieczeństwo Elektryczne]]
- [[rezystory|Rezystory]]
- [[multimetr|Multimetr - Podstawy]]

---

#elektrotechnika #napięcie #prąd #opór #podstawy #bezpieczeństwo