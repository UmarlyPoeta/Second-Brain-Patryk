# 📡 WiFi - Standardy i Konfiguracja

## 📋 Wprowadzenie

WiFi (IEEE 802.11) to rodzina standardów bezprzewodowych sieci lokalnych (WLAN). Umożliwia komunikację urządzeń bez użycia kabli, wykorzystując fale radiowe.

## 🌐 Standardy WiFi

### Ewolucja Standardów
```
Standard    Rok   Pasmo        Max Speed   Nazwa WiFi Alliance
802.11      1997  2.4 GHz      2 Mbps      -
802.11b     1999  2.4 GHz      11 Mbps     -
802.11a     1999  5 GHz        54 Mbps     -
802.11g     2003  2.4 GHz      54 Mbps     -
802.11n     2009  2.4/5 GHz    600 Mbps    WiFi 4
802.11ac    2013  5 GHz        6.9 Gbps    WiFi 5
802.11ax    2019  2.4/5/6 GHz  9.6 Gbps    WiFi 6/6E
802.11be    2024  2.4/5/6 GHz  46 Gbps     WiFi 7
```

### WiFi 4 (802.11n)
```
Charakterystyka:
- Pasmo: 2.4 GHz i/lub 5 GHz
- Szerokość kanału: 20/40 MHz
- MIMO: Do 4×4 (4 anteny TX/RX)
- Modulacja: OFDM, do 64-QAM
- Backward compatible: 802.11a/b/g

Max prędkość:
- 20 MHz: 72.2 Mbps (single stream)
- 40 MHz: 150 Mbps (single stream)
- 40 MHz 4×4: 600 Mbps
```

### WiFi 5 (802.11ac)
```
Charakterystyka:
- Pasmo: Tylko 5 GHz
- Szerokość kanału: 20/40/80/160 MHz
- MU-MIMO: Multi-User (downlink)
- Modulacja: 256-QAM
- Beamforming: Kierunkowa transmisja

Max prędkość:
- 80 MHz 1×1: 433 Mbps
- 80 MHz 2×2: 867 Mbps
- 160 MHz 8×8: 6.9 Gbps (teoretycznie)

Typowo: 1.3-1.7 Gbps (3×3 lub 4×4)
```

### WiFi 6 (802.11ax)
```
Charakterystyka:
- Pasmo: 2.4 GHz, 5 GHz
- WiFi 6E: + 6 GHz (nowe pasmo)
- Szerokość kanału: 20/40/80/160 MHz
- OFDMA: Efficiency w dense environments
- MU-MIMO: Uplink + Downlink
- Modulacja: 1024-QAM
- TWT (Target Wake Time): Oszczędność energii

Max prędkość:
- 160 MHz 8×8: 9.6 Gbps
- Typowo: 2.4 Gbps (4×4)

Zalety:
✓ Lepsza wydajność w zatłoczonych sieciach
✓ Niższe opóźnienia
✓ Większy zasięg
✓ Lepsze zarządzanie energią (IoT)
```

### WiFi 7 (802.11be)
```
Charakterystyka:
- Pasmo: 2.4/5/6 GHz (tri-band)
- Szerokość kanału: Do 320 MHz
- CMU-MIMO: Coordinated Multi-User
- 4096-QAM
- Multi-Link Operation (MLO)
- Multi-AP coordination

Max prędkość: 46 Gbps
Typowo: 5-10 Gbps

Nowe funkcje:
- MLO: Jednoczesna transmisja na wielu pasmach
- Multi-RU: Flexible resource allocation
- Improved MU-MIMO
```

## 📶 Pasma i Kanały

### Pasmo 2.4 GHz
```
Kanały (14 dostępnych, region-dependent):

USA/Europe (13 kanałów):
  1 [2412 MHz]  ▓▓▓▓▓
  2 [2417 MHz]    ▓▓▓▓▓
  3 [2422 MHz]      ▓▓▓▓▓
  ...
  11 [2462 MHz]                ▓▓▓▓▓
  
Non-overlapping (USA): 1, 6, 11
Non-overlapping (Europe): 1, 5, 9, 13

Zalety:
✓ Większy zasięg
✓ Lepsza penetracja ścian
✓ Kompatybilność ze starszymi urządzeniami

Wady:
✗ Zatłoczenie (WiFi, Bluetooth, mikrofale)
✗ Tylko 3-4 kanały bez nakładania
✗ Wolniejsze niż 5 GHz
```

### Pasmo 5 GHz
```
Kanały (różne w zależności od regionu):

DFS channels (Dynamic Frequency Selection):
- Muszą wykrywać radary
- 52-144 (Europe), 52-144 (USA)

Non-DFS:
- 36, 40, 44, 48 (UNII-1)
- 149, 153, 157, 161, 165 (UNII-3, USA)

Szerokość kanału:
- 20 MHz: ~24 kanały
- 40 MHz: ~12 kanałów
- 80 MHz: 6 kanałów
- 160 MHz: 2 kanały

Zalety:
✓ Więcej kanałów
✓ Mniej zakłóceń
✓ Wyższe prędkości

Wady:
✗ Mniejszy zasięg
✗ Gorsza penetracja przeszkód
✗ DFS wymaga czasu na skanowanie radarów
```

### Pasmo 6 GHz (WiFi 6E/7)
```
Nowe pasmo: 5.925 - 7.125 GHz

Kanały:
- USA: 59 kanałów po 20 MHz
- 14 × 80 MHz lub 7 × 160 MHz
- 3 × 320 MHz (WiFi 7)

Zalety:
✓ Brak legacy devices (czyste pasmo)
✓ Brak nakładania z 2.4/5 GHz
✓ Szersze kanały (320 MHz)
✓ Niskie opóźnienia

Wady:
✗ Jeszcze mniejszy zasięg
✗ Wymaga WiFi 6E/7
✗ Dostępność zależy od regionu
```

## 🔐 Bezpieczeństwo WiFi

### Protokoły Szyfrowania

#### WEP (Wired Equivalent Privacy) - PRZESTARZAŁE
```
Status: NIGDY NIE UŻYWAJ
Rok: 1997
Klucz: 64 lub 128 bit
Problem: Łatwo złamać (minuty)
```

#### WPA (WiFi Protected Access)
```
Status: Przestarzałe
Rok: 2003
Klucz: TKIP (Temporal Key Integrity Protocol)
Problem: Podatności (TKIP broken)
```

#### WPA2 (802.11i)
```
Status: Standard (ale nie najlepszy)
Rok: 2004
Szyfrowanie: AES-CCMP (128-bit)
Autentykacja: PSK (Personal) lub 802.1X (Enterprise)

WPA2-PSK (Personal):
- Pre-Shared Key (hasło)
- Dla domów i małych biur

WPA2-Enterprise:
- RADIUS server (autentykacja użytkowników)
- Certyfikaty lub login/hasło
- Dla korporacji

Podatności:
- KRACK (2017) - wymaga patcha
- Brute force na słabe hasła
```

#### WPA3
```
Status: Zalecany (nowy standard)
Rok: 2018
Szyfrowanie: AES-GCMP (128-bit) lub 192-bit

WPA3-Personal:
- SAE (Simultaneous Authentication of Equals)
- Ochrona przed offline dictionary attacks
- Forward secrecy

WPA3-Enterprise:
- 192-bit encryption (optional)
- Stronger algorithms

Zalety:
✓ Ochrona przed brute force
✓ Forward secrecy (każda sesja nowy klucz)
✓ Łatwiejsze łączenie (Easy Connect)
✓ Enhanced Open (szyfrowanie bez hasła)
```

### Autentykacja Enterprise (802.1X)

#### EAP (Extensible Authentication Protocol)
```
Typy EAP:
- EAP-TLS: Certyfikaty (najbezpieczniejsze)
- EAP-TTLS: Tunel + login/hasło
- PEAP: Protected EAP (Microsoft)
- EAP-FAST: Flexible Authentication (Cisco)

Architektura:
Client (Supplicant) ←→ AP (Authenticator) ←→ RADIUS Server
```

#### RADIUS Server
```
Funkcje:
- Centralna autentykacja
- Accounting (logowanie sesji)
- Authorization (polityki dostępu)

Konfiguracja przykład (FreeRADIUS):
clients.conf:
  client ap1 {
    ipaddr = 192.168.1.10
    secret = shared_secret_key
  }

users:
  jan Cleartext-Password := "haslo123"
    Reply-Message = "Welcome Jan"
```

## 🔧 Konfiguracja Access Point

### Podstawowe Ustawienia
```
SSID: MyNetwork
Pasmo: 2.4 GHz + 5 GHz (dual-band)
Kanał 2.4: Auto (lub 1/6/11)
Kanał 5: Auto (lub 36/40/44/48)
Szerokość: 20 MHz (2.4), 80 MHz (5)
Moc: Auto (lub 50-75%)
Bezpieczeństwo: WPA3 (fallback WPA2)
Hasło: [silne_haslo_min_12_znaków]
```

### Zaawansowane

#### Band Steering
```
Funkcja: Kierowanie klientów do 5 GHz (gdy możliwe)
Cel: Odciążenie 2.4 GHz, lepsze prędkości

Ustawienia:
- Threshold RSSI: -70 dBm (poniżej → 2.4 GHz)
- Prefer 5 GHz: Enabled
```

#### Roaming (Fast Roaming)
```
802.11k: Radio Resource Management
  - AP wysyła informacje o sąsiednich AP
  
802.11v: BSS Transition Management  
  - AP sugeruje klientowi zmianę AP
  
802.11r: Fast Transition (FT)
  - Pre-authentication
  - Seamless handoff (VoIP, streaming)
```

#### Airtime Fairness
```
Problem: Wolne klienty blokują szybkie

Rozwiązanie:
- Każdy klient dostaje równy czas transmisji
- Szybsze urządzenia = więcej danych w tym samym czasie
```

#### Beamforming
```
Funkcja: Kierunkowa transmisja do klienta

Bez beamforming:
  AP ))) wszystkie kierunki

Z beamforming:
  AP >>>>>> klient (focused signal)

Wymaga: Obsługa przez AP i klienta
```

## 🛠️ Troubleshooting WiFi

### Typowe Problemy

#### Słaby Sygnał
```
Diagnoza:
- RSSI < -70 dBm (słaby)
- Przeszkody (ściany, meble)
- Odległość od AP

Rozwiązanie:
- Reposition AP (centralnie, wysoko)
- Dodatkowe AP / mesh
- 2.4 GHz (lepszy zasięg)
- External antennas
```

#### Zakłócenia
```
Diagnoza:
- WiFi scanner (inSSIDer, WiFi Analyzer)
- Nakładające się kanały
- Non-WiFi interference (mikrofale, Bluetooth)

Rozwiązanie:
- Zmiana kanału (1, 6, 11 dla 2.4 GHz)
- Użyj 5 GHz (mniej zatłoczone)
- Zmniejsz szerokość kanału (40→20 MHz)
```

#### Niskie Prędkości
```
Diagnoza:
- Speed test (iperf3, fast.com)
- Sprawdź negotiated rate (PHY rate vs throughput)
- Channel utilization

Rozwiązanie:
- 5 GHz zamiast 2.4 GHz
- Szersze kanały (80/160 MHz)
- WiFi 6/7 (jeśli wspierane)
- Reduce interference
```

#### Problemy z Roamingiem
```
Diagnoza:
- Client "sticky" (nie zmienia AP)
- Nakładające się AP coverage

Rozwiązanie:
- 802.11k/v/r (Fast Roaming)
- Reduce AP power (force handoff)
- Minimum RSSI threshold
```

### Narzędzia Diagnostyczne

#### WiFi Scanner
```bash
# Linux
iwlist wlan0 scan
nmcli dev wifi list

# Windows
netsh wlan show networks mode=bssid

# Android/iOS
WiFi Analyzer, Network Analyzer
```

#### Signal Strength
```bash
# Linux
iwconfig wlan0
watch -n 1 'iwconfig wlan0 | grep -i quality'

# Windows
netsh wlan show interfaces
```

#### Speed Test
```bash
# iperf3 (server)
iperf3 -s

# iperf3 (client)
iperf3 -c server_ip -t 30
```

## 🔗 Powiązane Tematy

- [[warstwa_fizyczna|Warstwa Fizyczna]]
- [[warstwa_laczna|Warstwa Łącza Danych]]
- [[sieci_bezprzewodowe|Sieci Bezprzewodowe - Bezpieczeństwo]]
- [[access_point|Access Point]]
- [[SIECI KOMPUTEROWE]]

---

#wifi #wireless #802.11 #wpa3 #bezpieczeństwo #access-point #wifi6
