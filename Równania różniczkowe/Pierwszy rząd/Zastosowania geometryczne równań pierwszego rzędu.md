# Zastosowania geometryczne równań pierwszego rzędu

## 🎯 Wprowadzenie

Równania różniczkowe pierwszego rzędu znajdują szerokie zastosowanie w geometrii analitycznej, pozwalając na:
- Znajdowanie krzywych o zadanych właściwościach geometrycznych
- Rozwiązywanie problemów dotyczących stycznych, normalnych
- Analizę trajektorii i ścieżek
- Badanie ortogonalnych trajektorii

## 📐 Podstawowe pojęcia geometryczne

### Nachylenie stycznej
Dla krzywej $y = f(x)$, nachylenie stycznej w punkcie $(x,y)$ to:
$$m = \frac{dy}{dx}$$

### Kąt między krzywymi
Kąt $\theta$ między dwiema krzywymi w punkcie przecięcia:
$$\tan \theta = \left|\frac{m_1 - m_2}{1 + m_1 m_2}\right|$$

gdzie $m_1$ i $m_2$ to nachylenia stycznych.

## 📝 Klasyczne przykłady

### Przykład 1: Krzywe o stałym nachyleniu stycznej
**Problem:** Znajdź krzywe, których styczna tworzy stały kąt $\alpha$ z osią $x$.

#### Rozwiązanie:
1. **Warunek:** $\frac{dy}{dx} = \tan \alpha = c$ (stała)
2. **Całkowanie:** $y = cx + C$
3. **Rozwiązanie:** Rodzina prostych

### Przykład 2: Krzywe przechodząc przez początek układu
**Problem:** Znajdź krzywe, dla których odcinek stycznej od punktu styczności do osi $x$ ma stałą długość $a$.

#### Rozwiązanie:
1. **Równanie stycznej:** $Y - y = y'(X - x)$
2. **Przecięcie z osią $x$:** $Y = 0$ → $X = x - \frac{y}{y'}$
3. **Długość odcinka:** $|x - (x - \frac{y}{y'})| = \frac{|y|}{|y'|} = a$
4. **Równanie różniczkowe:** $\frac{y}{y'} = \pm a$
5. **Rozwiązanie:** $y' = \pm \frac{y}{a}$
6. **Całkując:** $y = Ce^{\pm x/a}$

### Przykład 3: Trajektorie ortogonalne
**Problem:** Znajdź trajektorie ortogonalne do rodziny krzywych $x^2 + y^2 = C$.

#### Rozwiązanie:
1. **Różniczkowanie rodziny bazowej:**
   $2x + 2y\frac{dy}{dx} = 0$ → $\frac{dy}{dx} = -\frac{x}{y}$

2. **Warunek ortogonalności:**
   Nachylenia się przeciwnie odwracają: $\frac{dy}{dx} = \frac{y}{x}$

3. **Rozwiązanie równania:**
   $\frac{dy}{y} = \frac{dx}{x}$ → $\ln|y| = \ln|x| + \ln|K|$

4. **Trajektorie ortogonalne:** $y = Kx$ (proste przez początek)

## 🌟 Zastosowania w fizyce i inżynierii

### 1. Linie sił pola elektrostatycznego
**Równanie pola:** $\vec{E} = -\nabla V$

Linie sił są ortogonalne do ekwipotencjałów:
$$\frac{dy}{dx} = \frac{E_y}{E_x}$$

### 2. Trajektorie cząstek
**Dla cząstki w polu siłowym:**
$$m\frac{d^2\vec{r}}{dt^2} = \vec{F}(\vec{r})$$

W przypadku 2D można wyprowadzić równanie na trajektorię $y(x)$.

### 3. Linie prądu w hydrodynamice
**Równanie kontinuacji:**
$$\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \vec{v}) = 0$$

Linie prądu spełniają: $\frac{dy}{dx} = \frac{v_y}{v_x}$

## 🎨 Problemy konstrukcyjne

### Problem enveloppe (obwiedni)
**Definicja:** Obwiednia rodziny krzywych to krzywa styczna do każdej krzywej z rodziny.

**Metoda znajdowania:**
1. Rodzina krzywych: $F(x,y,c) = 0$
2. Warunek: $\frac{\partial F}{\partial c} = 0$
3. Eliminuj parametr $c$ z obu równań

#### Przykład: Obwiednia rodziny prostych
**Rodzina:** $y = mx + \frac{a^2}{m}$ (styczne do paraboli)

1. **Warunek:** $\frac{\partial}{\partial m}(y - mx - \frac{a^2}{m}) = -x + \frac{a^2}{m^2} = 0$
2. **Stąd:** $m^2 = \frac{a^2}{x}$ → $m = \pm \frac{a}{\sqrt{x}}$
3. **Podstawiając:** $y = \pm a\sqrt{x} + \frac{a^2}{\pm a/\sqrt{x}} = \pm a\sqrt{x} \pm a\sqrt{x} = \pm 2a\sqrt{x}$
4. **Obwiednia:** $y^2 = 4a^2x$ (parabola)

## 📊 Klasyfikacja problemów geometrycznych

| Typ problemu | Równanie | Przykład |
|--------------|----------|----------|
| **Stałe nachylenie** | $y' = c$ | Proste równoległe |
| **Nachylenie funkcją $x$** | $y' = f(x)$ | $y' = x$ → parabole |
| **Nachylenie funkcją $y$** | $y' = g(y)$ | $y' = y$ → eksponenty |
| **Nachylenie funkcją $(x,y)$** | $y' = h(x,y)$ | Pola kierunkowe |

## 🔄 Trajektorie ortogonalne - metoda ogólna

### Algorytm:
1. **Dana rodzina:** $\Phi(x,y,c) = 0$
2. **Różniczkuj:** Otrzymaj $\frac{dy}{dx} = f(x,y)$
3. **Ortogonalność:** $\frac{dy}{dx} = -\frac{1}{f(x,y)}$
4. **Rozwiąż** nowe równanie różniczkowe

### Zastosowania:
- **Linie sił i ekwipotencjały** w fizyce
- **Linie prądu i linie potencjału** w hydrodynamice  
- **Trajektorie cząstek** w polach siłowych

## ⚙️ Metody numeryczne w geometrii

### Metoda Eulera dla trajektorii:
$$x_{n+1} = x_n + h$$
$$y_{n+1} = y_n + h \cdot f(x_n, y_n)$$

Pozwala na śledzenie krzywych całkowych numerycznie.

## 🔗 Powiązane tematy

- [[Równania o zmiennych rozdzielonych]]
- [[Równania jednorodne pierwszego rzędu]]
- [[Pole kierunkowe]] 
- [[Krzywe parametryczne]]
- [[Geometria różniczkowa]]

## 📖 Terminologia angielska

| Polski | English |
|--------|---------|
| Trajektorie ortogonalne | Orthogonal trajectories |
| Nachylenie stycznej | Slope of tangent |
| Obwiednia | Envelope |
| Linie sił | Field lines |
| Ekwipotencjały | Equipotentials |
| Pole kierunkowe | Direction field |
| Krzywe całkowe | Integral curves |

## 🎯 Przykłady do ćwiczeń

1. Znajdź trajektorie ortogonalne do $y = cx^2$
2. Znajdź krzywę, której normalna w każdym punkcie przechodzi przez początek
3. Znajdź obwiednię rodziny okręgów o środkach na osi $x$ i promieniu równym odległości środka od początku

---
*Notatka utworzona: {{date}} | Ostatnia aktualizacja: {{date}}*