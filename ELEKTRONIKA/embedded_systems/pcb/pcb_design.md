# Projektowanie PCB - Kompendium dla Początkujących

Witaj w kompendium wiedzy o projektowaniu płytek drukowanych (PCB)! Ta kolekcja notatek obejmuje wszystkie kluczowe aspekty projektowania PCB, od podstawowych pojęć po zaawansowane techniki, specjalnie przygotowana dla osób rozpoczynających przygodę z projektowaniem elektroniki.

## 🎯 Cele edukacyjne

Po przejściu przez to kompendium będziesz potrafić:
- Zrozumieć podstawowe pojęcia związane z PCB
- Zaprojektować schemat elektryczny dla prostych układów
- Utworzyć layout PCB z właściwym routingiem
- Wybrać odpowiednie komponenty i obudowy
- Przygotować projekt do produkcji
- Unikać najczęstszych błędów projektowych

## 📋 Spis treści

### 🔧 Podstawy PCB
- **[[pcb_podstawy|Podstawy PCB]]** - Historia, rodzaje, materiały, podstawowe pojęcia
- **[[pcb_komponenty_elektroniczne|Komponenty Elektroniczne]]** - Przegląd elementów używanych w PCB
- **[[pcb_schemat_elektryczny|Schemat Elektryczny]]** - Projektowanie schematów, zasady, dobre praktyki
- **[[pcb_symbole_graficzne|Symbole Graficzne]]** - Standardowe symbole schematów elektronicznych
- **[[pcb_biblioteki_komponentow|Biblioteki Komponentów]]** - Tworzenie i zarządzanie bibliotekami

### 🎨 Projektowanie Layoutu
- **[[pcb_projekt_layoutu|Projekt Layoutu]]** - Proces projektowania layoutu PCB
- **[[pcb_warstwy_pcb|Warstwy PCB]]** - Struktura wielowarstwowych płytek
- **[[pcb_routing_sciezki|Routing Ścieżek]]** - Prowadzenie ścieżek, szerokości, odstępy
- **[[pcb_via_i_drillholes|Via i Otwory]]** - Rodzaje otworów, projektowanie via
- **[[pcb_plane_zasilania|Płaszczyzny Zasilania]]** - Projektowanie power planes
- **[[pcb_plane_masy|Płaszczyzny Masy]]** - Ground planes, techniki uziemienia

### ⚡ Zagadnienia Zaawansowane
- **[[pcb_impedancja_kontrolowana|Impedancja Kontrolowana]]** - Linie transmisyjne, dopasowanie impedancji
- **[[pcb_emi_emc|EMI/EMC]]** - Kompatybilność elektromagnetyczna, redukcja zakłóceń
- **[[pcb_thermal_management|Zarządzanie Cieplne]]** - Odprowadzanie ciepła, thermal vias
- **[[pcb_rozmiary_obudowy|Rozmiary i Obudowy]]** - Wymiary PCB, standardy, obudowy

### 🏭 Produkcja i Montaż
- **[[pcb_produkcja_wytwarzanie|Produkcja PCB]]** - Proces wytwarzania, specyfikacje techniczne
- **[[pcb_montaz_komponenow|Montaż Komponentów]]** - THT vs SMD, technologie montażu
- **[[pcb_testowanie_debug|Testowanie i Debug]]** - Metody testowania, rozwiązywanie problemów

### 🛠️ Narzędzia Projektowe
- **[[pcb_narzedzia_kicad|KiCad]]** - Darmowe narzędzie do projektowania PCB
- **[[pcb_narzedzia_altium|Altium Designer]]** - Profesjonalne narzędzie przemysłowe
- **[[pcb_narzedzia_eagle|EAGLE PCB]]** - Popularne narzędzie dla hobbystów

### 🚀 Praktyczne Zastosowania
- **[[pcb_projekty_praktyczne|Projekty Praktyczne]]** - Przykładowe projekty PCB krok po kroku
- **[[pcb_bledy_czestie|Częste Błędy]]** - Najczęstsze problemy i jak ich unikać
- **[[pcb_najlepsze_praktyki|Najlepsze Praktyki]]** - Sprawdzone metody projektowania

---

## 🎯 Jak korzystać z tego kompendium

### Dla kompletnie początkujących
1. Zacznij od [[pcb_podstawy|podstaw PCB]]
2. Poznaj [[pcb_komponenty_elektroniczne|komponenty elektroniczne]]
3. Naucz się [[pcb_schemat_elektryczny|projektować schematy]]
4. Wypróbuj [[pcb_narzedzia_kicad|KiCad]] - darmowe narzędzie

### Dla osób z podstawową wiedzą
1. Pogłęb wiedzę o [[pcb_projekt_layoutu|projektowaniu layoutu]]
2. Zrozum [[pcb_warstwy_pcb|strukturę warstw PCB]]
3. Naucz się [[pcb_routing_sciezki|właściwego routingu]]
4. Zapoznaj się z [[pcb_produkcja_wytwarzanie|procesem produkcji]]

### Dla średniozaawansowanych
1. Opanuj [[pcb_impedancja_kontrolowana|impedancję kontrolowaną]]
2. Zajmij się [[pcb_emi_emc|zagadnieniami EMI/EMC]]
3. Naucz się [[pcb_thermal_management|zarządzania cieplnego]]
4. Rozwijaj umiejętności w [[pcb_testowanie_debug|testowaniu i debugowaniu]]

---

## 💡 Kluczowe pojęcia

### Podstawowe terminy
- **PCB** - Printed Circuit Board (płytka drukowana)
- **Footprint** - fizyczny kształt komponentu na PCB
- **Pad** - miejsce lutowania komponentu
- **Via** - połączenie między warstwami
- **Track/Trace** - ścieżka przewodząca na PCB

### Warstwy PCB
- **Copper layer** - warstwa miedziana przewodząca
- **Solder mask** - maska lutownicza
- **Silk screen** - warstwa opisowa
- **Drill layer** - warstwa otworów

### Technologie montażu
- **THT** - Through-Hole Technology (montaż przewlekany)
- **SMD/SMT** - Surface Mount Technology (montaż powierzchniowy)
- **BGA** - Ball Grid Array
- **QFP** - Quad Flat Package

---

## 🔗 Przydatne zasoby

### Narzędzia CAD (bezpłatne)
- **[KiCad](https://kicad.org/)** - kompletny pakiet do projektowania PCB
- **[FreePCB](http://freepcb.com/)** - prosty edytor PCB
- **[LibrePCB](https://librepcb.org/)** - nowoczesne narzędzie open source

### Narzędzia komercyjne
- **[Altium Designer](https://www.altium.com/)** - standard przemysłowy
- **[EAGLE](https://www.autodesk.com/products/eagle/)** - popularne w środowisku makers
- **[OrCAD](https://www.orcad.com/)** - profesjonalne narzędzie

### Producenci PCB
- **[JLCPCB](https://jlcpcb.com/)** - tanie prototypy z Chin
- **[PCBWay](https://www.pcbway.com/)** - dobra jakość, rozsądne ceny
- **[EuroCircuits](https://www.eurocircuits.com/)** - europejski producent

### Bazy danych komponentów
- **[Octopart](https://octopart.com/)** - wyszukiwarka komponentów elektronicznych
- **[DigiKey](https://www.digikey.com/)** - duży dystrybutor z bazą danych
- **[Mouser](https://www.mouser.com/)** - alternatywny dystrybutor

---

## 📚 Metodologia nauki

### 1. Teoria + Praktyka
- Każdy temat zawiera przykłady praktyczne
- Teoretyczne podstawy wsparte wizualizacjami
- Projekty można bezpośrednio implementować

### 2. Podejście projektowe
- Wiedza organizowana wokół rzeczywistych projektów
- Od prostych układów do złożonych systemów
- Stopniowe wprowadzanie nowych konceptów

### 3. Powiązania między tematami
- Tematy są połączone linkami
- Łatwe nawigowanie między powiązanymi zagadnieniami
- Budowanie kompleksowej wiedzy

### 4. Rozwiązywanie problemów
- Typowe problemy i ich rozwiązania
- Debug tips i best practices
- Nauka z błędów

---

## 🎯 Ścieżki rozwoju

### Poziom podstawowy (0-3 miesiące)
- [ ] Zrozumienie podstaw PCB i komponentów
- [ ] Umiejętność czytania schematów
- [ ] Pierwszy prosty projekt w KiCad
- [ ] Podstawy routing'u i layout'u

### Poziom średniozaawansowany (3-12 miesięcy)
- [ ] Projektowanie wielowarstwowych PCB
- [ ] Zarządzanie impedancją i high-speed signals
- [ ] Zaawansowany routing i optymalizacja
- [ ] Przygotowywanie projektów do produkcji

### Poziom zaawansowany (1-2 lata)
- [ ] Projektowanie systemów high-frequency
- [ ] Zaawansowane zagadnienia EMI/EMC
- [ ] Optymalizacja termalna i mechaniczna
- [ ] Projektowanie dla manufacturing (DFM)

---

## 🤝 Współpraca i rozwój

To kompendium jest żywym dokumentem, który stale się rozwija. Każdy temat może być rozszerzany o nowe informacje, przykłady i projekty.

### Wskazówki do rozwoju
- Dodawaj nowe przykłady projektów
- Dokumentuj napotkane problemy i rozwiązania
- Rozszerzaj tematy o najnowsze technologie
- Twórz cross-linki między powiązanymi zagadnieniami

---

## 🔍 Szybka nawigacja

**Jestem początkującym** → Zacznij od [[pcb_podstawy|Podstaw PCB]]
**Znam podstawy** → Przejdź do [[pcb_projekt_layoutu|Projektowania Layoutu]]  
**Chcę się specjalizować** → Wybierz [[pcb_emi_emc|EMI/EMC]] lub [[pcb_impedancja_kontrolowana|High-Speed Design]]
**Szukam narzędzi** → Zobacz [[pcb_narzedzia_kicad|KiCad]] lub [[pcb_narzedzia_altium|Altium]]
**Mam problem** → Sprawdź [[pcb_bledy_czestie|Częste Błędy]] lub [[pcb_testowanie_debug|Testowanie]]

---

*Ostatnia aktualizacja: 2024*  
*Wersja: 1.0*  

**Powodzenia w projektowaniu PCB! 🚀**

## Powiązane tematy
- [[embedded_systems_index|Systemy Wbudowane - Główny Index]]
- [[projekty_i_cwiczenia|Projekty i Ćwiczenia Laboratoryjne]]
- [[debugging_embedded|Debugowanie Embedded]]
- [[interfejsy_sprzętowe|Interfejsy Sprzętowe]]