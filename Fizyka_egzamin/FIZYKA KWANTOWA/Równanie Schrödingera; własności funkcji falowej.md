# 78. Równanie Schrödingera; własności funkcji falowej

## Równanie Schrödingera niestacjonarne

**Ogólna postać:**
$$i\hbar \frac{\partial Ψ}{\partial t} = \hat{H}Ψ$$

gdzie:
- Ψ(x,t) - funkcja falowa
- $\hat{H}$ - operator Hamiltona (energia całkowita)
- ℏ - zredukowana stała Plancka

**Dla jednego wymiaru:**
$$i\hbar \frac{\partial Ψ}{\partial t} = -\frac{\hbar^2}{2m}\frac{\partial^2 Ψ}{\partial x^2} + V(x)Ψ$$

## Równanie Schrödingera stacjonarne

**Dla stanów stacjonarnych** (V nie zależy od czasu):
$$\hat{H}ψ = Eψ$$

**Postać jednowymiarowa:**
$$-\frac{\hbar^2}{2m}\frac{d^2ψ}{dx^2} + V(x)ψ = Eψ$$

**Rozwiązanie metodą separacji zmiennych:**
$$Ψ(x,t) = ψ(x)e^{-iEt/\hbar}$$

## Właściwości funkcji falowej

### Interpretacja Born'a
**Gęstość prawdopodobieństwa:**
$$ρ(x,t) = |Ψ(x,t)|^2 = Ψ^*(x,t)Ψ(x,t)$$

**Prawdopodobieństwo znalezienia cząstki w przedziale [a,b]:**
$$P = \int_a^b |Ψ(x,t)|^2 dx$$

### Warunki normalizacji
$$\int_{-∞}^{+∞} |Ψ(x,t)|^2 dx = 1$$

### Warunki ciągłości
**Funkcja falowa musi być:**
1. **Ciągła** w całej przestrzeni
2. **Jednoznaczna** w każdym punkcie
3. **Skończona** w całej przestrzeni
4. **Mieć ciągłą pierwszą pochodną** (jeśli V(x) jest skończone)

## Wartości oczekiwane obserwabli

**Ogólny wzór:**
$$⟨\hat{A}⟩ = \int_{-∞}^{+∞} Ψ^*(x,t) \hat{A} Ψ(x,t) dx$$

**Położenie:**
$$⟨x⟩ = \int_{-∞}^{+∞} Ψ^*(x,t) \cdot x \cdot Ψ(x,t) dx$$

**Pęd:**
$$⟨p⟩ = \int_{-∞}^{+∞} Ψ^*(x,t) \left(-i\hbar\frac{\partial}{\partial x}\right) Ψ(x,t) dx$$

**Energia:**
$$⟨E⟩ = \int_{-∞}^{+∞} Ψ^*(x,t) \hat{H} Ψ(x,t) dx$$

## Operatory w mechanice kwantowej

| Obserwabla | Operator klasyczny | Operator kwantowy |
|------------|-------------------|-------------------|
| Położenie | x | $\hat{x} = x$ |
| Pęd | p | $\hat{p} = -i\hbar\frac{\partial}{\partial x}$ |
| Energia kinetyczna | p²/(2m) | $\hat{T} = -\frac{\hbar^2}{2m}\frac{\partial^2}{\partial x^2}$ |
| Energia potencjalna | V(x) | $\hat{V} = V(x)$ |

## Równanie ciągłości

**Zachowanie prawdopodobieństwa:**
$$\frac{\partial ρ}{\partial t} + \frac{\partial j}{\partial x} = 0$$

**Gęstość prądu prawdopodobieństwa:**
$$j = \frac{\hbar}{2mi}\left(Ψ^*\frac{\partial Ψ}{\partial x} - Ψ\frac{\partial Ψ^*}{\partial x}\right)$$

## Przykład: Swobodna cząstka

**Potencjał:** V(x) = 0

**Równanie:**
$$-\frac{\hbar^2}{2m}\frac{d^2ψ}{dx^2} = Eψ$$

**Rozwiązanie:**
$$ψ(x) = Ae^{ikx} + Be^{-ikx}$$

gdzie $k = \sqrt{2mE}/\hbar$

**Interpretacja:**
- Pierwszy składnik: fala biegnąca w prawo
- Drugi składnik: fala biegnąca w lewo
- |ψ|² = const → równomierne prawdopodobieństwo

## Zastosowania

- **Projektowanie urządzeń kwantowych**
- **Spektroskopia** - przewidywanie widm
- **Chemia kwantowa** - struktura molekuł
- **Technologie kwantowe** - komputery, kryptografia

![[schrodinger.pdf]]
