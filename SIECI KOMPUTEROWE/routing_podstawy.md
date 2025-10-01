# 🔀 Routing - Podstawy Trasowania

## 📋 Definicja

Routing to proces wyboru ścieżki, którą pakiety powinny podążać przez sieć, aby dotrzeć do miejsca docelowego. Router analizuje adres docelowy i na podstawie tablicy routingu podejmuje decyzję o przekazaniu pakietu.

## 🗺️ Tablica Routingu (Routing Table)

### Struktura Tablicy
```
Destination     Gateway         Genmask         Metric  Iface
0.0.0.0         192.168.1.1     0.0.0.0         100     eth0
10.0.0.0        192.168.1.254   255.0.0.0       10      eth0
192.168.1.0     0.0.0.0         255.255.255.0   0       eth0
```

### Elementy Wpisu
- **Destination**: Sieć docelowa
- **Gateway**: Next hop (następny router) lub 0.0.0.0 (direct)
- **Genmask/Netmask**: Maska sieci
- **Metric**: Koszt trasy (niższy = lepszy)
- **Interface**: Interfejs wyjściowy

### Typy Tras

#### 1. Connected Route (Bezpośrednia)
```
192.168.1.0/24 via 0.0.0.0 dev eth0
```
Sieć bezpośrednio podłączona do interfejsu.

#### 2. Static Route (Statyczna)
```
10.0.0.0/8 via 192.168.1.254 dev eth0
```
Ręcznie skonfigurowana trasa.

#### 3. Dynamic Route (Dynamiczna)
```
172.16.0.0/12 via 192.168.1.250 dev eth0 proto ospf metric 20
```
Nauczono z protokołu dynamicznego (RIP, OSPF, BGP).

#### 4. Default Route (Trasa Domyślna)
```
0.0.0.0/0 via 192.168.1.1 dev eth0
```
Gateway of last resort - używany gdy brak innych tras.

## 🔍 Proces Routingu

### Algorytm Longest Prefix Match
```
Pakiet do: 192.168.1.100

Tablica routingu:
1. 0.0.0.0/0         via 192.168.1.1     (/0  - 0 bitów)
2. 192.168.0.0/16    via 192.168.1.254   (/16 - 16 bitów)
3. 192.168.1.0/24    via 0.0.0.0         (/24 - 24 bity)

Wynik: Użyj trasy 3 (/24 - najdłuższy prefix)
```

### Kroki Routingu
```
1. Sprawdź adres docelowy pakietu: 10.0.0.50
2. Przeszukaj tablicę routingu:
   - 10.0.0.0/8 via 192.168.1.254
3. Pakiet przekazany do 192.168.1.254 (next hop)
4. TTL zmniejszone o 1
5. Checksum przeliczony
6. Pakiet wysłany przez interfejs eth0
```

## 🛤️ Typy Routingu

### Static Routing (Statyczny)

#### Zalety
- Pełna kontrola nad trasami
- Brak obciążenia procesora
- Przewidywalne zachowanie
- Bezpieczeństwo (brak reklam tras)

#### Wady
- Ręczna konfiguracja
- Brak automatycznej zmiany tras
- Nie skaluje się w dużych sieciach

#### Konfiguracja
```bash
# Linux
ip route add 10.0.0.0/8 via 192.168.1.254
ip route add default via 192.168.1.1

# Windows
route add 10.0.0.0 mask 255.0.0.0 192.168.1.254
route add 0.0.0.0 mask 0.0.0.0 192.168.1.1

# Cisco
ip route 10.0.0.0 255.0.0.0 192.168.1.254
ip route 0.0.0.0 0.0.0.0 192.168.1.1
```

### Dynamic Routing (Dynamiczny)

#### Zalety
- Automatyczna adaptacja do zmian topologii
- Skalowalne w dużych sieciach
- Automatyczne load balancing
- Redundancja i failover

#### Wady
- Większe zużycie zasobów (CPU, RAM, bandwidth)
- Złożona konfiguracja
- Konwergencja może trwać

## 🔄 Protokoły Routingu Dynamicznego

### Distance Vector

#### RIP (Routing Information Protocol)
```
Charakterystyka:
- Metryka: Hop count
- Max: 15 hopów (16 = unreachable)
- Aktualizacje: co 30 sekund (broadcast/multicast)
- Wersje: RIPv1 (classful), RIPv2 (classless, CIDR)

Problemy:
- Count to infinity
- Slow convergence
- Ograniczona skalowalność

Timers:
- Update: 30s
- Invalid: 180s
- Holddown: 180s
- Flush: 240s
```

#### EIGRP (Enhanced Interior Gateway Routing Protocol)
```
Charakterystyka:
- Cisco proprietary (stary), teraz RFC 7868
- Metryka: Bandwidth + Delay (+ Load, Reliability)
- Algorytm: DUAL (Diffusing Update Algorithm)
- Aktualizacje: Tylko zmiany (triggered updates)
- Konwergencja: Bardzo szybka

Zalety:
- Szybka konwergencja
- Efektywne użycie bandwidth
- VLSM i CIDR support
- Load balancing (unequal cost)
```

### Link State

#### OSPF (Open Shortest Path First)
```
Charakterystyka:
- Open standard (RFC 2328)
- Metryka: Cost (100,000,000 / bandwidth)
- Algorytm: Dijkstra (SPF - Shortest Path First)
- Aktualizacje: LSA (Link State Advertisement)
- Hierarchia: Areas (backbone = Area 0)

Areas:
- Area 0 (Backbone): Centrum topologii
- Standard Area: Normalne areas
- Stub Area: Brak tras zewnętrznych
- Totally Stub: Tylko default route
- NSSA: Not-So-Stubby Area

Typy LSA:
- Type 1 (Router LSA): Routery w area
- Type 2 (Network LSA): DR w segmencie
- Type 3 (Summary LSA): Trasy między areas
- Type 4 (ASBR Summary): ASBR location
- Type 5 (External LSA): Trasy zewnętrzne
```

### Path Vector

#### BGP (Border Gateway Protocol)
```
Charakterystyka:
- Routing między AS (Autonomous Systems)
- Metryka: AS Path, policies
- Protokół: TCP port 179
- Skalowanie: Internet (>900k tras)

Typy:
- eBGP (External): Między różnymi AS
- iBGP (Internal): W ramach AS

Atrybuty:
- AS_PATH: Lista przejść przez AS
- NEXT_HOP: Next hop IP
- LOCAL_PREF: Preferencja lokalna
- MED: Multi-Exit Discriminator
- COMMUNITY: Tagging
```

## 📊 Metryki Routingu

### Typy Metryk

#### Hop Count (RIP)
```
Liczba routerów do celu:
A → B → C → D = 3 hopy
```

#### Bandwidth (OSPF)
```
Cost = Reference Bandwidth / Interface Bandwidth

Przykład (ref=100 Mbps):
FastEthernet (100 Mbps):  100/100 = 1
GigabitEthernet (1 Gbps): 100/1000 = 0.1 → 1 (min)
Serial (1.544 Mbps):      100/1.544 = 64
```

#### Composite (EIGRP)
```
Metryka = [K1*Bandwidth + (K2*Bandwidth)/(256-Load) + K3*Delay] * [K5/(Reliability+K4)]

Domyślnie (K1=1, K3=1, K2=K4=K5=0):
Metryka = Bandwidth + Delay
```

### Administrative Distance (AD)

Priorytet źródeł tras (niższy = lepszy):
```
Connected:        0
Static:           1
EIGRP Summary:    5
eBGP:            20
EIGRP Internal:  90
IGRP:           100
OSPF:           110
IS-IS:          115
RIP:            120
EIGRP External: 170
iBGP:           200
Unknown:        255 (nie używaj)
```

## 🔄 Load Balancing

### Equal Cost Multi-Path (ECMP)
```
Dwie trasy o tym samym koszcie:
10.0.0.0/8 via 192.168.1.10  cost 10
10.0.0.0/8 via 192.168.1.20  cost 10

Ruch dzielony między obie trasy:
- Per-packet (legacy)
- Per-flow (nowoczesne)
```

### Unequal Cost (EIGRP)
```
Variance 2:
10.0.0.0/8 via 192.168.1.10  metric 100
10.0.0.0/8 via 192.168.1.20  metric 150

150 < 100*2, więc obie trasy aktywne
```

## 🛡️ Route Filtering i Summarization

### Route Filtering
```cisco
# Access-list
access-list 10 deny 10.0.0.0 0.255.255.255
access-list 10 permit any

router ospf 1
 distribute-list 10 out

# Prefix-list
ip prefix-list FILTER deny 10.0.0.0/8
ip prefix-list FILTER permit 0.0.0.0/0 le 32

router ospf 1
 distribute-list prefix FILTER out
```

### Route Summarization
```
Sieci:
192.168.0.0/24
192.168.1.0/24
192.168.2.0/24
192.168.3.0/24

Summary:
192.168.0.0/22 (obejmuje .0-.3)

Binary:
192.168.0.0  = 11000000.10101000.000000 00.00000000
192.168.3.255= 11000000.10101000.000000 11.11111111
                                  ^^^^^^
                                  22 bity
```

## 🛠️ Komendy Diagnostyczne

### Wyświetlanie Tablic Routingu
```bash
# Linux
ip route show
route -n
netstat -rn

# Windows
route print
netstat -r

# Cisco
show ip route
show ip route ospf
show ip route summary
```

### Śledzenie Trasy
```bash
# Traceroute
traceroute google.com        # Linux/Mac
tracert google.com           # Windows

# MTR (My TraceRoute)
mtr google.com               # Continuous traceroute

# Cisco
traceroute 8.8.8.8
```

### Debugging Routingu
```cisco
# OSPF
show ip ospf neighbor
show ip ospf database
debug ip ospf events

# EIGRP
show ip eigrp neighbors
show ip eigrp topology
debug ip eigrp

# BGP
show ip bgp summary
show ip bgp neighbors
show ip bgp
```

## 🔍 Troubleshooting Routingu

### Problemy i Rozwiązania

#### Brak Trasy
```
Problem: Pakiety dropowane
Diagnoza: 
  - show ip route 10.0.0.0
  - ping 10.0.0.1
  
Rozwiązanie:
  - Dodaj static route
  - Sprawdź protokoły dynamiczne
  - Sprawdź default route
```

#### Routing Loop
```
Problem: Pakiety krążą w pętli
Objawy:
  - TTL exceeded
  - Duże opóźnienia
  
Diagnoza:
  - traceroute pokazuje pętlę
  - show ip route (check next-hop)
  
Rozwiązanie:
  - Popraw routing
  - Route summarization
  - Route filtering
```

#### Asymmetric Routing
```
Problem: Różne ścieżki tam i z powrotem
Skutki:
  - Problemy z firewall/NAT
  - Performance issues
  
Diagnoza:
  - traceroute z obu stron
  
Rozwiązanie:
  - Policy-based routing
  - Adjust metrics
```

## 🔗 Powiązane Tematy

- [[warstwa_sieciowa|Warstwa Sieciowa]]
- [[adresowanie_ip|Adresowanie IP]]
- [[router_dzialanie|Router - Działanie]]
- [[protokol_ip|Protokół IP]]
- [[nat_pat|NAT i PAT]]
- [[SIECI KOMPUTEROWE]]

---

#routing #trasowanie #ospf #bgp #eigrp #rip #dynamic-routing #static-routing
