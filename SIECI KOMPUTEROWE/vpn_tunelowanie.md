# 🔗 VPN - Virtual Private Network

## 📋 Definicja

VPN (Virtual Private Network) to technologia umożliwiająca tworzenie bezpiecznego, szyfrowanego połączenia przez niezaufaną sieć (np. Internet). Tworzy "tunel" chroniący dane przed podsłuchem i modyfikacją.

## 🌐 Typy VPN

### 1. Remote Access VPN
```
Użytkownik zdalny → VPN → Sieć korporacyjna

Scenariusze:
- Praca zdalna (home office)
- Podróże służbowe
- Dostęp mobilny

Architektura:
[Laptop/Phone] ←→ Internet ←→ [VPN Server] ←→ [Corporate LAN]
```

### 2. Site-to-Site VPN
```
Sieć A ←→ VPN ←→ Sieć B

Scenariusze:
- Łączenie oddziałów firmy
- Połączenie data centers
- Partner/vendor access

Architektura:
[Office A] ←→ [Router VPN] ←→ Internet ←→ [Router VPN] ←→ [Office B]
```

### 3. Client-to-Site (Hybrid)
```
Kombinacja remote access i site-to-site
```

## 🔐 Protokoły VPN

### IPsec (IP Security)

#### Komponenty
```
1. AH (Authentication Header):
   - Integralność
   - Autentykacja
   - Nie szyfruje danych
   - Protocol number: 51

2. ESP (Encapsulating Security Payload):
   - Integralność
   - Autentykacja
   - Szyfrowanie
   - Protocol number: 50

3. IKE (Internet Key Exchange):
   - Negocjacja parametrów
   - Wymiana kluczy
   - UDP port 500 (IKEv1/v2)
   - UDP port 4500 (NAT-T)
```

#### Tryby IPsec

##### Transport Mode
```
Struktura pakietu:
[Original IP Header][IPsec Header][Payload]

Zastosowanie:
- End-to-end (host-to-host)
- Tylko payload szyfrowany
- IP headers widoczne

Przykład:
PC ←→ Server (both with IPsec)
```

##### Tunnel Mode
```
Struktura pakietu:
[New IP Header][IPsec Header][Original IP Header + Payload]

Zastosowanie:
- Site-to-site VPN
- Remote access VPN
- Cały oryginalny pakiet szyfrowany

Przykład:
Office A ←→ VPN Gateway ←→ VPN Gateway ←→ Office B
```

#### Fazy IKE

##### Phase 1 (IKE SA)
```
Cel: Secure channel for Phase 2

Tryby (IKEv1):
- Main Mode: 6 messages (bezpieczniejszy)
- Aggressive Mode: 3 messages (szybszy, mniej bezpieczny)

IKEv2: 4 messages (zawsze)

Negocjacja:
- Encryption: AES, 3DES
- Hash: SHA-256, SHA-1
- Authentication: PSK, certificates
- DH Group: 14 (2048-bit), 19 (256-bit ECC)
```

##### Phase 2 (IPsec SA)
```
Cel: Tunel danych

Quick Mode (IKEv1): 3 messages
CREATE_CHILD_SA (IKEv2)

Negocjacja:
- ESP/AH
- Encryption
- Hash
- Lifetime
- PFS (Perfect Forward Secrecy)
```

#### Konfiguracja IPsec (Cisco)
```cisco
! IKE Phase 1
crypto isakmp policy 10
 encryption aes 256
 hash sha256
 authentication pre-share
 group 14
 lifetime 86400

crypto isakmp key MySecretKey address 203.0.113.1

! IKE Phase 2
crypto ipsec transform-set MY_TS esp-aes 256 esp-sha256-hmac
 mode tunnel

! Crypto map
crypto map VPN_MAP 10 ipsec-isakmp
 set peer 203.0.113.1
 set transform-set MY_TS
 match address VPN_TRAFFIC

! ACL
ip access-list extended VPN_TRAFFIC
 permit ip 192.168.1.0 0.0.0.255 10.0.0.0 0.0.0.255

! Apply to interface
interface GigabitEthernet0/1
 crypto map VPN_MAP
```

### OpenVPN

#### Charakterystyka
```
Protokół: SSL/TLS based
Transport: TCP 1194 lub UDP 1194
Szyfrowanie: OpenSSL library (AES, etc.)
Autentykacja: Certificates, username/password, 2FA

Zalety:
✓ Open-source
✓ Cross-platform (Windows, Linux, Mac, mobile)
✓ Przechodzi przez NAT/firewalle (TCP 443)
✓ Elastyczna konfiguracja

Wady:
✗ Wymaga client software
✗ Może być wolniejszy od IPsec
```

#### Konfiguracja Server (Linux)
```bash
# Instalacja
apt install openvpn easy-rsa

# Generuj CA i certyfikaty
make-cadir ~/openvpn-ca
cd ~/openvpn-ca
./easyrsa init-pki
./easyrsa build-ca
./easyrsa gen-dh
./easyrsa build-server-full server nopass
./easyrsa build-client-full client1 nopass

# Konfiguracja server (server.conf)
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem
server 10.8.0.0 255.255.255.0
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
cipher AES-256-CBC
auth SHA256
user nobody
group nogroup
persist-key
persist-tun

# Start
systemctl start openvpn@server
```

#### Konfiguracja Client
```
# client.ovpn
client
dev tun
proto udp
remote vpn.example.com 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client1.crt
key client1.key
remote-cert-tls server
cipher AES-256-CBC
auth SHA256
verb 3

# Połącz
openvpn --config client.ovpn
```

### WireGuard

#### Charakterystyka
```
Protokół: Własny (UDP-based)
Port: Dowolny (domyślnie 51820)
Szyfrowanie: ChaCha20, Curve25519
Kod: ~4000 linii (vs OpenVPN ~100k)

Zalety:
✓ Bardzo szybki (kernel space)
✓ Prosty (łatwa konfiguracja)
✓ Nowoczesna kryptografia
✓ Mniejsze zużycie baterii (mobile)
✓ Roaming (zmiana IP bez reconnect)

Wady:
✗ Stosunkowo nowy
✗ Przechowuje IP klientów (privacy concern)
```

#### Konfiguracja Server (Linux)
```bash
# Instalacja
apt install wireguard

# Generuj klucze
wg genkey | tee server_private.key | wg pubkey > server_public.key
wg genkey | tee client_private.key | wg pubkey > client_public.key

# Konfiguracja server (/etc/wireguard/wg0.conf)
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server_private_key>
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32

# Start
wg-quick up wg0
systemctl enable wg-quick@wg0
```

#### Konfiguracja Client
```
[Interface]
Address = 10.0.0.2/24
PrivateKey = <client_private_key>
DNS = 8.8.8.8

[Peer]
PublicKey = <server_public_key>
Endpoint = vpn.example.com:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

### PPTP (Point-to-Point Tunneling Protocol)
```
Port: TCP 1723 + GRE (Protocol 47)
Status: PRZESTARZAŁE, NIEBEZPIECZNE

Problemy:
✗ Słabe szyfrowanie (MS-CHAPv2)
✗ Znane exploity
✗ NSA-capable decryption

Nie używaj! Alternatywy: L2TP/IPsec, OpenVPN, WireGuard
```

### L2TP/IPsec
```
L2TP (Layer 2 Tunneling Protocol):
- Port: UDP 1701
- Nie szyfruje (tylko tuneluje)

IPsec:
- Szyfrowanie i autentykacja

Kombinacja:
L2TP (tunelowanie) + IPsec (szyfrowanie)

Zalety:
✓ Wbudowana obsługa (Windows, iOS, Android)
✓ Bezpieczny (IPsec)

Wady:
✗ Wolniejszy (double encapsulation)
✗ Problemy z NAT (wymaga NAT-T)
```

## 🔧 Split Tunneling

### Full Tunnel
```
Cały ruch → VPN → Internet

┌──────┐      ┌─────────┐      ┌──────────┐
│Client│─────→│VPN Server│─────→│ Internet │
└──────┘      └─────────┘      └──────────┘

Zalety:
✓ Maksymalne bezpieczeństwo
✓ Pełna kontrola IT

Wady:
✗ Obciążenie VPN server
✗ Wyższe latency dla internetu
```

### Split Tunnel
```
Tylko ruch korporacyjny → VPN
Ruch internetowy → Direct

┌──────┐  Corporate ┌─────────┐
│Client│───────────→│VPN Server│
│      │            └─────────┘
│      │  Internet
│      │───────────→ (Direct)
└──────┘

Zalety:
✓ Niższe obciążenie VPN
✓ Szybszy dostęp do internetu

Wady:
✗ Mniejsze bezpieczeństwo
✗ Ryzyko data leakage
```

### Konfiguracja (OpenVPN)
```
# Full tunnel
push "redirect-gateway def1"

# Split tunnel
push "route 192.168.1.0 255.255.255.0"
push "route 10.0.0.0 255.0.0.0"
```

## 🛠️ VPN na Routerach

### Cisco Site-to-Site IPsec
```cisco
! Site A Router
crypto isakmp policy 10
 encryption aes 256
 hash sha256
 authentication pre-share
 group 14

crypto isakmp key SecretKey123 address 203.0.113.2

crypto ipsec transform-set ESP_AES_SHA esp-aes 256 esp-sha256-hmac
 mode tunnel

crypto map SITE_TO_SITE 10 ipsec-isakmp
 set peer 203.0.113.2
 set transform-set ESP_AES_SHA
 match address VPN_TRAFFIC

ip access-list extended VPN_TRAFFIC
 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255

interface GigabitEthernet0/1
 ip address 203.0.113.1 255.255.255.0
 crypto map SITE_TO_SITE
```

### pfSense/OPNsense
```
1. VPN → IPsec → Tunnels → Add
2. General:
   - Remote Gateway: 203.0.113.2
   - Pre-Shared Key: SecretKey123
3. Phase 1:
   - Encryption: AES256
   - Hash: SHA256
   - DH Group: 14
4. Phase 2:
   - Local Network: 192.168.1.0/24
   - Remote Network: 192.168.2.0/24
   - Protocol: ESP
   - Encryption: AES256
   - Hash: SHA256
```

## 🔍 Troubleshooting VPN

### Sprawdzanie Statusu

#### IPsec (Cisco)
```cisco
show crypto isakmp sa
show crypto ipsec sa
show crypto session
debug crypto isakmp
debug crypto ipsec
```

#### OpenVPN
```bash
# Status
systemctl status openvpn@server

# Logi
journalctl -u openvpn@server -f
tail -f /var/log/openvpn.log

# Połączeni klienci
cat /var/log/openvpn-status.log
```

#### WireGuard
```bash
wg show
wg show wg0
```

### Typowe Problemy

#### Phase 1 Failure
```
Problem: IKE SA nie nawiązane

Przyczyny:
- Błędny pre-shared key
- Niezgodne encryption/hash
- Firewall blokuje UDP 500/4500

Diagnoza:
show crypto isakmp sa  # Powinno być QM_IDLE lub ACTIVE
debug crypto isakmp
```

#### Phase 2 Failure
```
Problem: IPsec SA nie nawiązane

Przyczyny:
- Niezgodne proxy ACL (interesting traffic)
- Niezgodne transform-set
- Firewall blokuje ESP (Protocol 50)

Diagnoza:
show crypto ipsec sa
debug crypto ipsec
```

#### Tunelowanie nie działa
```
Problem: VPN up, ale brak komunikacji

Przyczyny:
- Brak routingu
- Firewall w sieci docelowej
- NAT przed VPN

Diagnoza:
- ping przez tunel
- traceroute
- show ip route (czy są trasy przez tunel)
```

## 🔗 Powiązane Tematy

- [[bezpieczenstwo_sieci|Bezpieczeństwo Sieci]]
- [[firewall_zasady|Firewall]]
- [[warstwa_prezentacji|Warstwa Prezentacji (Szyfrowanie)]]
- [[router_dzialanie|Router]]
- [[SIECI KOMPUTEROWE]]

---

#vpn #ipsec #openvpn #wireguard #tunelowanie #szyfrowanie #remote-access
