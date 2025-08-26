# 🚀 Java - Koncepcje Zaawansowane

## 🔧 Generyki (Generics)

### 📝 Podstawy Generików

```java
// Klasa generyczna
public class Kontener<T> {
    private T wartosc;
    
    public Kontener(T wartosc) {
        this.wartosc = wartosc;
    }
    
    public T getWartosc() {
        return wartosc;
    }
    
    public void setWartosc(T wartosc) {
        this.wartosc = wartosc;
    }
}

// Użycie
Kontener<String> tekstKontener = new Kontener<>("Hello World");
Kontener<Integer> liczbaKontener = new Kontener<>(42);
```

### 🎯 Bounded Type Parameters

```java
// Ograniczenie do Number i jego podklas
public class StatystykaLiczb<T extends Number> {
    private List<T> lista;
    
    public StatystykaLiczb() {
        this.lista = new ArrayList<>();
    }
    
    public void dodaj(T liczba) {
        lista.add(liczba);
    }
    
    public double srednia() {
        return lista.stream()
                   .mapToDouble(Number::doubleValue)
                   .average()
                   .orElse(0.0);
    }
}
```

### 🔄 Wildcards

```java
// Wildcard z upper bound
public void wyswietlListe(List<? extends Number> lista) {
    for (Number n : lista) {
        System.out.println(n);
    }
}

// Wildcard z lower bound
public void dodajLiczby(List<? super Integer> lista) {
    lista.add(1);
    lista.add(2);
    lista.add(3);
}
```

## 🌊 Stream API (Java 8+)

### 💧 Podstawowe Operacje

```java
import java.util.stream.Collectors;

List<String> imiona = Arrays.asList("Anna", "Bartek", "Ania", "Michał", "Aleksandra");

// Filter, Map, Collect
List<String> dlugie = imiona.stream()
    .filter(imie -> imie.length() > 4)
    .map(String::toUpperCase)
    .collect(Collectors.toList());
// Wynik: [BARTEK, MICHAŁ, ALEKSANDRA]

// Sortowanie
List<String> posortowane = imiona.stream()
    .sorted()
    .collect(Collectors.toList());

// Find first
Optional<String> pierwsze = imiona.stream()
    .filter(imie -> imie.startsWith("A"))
    .findFirst();
```

### 📊 Zaawansowane Stream Operations

```java
// Parallel stream dla wydajności
long liczbaLong = imiona.parallelStream()
    .filter(imie -> imie.length() > 3)
    .count();

// Reduction
int suma = Arrays.asList(1, 2, 3, 4, 5).stream()
    .reduce(0, Integer::sum);

// Grouping
Map<Integer, List<String>> poGrupach = imiona.stream()
    .collect(Collectors.groupingBy(String::length));

// Partitioning
Map<Boolean, List<String>> podzielone = imiona.stream()
    .collect(Collectors.partitioningBy(imie -> imie.length() > 4));
```

### 🔗 Collectors

```java
// Zbieranie do różnych kolekcji
Set<String> zbiorImion = imiona.stream()
    .collect(Collectors.toSet());

// Joining strings
String polaczone = imiona.stream()
    .collect(Collectors.joining(", ", "[", "]"));

// Statystyki
IntSummaryStatistics statystyki = imiona.stream()
    .mapToInt(String::length)
    .summaryStatistics();

System.out.println("Średnia długość: " + statystyki.getAverage());
```

## ⚡ Lambda Expressions

### 🎯 Functional Interfaces

```java
// Predefined functional interfaces
Predicate<String> niePoste = tekst -> !tekst.isEmpty();
Function<String, Integer> dlugosc = String::length;
Consumer<String> wyswietl = System.out::println;
Supplier<String> losoweTekst = () -> "Random: " + Math.random();

// Użycie
List<String> teksty = Arrays.asList("Java", "", "Spring", "Boot");
teksty.stream()
     .filter(niePoste)
     .map(dlugosc)
     .forEach(wyswietl);
```

### 🔧 Własne Functional Interface

```java
@FunctionalInterface
public interface Kalkulator {
    int oblicz(int a, int b);
}

// Użycie z lambda
Kalkulator dodawanie = (a, b) -> a + b;
Kalkulator mnozenie = (a, b) -> a * b;

int wynik1 = dodawanie.oblicz(5, 3); // 8
int wynik2 = mnozenie.oblicz(5, 3);  // 15
```

## 📅 Optional (Java 8+)

### 🛡️ Bezpieczne Obsługiwanie Null

```java
// Tworzenie Optional
Optional<String> pusty = Optional.empty();
Optional<String> wartosc = Optional.of("Java");
Optional<String> mozeNull = Optional.ofNullable(getString()); // może być null

// Sprawdzanie obecności
if (wartosc.isPresent()) {
    System.out.println(wartosc.get());
}

// Bezpieczniejsze podejście
wartosc.ifPresent(System.out::println);

// Wartość domyślna
String wynik = mozeNull.orElse("Domyślny tekst");
String wynik2 = mozeNull.orElseGet(() -> "Wygenerowany tekst");

// Przekształcenia
Optional<Integer> dlugosc = wartosc
    .map(String::length)
    .filter(len -> len > 3);
```

## 🏭 Method References

```java
List<String> lista = Arrays.asList("java", "spring", "boot");

// Static method reference
lista.sort(String::compareToIgnoreCase);

// Instance method reference
lista.forEach(System.out::println);

// Constructor reference
Function<String, StringBuilder> konstruktor = StringBuilder::new;
StringBuilder sb = konstruktor.apply("Hello");

// Method reference na instancji
String prefix = "Prefix: ";
Function<String, String> dodajPrefix = prefix::concat;
```

## 🕐 Date/Time API (Java 8+)

```java
import java.time.*;
import java.time.format.DateTimeFormatter;

// Obecny czas
LocalDate dzisiaj = LocalDate.now();
LocalTime teraz = LocalTime.now();
LocalDateTime terazPelny = LocalDateTime.now();

// Tworzenie konkretnej daty
LocalDate konkretnaData = LocalDate.of(2024, 12, 25);
LocalTime konkretnyczas = LocalTime.of(14, 30, 0);

// Formatowanie
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");
String sformatowana = terazPelny.format(formatter);

// Operacje na datach
LocalDate jutro = dzisiaj.plusDays(1);
LocalDate tygodienTemu = dzisiaj.minusWeeks(1);
LocalDate pierwszyDzienMiesiaca = dzisiaj.withDayOfMonth(1);

// Period i Duration
Period okres = Period.between(LocalDate.of(2020, 1, 1), dzisiaj);
Duration czas = Duration.between(LocalTime.of(9, 0), teraz);
```

---

## 🔗 Następny Krok
[[Spring Boot Wprowadzenie|🌱 Spring Boot - Wprowadzenie]] - framework do budowania aplikacji Java

---
*Czas nauki: ~15 minut łącznie z podstawami*