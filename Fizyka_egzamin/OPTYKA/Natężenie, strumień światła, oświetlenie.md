# 72. Natężenie, strumień światła, oświetlenie

## Podstawowe wielkości fotometryczne

### Strumień świetlny (Φ)

**Definicja**: Moc promieniowania elektromagnetycznego oceniana przez oko ludzkie.

**Jednostka**: lumen [lm]

**Wzór**:
$$Φ = K \int V(λ) \cdot P(λ) \, dλ$$

gdzie:
- K = 683 lm/W (stała fotometryczna maksymalna)
- V(λ) - względna czułość oka (maksimum przy λ = 555 nm)
- P(λ) - moc promieniowania na długości fali λ

### Natężenie światła (I)

**Definicja**: Strumień świetlny przypadający na jednostkę kąta bryłowego.

**Wzór**:
$$I = \frac{dΦ}{dΩ}$$

**Jednostka**: kandela [cd] = [lm/sr]

**Dla źródła punktowego o równomiernym rozsyłaniu:**
$$I = \frac{Φ}{4π}$$

### Luminancja (L)

**Definicja**: Natężenie światła przypadające na jednostkę powierzchni pozornej źródła.

**Wzór**:
$$L = \frac{dI}{dS \cos θ}$$

gdzie θ - kąt między normalną do powierzchni a kierunkiem obserwacji

**Jednostka**: [cd/m²] = nit

### Oświetlenie (E)

**Definicja**: Strumień świetlny padający na jednostkę powierzchni.

**Wzór**:
$$E = \frac{dΦ}{dS}$$

**Jednostka**: luks [lx] = [lm/m²]

## Prawo odwrotności kwadratów

**Dla źródła punktowego:**
$$E = \frac{I \cos α}{r^2}$$

gdzie:
- α - kąt między normalną do powierzchni a kierunkiem światła
- r - odległość od źródła

**Dla powierzchni prostopadłej do kierunku światła (α = 0):**
$$E = \frac{I}{r^2}$$

## Prawo Lamberta (cosinus)

**Dla powierzchni rozpraszających idealnie:**
$$I(θ) = I_0 \cos θ$$

gdzie θ - kąt od normalnej do powierzchni

## Przykłady typowych wartości

### Natężenie światła:
- Świeca: ~1 cd
- Żarówka 100W: ~100 cd
- Reflektor samochodowy: ~10⁴ cd

### Oświetlenie:
- Noc księżycowa: 0,1 lx
- Pokój: 100-300 lx
- Biuro: 500-1000 lx
- Dzień słoneczny: 10⁴-10⁵ lx

### Luminancja:
- Papier biały w świetle dziennym: ~30 cd/m²
- Monitor komputera: 100-300 cd/m²
- Słońce: ~10⁹ cd/m²

## Przykład liczbowy

**Dane:**
- Żarówka o natężeniu I = 150 cd
- Odległość r = 2 m
- Powierzchnia prostopadła do kierunku światła

**Szukane**: Oświetlenie powierzchni

**Rozwiązanie:**
$$E = \frac{I}{r^2} = \frac{150}{2^2} = 37,5 \text{ lx}$$

## Sprawność świetlna

**Definicja**: Stosunek strumienia świetlnego do mocy elektrycznej.

$$η = \frac{Φ}{P}$$ [lm/W]

**Przykłady:**
- Żarówka wolframowa: 10-20 lm/W
- Świetlówka: 50-100 lm/W
- LED: 80-200 lm/W
- Teoretyczne maksimum: 683 lm/W

## Fotometria vs radiometria

| Wielkość fotometryczna | Jednostka | Wielkość radiometryczna | Jednostka |
|------------------------|-----------|-------------------------|-----------|
| Strumień świetlny (Φ) | lm | Strumień energii (P) | W |
| Natężenie światła (I) | cd | Natężenie energetyczne | W/sr |
| Luminancja (L) | cd/m² | Radiancja | W/(sr·m²) |
| Oświetlenie (E) | lx | Naświetlanie | W/m² |

![[natezenie_strumien_oswietlenie.pdf]]