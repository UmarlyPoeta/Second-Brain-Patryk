# 🔐 Bezpieczeństwo Sieci - Podstawy

## 📋 Wprowadzenie

Bezpieczeństwo sieci obejmuje polityki, procedury i narzędzia chroniące infrastrukturę sieciową przed nieautoryzowanym dostępem, niewłaściwym użyciem, modyfikacją i atakami.

## 🛡️ Trójkąt CIA (Fundamenty Bezpieczeństwa)

### Confidentiality (Poufność)
```
Cel: Dane dostępne tylko dla uprawnionych

Mechanizmy:
- Szyfrowanie (AES, RSA)
- Kontrola dostępu (ACL, firewalle)
- Autentykacja (hasła, certyfikaty)
- VPN (tunelowanie)

Zagrożenia:
- Podsłuch (sniffing)
- Man-in-the-Middle
- Nieautoryzowany dostęp
```

### Integrity (Integralność)
```
Cel: Dane niezmienione podczas transmisji

Mechanizmy:
- Hash functions (SHA-256, MD5)
- Digital signatures
- Checksums (CRC)
- IPsec (AH - Authentication Header)

Zagrożenia:
- Modyfikacja pakietów
- Replay attacks
- Injection attacks
```

### Availability (Dostępność)
```
Cel: Usługi dostępne gdy potrzebne

Mechanizmy:
- Redundancja (HSRP, VRRP)
- Load balancing
- DDoS mitigation
- Backup & recovery

Zagrożenia:
- DoS/DDoS
- Power failures
- Hardware failures
```

## 🔒 Mechanizmy Szyfrowania

### Szyfrowanie Symetryczne
```
Jeden klucz do szyfrowania i deszyfrowania

Algorytmy:
- AES (Advanced Encryption Standard)
  • 128, 192, 256 bit
  • Najczęściej używany
  
- 3DES (Triple DES)
  • 168 bit
  • Legacy, wolny
  
- ChaCha20
  • Nowszy, szybki
  • Mobile/IoT

Zalety:
✓ Szybki
✓ Niskie zużycie zasobów

Wady:
✗ Problem dystrybucji klucza
✗ Wymaga bezpiecznego kanału
```

### Szyfrowanie Asymetryczne
```
Para kluczy: publiczny (encrypt) + prywatny (decrypt)

Algorytmy:
- RSA (Rivest-Shamir-Adleman)
  • 2048, 3072, 4096 bit
  • Najpopularniejszy
  
- ECC (Elliptic Curve Cryptography)
  • Mniejsze klucze (256 bit ≈ RSA 3072)
  • Szybszy, efficient
  
- Diffie-Hellman
  • Wymiana kluczy
  • Nie szyfruje danych

Zastosowania:
- Key exchange
- Digital signatures
- SSL/TLS handshake
- SSH authentication

Zalety:
✓ Bezpieczna wymiana kluczy
✓ Digital signatures

Wady:
✗ Wolny
✗ Większe klucze
```

### Hybrid (Najczęściej Używane)
```
1. Asymetryczny: Wymiana session key
2. Symetryczny: Szyfrowanie danych

Przykład TLS:
1. RSA/ECDHE: Wymiana AES key
2. AES-256-GCM: Szyfrowanie HTTP traffic
```

## 🔐 Protokoły Bezpieczeństwa

### SSL/TLS (Transport Layer Security)
```
Wersje:
- SSL 2.0/3.0: PRZESTARZAŁE, niebezpieczne
- TLS 1.0/1.1: Przestarzałe (deprecated 2020)
- TLS 1.2: Obecnie używane
- TLS 1.3: Zalecane (szybsze, bezpieczniejsze)

TLS 1.3 Improvements:
✓ Szybszy handshake (1-RTT)
✓ 0-RTT resumption
✓ Usunięte słabe algorytmy
✓ Forward secrecy (mandatory)

Zastosowania:
- HTTPS (443/tcp)
- SMTPS (465/tcp)
- IMAPS (993/tcp)
```

### IPsec (IP Security)
```
Protokoły:
- AH (Authentication Header): Integralność
- ESP (Encapsulating Security Payload): Szyfrowanie

Tryby:
Transport mode:
  [IP Header][IPsec Header][Data]
  • Tylko payload szyfrowany
  • End-to-end

Tunnel mode:
  [New IP][IPsec][Original IP][Data]
  • Cały pakiet IP szyfrowany
  • Site-to-site VPN

IKE (Internet Key Exchange):
- IKEv1: Starszy (main/aggressive mode)
- IKEv2: Nowszy, lepszy (less overhead)

Zastosowania:
- Site-to-site VPN
- Remote access VPN
- Szyfrowanie na poziomie IP
```

### SSH (Secure Shell)
```
Port: 22/tcp
Zamiennik: Telnet (23/tcp - nieszyfrowany!)

Funkcje:
- Zdalny terminal
- Secure file transfer (SCP, SFTP)
- Port forwarding (tunneling)
- X11 forwarding

Autentykacja:
1. Password-based (słabsze)
2. Key-based (zalecane):
   ssh-keygen -t ed25519
   ssh-copy-id user@host

Best practices:
- Wyłącz root login
- Wyłącz password auth (tylko keys)
- Zmień port (security by obscurity)
- Użyj fail2ban (brute force protection)
```

## 🚨 Typy Ataków

### Ataki Pasywne (Podsłuch)

#### Packet Sniffing
```
Cel: Przechwycenie danych w sieci

Narzędzia:
- Wireshark
- tcpdump
- Ettercap

Ochrona:
✓ Szyfrowanie (TLS, VPN)
✓ Segmentacja sieci (VLAN)
✓ Switch zamiast hub
✓ Port security
```

#### Traffic Analysis
```
Cel: Analiza metadanych (kto z kim, kiedy)

Ochrona:
✓ VPN (ukrycie destination)
✓ Tor (anonymity)
✓ Padding (ukrycie rozmiaru)
```

### Ataki Aktywne

#### Man-in-the-Middle (MITM)
```
Atakujący pośredniczy w komunikacji:
Client ←→ Attacker ←→ Server

Typy:
- ARP spoofing
- DNS spoofing
- SSL stripping
- Rogue AP

Ochrona:
✓ HTTPS (sprawdzaj certyfikat!)
✓ HSTS (HTTP Strict Transport Security)
✓ Certificate pinning
✓ Static ARP entries
✓ DAI (Dynamic ARP Inspection)
```

#### DoS/DDoS (Denial of Service)
```
DoS: Jeden źródło ataku
DDoS: Wiele źródeł (botnet)

Typy:
1. Volumetric: Zalanie bandwidth
   - UDP flood
   - ICMP flood
   - Amplification (DNS, NTP)

2. Protocol: Wykorzystanie protokołów
   - SYN flood (TCP half-open)
   - Ping of Death
   - Smurf attack

3. Application layer: Ataki L7
   - HTTP flood
   - Slowloris
   - Application exploits

Ochrona:
✓ Rate limiting
✓ SYN cookies
✓ Anti-DDoS services (Cloudflare, Akamai)
✓ IPS/IDS
✓ Load balancing
```

#### Spoofing
```
IP Spoofing:
- Fałszowanie source IP
- Ochrona: Ingress filtering (RFC 2827)

ARP Spoofing:
- Fałszowanie ARP replies
- Ochrona: DAI, static ARP

DNS Spoofing:
- Fałszowanie DNS responses
- Ochrona: DNSSEC
```

### Exploity i Malware

#### SQL Injection
```
Wstrzyknięcie SQL w input:
' OR '1'='1

Ochrona:
✓ Prepared statements
✓ Input validation
✓ WAF (Web Application Firewall)
```

#### XSS (Cross-Site Scripting)
```
Wstrzyknięcie JavaScript w stronę

Ochrona:
✓ Output encoding
✓ Content Security Policy (CSP)
✓ Input validation
```

#### Malware/Ransomware
```
Typy:
- Virus: Infekuje pliki
- Worm: Rozprzestrzenia się sam
- Trojan: Udaje legalny program
- Ransomware: Szyfruje dane (okupy)

Ochrona:
✓ Antivirus/Antimalware
✓ Firewalle
✓ Email filtering
✓ User training
✓ Regular backups
```

## 🛠️ Narzędzia Obrony

### Firewall
```
Typy:
- Packet filtering (L3-L4)
- Stateful (connection tracking)
- Application (L7, WAF)
- NGFW (Next-Generation)

Funkcje:
- Filtrowanie ruchu (ACL)
- NAT
- VPN
- IPS/IDS
- DPI (Deep Packet Inspection)
```

### IDS/IPS
```
IDS (Intrusion Detection System):
- Wykrywa ataki
- Alarmuje
- Nie blokuje

IPS (Intrusion Prevention System):
- Wykrywa ataki
- Blokuje
- Inline mode

Metody detekcji:
1. Signature-based: Wzorce znanych ataków
2. Anomaly-based: Odchylenia od normy
3. Heuristic: Heurystyka

Narzędzia:
- Snort
- Suricata
- Zeek (Bro)
```

### VPN (Virtual Private Network)
```
Typy:
1. Remote Access:
   Client → VPN Server → Corporate Network
   
2. Site-to-Site:
   Office A ←→ VPN ←→ Office B

Protokoły:
- OpenVPN: Open-source, secure
- IPsec: Standard, hardware support
- WireGuard: Nowszy, szybszy, prostszy
- L2TP/IPsec: Compatibility
- PPTP: PRZESTARZAŁE

Split Tunneling:
- All traffic → VPN (full tunnel)
- Only corporate → VPN (split)
```

### SIEM (Security Information & Event Management)
```
Funkcje:
- Agregacja logów
- Korelacja zdarzeń
- Alarmowanie
- Compliance reporting

Narzędzia:
- Splunk
- ELK Stack (Elasticsearch, Logstash, Kibana)
- IBM QRadar
- ArcSight
```

## 🔍 Best Practices

### Defense in Depth
```
Wiele warstw obrony:
1. Perimeter: Firewall, IPS
2. Network: Segmentacja, VLAN
3. Host: Antivirus, HIPS
4. Application: WAF, input validation
5. Data: Szyfrowanie, backup
```

### Principle of Least Privilege
```
Minimalne uprawnienia:
- Users: Tylko niezbędne
- Services: Minimal permissions
- Network: Strict ACL/firewall rules
```

### Regular Updates & Patching
```
Aktualizuj:
- OS (Windows, Linux)
- Aplikacje
- Firmware (router, switch)
- Antivirus signatures
- IPS/IDS rules

Proces:
1. Test w środowisku dev
2. Deploy stopniowo
3. Monitoruj
```

### Security Awareness Training
```
Użytkownicy = najsłabsze ogniwo:
- Phishing awareness
- Strong passwords
- Social engineering
- Physical security
```

### Incident Response Plan
```
Fazy:
1. Preparation: Plan, narzędzia, team
2. Detection: Monitoring, alerty
3. Containment: Izolacja zagrożenia
4. Eradication: Usunięcie zagrożenia
5. Recovery: Przywrócenie usług
6. Lessons Learned: Post-mortem
```

## 🔗 Powiązane Tematy

- [[firewall_zasady|Firewall - Zasady i Typy]]
- [[vpn_tunelowanie|VPN - Tunelowanie]]
- [[warstwa_prezentacji|Warstwa Prezentacji (Szyfrowanie)]]
- [[wifi_standardy|WiFi - Bezpieczeństwo]]
- [[SIECI KOMPUTEROWE]]

---

#bezpieczeństwo #security #szyfrowanie #firewall #vpn #ips #ids #tls #ipsec
