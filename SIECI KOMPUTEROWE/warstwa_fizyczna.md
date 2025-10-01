# 1️⃣ Warstwa Fizyczna (Physical Layer)

## 📋 Definicja

Warstwa fizyczna jest najniższą warstwą modelu OSI. Odpowiada za transmisję nieprzetworzonego strumienia bitów przez medium fizyczne. Określa charakterystykę elektryczną, mechaniczną i funkcjonalną interfejsu fizycznego.

## 🔧 Główne Funkcje

- **Transmisja bitów**: Przekształcanie bitów (0 i 1) na sygnały elektryczne, świetlne lub radiowe
- **Kodowanie sygnału**: Definiowanie jak przedstawić bit 0 i 1
- **Synchronizacja bitów**: Zapewnienie synchronizacji zegara między nadajnikiem a odbiornikiem
- **Kontrola Medium**: Określenie kiedy i jak urządzenie może przesyłać dane

## 🌐 Media Transmisyjne

### 1. Kable miedziane

#### Skrętka (UTP/STP)
```
Kategorie:
- Cat 5e:  100 MHz, 1 Gbps (do 100m)
- Cat 6:   250 MHz, 1 Gbps (do 100m), 10 Gbps (do 55m)
- Cat 6a:  500 MHz, 10 Gbps (do 100m)
- Cat 7:   600 MHz, 10 Gbps (do 100m)
- Cat 8:   2000 MHz, 25-40 Gbps (do 30m)
```

**Typy skrętek**:
- **UTP** (Unshielded Twisted Pair) - bez ekranowania
- **STP** (Shielded Twisted Pair) - z ekranowaniem
- **FTP** (Foiled Twisted Pair) - z folią aluminiową

#### Kabel koncentryczny
- **Zastosowanie**: Telewizja kablowa, sieci legacy
- **Typy**: RG-58 (thin), RG-59 (CATV), RG-6 (CATV/SAT)

### 2. Światłowody (Fiber Optic)

#### Single-mode (SM)
- **Rdzeń**: 8-10 μm
- **Zasięg**: Do 100 km+
- **Zastosowanie**: Sieci WAN, backbone
- **Długość fali**: 1310 nm, 1550 nm

#### Multi-mode (MM)
- **Rdzeń**: 50-62.5 μm
- **Zasięg**: Do 2 km
- **Zastosowanie**: Sieci LAN, data center
- **Długość fali**: 850 nm, 1300 nm

**Zalety światłowodów**:
- Odporność na zakłócenia elektromagnetyczne
- Bardzo duża przepustowość
- Niskie tłumienie sygnału
- Bezpieczeństwo (trudne do podsłuchu)

### 3. Media bezprzewodowe

- **WiFi**: 2.4 GHz, 5 GHz, 6 GHz (WiFi 6E)
- **Bluetooth**: 2.4 GHz
- **Fale radiowe**: Różne częstotliwości
- **Podczerwień**: Krótki zasięg, line-of-sight

## ⚡ Typy Sygnałów

### Sygnały analogowe
- Ciągła zmiana amplitudy, częstotliwości lub fazy
- Wykorzystywane w starszych technologiach (modem dial-up)

### Sygnały cyfrowe
- Dyskretne poziomy napięcia (0 i 1)
- Współczesne sieci Ethernet

## 📊 Kodowanie Sygnału

### Kodowanie Manchester (Ethernet 10 Mbps)
```
Bit 0: Przejście z wysokiego na niski poziom (w środku okresu bitowego)
Bit 1: Przejście z niskiego na wysoki poziom (w środku okresu bitowego)
```

### Kodowanie 4B/5B (Fast Ethernet)
- 4 bity danych kodowane jako 5 bitów
- Zapewnia wystarczającą liczbę przejść sygnału dla synchronizacji

### Kodowanie 8B/10B (Gigabit Ethernet)
- 8 bitów danych kodowane jako 10 bitów
- Lepsze właściwości synchronizacji

## 🔌 Złącza i Interfejsy

### RJ-45 (Ethernet)
```
Standard T568A:
Pin 1: Biały-zielony
Pin 2: Zielony
Pin 3: Biały-pomarańczowy
Pin 4: Niebieski
Pin 5: Biały-niebieski
Pin 6: Pomarańczowy
Pin 7: Biały-brązowy
Pin 8: Brązowy

Standard T568B (częściej używany):
Pin 1: Biały-pomarańczowy
Pin 2: Pomarańczowy
Pin 3: Biały-zielony
Pin 4: Niebieski
Pin 5: Biały-niebieski
Pin 6: Zielony
Pin 7: Biały-brązowy
Pin 8: Brązowy
```

### Inne złącza
- **LC/SC/ST**: Światłowody
- **BNC**: Koncentryk (legacy)
- **USB**: Urządzenia peryferyjne

## 📡 Topologie Fizyczne

### Gwiazda (Star)
- Wszystkie urządzenia połączone do centralnego punktu (switch/hub)
- Najpopularniejsza w sieciach Ethernet

### Magistrala (Bus)
- Wszystkie urządzenia na jednym kablu
- Legacy (10Base2, 10Base5)

### Pierścień (Ring)
- Urządzenia połączone w zamkniętą pętlę
- Token Ring, FDDI (legacy)

### Siatka (Mesh)
- Każde urządzenie połączone z wieloma innymi
- WiFi mesh, sieci ad-hoc

## ⚙️ Urządzenia Warstwy Fizycznej

### Hub (koncentrator)
- Powtarza sygnał na wszystkie porty
- Działa na poziomie bitów
- Powoduje kolizje (legacy)

### Repeater (wzmacniacz)
- Regeneruje i wzmacnia sygnał
- Zwiększa zasięg sieci

### Media converter
- Konwertuje między różnymi mediami (np. UTP ↔ Fiber)

## 🔍 Parametry Fizyczne

### Przepustowość (Bandwidth)
- Maksymalna ilość danych możliwa do przesłania
- Mierzona w Mbps/Gbps

### Tłumienie (Attenuation)
- Utrata mocy sygnału podczas transmisji
- Mierzona w dB (decybelach)

### Zakłócenia
- **EMI** (Electromagnetic Interference): Zakłócenia elektromagnetyczne
- **RFI** (Radio Frequency Interference): Zakłócenia radiowe
- **Crosstalk**: Przenikanie sygnałów między parami przewodów

### Opóźnienie (Latency)
- Czas propagacji sygnału przez medium
- Zależy od medium i odległości

## 🛠️ Standardy

- **IEEE 802.3**: Ethernet (wired)
- **IEEE 802.11**: WiFi (wireless)
- **TIA/EIA-568**: Okablowanie strukturalne
- **ITU-T G.652**: Światłowody single-mode

## 🔗 Powiązane Tematy

- [[warstwa_laczna|Warstwa Łącza Danych]]
- [[model_osi_overview|Model OSI - Przegląd]]
- [[switch_dzialanie|Switch - Przełącznik]]
- [[wifi_standardy|WiFi - Standardy]]
- [[SIECI KOMPUTEROWE]]

---

#warstwa-fizyczna #physical-layer #ethernet #światłowody #okablowanie #osi-layer1
