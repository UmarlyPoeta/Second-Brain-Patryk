# 🔐 Firewall - Zasady i Typy

## 📋 Definicja

Firewall (zapora sieciowa) to system bezpieczeństwa, który monitoruje i kontroluje ruch sieciowy na podstawie predefiniowanych reguł bezpieczeństwa. Stanowi barierę między zaufaną siecią wewnętrzną a niezaufaną siecią zewnętrzną (Internet).

## 🛡️ Typy Firewalli

### 1. Packet Filtering Firewall (Warstwa 3-4)

#### Charakterystyka
```
Filtrowanie na podstawie:
- Source/Destination IP
- Source/Destination Port
- Protokół (TCP/UDP/ICMP)
- Flagi TCP (SYN, ACK, FIN, etc.)
```

#### Przykład reguł
```
Reguła 1: ALLOW   TCP  192.168.1.0/24  ANY     Port 80   (HTTP)
Reguła 2: ALLOW   TCP  192.168.1.0/24  ANY     Port 443  (HTTPS)
Reguła 3: ALLOW   UDP  192.168.1.0/24  8.8.8.8 Port 53   (DNS)
Reguła 4: DENY    ALL  ANY             ANY     ANY       (Default)
```

#### Zalety i Wady
```
Zalety:
✓ Szybki (minimalne przetwarzanie)
✓ Niski koszt
✓ Prosty w konfiguracji

Wady:
✗ Brak inspekcji zawartości
✗ Podatny na IP spoofing
✗ Nie rozumie stanów połączeń
```

### 2. Stateful Firewall (Warstwa 3-4)

#### Connection Tracking
```
Tablica stanów:
Source IP:Port   Dest IP:Port     Protocol  State      Timeout
192.168.1.10:500 93.184.216.34:80 TCP       ESTABLISHED 3600s
192.168.1.20:501 8.8.8.8:53       UDP       NEW        30s
192.168.1.30:502 1.1.1.1:443      TCP       TIME_WAIT  120s

Stany TCP:
NEW         - Nowe połączenie (SYN)
ESTABLISHED - Połączenie nawiązane
RELATED     - Powiązane (np. FTP data)
INVALID     - Nieprawidłowe pakiety
```

#### Przykład (iptables)
```bash
# Domyślna polityka
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Zezwól na established/related
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Zezwól na nowe połączenia SSH
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -j ACCEPT

# Zezwól na loopback
iptables -A INPUT -i lo -j ACCEPT
```

#### Zalety i Wady
```
Zalety:
✓ Śledzenie stanów połączeń
✓ Lepsza ochrona niż packet filtering
✓ Automatyczne zezwolenie na odpowiedzi
✓ Wykrywa anomalie stanów

Wady:
✗ Wyższe zużycie zasobów
✗ Nadal brak inspekcji aplikacji
✗ Podatny na ataki na warstwę aplikacji
```

### 3. Application Layer Firewall (Warstwa 7)

#### Deep Packet Inspection (DPI)
```
Inspekcja:
- Protokoły aplikacji (HTTP, FTP, SMTP)
- Zawartość payload
- Komendy aplikacji
- Wykrywanie malware
- Data Loss Prevention (DLP)
```

#### Przykład - HTTP Filtering
```
Reguły HTTP:
- Blokuj żądania z User-Agent: "malware"
- Blokuj POST do /admin bez autentykacji
- Zezwalaj tylko na GET i POST (blokuj DELETE)
- Filtruj zawartość (SQL injection, XSS)
```

#### WAF (Web Application Firewall)
```
Ochrona aplikacji web:
- OWASP Top 10
- SQL Injection detection
- XSS (Cross-Site Scripting) prevention
- CSRF protection
- Rate limiting
- Bot detection
```

### 4. Next-Generation Firewall (NGFW)

#### Funkcje NGFW
```
Traditional Firewall +
├─ Application Awareness (rozpoznawanie aplikacji)
├─ IPS (Intrusion Prevention System)
├─ SSL/TLS Inspection
├─ Advanced Malware Protection
├─ URL Filtering
├─ User Identity Integration
└─ Threat Intelligence
```

#### Przykład - Application Control
```
Reguły aplikacyjne:
- Zezwól: Office 365, Google Workspace
- Blokuj: BitTorrent, Tor
- Ogranicz bandwidth: YouTube (max 10 Mbps)
- Loguj: Facebook, Twitter
- Inspect SSL: Gmail (malware scan)
```

## 🔧 Architektury Firewall

### 1. Screened Subnet (DMZ)
```
Internet
   │
   ▼
[Firewall Outside]
   │
   ▼
DMZ (Serwery publiczne)
├─ Web Server
├─ Mail Server
└─ DNS Server
   │
   ▼
[Firewall Inside]
   │
   ▼
LAN (Sieć wewnętrzna)
```

### 2. Dual-Homed Firewall
```
Internet ←→ [Firewall] ←→ LAN
            (2 interfaces)
```

### 3. Three-Legged Firewall
```
         [Firewall]
         /    |    \
        /     |     \
   Internet  DMZ   LAN
```

### 4. Distributed Firewall
```
Central Management
       │
   ┌───┴───┬───────┐
   ▼       ▼       ▼
Branch1 Branch2  Branch3
[FW]    [FW]     [FW]
```

## 📜 Polityki i Reguły Firewall

### Domyślne Polityki

#### 1. Default Deny (Zalecane)
```
Policy: DENY ALL
Reguły: Explicite ALLOW tylko potrzebny ruch

Przykład:
Rule 1: ALLOW TCP ANY → 192.168.1.100:80  (Web)
Rule 2: ALLOW TCP ANY → 192.168.1.101:22  (SSH admin)
Default: DENY ALL
```

#### 2. Default Allow (Niezalecane)
```
Policy: ALLOW ALL
Reguły: Explicite DENY zagrożenia

Ryzyko: Wszystko dozwolone domyślnie
```

### Kolejność Reguł
```
Top-to-bottom processing:

Rule 1: ALLOW SSH from 10.0.0.0/8        ← Sprawdź pierwszą
Rule 2: DENY  SSH from ANY               ← Potem drugą
Rule 3: ALLOW HTTP from ANY              ← Itd.
Default: DENY ALL                        ← Ostatnia

Najważniejsze reguły na górze!
```

### Przykładowy Zestaw Reguł
```
# Anti-spoofing
1.  DENY  IP  127.0.0.0/8      ANY  (Loopback from outside)
2.  DENY  IP  192.168.0.0/16   ANY  (RFC 1918 from outside)
3.  DENY  IP  10.0.0.0/8       ANY  (RFC 1918 from outside)

# Management
10. ALLOW TCP  10.0.0.0/8      ANY:22   (SSH from admin network)

# Services
20. ALLOW TCP  ANY → DMZ:80           (HTTP to web server)
21. ALLOW TCP  ANY → DMZ:443          (HTTPS to web server)
22. ALLOW TCP  ANY → DMZ:25           (SMTP to mail server)

# Outbound
30. ALLOW TCP  LAN → ANY:80,443       (Web browsing)
31. ALLOW UDP  LAN → ANY:53           (DNS)
32. ALLOW TCP  LAN → ANY:22           (SSH outbound)

# ICMP
40. ALLOW ICMP LAN → ANY (echo-request)
41. ALLOW ICMP ANY → FW  (echo-request, limited)

# Default
99. DENY  ALL  ANY → ANY              (Log & drop)
```

## 🔍 Inspekcja Ruchu

### Stateless vs Stateful
```
Stateless:
Pakiet 1: SYN  192.168.1.10:5000 → 8.8.8.8:80   [ALLOW]
Pakiet 2: ACK  8.8.8.8:80 → 192.168.1.10:5000   [DENY - brak reguły]

Stateful:
Pakiet 1: SYN  192.168.1.10:5000 → 8.8.8.8:80   [ALLOW, track]
Pakiet 2: ACK  8.8.8.8:80 → 192.168.1.10:5000   [ALLOW - established]
```

### SSL/TLS Inspection
```
Problem: Szyfrowany ruch (HTTPS) nie jest widoczny

Rozwiązanie: Man-in-the-Middle Inspection
1. Client → Firewall: SSL handshake
2. Firewall → Server: Osobne SSL handshake
3. Firewall dekryptuje, inspekuje, re-enkryptuje

Wymagania:
- Certyfikat CA firewalla w zaufanych klientów
- Wydajny hardware (kryptografia)
```

### DPI (Deep Packet Inspection)
```
Analiza:
- Nagłówki (IP, TCP/UDP)
- Payload (zawartość aplikacji)
- Wzorce (signatures)
- Anomalie (heurystyka)

Detekcja:
- Malware (known signatures)
- Exploits (CVE patterns)
- Data leakage (credit cards, SSN)
- Compliance (HIPAA, PCI-DSS)
```

## 🛠️ Implementacje Firewall

### Linux iptables/nftables
```bash
# iptables - Stateful firewall
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -j DROP

# nftables (nowszy)
nft add table inet filter
nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }
nft add rule inet filter input ct state established,related accept
nft add rule inet filter input tcp dport 22 accept
```

### Windows Firewall
```powershell
# PowerShell
New-NetFirewallRule -DisplayName "Allow SSH" -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow
New-NetFirewallRule -DisplayName "Block Telnet" -Direction Outbound -Protocol TCP -RemotePort 23 -Action Block

# GUI: Windows Defender Firewall with Advanced Security
```

### pfSense/OPNsense
```
Open-source firewall/router:
- Web GUI
- Stateful firewall
- NAT, VPN (OpenVPN, IPsec, WireGuard)
- Packages: Snort/Suricata (IDS/IPS), Squid (proxy)
```

### Cisco ASA
```cisco
! Access-list
access-list OUTSIDE_IN extended permit tcp any host 203.0.113.10 eq 80
access-list OUTSIDE_IN extended deny ip any any log

! Apply to interface
access-group OUTSIDE_IN in interface outside

! Object groups
object-group service WEB_SERVICES
 service-object tcp destination eq 80
 service-object tcp destination eq 443
 
access-list OUTSIDE_IN extended permit object-group WEB_SERVICES any host 203.0.113.10
```

## 🔒 Best Practices

### 1. Zasada Najmniejszych Uprawnień
```
Zezwalaj tylko na niezbędny ruch:
- Specific source/destination
- Specific ports/protocols
- Specific time windows (jeśli możliwe)
```

### 2. Logowanie i Monitoring
```
Loguj:
- Wszystkie deny (dropped packets)
- Krytyczne allow (admin access)
- Anomalie (port scanning, flood)

Monitoring:
- SIEM integration
- Real-time alerts
- Regular log review
```

### 3. Regularne Audyty
```
Co robić:
1. Review reguł (usuwaj nieużywane)
2. Test penetracyjny
3. Update signatures (IPS/IDS)
4. Patch management
5. Backup konfiguracji
```

### 4. Defense in Depth
```
Warstwy obrony:
1. Perimeter Firewall (brzeg sieci)
2. Internal Firewall (segmentacja)
3. Host Firewall (każdy serwer/PC)
4. Application Firewall (WAF)
5. IDS/IPS
6. Antimalware
```

## 🔗 Powiązane Tematy

- [[warstwa_sieciowa|Warstwa Sieciowa]]
- [[warstwa_transportowa|Warstwa Transportowa]]
- [[nat_pat|NAT i PAT]]
- [[bezpieczenstwo_sieci|Bezpieczeństwo Sieci]]
- [[vpn_tunelowanie|VPN]]
- [[SIECI KOMPUTEROWE]]

---

#firewall #zapora #bezpieczeństwo #acl #iptables #ngfw #waf
