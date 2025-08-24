## 🔢 NumPy - Linear Algebra Advanced

_Zaawansowane operacje algebry liniowej w NumPy_

---

### 📝 Wprowadzenie do algebry liniowej w NumPy

**NumPy** dostarcza kompleksowe narzędzia do operacji algebry liniowej przez:

1. **Moduł numpy.linalg**
   - Funkcje do dekompozycji macierzy
   - Rozwiązywanie układów równań
   - Obliczanie wartości własnych

2. **Optimized BLAS/LAPACK**
   - Wysokowydajne biblioteki matematyczne
   - Automatyczna parallelizacja
   - Stabilność numeryczna

3. **Broadcasting dla macierzy**
   - Automatyczne dopasowanie wymiarów
   - Efektywne operacje na różnych rozmiarach

---

### 🔄 Podstawowe operacje macierzowe

#### Mnożenie macierzy

```python
import numpy as np

# Różne sposoby mnożenia macierzy
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Element-wise multiplication (Hadamard product)
hadamard = A * B
print("Hadamard product:")
print(hadamard)

# Matrix multiplication
matrix_mult1 = A @ B  # Operator @
matrix_mult2 = np.dot(A, B)  # Funkcja dot
matrix_mult3 = A.dot(B)  # Metoda dot

print("\nMatrix multiplication:")
print(matrix_mult1)

# Transpozycja
A_T = A.T
A_transpose = np.transpose(A)
print(f"\nTranspose:\n{A_T}")
```

#### Operacje na wektorach

```python
# Iloczyn skalarny (dot product)
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])

dot_product = np.dot(v1, v2)
print(f"Dot product: {dot_product}")

# Iloczyn wektorowy (cross product) - tylko dla wektorów 3D
v3d_1 = np.array([1, 2, 3])
v3d_2 = np.array([4, 5, 6])

cross_product = np.cross(v3d_1, v3d_2)
print(f"Cross product: {cross_product}")

# Norma wektora
norm_l2 = np.linalg.norm(v1)  # L2 norm (Euclidean)
norm_l1 = np.linalg.norm(v1, ord=1)  # L1 norm (Manhattan)
norm_inf = np.linalg.norm(v1, ord=np.inf)  # L∞ norm

print(f"L2 norm: {norm_l2:.4f}")
print(f"L1 norm: {norm_l1}")
print(f"L∞ norm: {norm_inf}")
```

---

### 🏭 Dekompozycje macierzy

#### Singular Value Decomposition (SVD)

```python
# SVD - bardzo ważne w analizie danych i ML
A = np.random.rand(5, 3)

U, s, Vt = np.linalg.svd(A)

print(f"Original shape: {A.shape}")
print(f"U shape: {U.shape}")
print(f"s shape: {s.shape}")  # singular values
print(f"Vt shape: {Vt.shape}")

# Rekonstrukcja oryginalnej macierzy
S = np.zeros_like(A)
S[:min(A.shape), :min(A.shape)] = np.diag(s)
A_reconstructed = U @ S @ Vt

print(f"\nReconstruction error: {np.linalg.norm(A - A_reconstructed):.10f}")

# SVD do redukcji wymiarowości
def svd_compress(A, k):
    """Kompresja macierzy używając k największych wartości singularnych"""
    U, s, Vt = np.linalg.svd(A)
    return U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]

# Kompresja do k=2 wymiarów
A_compressed = svd_compress(A, 2)
print(f"\nCompressed shape: {A_compressed.shape}")
```

#### QR Decomposition

```python
# QR decomposition - ortogonalizacja Gram-Schmidt
A = np.random.rand(5, 3)
Q, R = np.linalg.qr(A)

print(f"Q shape: {Q.shape}")
print(f"R shape: {R.shape}")

# Sprawdzenie właściwości
print(f"\nQ jest ortogonalna: {np.allclose(Q.T @ Q, np.eye(Q.shape[1]))}")
print(f"R jest górnotrójkątna: {np.allclose(np.tril(R, -1), 0)}")
print(f"A = Q @ R: {np.allclose(A, Q @ R)}")

# QR do rozwiązywania układów równań
b = np.random.rand(5)
x = np.linalg.solve(R, Q.T @ b)  # Rozwiązanie Rx = Q^T b
```

#### Eigendecomposition

```python
# Wartości własne i wektory własne
A_square = np.array([[4, 2], [1, 3]])

eigenvalues, eigenvectors = np.linalg.eig(A_square)

print(f"Eigenvalues: {eigenvalues}")
print(f"Eigenvectors:\n{eigenvectors}")

# Sprawdzenie: A * v = λ * v
for i in range(len(eigenvalues)):
    lambda_i = eigenvalues[i]
    v_i = eigenvectors[:, i]
    
    Av = A_square @ v_i
    lambda_v = lambda_i * v_i
    
    print(f"\nFor eigenvalue {lambda_i:.4f}:")
    print(f"A*v = {Av}")
    print(f"λ*v = {lambda_v}")
    print(f"Equal: {np.allclose(Av, lambda_v)}")
```

---

### 🔧 Rozwiązywanie układów równań

#### Układy liniowe

```python
# Układ równań: Ax = b
A = np.array([[3, 2, 1],
              [1, 4, 2],
              [2, 1, 3]])
b = np.array([1, 2, 3])

# Rozwiązanie bezpośrednie
x = np.linalg.solve(A, b)
print(f"Solution: {x}")

# Sprawdzenie rozwiązania
verification = A @ x
print(f"A @ x = {verification}")
print(f"b = {b}")
print(f"Correct: {np.allclose(verification, b)}")

# Rozwiązanie używając pseudoinverse (dla macierzy nieodwracalnych)
x_pseudo = np.linalg.pinv(A) @ b
print(f"\nPseudoinverse solution: {x_pseudo}")

# Najmniejsze kwadraty dla systemów overdetermined
A_overdetermined = np.random.rand(10, 3)  # Więcej równań niż niewiadomych
b_overdetermined = np.random.rand(10)

x_lstsq, residuals, rank, s = np.linalg.lstsq(A_overdetermined, b_overdetermined, rcond=None)
print(f"\nLeast squares solution: {x_lstsq}")
print(f"Residuals: {residuals}")
```

#### Macierz odwrotna i wyznacznik

```python
# Wyznacznik
det_A = np.linalg.det(A)
print(f"Determinant: {det_A:.6f}")

# Macierz odwrotna (jeśli det != 0)
if det_A != 0:
    A_inv = np.linalg.inv(A)
    print(f"\nInverse matrix:\n{A_inv}")
    
    # Sprawdzenie: A * A^(-1) = I
    identity_check = A @ A_inv
    print(f"\nA @ A_inv:\n{identity_check}")
    print(f"Is identity: {np.allclose(identity_check, np.eye(3))}")

# Warunek macierzy (condition number)
cond_num = np.linalg.cond(A)
print(f"\nCondition number: {cond_num:.6f}")
if cond_num > 1e12:
    print("⚠️  Macierz jest źle uwarunkowana (numerycznie niestabilna)")
```

---

### 📐 Zaawansowane operacje geometryczne

#### Transformacje geometryczne

```python
def create_rotation_matrix_2d(angle_degrees):
    """Tworzy macierz obrotu 2D"""
    angle_rad = np.radians(angle_degrees)
    cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
    return np.array([[cos_a, -sin_a], 
                     [sin_a, cos_a]])

def create_scaling_matrix_2d(sx, sy):
    """Tworzy macierz skalowania 2D"""
    return np.array([[sx, 0], 
                     [0, sy]])

# Przykład transformacji punktów
points = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]]).T  # Kwadratu jednostkowego

# Obrót o 45 stopni
rotation_45 = create_rotation_matrix_2d(45)
rotated_points = rotation_45 @ points

print("Original points:")
print(points.T)
print("\nAfter 45° rotation:")
print(rotated_points.T)

# Skalowanie x2 w kierunku x, x0.5 w kierunku y
scaling = create_scaling_matrix_2d(2, 0.5)
scaled_points = scaling @ points

print("\nAfter scaling (2x, 0.5y):")
print(scaled_points.T)

# Kombinacja transformacji
combined_transform = scaling @ rotation_45
transformed_points = combined_transform @ points

print("\nAfter combined transformation (rotation then scaling):")
print(transformed_points.T)
```

#### Projekcje ortogonalne

```python
def orthogonal_projection(v, onto_space_basis):
    """
    Projekcja ortogonalna wektora v na przestrzeń rozpięta przez basis
    """
    # Konwertuj basis na macierz (kolumny = wektory bazowe)
    A = np.array(onto_space_basis).T
    
    # Projekcja: P = A(A^T A)^(-1) A^T
    projection_matrix = A @ np.linalg.pinv(A.T @ A) @ A.T
    return projection_matrix @ v

# Przykład: projekcja na płaszczyznę
v = np.array([1, 2, 3])  # Wektor do projekcji

# Basis płaszczyzny xy (z=0)
basis_xy = [[1, 0, 0], [0, 1, 0]]
projection_xy = orthogonal_projection(v, basis_xy)

print(f"Original vector: {v}")
print(f"Projection onto xy-plane: {projection_xy}")

# Sprawdzenie: składowa z powinna być 0
print(f"z-component is zero: {np.isclose(projection_xy[2], 0)}")
```

---

### 🎯 Praktyczne zastosowania

#### Principal Component Analysis (PCA)

```python
def pca_numpy(X, n_components=2):
    """
    Implementacja PCA używając NumPy
    X: macierz danych (samples x features)
    """
    # Centrowanie danych
    X_centered = X - np.mean(X, axis=0)
    
    # Macierz kowariancji
    cov_matrix = np.cov(X_centered.T)
    
    # Eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    
    # Sortowanie według wartości własnych (malejąco)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # Wybór pierwszych n_components składowych
    principal_components = eigenvectors[:, :n_components]
    
    # Transformacja danych
    X_pca = X_centered @ principal_components
    
    # Wyjaśniona wariancja
    explained_variance_ratio = eigenvalues[:n_components] / np.sum(eigenvalues)
    
    return X_pca, principal_components, explained_variance_ratio, eigenvalues

# Przykład na danych syntetycznych
np.random.seed(42)
# Dane skorelowane
X = np.random.randn(100, 3)
X[:, 1] = X[:, 0] + 0.5 * np.random.randn(100)  # y skorelowane z x
X[:, 2] = -X[:, 0] + 0.3 * np.random.randn(100)  # z anty-skorelowane z x

X_pca, components, var_ratio, eigenvals = pca_numpy(X, n_components=2)

print("Original data shape:", X.shape)
print("PCA data shape:", X_pca.shape)
print(f"Explained variance ratio: {var_ratio}")
print(f"Total explained variance: {np.sum(var_ratio):.4f}")

print("\nPrincipal components (directions of maximum variance):")
print(components)
```

#### Rozwiązywanie problemów optymalizacji

```python
def linear_regression_normal_equation(X, y):
    """
    Regresja liniowa przez równanie normalne: θ = (X^T X)^(-1) X^T y
    """
    # Dodanie kolumny bias (intercept)
    X_with_bias = np.column_stack([np.ones(X.shape[0]), X])
    
    # Równanie normalne
    theta = np.linalg.pinv(X_with_bias.T @ X_with_bias) @ X_with_bias.T @ y
    
    return theta

# Przykład regresji liniowej
np.random.seed(42)
X = np.random.randn(100, 1)
true_theta = np.array([2, 3])  # [bias, slope]
y = 2 + 3 * X.ravel() + 0.1 * np.random.randn(100)

# Rozwiązanie metodą normalnych równań
theta_estimated = linear_regression_normal_equation(X, y)

print(f"True parameters: {true_theta}")
print(f"Estimated parameters: {theta_estimated}")
print(f"Estimation error: {np.linalg.norm(true_theta - theta_estimated):.6f}")

# Predykcje
X_test = np.linspace(-3, 3, 50).reshape(-1, 1)
X_test_with_bias = np.column_stack([np.ones(X_test.shape[0]), X_test])
y_pred = X_test_with_bias @ theta_estimated
```

---

### ⚡ Wskazówki dotyczące wydajności

#### Wykorzystanie cache i in-place operations

```python
# Unikaj tworzenia tymczasowych kopii
A = np.random.rand(1000, 1000)
B = np.random.rand(1000, 1000)

# ❌ Nieefektywne - tworzy kopie
result_bad = (A + B) @ (A - B)

# ✅ Efektywne - używa buforów
result_good = np.empty_like(A)
np.add(A, B, out=result_good)  # A + B -> result_good
temp = np.empty_like(A)
np.subtract(A, B, out=temp)    # A - B -> temp
np.dot(result_good, temp, out=result_good)  # result_good @ temp -> result_good

# In-place operations gdzie to możliwe
A += 1  # zamiast A = A + 1
A *= 2  # zamiast A = A * 2
```

#### Wybór odpowiednich funkcji

```python
# Dla dużych macierzy, użyj specialized functions
A = np.random.rand(10000, 10000)

# ❌ Wolne
det_slow = np.linalg.det(A)

# ✅ Szybsze dla specjalnych przypadków
if np.allclose(A, A.T):  # Jeśli macierz jest symetryczna
    eigenvals_sym = np.linalg.eigvals(A)  # Szybsza dla macierzy symetrycznych
else:
    eigenvals_general = np.linalg.eigvals(A)

# Użyj decomposition tylko gdy potrzebujesz wszystkich składników
U, s, Vt = np.linalg.svd(A, full_matrices=False)  # Ekonomiczna SVD
```

---

### 🚨 Częste błędy i pułapki

#### Stabilność numeryczna

```python
# Problem: źle uwarunkowane macierze
A_ill_conditioned = np.array([[1, 1], [1, 1 + 1e-15]])
print(f"Condition number: {np.linalg.cond(A_ill_conditioned):.2e}")

# Rozwiązanie: używaj pinv zamiast inv dla niestabilnych macierzy
try:
    inv_unstable = np.linalg.inv(A_ill_conditioned)
    print("Inversion successful (but potentially inaccurate)")
except np.linalg.LinAlgError:
    print("Matrix is singular")

# Bezpieczniejsza alternatywa
pinv_stable = np.linalg.pinv(A_ill_conditioned)
print("Pseudoinverse computed successfully")

# Problem: utrata precyzji w odejmowaniu
large = 1e16
small = 1.0
result = (large + small) - large  # Powinno być 1.0
print(f"Expected: 1.0, Got: {result}")

# Rozwiązanie: reorganizacja obliczeń
result_correct = small + (large - large)
print(f"Correct result: {result_correct}")
```

---

### 📚 Podsumowanie najważniejszych funkcji

```python
# Podstawowe operacje
np.dot(A, B)              # Mnożenie macierzy
np.linalg.norm(v)         # Norma wektora/macierzy
np.transpose(A)           # Transpozycja

# Decompositions
np.linalg.svd(A)          # Singular Value Decomposition
np.linalg.qr(A)           # QR Decomposition  
np.linalg.eig(A)          # Eigendecomposition

# Rozwiązywanie układów
np.linalg.solve(A, b)     # Ax = b
np.linalg.lstsq(A, b)     # Najmniejsze kwadraty
np.linalg.pinv(A)         # Pseudoinverse

# Właściwości macierzy
np.linalg.det(A)          # Wyznacznik
np.linalg.inv(A)          # Odwrotność
np.linalg.cond(A)         # Condition number
np.linalg.matrix_rank(A)  # Rząd macierzy
```

---

### 🔗 Powiązane tematy

- [[NumPy - Podstawy]] - Podstawowe operacje NumPy
- [[NumPy - Performance Optimization]] - Optymalizacja wydajności
- [[Machine Learning Pipeline - Preprocessing]] - Zastosowanie w ML
- [[Statistical Testing - Podstawy]] - Testy statystyczne z algebrą liniową