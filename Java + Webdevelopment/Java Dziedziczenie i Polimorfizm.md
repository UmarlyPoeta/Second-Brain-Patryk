# 🧬 Java - Dziedziczenie i Polimorfizm

## 📚 Wprowadzenie
Dziedziczenie i polimorfizm to fundamentalne koncepcje programowania obiektowego w Javie. Dziedziczenie pozwala na tworzenie nowych klas na podstawie istniejących, podczas gdy polimorfizm umożliwia używanie obiektów różnych typów przez wspólny interfejs.

## 🌳 Dziedziczenie (Inheritance)

### Podstawowe Koncepcje
```java
// Klasa bazowa (nadklasa)
public class Animal {
    protected String name;
    protected int age;
    
    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void eat() {
        System.out.println(name + " je pokarm.");
    }
    
    public void sleep() {
        System.out.println(name + " śpi.");
    }
    
    public void makeSound() {
        System.out.println(name + " wydaje dźwięk.");
    }
    
    public String getInfo() {
        return "Imię: " + name + ", Wiek: " + age;
    }
}

// Klasa pochodna (podklasa)
public class Dog extends Animal {
    private String breed;
    
    public Dog(String name, int age, String breed) {
        super(name, age);  // Wywołanie konstruktora klasy bazowej
        this.breed = breed;
    }
    
    // Nadpisanie metody (Override)
    @Override
    public void makeSound() {
        System.out.println(name + " szczeka: Woof! Woof!");
    }
    
    // Nowa metoda specyficzna dla Dog
    public void wagTail() {
        System.out.println(name + " merda ogonem.");
    }
    
    @Override
    public String getInfo() {
        return super.getInfo() + ", Rasa: " + breed;
    }
}
```

### Słowo Kluczowe `super`
```java
public class Cat extends Animal {
    private boolean isIndoor;
    
    public Cat(String name, int age, boolean isIndoor) {
        super(name, age);  // Wywołanie konstruktora Animal
        this.isIndoor = isIndoor;
    }
    
    @Override
    public void makeSound() {
        super.makeSound();  // Wywołanie metody z klasy bazowej
        System.out.println("Dodatkowo: Miau! Miau!");
    }
    
    public void climb() {
        if (!isIndoor) {
            System.out.println(name + " wspina się na drzewo.");
        } else {
            System.out.println(name + " wspina się na meble.");
        }
    }
}
```

### Modyfikatory Dostępu w Dziedziczeniu
```java
public class Vehicle {
    public String brand;        // Dostępne wszędzie
    protected int year;         // Dostępne w pakiecie i podklasach
    private String serialNumber; // Dostępne tylko w tej klasie
    String model;              // Package-private - dostępne w pakiecie
    
    // Getter dla prywatnego pola
    public String getSerialNumber() {
        return serialNumber;
    }
    
    protected void startEngine() {
        System.out.println("Silnik uruchamia się...");
    }
}

public class Car extends Vehicle {
    private int doors;
    
    public Car(String brand, int year, String model, int doors) {
        this.brand = brand;      // OK - public
        this.year = year;        // OK - protected
        this.model = model;      // OK - package-private (ten sam pakiet)
        // this.serialNumber = sn; // BŁĄD - private nie jest dziedziczny
        this.doors = doors;
    }
    
    public void start() {
        startEngine();  // OK - protected method
    }
}
```

## 🎭 Polimorfizm

### Polimorfizm przez Dziedziczenie
```java
public class AnimalDemo {
    public static void main(String[] args) {
        // Referencje typu Animal wskazujące na różne obiekty
        Animal[] animals = {
            new Dog("Burek", 5, "Labrador"),
            new Cat("Mruczek", 3, true),
            new Dog("Azor", 7, "Owczarek"),
            new Animal("Nieznane", 2)
        };
        
        // Polimorficzne wywołanie metod
        for (Animal animal : animals) {
            System.out.println(animal.getInfo());
            animal.makeSound();  // Każde zwierzę wydaje swój dźwięk
            animal.eat();
            System.out.println("---");
        }
        
        // Sprawdzanie typu i casting
        for (Animal animal : animals) {
            if (animal instanceof Dog) {
                Dog dog = (Dog) animal;  // Downcasting
                dog.wagTail();          // Metoda specyficzna dla Dog
            } else if (animal instanceof Cat) {
                Cat cat = (Cat) animal;  // Downcasting
                cat.climb();            // Metoda specyficzna dla Cat
            }
        }
    }
}
```

### Metody Abstrakcyjne i Klasy Abstrakcyjne
```java
// Klasa abstrakcyjna - nie można tworzyć jej instancji
public abstract class Shape {
    protected String color;
    protected double x, y;  // Pozycja
    
    public Shape(String color, double x, double y) {
        this.color = color;
        this.x = x;
        this.y = y;
    }
    
    // Metoda konkretna
    public void move(double deltaX, double deltaY) {
        this.x += deltaX;
        this.y += deltaY;
        System.out.println("Figura przeniesiona do (" + x + ", " + y + ")");
    }
    
    // Metody abstrakcyjne - muszą być zaimplementowane w podklasach
    public abstract double calculateArea();
    public abstract double calculatePerimeter();
    public abstract void draw();
    
    // Metoda używająca abstrakcyjnych metod
    public void showInfo() {
        System.out.println("Kolor: " + color);
        System.out.println("Pozycja: (" + x + ", " + y + ")");
        System.out.println("Pole: " + calculateArea());
        System.out.println("Obwód: " + calculatePerimeter());
    }
}

// Implementacja dla Rectangle
public class Rectangle extends Shape {
    private double width, height;
    
    public Rectangle(String color, double x, double y, double width, double height) {
        super(color, x, y);
        this.width = width;
        this.height = height;
    }
    
    @Override
    public double calculateArea() {
        return width * height;
    }
    
    @Override
    public double calculatePerimeter() {
        return 2 * (width + height);
    }
    
    @Override
    public void draw() {
        System.out.println("Rysowanie prostokąta " + color + " o wymiarach " + width + "x" + height);
    }
}

// Implementacja dla Circle
public class Circle extends Shape {
    private double radius;
    
    public Circle(String color, double x, double y, double radius) {
        super(color, x, y);
        this.radius = radius;
    }
    
    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
    
    @Override
    public double calculatePerimeter() {
        return 2 * Math.PI * radius;
    }
    
    @Override
    public void draw() {
        System.out.println("Rysowanie koła " + color + " o promieniu " + radius);
    }
}
```

### Method Overloading vs Method Overriding

```java
public class Calculator {
    // Method Overloading - ta sama nazwa, różne parametry
    public int add(int a, int b) {
        return a + b;
    }
    
    public double add(double a, double b) {
        return a + b;
    }
    
    public int add(int a, int b, int c) {
        return a + b + c;
    }
    
    public String add(String a, String b) {
        return a + b;
    }
}

public class ScientificCalculator extends Calculator {
    // Method Overriding - nadpisanie metody z klasy bazowej
    @Override
    public double add(double a, double b) {
        System.out.println("Wykonywanie zaawansowanego dodawania...");
        return super.add(a, b);
    }
    
    // Dodatkowe metody
    public double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }
    
    public double sqrt(double number) {
        return Math.sqrt(number);
    }
}
```

## 🎯 Operator instanceof i Pattern Matching

### Klasyczne Użycie instanceof
```java
public class TypeChecker {
    public static void processAnimal(Animal animal) {
        if (animal instanceof Dog) {
            Dog dog = (Dog) animal;
            System.out.println("To jest pies rasy: " + dog.getBreed());
            dog.wagTail();
        } else if (animal instanceof Cat) {
            Cat cat = (Cat) animal;
            System.out.println("To jest kot");
            cat.climb();
        } else {
            System.out.println("To jest ogólne zwierzę");
        }
    }
    
    // Pattern matching (Java 16+)
    public static void processAnimalModern(Animal animal) {
        if (animal instanceof Dog dog) {
            System.out.println("To jest pies rasy: " + dog.getBreed());
            dog.wagTail();
        } else if (animal instanceof Cat cat) {
            System.out.println("To jest kot");
            cat.climb();
        } else {
            System.out.println("To jest ogólne zwierzę");
        }
    }
}
```

## 🏗️ Przykład Kompleksowy - System Zarządzania Pracownikami

```java
// Klasa bazowa
public abstract class Employee {
    protected String firstName;
    protected String lastName;
    protected int id;
    protected double baseSalary;
    
    public Employee(String firstName, String lastName, int id, double baseSalary) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.id = id;
        this.baseSalary = baseSalary;
    }
    
    // Metoda abstrakcyjna - każdy typ pracownika liczy wynagrodzenie inaczej
    public abstract double calculateSalary();
    
    // Metoda konkretna
    public void displayInfo() {
        System.out.println("ID: " + id + ", Imię: " + firstName + " " + lastName);
        System.out.println("Wynagrodzenie: " + calculateSalary() + " PLN");
    }
    
    public String getFullName() {
        return firstName + " " + lastName;
    }
    
    // Getters
    public int getId() { return id; }
    public double getBaseSalary() { return baseSalary; }
}

// Pracownik etatowy
public class FullTimeEmployee extends Employee {
    private double bonus;
    
    public FullTimeEmployee(String firstName, String lastName, int id, 
                           double baseSalary, double bonus) {
        super(firstName, lastName, id, baseSalary);
        this.bonus = bonus;
    }
    
    @Override
    public double calculateSalary() {
        return baseSalary + bonus;
    }
    
    @Override
    public void displayInfo() {
        super.displayInfo();
        System.out.println("Typ: Pracownik etatowy, Premia: " + bonus + " PLN");
    }
}

// Pracownik na zlecenie
public class ContractEmployee extends Employee {
    private double hourlyRate;
    private int hoursWorked;
    
    public ContractEmployee(String firstName, String lastName, int id, 
                           double hourlyRate, int hoursWorked) {
        super(firstName, lastName, id, 0); // baseSalary = 0
        this.hourlyRate = hourlyRate;
        this.hoursWorked = hoursWorked;
    }
    
    @Override
    public double calculateSalary() {
        return hourlyRate * hoursWorked;
    }
    
    @Override
    public void displayInfo() {
        super.displayInfo();
        System.out.println("Typ: Zleceniobiorca, Stawka: " + hourlyRate + 
                          " PLN/h, Godziny: " + hoursWorked);
    }
    
    public void addHours(int additionalHours) {
        this.hoursWorked += additionalHours;
    }
}

// Manager - rozszerza FullTimeEmployee
public class Manager extends FullTimeEmployee {
    private double managementBonus;
    private int teamSize;
    
    public Manager(String firstName, String lastName, int id, 
                   double baseSalary, double bonus, int teamSize) {
        super(firstName, lastName, id, baseSalary, bonus);
        this.teamSize = teamSize;
        this.managementBonus = teamSize * 500; // 500 PLN za każdego członka zespołu
    }
    
    @Override
    public double calculateSalary() {
        return super.calculateSalary() + managementBonus;
    }
    
    @Override
    public void displayInfo() {
        super.displayInfo();
        System.out.println("Pozycja: Manager, Zespół: " + teamSize + 
                          " osób, Premia za zarządzanie: " + managementBonus + " PLN");
    }
    
    public void manageTeam() {
        System.out.println(getFullName() + " zarządza zespołem " + teamSize + " osób.");
    }
}

// Przykład użycia
public class CompanyDemo {
    public static void main(String[] args) {
        Employee[] employees = {
            new FullTimeEmployee("Anna", "Kowalska", 1, 5000, 1000),
            new ContractEmployee("Piotr", "Nowak", 2, 50, 160),
            new Manager("Maria", "Wiśniewska", 3, 8000, 2000, 5),
            new ContractEmployee("Tomasz", "Kowalczyk", 4, 60, 120)
        };
        
        double totalCost = 0;
        
        System.out.println("=== LISTA PRACOWNIKÓW ===");
        for (Employee emp : employees) {
            emp.displayInfo();
            totalCost += emp.calculateSalary();
            
            // Specjalne działania dla różnych typów
            if (emp instanceof Manager manager) {
                manager.manageTeam();
            } else if (emp instanceof ContractEmployee contractor) {
                System.out.println("Godziny: " + contractor.getHoursWorked());
            }
            
            System.out.println("---");
        }
        
        System.out.println("CAŁKOWITY KOSZT WYNAGRODZEŃ: " + totalCost + " PLN");
    }
}
```

## 🔗 Powiązane Tematy
- [[Java Podstawy]] - Podstawy klas i obiektów
- [[Java Interfejsy i Klasy Abstrakcyjne]] - Dalsze zagadnienia abstrakcji
- [[Java Design Patterns]] - Wzorce wykorzystujące polimorfizm
- [[Java Zaawansowane]] - Generyki i dziedziczenie

## 💡 Najlepsze Praktyki

1. **Używaj `@Override`** - zawsze oznaczaj nadpisywane metody
2. **Preferuj kompozycję nad dziedziczeniem** gdy to możliwe
3. **Projektuj hierarchie klas z góry** - unikaj zbyt głębokich hierarchii
4. **Używaj modyfikatora `protected`** dla pól które powinny być dostępne w podklasach
5. **Testuj polimorfizm** - upewnij się że metody działają poprawnie dla wszystkich typów

## ⚠️ Częste Błędy
- **Zapominanie o wywołaniu `super()`** w konstruktorach
- **Nieprawidłowe castowanie** bez sprawdzenia `instanceof`
- **Nadpisywanie metod `final`** - nie jest możliwe
- **Confusion między overloading a overriding**

---
*Czas nauki: ~25 minut | Poziom: Średniozaawansowany*