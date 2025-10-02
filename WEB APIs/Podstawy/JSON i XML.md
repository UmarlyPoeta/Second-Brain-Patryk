# 📄 JSON i XML - Formaty Danych

## 🔍 Porównanie JSON vs XML

### JSON (JavaScript Object Notation)

**Definicja:** Lekki format wymiany danych, łatwy do czytania dla ludzi i maszyn.

```json
{
  "user": {
    "id": 123,
    "name": "Jan Kowalski",
    "email": "jan@example.com",
    "active": true,
    "roles": ["user", "admin"],
    "address": {
      "city": "Warszawa",
      "country": "Polska"
    }
  }
}
```

**Zalety:**
```
✅ Prostota i czytelność
✅ Mniejszy rozmiar
✅ Szybsze parsowanie
✅ Natywne wsparcie w JavaScript
✅ Lepsze dla REST API
✅ Łatwa serializacja/deserializacja
```

**Wady:**
```
❌ Brak walidacji schematu (choć istnieje JSON Schema)
❌ Brak komentarzy
❌ Ograniczone typy danych
❌ Brak przestrzeni nazw
```

### XML (eXtensible Markup Language)

**Definicja:** Rozszerzalny język znaczników do reprezentacji danych strukturalnych.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<user>
    <id>123</id>
    <name>Jan Kowalski</name>
    <email>jan@example.com</email>
    <active>true</active>
    <roles>
        <role>user</role>
        <role>admin</role>
    </roles>
    <address>
        <city>Warszawa</city>
        <country>Polska</country>
    </address>
</user>
```

**Zalety:**
```
✅ Silna walidacja (XSD, DTD)
✅ Przestrzenie nazw (namespaces)
✅ Wsparcie dla metadanych (atrybuty)
✅ XSLT dla transformacji
✅ Komentarze w dokumencie
✅ Lepsze dla dokumentów
```

**Wady:**
```
❌ Większy rozmiar
❌ Wolniejsze parsowanie
❌ Bardziej skomplikowany
❌ Więcej boilerplate
```

## 📊 JSON - Szczegóły

### Typy Danych JSON
```json
{
  "string": "tekst",
  "number": 123,
  "float": 123.45,
  "boolean": true,
  "null": null,
  "array": [1, 2, 3],
  "object": {"key": "value"}
}
```

### Zagnieżdżanie Struktur
```json
{
  "company": {
    "name": "Tech Corp",
    "employees": [
      {
        "id": 1,
        "name": "Jan",
        "department": {
          "id": 10,
          "name": "IT"
        },
        "projects": [
          {"id": 101, "name": "Project A"},
          {"id": 102, "name": "Project B"}
        ]
      }
    ]
  }
}
```

### JSON Schema (Walidacja)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 2,
      "maxLength": 50
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 120
    }
  },
  "required": ["name", "email"]
}
```

### Serializacja/Deserializacja JSON

**JavaScript:**
```javascript
// Obiekt → JSON (serializacja)
const user = {name: "Jan", age: 30};
const json = JSON.stringify(user);
// '{"name":"Jan","age":30}'

// JSON → Obiekt (deserializacja)
const parsed = JSON.parse(json);
// {name: "Jan", age: 30}

// Pretty print
JSON.stringify(user, null, 2);
```

**Java:**
```java
// Jackson
ObjectMapper mapper = new ObjectMapper();

// Obiekt → JSON
String json = mapper.writeValueAsString(user);

// JSON → Obiekt
User user = mapper.readValue(json, User.class);

// Pretty print
String prettyJson = mapper.writerWithDefaultPrettyPrinter()
                         .writeValueAsString(user);
```

**Python:**
```python
import json

# Obiekt → JSON
user = {"name": "Jan", "age": 30}
json_str = json.dumps(user)

# JSON → Obiekt
user = json.loads(json_str)

# Pretty print
print(json.dumps(user, indent=2))
```

## 🔧 XML - Szczegóły

### Struktura XML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Komentarz -->
<catalog xmlns:book="http://example.com/books">
    <book:item id="1" category="tech">
        <title lang="pl">REST API Guide</title>
        <author>Jan Kowalski</author>
        <price currency="PLN">99.99</price>
        <tags>
            <tag>API</tag>
            <tag>REST</tag>
        </tags>
    </book:item>
</catalog>
```

### Atrybuty vs Elementy
```xml
<!-- Atrybuty - dla metadanych -->
<user id="123" type="admin">
    <!-- Elementy - dla danych -->
    <name>Jan Kowalski</name>
    <email>jan@example.com</email>
</user>

<!-- Równoważne z samymi elementami -->
<user>
    <id>123</id>
    <type>admin</type>
    <name>Jan Kowalski</name>
    <email>jan@example.com</email>
</user>
```

### XML Schema (XSD)
```xml
<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="user">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="name" type="xs:string"/>
                <xs:element name="email" type="xs:string"/>
                <xs:element name="age" type="xs:integer" 
                           minOccurs="0"/>
            </xs:sequence>
            <xs:attribute name="id" type="xs:integer" 
                         use="required"/>
        </xs:complexType>
    </xs:element>
</xs:schema>
```

### Parsowanie XML

**Java (DOM):**
```java
DocumentBuilderFactory factory = 
    DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new File("data.xml"));

NodeList users = doc.getElementsByTagName("user");
Element user = (Element) users.item(0);
String name = user.getElementsByTagName("name")
                 .item(0).getTextContent();
```

**Python:**
```python
import xml.etree.ElementTree as ET

tree = ET.parse('data.xml')
root = tree.getroot()

for user in root.findall('user'):
    name = user.find('name').text
    email = user.find('email').text
```

## 🔄 Konwersja JSON ↔ XML

### JSON → XML
```json
{"user": {"name": "Jan", "age": 30}}
```
↓
```xml
<user>
    <name>Jan</name>
    <age>30</age>
</user>
```

### Wyzwania Konwersji
```
• Tablice w JSON vs XML
• Atrybuty XML → JSON
• Typy danych (JSON ma typy, XML wszystko to string)
• Przestrzenie nazw XML
```

## 🌐 Użycie w HTTP API

### Content Negotiation
```http
# Request z preferencją JSON
GET /api/users/123 HTTP/1.1
Accept: application/json

# Response JSON
HTTP/1.1 200 OK
Content-Type: application/json

{"id": 123, "name": "Jan"}
```

```http
# Request z preferencją XML
GET /api/users/123 HTTP/1.1
Accept: application/xml

# Response XML
HTTP/1.1 200 OK
Content-Type: application/xml

<user><id>123</id><name>Jan</name></user>
```

### MIME Types
```
JSON:
- application/json (standard)
- application/vnd.api+json (JSON API)
- application/hal+json (HAL)

XML:
- application/xml
- text/xml
- application/rss+xml (RSS feeds)
- application/soap+xml (SOAP)
```

## 📈 Statystyki Użycia

```
REST APIs:
├── JSON: ~95%
├── XML: ~3%
└── Inne: ~2%

SOAP APIs:
└── XML: 100%

Config Files:
├── JSON: ~40%
├── YAML: ~35%
├── XML: ~15%
└── Inne: ~10%
```

## 🎯 Kiedy Używać?

### Używaj JSON gdy:
```
✓ Tworzysz REST API
✓ Pracujesz z JavaScript/Node.js
✓ Potrzebujesz wydajności
✓ Dane są proste
✓ Mobile/Web aplikacje
```

### Używaj XML gdy:
```
✓ Potrzebujesz silnej walidacji
✓ Pracujesz z SOAP
✓ Potrzebujesz przestrzeni nazw
✓ Złożone dokumenty (np. DocBook)
✓ Legacy systems
✓ Transformacje XSLT
```

## 💡 Best Practices

### JSON
```javascript
// ✅ DOBRZE - camelCase dla kluczy
{
  "firstName": "Jan",
  "lastName": "Kowalski"
}

// ❌ ŹLE - snake_case (chyba że backend wymaga)
{
  "first_name": "Jan",
  "last_name": "Kowalski"
}

// ✅ DOBRZE - spójne nazewnictwo
{
  "users": [
    {"id": 1, "name": "Jan"},
    {"id": 2, "name": "Anna"}
  ]
}

// ❌ ŹLE - inconsistent naming
{
  "users": [
    {"userId": 1, "userName": "Jan"},
    {"id": 2, "name": "Anna"}
  ]
}
```

### XML
```xml
<!-- ✅ DOBRZE - czytelna struktura -->
<users>
    <user id="1">
        <name>Jan</name>
        <email>jan@example.com</email>
    </user>
</users>

<!-- ❌ ŹLE - wszystko w atrybutach -->
<users>
    <user id="1" name="Jan" email="jan@example.com"/>
</users>
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[HTTP Metody i Kody Statusu|📮 HTTP Metody]]
- [[OpenAPI i Swagger|📋 OpenAPI]]
- [[warstwa_prezentacji|6️⃣ Warstwa Prezentacji]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~10 minut*

#json #xml #data-formats #serialization #api
