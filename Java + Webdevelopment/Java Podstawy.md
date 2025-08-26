# 🔰 Java - Podstawowe Koncepcje

## 🏗️ Programowanie Obiektowe (OOP)

### 📋 Cztery Filary OOP
1. **Enkapsulacja** - ukrywanie implementacji
2. **Dziedziczenie** - rozszerzanie klas
3. **Polimorfizm** - wiele form tego samego obiektu
4. **Abstrakcja** - upraszczanie złożoności

```java
// Przykład klasy z enkapsulacją
public class Uzytkownik {
    private String imie;
    private String email;
    
    // Konstruktor
    public Uzytkownik(String imie, String email) {
        this.imie = imie;
        this.email = email;
    }
    
    // Gettery i settery
    public String getImie() { return imie; }
    public void setImie(String imie) { this.imie = imie; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

### 🔄 Dziedziczenie i Interfejsy

```java
// Klasa bazowa
public abstract class Pojazd {
    protected String marka;
    
    public abstract void uruchom();
}

// Dziedziczenie
public class Samochod extends Pojazd {
    private int liczbaDrzwi;
    
    @Override
    public void uruchom() {
        System.out.println("Samochód " + marka + " został uruchomiony");
    }
}

// Interfejs
public interface Silnik {
    void zaplon();
    void wylacz();
}
```

## 📦 Kolekcje Java

### 🗂️ Najważniejsze Typy Kolekcji

```java
import java.util.*;

// Lista - zachowuje kolejność, pozwala duplikaty
List<String> lista = new ArrayList<>();
lista.add("Java");
lista.add("Python");
lista.add("Java"); // duplikat OK

// Set - unikalne elementy
Set<String> zbior = new HashSet<>();
zbior.add("Java");
zbior.add("Python");
zbior.add("Java"); // zostanie zignorowane

// Mapa - pary klucz-wartość
Map<String, Integer> mapa = new HashMap<>();
mapa.put("Java", 25);
mapa.put("Python", 30);

// Iteracja przez mapę
for (Map.Entry<String, Integer> entry : mapa.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
```

### 🔍 Operacje na Kolekcjach

```java
List<Integer> liczby = Arrays.asList(1, 2, 3, 4, 5);

// Sprawdzenie czy zawiera element
boolean zawiera = liczby.contains(3);

// Rozmiar kolekcji
int rozmiar = liczby.size();

// Sprawdzenie czy pusta
boolean pusta = liczby.isEmpty();

// Usunięcie elementu
lista.remove("Java"); // usuwa pierwsze wystąpienie
```

## ⚠️ Obsługa Wyjątków

### 🎯 Try-Catch-Finally

```java
public void odczytajPlik(String sciezka) {
    try {
        FileReader plik = new FileReader(sciezka);
        // operacje na pliku
        
    } catch (FileNotFoundException e) {
        System.out.println("Plik nie został znaleziony: " + e.getMessage());
        
    } catch (IOException e) {
        System.out.println("Błąd I/O: " + e.getMessage());
        
    } finally {
        // kod wykonywany zawsze
        System.out.println("Sprzątanie zasobów");
    }
}
```

### 🚀 Try-with-resources (Java 7+)

```java
// Automatyczne zamykanie zasobów
public String odczytajPlikJakoString(String sciezka) {
    try (BufferedReader reader = Files.newBufferedReader(Paths.get(sciezka))) {
        return reader.lines()
                    .collect(Collectors.joining("\n"));
    } catch (IOException e) {
        throw new RuntimeException("Nie można odczytać pliku", e);
    }
}
```

### 📋 Własne Wyjątki

```java
// Własny wyjątek
public class UzytkownikNieZnalezionyException extends Exception {
    public UzytkownikNieZnalezionyException(String wiadomosc) {
        super(wiadomosc);
    }
}

// Użycie
public Uzytkownik znajdzUzytkownika(String email) throws UzytkownikNieZnalezionyException {
    // logika wyszukiwania
    if (uzytkownik == null) {
        throw new UzytkownikNieZnalezionyException("Użytkownik z email " + email + " nie istnieje");
    }
    return uzytkownik;
}
```

## 🧵 Podstawy Wielowątkowości

```java
// Implementacja Runnable
public class MojeZadanie implements Runnable {
    @Override
    public void run() {
        System.out.println("Wykonywane w wątku: " + Thread.currentThread().getName());
    }
}

// Tworzenie i uruchamianie wątku
Thread watek = new Thread(new MojeZadanie());
watek.start();

// Lambda expression (Java 8+)
Thread watek2 = new Thread(() -> {
    System.out.println("Lambda w wątku: " + Thread.currentThread().getName());
});
watek2.start();
```

---

## 🔗 Następny Krok
[[Java Zaawansowane|🚀 Java - Koncepcje Zaawansowane]] - generyki, streams, lambda expressions

---
*Czas nauki: ~15 minut*