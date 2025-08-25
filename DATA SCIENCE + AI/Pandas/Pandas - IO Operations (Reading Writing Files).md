## 📁 Pandas - IO Operations (Reading/Writing Files)

_Zaawansowane techniki wczytywania i zapisywania danych w różnych formatach_

---

### 📝 Wprowadzenie do IO Operations

**Pandas IO operations** obejmują:

1. **CSV operations** - zaawansowane czytanie/zapisywanie CSV
2. **Excel integration** - praca z plikami Excel
3. **Database connectivity** - połączenia z bazami danych
4. **JSON/XML handling** - structured data formats
5. **Parquet/HDF5** - binary formats dla performance
6. **Web scraping** - HTML tables i APIs

---

### 📊 Advanced CSV Operations

#### Optimized CSV reading strategies

```python
import pandas as pd
import numpy as np
import time
import tempfile
import os

def demonstrate_advanced_csv_operations():
    """Demonstracja zaawansowanych operacji CSV"""
    
    # Create large test CSV file
    def create_test_csv(filename, rows=100000):
        """Create test CSV file"""
        with open(filename, 'w') as f:
            # Header
            f.write('id,name,category,value,date,description,flag\n')
            
            # Data rows
            for i in range(rows):
                name = f"Customer_{i % 1000}"
                category = np.random.choice(['A', 'B', 'C', 'D'])
                value = np.random.normal(1000, 200)
                date = f"2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}"
                description = f"Description with some text {i % 100}"
                flag = 'Y' if i % 3 == 0 else 'N'
                
                f.write(f"{i},{name},{category},{value:.2f},{date},{description},{flag}\n")
    
    # Create test file
    test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    create_test_csv(test_file.name)
    
    print("Advanced CSV Reading Strategies:")
    print("=" * 50)
    
    # Strategy 1: Basic reading (baseline)
    print("1. Basic Reading:")
    start = time.time()
    df_basic = pd.read_csv(test_file.name)
    basic_time = time.time() - start
    basic_memory = df_basic.memory_usage(deep=True).sum() / 1024 / 1024
    
    print(f"   Time: {basic_time:.4f}s")
    print(f"   Memory: {basic_memory:.2f} MB")
    print(f"   Shape: {df_basic.shape}")
    
    # Strategy 2: Optimized dtypes
    print(f"\n2. Optimized Data Types:")
    
    optimized_dtypes = {
        'id': 'int32',
        'name': 'category',
        'category': 'category', 
        'value': 'float32',
        'description': 'category',  # Repeating descriptions
        'flag': 'category'
    }
    
    start = time.time()
    df_optimized = pd.read_csv(
        test_file.name,
        dtype=optimized_dtypes,
        parse_dates=['date']
    )
    optimized_time = time.time() - start
    optimized_memory = df_optimized.memory_usage(deep=True).sum() / 1024 / 1024
    
    print(f"   Time: {optimized_time:.4f}s")
    print(f"   Memory: {optimized_memory:.2f} MB")
    print(f"   Memory reduction: {(1-optimized_memory/basic_memory)*100:.1f}%")
    
    # Strategy 3: Selective column loading
    print(f"\n3. Selective Column Loading:")
    
    selected_columns = ['id', 'category', 'value', 'date']
    
    start = time.time()
    df_selective = pd.read_csv(
        test_file.name,
        usecols=selected_columns,
        dtype={'id': 'int32', 'category': 'category', 'value': 'float32'},
        parse_dates=['date']
    )
    selective_time = time.time() - start
    selective_memory = df_selective.memory_usage(deep=True).sum() / 1024 / 1024
    
    print(f"   Time: {selective_time:.4f}s")  
    print(f"   Memory: {selective_memory:.2f} MB")
    print(f"   Memory reduction: {(1-selective_memory/basic_memory)*100:.1f}%")
    
    # Strategy 4: Chunked reading
    print(f"\n4. Chunked Reading:")
    
    def process_chunk(chunk):
        """Process jednotlivého chunk"""
        # Example: filter and aggregate
        filtered = chunk[chunk['value'] > 1000]
        return filtered.groupby('category')['value'].mean()
    
    start = time.time()
    chunk_results = []
    
    for chunk in pd.read_csv(test_file.name, chunksize=10000, dtype=optimized_dtypes):
        processed = process_chunk(chunk)
        chunk_results.append(processed)
    
    # Combine chunk results
    final_result = pd.concat(chunk_results).groupby(level=0).mean()
    chunked_time = time.time() - start
    
    print(f"   Time: {chunked_time:.4f}s")
    print(f"   Result: {final_result}")
    print(f"   Peak memory: Much lower (only chunk in memory)")
    
    # Strategy 5: Using converters
    print(f"\n5. Using Converters:")
    
    def value_converter(x):
        """Custom value converter"""
        try:
            val = float(x)
            return val if val > 0 else 0
        except:
            return 0
    
    def description_converter(x):
        """Extract numeric part from description"""
        try:
            import re
            match = re.search(r'\d+', str(x))
            return int(match.group()) if match else 0
        except:
            return 0
    
    converters = {
        'value': value_converter,
        'description': description_converter
    }
    
    start = time.time()
    df_converted = pd.read_csv(
        test_file.name,
        converters=converters,
        usecols=['id', 'category', 'value', 'description']
    )
    converter_time = time.time() - start
    
    print(f"   Time: {converter_time:.4f}s")
    print(f"   Sample converted data:")
    print(df_converted.head())
    
    # Cleanup
    os.unlink(test_file.name)

demonstrate_advanced_csv_operations()
```

#### Advanced CSV writing techniques

```python
def demonstrate_csv_writing():
    """Zaawansowane techniki zapisywania CSV"""
    
    # Test data
    np.random.seed(42)
    n = 50000
    
    df = pd.DataFrame({
        'id': range(n),
        'name': [f"Name_{i}" for i in range(n)],
        'category': np.random.choice(['A', 'B', 'C'], n),
        'value': np.random.normal(1000, 200, n),
        'date': pd.date_range('2020-01-01', periods=n, freq='H'),
        'large_text': [f"This is a long description for record {i} " * 5 for i in range(n)]
    })
    
    print("Advanced CSV Writing:")
    print("=" * 30)
    
    # 1. Basic writing (baseline)
    temp_file1 = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    
    start = time.time()
    df.to_csv(temp_file1.name, index=False)
    basic_write_time = time.time() - start
    basic_size = os.path.getsize(temp_file1.name) / 1024 / 1024  # MB
    
    print(f"1. Basic writing:")
    print(f"   Time: {basic_write_time:.4f}s")
    print(f"   File size: {basic_size:.2f} MB")
    
    # 2. Compressed writing
    temp_file2 = tempfile.NamedTemporaryFile(delete=False, suffix='.csv.gz')
    
    start = time.time()
    df.to_csv(temp_file2.name, index=False, compression='gzip')
    compressed_time = time.time() - start
    compressed_size = os.path.getsize(temp_file2.name) / 1024 / 1024  # MB
    
    print(f"\n2. Compressed writing (gzip):")
    print(f"   Time: {compressed_time:.4f}s")
    print(f"   File size: {compressed_size:.2f} MB")
    print(f"   Compression ratio: {basic_size/compressed_size:.1f}x")
    
    # 3. Chunked writing dla large datasets
    def write_in_chunks(dataframe, filename, chunk_size=10000):
        """Write large DataFrame w chunks"""
        
        start_time = time.time()
        
        # Write header
        header_written = False
        
        for start_idx in range(0, len(dataframe), chunk_size):
            end_idx = min(start_idx + chunk_size, len(dataframe))
            chunk = dataframe.iloc[start_idx:end_idx]
            
            # Write chunk
            chunk.to_csv(
                filename,
                mode='w' if not header_written else 'a',
                header=not header_written,
                index=False
            )
            header_written = True
        
        return time.time() - start_time
    
    temp_file3 = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    chunked_write_time = write_in_chunks(df, temp_file3.name)
    
    print(f"\n3. Chunked writing:")
    print(f"   Time: {chunked_write_time:.4f}s")
    
    # 4. Selective column writing
    temp_file4 = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    
    selected_columns = ['id', 'category', 'value', 'date']
    
    start = time.time()
    df[selected_columns].to_csv(temp_file4.name, index=False)
    selective_time = time.time() - start
    selective_size = os.path.getsize(temp_file4.name) / 1024 / 1024
    
    print(f"\n4. Selective column writing:")
    print(f"   Time: {selective_time:.4f}s")
    print(f"   File size: {selective_size:.2f} MB")
    print(f"   Size reduction: {(1-selective_size/basic_size)*100:.1f}%")
    
    # 5. Custom formatting during write
    def format_currency(x):
        """Format numbers as currency"""
        return f"${x:.2f}"
    
    def format_date(x):
        """Format dates"""
        return x.strftime('%Y-%m-%d %H:%M')
    
    # Apply formatting
    df_formatted = df.copy()
    df_formatted['value'] = df_formatted['value'].apply(format_currency)
    df_formatted['date'] = df_formatted['date'].apply(format_date)
    
    temp_file5 = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    
    start = time.time()
    df_formatted[['id', 'category', 'value', 'date']].to_csv(temp_file5.name, index=False)
    formatted_time = time.time() - start
    
    print(f"\n5. Formatted writing:")
    print(f"   Time: {formatted_time:.4f}s")
    
    # Show sample of formatted data
    print("   Sample formatted data:")
    print(df_formatted[['id', 'category', 'value', 'date']].head(3))
    
    # Cleanup
    for temp_file in [temp_file1, temp_file2, temp_file3, temp_file4, temp_file5]:
        try:
            os.unlink(temp_file.name)
        except:
            pass

demonstrate_csv_writing()
```

---

### 📗 Excel Integration

#### Advanced Excel operations

```python
def demonstrate_excel_operations():
    """Zaawansowane operacje Excel"""
    
    print("Excel Operations:")
    print("=" * 25)
    
    try:
        # Test data
        np.random.seed(42)
        
        # Multiple sheets data
        sales_data = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=100, freq='D'),
            'Product': np.random.choice(['A', 'B', 'C'], 100),
            'Sales': np.random.exponential(1000, 100),
            'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
        })
        
        summary_data = sales_data.groupby(['Product', 'Region']).agg({
            'Sales': ['sum', 'mean', 'count']
        }).round(2)
        
        metadata = pd.DataFrame({
            'Info': ['Created', 'Records', 'Date Range', 'Products'],
            'Value': [
                pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
                len(sales_data),
                f"{sales_data['Date'].min()} to {sales_data['Date'].max()}",
                ', '.join(sales_data['Product'].unique())
            ]
        })
        
        # Create Excel file z multiple sheets
        temp_excel = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        
        print("1. Writing Multiple Sheets:")
        
        with pd.ExcelWriter(temp_excel.name, engine='openpyxl') as writer:
            # Main data sheet
            sales_data.to_excel(writer, sheet_name='Sales_Data', index=False)
            
            # Summary sheet  
            summary_data.to_excel(writer, sheet_name='Summary')
            
            # Metadata sheet
            metadata.to_excel(writer, sheet_name='Metadata', index=False)
        
        print(f"   Excel file created: {temp_excel.name}")
        print(f"   File size: {os.path.getsize(temp_excel.name) / 1024:.2f} KB")
        
        # 2. Reading z specific sheets
        print(f"\n2. Reading Specific Sheets:")
        
        # Read all sheets
        all_sheets = pd.read_excel(temp_excel.name, sheet_name=None)
        
        print(f"   Available sheets: {list(all_sheets.keys())}")
        
        for sheet_name, df in all_sheets.items():
            print(f"   {sheet_name}: {df.shape}")
        
        # Read specific sheet z options
        sales_df = pd.read_excel(
            temp_excel.name, 
            sheet_name='Sales_Data',
            parse_dates=['Date'],
            dtype={'Product': 'category', 'Region': 'category'}
        )
        
        print(f"   Sales data dtypes:")
        print(f"   {sales_df.dtypes}")
        
        # 3. Reading z ranges i filtering
        print(f"\n3. Range Reading and Filtering:")
        
        # Read specific range
        range_data = pd.read_excel(
            temp_excel.name,
            sheet_name='Sales_Data', 
            usecols=['Date', 'Product', 'Sales'],
            nrows=20  # First 20 rows only
        )
        
        print(f"   Range data shape: {range_data.shape}")
        print(f"   Date range: {range_data['Date'].min()} to {range_data['Date'].max()}")
        
        # 4. Advanced formatting podczas writing
        print(f"\n4. Advanced Excel Formatting:")
        
        temp_formatted_excel = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        
        with pd.ExcelWriter(temp_formatted_excel.name, engine='openpyxl') as writer:
            # Write main data
            sales_data.to_excel(writer, sheet_name='Formatted_Data', index=False)
            
            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Formatted_Data']
            
            # Add some formatting (basic example)
            from openpyxl.styles import Font, PatternFill
            
            # Header formatting
            header_font = Font(bold=True)
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            
            for cell in worksheet[1]:  # First row (header)
                cell.font = header_font
                # cell.fill = header_fill  # Commented out to avoid color issues
        
        print(f"   Formatted Excel created")
        
        # Cleanup
        os.unlink(temp_excel.name)
        os.unlink(temp_formatted_excel.name)
        
    except ImportError as e:
        print(f"Excel operations require additional packages: {e}")
        print("Install with: pip install openpyxl xlsxwriter")
    except Exception as e:
        print(f"Excel operations error: {e}")

# demonstrate_excel_operations()  # Commented out due to potential missing dependencies
```

---

### 🗄️ Database Connectivity

#### SQL database operations

```python
def demonstrate_database_operations():
    """Database connectivity i operations"""
    
    print("Database Operations:")
    print("=" * 25)
    
    try:
        import sqlite3
        
        # Create in-memory SQLite database dla testing
        conn = sqlite3.connect(':memory:')
        
        # Sample data
        np.random.seed(42)
        customers = pd.DataFrame({
            'customer_id': range(1, 1001),
            'name': [f"Customer_{i}" for i in range(1, 1001)],
            'email': [f"customer{i}@example.com" for i in range(1, 1001)],
            'age': np.random.randint(18, 80, 1000),
            'city': np.random.choice(['New York', 'London', 'Paris', 'Tokyo'], 1000),
            'registration_date': pd.date_range('2020-01-01', periods=1000, freq='D')
        })
        
        orders = pd.DataFrame({
            'order_id': range(1, 2001),
            'customer_id': np.random.randint(1, 1001, 2000),
            'product': np.random.choice(['Product_A', 'Product_B', 'Product_C'], 2000),
            'amount': np.random.exponential(100, 2000),
            'order_date': pd.date_range('2020-01-01', periods=2000, freq='6H')
        })
        
        print("1. Writing DataFrames to Database:")
        
        # Write DataFrames to database
        customers.to_sql('customers', conn, index=False, if_exists='replace')
        orders.to_sql('orders', conn, index=False, if_exists='replace')
        
        print(f"   Customers table: {len(customers)} records")
        print(f"   Orders table: {len(orders)} records")
        
        # 2. Basic SQL queries
        print(f"\n2. Basic SQL Queries:")
        
        # Simple query
        customer_count = pd.read_sql_query("SELECT COUNT(*) as count FROM customers", conn)
        print(f"   Total customers: {customer_count['count'].iloc[0]}")
        
        # Query z WHERE clause
        young_customers = pd.read_sql_query("""
            SELECT name, age, city 
            FROM customers 
            WHERE age < 25 
            ORDER BY age
        """, conn)
        
        print(f"   Young customers (age < 25): {len(young_customers)}")
        
        # 3. Complex JOIN queries
        print(f"\n3. Complex JOIN Queries:")
        
        # Customer order summary
        order_summary = pd.read_sql_query("""
            SELECT 
                c.name,
                c.city,
                COUNT(o.order_id) as order_count,
                SUM(o.amount) as total_spent,
                AVG(o.amount) as avg_order_value
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.name, c.city
            HAVING COUNT(o.order_id) > 0
            ORDER BY total_spent DESC
            LIMIT 10
        """, conn)
        
        print("   Top 10 customers by total spent:")
        print(order_summary)
        
        # 4. Parameterized queries (safe z SQL injection)
        print(f"\n4. Parameterized Queries:")
        
        def get_customers_by_city(city_name):
            """Safe parameterized query"""
            query = """
                SELECT c.name, c.age, COUNT(o.order_id) as orders
                FROM customers c
                LEFT JOIN orders o ON c.customer_id = o.customer_id  
                WHERE c.city = ?
                GROUP BY c.customer_id, c.name, c.age
                ORDER BY orders DESC
            """
            return pd.read_sql_query(query, conn, params=[city_name])
        
        tokyo_customers = get_customers_by_city('Tokyo')
        print(f"   Tokyo customers with orders: {len(tokyo_customers)}")
        print(tokyo_customers.head())
        
        # 5. Chunked database operations
        print(f"\n5. Chunked Database Operations:")
        
        def process_large_query_chunked(query, chunk_size=100):
            """Process large query results w chunks"""
            results = []
            offset = 0
            
            while True:
                chunked_query = f"{query} LIMIT {chunk_size} OFFSET {offset}"
                chunk = pd.read_sql_query(chunked_query, conn)
                
                if len(chunk) == 0:
                    break
                
                # Process chunk (przykład: just collect)
                results.append(chunk)
                offset += chunk_size
                
                print(f"     Processed chunk starting at offset {offset - chunk_size}: {len(chunk)} records")
                
                if len(chunk) < chunk_size:  # Last chunk
                    break
            
            return pd.concat(results, ignore_index=True) if results else pd.DataFrame()
        
        # Process all orders w chunks
        all_orders_chunked = process_large_query_chunked(
            "SELECT * FROM orders ORDER BY order_id", 
            chunk_size=500
        )
        
        print(f"   Total orders processed in chunks: {len(all_orders_chunked)}")
        
        # 6. Database performance optimization
        print(f"\n6. Performance Optimization:")
        
        # Create index dla better performance
        conn.execute("CREATE INDEX idx_customer_id ON orders(customer_id)")
        conn.execute("CREATE INDEX idx_order_date ON orders(order_date)")
        
        # Test query performance (przed i po indexing)
        import time
        
        performance_query = """
            SELECT c.city, COUNT(o.order_id) as order_count, AVG(o.amount) as avg_amount
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE o.order_date >= '2021-01-01'
            GROUP BY c.city
            ORDER BY order_count DESC
        """
        
        start = time.time()
        performance_result = pd.read_sql_query(performance_query, conn)
        query_time = time.time() - start
        
        print(f"   Query execution time: {query_time:.6f}s")
        print("   Results by city:")
        print(performance_result)
        
        conn.close()
        
    except ImportError:
        print("Database operations require sqlite3 (usually included z Python)")
    except Exception as e:
        print(f"Database error: {e}")

demonstrate_database_operations()
```

---

### 🌐 JSON i Web Data

#### JSON operations

```python
def demonstrate_json_operations():
    """JSON data handling"""
    
    print("JSON Operations:")
    print("=" * 20)
    
    # 1. Basic JSON operations
    print("1. Basic JSON Operations:")
    
    # Sample nested JSON data
    json_data = {
        'users': [
            {
                'id': 1,
                'name': 'John Doe',
                'email': 'john@example.com',
                'address': {
                    'street': '123 Main St',
                    'city': 'New York',
                    'country': 'USA'
                },
                'orders': [
                    {'order_id': 101, 'amount': 150.00, 'date': '2023-01-15'},
                    {'order_id': 102, 'amount': 75.50, 'date': '2023-02-20'}
                ],
                'preferences': {'newsletter': True, 'sms': False}
            },
            {
                'id': 2,
                'name': 'Jane Smith',
                'email': 'jane@example.com', 
                'address': {
                    'street': '456 Oak Ave',
                    'city': 'London',
                    'country': 'UK'
                },
                'orders': [
                    {'order_id': 103, 'amount': 200.00, 'date': '2023-01-10'},
                    {'order_id': 104, 'amount': 125.75, 'date': '2023-03-05'},
                    {'order_id': 105, 'amount': 89.99, 'date': '2023-03-15'}
                ],
                'preferences': {'newsletter': False, 'sms': True}
            }
        ]
    }
    
    # Write JSON to temp file
    import json
    temp_json = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    json.dump(json_data, temp_json, indent=2)
    temp_json.close()
    
    # Basic JSON reading
    df_basic = pd.read_json(temp_json.name)
    print(f"   Basic JSON read shape: {df_basic.shape}")
    print(f"   Columns: {df_basic.columns.tolist()}")
    
    # 2. Normalizing nested JSON
    print(f"\n2. JSON Normalization:")
    
    # Normalize users data
    users_df = pd.json_normalize(json_data['users'])
    print(f"   Normalized users shape: {users_df.shape}")
    print("   Normalized columns:")
    for col in users_df.columns:
        print(f"     {col}")
    
    print("\n   Sample normalized data:")
    print(users_df[['name', 'address.city', 'address.country', 'preferences.newsletter']].head())
    
    # 3. Extracting nested lists
    print(f"\n3. Extracting Nested Lists:")
    
    # Extract orders data
    orders_data = []
    for user in json_data['users']:
        user_id = user['id']
        user_name = user['name']
        for order in user['orders']:
            order_record = order.copy()
            order_record['user_id'] = user_id
            order_record['user_name'] = user_name
            orders_data.append(order_record)
    
    orders_df = pd.DataFrame(orders_data)
    print(f"   Orders DataFrame shape: {orders_df.shape}")
    print("   Orders sample:")
    print(orders_df.head())
    
    # 4. JSON Lines format
    print(f"\n4. JSON Lines Format:")
    
    # Create JSON Lines data
    jsonl_data = [
        {'id': 1, 'name': 'Product A', 'price': 99.99, 'category': 'Electronics'},
        {'id': 2, 'name': 'Product B', 'price': 149.99, 'category': 'Electronics'},
        {'id': 3, 'name': 'Product C', 'price': 29.99, 'category': 'Books'}
    ]
    
    # Write JSON Lines
    temp_jsonl = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl')
    for record in jsonl_data:
        json.dump(record, temp_jsonl)
        temp_jsonl.write('\n')
    temp_jsonl.close()
    
    # Read JSON Lines
    df_jsonl = pd.read_json(temp_jsonl.name, lines=True)
    print(f"   JSON Lines shape: {df_jsonl.shape}")
    print("   JSON Lines data:")
    print(df_jsonl)
    
    # 5. Writing complex DataFrames to JSON
    print(f"\n5. Writing Complex DataFrames:")
    
    # Create complex DataFrame
    complex_df = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'scores': [[85, 90, 78], [92, 88, 95], [76, 82, 89]],
        'metadata': [
            {'age': 25, 'city': 'NYC'},
            {'age': 30, 'city': 'LA'}, 
            {'age': 35, 'city': 'Chicago'}
        ],
        'timestamp': pd.date_range('2023-01-01', periods=3, freq='D')
    })
    
    # Write z different orientations
    temp_records = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    complex_df.to_json(temp_records.name, orient='records', date_format='iso', indent=2)
    
    print("   Complex DataFrame written as records")
    
    # Read back and verify
    df_read_back = pd.read_json(temp_records.name)
    print(f"   Read back shape: {df_read_back.shape}")
    
    # Cleanup
    for temp_file in [temp_json.name, temp_jsonl.name, temp_records.name]:
        try:
            os.unlink(temp_file)
        except:
            pass

demonstrate_json_operations()
```

#### Web scraping and APIs

```python
def demonstrate_web_operations():
    """Web scraping i API operations"""
    
    print("Web Operations:")
    print("=" * 20)
    
    # 1. HTML table reading (mock example)
    print("1. HTML Table Operations:")
    
    # Create mock HTML content
    html_content = """
    <html>
    <body>
        <table id="data-table">
            <thead>
                <tr><th>Name</th><th>Age</th><th>City</th><th>Score</th></tr>
            </thead>
            <tbody>
                <tr><td>Alice</td><td>25</td><td>New York</td><td>85</td></tr>
                <tr><td>Bob</td><td>30</td><td>London</td><td>92</td></tr>
                <tr><td>Charlie</td><td>35</td><td>Paris</td><td>78</td></tr>
                <tr><td>Diana</td><td>28</td><td>Tokyo</td><td>96</td></tr>
            </tbody>
        </table>
        
        <table id="summary-table">
            <thead>
                <tr><th>Metric</th><th>Value</th></tr>
            </thead>
            <tbody>
                <tr><td>Total Records</td><td>4</td></tr>
                <tr><td>Average Age</td><td>29.5</td></tr>
                <tr><td>Average Score</td><td>87.75</td></tr>
            </tbody>
        </table>
    </body>
    </html>
    """
    
    # Write HTML to temp file
    temp_html = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html')
    temp_html.write(html_content)
    temp_html.close()
    
    try:
        # Read HTML tables
        tables = pd.read_html(temp_html.name)
        print(f"   Found {len(tables)} tables")
        
        for i, table in enumerate(tables):
            print(f"   Table {i+1} shape: {table.shape}")
            print(f"   Table {i+1} preview:")
            print(table.head())
            print()
        
        # Read specific table with attributes
        specific_tables = pd.read_html(temp_html.name, attrs={'id': 'data-table'})
        print(f"   Specific table (id='data-table'):")
        print(specific_tables[0])
        
    except ImportError:
        print("   HTML reading requires: pip install lxml beautifulsoup4 html5lib")
    except Exception as e:
        print(f"   HTML reading error: {e}")
    
    # 2. API simulation (mock data)
    print(f"\n2. API-like Data Operations:")
    
    # Simulate API response data
    api_response_data = {
        'status': 'success',
        'data': {
            'records': [
                {'id': 1, 'value': 100, 'timestamp': '2023-01-01T10:00:00Z'},
                {'id': 2, 'value': 150, 'timestamp': '2023-01-01T11:00:00Z'},
                {'id': 3, 'value': 125, 'timestamp': '2023-01-01T12:00:00Z'}
            ],
            'metadata': {
                'total_count': 3,
                'page': 1,
                'per_page': 10
            }
        }
    }
    
    # Process API-like data
    records_df = pd.DataFrame(api_response_data['data']['records'])
    records_df['timestamp'] = pd.to_datetime(records_df['timestamp'])
    
    print("   API-like data processed:")
    print(records_df)
    print(f"   Metadata: {api_response_data['data']['metadata']}")
    
    # 3. Handling pagination-like data
    print(f"\n3. Pagination Simulation:")
    
    def simulate_paginated_api(page_size=2, total_records=10):
        """Simulate paginated API responses"""
        
        all_data = []
        
        for page in range(1, (total_records // page_size) + 2):
            start_idx = (page - 1) * page_size
            end_idx = min(start_idx + page_size, total_records)
            
            if start_idx >= total_records:
                break
            
            # Simulate API response dla this page
            page_data = []
            for i in range(start_idx, end_idx):
                page_data.append({
                    'id': i + 1,
                    'value': np.random.randint(50, 200),
                    'category': np.random.choice(['A', 'B', 'C']),
                    'timestamp': f"2023-01-01T{10 + i}:00:00Z"
                })
            
            print(f"     Page {page}: {len(page_data)} records")
            all_data.extend(page_data)
        
        return pd.DataFrame(all_data)
    
    paginated_df = simulate_paginated_api(page_size=3, total_records=10)
    print(f"   Total paginated records: {len(paginated_df)}")
    print("   Sample paginated data:")
    print(paginated_df.head())
    
    # Cleanup
    try:
        os.unlink(temp_html.name)
    except:
        pass

demonstrate_web_operations()
```

---

### ⚡ High-Performance Formats

#### Parquet operations

```python
def demonstrate_high_performance_formats():
    """High-performance file formats"""
    
    print("High-Performance Formats:")
    print("=" * 35)
    
    # Create test data
    np.random.seed(42)
    n = 100000
    
    df_large = pd.DataFrame({
        'id': range(n),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n),
        'value1': np.random.normal(1000, 200, n),
        'value2': np.random.exponential(50, n),
        'date': pd.date_range('2020-01-01', periods=n, freq='H'),
        'flag': np.random.choice([True, False], n),
        'text': [f"Description_{i%1000}" for i in range(n)]
    })
    
    # 1. Parquet format
    print("1. Parquet Format:")
    
    try:
        temp_parquet = tempfile.NamedTemporaryFile(delete=False, suffix='.parquet')
        
        # Write to parquet
        start = time.time()
        df_large.to_parquet(temp_parquet.name, compression='snappy')
        parquet_write_time = time.time() - start
        parquet_size = os.path.getsize(temp_parquet.name) / 1024 / 1024
        
        # Read from parquet
        start = time.time()
        df_parquet_read = pd.read_parquet(temp_parquet.name)
        parquet_read_time = time.time() - start
        
        print(f"   Write time: {parquet_write_time:.4f}s")
        print(f"   Read time: {parquet_read_time:.4f}s")
        print(f"   File size: {parquet_size:.2f} MB")
        print(f"   Data integrity: {df_large.equals(df_parquet_read)}")
        
        # Compare z CSV
        temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        
        start = time.time()
        df_large.to_csv(temp_csv.name, index=False)
        csv_write_time = time.time() - start
        csv_size = os.path.getsize(temp_csv.name) / 1024 / 1024
        
        start = time.time()
        df_csv_read = pd.read_csv(temp_csv.name, parse_dates=['date'])
        csv_read_time = time.time() - start
        
        print(f"\n   CSV Comparison:")
        print(f"   CSV write time: {csv_write_time:.4f}s")
        print(f"   CSV read time: {csv_read_time:.4f}s")
        print(f"   CSV file size: {csv_size:.2f} MB")
        print(f"   Parquet size advantage: {csv_size/parquet_size:.1f}x smaller")
        print(f"   Parquet read speed: {csv_read_time/parquet_read_time:.1f}x faster")
        
        os.unlink(temp_parquet.name)
        os.unlink(temp_csv.name)
        
    except ImportError:
        print("   Parquet requires: pip install pyarrow or pip install fastparquet")
    
    # 2. HDF5 format
    print(f"\n2. HDF5 Format:")
    
    try:
        temp_hdf5 = tempfile.NamedTemporaryFile(delete=False, suffix='.h5')
        
        # Write to HDF5
        start = time.time()
        df_large.to_hdf(temp_hdf5.name, key='data', mode='w', complevel=9)
        hdf5_write_time = time.time() - start
        hdf5_size = os.path.getsize(temp_hdf5.name) / 1024 / 1024
        
        # Read from HDF5
        start = time.time()
        df_hdf5_read = pd.read_hdf(temp_hdf5.name, key='data')
        hdf5_read_time = time.time() - start
        
        print(f"   Write time: {hdf5_write_time:.4f}s")
        print(f"   Read time: {hdf5_read_time:.4f}s")
        print(f"   File size: {hdf5_size:.2f} MB")
        
        # Multiple datasets w HDF5
        df_subset1 = df_large[['id', 'category', 'value1']].head(10000)
        df_subset2 = df_large[['id', 'date', 'flag']].head(5000)
        
        temp_hdf5_multi = tempfile.NamedTemporaryFile(delete=False, suffix='.h5')
        
        df_subset1.to_hdf(temp_hdf5_multi.name, key='subset1', mode='w')
        df_subset2.to_hdf(temp_hdf5_multi.name, key='subset2', mode='a')  # append mode
        
        # List keys w HDF5 file
        with pd.HDFStore(temp_hdf5_multi.name, 'r') as store:
            print(f"   HDF5 keys: {list(store.keys())}")
        
        os.unlink(temp_hdf5.name)
        os.unlink(temp_hdf5_multi.name)
        
    except ImportError:
        print("   HDF5 requires: pip install tables")
    
    # 3. Pickle format (fastest ale nie portable)
    print(f"\n3. Pickle Format:")
    
    temp_pickle = tempfile.NamedTemporaryFile(delete=False, suffix='.pkl')
    
    # Write to pickle
    start = time.time()
    df_large.to_pickle(temp_pickle.name)
    pickle_write_time = time.time() - start
    pickle_size = os.path.getsize(temp_pickle.name) / 1024 / 1024
    
    # Read from pickle
    start = time.time()
    df_pickle_read = pd.read_pickle(temp_pickle.name)
    pickle_read_time = time.time() - start
    
    print(f"   Write time: {pickle_write_time:.4f}s")
    print(f"   Read time: {pickle_read_time:.4f}s")
    print(f"   File size: {pickle_size:.2f} MB")
    print(f"   Data integrity: {df_large.equals(df_pickle_read)}")
    
    os.unlink(temp_pickle.name)
    
    # 4. Performance summary
    print(f"\n4. Performance Summary:")
    print("   Format comparisons (100k records):")
    print("   ===================================")
    print(f"   {'Format':<10} {'Write(s)':<10} {'Read(s)':<10} {'Size(MB)':<10}")
    print(f"   {'Pickle':<10} {pickle_write_time:<10.4f} {pickle_read_time:<10.4f} {pickle_size:<10.2f}")

demonstrate_high_performance_formats()
```

---

### 💡 IO Best Practices

#### Comprehensive optimization strategies

```python
def io_best_practices():
    """Best practices dla IO operations"""
    
    best_practices = """
    ✅ FILE FORMAT SELECTION:
    - CSV: Human-readable, universal compatibility
    - Parquet: Best compression, fast read/write, preserves dtypes
    - HDF5: Complex hierarchical data, partial reading
    - Pickle: Fastest for pandas objects (Python only)
    - Excel: Business users, formatting needs
    
    ✅ PERFORMANCE OPTIMIZATION:
    - Specify dtypes during reading (dtype parameter)
    - Use compression dla storage savings
    - Implement chunking dla memory management
    - Cache frequently accessed data
    - Use columnar formats (Parquet) dla analytics
    
    ✅ MEMORY MANAGEMENT:
    - Read only needed columns (usecols)
    - Use chunksize dla large files
    - Process data in batches
    - Monitor memory usage during operations
    - Clean up temporary files
    
    ✅ DATA INTEGRITY:
    - Validate data after reading
    - Handle missing/corrupt data gracefully
    - Use checksums dla critical data
    - Implement error handling i logging
    - Test with edge cases
    
    ✅ SECURITY:
    - Validate file paths i extensions
    - Sanitize user inputs
    - Use parameterized queries dla databases
    - Avoid executing untrusted code
    - Implement access controls
    """
    
    print("IO Operations Best Practices:")
    print("=" * 40)
    print(best_practices)

io_best_practices()

# Example comprehensive IO workflow
class DataIOManager:
    """Comprehensive data IO management class"""
    
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir or tempfile.gettempdir()
        self.supported_formats = ['.csv', '.parquet', '.pkl', '.json', '.xlsx']
    
    def smart_read(self, file_path, format_hint=None, **kwargs):
        """Smart data reading z format detection"""
        
        # Detect format
        if format_hint:
            file_format = format_hint
        else:
            _, ext = os.path.splitext(file_path)
            file_format = ext.lower()
        
        # Validate format
        if file_format not in self.supported_formats:
            raise ValueError(f"Unsupported format: {file_format}")
        
        # Read based na format
        start_time = time.time()
        
        try:
            if file_format == '.csv':
                df = pd.read_csv(file_path, **kwargs)
            elif file_format == '.parquet':
                df = pd.read_parquet(file_path, **kwargs)
            elif file_format == '.pkl':
                df = pd.read_pickle(file_path, **kwargs)
            elif file_format == '.json':
                df = pd.read_json(file_path, **kwargs)
            elif file_format == '.xlsx':
                df = pd.read_excel(file_path, **kwargs)
            else:
                raise ValueError(f"Format {file_format} not implemented")
            
            read_time = time.time() - start_time
            
            return {
                'data': df,
                'read_time': read_time,
                'format': file_format,
                'shape': df.shape,
                'memory_usage': df.memory_usage(deep=True).sum()
            }
        
        except Exception as e:
            return {
                'data': None,
                'error': str(e),
                'format': file_format
            }
    
    def smart_write(self, df, file_path, optimize=True, **kwargs):
        """Smart data writing z optimization"""
        
        _, ext = os.path.splitext(file_path)
        file_format = ext.lower()
        
        start_time = time.time()
        
        try:
            if optimize:
                # Auto-optimize dtypes
                df = self._optimize_dtypes(df)
            
            if file_format == '.csv':
                df.to_csv(file_path, index=False, **kwargs)
            elif file_format == '.parquet':
                df.to_parquet(file_path, compression='snappy', **kwargs)
            elif file_format == '.pkl':
                df.to_pickle(file_path, **kwargs)
            elif file_format == '.json':
                df.to_json(file_path, **kwargs)
            elif file_format == '.xlsx':
                df.to_excel(file_path, index=False, **kwargs)
            else:
                raise ValueError(f"Format {file_format} not supported dla writing")
            
            write_time = time.time() - start_time
            file_size = os.path.getsize(file_path)
            
            return {
                'success': True,
                'write_time': write_time,
                'file_size': file_size,
                'format': file_format
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'format': file_format
            }
    
    def _optimize_dtypes(self, df):
        """Auto-optimize DataFrame dtypes"""
        optimized_df = df.copy()
        
        for col in optimized_df.columns:
            if optimized_df[col].dtype == 'object':
                # Try category
                unique_ratio = optimized_df[col].nunique() / len(optimized_df)
                if unique_ratio < 0.5:  # Less than 50% unique
                    try:
                        optimized_df[col] = optimized_df[col].astype('category')
                    except:
                        pass
        
        return optimized_df

# Test DataIOManager
def test_io_manager():
    """Test comprehensive IO manager"""
    
    # Create test data
    test_df = pd.DataFrame({
        'id': range(1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'value': np.random.normal(100, 20, 1000)
    })
    
    manager = DataIOManager()
    
    # Test writing
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.parquet')
    
    write_result = manager.smart_write(test_df, temp_file.name, optimize=True)
    print("IO Manager Test:")
    print(f"Write result: {write_result}")
    
    # Test reading
    read_result = manager.smart_read(temp_file.name)
    print(f"Read result keys: {read_result.keys()}")
    print(f"Data shape: {read_result['shape']}")
    print(f"Read time: {read_result['read_time']:.6f}s")
    
    # Cleanup
    os.unlink(temp_file.name)

test_io_manager()
```

---

### 🔗 Powiązane tematy

- [[Pandas - Performance Optimization]] - Optymalizacja wydajności
- [[Data Cleaning - Missing Values]] - Czyszczenie danych
- [[EDA - Exploratory Data Analysis]] - Analiza eksploracyjna
- [[Machine Learning Pipeline - Preprocessing]] - Preprocessing w ML