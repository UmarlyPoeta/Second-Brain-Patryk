# 73. Promieniowanie termiczne; prawo Stefana-Boltzmanna oraz przesunięć Wiena; teoria Plancka

## Promieniowanie termiczne

**Definicja**: Promieniowanie elektromagnetyczne emitowane przez ciała o temperaturze wyższej od zera bezwzględnego.

**Cechy:**
- Widmo ciągłe
- Intensywność i rozkład spektralny zależą tylko od temperatury
- Wszystkie ciała promieniują energię cieplną

## Ciało doskonale czarne

**Definicja**: Idealny absorber i emiter promieniowania - pochłania całe padające promieniowanie przy każdej długości fali.

**Właściwości:**
- Absorpcja α = 1 dla wszystkich λ
- Najlepszy możliwy emiter przy danej temperaturze
- Model teoretyczny dla rzeczywistych ciał

## Prawo Stefana-Boltzmanna

**Moc całkowita promieniowanią przez ciało doskonale czarne:**
$$P = σAT^4$$

gdzie:
- σ = 5,67×10⁻⁸ W/(m²·K⁴) - stała Stefana-Boltzmanna
- A - powierzchnia ciała [m²]
- T - temperatura bezwzględna [K]

**Gęstość strumienia energii:**
$$j = \frac{P}{A} = σT^4$$

**Dla ciał rzeczywistych:**
$$P = εσAT^4$$

gdzie ε - emisyjność (0 < ε < 1)

## Prawo przesunięć Wiena

**Długość fali maksimum emisji:**
$$λ_{max} = \frac{b}{T}$$

gdzie b = 2,898×10⁻³ m·K - stała Wiena

**Wnioski:**
- Im wyższa temperatura, tym krótsze λ_{max}
- Słońce (T≈6000K): λ_{max} ≈ 500 nm (zielony)
- Człowiek (T≈310K): λ_{max} ≈ 9,4 μm (podczerwień)

## Teoria Plancka

**Funkcja Plancka - rozkład spektralny energii:**
$$u(λ,T) = \frac{8πhc}{λ^5} \cdot \frac{1}{e^{hc/λkT} - 1}$$

gdzie:
- h = 6,626×10⁻³⁴ J·s - stała Plancka
- c - prędkość światła
- k = 1,38×10⁻²³ J/K - stała Boltzmanna

**Hipoteza kwantowa Plancka:**
- Energia promieniowania jest skwantowana
- Energia fotonu: E = hf = hc/λ
- Emisja i absorpcja w porcjach (kwantach)

## Przybliżenia graniczne

**Prawo Rayleigha-Jeansa** (długie fale, hf << kT):
$$u(λ,T) ≈ \frac{8πkT}{λ^4}$$

**Prawo Wiena** (krótkie fale, hf >> kT):
$$u(λ,T) ≈ \frac{8πhc}{λ^5} e^{-hc/λkT}$$

## Przykłady liczbowe

**Przykład 1**: Temperatura Słońca
- λ_{max} = 500 nm
- T = b/λ_{max} = 2,898×10⁻³/500×10⁻⁹ = 5796 K

**Przykład 2**: Moc promieniowania człowieka
- T = 310 K, A ≈ 2 m², ε ≈ 0,98
- P = 0,98 × 5,67×10⁻⁸ × 2 × 310⁴ = 103 W

## Zastosowania

- **Pirometry** - pomiary temperatury
- **Termowizja** - obrazowanie w podczerwieni
- **Astronomia** - określanie temperatur gwiazd
- **Energetyka słoneczna** - optymalizacja paneli

![[termiczne_boltzman_wiena_planck.pdf]]
