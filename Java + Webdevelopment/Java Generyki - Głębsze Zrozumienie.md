# 🧬 Java - Generyki - Głębsze Zrozumienie

## 📚 Wprowadzenie
Generyki (Generics) to mechanizm w Javie pozwalający na tworzenie kodu, który może pracować z różnymi typami danych przy zachowaniu bezpieczeństwa typów. Zostały wprowadzone w Java 5 i są fundamentem nowoczesnego programowania w Javie.

## 🔤 Podstawowa Składnia Generików

### Klasy Generyczne
```java
// Klasa generyczna z jednym parametrem typu
public class Box<T> {
    private T content;
    
    public Box(T content) {
        this.content = content;
    }
    
    public T getContent() {
        return content;
    }
    
    public void setContent(T content) {
        this.content = content;
    }
    
    public boolean isEmpty() {
        return content == null;
    }
    
    @Override
    public String toString() {
        return "Box{content=" + content + "}";
    }
}

// Użycie klasy generycznej
public class BoxDemo {
    public static void main(String[] args) {
        // Jawne określenie typu
        Box<String> stringBox = new Box<>("Hello World");
        Box<Integer> intBox = new Box<>(42);
        Box<Double> doubleBox = new Box<>(3.14);
        
        // Diamond operator (Java 7+)
        Box<String> anotherStringBox = new Box<>("Hello");
        
        System.out.println("String box: " + stringBox.getContent());
        System.out.println("Int box: " + intBox.getContent());
        System.out.println("Double box: " + doubleBox.getContent());
        
        // Kompilator zapewnia bezpieczeństwo typów
        // stringBox.setContent(123); // Błąd kompilacji!
    }
}
```

### Klasy z Wieloma Parametrami Typu
```java
public class Pair<T, U> {
    private T first;
    private U second;
    
    public Pair(T first, U second) {
        this.first = first;
        this.second = second;
    }
    
    public T getFirst() { return first; }
    public U getSecond() { return second; }
    
    public void setFirst(T first) { this.first = first; }
    public void setSecond(U second) { this.second = second; }
    
    @Override
    public String toString() {
        return "Pair{first=" + first + ", second=" + second + "}";
    }
    
    // Metoda generyczna w klasie generycznej
    public <V> Pair<T, V> replaceSecond(V newSecond) {
        return new Pair<>(this.first, newSecond);
    }
}

// Triple z trzema parametrami typu
public class Triple<T, U, V> {
    private T first;
    private U second;
    private V third;
    
    public Triple(T first, U second, V third) {
        this.first = first;
        this.second = second;
        this.third = third;
    }
    
    // Factory methods dla popularnych kombinacji
    public static <T> Triple<T, T, T> of(T value) {
        return new Triple<>(value, value, value);
    }
    
    public static <T, U, V> Triple<T, U, V> of(T first, U second, V third) {
        return new Triple<>(first, second, third);
    }
    
    // Gettery i settery...
    public T getFirst() { return first; }
    public U getSecond() { return second; }
    public V getThird() { return third; }
    
    @Override
    public String toString() {
        return "Triple{" + first + ", " + second + ", " + third + "}";
    }
}

// Przykłady użycia
public class PairTripleDemo {
    public static void main(String[] args) {
        // Pair examples
        Pair<String, Integer> nameAge = new Pair<>("Anna", 25);
        Pair<Integer, String> idName = new Pair<>(1001, "Jan Kowalski");
        Pair<Double, Double> coordinates = new Pair<>(52.2297, 21.0122);
        
        System.out.println("Imię i wiek: " + nameAge);
        System.out.println("ID i imię: " + idName);
        System.out.println("Współrzędne Warszawy: " + coordinates);
        
        // Użycie metody generycznej
        Pair<String, Double> nameScore = nameAge.replaceSecond(95.5);
        System.out.println("Imię i wynik: " + nameScore);
        
        // Triple examples
        Triple<String, Integer, Boolean> personInfo = 
            new Triple<>("Piotr", 30, true);
        Triple<Integer, Integer, Integer> rgbColor = Triple.of(255, 128, 64);
        
        System.out.println("Informacje o osobie: " + personInfo);
        System.out.println("Kolor RGB: " + rgbColor);
    }
}
```

## 🔧 Metody Generyczne

```java
public class GenericMethods {
    
    // Metoda generyczna - parametr typu przed typem zwracanym
    public static <T> void swap(T[] array, int i, int j) {
        if (i >= 0 && j >= 0 && i < array.length && j < array.length) {
            T temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
    }
    
    // Metoda z multiple type parameters
    public static <T, U> Pair<U, T> reversePair(Pair<T, U> original) {
        return new Pair<>(original.getSecond(), original.getFirst());
    }
    
    // Bounded type parameter
    public static <T extends Number> double sum(T[] numbers) {
        double total = 0.0;
        for (T number : numbers) {
            total += number.doubleValue();
        }
        return total;
    }
    
    // Multiple bounds
    public static <T extends Number & Comparable<T>> T findMax(T[] array) {
        if (array == null || array.length == 0) {
            return null;
        }
        
        T max = array[0];
        for (int i = 1; i < array.length; i++) {
            if (array[i].compareTo(max) > 0) {
                max = array[i];
            }
        }
        return max;
    }
    
    // Generic method z constraints na return type
    public static <T> T findFirst(java.util.List<T> list, java.util.function.Predicate<T> predicate) {
        for (T item : list) {
            if (predicate.test(item)) {
                return item;
            }
        }
        return null;
    }
    
    // Type inference examples
    public static void demonstrateMethods() {
        // Swap arrays
        String[] names = {"Anna", "Bartosz", "Cecylia"};
        System.out.println("Przed: " + java.util.Arrays.toString(names));
        swap(names, 0, 2); // Type inferred as String
        System.out.println("Po: " + java.util.Arrays.toString(names));
        
        Integer[] numbers = {1, 2, 3, 4, 5};
        swap(numbers, 1, 3); // Type inferred as Integer
        System.out.println("Liczby po swap: " + java.util.Arrays.toString(numbers));
        
        // Reverse pair
        Pair<String, Integer> original = new Pair<>("Hello", 42);
        Pair<Integer, String> reversed = reversePair(original);
        System.out.println("Oryginał: " + original);
        System.out.println("Odwrócony: " + reversed);
        
        // Sum numbers
        Double[] doubles = {1.5, 2.5, 3.5};
        Integer[] ints = {10, 20, 30};
        
        System.out.println("Suma doubles: " + sum(doubles));
        System.out.println("Suma integers: " + sum(ints));
        
        // Find max
        System.out.println("Max double: " + findMax(doubles));
        System.out.println("Max integer: " + findMax(ints));
        
        // Find first with predicate
        java.util.List<String> words = java.util.Arrays.asList("apple", "banana", "cherry");
        String longWord = findFirst(words, word -> word.length() > 5);
        System.out.println("Pierwsze długie słowo: " + longWord);
    }
}
```

## 🌟 Wildcards (Symbole Wieloznaczne)

### Upper Bounded Wildcards (? extends)
```java
import java.util.*;

public class WildcardsDemo {
    
    // ? extends Number - może być Number lub jego podklasy
    public static double sumNumbers(List<? extends Number> numbers) {
        double sum = 0.0;
        for (Number number : numbers) {
            sum += number.doubleValue();
        }
        return sum;
    }
    
    // Consumer - może dodawać tylko do kolekcji
    public static void addNumbers(List<? super Integer> list) {
        list.add(42);
        list.add(100);
        // list.add(3.14); // Błąd - nie można dodać Double
    }
    
    // Copy method demonstrating PECS (Producer Extends, Consumer Super)
    public static <T> void copy(List<? super T> dest, List<? extends T> src) {
        for (T item : src) {
            dest.add(item);
        }
    }
    
    public static void demonstrateWildcards() {
        // Upper bounded - producer
        List<Integer> integers = Arrays.asList(1, 2, 3, 4, 5);
        List<Double> doubles = Arrays.asList(1.1, 2.2, 3.3);
        List<Number> numbers = Arrays.asList(1, 2.5, 3);
        
        System.out.println("Suma integers: " + sumNumbers(integers));
        System.out.println("Suma doubles: " + sumNumbers(doubles));
        System.out.println("Suma numbers: " + sumNumbers(numbers));
        
        // Lower bounded - consumer
        List<Number> numberList = new ArrayList<>();
        List<Object> objectList = new ArrayList<>();
        
        addNumbers(numberList);  // Number is super type of Integer
        addNumbers(objectList);  // Object is super type of Integer
        // addNumbers(integers);    // Błąd - Integer nie jest super type of Integer
        
        System.out.println("Number list: " + numberList);
        System.out.println("Object list: " + objectList);
        
        // Copy demonstration
        List<String> source = Arrays.asList("a", "b", "c");
        List<Object> destination = new ArrayList<>();
        copy(destination, source);
        System.out.println("Skopiowane: " + destination);
    }
}
```

### Unbounded Wildcards (?)
```java
public class UnboundedWildcardsDemo {
    
    // Unbounded wildcard - dla operacji które nie zależą od typu
    public static void printList(List<?> list) {
        for (Object item : list) {
            System.out.print(item + " ");
        }
        System.out.println();
    }
    
    public static int getSize(List<?> list) {
        return list.size();
    }
    
    public static boolean isEmpty(Collection<?> collection) {
        return collection.isEmpty();
    }
    
    // Capture helper dla complex scenarios
    public static void reverse(List<?> list) {
        reverseHelper(list);
    }
    
    private static <T> void reverseHelper(List<T> list) {
        Collections.reverse(list);
    }
    
    public static void demonstrateUnbounded() {
        List<String> strings = Arrays.asList("jeden", "dwa", "trzy");
        List<Integer> integers = Arrays.asList(1, 2, 3, 4);
        List<Double> doubles = Arrays.asList(1.1, 2.2, 3.3);
        
        System.out.print("Strings: ");
        printList(strings);
        
        System.out.print("Integers: ");
        printList(integers);
        
        System.out.print("Doubles: ");
        printList(doubles);
        
        System.out.println("Size of strings: " + getSize(strings));
        System.out.println("Is integers empty: " + isEmpty(integers));
        
        List<String> mutableStrings = new ArrayList<>(Arrays.asList("a", "b", "c"));
        System.out.println("Before reverse: " + mutableStrings);
        reverse(mutableStrings);
        System.out.println("After reverse: " + mutableStrings);
    }
}
```

## 🏗️ Zaawansowane Konstrukcje Generyczne

### Generic Interfaces
```java
// Generic interface
interface Comparable<T> {
    int compareTo(T other);
}

interface Repository<T, ID> {
    T findById(ID id);
    List<T> findAll();
    T save(T entity);
    void deleteById(ID id);
    boolean existsById(ID id);
}

// Implementacja generic interface
class Student implements Comparable<Student> {
    private int id;
    private String name;
    private double gpa;
    
    public Student(int id, String name, double gpa) {
        this.id = id;
        this.name = name;
        this.gpa = gpa;
    }
    
    @Override
    public int compareTo(Student other) {
        return Double.compare(this.gpa, other.gpa);
    }
    
    // Getters, setters, toString...
    public int getId() { return id; }
    public String getName() { return name; }
    public double getGpa() { return gpa; }
    
    @Override
    public String toString() {
        return "Student{id=" + id + ", name='" + name + "', gpa=" + gpa + "}";
    }
}

class StudentRepository implements Repository<Student, Integer> {
    private Map<Integer, Student> students = new HashMap<>();
    
    @Override
    public Student findById(Integer id) {
        return students.get(id);
    }
    
    @Override
    public List<Student> findAll() {
        return new ArrayList<>(students.values());
    }
    
    @Override
    public Student save(Student student) {
        students.put(student.getId(), student);
        return student;
    }
    
    @Override
    public void deleteById(Integer id) {
        students.remove(id);
    }
    
    @Override
    public boolean existsById(Integer id) {
        return students.containsKey(id);
    }
}
```

### Bounded Type Parameters
```java
// Class with bounded type parameter
public class NumberContainer<T extends Number & Comparable<T>> {
    private List<T> numbers;
    
    public NumberContainer() {
        this.numbers = new ArrayList<>();
    }
    
    public void add(T number) {
        numbers.add(number);
    }
    
    public T getMax() {
        if (numbers.isEmpty()) return null;
        
        T max = numbers.get(0);
        for (T number : numbers) {
            if (number.compareTo(max) > 0) {
                max = number;
            }
        }
        return max;
    }
    
    public T getMin() {
        if (numbers.isEmpty()) return null;
        
        T min = numbers.get(0);
        for (T number : numbers) {
            if (number.compareTo(min) < 0) {
                min = number;
            }
        }
        return min;
    }
    
    public double getAverage() {
        if (numbers.isEmpty()) return 0.0;
        
        double sum = 0.0;
        for (T number : numbers) {
            sum += number.doubleValue();
        }
        return sum / numbers.size();
    }
    
    public List<T> getSorted() {
        List<T> sorted = new ArrayList<>(numbers);
        Collections.sort(sorted);
        return sorted;
    }
}

// Recursive type bounds
class EnumContainer<E extends Enum<E> & Serializable> {
    private Class<E> enumClass;
    
    public EnumContainer(Class<E> enumClass) {
        this.enumClass = enumClass;
    }
    
    public E[] getAllValues() {
        return enumClass.getEnumConstants();
    }
    
    public E valueOf(String name) {
        return Enum.valueOf(enumClass, name);
    }
}
```

## 🧪 Type Erasure i Raw Types

```java
public class TypeErasureDemo {
    
    // Type erasure demonstration
    public static void demonstrateTypeErasure() {
        List<String> stringList = new ArrayList<>();
        List<Integer> integerList = new ArrayList<>();
        
        // W runtime oba mają ten sam typ Class
        System.out.println("String list class: " + stringList.getClass());
        System.out.println("Integer list class: " + integerList.getClass());
        System.out.println("Same class? " + (stringList.getClass() == integerList.getClass()));
        
        // Type information jest usunięta w runtime
        // stringList i integerList mają type java.util.ArrayList
    }
    
    @SuppressWarnings("rawtypes") // Suppress raw type warnings
    public static void demonstrateRawTypes() {
        // Raw type - bez parametrów generycznych
        List rawList = new ArrayList();
        rawList.add("String");
        rawList.add(42);
        rawList.add(new Date());
        
        // Niebezpieczne - brak type safety
        for (Object item : rawList) {
            System.out.println("Item: " + item);
            // if (item instanceof String) {
            //     String str = (String) item; // Manual casting needed
            // }
        }
        
        // Mixing raw and parameterized types
        List<String> stringList = new ArrayList<>();
        assignRawToParameterized(rawList, stringList);
    }
    
    @SuppressWarnings({"unchecked", "rawtypes"})
    private static void assignRawToParameterized(List raw, List<String> parameterized) {
        // Compiler warning: unchecked assignment
        parameterized = raw;
        
        // Runtime ClassCastException możliwy przy próbie dostępu
        try {
            String first = parameterized.get(0); // Może rzucić ClassCastException
            System.out.println("First string: " + first);
        } catch (ClassCastException e) {
            System.err.println("ClassCastException: " + e.getMessage());
        }
    }
    
    // Cannot create instances of generic types
    public static <T> void cannotCreateGenericArray() {
        // T[] array = new T[10]; // Błąd kompilacji!
        // List<T>[] arrayOfLists = new List<T>[10]; // Błąd kompilacji!
        
        // Workaround using Object array
        @SuppressWarnings("unchecked")
        T[] array = (T[]) new Object[10];
        
        // Or using reflection (advanced)
        // T[] array = (T[]) Array.newInstance(clazz, size);
    }
}
```

## 🎯 Przykład Kompleksowy - Generic Cache System

```java
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Function;
import java.util.function.Supplier;

// Cache interface with generic key and value types
interface Cache<K, V> {
    V get(K key);
    V get(K key, Supplier<V> loader);
    void put(K key, V value);
    void remove(K key);
    void clear();
    int size();
    boolean containsKey(K key);
    Set<K> keySet();
    Collection<V> values();
}

// Generic cache implementation with TTL support
public class GenericCache<K, V> implements Cache<K, V> {
    
    // Internal cache entry with timestamp
    private static class CacheEntry<V> {
        final V value;
        final long timestamp;
        final long ttl;
        
        CacheEntry(V value, long ttl) {
            this.value = value;
            this.timestamp = System.currentTimeMillis();
            this.ttl = ttl;
        }
        
        boolean isExpired() {
            return ttl > 0 && (System.currentTimeMillis() - timestamp) > ttl;
        }
    }
    
    private final Map<K, CacheEntry<V>> cache;
    private final long defaultTtl;
    private final int maxSize;
    
    public GenericCache() {
        this(1000, 300000); // Default: 1000 entries, 5 minutes TTL
    }
    
    public GenericCache(int maxSize, long defaultTtlMs) {
        this.cache = new ConcurrentHashMap<>();
        this.maxSize = maxSize;
        this.defaultTtl = defaultTtlMs;
    }
    
    @Override
    public V get(K key) {
        CacheEntry<V> entry = cache.get(key);
        if (entry == null || entry.isExpired()) {
            if (entry != null) {
                cache.remove(key); // Remove expired entry
            }
            return null;
        }
        return entry.value;
    }
    
    @Override
    public V get(K key, Supplier<V> loader) {
        V value = get(key);
        if (value == null) {
            value = loader.get();
            if (value != null) {
                put(key, value);
            }
        }
        return value;
    }
    
    @Override
    public void put(K key, V value) {
        put(key, value, defaultTtl);
    }
    
    public void put(K key, V value, long ttl) {
        // Evict if cache is full
        if (cache.size() >= maxSize && !cache.containsKey(key)) {
            evictOldest();
        }
        
        cache.put(key, new CacheEntry<>(value, ttl));
    }
    
    @Override
    public void remove(K key) {
        cache.remove(key);
    }
    
    @Override
    public void clear() {
        cache.clear();
    }
    
    @Override
    public int size() {
        cleanupExpired();
        return cache.size();
    }
    
    @Override
    public boolean containsKey(K key) {
        return get(key) != null;
    }
    
    @Override
    public Set<K> keySet() {
        cleanupExpired();
        return new HashSet<>(cache.keySet());
    }
    
    @Override
    public Collection<V> values() {
        cleanupExpired();
        return cache.values().stream()
                    .map(entry -> entry.value)
                    .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
    }
    
    public Map<K, V> getAllValid() {
        cleanupExpired();
        Map<K, V> result = new HashMap<>();
        cache.forEach((key, entry) -> {
            if (!entry.isExpired()) {
                result.put(key, entry.value);
            }
        });
        return result;
    }
    
    private void evictOldest() {
        // Find oldest entry
        K oldestKey = cache.entrySet().stream()
                          .min(Map.Entry.<K, CacheEntry<V>>comparingByValue(
                              (e1, e2) -> Long.compare(e1.timestamp, e2.timestamp)))
                          .map(Map.Entry::getKey)
                          .orElse(null);
        
        if (oldestKey != null) {
            cache.remove(oldestKey);
        }
    }
    
    private void cleanupExpired() {
        cache.entrySet().removeIf(entry -> entry.getValue().isExpired());
    }
    
    public void printStats() {
        cleanupExpired();
        System.out.println("Cache Stats:");
        System.out.println("  Size: " + cache.size() + "/" + maxSize);
        System.out.println("  Default TTL: " + defaultTtl + "ms");
        System.out.println("  Keys: " + keySet());
    }
}

// Specialized cache implementations
class StringCache extends GenericCache<String, String> {
    public StringCache() {
        super(500, 600000); // 500 entries, 10 minutes TTL
    }
    
    public void putUpperCase(String key, String value) {
        put(key.toUpperCase(), value.toUpperCase());
    }
    
    public String getIgnoreCase(String key) {
        // Try exact match first
        String value = get(key);
        if (value != null) return value;
        
        // Try case-insensitive search
        return keySet().stream()
                      .filter(k -> k.equalsIgnoreCase(key))
                      .findFirst()
                      .map(this::get)
                      .orElse(null);
    }
}

class NumericCache<T extends Number> extends GenericCache<String, T> {
    private final Function<String, T> parser;
    
    public NumericCache(Function<String, T> parser) {
        this.parser = parser;
    }
    
    public T getOrParse(String key) {
        return get(key, () -> parser.apply(key));
    }
    
    public void putComputed(String expression, T value) {
        put("computed_" + expression, value);
    }
    
    public List<T> getAllNumbers() {
        return new ArrayList<>(values());
    }
}

// Demo class
public class GenericCacheDemo {
    public static void main(String[] args) {
        // Basic generic cache
        Cache<Integer, String> userCache = new GenericCache<>(100, 10000);
        userCache.put(1, "Anna Kowalska");
        userCache.put(2, "Piotr Nowak");
        
        System.out.println("User 1: " + userCache.get(1));
        System.out.println("User 3: " + userCache.get(3, () -> "Default User"));
        
        // String cache with specialized methods
        StringCache stringCache = new StringCache();
        stringCache.put("greeting", "Hello World");
        stringCache.putUpperCase("name", "john doe");
        
        System.out.println("Greeting: " + stringCache.get("greeting"));
        System.out.println("Name (exact): " + stringCache.get("NAME"));
        System.out.println("Name (ignore case): " + stringCache.getIgnoreCase("name"));
        
        // Numeric cache
        NumericCache<Double> doubleCache = new NumericCache<>(Double::parseDouble);
        doubleCache.put("pi", 3.14159);
        doubleCache.putComputed("2+2", 4.0);
        
        Double parsedValue = doubleCache.getOrParse("42.5");
        System.out.println("Parsed value: " + parsedValue);
        System.out.println("All numbers: " + doubleCache.getAllNumbers());
        
        // Complex object cache
        Cache<String, List<Integer>> listCache = new GenericCache<>();
        listCache.put("fibonacci", Arrays.asList(1, 1, 2, 3, 5, 8, 13));
        listCache.put("primes", Arrays.asList(2, 3, 5, 7, 11, 13, 17));
        
        List<Integer> fibonacci = listCache.get("fibonacci");
        System.out.println("Fibonacci: " + fibonacci);
        
        // Cache stats
        if (stringCache instanceof GenericCache) {
            ((GenericCache<String, String>) stringCache).printStats();
        }
    }
}
```

## 🔗 Powiązane Tematy
- [[Java Kolekcje - Szczegółowe Omówienie]] - Generyki w kolekcjach
- [[Java Stream API - Pełny Przewodnik]] - Generyki w Stream API
- [[Java Reflection API]] - Type tokens i generic reflection
- [[Java Design Patterns]] - Wzorce wykorzystujące generyki

## 💡 Najlepsze Praktyki

1. **Używaj generików zawsze gdy to możliwe** - zapewniają bezpieczeństwo typów
2. **Preferuj `List<String>` nad raw `List`** - unikaj raw types
3. **Używaj bounded parameters** gdy potrzebujesz konkretnych operacji
4. **Stosuj PECS rule**: Producer Extends, Consumer Super
5. **Unikaj generic arrays** - używaj kolekcji zamiast tego
6. **Używaj type witnesses** w niejasnych sytuacjach: `Collections.<String>emptyList()`
7. **Definiuj pomocnicze metody factory** dla complex generic types

## ⚠️ Częste Pułapki

1. **Type erasure** - informacje o typie są usuwane w runtime
2. **Cannot instantiate generic types** - `new T()` nie jest możliwe
3. **Generic array creation** - `new List<String>[10]` jest zabronione
4. **Raw type warnings** - zawsze używaj parametryzowanych typów
5. **Overloading with erasure conflicts** - `method(List<String>)` i `method(List<Integer>)` to konflikt

---
*Czas nauki: ~35 minut | Poziom: Zaawansowany*