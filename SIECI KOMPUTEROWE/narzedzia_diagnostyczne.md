# 🔍 Narzędzia Diagnostyczne Sieci

## 📋 Wprowadzenie

Narzędzia diagnostyczne sieci są niezbędne do analizy, monitorowania i rozwiązywania problemów sieciowych. Pozwalają na testowanie połączeń, analizę ruchu, sprawdzanie konfiguracji i identyfikację problemów.

## 🔌 Podstawowe Narzędzia

### ping - Test Połączenia

#### Podstawowe Użycie
```bash
# Linux/Mac
ping google.com
ping -c 4 8.8.8.8           # 4 pakiety
ping -i 0.5 192.168.1.1     # Co 0.5s
ping -s 1000 8.8.8.8        # Rozmiar pakietu 1000B

# Windows
ping google.com
ping -n 4 8.8.8.8           # 4 pakiety
ping -l 1000 8.8.8.8        # Rozmiar 1000B
ping -t 8.8.8.8             # Ciągły ping
```

#### Analiza Wyników
```
PING google.com (142.250.185.206): 56 data bytes
64 bytes from 142.250.185.206: icmp_seq=0 ttl=117 time=15.2 ms
64 bytes from 142.250.185.206: icmp_seq=1 ttl=117 time=14.8 ms
64 bytes from 142.250.185.206: icmp_seq=2 ttl=117 time=15.1 ms

--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss
round-trip min/avg/max/stddev = 14.8/15.0/15.2/0.2 ms

Analiza:
- 0% packet loss → Dobre połączenie
- time=15ms → Niskie opóźnienie
- ttl=117 → Pakiet przeszedł ~11 hopów (128-117)
```

#### Diagnozy
```
Request timeout → Firewall/host down
Destination unreachable → Routing problem
TTL expired → Pętla routingu lub za daleko
High latency → Przeciążenie/słabe łącze
Packet loss → Problemy z łączem
```

### traceroute/tracert - Śledzenie Ścieżki

#### Użycie
```bash
# Linux/Mac
traceroute google.com
traceroute -n google.com    # Bez DNS lookup
traceroute -m 20 google.com # Max 20 hopów

# Windows
tracert google.com
tracert -d google.com       # Bez DNS lookup
tracert -h 20 google.com    # Max 20 hopów
```

#### Przykładowy Wynik
```
traceroute to google.com (142.250.185.206), 30 hops max
 1  192.168.1.1 (192.168.1.1)  1.234 ms  1.123 ms  1.098 ms
 2  10.0.0.1 (10.0.0.1)  5.432 ms  5.321 ms  5.298 ms
 3  * * *
 4  72.14.238.1 (72.14.238.1)  15.234 ms  15.123 ms  15.098 ms
 5  142.250.185.206 (142.250.185.206)  16.234 ms  16.123 ms  16.098 ms

Analiza:
- Hop 1: Gateway (router lokalny)
- Hop 2: ISP router
- Hop 3: * * * → Firewall blokuje ICMP/timeout
- Hop 4-5: Google network
```

#### MTR (My TraceRoute)
```bash
# Ciągły traceroute z statystykami
mtr google.com
mtr -n google.com           # Bez DNS
mtr -r -c 100 google.com    # Report mode, 100 pakietów

Wynik:
Host                    Loss%   Snt   Last   Avg  Best  Wrst
1. 192.168.1.1           0.0%   100    1.2   1.3   1.1   2.5
2. 10.0.0.1              0.0%   100    5.4   5.5   5.2   7.8
3. 72.14.238.1           2.0%   100   15.2  15.4  15.0  18.9
```

### nslookup/dig/host - DNS Lookup

#### nslookup (Wszędzie)
```bash
# Podstawowe
nslookup google.com

# Specific DNS server
nslookup google.com 8.8.8.8

# Typ rekordu
nslookup -type=MX google.com
nslookup -type=NS google.com
nslookup -type=TXT google.com

# Reverse lookup
nslookup 8.8.8.8
```

#### dig (Linux/Mac - bardziej szczegółowe)
```bash
# Podstawowe
dig google.com

# Krótka odpowiedź
dig google.com +short

# Specific DNS server
dig @8.8.8.8 google.com

# Typ rekordu
dig google.com MX
dig google.com NS
dig google.com ANY

# Trace (pokazuje całą ścieżkę DNS)
dig +trace google.com

# Reverse lookup
dig -x 8.8.8.8
```

#### host (Linux/Mac - proste)
```bash
host google.com
host -t MX google.com
host -t NS google.com
host 8.8.8.8            # Reverse
```

### netstat/ss - Połączenia i Porty

#### netstat
```bash
# Wszystkie połączenia
netstat -a

# TCP/UDP listening ports
netstat -tuln              # Linux
netstat -ano               # Windows

# Z nazwami programów
netstat -tulnp             # Linux (wymaga root)
netstat -ano | findstr :80 # Windows

# Routing table
netstat -r
netstat -rn                # Bez DNS lookup

# Statystyki interfejsów
netstat -i                 # Linux
netstat -e                 # Windows
```

#### ss (nowszy zamiennik netstat - Linux)
```bash
# Wszystkie TCP sockets
ss -ta

# Listening ports
ss -tuln

# Z procesami
ss -tulnp

# Statystyki
ss -s

# Filtrowanie
ss -tn dst 192.168.1.100
ss -tn sport :80
```

### arp - Tablica ARP

#### Podstawowe
```bash
# Wyświetl tablicę ARP
arp -a                     # Wszystkie

# Linux - nowsze
ip neigh                   # Zamiast arp
ip neigh show dev eth0     # Dla interfejsu

# Dodaj wpis statyczny
arp -s 192.168.1.100 00:11:22:33:44:55

# Usuń wpis
arp -d 192.168.1.100

# Wyczyść tablicę (Linux)
ip -s neigh flush all
```

### route/ip route - Tablica Routingu

#### route (legacy)
```bash
# Wyświetl
route -n                   # Linux (bez DNS)
route print                # Windows

# Dodaj trasę statyczną
route add -net 10.0.0.0/8 gw 192.168.1.254    # Linux
route add 10.0.0.0 mask 255.0.0.0 192.168.1.254   # Windows

# Usuń
route del -net 10.0.0.0/8  # Linux
route delete 10.0.0.0      # Windows
```

#### ip route (Linux - nowocześniejsze)
```bash
# Wyświetl
ip route show
ip route show dev eth0

# Dodaj
ip route add 10.0.0.0/8 via 192.168.1.254
ip route add default via 192.168.1.1

# Usuń
ip route del 10.0.0.0/8
```

## 🔬 Zaawansowane Narzędzia

### tcpdump - Przechwytywanie Pakietów (Linux/Mac)

#### Podstawowe
```bash
# Wszystkie pakiety na interfejsie
tcpdump -i eth0

# Zapisz do pliku
tcpdump -i eth0 -w capture.pcap

# Czytaj z pliku
tcpdump -r capture.pcap

# Verbose
tcpdump -i eth0 -vvv
```

#### Filtry
```bash
# Host
tcpdump -i eth0 host 192.168.1.100
tcpdump -i eth0 src 192.168.1.100
tcpdump -i eth0 dst 192.168.1.100

# Port
tcpdump -i eth0 port 80
tcpdump -i eth0 dst port 443

# Protokół
tcpdump -i eth0 tcp
tcpdump -i eth0 udp
tcpdump -i eth0 icmp

# Kombinacje
tcpdump -i eth0 'tcp port 80 and host 192.168.1.100'
tcpdump -i eth0 'tcp and (port 80 or port 443)'
tcpdump -i eth0 'not port 22'

# Flagi TCP
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'  # SYN packets
```

#### Zaawansowane
```bash
# Pokaż hex i ASCII
tcpdump -i eth0 -X

# Zwiększ snapshot length
tcpdump -i eth0 -s 65535

# Rotacja plików (100 plików × 100MB)
tcpdump -i eth0 -w capture.pcap -C 100 -W 100
```

### Wireshark - GUI Analyzer

#### Użycie
```
1. Wybierz interfejs (eth0, wlan0, etc.)
2. Start capture
3. Zatrzymaj po zebraniu danych
4. Analiza z filtrami
```

#### Filtry Wyświetlania
```
# Display filters (nie capture filters!)
ip.addr == 192.168.1.100
tcp.port == 80
http
dns
icmp

# Kombinacje
ip.src == 192.168.1.100 && tcp.port == 443
http.request.method == "POST"
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Follow TCP stream (prawy klik → Follow → TCP Stream)
```

#### Capture Filters (BPF - Berkeley Packet Filter)
```
host 192.168.1.100
port 80
tcp port 443
not broadcast and not multicast
```

### nmap - Port Scanning

#### Podstawowe Skany
```bash
# Skan pojedynczego hosta
nmap 192.168.1.100

# Skan sieci
nmap 192.168.1.0/24

# Skan zakres portów
nmap -p 1-1000 192.168.1.100
nmap -p 80,443,22 192.168.1.100
nmap -p- 192.168.1.100       # Wszystkie porty (1-65535)
```

#### Typy Skanów
```bash
# TCP SYN scan (domyślny, wymaga root)
nmap -sS 192.168.1.100

# TCP Connect scan
nmap -sT 192.168.1.100

# UDP scan
nmap -sU 192.168.1.100

# Wykrywanie OS
nmap -O 192.168.1.100

# Wersje serwisów
nmap -sV 192.168.1.100

# Aggressive scan (OS, version, scripts, traceroute)
nmap -A 192.168.1.100

# Szybki skan (top 100 portów)
nmap -F 192.168.1.100
```

#### NSE Scripts
```bash
# Lista skryptów
nmap --script-help all

# Vulnerability scan
nmap --script vuln 192.168.1.100

# SMB enum
nmap --script smb-enum-shares 192.168.1.100

# HTTP info
nmap --script http-title,http-headers 192.168.1.100
```

### iperf3 - Test Przepustowości

#### Server
```bash
# Start server
iperf3 -s
iperf3 -s -p 5201            # Custom port
```

#### Client
```bash
# TCP test (10 seconds)
iperf3 -c server_ip

# UDP test
iperf3 -c server_ip -u -b 100M   # 100 Mbps

# Reverse mode (server→client)
iperf3 -c server_ip -R

# Parallel streams
iperf3 -c server_ip -P 4         # 4 streams

# Time duration
iperf3 -c server_ip -t 60        # 60 seconds
```

### curl/wget - HTTP Testing

#### curl
```bash
# GET request
curl https://example.com

# Verbose (pokaż headers)
curl -v https://example.com

# Tylko headers
curl -I https://example.com

# POST request
curl -X POST -d "param=value" https://example.com/api

# JSON POST
curl -X POST -H "Content-Type: application/json" \
     -d '{"key":"value"}' https://api.example.com

# Save to file
curl -o output.html https://example.com

# Follow redirects
curl -L https://example.com

# Timing info
curl -w "@curl-format.txt" -o /dev/null -s https://example.com

# curl-format.txt:
#   time_namelookup:  %{time_namelookup}\n
#   time_connect:     %{time_connect}\n
#   time_total:       %{time_total}\n
```

### netcat (nc) - Swiss Army Knife

#### Port Scanning
```bash
# Test portu TCP
nc -zv example.com 80

# Skan portów
nc -zv example.com 20-100

# Test portu UDP
nc -uzv example.com 53
```

#### Transfer Plików
```bash
# Receiver (server)
nc -l -p 1234 > received_file.txt

# Sender (client)
nc server_ip 1234 < file_to_send.txt
```

#### Chat/Remote Shell
```bash
# Server
nc -l -p 1234

# Client
nc server_ip 1234

# Remote shell (NIEBEZPIECZNE!)
# Server
nc -l -p 1234 -e /bin/bash

# Client
nc server_ip 1234
```

## 🛠️ Narzędzia Specjalistyczne

### hping3 - Advanced Packet Crafting
```bash
# ICMP ping
hping3 -1 192.168.1.100

# SYN scan
hping3 -S -p 80 192.168.1.100

# UDP scan
hping3 -2 -p 53 192.168.1.100

# Spoofed source
hping3 -a 10.0.0.1 -S -p 80 192.168.1.100
```

### iftop - Real-time Bandwidth Monitor
```bash
iftop -i eth0
iftop -i eth0 -n          # Bez DNS lookup
iftop -i eth0 -B          # Bytes zamiast bits
```

### speedtest-cli - Internet Speed Test
```bash
speedtest-cli
speedtest-cli --simple
speedtest-cli --json
```

## 🔗 Powiązane Tematy

- [[rozwiazywanie_problemow|Rozwiązywanie Problemów Sieciowych]]
- [[warstwa_sieciowa|Warstwa Sieciowa]]
- [[warstwa_transportowa|Warstwa Transportowa]]
- [[routing_podstawy|Routing]]
- [[SIECI KOMPUTEROWE]]

---

#narzędzia #diagnostyka #troubleshooting #ping #traceroute #tcpdump #wireshark #nmap
