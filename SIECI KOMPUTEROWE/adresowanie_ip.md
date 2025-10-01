# 📍 Adresowanie IP (IPv4 i IPv6)

## 📋 Wprowadzenie

Adresowanie IP to system logicznej identyfikacji urządzeń w sieci. Umożliwia routing pakietów między różnymi sieciami oraz jednoznaczną identyfikację hostów.

## 🔢 IPv4 (Internet Protocol version 4)

### Struktura Adresu IPv4
```
Format: 32 bity (4 bajty)
Notacja dziesiętna z kropkami: XXX.XXX.XXX.XXX

Przykład:
192.168.1.100

Binary:
11000000.10101000.00000001.01100100

Zakres każdego oktetu: 0-255
```

### Klasy Adresów IPv4 (Classful)

```
Klasa A:
  Zakres:     1.0.0.0 - 126.255.255.255
  Maska:      255.0.0.0 (/8)
  Format:     N.H.H.H
  Sieci:      126 (2^7 - 2)
  Hosty/sieć: 16,777,214 (2^24 - 2)
  Pierwsze bity: 0

Klasa B:
  Zakres:     128.0.0.0 - 191.255.255.255
  Maska:      255.255.0.0 (/16)
  Format:     N.N.H.H
  Sieci:      16,384 (2^14)
  Hosty/sieć: 65,534 (2^16 - 2)
  Pierwsze bity: 10

Klasa C:
  Zakres:     192.0.0.0 - 223.255.255.255
  Maska:      255.255.255.0 (/24)
  Format:     N.N.N.H
  Sieci:      2,097,152 (2^21)
  Hosty/sieć: 254 (2^8 - 2)
  Pierwsze bity: 110

Klasa D (Multicast):
  Zakres:     224.0.0.0 - 239.255.255.255
  Pierwsze bity: 1110

Klasa E (Eksperymentalne):
  Zakres:     240.0.0.0 - 255.255.255.255
  Pierwsze bity: 1111
```

### Adresy Specjalne IPv4

```
0.0.0.0/8           - "This network" (routing)
10.0.0.0/8          - Private (RFC 1918) - Klasa A
127.0.0.0/8         - Loopback (localhost)
127.0.0.1           - Localhost (standardowy)
169.254.0.0/16      - Link-Local (APIPA - Automatic Private IP Addressing)
172.16.0.0/12       - Private (RFC 1918) - Klasa B
192.0.0.0/24        - IETF Protocol Assignments
192.0.2.0/24        - TEST-NET-1 (dokumentacja)
192.168.0.0/16      - Private (RFC 1918) - Klasa C
198.18.0.0/15       - Benchmark testing
224.0.0.0/4         - Multicast
255.255.255.255     - Limited broadcast
```

### Adresy Prywatne (RFC 1918)

Nie są routowane w Internecie, używane w sieciach lokalnych:
```
10.0.0.0/8          - 10.0.0.0 - 10.255.255.255     (1 sieć A)
172.16.0.0/12       - 172.16.0.0 - 172.31.255.255   (16 sieci B)
192.168.0.0/16      - 192.168.0.0 - 192.168.255.255 (256 sieci C)
```

## 🔢 IPv6 (Internet Protocol version 6)

### Struktura Adresu IPv6
```
Format: 128 bitów (16 bajtów)
Notacja: 8 grup po 16 bitów (4 cyfry hex)

Pełny format:
2001:0db8:85a3:0000:0000:8a2e:0370:7334

Zasady skracania:
1. Wiodące zera w grupie można pominąć:
   2001:db8:85a3:0:0:8a2e:370:7334

2. Ciąg zer można zastąpić :: (raz w adresie):
   2001:db8:85a3::8a2e:370:7334

3. Localhost:
   ::1  (zamiast 0000:0000:0000:0000:0000:0000:0000:0001)
```

### Typy Adresów IPv6

#### Unicast
```
Global Unicast:
  2000::/3  - Publicznie routowalne (Internet)
  
Unique Local (ULA):
  fc00::/7  - Prywatne (jak 192.168.x.x w IPv4)
  fd00::/8  - Najczęściej używane
  
Link-Local:
  fe80::/10 - Automatycznie generowane, nie routowane
  Przykład: fe80::1
```

#### Multicast
```
ff00::/8  - Wszystkie adresy multicast

Zakresy:
ff01::/16 - Interface-local
ff02::/16 - Link-local
ff05::/16 - Site-local
ff0e::/16 - Global

Popularne:
ff02::1   - Wszystkie węzły (link-local)
ff02::2   - Wszystkie routery (link-local)
ff02::1:2 - DHCPv6 servers
```

#### Anycast
- Ten sam adres przypisany do wielu interfejsów
- Pakiet trafia do najbliższego węzła

### Format IPv6 z Prefiksem
```
2001:db8:85a3::8a2e:370:7334/64

Struktura:
┌────────────────────────────────┬────────────────────────────────┐
│      Network Prefix (64)       │     Interface ID (64)          │
└────────────────────────────────┴────────────────────────────────┘

Network prefix: Identyfikuje sieć
Interface ID: Identyfikuje host (często z MAC - EUI-64)
```

### Konfiguracja IPv6

#### SLAAC (Stateless Address Autoconfiguration)
```
1. Host generuje link-local (fe80::...)
2. Router Advertisement zawiera prefix (np. 2001:db8::/64)
3. Host generuje Interface ID (z MAC lub random)
4. Host ma globalny adres: 2001:db8::generated-id/64
```

#### DHCPv6 (Stateful)
```
Podobnie do DHCP w IPv4, ale:
- Stateful: Serwer przydziela pełny adres
- Stateless: Serwer podaje tylko dodatkowe opcje (DNS, etc.)
```

### EUI-64 (Extended Unique Identifier)
Generowanie Interface ID z adresu MAC:
```
MAC: 00:1A:2B:3C:4D:5E

1. Podziel na pół: 00:1A:2B | 3C:4D:5E
2. Wstaw FF:FE:  00:1A:2B:FF:FE:3C:4D:5E
3. Odwróć 7. bit: 02:1A:2B:FF:FE:3C:4D:5E
4. Interface ID: 021a:2bff:fe3c:4d5e

Wynikowy IPv6:
2001:db8::21a:2bff:fe3c:4d5e/64
```

## 🔀 Podział na Podsieci (Subnetting)

### Maska Podsieci (Subnet Mask)

#### Notacja
```
Dziesiętna:   255.255.255.0
Binarna:      11111111.11111111.11111111.00000000
CIDR:         /24

1 = część sieciowa
0 = część hostowa
```

#### Popularne Maski
```
/8   = 255.0.0.0        = 16,777,214 hostów
/16  = 255.255.0.0      = 65,534 hostów
/24  = 255.255.255.0    = 254 hosty
/25  = 255.255.255.128  = 126 hostów
/26  = 255.255.255.192  = 62 hosty
/27  = 255.255.255.224  = 30 hostów
/28  = 255.255.255.240  = 14 hostów
/29  = 255.255.255.248  = 6 hostów
/30  = 255.255.255.252  = 2 hosty (link point-to-point)
/31  = 255.255.255.254  = 2 hosty (RFC 3021, bez broadcast)
/32  = 255.255.255.255  = 1 host (host route)
```

### Obliczenia Subnettingu

#### Przykład: 192.168.1.0/24 → 4 podsieci

```
1. Określ liczbę potrzebnych bitów:
   4 podsieci = 2^2, więc 2 bity

2. Nowa maska: /24 + 2 = /26 (255.255.255.192)

3. Rozmiar podsieci: 2^(32-26) = 64 adresy
   Użyteczne hosty: 64 - 2 = 62

4. Podsieci:
   192.168.1.0/26    (0-63)     Network: .0    Broadcast: .63
   192.168.1.64/26   (64-127)   Network: .64   Broadcast: .127
   192.168.1.128/26  (128-191)  Network: .128  Broadcast: .191
   192.168.1.192/26  (192-255)  Network: .192  Broadcast: .255
```

#### Tablica /24
```
Podsieci  Bity  Maska      CIDR  Hosty/podsieć
2         1     .128       /25   126
4         2     .192       /26   62
8         3     .224       /27   30
16        4     .240       /28   14
32        5     .248       /29   6
64        6     .252       /30   2
128       7     .254       /31   2 (bez broadcast)
```

### VLSM (Variable Length Subnet Mask)

Różne rozmiary podsieci w tej samej sieci:
```
Sieć: 192.168.1.0/24

Wymagania:
- Oddział A: 100 hostów → /25 (126 hostów)
- Oddział B: 50 hostów  → /26 (62 hosty)
- Oddział C: 20 hostów  → /27 (30 hostów)
- Links: 3x2 hosty      → 3x /30 (2 hosty każdy)

Podział:
192.168.1.0/25    - Oddział A (0-127)
192.168.1.128/26  - Oddział B (128-191)
192.168.1.192/27  - Oddział C (192-223)
192.168.1.224/30  - Link 1 (224-227)
192.168.1.228/30  - Link 2 (228-231)
192.168.1.232/30  - Link 3 (232-235)
```

## 🔍 Określanie Sieci i Hosta

### Operacja AND
```
IP:      192.168.1.130    11000000.10101000.00000001.10000010
Maska:   255.255.255.192  11111111.11111111.11111111.11000000
                          ────────────────────────────────────
Network: 192.168.1.128    11000000.10101000.00000001.10000000
```

### Broadcast Address
```
Network:   192.168.1.128  11000000.10101000.00000001.10 000000
Broadcast: 192.168.1.191  11000000.10101000.00000001.10 111111
                                                          ^^^^^^
                                                       (hosty=1)
```

### Zakres Użytecznych Adresów
```
Sieć: 192.168.1.128/26

Network:    192.168.1.128 (nie przydzielaj)
Pierwszy:   192.168.1.129 (pierwszy użyteczny)
Ostatni:    192.168.1.190 (ostatni użyteczny)
Broadcast:  192.168.1.191 (nie przydzielaj)

Użyteczne hosty: 62 (190 - 129 + 1)
```

## 🛠️ Narzędzia i Komendy

### Sprawdzenie Konfiguracji IP
```bash
# Linux
ip addr show
ip -4 addr       # Tylko IPv4
ip -6 addr       # Tylko IPv6

# Windows
ipconfig
ipconfig /all

# Mac
ifconfig
```

### Kalkulator Podsieci
```bash
# ipcalc (Linux)
ipcalc 192.168.1.0/24
ipcalc 192.168.1.0/255.255.255.0

# sipcalc
sipcalc 192.168.1.0/24
sipcalc 2001:db8::/32

# Online:
# https://www.subnet-calculator.com/
```

### Test Połączenia
```bash
# IPv4
ping 192.168.1.1
ping -c 4 8.8.8.8

# IPv6
ping6 2001:4860:4860::8888
ping6 fe80::1%eth0  # Link-local wymaga interfejsu
```

## 🔗 Powiązane Tematy

- [[warstwa_sieciowa|Warstwa Sieciowa]]
- [[protokol_ip|Protokół IP]]
- [[podsieci_maski|Podsieci i Maski - Zaawansowane]]
- [[routing_podstawy|Routing - Podstawy]]
- [[nat_pat|NAT i PAT]]
- [[SIECI KOMPUTEROWE]]

---

#adresowanie #ip #ipv4 #ipv6 #subnetting #vlsm #cidr #maski-sieci
