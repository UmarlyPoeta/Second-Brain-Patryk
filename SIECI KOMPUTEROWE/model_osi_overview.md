# 🔷 Model OSI - Przegląd

## 📋 Wprowadzenie

Model OSI (Open Systems Interconnection) to standardowy model referencyjny opisujący sposób komunikacji systemów komputerowych w sieci. Został opracowany przez ISO (International Organization for Standardization) w latach 80. XX wieku.

## 🏗️ Siedem Warstw Modelu OSI

### Tabela warstw
```
┌─────────────────────────────────────────┐
│  7. Warstwa Aplikacji (Application)     │  <- Dane użytkownika
├─────────────────────────────────────────┤
│  6. Warstwa Prezentacji (Presentation)  │  <- Formatowanie, szyfrowanie
├─────────────────────────────────────────┤
│  5. Warstwa Sesji (Session)             │  <- Zarządzanie sesjami
├─────────────────────────────────────────┤
│  4. Warstwa Transportowa (Transport)    │  <- Segmenty (TCP/UDP)
├─────────────────────────────────────────┤
│  3. Warstwa Sieciowa (Network)          │  <- Pakiety (IP)
├─────────────────────────────────────────┤
│  2. Warstwa Łącza Danych (Data Link)    │  <- Ramki (Ethernet)
├─────────────────────────────────────────┤
│  1. Warstwa Fizyczna (Physical)         │  <- Bity (kable, fale)
└─────────────────────────────────────────┘
```

## 📝 Skrót Mnemoniczny

**Od góry do dołu**: "**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing"
- **A**pplication
- **P**resentation
- **S**ession
- **T**ransport
- **N**etwork
- **D**ata Link
- **P**hysical

**Po polsku**: "**A**sia **P**ije **S**ok **T**ruskawkowy **N**a **D**użym **P**odwórku"

## 🔍 Szczegółowy Opis Warstw

### [[warstwa_aplikacji|7. Warstwa Aplikacji]]
- **Funkcja**: Interfejs użytkownika, usługi sieciowe
- **Protokoły**: HTTP, HTTPS, FTP, SMTP, DNS, SSH
- **Jednostka danych**: Dane (Data)

### [[warstwa_prezentacji|6. Warstwa Prezentacji]]
- **Funkcja**: Formatowanie, szyfrowanie, kompresja
- **Protokoły**: SSL/TLS, JPEG, MPEG, ASCII
- **Jednostka danych**: Dane (Data)

### [[warstwa_sesji|5. Warstwa Sesji]]
- **Funkcja**: Nawiązywanie, zarządzanie i kończenie sesji
- **Protokoły**: NetBIOS, RPC, SQL
- **Jednostka danych**: Dane (Data)

### [[warstwa_transportowa|4. Warstwa Transportowa]]
- **Funkcja**: Niezawodna transmisja end-to-end
- **Protokoły**: TCP, UDP, SCTP
- **Jednostka danych**: Segment (TCP) / Datagram (UDP)

### [[warstwa_sieciowa|3. Warstwa Sieciowa]]
- **Funkcja**: Routing, adresowanie logiczne
- **Protokoły**: IP, ICMP, ARP, OSPF, BGP
- **Jednostka danych**: Pakiet (Packet)

### [[warstwa_laczna|2. Warstwa Łącza Danych]]
- **Funkcja**: Adresowanie fizyczne, kontrola błędów
- **Protokoły**: Ethernet, WiFi (802.11), PPP
- **Jednostka danych**: Ramka (Frame)

### [[warstwa_fizyczna|1. Warstwa Fizyczna]]
- **Funkcja**: Transmisja bitów przez medium fizyczne
- **Technologie**: Kable (UTP, fiber), WiFi, Bluetooth
- **Jednostka danych**: Bit

## 🔄 Proces Komunikacji

### Wysyłanie danych (Enkapsulacja)
```
Aplikacja          →  Dane
Prezentacja        →  Dane (formatowane)
Sesja              →  Dane (z informacją o sesji)
Transport          →  Segment (+ port)
Sieć               →  Pakiet (+ IP)
Łącze danych       →  Ramka (+ MAC)
Fizyczna           →  Bity (sygnał elektryczny/świetlny)
```

### Odbieranie danych (Dekapsulacja)
```
Fizyczna           ←  Bity
Łącze danych       ←  Ramka (sprawdzenie MAC)
Sieć               ←  Pakiet (sprawdzenie IP)
Transport          ←  Segment (sprawdzenie portu)
Sesja              ←  Dane (odtworzenie sesji)
Prezentacja        ←  Dane (deszyfrowanie)
Aplikacja          ←  Dane (wyświetlenie)
```

## 🆚 Model OSI vs TCP/IP

| Warstwa OSI           | Warstwa TCP/IP    | Protokoły           |
|-----------------------|-------------------|---------------------|
| 7. Aplikacji          |                   |                     |
| 6. Prezentacji        | 4. Aplikacji      | HTTP, FTP, DNS      |
| 5. Sesji              |                   |                     |
| 4. Transportowa       | 3. Transportowa   | TCP, UDP            |
| 3. Sieciowa           | 2. Internetowa    | IP, ICMP            |
| 2. Łącza danych       |                   |                     |
| 1. Fizyczna           | 1. Dostępu        | Ethernet, WiFi      |

## 💡 Znaczenie Modelu OSI

### Zalety
- **Standaryzacja**: Wspólny język dla producentów
- **Modularność**: Łatwiejszy rozwój i debugowanie
- **Interoperacyjność**: Różne systemy mogą się komunikować
- **Edukacja**: Ułatwia naukę sieci komputerowych

### Zastosowania
- Projektowanie protokołów sieciowych
- Diagnostyka problemów sieciowych
- Planowanie infrastruktury IT
- Certyfikacje IT (CCNA, CompTIA Network+)

## 🔧 Przykład Praktyczny - Przeglądanie Strony WWW

1. **Warstwa 7 (Aplikacji)**: Przeglądarka wysyła żądanie HTTP
2. **Warstwa 6 (Prezentacji)**: Dane są szyfrowane (HTTPS/TLS)
3. **Warstwa 5 (Sesji)**: Nawiązana sesja HTTP
4. **Warstwa 4 (Transportowa)**: TCP dzieli dane na segmenty, port 443
5. **Warstwa 3 (Sieciowa)**: IP dodaje adres źródłowy i docelowy
6. **Warstwa 2 (Łącza)**: Ethernet dodaje adresy MAC
7. **Warstwa 1 (Fizyczna)**: Dane przekształcone na sygnały elektryczne/świetlne

## 🔗 Powiązane Tematy

- [[protokol_tcp|TCP - Transmission Control Protocol]]
- [[protokol_ip|IP - Internet Protocol]]
- [[protokol_http_https|HTTP/HTTPS]]
- [[routing_podstawy|Routing - Podstawy]]
- [[switch_dzialanie|Switch - Przełącznik]]
- [[SIECI KOMPUTEROWE]]

---

#osi #model-osi #warstwy-sieciowe #tcp-ip #protokoły #networking
