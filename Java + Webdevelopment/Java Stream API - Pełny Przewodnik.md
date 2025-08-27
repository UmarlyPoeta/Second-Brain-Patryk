# 🌊 Java - Stream API - Pełny Przewodnik

## 📚 Wprowadzenie
Stream API zostało wprowadzone w Java 8 i rewolucjonizowało sposób przetwarzania kolekcji w Javie. Streamy umożliwiają deklaratywne programowanie funkcjonalne, czytelne transformacje danych i efektywne przetwarzanie zarówno sekwencyjne jak i równoległe.

## 🔄 Podstawowe Koncepcje

### Czym jest Stream?
```java
import java.util.*;
import java.util.stream.*;

public class StreamBasics {
    
    public static void demonstrateStreamConcept() {
        List<String> names = Arrays.asList("Anna", "Bartosz", "Cecylia", "Dawid", "Ewa");
        
        // Tradycyjne podejście (imperatywne)
        List<String> longNamesTraditional = new ArrayList<>();
        for (String name : names) {
            if (name.length() > 4) {
                longNamesTraditional.add(name.toUpperCase());
            }
        }
        Collections.sort(longNamesTraditional);
        
        System.out.println("Tradycyjnie: " + longNamesTraditional);
        
        // Stream API (deklaratywne)
        List<String> longNamesStream = names.stream()
            .filter(name -> name.length() > 4)    // Intermediate operation
            .map(String::toUpperCase)             // Intermediate operation
            .sorted()                             // Intermediate operation
            .collect(Collectors.toList());        // Terminal operation
            
        System.out.println("Stream API: " + longNamesStream);
    }
    
    // Charakterystyki Stream
    public static void streamCharacteristics() {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        
        // 1. Stream nie modyfikuje źródła danych
        List<Integer> doubled = numbers.stream()
            .map(n -> n * 2)
            .collect(Collectors.toList());
        
        System.out.println("Oryginalne: " + numbers);    // [1, 2, 3, 4, 5]
        System.out.println("Podwojone: " + doubled);      // [2, 4, 6, 8, 10]
        
        // 2. Lazy evaluation - operacje intermediate są wykonywane dopiero przy terminal operation
        Stream<Integer> lazyStream = numbers.stream()
            .map(n -> {
                System.out.println("Mapowanie: " + n);
                return n * 2;
            });
        
        System.out.println("Stream utworzony, ale mapowanie jeszcze nie wykonane");
        
        // Dopiero teraz mapowanie się wykona
        List<Integer> result = lazyStream.collect(Collectors.toList());
        
        // 3. Stream można użyć tylko raz
        Stream<Integer> stream = numbers.stream();
        stream.count(); // Pierwsze użycie - OK
        // stream.count(); // Drugie użycie - IllegalStateException!
    }
}
```

## 🏗️ Tworzenie Streamów

```java
public class StreamCreation {
    
    public static void demonstrateCreationMethods() {
        // 1. Z kolekcji
        List<String> list = Arrays.asList("a", "b", "c");
        Stream<String> streamFromList = list.stream();
        
        // 2. Z tablicy
        String[] array = {"x", "y", "z"};
        Stream<String> streamFromArray = Arrays.stream(array);
        
        // 3. Z wartości
        Stream<String> streamOfValues = Stream.of("jeden", "dwa", "trzy");
        
        // 4. Pusty stream
        Stream<String> emptyStream = Stream.empty();
        
        // 5. Stream nieskończony - iterate
        Stream<Integer> infiniteStream = Stream.iterate(0, n -> n + 2);
        List<Integer> first10Even = infiniteStream.limit(10).collect(Collectors.toList());
        System.out.println("Pierwsze 10 liczb parzystych: " + first10Even);
        
        // 6. Stream nieskończony - generate
        Stream<String> randomStrings = Stream.generate(() -> "random_" + Math.random());
        List<String> first5Random = randomStrings.limit(5).collect(Collectors.toList());
        System.out.println("5 losowych stringów: " + first5Random);
        
        // 7. IntStream, LongStream, DoubleStream
        IntStream intStream = IntStream.range(1, 11);  // 1 do 10
        IntStream intStreamClosed = IntStream.rangeClosed(1, 10); // 1 do 10 włącznie
        
        System.out.println("Suma 1-10: " + intStream.sum());
        System.out.println("Średnia 1-10: " + intStreamClosed.average().orElse(0));
        
        // 8. Random streams
        Random random = new Random();
        DoubleStream randomDoubles = random.doubles(5, 0.0, 1.0);
        randomDoubles.forEach(System.out::println);
        
        // 9. Stream z Regex
        Stream<String> wordsFromString = "To jest przykład tekstu"
            .chars()
            .mapToObj(c -> String.valueOf((char) c))
            .filter(c -> !c.equals(" "));
        System.out.println("Znaki bez spacji: " + 
            wordsFromString.collect(Collectors.joining()));
    }
    
    // Builder pattern dla Stream
    public static void streamBuilder() {
        Stream<String> streamBuilder = Stream.<String>builder()
            .add("a")
            .add("b")
            .add("c")
            .build();
            
        streamBuilder.forEach(System.out::println);
    }
}
```

## 🔄 Operacje Intermediate

```java
public class IntermediateOperations {
    
    public static void demonstrateFiltering() {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        
        // filter - filtrowanie elementów
        List<Integer> evenNumbers = numbers.stream()
            .filter(n -> n % 2 == 0)
            .collect(Collectors.toList());
        System.out.println("Liczby parzyste: " + evenNumbers);
        
        // distinct - usuwanie duplikatów
        List<String> words = Arrays.asList("apple", "banana", "apple", "cherry", "banana");
        List<String> uniqueWords = words.stream()
            .distinct()
            .collect(Collectors.toList());
        System.out.println("Unikalne słowa: " + uniqueWords);
        
        // limit - ograniczenie liczby elementów
        List<Integer> first5Numbers = numbers.stream()
            .limit(5)
            .collect(Collectors.toList());
        System.out.println("Pierwsze 5 liczb: " + first5Numbers);
        
        // skip - pominięcie pierwszych n elementów
        List<Integer> numbersAfterSkip = numbers.stream()
            .skip(3)
            .collect(Collectors.toList());
        System.out.println("Po pominięciu 3: " + numbersAfterSkip);
        
        // takeWhile (Java 9+) - bierz elementy dopóki warunek jest spełniony
        List<Integer> takeWhileExample = numbers.stream()
            .takeWhile(n -> n < 6)
            .collect(Collectors.toList());
        System.out.println("Take while < 6: " + takeWhileExample);
        
        // dropWhile (Java 9+) - pomiń elementy dopóki warunek jest spełniony
        List<Integer> dropWhileExample = numbers.stream()
            .dropWhile(n -> n < 6)
            .collect(Collectors.toList());
        System.out.println("Drop while < 6: " + dropWhileExample);
    }
    
    public static void demonstrateMapping() {
        List<String> words = Arrays.asList("hello", "world", "java", "stream");
        
        // map - transformacja 1:1
        List<String> upperCaseWords = words.stream()
            .map(String::toUpperCase)
            .collect(Collectors.toList());
        System.out.println("Wielkie litery: " + upperCaseWords);
        
        List<Integer> wordLengths = words.stream()
            .map(String::length)
            .collect(Collectors.toList());
        System.out.println("Długości słów: " + wordLengths);
        
        // mapToInt, mapToLong, mapToDouble - specjalizowane mapowanie
        IntStream lengths = words.stream().mapToInt(String::length);
        System.out.println("Średnia długość słowa: " + lengths.average().orElse(0));
        
        // flatMap - spłaszczanie nested structures
        List<List<String>> nestedLists = Arrays.asList(
            Arrays.asList("a", "b"),
            Arrays.asList("c", "d"),
            Arrays.asList("e", "f")
        );
        
        List<String> flattenedList = nestedLists.stream()
            .flatMap(Collection::stream)
            .collect(Collectors.toList());
        System.out.println("Spłaszczona lista: " + flattenedList);
        
        // flatMap z mapowaniem
        List<String> sentences = Arrays.asList("Hello world", "Java streams", "Are awesome");
        List<String> allWords = sentences.stream()
            .flatMap(sentence -> Arrays.stream(sentence.split(" ")))
            .collect(Collectors.toList());
        System.out.println("Wszystkie słowa: " + allWords);
    }
    
    public static void demonstrateSorting() {
        List<String> names = Arrays.asList("Anna", "Bartosz", "Cecylia", "adam", "barbara");
        
        // sorted() - sortowanie naturalne
        List<String> sortedNames = names.stream()
            .sorted()
            .collect(Collectors.toList());
        System.out.println("Posortowane naturalnie: " + sortedNames);
        
        // sorted(Comparator) - sortowanie z comparatorem
        List<String> sortedByLength = names.stream()
            .sorted(Comparator.comparing(String::length))
            .collect(Collectors.toList());
        System.out.println("Posortowane po długości: " + sortedByLength);
        
        // Złożone sortowanie
        List<String> complexSort = names.stream()
            .sorted(Comparator
                .comparing(String::length)
                .thenComparing(String.CASE_INSENSITIVE_ORDER))
            .collect(Collectors.toList());
        System.out.println("Sortowanie złożone: " + complexSort);
        
        // Sortowanie odwrotne
        List<String> reversedSort = names.stream()
            .sorted(Collections.reverseOrder())
            .collect(Collectors.toList());
        System.out.println("Sortowanie odwrotne: " + reversedSort);
    }
    
    public static void demonstratePeeking() {
        List<String> words = Arrays.asList("apple", "banana", "cherry");
        
        // peek - wykonanie akcji bez zmiany strumienia (do debugowania)
        List<String> result = words.stream()
            .peek(word -> System.out.println("Przetwarzanie: " + word))
            .map(String::toUpperCase)
            .peek(word -> System.out.println("Po mapowaniu: " + word))
            .filter(word -> word.length() > 5)
            .peek(word -> System.out.println("Po filtrowaniu: " + word))
            .collect(Collectors.toList());
            
        System.out.println("Końcowy wynik: " + result);
    }
}
```

## 🎯 Operacje Terminal

```java
public class TerminalOperations {
    
    public static void demonstrateCollecting() {
        List<String> names = Arrays.asList("Anna", "Bartosz", "Cecylia", "Dawid", "Ewa");
        
        // collect(Collectors.toList())
        List<String> namesList = names.stream()
            .filter(name -> name.length() > 4)
            .collect(Collectors.toList());
            
        // collect(Collectors.toSet())
        Set<String> namesSet = names.stream()
            .collect(Collectors.toSet());
            
        // collect(Collectors.toCollection())
        LinkedHashSet<String> linkedSet = names.stream()
            .collect(Collectors.toCollection(LinkedHashSet::new));
            
        // collect(Collectors.toMap())
        Map<String, Integer> nameToLength = names.stream()
            .collect(Collectors.toMap(
                name -> name,           // key
                String::length          // value
            ));
        System.out.println("Imiona i długości: " + nameToLength);
        
        // collect(Collectors.joining())
        String joinedNames = names.stream()
            .collect(Collectors.joining(", ", "[", "]"));
        System.out.println("Połączone imiona: " + joinedNames);
    }
    
    public static void demonstrateReductions() {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        
        // reduce - redukcja do pojedynczej wartości
        Optional<Integer> sum = numbers.stream()
            .reduce((a, b) -> a + b);
        System.out.println("Suma (reduce): " + sum.orElse(0));
        
        // reduce z identity value
        Integer sumWithIdentity = numbers.stream()
            .reduce(0, (a, b) -> a + b);
        System.out.println("Suma z identity: " + sumWithIdentity);
        
        // reduce z combiner (dla parallel streams)
        Integer sumParallel = numbers.parallelStream()
            .reduce(0, 
                Integer::sum,           // accumulator
                Integer::sum            // combiner
            );
        System.out.println("Suma parallel: " + sumParallel);
        
        // Znajdz maksimum
        Optional<Integer> max = numbers.stream()
            .reduce(Integer::max);
        System.out.println("Maksimum: " + max.orElse(0));
        
        // String reduction
        List<String> words = Arrays.asList("Java", "is", "awesome");
        String concatenated = words.stream()
            .reduce("", (a, b) -> a + " " + b);
        System.out.println("Połączone słowa: " + concatenated.trim());
    }
    
    public static void demonstrateMatching() {
        List<Integer> numbers = Arrays.asList(2, 4, 6, 8, 10);
        List<Integer> mixedNumbers = Arrays.asList(1, 2, 3, 4, 5);
        
        // allMatch - czy wszystkie elementy spełniają warunek
        boolean allEven = numbers.stream()
            .allMatch(n -> n % 2 == 0);
        System.out.println("Wszystkie parzyste: " + allEven); // true
        
        // anyMatch - czy jakikolwiek element spełnia warunek
        boolean anyEven = mixedNumbers.stream()
            .anyMatch(n -> n % 2 == 0);
        System.out.println("Jakikolwiek parzysty: " + anyEven); // true
        
        // noneMatch - czy żaden element nie spełnia warunku
        boolean noneNegative = numbers.stream()
            .noneMatch(n -> n < 0);
        System.out.println("Żaden ujemny: " + noneNegative); // true
    }
    
    public static void demonstrateFindingAndCounting() {
        List<String> names = Arrays.asList("Anna", "Bartosz", "Cecylia", "Adam", "Barbara");
        
        // findFirst - znajdź pierwszy element
        Optional<String> firstLongName = names.stream()
            .filter(name -> name.length() > 5)
            .findFirst();
        System.out.println("Pierwsze długie imię: " + firstLongName.orElse("Brak"));
        
        // findAny - znajdź jakikolwiek element (przydatne w parallel streams)
        Optional<String> anyLongName = names.parallelStream()
            .filter(name -> name.length() > 5)
            .findAny();
        System.out.println("Jakiekolwiek długie imię: " + anyLongName.orElse("Brak"));
        
        // count - policz elementy
        long longNamesCount = names.stream()
            .filter(name -> name.length() > 5)
            .count();
        System.out.println("Liczba długich imion: " + longNamesCount);
    }
    
    public static void demonstrateForEach() {
        List<String> words = Arrays.asList("apple", "banana", "cherry");
        
        // forEach - wykonaj akcję dla każdego elementu
        System.out.println("For each:");
        words.stream()
            .map(String::toUpperCase)
            .forEach(System.out::println);
        
        // forEachOrdered - zachowaj kolejność (ważne w parallel streams)
        System.out.println("For each ordered (parallel):");
        words.parallelStream()
            .map(String::toUpperCase)
            .forEachOrdered(System.out::println);
    }
}
```

## 📊 Specjalne Operacje Collector

```java
public class AdvancedCollectors {
    
    static class Person {
        String name;
        int age;
        String city;
        double salary;
        
        Person(String name, int age, String city, double salary) {
            this.name = name;
            this.age = age;
            this.city = city;
            this.salary = salary;
        }
        
        // Getters
        public String getName() { return name; }
        public int getAge() { return age; }
        public String getCity() { return city; }
        public double getSalary() { return salary; }
        
        @Override
        public String toString() {
            return String.format("Person{name='%s', age=%d, city='%s', salary=%.2f}",
                               name, age, city, salary);
        }
    }
    
    public static void demonstrateGrouping() {
        List<Person> people = Arrays.asList(
            new Person("Anna", 25, "Warszawa", 5000),
            new Person("Bartosz", 30, "Kraków", 6000),
            new Person("Cecylia", 28, "Warszawa", 5500),
            new Person("Dawid", 35, "Gdańsk", 7000),
            new Person("Ewa", 27, "Kraków", 5800)
        );
        
        // groupingBy - grupowanie po kluczu
        Map<String, List<Person>> peopleByCity = people.stream()
            .collect(Collectors.groupingBy(Person::getCity));
        
        System.out.println("Grupowanie po mieście:");
        peopleByCity.forEach((city, persons) -> {
            System.out.println(city + ": " + persons.size() + " osób");
        });
        
        // groupingBy z downstream collector
        Map<String, Double> avgSalaryByCity = people.stream()
            .collect(Collectors.groupingBy(
                Person::getCity,
                Collectors.averagingDouble(Person::getSalary)
            ));
        
        System.out.println("Średnia pensja po mieście: " + avgSalaryByCity);
        
        // groupingBy z counting
        Map<String, Long> countByCity = people.stream()
            .collect(Collectors.groupingBy(
                Person::getCity,
                Collectors.counting()
            ));
        
        System.out.println("Liczba osób po mieście: " + countByCity);
        
        // Wielopoziomowe grupowanie
        Map<String, Map<String, List<Person>>> groupedByCityAndAgeRange = people.stream()
            .collect(Collectors.groupingBy(
                Person::getCity,
                Collectors.groupingBy(person -> 
                    person.getAge() < 30 ? "Młodzi" : "Starsi"
                )
            ));
        
        System.out.println("Grupowanie po mieście i wieku:");
        groupedByCityAndAgeRange.forEach((city, ageGroups) -> {
            System.out.println(city + ":");
            ageGroups.forEach((ageGroup, persons) -> {
                System.out.println("  " + ageGroup + ": " + persons.size());
            });
        });
    }
    
    public static void demonstratePartitioning() {
        List<Person> people = Arrays.asList(
            new Person("Anna", 25, "Warszawa", 5000),
            new Person("Bartosz", 30, "Kraków", 6000),
            new Person("Cecylia", 28, "Warszawa", 5500),
            new Person("Dawid", 35, "Gdańsk", 7000),
            new Person("Ewa", 27, "Kraków", 5800)
        );
        
        // partitioningBy - podział na dwie grupy (true/false)
        Map<Boolean, List<Person>> partitionedByAge = people.stream()
            .collect(Collectors.partitioningBy(person -> person.getAge() >= 30));
        
        System.out.println("Młodzi (< 30): " + partitionedByAge.get(false).size());
        System.out.println("Starsi (>= 30): " + partitionedByAge.get(true).size());
        
        // partitioningBy z downstream collector
        Map<Boolean, Double> avgSalaryByAgeGroup = people.stream()
            .collect(Collectors.partitioningBy(
                person -> person.getAge() >= 30,
                Collectors.averagingDouble(Person::getSalary)
            ));
        
        System.out.println("Średnia pensja młodych: " + avgSalaryByAgeGroup.get(false));
        System.out.println("Średnia pensja starszych: " + avgSalaryByAgeGroup.get(true));
    }
    
    public static void demonstrateStatistics() {
        List<Person> people = Arrays.asList(
            new Person("Anna", 25, "Warszawa", 5000),
            new Person("Bartosz", 30, "Kraków", 6000),
            new Person("Cecylia", 28, "Warszawa", 5500),
            new Person("Dawid", 35, "Gdańsk", 7000),
            new Person("Ewa", 27, "Kraków", 5800)
        );
        
        // Statystyki opisowe
        DoubleSummaryStatistics salaryStats = people.stream()
            .collect(Collectors.summarizingDouble(Person::getSalary));
        
        System.out.println("Statystyki pensji:");
        System.out.println("  Liczba: " + salaryStats.getCount());
        System.out.println("  Suma: " + salaryStats.getSum());
        System.out.println("  Średnia: " + salaryStats.getAverage());
        System.out.println("  Minimum: " + salaryStats.getMin());
        System.out.println("  Maksimum: " + salaryStats.getMax());
        
        // Statystyki wieku
        IntSummaryStatistics ageStats = people.stream()
            .collect(Collectors.summarizingInt(Person::getAge));
        
        System.out.println("Statystyki wieku:");
        System.out.println("  Średnia: " + ageStats.getAverage());
        System.out.println("  Zakres: " + ageStats.getMin() + " - " + ageStats.getMax());
    }
    
    public static void demonstrateCustomCollectors() {
        List<String> words = Arrays.asList("apple", "banana", "cherry", "date");
        
        // mapping collector
        Set<Integer> wordLengths = words.stream()
            .collect(Collectors.mapping(
                String::length,
                Collectors.toSet()
            ));
        System.out.println("Długości słów: " + wordLengths);
        
        // filtering collector (Java 9+)
        List<String> longWords = words.stream()
            .collect(Collectors.filtering(
                word -> word.length() > 5,
                Collectors.toList()
            ));
        System.out.println("Długie słowa: " + longWords);
        
        // flatMapping collector (Java 9+)
        List<Character> allCharacters = words.stream()
            .collect(Collectors.flatMapping(
                word -> word.chars().mapToObj(c -> (char) c),
                Collectors.toList()
            ));
        System.out.println("Wszystkie znaki: " + allCharacters);
        
        // teeing collector (Java 12+) - łączenie dwóch collectors
        String wordStats = words.stream()
            .collect(Collectors.teeing(
                Collectors.counting(),
                Collectors.averagingInt(String::length),
                (count, avgLength) -> String.format("Słów: %d, Średnia długość: %.1f", count, avgLength)
            ));
        System.out.println("Statystyki słów: " + wordStats);
    }
}
```

## ⚡ Parallel Streams

```java
public class ParallelStreams {
    
    public static void demonstrateParallelProcessing() {
        List<Integer> largeList = IntStream.range(0, 10_000_000)
            .boxed()
            .collect(Collectors.toList());
        
        // Sequential stream
        long startTime = System.currentTimeMillis();
        long sumSequential = largeList.stream()
            .filter(n -> n % 2 == 0)
            .mapToLong(n -> n * n)
            .sum();
        long sequentialTime = System.currentTimeMillis() - startTime;
        
        // Parallel stream
        startTime = System.currentTimeMillis();
        long sumParallel = largeList.parallelStream()
            .filter(n -> n % 2 == 0)
            .mapToLong(n -> n * n)
            .sum();
        long parallelTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Suma sequential: " + sumSequential + " czas: " + sequentialTime + "ms");
        System.out.println("Suma parallel: " + sumParallel + " czas: " + parallelTime + "ms");
        System.out.println("Przyspieszenie: " + (double) sequentialTime / parallelTime + "x");
    }
    
    public static void parallelStreamPitfalls() {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        
        // Problem 1: Shared mutable state
        List<Integer> results = new ArrayList<>(); // Not thread-safe!
        
        // NIEPOPRAWNE - może prowadzić do race conditions
        // numbers.parallelStream().forEach(n -> results.add(n * 2));
        
        // POPRAWNE - używaj collectors
        List<Integer> correctResults = numbers.parallelStream()
            .map(n -> n * 2)
            .collect(Collectors.toList());
        
        // Problem 2: Kolejność wykonania
        System.out.println("Sequential forEach:");
        numbers.stream().forEach(System.out::print);
        System.out.println();
        
        System.out.println("Parallel forEach (kolejność może być inna):");
        numbers.parallelStream().forEach(System.out::print);
        System.out.println();
        
        System.out.println("Parallel forEachOrdered (zachowuje kolejność):");
        numbers.parallelStream().forEachOrdered(System.out::print);
        System.out.println();
    }
    
    public static void whenToUseParallel() {
        System.out.println("Kiedy używać parallel streams:");
        System.out.println("✅ Duże zbiory danych (>10,000 elementów)");
        System.out.println("✅ Kosztowne operacje obliczeniowe");
        System.out.println("✅ Stateless operations");
        System.out.println("✅ Associative operations (dla reduce)");
        System.out.println();
        System.out.println("❌ Kiedy NIE używać:");
        System.out.println("❌ Małe zbiory danych");
        System.out.println("❌ I/O operations");
        System.out.println("❌ Shared mutable state");
        System.out.println("❌ Operations zależne od kolejności");
    }
    
    // Custom ForkJoinPool
    public static void customThreadPool() {
        List<Integer> numbers = IntStream.range(1, 1000)
            .boxed()
            .collect(Collectors.toList());
        
        // Domyślny pool (liczba procesorów)
        int defaultResult = numbers.parallelStream()
            .mapToInt(n -> heavyComputation(n))
            .sum();
        
        // Custom pool z większą liczbą wątków
        ForkJoinPool customThreadPool = new ForkJoinPool(32);
        try {
            Integer customResult = customThreadPool.submit(() ->
                numbers.parallelStream()
                    .mapToInt(n -> heavyComputation(n))
                    .sum()
            ).get();
            
            System.out.println("Default pool result: " + defaultResult);
            System.out.println("Custom pool result: " + customResult);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            customThreadPool.shutdown();
        }
    }
    
    private static int heavyComputation(int n) {
        // Symulacja kosztownej operacji
        return n * n + (int) (Math.random() * 100);
    }
}
```

## 🎯 Przykład Kompleksowy - System Analizy Danych

```java
import java.time.LocalDate;
import java.util.*;
import java.util.stream.*;

public class DataAnalysisSystem {
    
    static class Transaction {
        private String id;
        private String customerId;
        private String category;
        private double amount;
        private LocalDate date;
        private String region;
        
        public Transaction(String id, String customerId, String category, 
                         double amount, LocalDate date, String region) {
            this.id = id;
            this.customerId = customerId;
            this.category = category;
            this.amount = amount;
            this.date = date;
            this.region = region;
        }
        
        // Getters
        public String getId() { return id; }
        public String getCustomerId() { return customerId; }
        public String getCategory() { return category; }
        public double getAmount() { return amount; }
        public LocalDate getDate() { return date; }
        public String getRegion() { return region; }
        
        @Override
        public String toString() {
            return String.format("Transaction{id='%s', customer='%s', category='%s', amount=%.2f, date=%s, region='%s'}",
                               id, customerId, category, amount, date, region);
        }
    }
    
    static class Customer {
        private String id;
        private String name;
        private String tier; // GOLD, SILVER, BRONZE
        private int age;
        private String region;
        
        public Customer(String id, String name, String tier, int age, String region) {
            this.id = id;
            this.name = name;
            this.tier = tier;
            this.age = age;
            this.region = region;
        }
        
        // Getters
        public String getId() { return id; }
        public String getName() { return name; }
        public String getTier() { return tier; }
        public int getAge() { return age; }
        public String getRegion() { return region; }
        
        @Override
        public String toString() {
            return String.format("Customer{id='%s', name='%s', tier='%s', age=%d, region='%s'}",
                               id, name, tier, age, region);
        }
    }
    
    private List<Transaction> transactions;
    private List<Customer> customers;
    
    public DataAnalysisSystem() {
        generateSampleData();
    }
    
    private void generateSampleData() {
        // Generate customers
        customers = Arrays.asList(
            new Customer("C001", "Anna Kowalska", "GOLD", 35, "North"),
            new Customer("C002", "Piotr Nowak", "SILVER", 28, "South"),
            new Customer("C003", "Maria Wiśniewska", "BRONZE", 42, "North"),
            new Customer("C004", "Tomasz Kowalczyk", "GOLD", 31, "East"),
            new Customer("C005", "Agnieszka Wójcik", "SILVER", 26, "South"),
            new Customer("C006", "Krzysztof Kamiński", "BRONZE", 39, "West"),
            new Customer("C007", "Małgorzata Lewandowska", "GOLD", 33, "North"),
            new Customer("C008", "Paweł Dąbrowski", "SILVER", 29, "East")
        );
        
        // Generate transactions
        transactions = Arrays.asList(
            new Transaction("T001", "C001", "Electronics", 1200.00, LocalDate.of(2023, 1, 15), "North"),
            new Transaction("T002", "C002", "Clothing", 299.99, LocalDate.of(2023, 1, 20), "South"),
            new Transaction("T003", "C001", "Books", 89.50, LocalDate.of(2023, 2, 5), "North"),
            new Transaction("T004", "C003", "Electronics", 2500.00, LocalDate.of(2023, 2, 10), "North"),
            new Transaction("T005", "C004", "Food", 156.75, LocalDate.of(2023, 2, 15), "East"),
            new Transaction("T006", "C002", "Electronics", 899.99, LocalDate.of(2023, 3, 1), "South"),
            new Transaction("T007", "C005", "Clothing", 199.99, LocalDate.of(2023, 3, 8), "South"),
            new Transaction("T008", "C006", "Books", 45.00, LocalDate.of(2023, 3, 12), "West"),
            new Transaction("T009", "C007", "Electronics", 3200.00, LocalDate.of(2023, 3, 20), "North"),
            new Transaction("T010", "C008", "Food", 278.30, LocalDate.of(2023, 4, 2), "East"),
            new Transaction("T011", "C001", "Clothing", 450.00, LocalDate.of(2023, 4, 10), "North"),
            new Transaction("T012", "C003", "Food", 123.45, LocalDate.of(2023, 4, 15), "North")
        );
    }
    
    public void performComprehensiveAnalysis() {
        System.out.println("=== KOMPLEKSOWA ANALIZA DANYCH ===\n");
        
        // 1. Top customers by total spending
        Map<String, Double> customerSpending = transactions.stream()
            .collect(Collectors.groupingBy(
                Transaction::getCustomerId,
                Collectors.summingDouble(Transaction::getAmount)
            ));
        
        List<Map.Entry<String, Double>> topCustomers = customerSpending.entrySet().stream()
            .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
            .limit(3)
            .collect(Collectors.toList());
        
        System.out.println("TOP 3 KLIENTÓW WEDŁUG WYDATKÓW:");
        topCustomers.forEach(entry -> {
            String customerName = customers.stream()
                .filter(c -> c.getId().equals(entry.getKey()))
                .findFirst()
                .map(Customer::getName)
                .orElse("Unknown");
            System.out.printf("  %s: %.2f PLN%n", customerName, entry.getValue());
        });
        
        // 2. Average spending by customer tier
        Map<String, Double> avgSpendingByTier = transactions.stream()
            .collect(Collectors.groupingBy(
                transaction -> customers.stream()
                    .filter(c -> c.getId().equals(transaction.getCustomerId()))
                    .findFirst()
                    .map(Customer::getTier)
                    .orElse("UNKNOWN"),
                Collectors.averagingDouble(Transaction::getAmount)
            ));
        
        System.out.println("\nŚREDNIE WYDATKI WEDŁUG POZIOMU KLIENTA:");
        avgSpendingByTier.entrySet().stream()
            .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
            .forEach(entry -> 
                System.out.printf("  %s: %.2f PLN%n", entry.getKey(), entry.getValue()));
        
        // 3. Monthly sales trends
        Map<Integer, Double> monthlySales = transactions.stream()
            .collect(Collectors.groupingBy(
                transaction -> transaction.getDate().getMonthValue(),
                Collectors.summingDouble(Transaction::getAmount)
            ));
        
        System.out.println("\nTRENDY SPRZEDAŻY MIESIĘCZNEJ:");
        monthlySales.entrySet().stream()
            .sorted(Map.Entry.comparingByKey())
            .forEach(entry -> 
                System.out.printf("  Miesiąc %d: %.2f PLN%n", entry.getKey(), entry.getValue()));
        
        // 4. Category performance analysis
        Map<String, Map<String, Object>> categoryAnalysis = transactions.stream()
            .collect(Collectors.groupingBy(
                Transaction::getCategory,
                Collectors.teeing(
                    Collectors.counting(),
                    Collectors.summingDouble(Transaction::getAmount),
                    (count, sum) -> {
                        Map<String, Object> stats = new HashMap<>();
                        stats.put("count", count);
                        stats.put("total", sum);
                        stats.put("average", sum / count);
                        return stats;
                    }
                )
            ));
        
        System.out.println("\nANALIZA KATEGORII PRODUKTÓW:");
        categoryAnalysis.entrySet().stream()
            .sorted((e1, e2) -> Double.compare(
                (Double) e2.getValue().get("total"),
                (Double) e1.getValue().get("total")
            ))
            .forEach(entry -> {
                String category = entry.getKey();
                Map<String, Object> stats = entry.getValue();
                System.out.printf("  %s: %d transakcji, %.2f PLN total, %.2f PLN średnio%n",
                    category, 
                    (Long) stats.get("count"),
                    (Double) stats.get("total"),
                    (Double) stats.get("average"));
            });
        
        // 5. Regional analysis with customer demographics
        Map<String, Map<String, Object>> regionalAnalysis = transactions.stream()
            .collect(Collectors.groupingBy(
                Transaction::getRegion,
                Collectors.teeing(
                    Collectors.summingDouble(Transaction::getAmount),
                    Collectors.mapping(
                        Transaction::getCustomerId,
                        Collectors.collectingAndThen(
                            Collectors.toSet(),
                            customerIds -> {
                                return customers.stream()
                                    .filter(c -> customerIds.contains(c.getId()))
                                    .collect(Collectors.averagingInt(Customer::getAge));
                            }
                        )
                    ),
                    (totalSales, avgAge) -> {
                        Map<String, Object> stats = new HashMap<>();
                        stats.put("totalSales", totalSales);
                        stats.put("avgCustomerAge", avgAge);
                        return stats;
                    }
                )
            ));
        
        System.out.println("\nANALIZA REGIONALNA:");
        regionalAnalysis.forEach((region, stats) -> {
            System.out.printf("  %s: %.2f PLN sprzedaży, średni wiek klientów: %.1f lat%n",
                region, 
                (Double) stats.get("totalSales"),
                (Double) stats.get("avgCustomerAge"));
        });
        
        // 6. High-value transaction analysis
        List<Transaction> highValueTransactions = transactions.stream()
            .filter(t -> t.getAmount() > 1000)
            .sorted(Comparator.comparing(Transaction::getAmount).reversed())
            .collect(Collectors.toList());
        
        System.out.println("\nTRANSAKCJE WYSOKOWARTOŚCIOWE (>1000 PLN):");
        highValueTransactions.forEach(transaction -> {
            String customerName = customers.stream()
                .filter(c -> c.getId().equals(transaction.getCustomerId()))
                .findFirst()
                .map(Customer::getName)
                .orElse("Unknown");
            System.out.printf("  %.2f PLN - %s - %s - %s%n",
                transaction.getAmount(),
                customerName,
                transaction.getCategory(),
                transaction.getDate());
        });
        
        // 7. Customer loyalty analysis
        Map<String, Long> customerTransactionCount = transactions.stream()
            .collect(Collectors.groupingBy(
                Transaction::getCustomerId,
                Collectors.counting()
            ));
        
        Map<String, List<String>> loyaltySegments = customerTransactionCount.entrySet().stream()
            .collect(Collectors.groupingBy(
                entry -> {
                    long count = entry.getValue();
                    if (count >= 3) return "Highly Loyal";
                    else if (count >= 2) return "Moderately Loyal";
                    else return "New/Occasional";
                },
                Collectors.mapping(Map.Entry::getKey, Collectors.toList())
            ));
        
        System.out.println("\nANALIZA LOJALNOŚCI KLIENTÓW:");
        loyaltySegments.forEach((segment, customerIds) -> {
            System.out.printf("  %s: %d klientów%n", segment, customerIds.size());
            customerIds.stream()
                .map(id -> customers.stream()
                    .filter(c -> c.getId().equals(id))
                    .findFirst()
                    .map(Customer::getName)
                    .orElse("Unknown"))
                .forEach(name -> System.out.println("    - " + name));
        });
    }
    
    public static void main(String[] args) {
        DataAnalysisSystem system = new DataAnalysisSystem();
        system.performComprehensiveAnalysis();
    }
}
```

## 🔗 Powiązane Tematy
- [[Java Kolekcje - Szczegółowe Omówienie]] - Podstawa dla Stream API
- [[Java Lambda i Functional Programming]] - Lambda expressions w Stream
- [[Java Optional - Najlepsze Praktyki]] - Handling null values
- [[Java Wielowątkowość - Threading]] - Parallel streams

## 💡 Najlepsze Praktyki

1. **Preferuj Stream API nad pętle** dla operacji na kolekcjach
2. **Używaj method references** gdy to możliwe: `String::length` zamiast `s -> s.length()`
3. **Unikaj side effects** w intermediate operations
4. **Używaj Optional** zamiast null checks
5. **Rozważ parallel streams** tylko dla dużych zbiorów danych i kosztownych operacji
6. **Łącz operacje** w logiczne łańcuchy
7. **Używaj specific collectors** zamiast generic collect()

## ⚠️ Częste Błędy

1. **Reusing streams** - stream można użyć tylko raz
2. **Mutating source** podczas operacji stream
3. **Boxing/unboxing overhead** - używaj IntStream, LongStream, DoubleStream
4. **Overusing parallel streams** dla małych kolekcji
5. **Nie handling Optional** properly z findFirst/findAny

---
*Czas nauki: ~40 minut | Poziom: Zaawansowany*