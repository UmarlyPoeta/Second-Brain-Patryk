# 🔒 NAT i PAT - Translacja Adresów

## 📋 Definicja

NAT (Network Address Translation) to mechanizm tłumaczenia prywatnych adresów IP na publiczne (i odwrotnie), umożliwiający wielu urządzeniom z prywatną siecią dostęp do Internetu przy użyciu jednego lub kilku publicznych adresów IP.

## 🔧 Typy NAT

### 1. Static NAT (Statyczny NAT)

#### Mapowanie 1:1
```
Prywatny IP     ←→    Publiczny IP
192.168.1.10    ←→    203.0.113.10
192.168.1.20    ←→    203.0.113.20
192.168.1.30    ←→    203.0.113.30

Stałe przypisanie:
- Zawsze ten sam publiczny IP dla danego prywatnego
- Używane dla serwerów (web, mail, etc.)
```

#### Konfiguracja (Cisco)
```cisco
! Inside interface
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 ip nat inside

! Outside interface  
interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.0
 ip nat outside

! Static NAT mapping
ip nat inside source static 192.168.1.10 203.0.113.10
ip nat inside source static 192.168.1.20 203.0.113.20
```

#### Zastosowania
- Serwery dostępne z Internetu
- VPN endpoints
- Urządzenia wymagające stałego IP

### 2. Dynamic NAT

#### Pool adresów publicznych
```
Prywatne: 192.168.1.0/24 (254 hosty)
Pool publiczny: 203.0.113.10 - 203.0.113.20 (11 adresów)

Dynamiczne przypisanie:
- Host A: 192.168.1.50 → 203.0.113.10 (dostępny z pool)
- Host B: 192.168.1.51 → 203.0.113.11 (dostępny z pool)
- ...
- Host L: 192.168.1.61 → Czeka (pool wyczerpany)
```

#### Konfiguracja (Cisco)
```cisco
! Definiuj ACL (które IP mają NAT)
access-list 1 permit 192.168.1.0 0.0.0.255

! Definiuj pool
ip nat pool PUBLIC_POOL 203.0.113.10 203.0.113.20 netmask 255.255.255.0

! Połącz ACL z pool
ip nat inside source list 1 pool PUBLIC_POOL

! Interfaces
interface GigabitEthernet0/0
 ip nat inside
 
interface GigabitEthernet0/1
 ip nat outside
```

### 3. PAT (Port Address Translation) / NAT Overload

#### Najpopularniejsza forma - NAT Overload
```
Wielu hostów → Jeden publiczny IP + różne porty

Przykład:
192.168.1.10:50000 → 203.0.113.1:10000
192.168.1.20:50000 → 203.0.113.1:10001
192.168.1.30:60000 → 203.0.113.1:10002
192.168.1.10:50001 → 203.0.113.1:10003

Maks. ~65,000 jednoczesnych połączeń na IP
```

#### Tablica Translacji NAT
```
Inside Local      Inside Global       Outside Local      Outside Global
192.168.1.10:5000 203.0.113.1:10000  93.184.216.34:80   93.184.216.34:80
192.168.1.20:5001 203.0.113.1:10001  8.8.8.8:53         8.8.8.8:53

Inside Local:  Prywatny IP:Port (LAN)
Inside Global: Publiczny IP:Port (translowany)
Outside Local: Adres zdalny (widziany w LAN)
Outside Global: Adres zdalny (rzeczywisty w WAN)
```

#### Konfiguracja (Cisco)
```cisco
! ACL dla źródłowych IP
access-list 1 permit 192.168.1.0 0.0.0.255

! PAT z interfejsem outside
ip nat inside source list 1 interface GigabitEthernet0/1 overload

! Lub PAT z konkretnym IP
ip nat inside source list 1 pool PUBLIC_POOL overload

! Interfaces
interface GigabitEthernet0/0
 ip nat inside
 
interface GigabitEthernet0/1
 ip nat outside
```

## 🔄 Proces Translacji NAT/PAT

### Outbound (Inside → Outside)
```
1. Pakiet z 192.168.1.10:5000 → 8.8.8.8:53
2. Router sprawdza NAT rule
3. Tworzy wpis w tablicy NAT:
   192.168.1.10:5000 → 203.0.113.1:10000
4. Zmienia Source IP:Port w pakiecie:
   203.0.113.1:10000 → 8.8.8.8:53
5. Pakiet wysyłany do Internetu
```

### Inbound (Outside → Inside)
```
1. Pakiet z 8.8.8.8:53 → 203.0.113.1:10000
2. Router sprawdza tablicę NAT
3. Znajduje wpis: 10000 → 192.168.1.10:5000
4. Zmienia Destination IP:Port:
   8.8.8.8:53 → 192.168.1.10:5000
5. Pakiet przekazany do LAN
```

## 🌐 Port Forwarding (DNAT)

### Przekierowanie portów do serwera wewnętrznego
```
Internet → Router:80 → Serwer Web (192.168.1.100:80)
Internet → Router:22 → Serwer SSH (192.168.1.100:22)
Internet → Router:3389 → Desktop RDP (192.168.1.50:3389)
```

### Konfiguracja (Cisco)
```cisco
! Port forwarding dla Web Server
ip nat inside source static tcp 192.168.1.100 80 203.0.113.1 80

! Port forwarding dla SSH
ip nat inside source static tcp 192.168.1.100 22 203.0.113.1 22

! Port forwarding z różnymi portami
ip nat inside source static tcp 192.168.1.50 3389 203.0.113.1 13389
```

### Linux (iptables)
```bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# SNAT (Source NAT) - PAT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT (Destination NAT) - Port forwarding
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.100:80
iptables -t nat -A PREROUTING -p tcp --dport 22 -j DNAT --to-destination 192.168.1.100:22
```

## 🔍 Zalety i Wady NAT

### Zalety ✓
```
1. Oszczędność adresów IPv4:
   - Tysiące urządzeń → Jeden publiczny IP
   
2. Bezpieczeństwo:
   - Ukrycie topologii wewnętrznej
   - Dodatkowa warstwa ochrony (nie bezpośredni dostęp)
   
3. Elastyczność:
   - Zmiana providera bez zmiany adresacji wewnętrznej
   - Łączenie sieci z pokrywającymi się adresami
```

### Wady ✗
```
1. Problemy z protokołami:
   - FTP (tryb aktywny)
   - SIP/VoIP (embedded IP)
   - IPsec (modyfikacja nagłówków)
   - P2P (wymagają port forwarding)
   
2. Performance:
   - Dodatkowe przetwarzanie na routerze
   - Modyfikacja checksumów
   
3. Troubleshooting:
   - Utrudnione śledzenie połączeń
   - Logi z przetłumaczonymi IP
   
4. End-to-end connectivity:
   - Brak bezpośredniej komunikacji
   - Problemy z niektórymi aplikacjami
```

## 🛡️ NAT i Bezpieczeństwo

### NAT jako "Firewall"
```
Mylne przekonanie: NAT = Firewall

Rzeczywistość:
- NAT zapewnia podstawową ochronę (ukrycie IP)
- NIE zastępuje firewalla
- Nie filtruje ruchu wychodzącego
- Stateful inspection ograniczona

Prawidłowe podejście:
NAT + Firewall + IDS/IPS
```

### ALG (Application Layer Gateway)
```
Problem: Niektóre protokoły zawierają IP/Port w payload

Rozwiązanie ALG:
- FTP ALG: Modyfikuje komendy PORT/PASV
- SIP ALG: Poprawia SDP w komunikatach SIP
- H.323 ALG: Video conferencing
- PPTP ALG: VPN passthrough

Konfiguracja (Cisco):
ip nat service ftp tcp port 21
ip nat service sip udp port 5060
```

## 🔧 Zaawansowane Konfiguracje

### NAT z Route-Map (Policy NAT)
```cisco
! Różny NAT w zależności od destination
access-list 100 permit ip 192.168.1.0 0.0.0.255 10.0.0.0 0.255.255.255
access-list 101 permit ip 192.168.1.0 0.0.0.255 any

ip nat pool POOL1 203.0.113.10 203.0.113.20 netmask 255.255.255.0
ip nat pool POOL2 203.0.113.30 203.0.113.40 netmask 255.255.255.0

route-map NAT-POLICY permit 10
 match ip address 100
 match interface GigabitEthernet0/1

route-map NAT-POLICY permit 20
 match ip address 101
 match interface GigabitEthernet0/2

ip nat inside source route-map NAT-POLICY pool POOL1
```

### Twice NAT (Double NAT)
```
Scenariusz: Nakładające się sieci

Site A: 192.168.1.0/24
Site B: 192.168.1.0/24 (konflikt!)

NAT na obu stronach:
Site A widzi Site B jako 10.1.1.0/24
Site B widzi Site A jako 10.2.1.0/24
```

### Carrier-Grade NAT (CGN/CGNAT)
```
Provider → NAT dla wielu klientów

Problem: "NAT za NAT"
Klient (192.168.1.x) → CGN (100.64.0.x) → Internet (publiczny IP)

RFC 6598: 100.64.0.0/10 dla Shared Address Space
```

## 🛠️ Diagnostyka i Troubleshooting

### Komendy Cisco
```cisco
! Tablica NAT
show ip nat translations
show ip nat translations verbose

! Statystyki
show ip nat statistics

! Debugging
debug ip nat
debug ip nat detailed

! Czyszczenie tablicy
clear ip nat translation *
clear ip nat translation inside 192.168.1.10
```

### Problemy i Rozwiązania

#### Problem: Brak NAT
```
Diagnoza:
1. show ip nat statistics
2. show ip nat translations
3. Sprawdź ACL: show access-list
4. Sprawdź interfejsy: show ip interface brief

Rozwiązanie:
- Popraw ACL
- Dodaj ip nat inside/outside
- Sprawdź routing
```

#### Problem: Wyczerpanie portów
```
Objawy:
- Nowe połączenia nie działają
- show ip nat statistics pokazuje wysoki użycie

Rozwiązanie:
- Zwiększ timeout: ip nat translation timeout 60
- Dodaj więcej publicznych IP
- Użyj większej puli portów
```

#### Problem: FTP nie działa
```
Diagnoza:
- FTP active mode wymaga NAT ALG
- Sprawdź: show ip nat translations | include ftp

Rozwiązanie:
ip nat service ftp tcp port 21
! lub użyj FTP passive mode
```

## 🔗 Powiązane Tematy

- [[warstwa_sieciowa|Warstwa Sieciowa]]
- [[adresowanie_ip|Adresowanie IP]]
- [[router_dzialanie|Router]]
- [[firewall_zasady|Firewall]]
- [[protokol_ip|Protokół IP]]
- [[SIECI KOMPUTEROWE]]

---

#nat #pat #port-forwarding #translacja-adresów #ipv4 #routing
