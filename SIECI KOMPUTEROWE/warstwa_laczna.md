# 2️⃣ Warstwa Łącza Danych (Data Link Layer)

## 📋 Definicja

Warstwa łącza danych odpowiada za niezawodną transmisję ramek danych między dwoma węzłami połączonymi bezpośrednio. Zapewnia adresowanie fizyczne, kontrolę dostępu do medium i wykrywanie błędów.

## 🏗️ Podwarstwy

### LLC (Logical Link Control) - IEEE 802.2
- **Funkcje**:
  - Kontrola przepływu
  - Multipleksowanie protokołów warstwy sieciowej
  - Opcjonalna kontrola błędów
- **Niezależna** od medium fizycznego

### MAC (Media Access Control)
- **Funkcje**:
  - Adresowanie fizyczne (MAC address)
  - Kontrola dostępu do medium
  - Ramkowanie
- **Zależna** od technologii (Ethernet, WiFi, etc.)

## 🔧 Główne Funkcje

### 1. Ramkowanie (Framing)
Pakowanie danych z warstwy sieciowej w ramki z nagłówkiem i stopką:
```
┌──────────┬─────────┬──────────┬─────┬─────┐
│ Preamble │ Header  │   Data   │ FCS │ IFG │
└──────────┴─────────┴──────────┴─────┴─────┘
```

### 2. Adresowanie Fizyczne (MAC)
- **Format**: 48 bitów (6 bajtów)
- **Przykład**: `00:1A:2B:3C:4D:5E`
- **Struktura**:
  - 24 bity: OUI (Organizationally Unique Identifier) - producent
  - 24 bity: NIC (Network Interface Controller) - unikalny numer

```
Format MAC:
┌────────────────────┬────────────────────┐
│    OUI (vendor)    │   Device Serial    │
│      3 bajty       │      3 bajty       │
└────────────────────┴────────────────────┘

Przykład:
00:1A:2B:3C:4D:5E
│  │  │  │  │  │
│  │  │  │  │  └─ Bajt 6
│  │  │  │  └──── Bajt 5
│  │  │  └─────── Bajt 4
│  │  └────────── Bajt 3 (OUI)
│  └───────────── Bajt 2 (OUI)
└──────────────── Bajt 1 (OUI)
```

### 3. Kontrola Dostępu do Medium

#### CSMA/CD (Ethernet przewodowy)
**Carrier Sense Multiple Access with Collision Detection**
```
1. Nasłuchuj medium (CS)
2. Jeśli wolne - transmituj
3. Podczas transmisji wykrywaj kolizje (CD)
4. Jeśli kolizja:
   - Wyślij sygnał jam
   - Czekaj losowy czas (backoff)
   - Spróbuj ponownie
```

#### CSMA/CA (WiFi)
**Carrier Sense Multiple Access with Collision Avoidance**
```
1. Nasłuchuj medium
2. Jeśli wolne przez DIFS - czekaj random backoff
3. Wyślij RTS (Request To Send)
4. Odbierz CTS (Clear To Send)
5. Transmituj dane
6. Odbierz ACK
```

### 4. Kontrola Błędów

#### CRC (Cyclic Redundancy Check)
- Najczęściej używana metoda w Ethernet
- CRC-32: 32-bitowa suma kontrolna
- Wykrywa błędy pojedyncze i większość wielokrotnych

#### Parzystość (Parity)
- Prostsza metoda (legacy)
- Wykrywa tylko błędy pojedyncze

### 5. Kontrola Przepływu
- **Stop-and-Wait**: Czekaj na ACK przed wysłaniem następnej ramki
- **Sliding Window**: Wiele ramek bez ACK (określone okno)

## 📦 Struktura Ramki Ethernet II

```
┌──────────┬──────────┬──────────┬────────┬─────────┬─────┐
│ Preamble │ Dest MAC │ Src MAC  │  Type  │  Data   │ FCS │
│  8 bajtów│  6 bajtów│  6 bajtów│2 bajty │46-1500 B│4 B  │
└──────────┴──────────┴──────────┴────────┴─────────┴─────┘

Preamble: 7 bajtów (10101010...) + 1 bajt SFD (10101011)
Dest MAC: Adres docelowy
Src MAC: Adres źródłowy
Type: Protokół warstwy wyższej (0x0800=IPv4, 0x0806=ARP, 0x86DD=IPv6)
Data: Payload (min 46, max 1500 bajtów)
FCS: Frame Check Sequence (CRC-32)
```

## 🌐 Typy Adresów MAC

### Unicast
- Adres pojedynczego urządzenia
- LSB pierwszego bajtu = 0
- Przykład: `00:1A:2B:3C:4D:5E`

### Multicast
- Grupa urządzeń
- LSB pierwszego bajtu = 1
- Przykład: `01:00:5E:00:00:FB` (mDNS)

### Broadcast
- Wszystkie urządzenia w sieci lokalnej
- Adres: `FF:FF:FF:FF:FF:FF`

## 🔄 Protokoły Warstwy Łącza

### ARP (Address Resolution Protocol)
**Mapowanie IP → MAC**
```
Pytanie (broadcast):
"Kto ma IP 192.168.1.10? Odpowiedz na MAC: AA:BB:CC:DD:EE:FF"

Odpowiedź (unicast):
"IP 192.168.1.10 to ja, mój MAC: 11:22:33:44:55:66"
```

### RARP (Reverse ARP)
- Mapowanie MAC → IP (legacy)
- Zastąpione przez DHCP

### STP (Spanning Tree Protocol)
- Zapobiega pętlom w sieci
- Blokuje redundantne ścieżki
- Odblokuje w razie awarii

### VLAN (802.1Q)
- Wirtualne sieci LAN
- Tagowanie ramek (4 bajty):
```
┌──────────┬──────┬─────────┬──────┬─────────┬─────┐
│ Dest MAC │ Src  │ 802.1Q  │ Type │  Data   │ FCS │
│          │ MAC  │  Tag    │      │         │     │
└──────────┴──────┴─────────┴──────┴─────────┴─────┘
                    │
                    └─ VLAN ID (12 bitów): 1-4094
```

## ⚙️ Urządzenia Warstwy Łącza

### Switch (przełącznik)
- **Funkcje**:
  - Nauka adresów MAC (MAC table)
  - Przekazywanie ramek do właściwego portu
  - Filtrowanie ramek
  - Zarządzanie VLAN

- **Tablica MAC**:
```
MAC Address         Port    VLAN    Age
00:1A:2B:3C:4D:5E    1       1      60s
11:22:33:44:55:66    2       1      45s
AA:BB:CC:DD:EE:FF    3       10     120s
```

### Bridge (mostek)
- Łączy dwa segmenty sieci
- Filtruje ruch między segmentami
- Podobny do switcha, ale mniej portów

### NIC (Network Interface Card)
- Karta sieciowa
- Unikatowy adres MAC
- Konwersja między warstwą fizyczną a łącza

## 🔍 Metody Przełączania (Switching)

### Store-and-Forward
- Odbiera całą ramkę
- Sprawdza CRC
- Jeśli OK - przekazuje dalej
- **Zaleta**: Wykrywa błędy
- **Wada**: Większe opóźnienie

### Cut-Through
- Czyta tylko adres docelowy
- Natychmiast przekazuje
- **Zaleta**: Niskie opóźnienie
- **Wada**: Nie wykrywa błędów

### Fragment-Free
- Czyta pierwsze 64 bajty
- Kompromis między powyższymi

## 🌍 Technologie Warstwy Łącza

### Ethernet (IEEE 802.3)
- Najpopularniejsza technologia LAN
- CSMA/CD (w starszych wersjach)
- Ramka Ethernet II lub 802.3

### WiFi (IEEE 802.11)
- Bezprzewodowa sieć LAN
- CSMA/CA
- Ramka 802.11 (inna niż Ethernet)

### PPP (Point-to-Point Protocol)
- Połączenia punkt-punkt
- Modemy, DSL, szeregowe

### HDLC (High-Level Data Link Control)
- Połączenia WAN
- Cisco używa własnej wersji

## 🛠️ Komendy Diagnostyczne

### Sprawdzenie adresu MAC (Linux/Mac)
```bash
ip link show
ifconfig
```

### Sprawdzenie adresu MAC (Windows)
```cmd
ipconfig /all
getmac
```

### Wyświetlenie tablicy ARP
```bash
arp -a          # Windows/Linux
ip neigh        # Linux (nowszy)
```

### Wyświetlenie tablicy MAC na switchu (Cisco)
```cisco
show mac address-table
show mac address-table dynamic
```

## 🔗 Powiązane Tematy

- [[warstwa_fizyczna|Warstwa Fizyczna]]
- [[warstwa_sieciowa|Warstwa Sieciowa]]
- [[model_osi_overview|Model OSI]]
- [[switch_dzialanie|Switch - Przełącznik]]
- [[protokol_ip|Protokół IP]]
- [[SIECI KOMPUTEROWE]]

---

#warstwa-łącza #data-link #mac #ethernet #switch #arp #vlan #osi-layer2
