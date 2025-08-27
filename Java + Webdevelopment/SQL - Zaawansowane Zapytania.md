# 🗄️ SQL - Zaawansowane Zapytania

## 📚 Wprowadzenie
SQL (Structured Query Language) to standardowy język do zarządzania relacyjnymi bazami danych. Ta notatka pokrywa zaawansowane koncepty SQL używane w profesjonalnych aplikacjach Java, ze szczególnym uwzględnieniem integracji z JPA/Hibernate.

## 🏗️ DDL - Data Definition Language

### Tworzenie Tabel z Constraints
```sql
-- Tworzenie bazy danych
CREATE DATABASE ecommerce_db;
USE ecommerce_db;

-- Tabela użytkowników
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    
    -- Constraints
    CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT chk_age CHECK (date_of_birth IS NULL OR date_of_birth <= CURDATE() - INTERVAL 13 YEAR),
    
    -- Indexes
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    INDEX idx_last_login (last_login)
);

-- Tabela kategorii produktów
CREATE TABLE categories (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_category_id BIGINT,
    slug VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (parent_category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_parent_category (parent_category_id),
    INDEX idx_slug (slug)
);

-- Tabela produktów
CREATE TABLE products (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2),
    sku VARCHAR(100) NOT NULL UNIQUE,
    category_id BIGINT NOT NULL,
    stock_quantity INT DEFAULT 0,
    min_stock_level INT DEFAULT 0,
    weight DECIMAL(8,3),
    dimensions VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (category_id) REFERENCES categories(id),
    
    CONSTRAINT chk_price_positive CHECK (price > 0),
    CONSTRAINT chk_cost_price_positive CHECK (cost_price IS NULL OR cost_price >= 0),
    CONSTRAINT chk_stock_non_negative CHECK (stock_quantity >= 0),
    
    INDEX idx_category (category_id),
    INDEX idx_sku (sku),
    INDEX idx_price (price),
    INDEX idx_stock (stock_quantity),
    FULLTEXT idx_name_description (name, description)
);

-- Tabela zamówień
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    order_number VARCHAR(20) NOT NULL UNIQUE,
    status ENUM('PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED') DEFAULT 'PENDING',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ship_date TIMESTAMP NULL,
    delivery_date TIMESTAMP NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    shipping_cost DECIMAL(8,2) DEFAULT 0,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    
    -- Shipping address
    shipping_address_line1 VARCHAR(200),
    shipping_address_line2 VARCHAR(200),
    shipping_city VARCHAR(100),
    shipping_state VARCHAR(100),
    shipping_postal_code VARCHAR(20),
    shipping_country VARCHAR(100) DEFAULT 'Poland',
    
    -- Payment info
    payment_method VARCHAR(50),
    payment_status ENUM('PENDING', 'COMPLETED', 'FAILED', 'REFUNDED') DEFAULT 'PENDING',
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    
    CONSTRAINT chk_amounts_positive CHECK (
        subtotal >= 0 AND 
        tax_amount >= 0 AND 
        shipping_cost >= 0 AND 
        discount_amount >= 0 AND 
        total_amount >= 0
    ),
    
    INDEX idx_user (user_id),
    INDEX idx_order_number (order_number),
    INDEX idx_status (status),
    INDEX idx_order_date (order_date),
    INDEX idx_payment_status (payment_status)
);

-- Tabela szczegółów zamówienia
CREATE TABLE order_items (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(12,2) NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    
    CONSTRAINT chk_quantity_positive CHECK (quantity > 0),
    CONSTRAINT chk_unit_price_positive CHECK (unit_price > 0),
    CONSTRAINT chk_total_price_positive CHECK (total_price > 0),
    
    INDEX idx_order (order_id),
    INDEX idx_product (product_id),
    UNIQUE KEY unique_order_product (order_id, product_id)
);
```

### Indexes i Performance
```sql
-- Composite indexes dla często używanych zapytań
CREATE INDEX idx_products_category_price ON products(category_id, price);
CREATE INDEX idx_products_active_stock ON products(is_active, stock_quantity);
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);
CREATE INDEX idx_orders_status_date ON orders(status, order_date);

-- Partial index (dla MySQL 8.0+)
CREATE INDEX idx_active_products ON products(name, price) WHERE is_active = TRUE;

-- Functional index
CREATE INDEX idx_user_email_lower ON users((LOWER(email)));

-- Covering index
CREATE INDEX idx_product_summary ON products(category_id, price, stock_quantity, is_active);
```

## 📊 DML - Data Manipulation Language

### Complex INSERT Operations
```sql
-- Bulk insert z danymi testowymi
INSERT INTO users (username, email, password_hash, first_name, last_name, date_of_birth) VALUES
('john_doe', 'john.doe@example.com', '$2a$10$N9qo8uLOickgx2ZMRZoMye', 'John', 'Doe', '1990-05-15'),
('jane_smith', 'jane.smith@example.com', '$2a$10$N9qo8uLOickgx2ZMRZoMye', 'Jane', 'Smith', '1985-03-22'),
('bob_wilson', 'bob.wilson@example.com', '$2a$10$N9qo8uLOickgx2ZMRZoMye', 'Bob', 'Wilson', '1992-11-08'),
('alice_brown', 'alice.brown@example.com', '$2a$10$N9qo8uLOickgx2ZMRZoMye', 'Alice', 'Brown', '1988-07-30');

-- Insert z subquery
INSERT INTO categories (name, description, slug)
SELECT 
    CONCAT('Category ', ROW_NUMBER() OVER()) as name,
    CONCAT('Description for category ', ROW_NUMBER() OVER()) as description,
    CONCAT('category-', ROW_NUMBER() OVER()) as slug
FROM (SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) t;

-- Insert on duplicate key update (MySQL)
INSERT INTO products (name, sku, price, category_id, stock_quantity)
VALUES ('Laptop Pro', 'LAP001', 1299.99, 1, 10)
ON DUPLICATE KEY UPDATE 
    price = VALUES(price),
    stock_quantity = stock_quantity + VALUES(stock_quantity),
    updated_at = CURRENT_TIMESTAMP;

-- UPSERT using MERGE (SQL Standard - dostępne w PostgreSQL, SQL Server)
MERGE products AS target
USING (VALUES ('LAP001', 'Laptop Pro Updated', 1399.99)) AS source (sku, name, price)
ON target.sku = source.sku
WHEN MATCHED THEN
    UPDATE SET name = source.name, price = source.price, updated_at = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN
    INSERT (sku, name, price, category_id) VALUES (source.sku, source.name, source.price, 1);
```

### Advanced UPDATE Operations
```sql
-- Update z JOIN
UPDATE products p
JOIN categories c ON p.category_id = c.id
SET p.name = CONCAT(c.name, ' - ', p.name)
WHERE c.name = 'Electronics' AND p.name NOT LIKE 'Electronics -%';

-- Update z subquery
UPDATE products 
SET stock_quantity = (
    SELECT COALESCE(SUM(quantity), 0)
    FROM inventory_movements 
    WHERE product_id = products.id 
    AND movement_type = 'IN'
) - (
    SELECT COALESCE(SUM(quantity), 0)
    FROM inventory_movements 
    WHERE product_id = products.id 
    AND movement_type = 'OUT'
);

-- Conditional update
UPDATE orders 
SET status = CASE 
    WHEN DATEDIFF(CURRENT_DATE, order_date) > 30 AND status = 'PENDING' THEN 'CANCELLED'
    WHEN ship_date IS NOT NULL AND status = 'PROCESSING' THEN 'SHIPPED'
    WHEN delivery_date IS NOT NULL AND status = 'SHIPPED' THEN 'DELIVERED'
    ELSE status
END
WHERE status IN ('PENDING', 'PROCESSING', 'SHIPPED');
```

## 🔍 Advanced SELECT Queries

### Window Functions
```sql
-- Ranking produktów według ceny w każdej kategorii
SELECT 
    p.id,
    p.name,
    c.name as category_name,
    p.price,
    ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY p.price DESC) as price_rank,
    RANK() OVER (PARTITION BY p.category_id ORDER BY p.price DESC) as price_rank_with_ties,
    DENSE_RANK() OVER (PARTITION BY p.category_id ORDER BY p.price DESC) as dense_price_rank,
    PERCENT_RANK() OVER (PARTITION BY p.category_id ORDER BY p.price) as price_percentile
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = TRUE
ORDER BY c.name, p.price DESC;

-- Running totals i moving averages
SELECT 
    DATE(order_date) as order_date,
    COUNT(*) as daily_orders,
    SUM(total_amount) as daily_revenue,
    
    -- Running total
    SUM(SUM(total_amount)) OVER (ORDER BY DATE(order_date)) as cumulative_revenue,
    
    -- Moving average (7-day window)
    AVG(SUM(total_amount)) OVER (
        ORDER BY DATE(order_date) 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7day,
    
    -- Comparison with previous day
    LAG(SUM(total_amount), 1) OVER (ORDER BY DATE(order_date)) as prev_day_revenue,
    SUM(total_amount) - LAG(SUM(total_amount), 1) OVER (ORDER BY DATE(order_date)) as revenue_change
    
FROM orders 
WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
GROUP BY DATE(order_date)
ORDER BY order_date;

-- Top N per group
WITH ranked_products AS (
    SELECT 
        p.*,
        c.name as category_name,
        ROW_NUMBER() OVER (PARTITION BY p.category_id ORDER BY p.price DESC) as rn
    FROM products p
    JOIN categories c ON p.category_id = c.id
    WHERE p.is_active = TRUE
)
SELECT * 
FROM ranked_products 
WHERE rn <= 3;  -- Top 3 najdroższych produktów w każdej kategorii
```

### Common Table Expressions (CTE)
```sql
-- Recursive CTE - hierarchia kategorii
WITH RECURSIVE category_hierarchy AS (
    -- Base case: kategorie główne
    SELECT 
        id,
        name,
        parent_category_id,
        0 as level,
        name as path
    FROM categories 
    WHERE parent_category_id IS NULL
    
    UNION ALL
    
    -- Recursive case: podkategorie
    SELECT 
        c.id,
        c.name,
        c.parent_category_id,
        ch.level + 1,
        CONCAT(ch.path, ' > ', c.name)
    FROM categories c
    JOIN category_hierarchy ch ON c.parent_category_id = ch.id
)
SELECT 
    id,
    name,
    level,
    path,
    REPEAT('  ', level) || name as indented_name
FROM category_hierarchy
ORDER BY path;

-- Multiple CTEs - analiza klientów
WITH monthly_stats AS (
    SELECT 
        user_id,
        DATE_FORMAT(order_date, '%Y-%m') as month,
        COUNT(*) as order_count,
        SUM(total_amount) as total_spent
    FROM orders 
    WHERE order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
    GROUP BY user_id, DATE_FORMAT(order_date, '%Y-%m')
),
customer_segments AS (
    SELECT 
        user_id,
        AVG(order_count) as avg_monthly_orders,
        AVG(total_spent) as avg_monthly_spent,
        SUM(total_spent) as total_yearly_spent,
        CASE 
            WHEN SUM(total_spent) > 5000 THEN 'VIP'
            WHEN SUM(total_spent) > 1000 THEN 'Premium'
            WHEN SUM(total_spent) > 100 THEN 'Regular'
            ELSE 'Occasional'
        END as segment
    FROM monthly_stats
    GROUP BY user_id
)
SELECT 
    u.id,
    u.username,
    u.email,
    cs.avg_monthly_orders,
    cs.avg_monthly_spent,
    cs.total_yearly_spent,
    cs.segment,
    
    -- Ostatnie zamówienie
    (SELECT MAX(order_date) FROM orders WHERE user_id = u.id) as last_order_date,
    
    -- Liczba dni od ostatniego zamówienia
    DATEDIFF(CURRENT_DATE, (SELECT MAX(order_date) FROM orders WHERE user_id = u.id)) as days_since_last_order
    
FROM users u
JOIN customer_segments cs ON u.id = cs.user_id
ORDER BY cs.total_yearly_spent DESC;
```

### Advanced Aggregations
```sql
-- ROLLUP - podsumowania hierarchiczne
SELECT 
    COALESCE(c.name, 'TOTAL') as category,
    COALESCE(DATE_FORMAT(o.order_date, '%Y-%m'), 'ALL_MONTHS') as month,
    COUNT(*) as order_count,
    SUM(oi.total_price) as revenue
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE o.order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
GROUP BY c.name, DATE_FORMAT(o.order_date, '%Y-%m')
WITH ROLLUP
ORDER BY 
    CASE WHEN c.name IS NULL THEN 1 ELSE 0 END,
    c.name,
    CASE WHEN DATE_FORMAT(o.order_date, '%Y-%m') IS NULL THEN 1 ELSE 0 END,
    month;

-- CUBE - wszystkie możliwe kombinacje grupowania
SELECT 
    COALESCE(c.name, 'ALL_CATEGORIES') as category,
    COALESCE(o.status, 'ALL_STATUSES') as status,
    COALESCE(DATE_FORMAT(o.order_date, '%Y-%m'), 'ALL_MONTHS') as month,
    COUNT(*) as count,
    AVG(o.total_amount) as avg_amount
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE o.order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 3 MONTH)
GROUP BY CUBE(c.name, o.status, DATE_FORMAT(o.order_date, '%Y-%m'));

-- GROUPING SETS - niestandardowe grupowania
SELECT 
    category_id,
    YEAR(created_at) as year,
    MONTH(created_at) as month,
    COUNT(*) as product_count,
    AVG(price) as avg_price,
    
    -- Identyfikacja poziomu grupowania
    GROUPING(category_id) as is_category_total,
    GROUPING(YEAR(created_at)) as is_year_total,
    GROUPING(MONTH(created_at)) as is_month_total
    
FROM products 
GROUP BY GROUPING SETS (
    (category_id, YEAR(created_at), MONTH(created_at)),  -- Szczegółowe
    (category_id, YEAR(created_at)),                     -- Roczne per kategoria
    (YEAR(created_at), MONTH(created_at)),               -- Miesięczne ogółem
    (category_id),                                       -- Per kategoria ogółem
    ()                                                   -- Grand total
);
```

## 🔗 Joins i Subqueries

### Advanced JOIN Techniques
```sql
-- Self-join dla hierarchii
SELECT 
    c1.name as category,
    c2.name as parent_category,
    c3.name as grandparent_category
FROM categories c1
LEFT JOIN categories c2 ON c1.parent_category_id = c2.id
LEFT JOIN categories c3 ON c2.parent_category_id = c3.id;

-- LATERAL JOIN (PostgreSQL) / APPLY (SQL Server)
SELECT 
    u.username,
    u.email,
    recent_orders.*
FROM users u
CROSS JOIN LATERAL (
    SELECT 
        o.id,
        o.order_number,
        o.total_amount,
        o.order_date
    FROM orders o
    WHERE o.user_id = u.id
    ORDER BY o.order_date DESC
    LIMIT 3
) recent_orders;

-- Multiple table joins z agregacją
SELECT 
    u.id,
    u.username,
    u.email,
    
    -- Statystyki zamówień
    COUNT(DISTINCT o.id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    
    -- Statystyki produktów
    COUNT(DISTINCT oi.product_id) as unique_products_ordered,
    SUM(oi.quantity) as total_items_ordered,
    
    -- Ulubiona kategoria
    (
        SELECT c.name
        FROM order_items oi2
        JOIN orders o2 ON oi2.order_id = o2.id
        JOIN products p2 ON oi2.product_id = p2.id
        JOIN categories c ON p2.category_id = c.id
        WHERE o2.user_id = u.id
        GROUP BY c.id, c.name
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ) as favorite_category
    
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
LEFT JOIN order_items oi ON o.id = oi.order_id
WHERE u.is_active = TRUE
GROUP BY u.id, u.username, u.email
HAVING COUNT(DISTINCT o.id) > 0  -- Tylko klienci z zamówieniami
ORDER BY total_spent DESC;
```

### Subqueries i EXISTS
```sql
-- Korelowany subquery
SELECT 
    p.id,
    p.name,
    p.price,
    p.stock_quantity,
    (
        SELECT COUNT(*)
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        WHERE oi.product_id = p.id
        AND o.order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
    ) as orders_last_30_days
FROM products p
WHERE p.is_active = TRUE
ORDER BY orders_last_30_days DESC;

-- EXISTS vs IN performance comparison
-- EXISTS - zazwyczaj szybsze dla dużych tabel
SELECT u.id, u.username, u.email
FROM users u
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.user_id = u.id 
    AND o.total_amount > 500
);

-- IN - może być wolniejsze
SELECT u.id, u.username, u.email
FROM users u
WHERE u.id IN (
    SELECT DISTINCT o.user_id 
    FROM orders o 
    WHERE o.total_amount > 500
);

-- NOT EXISTS - znajdź użytkowników bez zamówień w ostatnim roku
SELECT u.id, u.username, u.email, u.created_at
FROM users u
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.user_id = u.id
    AND o.order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 1 YEAR)
)
AND u.is_active = TRUE;

-- Scalar subqueries w SELECT
SELECT 
    o.id,
    o.order_number,
    o.total_amount,
    o.status,
    
    -- Ilość pozycji w zamówieniu
    (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.id) as item_count,
    
    -- Nazwa głównej kategorii najdroższego produktu
    (
        SELECT c.name
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        JOIN categories c ON p.category_id = c.id
        WHERE oi.order_id = o.id
        ORDER BY oi.unit_price DESC
        LIMIT 1
    ) as top_category,
    
    -- Procent wartości zamówienia względem wszystkich zamówień użytkownika
    ROUND(
        o.total_amount / (
            SELECT SUM(total_amount) 
            FROM orders o2 
            WHERE o2.user_id = o.user_id
        ) * 100, 
        2
    ) as percentage_of_user_total
    
FROM orders o
WHERE o.status = 'DELIVERED'
ORDER BY o.order_date DESC;
```

## 📈 Performance Optimization

### Query Optimization Techniques
```sql
-- 1. Index Hints (MySQL)
SELECT /*+ USE_INDEX(products, idx_category_price) */
    p.name, p.price
FROM products p
WHERE p.category_id = 1 
AND p.price BETWEEN 100 AND 1000;

-- 2. EXPLAIN PLAN analysis
EXPLAIN ANALYZE
SELECT 
    u.username,
    COUNT(o.id) as order_count,
    SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2023-01-01'
GROUP BY u.id, u.username
HAVING COUNT(o.id) > 5
ORDER BY total_spent DESC;

-- 3. Partitioning-friendly queries
-- Zapytanie wykorzystujące partition pruning
SELECT *
FROM orders_partitioned
WHERE order_date >= '2023-01-01' 
AND order_date < '2023-02-01'  -- Partition elimination
AND status = 'DELIVERED';

-- 4. Materialized views / Summary tables
CREATE VIEW monthly_sales_summary AS
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') as month,
    COUNT(*) as order_count,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_order_value,
    COUNT(DISTINCT user_id) as unique_customers
FROM orders
WHERE status IN ('DELIVERED', 'SHIPPED')
GROUP BY DATE_FORMAT(order_date, '%Y-%m');

-- 5. Batch processing patterns
-- Bezpieczny batch delete
DELETE FROM audit_logs 
WHERE created_at < DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY)
LIMIT 1000;  -- Powtarzaj aż nie będzie więcej rekordów

-- Batch update z chunks
UPDATE products 
SET updated_at = CURRENT_TIMESTAMP 
WHERE id BETWEEN 1000 AND 1999  -- Process in chunks
AND is_active = TRUE;
```

### Database Maintenance
```sql
-- Table statistics update
ANALYZE TABLE products, orders, order_items;

-- Index maintenance
-- Sprawdź fragmentację indeksów
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    STAT_VALUE as fragmentation_percent
FROM mysql.innodb_index_stats 
WHERE STAT_NAME = 'n_page_split';

-- Reorganize indexes (MySQL)
ALTER TABLE products ENGINE=InnoDB;

-- Optimize table
OPTIMIZE TABLE products;

-- Check table integrity
CHECK TABLE products EXTENDED;

-- Repair table (jeśli potrzeba)
REPAIR TABLE products;
```

## 🔗 Powiązane Tematy
- [[Java JPA Hibernate]] - ORM mapping do SQL
- [[Spring Data JPA - Zaawansowane Operacje]] - Repository patterns
- [[Database Migrations - Flyway/Liquibase]] - Schema versioning
- [[Java Performance i Optymalizacja]] - Database performance

## 💡 Najlepsze Praktyki

1. **Używaj indexów strategicznie** - nie za dużo, nie za mało
2. **Preferuj JOIN nad subqueries** gdy to możliwe
3. **Używaj LIMIT** dla dużych result sets
4. **Unikaj SELECT *** - wybieraj tylko potrzebne kolumny
5. **Optymalizuj WHERE clauses** - najbardziej selektywne warunki pierwsze
6. **Używaj proper data types** - nie VARCHAR(255) dla wszystkiego
7. **Monitor query performance** - regularnie analizuj EXPLAIN plans

## ⚠️ Częste Błędy

1. **N+1 query problem** - wykonywanie zapytań w pętli
2. **Missing indexes** na często filtrowanych kolumnach
3. **Cartesian products** przez błędne JOIN conditions
4. **Over-normalization** prowadzące do złożonych JOINs
5. **Ignoring NULL handling** w calculations i comparisons

---
*Czas nauki: ~40 minut | Poziom: Zaawansowany*