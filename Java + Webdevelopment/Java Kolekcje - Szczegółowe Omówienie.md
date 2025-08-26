# 📦 Java - Kolekcje - Szczegółowe Omówienie

## 📚 Wprowadzenie
Java Collections Framework to zestaw klas i interfejsów do przechowywania i manipulowania grupami obiektów. Jest fundamentem większości aplikacji Java i kluczowym elementem efektywnego programowania.

## 🏗️ Hierarchia Kolekcji

```java
// Główne interfejsy
Collection<E>
├── List<E>          // Uporządkowana kolekcja z duplikatami
├── Set<E>           // Kolekcja bez duplikatów
├── Queue<E>         // Kolejka FIFO/LIFO
└── Deque<E>         // Dwukierunkowa kolejka

Map<E,V>             // Pary klucz-wartość (nie dziedziczy po Collection)
```

## 📋 Listy (Lists)

### ArrayList - Dynamiczna Tablica
```java
import java.util.*;

public class ArrayListDemo {
    public static void main(String[] args) {
        // Różne sposoby tworzenia
        List<String> names = new ArrayList<>();
        List<Integer> numbers = new ArrayList<>(20); // Początkowa pojemność
        List<String> cities = new ArrayList<>(Arrays.asList("Warszawa", "Kraków", "Gdańsk"));
        
        // Dodawanie elementów
        names.add("Anna");
        names.add("Bartosz");
        names.add(1, "Cecylia"); // Wstawienie na indeks 1
        names.addAll(Arrays.asList("Dawid", "Ewa"));
        
        System.out.println("Lista: " + names); // [Anna, Cecylia, Bartosz, Dawid, Ewa]
        
        // Dostęp do elementów
        String firstName = names.get(0);
        String lastName = names.get(names.size() - 1);
        
        // Modyfikacja
        names.set(1, "Celina"); // Zmiana na indeksie 1
        
        // Usuwanie
        names.remove(0);           // Usunięcie przez indeks
        names.remove("Dawid");     // Usunięcie przez wartość
        names.removeIf(name -> name.startsWith("E")); // Lambda
        
        // Iteracja
        for (String name : names) {
            System.out.println("Imię: " + name);
        }
        
        // Iterator
        Iterator<String> it = names.iterator();
        while (it.hasNext()) {
            String name = it.next();
            if (name.length() < 5) {
                it.remove(); // Bezpieczne usuwanie podczas iteracji
            }
        }
        
        // Wyszukiwanie
        boolean containsBartosz = names.contains("Bartosz");
        int indexOfBartosz = names.indexOf("Bartosz");
        int lastIndexOfBartosz = names.lastIndexOf("Bartosz");
        
        // Sortowanie
        Collections.sort(names);
        Collections.sort(names, Collections.reverseOrder());
        
        // Custom comparator
        Collections.sort(names, (a, b) -> a.length() - b.length());
        
        // Sublista
        List<String> subList = names.subList(1, 3); // Od indeksu 1 do 3 (exclusive)
    }
}
```

### LinkedList - Lista Podwójnie Łączona
```java
public class LinkedListDemo {
    public static void main(String[] args) {
        LinkedList<String> linkedList = new LinkedList<>();
        
        // LinkedList implementuje zarówno List jak i Deque
        linkedList.addFirst("Pierwszy");
        linkedList.addLast("Ostatni");
        linkedList.add(1, "Środkowy");
        
        System.out.println("Lista: " + linkedList);
        
        // Metody specyficzne dla LinkedList
        String first = linkedList.peekFirst();  // Nie usuwa
        String last = linkedList.peekLast();    // Nie usuwa
        
        String removedFirst = linkedList.pollFirst(); // Usuwa i zwraca
        String removedLast = linkedList.pollLast();   // Usuwa i zwraca
        
        // Używanie jako stos (LIFO)
        linkedList.push("Element 1");
        linkedList.push("Element 2");
        String popped = linkedList.pop(); // Usuwa i zwraca ostatni
        
        // Używanie jako kolejka (FIFO)
        linkedList.offer("Zadanie 1");
        linkedList.offer("Zadanie 2");
        String processed = linkedList.poll(); // Usuwa i zwraca pierwszy
    }
}
```

### Vector - Synchronizowana Lista (Legacy)
```java
public class VectorDemo {
    public static void main(String[] args) {
        Vector<Integer> vector = new Vector<>();
        
        // Vector jest thread-safe (synchronizowany)
        // Ale rzadko używany z powodu wydajności
        
        vector.add(10);
        vector.add(20);
        vector.addElement(30); // Stara metoda
        
        // Enumerator (stary sposób iteracji)
        Enumeration<Integer> enum = vector.elements();
        while (enum.hasMoreElements()) {
            System.out.println(enum.nextElement());
        }
        
        // Lepsze rozwiązanie dla thread-safety:
        List<Integer> syncList = Collections.synchronizedList(new ArrayList<>());
    }
}
```

## 🎯 Zbiory (Sets)

### HashSet - Zbiór Bez Kolejności
```java
public class HashSetDemo {
    public static void main(String[] args) {
        Set<String> uniqueNames = new HashSet<>();
        
        // Dodawanie (duplikaty są ignorowane)
        uniqueNames.add("Anna");
        uniqueNames.add("Bartosz");
        uniqueNames.add("Anna"); // Nie zostanie dodane
        
        System.out.println("Zbiór: " + uniqueNames); // [Anna, Bartosz] (kolejność nieważna)
        
        // Sprawdzanie zawartości
        boolean hasAnna = uniqueNames.contains("Anna");
        
        // Operacje na zbiorach
        Set<String> otherNames = new HashSet<>(Arrays.asList("Bartosz", "Cecylia", "Dawid"));
        
        // Suma zbiorów (union)
        Set<String> union = new HashSet<>(uniqueNames);
        union.addAll(otherNames);
        
        // Część wspólna (intersection)
        Set<String> intersection = new HashSet<>(uniqueNames);
        intersection.retainAll(otherNames);
        
        // Różnica zbiorów
        Set<String> difference = new HashSet<>(uniqueNames);
        difference.removeAll(otherNames);
        
        System.out.println("Suma: " + union);
        System.out.println("Część wspólna: " + intersection);
        System.out.println("Różnica: " + difference);
    }
}
```

### LinkedHashSet - Zbiór z Zachowaną Kolejnością
```java
public class LinkedHashSetDemo {
    public static void main(String[] args) {
        Set<String> orderedSet = new LinkedHashSet<>();
        
        orderedSet.add("Trzeci");
        orderedSet.add("Pierwszy");
        orderedSet.add("Drugi");
        orderedSet.add("Pierwszy"); // Duplikat - ignorowany
        
        System.out.println("LinkedHashSet: " + orderedSet); 
        // [Trzeci, Pierwszy, Drugi] - zachowana kolejność wstawiania
        
        // Użycie do usuwania duplikatów z zachowaniem kolejności
        List<String> listWithDuplicates = Arrays.asList("a", "b", "a", "c", "b", "d");
        List<String> withoutDuplicates = new ArrayList<>(new LinkedHashSet<>(listWithDuplicates));
        System.out.println("Bez duplikatów: " + withoutDuplicates); // [a, b, c, d]
    }
}
```

### TreeSet - Posortowany Zbiór
```java
public class TreeSetDemo {
    public static void main(String[] args) {
        Set<Integer> sortedNumbers = new TreeSet<>();
        
        sortedNumbers.add(5);
        sortedNumbers.add(2);
        sortedNumbers.add(8);
        sortedNumbers.add(1);
        
        System.out.println("TreeSet: " + sortedNumbers); // [1, 2, 5, 8] - automatyczne sortowanie
        
        // NavigableSet methods (TreeSet implementuje NavigableSet)
        TreeSet<Integer> treeSet = new TreeSet<>(Arrays.asList(1, 3, 5, 7, 9, 11));
        
        System.out.println("Lower than 5: " + treeSet.lower(5));     // 3
        System.out.println("Floor of 6: " + treeSet.floor(6));       // 5
        System.out.println("Ceiling of 6: " + treeSet.ceiling(6));   // 7
        System.out.println("Higher than 5: " + treeSet.higher(5));   // 7
        
        // Subsets
        SortedSet<Integer> headSet = treeSet.headSet(7);      // < 7
        SortedSet<Integer> tailSet = treeSet.tailSet(5);      // >= 5
        SortedSet<Integer> subSet = treeSet.subSet(3, 9);     // >= 3 and < 9
        
        System.out.println("Head set: " + headSet);  // [1, 3, 5]
        System.out.println("Tail set: " + tailSet);  // [5, 7, 9, 11]
        System.out.println("Sub set: " + subSet);    // [3, 5, 7]
        
        // Custom comparator
        TreeSet<String> reverseSet = new TreeSet<>(Collections.reverseOrder());
        reverseSet.addAll(Arrays.asList("apple", "banana", "cherry"));
        System.out.println("Reverse order: " + reverseSet); // [cherry, banana, apple]
    }
}
```

## 🗺️ Mapy (Maps)

### HashMap - Mapa Bez Kolejności
```java
public class HashMapDemo {
    public static void main(String[] args) {
        Map<String, Integer> studentGrades = new HashMap<>();
        
        // Dodawanie par klucz-wartość
        studentGrades.put("Anna", 85);
        studentGrades.put("Bartosz", 92);
        studentGrades.put("Cecylia", 78);
        studentGrades.put("Anna", 88); // Nadpisanie poprzedniej wartości
        
        // Bezpieczne dodawanie (tylko jeśli klucz nie istnieje)
        studentGrades.putIfAbsent("Dawid", 75);
        
        // Dostęp do wartości
        Integer annaGrade = studentGrades.get("Anna");          // 88
        Integer unknownGrade = studentGrades.get("Nieznany");   // null
        Integer defaultGrade = studentGrades.getOrDefault("Nieznany", 0); // 0
        
        // Sprawdzanie zawartości
        boolean hasAnna = studentGrades.containsKey("Anna");
        boolean hasGrade90 = studentGrades.containsValue(90);
        
        // Iteracja przez mapę
        for (Map.Entry<String, Integer> entry : studentGrades.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
        
        // Iteracja tylko po kluczach
        for (String student : studentGrades.keySet()) {
            System.out.println("Student: " + student);
        }
        
        // Iteracja tylko po wartościach
        for (Integer grade : studentGrades.values()) {
            System.out.println("Ocena: " + grade);
        }
        
        // Java 8 forEach
        studentGrades.forEach((student, grade) -> {
            System.out.println(student + " ma ocenę " + grade);
        });
        
        // Operacje z Java 8+
        studentGrades.compute("Anna", (key, val) -> val + 5);        // Anna: 93
        studentGrades.computeIfAbsent("Ewa", key -> 80);            // Dodaje Ewa: 80
        studentGrades.computeIfPresent("Bartosz", (key, val) -> val + 3); // Bartosz: 95
        
        // Merge values
        Map<String, Integer> additionalGrades = Map.of("Anna", 2, "Filip", 89);
        additionalGrades.forEach((student, grade) -> 
            studentGrades.merge(student, grade, (oldVal, newVal) -> oldVal + newVal)
        );
        
        // Replace operations
        studentGrades.replace("Cecylia", 78, 82); // Replace only if old value matches
        studentGrades.replaceAll((student, grade) -> grade > 90 ? grade : grade + 5);
    }
}
```

### LinkedHashMap - Mapa z Zachowaną Kolejnością
```java
public class LinkedHashMapDemo {
    public static void main(String[] args) {
        // Zachowuje kolejność wstawiania
        Map<String, String> insertionOrder = new LinkedHashMap<>();
        insertionOrder.put("C", "Third");
        insertionOrder.put("A", "First");
        insertionOrder.put("B", "Second");
        
        System.out.println("Insertion order: " + insertionOrder);
        // {C=Third, A=First, B=Second}
        
        // LRU Cache implementation
        Map<String, String> lruCache = new LinkedHashMap<String, String>(16, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<String, String> eldest) {
                return size() > 3; // Maksymalnie 3 elementy
            }
        };
        
        lruCache.put("A", "First");
        lruCache.put("B", "Second");
        lruCache.put("C", "Third");
        System.out.println("LRU Cache: " + lruCache);
        
        lruCache.get("A"); // A becomes most recently used
        lruCache.put("D", "Fourth"); // B will be removed (least recently used)
        System.out.println("After access and new insertion: " + lruCache);
        // {C=Third, A=First, D=Fourth}
    }
}
```

### TreeMap - Posortowana Mapa
```java
public class TreeMapDemo {
    public static void main(String[] args) {
        Map<String, Integer> sortedMap = new TreeMap<>();
        sortedMap.put("Charlie", 25);
        sortedMap.put("Alice", 30);
        sortedMap.put("Bob", 28);
        
        System.out.println("Sorted by keys: " + sortedMap);
        // {Alice=30, Bob=28, Charlie=25}
        
        // NavigableMap methods
        TreeMap<Integer, String> scores = new TreeMap<>();
        scores.put(85, "B");
        scores.put(92, "A");
        scores.put(78, "C");
        scores.put(96, "A+");
        
        System.out.println("Lower key than 90: " + scores.lowerKey(90));     // 85
        System.out.println("Floor key of 90: " + scores.floorKey(90));       // 85
        System.out.println("Ceiling key of 90: " + scores.ceilingKey(90));   // 92
        System.out.println("Higher key than 85: " + scores.higherKey(85));   // 92
        
        // Submaps
        SortedMap<Integer, String> headMap = scores.headMap(90);    // < 90
        SortedMap<Integer, String> tailMap = scores.tailMap(85);    // >= 85
        SortedMap<Integer, String> subMap = scores.subMap(80, 95);  // >= 80 and < 95
        
        System.out.println("Head map: " + headMap);  // {78=C, 85=B}
        System.out.println("Tail map: " + tailMap);  // {85=B, 92=A, 96=A+}
        System.out.println("Sub map: " + subMap);    // {85=B, 92=A}
        
        // First and last entries
        Map.Entry<Integer, String> firstEntry = scores.firstEntry();
        Map.Entry<Integer, String> lastEntry = scores.lastEntry();
        
        System.out.println("First: " + firstEntry);  // 78=C
        System.out.println("Last: " + lastEntry);    // 96=A+
    }
}
```

## 🚶 Kolejki (Queues)

### PriorityQueue - Kolejka Priorytetowa
```java
public class PriorityQueueDemo {
    public static void main(String[] args) {
        // Natural ordering (min heap)
        Queue<Integer> minHeap = new PriorityQueue<>();
        minHeap.offer(5);
        minHeap.offer(2);
        minHeap.offer(8);
        minHeap.offer(1);
        
        while (!minHeap.isEmpty()) {
            System.out.print(minHeap.poll() + " "); // 1 2 5 8
        }
        System.out.println();
        
        // Max heap using reverse order comparator
        Queue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        maxHeap.addAll(Arrays.asList(5, 2, 8, 1));
        
        while (!maxHeap.isEmpty()) {
            System.out.print(maxHeap.poll() + " "); // 8 5 2 1
        }
        System.out.println();
        
        // Custom objects with priority
        Queue<Task> taskQueue = new PriorityQueue<>();
        taskQueue.offer(new Task("Low priority task", 1));
        taskQueue.offer(new Task("High priority task", 5));
        taskQueue.offer(new Task("Medium priority task", 3));
        
        while (!taskQueue.isEmpty()) {
            System.out.println(taskQueue.poll());
        }
    }
    
    static class Task implements Comparable<Task> {
        String name;
        int priority;
        
        Task(String name, int priority) {
            this.name = name;
            this.priority = priority;
        }
        
        @Override
        public int compareTo(Task other) {
            return Integer.compare(other.priority, this.priority); // Higher priority first
        }
        
        @Override
        public String toString() {
            return name + " (Priority: " + priority + ")";
        }
    }
}
```

### ArrayDeque - Dwukierunkowa Kolejka
```java
public class ArrayDequeDemo {
    public static void main(String[] args) {
        Deque<String> deque = new ArrayDeque<>();
        
        // Dodawanie na końce
        deque.addFirst("First");
        deque.addLast("Last");
        deque.offerFirst("New First");
        deque.offerLast("New Last");
        
        System.out.println("Deque: " + deque);
        // [New First, First, Last, New Last]
        
        // Podglądanie bez usuwania
        String first = deque.peekFirst();
        String last = deque.peekLast();
        
        // Usuwanie z końców
        String removedFirst = deque.pollFirst();
        String removedLast = deque.pollLast();
        
        // Używanie jako stos (LIFO)
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(1);
        stack.push(2);
        stack.push(3);
        
        while (!stack.isEmpty()) {
            System.out.print(stack.pop() + " "); // 3 2 1
        }
        System.out.println();
        
        // Używanie jako kolejka (FIFO)
        Deque<String> queue = new ArrayDeque<>();
        queue.offer("Task 1");
        queue.offer("Task 2");
        queue.offer("Task 3");
        
        while (!queue.isEmpty()) {
            System.out.println("Processing: " + queue.poll());
        }
    }
}
```

## 🎯 Przykłady Praktyczne

### System Zarządzania Studentami
```java
import java.util.*;
import java.util.stream.Collectors;

public class StudentManagementSystem {
    private Map<String, Student> students = new HashMap<>();
    private Map<String, Set<Student>> courseEnrollments = new HashMap<>();
    private TreeSet<Student> topStudents = new TreeSet<>(
        Comparator.comparingDouble(Student::getGPA).reversed()
    );
    
    public void addStudent(Student student) {
        students.put(student.getId(), student);
        topStudents.add(student);
    }
    
    public void enrollStudentInCourse(String studentId, String courseName) {
        Student student = students.get(studentId);
        if (student != null) {
            courseEnrollments.computeIfAbsent(courseName, k -> new HashSet<>()).add(student);
            student.addCourse(courseName);
        }
    }
    
    public List<Student> getStudentsByCourse(String courseName) {
        return courseEnrollments.getOrDefault(courseName, Collections.emptySet())
                .stream()
                .sorted(Comparator.comparing(Student::getName))
                .collect(Collectors.toList());
    }
    
    public List<Student> getTopStudents(int count) {
        return topStudents.stream()
                .limit(count)
                .collect(Collectors.toList());
    }
    
    public Map<String, Long> getEnrollmentStatistics() {
        return courseEnrollments.entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> (long) entry.getValue().size()
                ));
    }
    
    static class Student implements Comparable<Student> {
        private String id;
        private String name;
        private double gpa;
        private Set<String> courses = new HashSet<>();
        
        public Student(String id, String name, double gpa) {
            this.id = id;
            this.name = name;
            this.gpa = gpa;
        }
        
        public void addCourse(String course) {
            courses.add(course);
        }
        
        @Override
        public int compareTo(Student other) {
            return this.id.compareTo(other.id);
        }
        
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            Student student = (Student) obj;
            return Objects.equals(id, student.id);
        }
        
        @Override
        public int hashCode() {
            return Objects.hash(id);
        }
        
        @Override
        public String toString() {
            return String.format("Student{id='%s', name='%s', gpa=%.2f, courses=%s}",
                    id, name, gpa, courses);
        }
        
        // Getters
        public String getId() { return id; }
        public String getName() { return name; }
        public double getGPA() { return gpa; }
        public Set<String> getCourses() { return new HashSet<>(courses); }
    }
    
    public static void main(String[] args) {
        StudentManagementSystem sms = new StudentManagementSystem();
        
        // Dodaj studentów
        sms.addStudent(new Student("001", "Anna Kowalska", 3.8));
        sms.addStudent(new Student("002", "Piotr Nowak", 3.2));
        sms.addStudent(new Student("003", "Maria Wiśniewska", 3.9));
        
        // Zapisz na kursy
        sms.enrollStudentInCourse("001", "Java Programming");
        sms.enrollStudentInCourse("002", "Java Programming");
        sms.enrollStudentInCourse("001", "Data Structures");
        sms.enrollStudentInCourse("003", "Java Programming");
        
        // Statystyki
        System.out.println("Studenci na kursie Java Programming:");
        sms.getStudentsByCourse("Java Programming").forEach(System.out::println);
        
        System.out.println("\nTop 2 studentów:");
        sms.getTopStudents(2).forEach(System.out::println);
        
        System.out.println("\nStatystyki zapisów:");
        sms.getEnrollmentStatistics().forEach((course, count) -> 
            System.out.println(course + ": " + count + " studentów"));
    }
}
```

### Cache Implementation
```java
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class MultiLevelCache<K, V> {
    private final Map<K, V> l1Cache; // Fast access, limited size
    private final Map<K, V> l2Cache; // Slower access, larger size
    private final Queue<K> l1AccessOrder;
    private final int l1MaxSize;
    private final int l2MaxSize;
    
    public MultiLevelCache(int l1MaxSize, int l2MaxSize) {
        this.l1MaxSize = l1MaxSize;
        this.l2MaxSize = l2MaxSize;
        this.l1Cache = new ConcurrentHashMap<>();
        this.l2Cache = new ConcurrentHashMap<>();
        this.l1AccessOrder = new ArrayDeque<>();
    }
    
    public V get(K key) {
        // Try L1 cache first
        V value = l1Cache.get(key);
        if (value != null) {
            updateAccessOrder(key);
            return value;
        }
        
        // Try L2 cache
        value = l2Cache.get(key);
        if (value != null) {
            // Promote to L1
            promoteToL1(key, value);
            return value;
        }
        
        return null; // Cache miss
    }
    
    public void put(K key, V value) {
        if (l1Cache.size() < l1MaxSize) {
            l1Cache.put(key, value);
            l1AccessOrder.offer(key);
        } else {
            // L1 is full, evict least recently used
            K evictedKey = l1AccessOrder.poll();
            if (evictedKey != null) {
                V evictedValue = l1Cache.remove(evictedKey);
                // Move evicted item to L2
                if (evictedValue != null) {
                    addToL2(evictedKey, evictedValue);
                }
            }
            l1Cache.put(key, value);
            l1AccessOrder.offer(key);
        }
    }
    
    private void promoteToL1(K key, V value) {
        l2Cache.remove(key);
        if (l1Cache.size() >= l1MaxSize) {
            // Evict from L1 to make space
            K evictedKey = l1AccessOrder.poll();
            if (evictedKey != null) {
                V evictedValue = l1Cache.remove(evictedKey);
                if (evictedValue != null) {
                    addToL2(evictedKey, evictedValue);
                }
            }
        }
        l1Cache.put(key, value);
        l1AccessOrder.offer(key);
    }
    
    private void addToL2(K key, V value) {
        if (l2Cache.size() >= l2MaxSize) {
            // Simple eviction strategy for L2 - remove random entry
            K randomKey = l2Cache.keySet().iterator().next();
            l2Cache.remove(randomKey);
        }
        l2Cache.put(key, value);
    }
    
    private void updateAccessOrder(K key) {
        l1AccessOrder.remove(key);
        l1AccessOrder.offer(key);
    }
    
    public void showCacheStatus() {
        System.out.println("L1 Cache (" + l1Cache.size() + "/" + l1MaxSize + "): " + l1Cache);
        System.out.println("L2 Cache (" + l2Cache.size() + "/" + l2MaxSize + "): " + l2Cache);
        System.out.println("L1 Access Order: " + l1AccessOrder);
    }
    
    public static void main(String[] args) {
        MultiLevelCache<String, String> cache = new MultiLevelCache<>(2, 3);
        
        // Fill cache
        cache.put("A", "Value A");
        cache.put("B", "Value B");
        cache.showCacheStatus();
        
        cache.put("C", "Value C"); // This should evict A to L2
        cache.showCacheStatus();
        
        // Access A - should promote back to L1
        System.out.println("Getting A: " + cache.get("A"));
        cache.showCacheStatus();
        
        cache.put("D", "Value D"); // This should evict B to L2
        cache.showCacheStatus();
    }
}
```

## 🔗 Powiązane Tematy
- [[Java Stream API - Pełny Przewodnik]] - Operacje na kolekcjach
- [[Java Zaawansowane]] - Generyki w kolekcjach
- [[Java Memory Management i Garbage Collection]] - Wpływ na wydajność
- [[Java Wielowątkowość - Threading]] - Thread-safe collections

## 💡 Najlepsze Praktyki

1. **Wybierz odpowiednią implementację** na podstawie przypadku użycia
2. **Używaj interfejsów** w deklaracjach typów (`List<String>` nie `ArrayList<String>`)
3. **Zdefiniuj początkową pojemność** dla lepszej wydajności
4. **Implementuj equals() i hashCode()** dla obiektów używanych jako klucze
5. **Używaj Collections utilities** do operacji pomocniczych
6. **Rozważ thread-safety** w środowisku wielowątkowym

## ⚙️ Wydajność Kolekcji

| Operacja | ArrayList | LinkedList | HashSet | TreeSet | HashMap | TreeMap |
|----------|-----------|------------|---------|---------|---------|---------|
| Add | O(1)* | O(1) | O(1) | O(log n) | O(1) | O(log n) |
| Get | O(1) | O(n) | O(1) | O(log n) | O(1) | O(log n) |
| Remove | O(n) | O(1)** | O(1) | O(log n) | O(1) | O(log n) |
| Contains | O(n) | O(n) | O(1) | O(log n) | O(1) | O(log n) |

*O(n) w przypadku resize  
**O(1) jeśli mamy iterator/referencję do węzła

---
*Czas nauki: ~35 minut | Poziom: Średniozaawansowany*