## Nadprzewodnictwo

### I. Wprowadzenie do Półprzewodników

Półprzewodniki to materiały o kluczowym znaczeniu dla współczesnej elektroniki, których przewodnictwo elektryczne plasuje się pomiędzy metalami (przewodnikami) a izolatorami (jak szkło). Ich unikalna właściwość polega na tym, że ich zachowanie przewodzące można precyzyjnie kontrolować pod wpływem czynników zewnętrznych, takich jak temperatura, promieniowanie czy pole elektryczne. Materiały te tworzą sieć krystaliczną, w której elektrony mogą przeskakiwać z pasma walencyjnego do pasma przewodnictwa po wzbudzeniu termicznym, tworząc elektrony i dziury – nośniki ładunku.

**Najważniejsze cechy i fakty:**

- **Definicja:** Materiał o przewodnictwie pomiędzy przewodnikami a izolatorami.
- **Kontrolowana przewodność:** Zachowanie przewodzące zmienia się pod wpływem temperatury, promieniowania, czy pola elektrycznego.
- **Struktura krystaliczna:** Elektrony z powłok atomowych mogą przeskakiwać z pasma walencyjnego do pasma przewodnictwa (wzbudzenie termiczne), generując elektrony i dziury.
- **Szerokość pasma wzbronionego (przerwa energetyczna):** Kluczowy parametr określający półprzewodnik. Dla krzemu (Si) wynosi około 1,1 eV. Jest to wartość wystarczająco mała dla wzbudzenia elektronów, ale na tyle duża, że w niskich temperaturach przewodność jest niewielka.
- **Ważne materiały półprzewodnikowe:Krzem (Si):** Najpowszechniej stosowany, np. w mikroprocesorach i tranzystorach MOSFET. Rocznie produkuje się 10^20 krzemowych tranzystorów.
- **German (Ge):** Wracający do łask w wysokich częstotliwościach i fotonice (0.66 eV).
- **Arsenek galu (GaAs):** Grupa III-V, stosowany w urządzeniach wysokoczęstotliwościowych (radar, telekomunikacja satelitarna) (1.4 eV).
- **Węglik krzemu (SiC):** Odporny na wysokie temperatury i napięcia, popularny w pojazdach elektrycznych.
- **Tlenki i azotki metali (np. ZnO, GaN):** Wykorzystywane w energoelektronice i optoelektronice (GaN: 3.4 eV, AlN: 6.2 eV, InN: 0.8 eV).
- **Półprzewodniki organiczne:** Stosowane w elastycznych ekranach OLED i ogniwach organicznych.

### II. Rodzaje Półprzewodników

**A. Półprzewodniki Samoistne (Intrinsic):**

- Czyste materiały bez domieszek chemicznych (np. krzem, german).
- Koncentracja elektronów i dziur jest identyczna, generowana przez wzbudzenie termiczne.
- Praktyczne zastosowanie ograniczone ze względu na niewielką przewodność w temperaturze pokojowej.

**B. Półprzewodniki Domieszkowane (Extrinsic):**

- Powstają przez wprowadzenie atomów domieszek w celu uzyskania pożądanych parametrów przewodzenia.
- **Typu n:** Powstaje przez dodanie pierwiastków z większą liczbą elektronów walencyjnych (np. fosfor, arsen). Nadmiar elektronów staje się większościowymi nośnikami ładunku. Poziom donorowy (Ed) znajduje się tuż poniżej pasma przewodnictwa.
- **Typu p:** Powstaje przez domieszkowanie pierwiastkami trójwartościowymi (np. bor, aluminium). Powodują one powstanie dziur, które stają się dominującymi nośnikami ładunku. Poziom akceptorowy (Ea) znajduje się tuż powyżej pasma walencyjnego.

### III. Kluczowe Elementy Elektroniki Półprzewodnikowej

**A. Złącze p-n (Dioda Półprzewodnikowa):**

- **Budowa:** Powstaje poprzez połączenie obszarów półprzewodnikowych typu p i typu n.
- **Działanie:** Przepływ nośników zachodzi aż do wyrównania poziomów Fermiego. Obszar typu p ładuje się ujemnie, a obszar typu n dodatnio, tworząc kontaktową różnicę potencjałów (V0).
- **Charakterystyka prądowo-napięciowa:** Nieliniowa. W kierunku przewodzenia (polaryzacja zgodna) prąd gwałtownie rośnie po przekroczeniu napięcia progowego. W kierunku zaporowym (polaryzacja wsteczna) płynie tylko niewielki prąd upływu, aż do napięcia przebicia lawinowego (np. w diodach Zenera).
- **Zastosowania:Prostowniki:** Przetwarzają prąd przemienny na prąd płynący w jednym kierunku (jedno- lub dwupołówkowe).
- **Diody Zenera:** Wykorzystują efekt przebicia lawinowego do stabilizacji napięcia.
- **Diody tunelowe:** Wykazują zakres ujemnej oporności, użyteczne w automatyce.
- **Baterie słoneczne (ogniwa fotowoltaiczne):** Zamieniają energię świetlną na elektryczną. Światło wzbudza elektrony z pasma walencyjnego do pasma przewodnictwa, tworząc pary elektron-dziura, które są rozdzielane przez pole elektryczne złącza p-n.
- **Fotokomórki:** Wykorzystują wzrost prądu pod wpływem oświetlenia.
- **Diody LED (Light Emitting Diodes):** Emitują światło podczas rekombinacji elektronów i dziur (np. GaAs – światło czerwone). Używane w wyświetlaczach cyfrowych, sygnalizatorach, laserach półprzewodnikowych (np. czytniki CD/DVD/BlueRay, komunikacja światłowodowa). Napięcie progowe od 1.5 do 3V w zależności od koloru.
- **Fotodiody:** Detektory światła widzialnego i podczerwonego, pracują przy polaryzacji zaporowej. Dzielą się na zwykłe, PIN (cienka warstwa samoistna, mała pojemność, mała bezwładność) i lawinowe (najbardziej czułe, wzmacniają sygnał wewnętrznie ok. 100 razy). Zastosowania: mierniki odległości, detektory w komunikacji światłowodowej, czujniki dymu, monitory pulsu.

**B. Tranzystory:**

- **Tranzystor bipolarny (BJT):Typy:** npn i pnp. Składa się z dwóch złączy p-n.
- **Zasada działania (npn):** Złącze emiter-baza (EB) spolaryzowane w kierunku przewodzenia, złącze baza-kolektor (BC) w kierunku zaporowym. Mała grubość bazy umożliwia wstrzykiwanie elektronów z emitera do kolektora, z niewielką rekombinacją w bazie.
- **Wzmocnienie prądowe (β):** Stosunek prądu kolektora do prądu bazy (typ. ok. 100).
- **Zastosowania:** Wzmacniacze sygnałów, przełączniki (np. w układy scalone).
- **Tranzystor unipolarny (FET/MOSFET):Zasada działania:** Złożony z półprzewodnika między elektrodą źródła (S) a drenu (D), który działa jak okładka kondensatora z bramką (G) jako drugą elektrodą. Zastosowanie napięcia na bramce kontroluje przewodnictwo kanału.
- **Zastosowania:** W układach scalonych (~99% tranzystorów to FET), technologia CMOS (komplementarne pary MOSFET typu p i n). Nowoczesne tranzystory (poniżej 32 nm) to FinFETy z trójwymiarowym kanałem.
- **Fototranzystory:** Tranzystory bipolarne (najczęściej npn) z oknem umożliwiającym oświetlenie obszaru bazy. Promieniowanie padające na bazę generuje nośniki, wzmacniając prąd. Są bardziej czułe od fotodiod, ale wolniejsze. Zastosowania: detektory podczerwieni, systemy zabezpieczające, piloty zdalnego sterowania.

**C. Inne Elementy Optoelektroniczne:**

- **Fotorezystory:** Bezzłączowe elementy półprzewodnikowe, których rezystancja silnie zmienia się pod wpływem światła. Maksymalna czułość dla określonej długości fali. Są czułe, ale wolne. Zastosowania: automatyczne włączanie lamp, mierniki światła, detektory podczerwieni.
- **Transoptory (optoizolatory):** Składają się z nadajnika (np. LED) i detektora światła (np. fototranzystor) w jednej obudowie. Służą do izolacji galwanicznej między obwodami, mogą przekazywać sygnały cyfrowe i analogowe.

### IV. Produkcja i Ekosystem Półprzewodników

**A. Globalny Łańcuch Dostaw:**

- **Skomplikowanie:** Produkcja półprzewodników jest niezwykle złożona, obejmując ponad 1000 etapów i wykorzystując około 300 materiałów, z 16000 dostawców na całym świecie. Żaden kraj ani region nie jest samowystarczalny.
- **Dominujące regiony:**USA: Badania i rozwój.
- Tajwan: Zaawansowane technologie produkcyjne (ponad 60% rynku foundry), najbardziej zaawansowane chipy (2-7 nm).
- Japonia: Produkcja płytek.
- Chiny: Surowce.
- Holandia: Kluczowy sprzęt do produkcji (np. ASML).
- **Etapy produkcji:Front-end:** Konwersja krzemu na zaprojektowane płytki krzemowe. Proces wysoce techniczny, kapitałochłonny, wymaga wysoko wykwalifikowanych pracowników (litografia, trawienie, implantacja jonowa).
- **Back-end:** Testowanie i pakowanie układów scalonych z płytek krzemowych. Mniej kapitałochłonny, ale coraz bardziej zaawansowany (pakowanie 2.5D/3D, heterogeniczna integracja).

**B. Europejski Chips Act (ECA):**

- **Cel:** Zwiększenie udziału UE w globalnej produkcji półprzewodników z 10% do 20% do 2030 roku.
- **Finansowanie:** 43 mld EUR z funduszy wspólnotowych do 2030 roku na obniżenie kosztów wejścia na rynek.

1. **Trzy filary:"Chips for Europe":** Wsparcie transferu wiedzy z laboratorium do fabryki, industrializacja innowacyjnych technologii (3.3 mld EUR). Obejmuje tworzenie linii pilotażowych, platformy projektowej, centrów kompetencyjnych, rozwój chipów kwantowych.
2. **Inwestycje w zakłady produkcyjne:** Zachęcanie do inwestycji publicznych i prywatnych, wsparcie MŚP. Pomoc tylko dla obiektów nowatorskich („first-of-a-kind”).
3. **Mechanizm koordynacji:** Zacieśnienie współpracy między państwami członkowskimi i Komisją, monitorowanie dostaw, szacowanie popytu.

- **Kierunki rozwoju:** Inwestycje w centra innowacji i start-upy. Trwają prace nad Chips Act 2.0 (planowane na 2025 rok) z szerszym zakresem wsparcia, obejmującym również centra projektowe, dostawców materiałów i sprzętu oraz inicjatywy badawczo-rozwojowe.

**C. Ekosystem Półprzewodników w Polsce (stan na 2025):**

- **Polska jako strategiczny partner:** Pozycja Polski w europejskim łańcuchu dostaw rośnie, zwłaszcza w kontekście planowanej fabryki TSMC w Dreźnie (100 km od granicy). Polska jest postrzegana jako integralna część "europejskiego trójkąta półprzewodnikowego" (Drezno-Praga-Wrocław).
- **Współpraca z Tajwanem:** Aktywne działania PAIH (Polska Agencja Inwestycji i Handlu) w promocji Polski na Tajwanie, misje badawczo-rozwojowe, udział w targach Semicon Taiwan, powołanie polsko-tajwańskiej grupy ds. półprzewodników.
- **Wiodący inwestorzy i firmy:Intel Technology Poland (Gdańsk):** Największe centrum technologiczne R&D Intela w Europie, zatrudnia 4000 osób, specjalizuje się w oprogramowaniu (PC, serwery, sieci, AI, 5G). W 2023 Intel ogłosił plany budowy zakładu integracji i testowania półprzewodników w Miękini pod Wrocławiem (wstrzymane w 2024, ostatecznie zrezygnowano w 2025).
- **SK Hynix (Gdańsk):** Otworzył Centrum Badań i Rozwoju w 2024, specjalizuje się w technologiach pamięci NAND flash.
- **Solidigm (Gdańsk):** Powstało w 2021 z przejęcia części Intela przez SK Hynix, dostawca innowacyjnych rozwiązań pamięci NAND flash.
- **Nordic Semiconductors (Kraków):** Rozwój technologii bezprzewodowych (Bluetooth Low Energy, IoT).
- **Analog Devices (Kraków):** Projektowanie półprzewodnikowych układów scalonych, specjalizacja w konwerterach.
- **Sii Polska:** Dostawca usług doradztwa technologicznego, transformacji cyfrowej, inżynierii i usług biznesowych, kompetencje w obszarze półprzewodników (firmware, BIOS, sterowniki graficzne, urządzenia sieciowe, FPGA, AI).
- **Digital Core Design (Bytom):** Projektowanie specjalizowanych układów scalonych (IP Core, SoC) od ponad 25 lat, klientami są m.in. VW, Toyota, Sony, Bosch.
- **ChipCraft (Warszawa):** Projektowanie bloków składowych analogowych i cyfrowych układów scalonych, specjalizacja w nawigacji GNSS.
- **Silicon Creations (Polska):** Projektowanie układów taktowania (PLL), oscylatorów, SerDes, LVDS I/O.
- **Phison / Wilk Elektronik j.v.:** Rozwój firmware dla dysków SSD i pamięci flash, rozważana technologia aiDAPTIV+ dla cyberbezpieczeństwa.
- **Openchip (Gdańsk):** Otworzyło centrum R&D w 2025, koncentruje się na systemach akceleracyjnych dla wysokowydajnych obliczeń (HPC) i System-on-Chip (SoC) na architekturze RISC-V.
- **Graphcore (Gdańsk):** Centrum R&D, projektuje procesory IPU (Intelligence Processing Unit) dla sztucznej inteligencji.
- **Phonemic (Lublin):** Projekty i weryfikacja RTL oraz firmware dla FPGA i specjalizowanych układów scalonych (5G, LTE, kryptografia).
- **OmniChip (Warszawa):** Projektuje układy scalone na zlecenie, opracowuje produkty i bloki IP.
- **Synopsys (Gdańsk):** Dostawca oprogramowania EDA (Electronic Design Automation), IP Core, wsparcie prototypowania i testowania.
- **ALDEC-ADT (Polska):** Producent oprogramowania do projektowania układów scalonych FPGA i ASIC.
- **ENSEMBLE³:** Centrum doskonałości w nanofotonice, materiałach i technologiach wzrostu kryształów (GaAs, InAs, GaP, InP, GaSb, SiC, tlenki).
- **VIGO Photonics (Warszawa):** Lider w fotonowych detektorach średniej podczerwieni, oferuje epitaksjalne warstwy półprzewodnikowe. Realizuje projekt HyperPIC (453.7 mln PLN dofinansowania UE) na rozwój zintegrowanych fotonicznych układów scalonych.
- **Kubara Lamina:** Produkcja półprzewodników dużych mocy (diody, tyrystory), wyrobów mikrofalowych.
- **TopGaN:** Produkcja zaawansowanych emiterów światła widzialnego i UV GaN (diody laserowe).
- **PCC Rokita:** Technologia wytwarzania tlenochlorku fosforu (POCl3) o wysokiej czystości dla produkcji farmaceutycznej i półprzewodnikowej.
- **CRW Telesystem Mesko:** B+R i produkcja dla przemysłu obronnego, unikalne fotodetektory InSb i PbS.
- **ResQuant (Łódź):** Polską firma deep-tech, specjalizująca się w sprzętowej implementacji standardów kryptografii postkwantowej (PQC), projektuje koprocesory kryptograficzne. Planuje produkcję prototypów w technologii 22 nm w fabrykach GlobalFoundries w Dreźnie.
- **SemiQa:** Pionier technologii ANNET (analogowych sieci neuronowych) dla aplikacji AI (50x szybsze, 5x niższe zużycie energii).
- **XTPL:** Ultraprecyzyjna depozycja i nanotusze do tworzenia nanostruktur dla półprzewodników, wyświetlaczy, biosensorów, PCB. Alternatywa dla fotolitografii.
- **ASYS Polska:** Produkcja przemysłowych robotów dla branży półprzewodnikowej.
- **Insoptics:** Produkcja urządzeń spektroskopowych do monitorowania procesów plazmowych.
- **Instytut Fotonowy:** Prototypy i unikalne urządzenia do charakteryzacji półprzewodników, fotoelektrochemii.
- **TRUMPF Huettinger:** Rozwija zasilacze dużej mocy (generatory plazmowe) i zasilanie do laserów, używane m.in. w maszynach ASML do produkcji półprzewodników.
- **Systerion:** Urządzenia do nanopozycjonowania i nanowyrównywania z ultra wysoką precyzją.
- **QNA Technology:** Rozwój technologii produkcji nanomateriałów półprzewodnikowych (kropek kwantowych) do wyświetlaczy.
- **Noctiluca:** Rozwój i produkcja zaawansowanych związków chemicznych dla wyświetlaczy OLED.
- **NanoresLAB:** Laboratorium nanotechnologiczne wspierające przemysł półprzewodnikowy w testowaniu i analizie struktur (SEM, FIB, TEM, EDS, CT).
- **Polskie Instytuty Badawcze:Łukasiewicz – IMiF:** Opracowuje konstrukcje i technologie wytwarzania mikro- i optoelektronicznych przyrządów, nowych materiałów (GaN, grafen, kompozyty ceramiczno-metalowe). Lider Centrum Kompetencji Mikroelektroniki i Fotoniki (projekt za 519.7 mln PLN, dofinansowanie UE 370.0 mln PLN).
- **CEZAMAT (Politechnika Warszawska):** Kompleks laboratoriów badawczych w dziedzinie mikroelektroniki, optoelektroniki, nanoelektroniki i bioelektroniki. Członek projektu PIXEurope.
- **Unipress (Instytut Wysokich Ciśnień PAN):** Wiodący ośrodek w dziedzinie fizyki i technologii półprzewodników, zwłaszcza krystalizacji objętościowych kryształów azotku galu (GaN). Członek projektu WBG Pilot Line (50 mln EUR).
- **Kadry dla branży:** Polska zajmuje 4. miejsce w Europie pod względem liczby absolwentów kierunków technicznych (STEM), a odsetek kobiet wynosi 43%. Uczelnie współpracują z przemysłem (np. Politechnika Wrocławska, Politechnika Gdańska z Intelem i Synopsys) w celu dostosowania programów nauczania.
- **Wsparcie rządowe:Program wspierania inwestycji o istotnym znaczeniu dla gospodarki polskiej (2011-2030):** Dofinansowanie dużych inwestycji strategicznych i średniej wielkości innowacyjnych projektów.
- **Krajowe Ramy Wspierania Strategicznych Inwestycji Półprzewodnikowych:** Budżet 1.5 mld USD, wsparcie projektów rozwijających produkcję półprzewodników w Polsce (wymóg min. 850 mln PLN inwestycji i 100 miejsc pracy).
- **Ulgi podatkowe:** Ulga B+R, ulga na innowacyjnego pracownika, ulga na robotyzację, ulga na prototyp.

### V. Nadprzewodnictwo

Nadprzewodnictwo to kwantowe zjawisko fizyczne charakteryzujące się zerową rezystancją elektryczną i wypychaniem pola magnetycznego (efekt Meissnera) z materiału, gdy przechodzi on w stan nadprzewodzący poniżej określonej temperatury krytycznej (Tc).

**A. Kluczowe Właściwości i Odkrycia:**

- **Zerowa rezystancja:** Brak oporu dla przepływu prądu elektrycznego. Odkryte w 1911 roku przez Heike Kamerlingha Onnesa dla rtęci w temperaturze 4.2 K.
- **Efekt Meissnera:** Wypychanie pola magnetycznego z wnętrza nadprzewodnika. Odkryte w 1933 roku przez Walthera Meissnera i Roberta Ochsenfelda. Jest to podstawowa cecha odróżniająca nadprzewodnik od idealnego przewodnika. Powoduje lewitację nadprzewodnika nad magnesem.
- **Temperatura krytyczna (Tc):** Temperatura, poniżej której materiał staje się nadprzewodnikiem. Zależy od materiału, ciśnienia i pola magnetycznego.
- **Kwantowy charakter:** Zjawisko niemożliwe do wyjaśnienia na gruncie fizyki klasycznej.

**B. Teorie Nadprzewodnictwa:**

- **Fenomenologiczne:Teoria Londonów (1935):** Opisuje zanik oporu i efekt Meissnera za pomocą równań, ale bez wyjaśniania przyczyn mikroskopowych. Wyprowadziła głębokość wnikania pola magnetycznego (λ).
- **Teoria Ginzburga-Landaua (1950):** Oparta na teorii przejść fazowych Landaua, wprowadziła parametry efektywne, ale nie wyjaśniła ich postaci.
- **Mikroskopowe:Teoria BCS (Bardeena, Coopera, Schrieffera) (1957):** Pierwsza mikroskopowa teoria, która wyjaśniła fizyczne podstawy nadprzewodnictwa.
- **Pary Coopera:** Elektrony przenoszą prąd w parach o przeciwnych spinach, tworząc bozony (całkowity spin 0). Teoria BCS zakłada, że elektrony blisko powierzchni Fermiego oddziałują ze sobą za pośrednictwem drgań sieci krystalicznej (fononów), co prowadzi do ich sparowania.
- **Kondensacja Bosego-Einsteina:** Pary Coopera, będąc bozonami, mogą kondensować na jednym poziomie energetycznym, co umożliwia im ruch bez oporu.
- **Przerwa energetyczna:** Wszystkie pary zajmują te same poziomy energetyczne, tworząc przerwę energetyczną, której pokonanie wymaga energii, co zapobiega rozpraszaniu pojedynczych elektronów.

**C. Rodzaje Nadprzewodników:**

- **I rodzaju:** Nadprzewodnictwo zanika całkowicie po przekroczeniu krytycznego pola magnetycznego (Bc).
- **II rodzaju:** W przedziale między dolnym (Bc1) a górnym (Bc2) polem krytycznym występuje stan mieszany (wirów magnetycznych / fluksonów), gdzie współistnieją obszary nadprzewodzące i normalne. Wewnątrz fluksonów pole magnetyczne jest uwięzione. Niszczenie stanu nadprzewodzącego następuje dopiero przy Bc2. Prąd krytyczny zależy od siły zaczepiania fluksonów przez defekty sieci.
- **Wysokotemperaturowe (HTS):** Odkryte w 1986 roku (Bednorz i Müller, 35 K), działają w temperaturach powyżej temperatury wrzenia ciekłego azotu (77 K, czyli -196 °C). Wcześniej uważane za izolatory. Mimo postępów, nadal są to temperatury zbyt niskie dla opłacalnych zastosowań przemysłowych (poszukuje się nadprzewodnictwa w temperaturze pokojowej).
- **Ferromagnetyczne:** Nowa grupa nadprzewodników (np. UGe2).

**D. Zastosowania Nadprzewodników:**

- **Energetyka:** Linie przesyłowe bez strat (kriokable z ciekłym wodorem lub helem).
- **Magnesy nadprzewodzące:** Generują silne pola magnetyczne przy niewielkim zużyciu energii (ciekły hel). Stosowane w:
- Aparatach MRI (obrazowanie rezonansem magnetycznym).
- Spektroskopach NMR (obrazowanie reakcji chemicznych).
- Akceleratorach cząstek elementarnych.
- Nadprzewodnikowych zasobnikach energii.
- Przemysłowych generatorach plazmy.
- **Trakcja na poduszce magnetycznej (Maglev):** Pociągi lewitujące nad torami dzięki siłom odpychania magnesów.
- **Tranzystory nadprzewodzące:** Wykorzystują zjawisko Josephsona, miniaturowe (3 μm).
- **Supertrony:** Nadprzewodzące soczewki wiązek elektronów, wykorzystujące efekt Meissnera do ogniskowania wiązki. Stosowane do emitowania spójnego promieniowania elektromagnetycznego.
- **Łożyska nadprzewodzące:** Wykorzystują lewitację magnesu nad nadprzewodnikiem. Mogą osiągać bardzo wysokie prędkości obrotowe (np. 135 000 obr/min).
- **Bolometry:** Urządzenia do detekcji promieniowania (w szerokim zakresie częstotliwości, np. fale milimetrowe, daleka podczerwień), wykorzystują silną zależność oporności nadprzewodnika od temperatury w zakresie przejścia.
- **SQUID (Superconducting Quantum Interference Device):** Nadprzewodzący interferometr kwantowy, do elektroniki bardzo słabych sygnałów.


![[Globalny_wyścig_o_chipy.mp4]]

![[Nadprzewodniki,_Półprzewodniki_i_Polska_w_Globalnym_Wyścigu_o_C.m4a]]

![[Od_Krzemu_po_Lewitację__Fascynująca_Podróż_przez_Świat_Półprzew.m4a]]

