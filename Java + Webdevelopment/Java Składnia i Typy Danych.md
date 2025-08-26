# 🔤 Java - Składnia i Typy Danych

## 📚 Wprowadzenie
Java jest silnie typowanym językiem programowania, co oznacza, że każda zmienna musi mieć określony typ. Składnia Java jest podobna do C/C++, ale jest prostsza i bezpieczniejsza.

## 🧩 Typy Podstawowe (Primitives)

### Typy Liczbowe Całkowite
```java
// Całkowite
byte myByte = 127;          // -128 do 127 (8 bit)
short myShort = 32767;      // -32,768 do 32,767 (16 bit)
int myInt = 2147483647;     // -2^31 do 2^31-1 (32 bit)
long myLong = 9223372036854775807L; // -2^63 do 2^63-1 (64 bit)

// Literały w różnych systemach
int decimal = 42;
int binary = 0b101010;      // System binarny
int hex = 0x2A;             // System szesnastkowy
int octal = 052;            // System ósemkowy (rzadko używany)
```

### Typy Liczbowe Zmiennoprzecinkowe
```java
float myFloat = 3.14f;      // 32-bit IEEE 754
double myDouble = 3.14159265359; // 64-bit IEEE 754 (domyślny)

// Notacja naukowa
double scientific = 1.23e-4; // 0.000123
float bigNumber = 1.5e6f;    // 1,500,000
```

### Typ Logiczny i Znakowy
```java
boolean isTrue = true;
boolean isFalse = false;

char letter = 'A';          // Pojedynczy znak Unicode
char unicode = '\u0041';    // 'A' w Unicode
char escape = '\n';         // Znak specjalny (nowa linia)
```

## 📝 Zmienne i Stałe

### Deklaracja i Inicjalizacja
```java
// Deklaracja z inicjalizacją
int age = 25;
String name = "Jan Kowalski";

// Deklaracja bez inicjalizacji
int count;
count = 10;

// Wiele zmiennych tego samego typu
int x = 1, y = 2, z = 3;

// Zmienne finalne (stałe)
final int MAX_SIZE = 100;
final String APPLICATION_NAME = "MyApp";
```

### Konwencje Nazewnictwa
```java
// Zmienne - camelCase
int studentAge;
String firstName;
boolean isActive;

// Stałe - UPPER_SNAKE_CASE
final int MAX_RETRY_COUNT = 3;
final double PI = 3.14159;

// Klasy - PascalCase (omawiane w innych notatkach)
class StudentManager { }
```

## 🔄 Operatory

### Operatory Arytmetyczne
```java
int a = 10, b = 3;

int sum = a + b;        // 13
int difference = a - b; // 7
int product = a * b;    // 30
int quotient = a / b;   // 3 (dzielenie całkowite)
int remainder = a % b;  // 1 (reszta z dzielenia)

// Operatory pre/post increment/decrement
int x = 5;
System.out.println(++x); // 6 (pre-increment)
System.out.println(x++); // 6, potem x = 7 (post-increment)
System.out.println(--x); // 6 (pre-decrement)
System.out.println(x--); // 6, potem x = 5 (post-decrement)
```

### Operatory Przypisania
```java
int x = 10;
x += 5;  // x = x + 5;  → x = 15
x -= 3;  // x = x - 3;  → x = 12
x *= 2;  // x = x * 2;  → x = 24
x /= 4;  // x = x / 4;  → x = 6
x %= 4;  // x = x % 4;  → x = 2
```

### Operatory Porównania
```java
int a = 10, b = 5;

boolean equal = (a == b);       // false
boolean notEqual = (a != b);    // true
boolean greater = (a > b);      // true
boolean greaterEqual = (a >= b); // true
boolean less = (a < b);         // false
boolean lessEqual = (a <= b);   // false
```

### Operatory Logiczne
```java
boolean x = true, y = false;

boolean and = x && y;    // false (koniunkcja)
boolean or = x || y;     // true (alternatywa)
boolean not = !x;        // false (negacja)

// Short-circuit evaluation
boolean result = (5 > 3) || (10 / 0 > 1); // true (drugie wyrażenie nie jest ewaluowane)
```

## 🔧 Konwersje Typów

### Konwersje Automatyczne (Widening)
```java
int intValue = 100;
long longValue = intValue;      // Automatyczna konwersja
double doubleValue = intValue;  // int → double

byte byteVal = 10;
int intVal = byteVal;          // byte → int
```

### Konwersje Jawne (Narrowing Casting)
```java
double doubleValue = 9.78;
int intValue = (int) doubleValue;  // 9 (utrata części dziesiętnej)

long longValue = 100L;
int intValue = (int) longValue;    // Może dojść do utraty danych

// Bezpieczne castowanie
if (longValue <= Integer.MAX_VALUE && longValue >= Integer.MIN_VALUE) {
    int safeInt = (int) longValue;
}
```

### Parsowanie Stringów
```java
// String → typy podstawowe
String numberStr = "123";
int intValue = Integer.parseInt(numberStr);
double doubleValue = Double.parseDouble("12.34");
boolean boolValue = Boolean.parseBoolean("true");

// Typy podstawowe → String
String intStr = Integer.toString(123);
String doubleStr = Double.toString(12.34);
String boolStr = Boolean.toString(true);

// Używając String.valueOf()
String valueStr = String.valueOf(42);
```

## 📊 Tablice (Arrays)

### Deklaracja i Inicjalizacja
```java
// Różne sposoby deklaracji
int[] numbers1 = new int[5];           // Tablica 5 elementów (wartości domyślne: 0)
int numbers2[] = new int[5];           // Alternatywna składnia
int[] numbers3 = {1, 2, 3, 4, 5};     // Inicjalizacja z wartościami
int[] numbers4 = new int[]{1, 2, 3, 4, 5}; // Jawna inicjalizacja

// Tablice różnych typów
String[] names = {"Anna", "Bartosz", "Czesław"};
boolean[] flags = new boolean[3];       // false, false, false
double[] prices = {19.99, 29.99, 39.99};
```

### Operacje na Tablicach
```java
int[] array = {10, 20, 30, 40, 50};

// Dostęp do elementów
int first = array[0];        // 10
int last = array[array.length - 1]; // 50

// Modyfikacja elementów
array[2] = 35;              // {10, 20, 35, 40, 50}

// Iteracja przez tablicę
for (int i = 0; i < array.length; i++) {
    System.out.println("Element " + i + ": " + array[i]);
}

// Enhanced for loop (for-each)
for (int value : array) {
    System.out.println("Wartość: " + value);
}
```

### Tablice Wielowymiarowe
```java
// Tablica dwuwymiarowa
int[][] matrix = new int[3][4];        // 3 wiersze, 4 kolumny
int[][] table = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};

// Dostęp do elementów
int element = table[1][2];             // 7

// Iteracja przez tablicę 2D
for (int row = 0; row < table.length; row++) {
    for (int col = 0; col < table[row].length; col++) {
        System.out.print(table[row][col] + " ");
    }
    System.out.println();
}

// Enhanced for loop dla 2D
for (int[] row : table) {
    for (int value : row) {
        System.out.print(value + " ");
    }
    System.out.println();
}
```

## 🎯 Przykłady Praktyczne

### Kalkulator Prosty
```java
public class SimpleCalculator {
    public static void main(String[] args) {
        double a = 15.5;
        double b = 4.2;
        
        System.out.println("Liczba a: " + a);
        System.out.println("Liczba b: " + b);
        System.out.println("Suma: " + (a + b));
        System.out.println("Różnica: " + (a - b));
        System.out.println("Iloczyn: " + (a * b));
        System.out.println("Iloraz: " + (a / b));
        System.out.println("Reszta: " + (a % b));
    }
}
```

### Analiza Tablicy
```java
public class ArrayAnalysis {
    public static void main(String[] args) {
        int[] scores = {85, 92, 78, 96, 87, 88, 91, 84};
        
        // Znajdź minimum i maksimum
        int min = scores[0];
        int max = scores[0];
        int sum = 0;
        
        for (int score : scores) {
            if (score < min) min = score;
            if (score > max) max = score;
            sum += score;
        }
        
        double average = (double) sum / scores.length;
        
        System.out.println("Wyniki: " + java.util.Arrays.toString(scores));
        System.out.println("Minimum: " + min);
        System.out.println("Maksimum: " + max);
        System.out.println("Średnia: " + average);
        System.out.println("Suma: " + sum);
    }
}
```

## 🔗 Powiązane Tematy
- [[Java Podstawy]] - Podstawowe koncepcje OOP
- [[Java Kolekcje - Szczegółowe Omówienie]] - Alternatywy dla tablic
- [[Java Zaawansowane]] - Generyki i Stream API
- [[Java Memory Management i Garbage Collection]] - Zarządzanie pamięcią

## 💡 Najlepsze Praktyki
1. **Używaj opisowych nazw zmiennych** - `studentAge` zamiast `x`
2. **Preferuj `double` nad `float`** dla liczb zmiennoprzecinkowych
3. **Używaj `final` dla stałych** - zapobiega przypadkowym modyfikacjom
4. **Inicjalizuj zmienne przy deklaracji** gdy to możliwe
5. **Uważaj na konwersje typu** - mogą prowadzić do utraty danych

---
*Czas nauki: ~20 minut | Poziom: Podstawowy*