# 🔄 Switch - Przełącznik Sieciowy

## 📋 Definicja

Switch (przełącznik) to urządzenie sieciowe warstwy 2 (łącza danych), które przekazuje ramki Ethernet między urządzeniami w sieci lokalnej na podstawie adresów MAC. Nowoczesne switche mogą również działać na warstwie 3 (routing).

## 🔧 Funkcje Switcha

### 1. Learning (Nauka Adresów)
```
1. Ramka wpływa na port 1
2. Switch sprawdza Source MAC: AA:BB:CC:DD:EE:FF
3. Zapisuje w tablicy:
   MAC: AA:BB:CC:DD:EE:FF → Port: 1
```

### 2. Forwarding (Przekazywanie)
```
1. Sprawdź Destination MAC w ramce
2. Przeszukaj tablicę MAC
3. Jeśli znaleziono → Przekaż do konkretnego portu
4. Jeśli nie znaleziono → Flood na wszystkie porty (oprócz wejściowego)
```

### 3. Filtering (Filtrowanie)
```
1. Sprawdź Source i Destination MAC
2. Jeśli oba na tym samym porcie → Drop frame
3. Jeśli na różnych → Forward
```

### 4. Avoiding Loops (Unikanie Pętli)
- STP (Spanning Tree Protocol)
- Blokowanie redundantnych połączeń
- Automatyczne odblokowanie przy awarii

## 📊 Tablica MAC (MAC Address Table)

### Struktura
```
MAC Address         Port    VLAN    Age (s)    Type
00:1A:2B:3C:4D:5E    1       1       120       Dynamic
11:22:33:44:55:66    2       1       45        Dynamic
AA:BB:CC:DD:EE:FF    3       10      300       Static
FF:FF:FF:FF:FF:FF    ALL     ALL     -         Permanent
```

### Typy Wpisów
- **Dynamic**: Nauczono automatycznie, timeout (domyślnie 300s)
- **Static**: Skonfigurowano ręcznie, nie wygasa
- **Permanent**: Wbudowane (np. broadcast)

### Aging Time
```
Domyślnie: 300 sekund (5 minut)

Jeśli MAC nie widoczny przez 300s → Usunięcie z tablicy
Przy każdej ramce → Odnowienie timera
```

## 🔄 Metody Przełączania

### 1. Store-and-Forward
```
Proces:
1. Odbierz całą ramkę (do FCS)
2. Sprawdź FCS (CRC-32)
3. Jeśli błąd → Drop
4. Jeśli OK → Lookup MAC i forward

Zalety:
✓ Wykrywa błędy
✓ Nie propaguje uszkodzonych ramek

Wady:
✗ Większe opóźnienie
✗ Latency zależy od rozmiaru ramki
```

### 2. Cut-Through
```
Proces:
1. Czytaj tylko Destination MAC (6 bajtów)
2. Natychmiast rozpocznij forwarding
3. Nie czekaj na całą ramkę

Zalety:
✓ Bardzo niskie opóźnienie (~10μs)
✓ Stałe opóźnienie niezależne od rozmiaru

Wady:
✗ Nie wykrywa błędów
✗ Propaguje uszkodzone ramki
```

### 3. Fragment-Free
```
Proces:
1. Czytaj pierwsze 64 bajty
2. Sprawdź czy jest kolizja (collision fragments <64B)
3. Forward dalej

Zalety:
✓ Wykrywa kolizje
✓ Niższe opóźnienie niż Store-and-Forward

Wady:
✗ Nie wykrywa wszystkich błędów
```

### 4. Adaptive Switching
```
Switch dynamicznie wybiera metodę:
- Niski error rate → Cut-Through
- Wysoki error rate → Store-and-Forward
```

## 🌐 VLAN (Virtual LAN)

### Definicja
Logiczny podział switcha na oddzielne sieci broadcast:
```
Switch fizyczny:
┌─────────────────────────────┐
│  VLAN 10 (Dział IT)         │
│  Porty: 1-8                 │
├─────────────────────────────┤
│  VLAN 20 (Biuro)            │
│  Porty: 9-16                │
├─────────────────────────────┤
│  VLAN 30 (Goście)           │
│  Porty: 17-24               │
└─────────────────────────────┘
```

### Typy VLAN

#### 1. Port-based VLAN (Access)
```cisco
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
```

#### 2. Tagged VLAN (Trunk) - 802.1Q
```
Frame Ethernet + 802.1Q Tag:
┌──────┬─────┬─────────┬──────┬──────┬─────┐
│ Dest │ Src │ 802.1Q  │ Type │ Data │ FCS │
│ MAC  │ MAC │  Tag    │      │      │     │
└──────┴─────┴─────────┴──────┴──────┴─────┘
              │
              ├─ TPID (0x8100)
              ├─ Priority (3 bit)
              ├─ CFI (1 bit)
              └─ VLAN ID (12 bit): 1-4094
```

```cisco
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
 switchport trunk native vlan 99
```

#### 3. Voice VLAN
```cisco
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 50
```

### Native VLAN
- Ramki bez tagu na trunk port
- Domyślnie VLAN 1
- **Best practice**: Zmień na nieużywany VLAN

### Inter-VLAN Routing

#### Router-on-a-Stick
```
Router
  │
  │ Trunk (802.1Q)
  │
Switch
  ├─ VLAN 10
  ├─ VLAN 20
  └─ VLAN 30

Router config:
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 
interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
```

#### Layer 3 Switch (SVI)
```cisco
ip routing

vlan 10
 name IT

vlan 20
 name Office

interface Vlan10
 ip address 192.168.10.1 255.255.255.0

interface Vlan20
 ip address 192.168.20.1 255.255.255.0
```

## 🔄 Spanning Tree Protocol (STP)

### Problem: Pętle L2
```
Bez STP:
Switch A ←→ Switch B
    ↑           ↓
    └─ Switch C ┘

Broadcast storm → Zapętlenie → Przeciążenie
```

### Rozwiązanie STP (802.1D)
```
1. Wybór Root Bridge (najniższy Bridge ID)
2. Obliczenie cost do Root
3. Wybór Root Port na każdym switchu (najniższy cost)
4. Wybór Designated Port na każdym segmencie
5. Blokowanie pozostałych portów (Alternate/Backup)
```

### Stany Portów STP
```
Disabled   → Port wyłączony
Blocking   → Nie przekazuje, nasłuchuje BPDU (20s)
Listening  → Uczestniczy w STP, nie uczy MAC (15s)
Learning   → Uczy się MAC, nie przekazuje (15s)
Forwarding → Normalny ruch

Czas konwergencji: 50s (20+15+15)
```

### Wersje STP

#### PVST+ (Per-VLAN STP - Cisco)
```
Osobny STP dla każdego VLAN
Można balansować ruch między linkami
```

#### RSTP (Rapid STP - 802.1w)
```
Konwergencja: <1s (zamiast 50s)
Stany portów:
- Discarding (zamiast Blocking/Listening)
- Learning
- Forwarding

Typy portów:
- Root Port
- Designated Port  
- Alternate Port (backup do Root)
- Backup Port (backup Designated)
```

#### MSTP (Multiple STP - 802.1s)
```
Grupa VLAN → Instance STP
Mniej instancji niż PVST+
Standard otwarty
```

### PortFast i BPDU Guard
```cisco
# PortFast - Natychmiastowe forwarding (tylko access porty)
interface FastEthernet0/1
 spanning-tree portfast

# BPDU Guard - Shutdown jeśli BPDU received
interface FastEthernet0/1
 spanning-tree bpduguard enable
```

## ⚡ EtherChannel (Link Aggregation)

### Definicja
Połączenie wielu fizycznych linków w jeden logiczny:
```
Switch A ═══════════ Switch B
         ═══════════
         ═══════════
         
3 × 1 Gbps = 3 Gbps agregowanego bandwidth
+ Redundancja
```

### Protokoły

#### LACP (Link Aggregation Control Protocol - 802.3ad)
```cisco
interface range GigabitEthernet0/1-3
 channel-group 1 mode active
 
interface Port-channel1
 switchport mode trunk
```

#### PAgP (Port Aggregation Protocol - Cisco)
```cisco
interface range GigabitEthernet0/1-3
 channel-group 1 mode desirable
```

### Load Balancing
```
Metody:
- src-mac       : Source MAC
- dst-mac       : Destination MAC
- src-dst-mac   : XOR obu MAC
- src-ip        : Source IP
- dst-ip        : Destination IP
- src-dst-ip    : XOR obu IP

Config:
port-channel load-balance src-dst-ip
```

## 🔐 Bezpieczeństwo Switcha

### Port Security
```cisco
interface FastEthernet0/1
 switchport mode access
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security violation shutdown
 
Violation modes:
- shutdown  : Err-disable port (default)
- restrict  : Drop + log
- protect   : Drop bez logu
```

### DHCP Snooping
```cisco
ip dhcp snooping
ip dhcp snooping vlan 10,20

interface GigabitEthernet0/1
 ip dhcp snooping trust     ! Uplink do DHCP server

interface range FastEthernet0/1-24
 ip dhcp snooping limit rate 10
```

### Dynamic ARP Inspection (DAI)
```cisco
ip arp inspection vlan 10,20

interface GigabitEthernet0/1
 ip arp inspection trust

! Opcjonalnie validate
ip arp inspection validate src-mac dst-mac ip
```

### IP Source Guard
```cisco
interface FastEthernet0/1
 ip verify source
```

## 🛠️ Komendy Diagnostyczne

### Tablica MAC
```cisco
show mac address-table
show mac address-table dynamic
show mac address-table address 0011.2233.4455
show mac address-table interface Fa0/1
show mac address-table vlan 10
```

### VLAN
```cisco
show vlan brief
show vlan id 10
show interfaces trunk
show interfaces switchport
```

### STP
```cisco
show spanning-tree
show spanning-tree vlan 10
show spanning-tree summary
show spanning-tree root
```

### EtherChannel
```cisco
show etherchannel summary
show etherchannel port-channel
show lacp neighbor
```

### Port Security
```cisco
show port-security
show port-security interface Fa0/1
show port-security address
```

## 🔗 Powiązane Tematy

- [[warstwa_laczna|Warstwa Łącza Danych]]
- [[warstwa_fizyczna|Warstwa Fizyczna]]
- [[router_dzialanie|Router]]
- [[model_osi_overview|Model OSI]]
- [[SIECI KOMPUTEROWE]]

---

#switch #przełącznik #vlan #stp #etherchannel #layer2 #mac-table
