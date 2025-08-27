# 🧵 Java - Wielowątkowość - Threading

## 📚 Wprowadzenie
Wielowątkowość (multithreading) w Javie pozwala na równoczesne wykonywanie kilku części programu. Jest kluczowa dla wydajności aplikacji, szczególnie w środowiskach wielordzeniowych i przy operacjach I/O.

## 🔧 Podstawy Thread

### Tworzenie i Uruchamianie Wątków
```java
public class ThreadBasics {
    
    // Sposób 1: Rozszerzanie klasy Thread
    static class MyThread extends Thread {
        private String name;
        
        public MyThread(String name) {
            this.name = name;
        }
        
        @Override
        public void run() {
            for (int i = 1; i <= 5; i++) {
                System.out.println(name + " - iteracja: " + i);
                try {
                    Thread.sleep(1000); // Zatrzymanie na 1 sekundę
                } catch (InterruptedException e) {
                    System.out.println(name + " został przerwany");
                    return;
                }
            }
            System.out.println(name + " zakończony");
        }
    }
    
    // Sposób 2: Implementacja interfejsu Runnable (PREFEROWANY)
    static class MyRunnable implements Runnable {
        private String name;
        
        public MyRunnable(String name) {
            this.name = name;
        }
        
        @Override
        public void run() {
            for (int i = 1; i <= 5; i++) {
                System.out.println(name + " - iteracja: " + i + 
                    " [Thread: " + Thread.currentThread().getName() + "]");
                try {
                    Thread.sleep(800);
                } catch (InterruptedException e) {
                    System.out.println(name + " został przerwany");
                    return;
                }
            }
            System.out.println(name + " zakończony");
        }
    }
    
    public static void demonstrateBasicThreads() {
        System.out.println("=== PODSTAWOWE WĄTKI ===");
        
        // Tworzenie przez rozszerzanie Thread
        MyThread thread1 = new MyThread("Thread-Extend");
        
        // Tworzenie przez Runnable
        Thread thread2 = new Thread(new MyRunnable("Thread-Runnable"));
        
        // Lambda expression (Java 8+)
        Thread thread3 = new Thread(() -> {
            for (int i = 1; i <= 3; i++) {
                System.out.println("Lambda Thread - iteracja: " + i);
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    return;
                }
            }
        });
        
        // Uruchomienie wątków
        thread1.start(); // NIE thread1.run()!
        thread2.start();
        thread3.start();
        
        try {
            // Czekanie na zakończenie wątków
            thread1.join();
            thread2.join();
            thread3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Wszystkie wątki zakończone");
    }
}
```

### Stany Wątków i Lifecycle
```java
public class ThreadLifecycle {
    
    static class StateMonitor {
        public static void printThreadState(Thread thread, String action) {
            System.out.printf("%s - %s: %s%n", 
                action, thread.getName(), thread.getState());
        }
    }
    
    public static void demonstrateThreadStates() {
        Thread worker = new Thread(() -> {
            try {
                System.out.println("Wątek rozpoczął pracę");
                
                // RUNNABLE state
                for (int i = 0; i < 1000000; i++) {
                    Math.sqrt(i); // CPU-intensive work
                }
                
                System.out.println("Przechodząc do stanu TIMED_WAITING");
                Thread.sleep(2000); // TIMED_WAITING state
                
                System.out.println("Wątek zakończył pracę");
            } catch (InterruptedException e) {
                System.out.println("Wątek przerwany");
            }
        }, "WorkerThread");
        
        StateMonitor.printThreadState(worker, "Przed start()"); // NEW
        
        worker.start();
        StateMonitor.printThreadState(worker, "Po start()"); // RUNNABLE
        
        try {
            Thread.sleep(100);
            StateMonitor.printThreadState(worker, "Podczas pracy"); // RUNNABLE
            
            Thread.sleep(2000);
            StateMonitor.printThreadState(worker, "Podczas sleep"); // TIMED_WAITING
            
            worker.join();
            StateMonitor.printThreadState(worker, "Po join()"); // TERMINATED
            
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    
    public static void demonstrateWaitingStates() {
        Object lock = new Object();
        
        Thread waiter = new Thread(() -> {
            synchronized (lock) {
                try {
                    System.out.println("Wątek czeka...");
                    lock.wait(); // WAITING state
                    System.out.println("Wątek został powiadomiony");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }, "WaiterThread");
        
        Thread notifier = new Thread(() -> {
            try {
                Thread.sleep(3000);
                synchronized (lock) {
                    System.out.println("Powiadamianie czekającego wątku");
                    lock.notify();
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }, "NotifierThread");
        
        waiter.start();
        
        try {
            Thread.sleep(1000);
            StateMonitor.printThreadState(waiter, "W trakcie wait()"); // WAITING
            
            notifier.start();
            
            waiter.join();
            notifier.join();
            
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

## 🔒 Synchronizacja

### Synchronized Methods i Blocks
```java
public class SynchronizationDemo {
    
    // Shared resource
    static class Counter {
        private int count = 0;
        
        // Synchronized method
        public synchronized void increment() {
            count++;
        }
        
        // Synchronized method
        public synchronized void decrement() {
            count--;
        }
        
        // Synchronized block
        public void add(int value) {
            synchronized (this) {
                count += value;
            }
        }
        
        public synchronized int getCount() {
            return count;
        }
        
        // Non-synchronized method for comparison
        public void unsafeIncrement() {
            count++; // Race condition possible!
        }
    }
    
    public static void demonstrateSynchronization() {
        Counter counter = new Counter();
        int threadCount = 10;
        int operationsPerThread = 1000;
        
        Thread[] threads = new Thread[threadCount];
        
        // Create threads that increment counter
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    counter.increment();
                }
            }, "Thread-" + i);
        }
        
        long startTime = System.currentTimeMillis();
        
        // Start all threads
        for (Thread thread : threads) {
            thread.start();
        }
        
        // Wait for all threads to complete
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        
        long endTime = System.currentTimeMillis();
        
        System.out.printf("Synchronized - Oczekiwana wartość: %d, Rzeczywista: %d, Czas: %dms%n",
            threadCount * operationsPerThread, counter.getCount(), (endTime - startTime));
    }
    
    public static void demonstrateUnsynchronized() {
        Counter counter = new Counter();
        int threadCount = 10;
        int operationsPerThread = 1000;
        
        Thread[] threads = new Thread[threadCount];
        
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    counter.unsafeIncrement(); // Not synchronized!
                }
            }, "Thread-" + i);
        }
        
        for (Thread thread : threads) {
            thread.start();
        }
        
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        
        System.out.printf("Unsynchronized - Oczekiwana wartość: %d, Rzeczywista: %d%n",
            threadCount * operationsPerThread, counter.getCount());
    }
}
```

### Producer-Consumer Problem
```java
import java.util.LinkedList;
import java.util.Queue;

public class ProducerConsumerDemo {
    
    static class SharedBuffer {
        private Queue<Integer> buffer;
        private int maxSize;
        
        public SharedBuffer(int maxSize) {
            this.buffer = new LinkedList<>();
            this.maxSize = maxSize;
        }
        
        public synchronized void produce(int value) throws InterruptedException {
            while (buffer.size() >= maxSize) {
                System.out.println("Buffer pełny, producer czeka...");
                wait(); // Release lock and wait
            }
            
            buffer.offer(value);
            System.out.println("Wyprodukowano: " + value + " (rozmiar bufora: " + buffer.size() + ")");
            
            notifyAll(); // Notify all waiting consumers
        }
        
        public synchronized int consume() throws InterruptedException {
            while (buffer.isEmpty()) {
                System.out.println("Buffer pusty, consumer czeka...");
                wait(); // Release lock and wait
            }
            
            int value = buffer.poll();
            System.out.println("Skonsumowano: " + value + " (rozmiar bufora: " + buffer.size() + ")");
            
            notifyAll(); // Notify all waiting producers
            return value;
        }
        
        public synchronized int size() {
            return buffer.size();
        }
    }
    
    static class Producer implements Runnable {
        private SharedBuffer buffer;
        private String name;
        
        public Producer(SharedBuffer buffer, String name) {
            this.buffer = buffer;
            this.name = name;
        }
        
        @Override
        public void run() {
            try {
                for (int i = 1; i <= 10; i++) {
                    int value = Integer.parseInt(name.substring(name.length() - 1)) * 100 + i;
                    buffer.produce(value);
                    Thread.sleep(200 + (int)(Math.random() * 300)); // Random delay
                }
            } catch (InterruptedException e) {
                System.out.println(name + " przerwany");
            }
            System.out.println(name + " zakończony");
        }
    }
    
    static class Consumer implements Runnable {
        private SharedBuffer buffer;
        private String name;
        
        public Consumer(SharedBuffer buffer, String name) {
            this.buffer = buffer;
            this.name = name;
        }
        
        @Override
        public void run() {
            try {
                for (int i = 0; i < 10; i++) {
                    int value = buffer.consume();
                    // Process the consumed value
                    Thread.sleep(150 + (int)(Math.random() * 200)); // Random processing time
                }
            } catch (InterruptedException e) {
                System.out.println(name + " przerwany");
            }
            System.out.println(name + " zakończony");
        }
    }
    
    public static void demonstrateProducerConsumer() {
        SharedBuffer buffer = new SharedBuffer(5);
        
        Thread producer1 = new Thread(new Producer(buffer, "Producer-1"));
        Thread producer2 = new Thread(new Producer(buffer, "Producer-2"));
        Thread consumer1 = new Thread(new Consumer(buffer, "Consumer-1"));
        Thread consumer2 = new Thread(new Consumer(buffer, "Consumer-2"));
        
        System.out.println("=== PRODUCER-CONSUMER DEMO ===");
        
        producer1.start();
        producer2.start();
        consumer1.start();
        consumer2.start();
        
        try {
            producer1.join();
            producer2.join();
            consumer1.join();
            consumer2.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Demo zakończone. Pozostało w buforze: " + buffer.size());
    }
}
```

## 🏭 Executor Framework

### Thread Pools
```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ExecutorDemo {
    
    static class Task implements Callable<String> {
        private int taskId;
        private int duration;
        
        public Task(int taskId, int duration) {
            this.taskId = taskId;
            this.duration = duration;
        }
        
        @Override
        public String call() throws Exception {
            String threadName = Thread.currentThread().getName();
            System.out.printf("Zadanie %d rozpoczęte w wątku %s%n", taskId, threadName);
            
            Thread.sleep(duration);
            
            System.out.printf("Zadanie %d zakończone w wątku %s%n", taskId, threadName);
            return "Wynik zadania " + taskId;
        }
    }
    
    public static void demonstrateFixedThreadPool() {
        System.out.println("=== FIXED THREAD POOL ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        try {
            // Submit tasks
            for (int i = 1; i <= 8; i++) {
                executor.submit(new Task(i, 1000 + (int)(Math.random() * 2000)));
            }
            
            // Shutdown executor
            executor.shutdown();
            
            // Wait for tasks to complete
            if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
                System.out.println("Wymuszenie zamknięcia...");
                executor.shutdownNow();
            }
            
        } catch (InterruptedException e) {
            executor.shutdownNow();
            e.printStackTrace();
        }
        
        System.out.println("Fixed Thread Pool zakończony");
    }
    
    public static void demonstrateCachedThreadPool() {
        System.out.println("=== CACHED THREAD POOL ===");
        
        ExecutorService executor = Executors.newCachedThreadPool();
        
        try {
            // Submit many tasks quickly
            for (int i = 1; i <= 20; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    System.out.printf("Cached Task %d w wątku %s%n", 
                        taskId, Thread.currentThread().getName());
                    try {
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }
            
            executor.shutdown();
            executor.awaitTermination(5, TimeUnit.SECONDS);
            
        } catch (InterruptedException e) {
            executor.shutdownNow();
            e.printStackTrace();
        }
        
        System.out.println("Cached Thread Pool zakończony");
    }
    
    public static void demonstrateScheduledExecutor() {
        System.out.println("=== SCHEDULED EXECUTOR ===");
        
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
        
        try {
            AtomicInteger counter = new AtomicInteger(0);
            
            // Schedule with fixed delay
            ScheduledFuture<?> periodicTask = scheduler.scheduleWithFixedDelay(() -> {
                int count = counter.incrementAndGet();
                System.out.println("Zadanie okresowe #" + count + " w " + 
                    Thread.currentThread().getName());
                
                if (count >= 5) {
                    System.out.println("Zatrzymanie zadania okresowego");
                    throw new RuntimeException("Stop"); // Stop the task
                }
            }, 1, 2, TimeUnit.SECONDS); // Initial delay: 1s, Period: 2s
            
            // Schedule one-time task
            scheduler.schedule(() -> {
                System.out.println("Zadanie jednorazowe wykonane");
            }, 3, TimeUnit.SECONDS);
            
            // Wait for completion
            Thread.sleep(15000);
            
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            scheduler.shutdown();
            try {
                if (!scheduler.awaitTermination(2, TimeUnit.SECONDS)) {
                    scheduler.shutdownNow();
                }
            } catch (InterruptedException e) {
                scheduler.shutdownNow();
            }
        }
    }
    
    public static void demonstrateFutureAndCallable() {
        System.out.println("=== FUTURE AND CALLABLE ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        try {
            // Submit Callable tasks and get Futures
            Future<String> future1 = executor.submit(new Task(1, 2000));
            Future<String> future2 = executor.submit(new Task(2, 1000));
            Future<String> future3 = executor.submit(new Task(3, 3000));
            
            // Get results (blocking calls)
            System.out.println("Oczekiwanie na wyniki...");
            
            String result1 = future1.get(5, TimeUnit.SECONDS);
            String result2 = future2.get(5, TimeUnit.SECONDS);
            String result3 = future3.get(5, TimeUnit.SECONDS);
            
            System.out.println("Wynik 1: " + result1);
            System.out.println("Wynik 2: " + result2);
            System.out.println("Wynik 3: " + result3);
            
            // CompletionService for processing results as they complete
            CompletionService<String> completionService = new ExecutorCompletionService<>(executor);
            
            for (int i = 4; i <= 6; i++) {
                completionService.submit(new Task(i, 1000 + i * 500));
            }
            
            // Process results as they complete
            for (int i = 0; i < 3; i++) {
                Future<String> completed = completionService.take();
                System.out.println("Otrzymano wynik: " + completed.get());
            }
            
        } catch (InterruptedException | ExecutionException | TimeoutException e) {
            e.printStackTrace();
        } finally {
            executor.shutdown();
        }
    }
}
```

## ⚡ Concurrent Collections

```java
import java.util.concurrent.*;

public class ConcurrentCollectionsDemo {
    
    public static void demonstrateConcurrentHashMap() {
        System.out.println("=== CONCURRENT HASH MAP ===");
        
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        
        // Thread-safe operations
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Writers
        for (int i = 1; i <= 10; i++) {
            final int value = i;
            executor.submit(() -> {
                map.put("key" + value, value);
                System.out.println("Put: key" + value + " = " + value);
            });
        }
        
        // Readers
        for (int i = 1; i <= 5; i++) {
            final int key = i;
            executor.submit(() -> {
                Integer value = map.get("key" + key);
                System.out.println("Get: key" + key + " = " + value);
            });
        }
        
        // Atomic operations
        executor.submit(() -> {
            map.compute("counter", (key, val) -> val == null ? 1 : val + 1);
            System.out.println("Computed counter: " + map.get("counter"));
        });
        
        executor.submit(() -> {
            map.merge("sum", 10, Integer::sum);
            System.out.println("Merged sum: " + map.get("sum"));
        });
        
        executor.shutdown();
        try {
            executor.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Final map: " + map);
    }
    
    public static void demonstrateBlockingQueue() {
        System.out.println("=== BLOCKING QUEUE ===");
        
        BlockingQueue<String> queue = new ArrayBlockingQueue<>(5);
        
        // Producer
        Thread producer = new Thread(() -> {
            try {
                for (int i = 1; i <= 10; i++) {
                    String item = "Item-" + i;
                    queue.put(item); // Blocks if queue is full
                    System.out.println("Produced: " + item + " (queue size: " + queue.size() + ")");
                    Thread.sleep(200);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Consumer
        Thread consumer = new Thread(() -> {
            try {
                while (true) {
                    String item = queue.take(); // Blocks if queue is empty
                    System.out.println("Consumed: " + item + " (queue size: " + queue.size() + ")");
                    Thread.sleep(500); // Slower than producer
                    
                    if (item.equals("Item-10")) {
                        break;
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        consumer.start();
        
        try {
            producer.join();
            consumer.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    
    public static void demonstrateCopyOnWriteArrayList() {
        System.out.println("=== COPY ON WRITE ARRAY LIST ===");
        
        CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
        
        // Add initial data
        list.add("Element-1");
        list.add("Element-2");
        list.add("Element-3");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Reader thread (iterates safely even during modifications)
        executor.submit(() -> {
            for (int i = 0; i < 10; i++) {
                System.out.println("Reading iteration " + (i + 1) + ":");
                for (String element : list) {
                    System.out.println("  " + element);
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        return;
                    }
                }
                System.out.println();
            }
        });
        
        // Writer threads
        executor.submit(() -> {
            try {
                for (int i = 4; i <= 6; i++) {
                    Thread.sleep(800);
                    list.add("Element-" + i);
                    System.out.println("Added Element-" + i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        executor.submit(() -> {
            try {
                Thread.sleep(2000);
                list.remove("Element-2");
                System.out.println("Removed Element-2");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        executor.shutdown();
        try {
            executor.awaitTermination(15, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Final list: " + list);
    }
}
```

## 🔢 Atomic Variables

```java
import java.util.concurrent.atomic.*;

public class AtomicVariablesDemo {
    
    private static AtomicInteger atomicCounter = new AtomicInteger(0);
    private static AtomicLong atomicLong = new AtomicLong(0);
    private static AtomicReference<String> atomicString = new AtomicReference<>("initial");
    
    public static void demonstrateAtomicInteger() {
        System.out.println("=== ATOMIC INTEGER ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        // Multiple threads incrementing atomically
        for (int i = 0; i < 10; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    int oldValue = atomicCounter.getAndIncrement();
                    
                    if (j % 250 == 0) {
                        System.out.printf("Thread %d: %d -> %d%n", 
                            threadId, oldValue, atomicCounter.get());
                    }
                }
            });
        }
        
        executor.shutdown();
        try {
            executor.awaitTermination(10, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Final atomic counter value: " + atomicCounter.get());
        System.out.println("Expected: " + (10 * 1000));
    }
    
    public static void demonstrateAtomicOperations() {
        System.out.println("=== ATOMIC OPERATIONS ===");
        
        AtomicInteger counter = new AtomicInteger(0);
        
        // Compare and set
        boolean updated = counter.compareAndSet(0, 10);
        System.out.println("CAS 0->10: " + updated + ", value: " + counter.get());
        
        // Get and set
        int oldValue = counter.getAndSet(20);
        System.out.println("Get and set to 20, old value: " + oldValue + ", new value: " + counter.get());
        
        // Increment and get
        int newValue = counter.incrementAndGet();
        System.out.println("After increment: " + newValue);
        
        // Add and get
        newValue = counter.addAndGet(5);
        System.out.println("After add 5: " + newValue);
        
        // Update with function
        counter.updateAndGet(val -> val * 2);
        System.out.println("After multiply by 2: " + counter.get());
        
        // Accumulate
        counter.accumulateAndGet(3, (current, update) -> current + update * 2);
        System.out.println("After accumulate (current + 3*2): " + counter.get());
    }
    
    public static void demonstrateAtomicReference() {
        System.out.println("=== ATOMIC REFERENCE ===");
        
        AtomicReference<StringBuilder> atomicStringBuilder = 
            new AtomicReference<>(new StringBuilder("Start"));
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        for (int i = 1; i <= 3; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 0; j < 5; j++) {
                    atomicStringBuilder.updateAndGet(sb -> {
                        sb.append(" T").append(threadId).append("_").append(j);
                        return sb;
                    });
                    
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        return;
                    }
                }
            });
        }
        
        executor.shutdown();
        try {
            executor.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Final string: " + atomicStringBuilder.get().toString());
    }
    
    // Lock-free stack implementation using AtomicReference
    static class LockFreeStack<T> {
        private static class Node<T> {
            T data;
            Node<T> next;
            
            Node(T data, Node<T> next) {
                this.data = data;
                this.next = next;
            }
        }
        
        private final AtomicReference<Node<T>> head = new AtomicReference<>();
        
        public void push(T item) {
            Node<T> newNode = new Node<>(item, null);
            Node<T> currentHead;
            
            do {
                currentHead = head.get();
                newNode.next = currentHead;
            } while (!head.compareAndSet(currentHead, newNode));
        }
        
        public T pop() {
            Node<T> currentHead;
            Node<T> newHead;
            
            do {
                currentHead = head.get();
                if (currentHead == null) {
                    return null;
                }
                newHead = currentHead.next;
            } while (!head.compareAndSet(currentHead, newHead));
            
            return currentHead.data;
        }
        
        public boolean isEmpty() {
            return head.get() == null;
        }
    }
    
    public static void demonstrateLockFreeStack() {
        System.out.println("=== LOCK-FREE STACK ===");
        
        LockFreeStack<Integer> stack = new LockFreeStack<>();
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Pushers
        for (int i = 1; i <= 2; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 1; j <= 10; j++) {
                    int value = threadId * 100 + j;
                    stack.push(value);
                    System.out.println("Pushed: " + value);
                    try {
                        Thread.sleep(50);
                    } catch (InterruptedException e) {
                        return;
                    }
                }
            });
        }
        
        // Poppers
        for (int i = 1; i <= 2; i++) {
            executor.submit(() -> {
                try {
                    Thread.sleep(200); // Let some items be pushed first
                    
                    for (int j = 1; j <= 8; j++) {
                        Integer value = stack.pop();
                        if (value != null) {
                            System.out.println("Popped: " + value);
                        } else {
                            System.out.println("Stack empty");
                        }
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        try {
            executor.awaitTermination(10, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        System.out.println("Stack empty: " + stack.isEmpty());
        
        // Pop remaining items
        Integer remaining;
        while ((remaining = stack.pop()) != null) {
            System.out.println("Remaining: " + remaining);
        }
    }
}
```

## 🔗 Powiązane Tematy
- [[Java Stream API - Pełny Przewodnik]] - Parallel streams
- [[Java Memory Management i Garbage Collection]] - Thread memory model
- [[Spring Boot Web]] - Thread pools w aplikacjach web
- [[Java Performance i Optymalizacja]] - Thread performance

## 💡 Najlepsze Praktyki

1. **Preferuj Executor Framework** nad tworzeniem Thread bezpośrednio
2. **Używaj thread-safe collections** zamiast synchronizacji ręcznej
3. **Unikaj deadlocków** - zawsze acquire locks w tej samej kolejności
4. **Minimalizuj synchronized sections** - tylko krytyczne sekcje
5. **Używaj atomic variables** dla prostych operacji
6. **Stosuj immutable objects** gdy to możliwe
7. **Handle InterruptedException** poprawnie

## ⚠️ Częste Pułapki

1. **Race conditions** - niesynchronizowany dostęp do shared state
2. **Deadlocks** - circular waiting for locks
3. **Memory consistency errors** - changes not visible across threads
4. **Thread leaks** - nie zamknięte ExecutorService
5. **Busy waiting** - zamiast blocking operations

---
*Czas nauki: ~35 minut | Poziom: Zaawansowany*