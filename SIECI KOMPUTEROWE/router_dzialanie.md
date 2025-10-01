# 🔧 Router - Działanie i Funkcje

## 📋 Definicja

Router to urządzenie sieciowe warstwy 3 (sieciowej), które przekazuje pakiety IP między różnymi sieciami. Podejmuje decyzje routingu na podstawie adresów IP i tablicy routingu.

## 🔧 Główne Funkcje Routera

### 1. Routing (Trasowanie)
```
Proces:
1. Odbierz pakiet IP
2. Sprawdź adres docelowy
3. Przeszukaj tablicę routingu (longest prefix match)
4. Określ next hop lub interfejs wyjściowy
5. Zmniejsz TTL o 1
6. Przelicz checksum
7. Przekaż pakiet dalej
```

### 2. Łączenie Różnych Sieci
```
Router może łączyć:
- LAN ←→ LAN
- LAN ←→ WAN
- IPv4 ←→ IPv6 (dual-stack)
- Ethernet ←→ Serial/Fiber
- Różne podsieci tej samej organizacji
```

### 3. Filtrowanie Ruchu (ACL)
```
Access Control Lists:
- Bezpieczeństwo (blokowanie IP/portów)
- QoS (priorytetyzacja ruchu)
- NAT (które IP translatować)
- Policy routing
```

### 4. NAT/PAT
```
Translacja adresów:
- Prywatne → Publiczne
- Oszczędność adresów IPv4
- Dodatkowa warstwa bezpieczeństwa
```

## 🏗️ Komponenty Routera

### Hardware

#### CPU
```
Funkcje:
- Przetwarzanie pakietów
- Protokoły routingu
- Zarządzanie
- Kontrola interfejsów

Typy:
- RISC (Reduced Instruction Set)
- ASIC (Application-Specific IC) - szybszy
```

#### RAM (Random Access Memory)
```
Przechowuje:
- Running configuration
- Tablica routingu
- Tablica ARP
- Packet buffers
- Fast switching cache

Utrata: Dane giną po restarcie
```

#### NVRAM (Non-Volatile RAM)
```
Przechowuje:
- Startup configuration
- Backup config

Zachowane po restarcie
```

#### Flash Memory
```
Przechowuje:
- IOS (Internetwork Operating System)
- Backup IOS
- Inne pliki systemowe

Może być aktualizowane
```

#### ROM (Read-Only Memory)
```
Przechowuje:
- Bootstrap program
- POST (Power-On Self Test)
- Mini IOS (ROMMON/RxBoot)

Nie może być zmienione (fabrication)
```

### Interfejsy

#### Ethernet (LAN)
```
FastEthernet:    100 Mbps
GigabitEthernet: 1 Gbps
10GbE:           10 Gbps

Auto-negotiation: speed & duplex
```

#### Serial (WAN)
```
Standardy:
- V.35
- RS-232
- HSSI (High-Speed Serial Interface)

Protokoły:
- PPP (Point-to-Point Protocol)
- HDLC (High-Level Data Link Control)
- Frame Relay (legacy)
```

#### Fiber
```
SFP (Small Form-factor Pluggable):
- 1 Gbps
- Single-mode lub Multi-mode

SFP+:
- 10 Gbps
```

## 🔄 Proces Routingu Pakietu

### Krok po Kroku
```
1. Pakiet wpływa na interfejs:
   - Sprawdź FCS (Frame Check Sequence)
   - Jeśli błąd → Drop
   
2. Dekapsulacja warstwy 2:
   - Usuń nagłówek Ethernet
   - Sprawdź Destination MAC
   - Jeśli nie pasuje → Drop (normalnie)
   
3. Sprawdź nagłówek IP:
   - Destination IP: 10.0.0.50
   - TTL: 64
   - Protocol: TCP
   
4. Lookup w tablicy routingu:
   - 10.0.0.0/8 via 192.168.2.1
   - Next hop: 192.168.2.1
   
5. Zmniejsz TTL:
   - 64 → 63
   - Jeśli TTL=0 → Drop (ICMP Time Exceeded)
   
6. Przelicz checksum:
   - TTL się zmienił → nowy checksum
   
7. ARP lookup dla next hop:
   - 192.168.2.1 → MAC: AA:BB:CC:DD:EE:FF
   - Jeśli brak w ARP → Wyślij ARP Request
   
8. Enkapsulacja warstwy 2:
   - Nowy nagłówek Ethernet
   - Src MAC: Router interface MAC
   - Dst MAC: Next hop MAC
   
9. Przekazanie pakietu:
   - Wyślij przez interfejs wyjściowy
```

### Przykład Kompletny
```
Oryginalny pakiet (LAN):
┌─────────────┬─────────────┬──────────────┬──────┐
│ Src MAC:    │ Dst MAC:    │ Src IP:      │ Data │
│ PC_MAC      │ Router_MAC  │ 192.168.1.10 │      │
│             │             │ Dst IP:      │      │
│             │             │ 10.0.0.50    │      │
└─────────────┴─────────────┴──────────────┴──────┘

Po routingu (WAN):
┌─────────────┬─────────────┬──────────────┬──────┐
│ Src MAC:    │ Dst MAC:    │ Src IP:      │ Data │
│ Router2_MAC │ NextHop_MAC │ 192.168.1.10 │      │
│             │             │ Dst IP:      │      │
│             │             │ 10.0.0.50    │      │
└─────────────┴─────────────┴──────────────┴──────┘

Zmiany:
✓ Source MAC: Router interface
✓ Destination MAC: Next hop
✓ TTL: Zmniejszone o 1
✗ IP adresy: BEZ ZMIAN (chyba że NAT)
```

## 📊 Typy Routingu

### Static Routing
```cisco
ip route 10.0.0.0 255.0.0.0 192.168.2.1
ip route 0.0.0.0 0.0.0.0 192.168.1.1        # Default route

Floating static route (backup):
ip route 10.0.0.0 255.0.0.0 192.168.3.1 200 # AD=200
```

### Dynamic Routing

#### Distance Vector (RIP, EIGRP)
```
- Wymiana tablic routingu z sąsiadami
- Periodic updates
- Metryka: Distance (hops, composite)
```

#### Link State (OSPF, IS-IS)
```
- Wymiana stanu linków (LSA)
- Budowanie topologii sieci
- SPF algorithm (Dijkstra)
- Triggered updates
```

#### Path Vector (BGP)
```
- Routing między AS (Autonomous Systems)
- Polityki routingu
- Best path selection
```

## 🔍 Funkcje Zaawansowane

### QoS (Quality of Service)
```cisco
# Klasyfikacja ruchu
class-map match-all VOICE
 match ip dscp ef

# Polityka
policy-map WAN_QOS
 class VOICE
  priority percent 30
 class VIDEO
  bandwidth percent 20
 class class-default
  fair-queue

# Aplikacja
interface Serial0/0/0
 service-policy output WAN_QOS
```

### VPN
```
Typy:
- Site-to-Site: Router ←→ Router
- Remote Access: Client ←→ Router

Protokoły:
- IPsec: Szyfrowanie IP
- GRE: Generic Routing Encapsulation (tunelowanie)
- L2TP: Layer 2 Tunneling Protocol
```

### DHCP Server
```cisco
ip dhcp excluded-address 192.168.1.1 192.168.1.10

ip dhcp pool LAN_POOL
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
 dns-server 8.8.8.8 8.8.4.4
 lease 7
```

### First Hop Redundancy (HSRP/VRRP/GLBP)
```
Problem: Single point of failure (jeden router)

Rozwiązanie:
- HSRP (Hot Standby Router Protocol) - Cisco
- VRRP (Virtual Router Redundancy Protocol) - Standard
- GLBP (Gateway Load Balancing Protocol) - Cisco

Działanie:
Router 1 (Active)  ─┐
                    ├─ Virtual IP: 192.168.1.254
Router 2 (Standby) ─┘

Klienci: Default gateway = 192.168.1.254 (wirtualny)
```

### Policy-Based Routing (PBR)
```cisco
# Route-map
route-map PBR_POLICY permit 10
 match ip address 100
 set ip next-hop 192.168.2.1

route-map PBR_POLICY permit 20
 match ip address 101
 set ip next-hop 192.168.3.1

# ACL
access-list 100 permit ip 10.1.0.0 0.0.255.255 any
access-list 101 permit ip 10.2.0.0 0.0.255.255 any

# Interface
interface GigabitEthernet0/0
 ip policy route-map PBR_POLICY
```

## 🛠️ Konfiguracja i Zarządzanie

### Cisco IOS - Podstawy
```cisco
# Tryby
Router>                          # User EXEC
Router# enable                   # Privileged EXEC
Router(config)# configure terminal    # Global config
Router(config-if)# interface Gi0/0   # Interface config

# Konfiguracja interfejsu
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 description LAN Interface
 
interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.0
 no shutdown
 description WAN Interface
```

### Routing Protocols
```cisco
# RIP
router rip
 version 2
 network 192.168.1.0
 network 10.0.0.0
 no auto-summary

# OSPF
router ospf 1
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
 network 10.0.0.0 0.255.255.255 area 1
 
# EIGRP
router eigrp 100
 network 192.168.1.0 0.0.0.255
 network 10.0.0.0 0.255.255.255
 no auto-summary
```

### Zapisywanie Konfiguracji
```cisco
# Zapis
copy running-config startup-config
write memory
wr

# Backup do TFTP
copy running-config tftp://192.168.1.100/router-backup.cfg

# Przywracanie
copy startup-config running-config
copy tftp://192.168.1.100/router-backup.cfg running-config
```

## 🔍 Diagnostyka i Troubleshooting

### Show Commands
```cisco
# Routing
show ip route
show ip route summary
show ip route 10.0.0.0

# Protocols
show ip protocols
show ip ospf neighbor
show ip eigrp neighbors
show ip bgp summary

# Interfaces
show ip interface brief
show interfaces
show interfaces GigabitEthernet0/0

# Stats
show ip traffic
show processes cpu
show memory
```

### Debug (Ostrożnie - może obciążyć router!)
```cisco
debug ip routing
debug ip packet
debug ip ospf events
debug ip eigrp

# Wyłącz debug
no debug all
undebug all
```

### Common Issues

#### Brak Routingu
```
Problem: Pakiety nie docierają do celu

Diagnoza:
1. show ip route → Czy jest trasa?
2. ping → Czy host odpowiada?
3. traceroute → Gdzie pakiet ginie?

Fix:
- Dodaj static route
- Sprawdź routing protocol
- Sprawdź firewall/ACL
```

#### Routing Loop
```
Problem: Pakiety krążą w pętli

Objawy:
- TTL exceeded
- High CPU usage

Diagnoza:
- traceroute pokazuje pętlę
- show ip route (check inconsistencies)

Fix:
- Popraw routing
- Route summarization
- Split horizon (RIP/EIGRP)
```

## 🔗 Powiązane Tematy

- [[warstwa_sieciowa|Warstwa Sieciowa]]
- [[routing_podstawy|Routing - Podstawy]]
- [[nat_pat|NAT i PAT]]
- [[adresowanie_ip|Adresowanie IP]]
- [[switch_dzialanie|Switch]]
- [[SIECI KOMPUTEROWE]]

---

#router #routing #cisco #ios #warstwa-sieciowa #ospf #eigrp #nat
