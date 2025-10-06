# Podstawy PCB - Printed Circuit Board

## 🎯 Czym jest PCB?

**PCB** (Printed Circuit Board) to płytka drukowana - podstawa każdego nowoczesnego urządzenia elektronicznego. To wielowarstwowa struktura, która mechanicznie wspiera komponenty elektroniczne i elektryczne je łączy poprzez przewodzące ścieżki.

## 📚 Historia PCB

### Początki
- **1936** - Paul Eisler wynajduje pierwszą płytkę drukowaną w Austrii
- **Lata 40.** - rozwój technologii dla potrzeb wojskowych (radar)
- **Lata 50.** - komercjalizacja technologii PCB
- **Lata 60.** - wprowadzenie płytek wielowarstwowych

### Ewolucja technologii
- **THT** (Through-Hole Technology) - dominacja do lat 80.
- **SMT** (Surface Mount Technology) - rewolucja miniaturyzacji
- **HDI** (High Density Interconnect) - nowoczesne aplikacje

## 🧱 Budowa PCB

### Podstawowe elementy

#### 1. Substrat (Core)
- **Materiał**: najczęściej FR-4 (fiberglass + żywica epoksydowa)
- **Grubość**: standardowo 1.6mm, dostępne 0.8mm, 1.0mm, 2.0mm
- **Właściwości**: izolacyjne, mechaniczne, termiczne

#### 2. Warstwy miedziowane
- **Grubość**: standardowo 35μm (1oz), dostępne 17μm, 70μm
- **Funkcja**: przewodzenie sygnałów i zasilania
- **Powlekanie**: zwykle cyną lub HASL

#### 3. Maska lutownicza (Solder Mask)
- **Kolor**: zielony (standard), czerwony, niebieski, czarny
- **Funkcja**: ochrona przed utlenianiem i zwarciem
- **Otwory**: pada dla komponentów

#### 4. Legenda (Silk Screen)
- **Kolor**: biały (standard), czarny, żółty
- **Zawartość**: oznaczenia komponentów, tekst, loga
- **Grubość**: minimum 0.15mm dla tekstu

## 🔢 Rodzaje PCB

### Według liczby warstw

#### 1. Jednowarstwowe (Single Layer)
- **Zastosowanie**: proste układy, prototypy
- **Koszt**: najniższy
- **Ograniczenia**: routing tylko z jednej strony

#### 2. Dwuwarstwowe (Double Layer)  
- **Zastosowanie**: większość projektów hobbystycznych
- **Zalety**: routing z obu stron, płaszczyzna masy
- **Koszt**: umiarkowany

#### 3. Wielowarstwowe (Multi-Layer)
- **4-warstwy**: standard dla projektów komercyjnych
- **6+ warstw**: zaawansowane systemy, high-speed
- **Zalety**: lepsza separacja sygnałów, EMI

### Według technologii montażu

#### THT (Through-Hole Technology)
- **Komponenty**: przewlekane przez otwory
- **Zalety**: mocne połączenia, łatwa naprawa
- **Wady**: większe rozmiary, gorszy routing

#### SMT (Surface Mount Technology)
- **Komponenty**: montowane na powierzchni
- **Zalety**: miniaturyzacja, automatyzacja produkcji
- **Wady**: trudniejsza naprawa, wymagają specjalne narzędzia

#### Mixed Technology
- **Kombinacja**: THT dla większych elementów, SMT dla reszty
- **Zastosowanie**: większość nowoczesnych PCB

## 📏 Standardowe rozmiary

### Popularne formaty
- **Arduino Uno**: 68.6 x 53.4 mm
- **Raspberry Pi**: 85 x 56 mm  
- **Euro Card**: 100 x 160 mm
- **Credit Card**: 85.6 x 53.98 mm

### Grubości standardowe
- **0.8mm**: cienkie aplikacje, flex PCB
- **1.0mm**: kompaktowe urządzenia
- **1.6mm**: standard przemysłowy
- **2.0mm**: aplikacje wymagające sztywności

## ⚡ Podstawowe pojęcia

### Terminologia
- **Pad**: miejsce lutowania komponentu
- **Via**: połączenie między warstwami
- **Track/Trace**: ścieżka przewodząca
- **Footprint**: fizyczny kształt komponentu na PCB
- **Drill**: otwór w PCB
- **Annular ring**: pierścień miedzi wokół otworu

### Jednostki miary
- **mil**: 1/1000 cala = 0.0254 mm
- **mm**: milimetr (preferowany w projektowaniu)
- **inch**: cal = 25.4 mm

## 🎨 Proces projektowania

### 1. Specyfikacja wymagań
- Funkcjonalność układu
- Rozmiary i ograniczenia mechaniczne  
- Warunki środowiskowe
- Budżet produkcji

### 2. Schemat elektryczny  
- Wybór komponentów
- Połączenia elektryczne
- Weryfikacja projektu
- → Zobacz [[pcb_schemat_elektryczny|Schemat Elektryczny]]

### 3. Projekt layoutu
- Rozmieszczenie komponentów
- Routing ścieżek
- Optymalizacja
- → Zobacz [[pcb_projekt_layoutu|Projekt Layoutu]]

### 4. Weryfikacja i testy
- DRC (Design Rule Check)
- Symulacje
- Prototyp i testy
- → Zobacz [[pcb_testowanie_debug|Testowanie i Debug]]

## 🏭 Materiały PCB

### FR-4 (Fire Retardant 4)
- **Skład**: włókno szklane + żywica epoksydowa
- **Zastosowanie**: 95% wszystkich PCB
- **Właściwości**: dobra izolacja, wytrzymałość mechaniczna
- **Temperatura**: do 130°C

### Alternatywne materiały
- **CEM-1**: tańszy substrat dla prostych aplikacji
- **Polyimide**: wysokie temperatury, aplikacje flex
- **Rogers**: high-frequency, kontrolowana impedancja
- **Aluminum**: odprowadzanie ciepła, LED

## 🔍 Design Rules (zasady projektowania)

### Minimalne wymiary
- **Track width**: 0.1mm (producenci budget), 0.15mm (bezpieczny)
- **Via size**: 0.2mm drill, 0.4mm pad
- **Spacing**: 0.1mm między ścieżkami
- **Drill size**: minimum 0.15mm

### Zasady bezpieczeństwa
- **Clearance**: minimum 0.2mm od krawędzi
- **Annular ring**: minimum 0.05mm
- **Mask expansion**: 0.1mm większe od pada

## 💰 Koszty produkcji

### Czynniki wpływające na koszt
1. **Rozmiar płytki** - większe = droższe
2. **Liczba warstw** - więcej = droższe  
3. **Ilość otworów** - więcej = droższe
4. **Powierzchnia miedzi** - więcej = droższe
5. **Tolerancje** - precyzyjniejsze = droższe

### Optymalizacja kosztów
- Standardowe grubości (1.6mm)
- Popularne rozmiary (100x100mm max dla tanich)
- Minimalna liczba warstw
- Unikanie małych otworów (<0.2mm)

## 🚀 Zalety PCB vs alternatywy

### PCB vs przewody
- ✅ Kompaktowość i organizacja
- ✅ Powtarzalność produkcji
- ✅ Niezawodność połączeń
- ✅ Wsparcie mechaniczne

### PCB vs perfboard
- ✅ Profesjonalny wygląd
- ✅ Automatyczna produkcja
- ✅ Lepsza wydajność elektryczna
- ❌ Większy koszt prototypu

## 📊 Trendy w technologii PCB

### Miniaturyzacja
- Mniejsze komponenty (0201, 01005)
- Większa gęstość układu
- HDI (High Density Interconnect)
- Embedded components

### High-Speed Design
- Kontrolowana impedancja
- Differential pairs
- Length matching
- → Zobacz [[pcb_impedancja_kontrolowana|Impedancja Kontrolowana]]

### Środowisko
- Lead-free soldering (RoHS)
- Recyclable materials
- Energy efficient manufacturing

## 🔗 Powiązane tematy
- [[pcb_komponenty_elektroniczne|Komponenty Elektroniczne]] - przegląd elementów PCB
- [[pcb_schemat_elektryczny|Schemat Elektryczny]] - projektowanie schematów
- [[pcb_projekt_layoutu|Projekt Layoutu]] - proces layoutu
- [[pcb_warstwy_pcb|Warstwy PCB]] - struktura wielowarstwowa
- [[pcb_narzedzia_kicad|KiCad]] - narzędzia do projektowania
- [[pcb_najlepsze_praktyki|Najlepsze Praktyki]] - sprawdzone metody

---

**🎯 Co dalej?**
Po opanowaniu podstaw PCB, przejdź do [[pcb_komponenty_elektroniczne|Komponentów Elektronicznych]] aby poznać elementy używane w projektowaniu płytek drukowanych.