# 6️⃣ Warstwa Prezentacji (Presentation Layer)

## 📋 Definicja

Warstwa prezentacji odpowiada za formatowanie, kodowanie i prezentację danych dla warstwy aplikacji. Działa jako translator między formatami danych używanymi przez aplikacje a formatem sieciowym.

## 🔧 Główne Funkcje

### 1. Translacja Danych (Data Translation)
- Konwersja między różnymi formatami danych
- Standaryzacja reprezentacji danych w sieci
- Niezależność aplikacji od formatu danych

### 2. Kodowanie/Dekodowanie
- ASCII ↔ EBCDIC
- Unicode (UTF-8, UTF-16, UTF-32)
- Kodowanie znaków specjalnych

### 3. Kompresja/Dekompresja
- Redukcja rozmiaru przesyłanych danych
- Oszczędność przepustowości
- Szybsza transmisja

### 4. Szyfrowanie/Deszyfrowanie
- Ochrona poufności danych
- Integralność danych
- Autentykacja

## 🔤 Kodowanie Danych

### Standardy Kodowania Znaków

#### ASCII (American Standard Code for Information Interchange)
```
7-bit: 0-127 znaków
8-bit extended: 0-255 znaków

Przykład:
'A' = 65 (decimal) = 0x41 (hex) = 01000001 (binary)
'a' = 97 (decimal) = 0x61 (hex) = 01100001 (binary)
```

#### EBCDIC (Extended Binary Coded Decimal Interchange Code)
- Używany w mainframe IBM
- Różne od ASCII wartości

#### Unicode
```
UTF-8 (variable length: 1-4 bytes):
  'A' = 0x41 (1 byte)
  'ą' = 0xC4 0x85 (2 bytes)
  '中' = 0xE4 0xB8 0xAD (3 bytes)
  '𝕳' = 0xF0 0x9D 0x95 0xB3 (4 bytes)

UTF-16: 2 lub 4 bajty
UTF-32: zawsze 4 bajty
```

### Base64 Encoding
- Kodowanie binarnych danych w ASCII
- 6 bitów → 1 znak ASCII
```
Oryginalny: "Hello"
Binary: 01001000 01100101 01101100 01101100 01101111
Base64: SGVsbG8=

Alfabet Base64:
A-Z, a-z, 0-9, +, /
Padding: =
```

### URL Encoding
```
Spacja → %20 lub +
!     → %21
#     → %23
%     → %25

Przykład:
"Hello World!" → "Hello%20World%21"
```

## 🗜️ Kompresja Danych

### Algorytmy Bezstratnej Kompresji

#### DEFLATE (ZIP, gzip)
- Kombinacja LZ77 i Huffman coding
- Używany w PNG, HTTP compression

#### LZ77/LZ78
- Słownikowa kompresja
- Podstawa dla wielu algorytmów

#### Huffman Coding
- Kompresja na podstawie częstotliwości
- Krótsze kody dla częstszych znaków

### Algorytmy Stratnej Kompresji

#### JPEG (obrazy)
- DCT (Discrete Cosine Transform)
- Quantization
- Stratność: regulowana jakość

#### MPEG (wideo)
- Kompresja przestrzenna i czasowa
- Klatki I, P, B

#### MP3 (audio)
- Usuwanie niesłyszalnych częstotliwości
- Psychoacoustic model

### Kompresja HTTP
```http
# Request
Accept-Encoding: gzip, deflate, br

# Response
Content-Encoding: gzip
Content-Length: 1234
```

## 🔐 Szyfrowanie i Bezpieczeństwo

### SSL/TLS (Secure Sockets Layer / Transport Layer Security)
**Funkcje**:
- Szyfrowanie połączenia
- Autentykacja serwera (certyfikat)
- Integralność danych

**Handshake TLS**:
```
Client                          Server
  │                               │
  ├─── ClientHello ──────────────→│
  │    (supported ciphers)        │
  │                               │
  │←── ServerHello ───────────────┤
  │    (chosen cipher)            │
  │    Certificate                │
  │    ServerHelloDone            │
  │                               │
  ├─── ClientKeyExchange ────────→│
  │    ChangeCipherSpec           │
  │    Finished                   │
  │                               │
  │←── ChangeCipherSpec ──────────┤
  │    Finished                   │
  │                               │
  │    ENCRYPTED DATA             │
```

### Cipher Suites
```
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384

Elementy:
- TLS: Protokół
- ECDHE: Key exchange (Elliptic Curve Diffie-Hellman Ephemeral)
- RSA: Autentykacja
- AES_256_GCM: Szyfrowanie (256-bit AES w trybie GCM)
- SHA384: Hash (integralność)
```

### Algorytmy Szyfrowania

#### Symetryczne
```
AES (Advanced Encryption Standard):
- Klucze: 128, 192, 256 bit
- Tryby: ECB, CBC, GCM, CTR

DES/3DES (przestarzałe):
- DES: 56 bit (słabe)
- 3DES: 168 bit (wolne)
```

#### Asymetryczne
```
RSA:
- Klucze: 2048, 3072, 4096 bit
- Używane do wymiany kluczy

ECC (Elliptic Curve Cryptography):
- Mniejsze klucze (256 bit ≈ RSA 3072 bit)
- Szybsze operacje
```

## 📄 Formaty Danych

### Formaty Tekstowe

#### XML (eXtensible Markup Language)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<person>
    <name>Jan Kowalski</name>
    <age>30</age>
    <city>Warszawa</city>
</person>
```

#### JSON (JavaScript Object Notation)
```json
{
    "name": "Jan Kowalski",
    "age": 30,
    "city": "Warszawa"
}
```

#### YAML
```yaml
person:
  name: Jan Kowalski
  age: 30
  city: Warszawa
```

### Formaty Binarne

#### Protocol Buffers (Protobuf)
- Google'owy format
- Bardzo wydajny
- Wymaga schema

#### MessagePack
- Binarny JSON
- Mniejszy rozmiar
- Szybszy parsing

#### ASN.1 (Abstract Syntax Notation One)
- Używany w X.509 certyfikatach
- SNMP, LDAP

## 🖼️ Kodowanie Multimediów

### Obrazy
```
JPEG: Stratne, fotografie
PNG: Bezstratne, grafika
GIF: Bezstratne, animacje (max 256 kolorów)
WebP: Nowoczesny, mały rozmiar
SVG: Wektorowy, skalowalny
```

### Wideo
```
H.264/AVC: Najpopularniejszy
H.265/HEVC: Lepsza kompresja
VP9: Google, YouTube
AV1: Otwarty standard, przyszłość
```

### Audio
```
MP3: Stratne, popularne
AAC: Lepsze od MP3
FLAC: Bezstratne
Opus: Nowoczesny, VoIP
```

## 🔄 Konwersje i Transformacje

### Endianness (Kolejność Bajtów)
```
Big-endian (network byte order):
0x12345678 → [12] [34] [56] [78]

Little-endian (x86):
0x12345678 → [78] [56] [34] [12]

Funkcje konwersji:
htonl() - host to network long
ntohl() - network to host long
htons() - host to network short
ntohs() - network to host short
```

### Serializacja/Deserializacja
```python
# JSON
import json
data = {'name': 'Jan', 'age': 30}
json_str = json.dumps(data)  # Serializacja
data_back = json.loads(json_str)  # Deserializacja

# Pickle (Python)
import pickle
binary = pickle.dumps(data)
data_back = pickle.loads(binary)
```

## 🛠️ MIME Types (Multipurpose Internet Mail Extensions)

### Struktur MIME Type
```
type/subtype; parameter=value

Przykłady:
text/html; charset=utf-8
application/json
image/png
video/mp4
application/pdf
```

### Najczęstsze MIME Types
```
text/plain          - Zwykły tekst
text/html           - HTML
text/css            - CSS
application/json    - JSON
application/xml     - XML
application/javascript - JavaScript
image/jpeg          - JPEG
image/png           - PNG
video/mp4           - MP4
audio/mpeg          - MP3
application/pdf     - PDF
```

### Content Negotiation (HTTP)
```http
# Request
Accept: application/json, text/html
Accept-Charset: utf-8
Accept-Encoding: gzip, deflate
Accept-Language: pl, en

# Response
Content-Type: application/json; charset=utf-8
Content-Encoding: gzip
Content-Language: pl
```

## 🔍 Praktyczne Zastosowania

### Email Encoding
```
MIME (Multipurpose Internet Mail Extensions):
- Base64 dla załączników
- Quoted-printable dla tekstów
- Multipart dla różnych części
```

### Web APIs
```
REST API:
- JSON jako format wymiany
- UTF-8 encoding
- Optional gzip compression

GraphQL:
- JSON request/response
- Schema-based
```

### Streaming Protocols
```
HLS (HTTP Live Streaming):
- H.264/H.265 video codec
- AAC audio codec
- Segmentacja na chunki

DASH:
- Adaptive bitrate
- Multiple codecs
```

## 🔗 Powiązane Tematy

- [[warstwa_sesji|Warstwa Sesji]]
- [[warstwa_aplikacji|Warstwa Aplikacji]]
- [[model_osi_overview|Model OSI]]
- [[protokol_http_https|HTTP/HTTPS]]
- [[bezpieczenstwo_sieci|Bezpieczeństwo Sieci]]
- [[SIECI KOMPUTEROWE]]

---

#warstwa-prezentacji #presentation-layer #szyfrowanie #kompresja #kodowanie #ssl-tls #osi-layer6
