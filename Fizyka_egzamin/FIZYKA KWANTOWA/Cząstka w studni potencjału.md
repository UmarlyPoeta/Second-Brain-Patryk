# 79. Cząstka w studni potencjału

## Model nieskończonej studni potencjału

**Potencjał:**
$$V(x) = \begin{cases} 
0 & \text{dla } 0 < x < L \\
∞ & \text{dla } x ≤ 0 \text{ lub } x ≥ L
\end{cases}$$

**Warunki brzegowe:**
$$ψ(0) = 0 \quad \text{i} \quad ψ(L) = 0$$

## Rozwiązanie równania Schrödingera

**Wewnątrz studni (V = 0):**
$$-\frac{\hbar^2}{2m}\frac{d^2ψ}{dx^2} = Eψ$$

**Ogólne rozwiązanie:**
$$ψ(x) = A\sin(kx) + B\cos(kx)$$

gdzie $k = \sqrt{2mE}/\hbar$

**Zastosowanie warunków brzegowych:**
- ψ(0) = 0 → B = 0
- ψ(L) = 0 → sin(kL) = 0 → kL = nπ

## Funkcje falowe i energie

**Skwantowane wartości k:**
$$k_n = \frac{nπ}{L}, \quad n = 1, 2, 3, ...$$

**Poziomy energetyczne:**
$$E_n = \frac{\hbar^2k_n^2}{2m} = \frac{n^2π^2\hbar^2}{2mL^2}$$

**Znormalizowane funkcje falowe:**
$$ψ_n(x) = \sqrt{\frac{2}{L}}\sin\left(\frac{nπx}{L}\right)$$
