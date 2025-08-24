## 📝 Data Cleaning - Text Processing

_Zaawansowane techniki przetwarzania tekstu w Pandas_

---

### 📝 Wprowadzenie do Text Processing

**Text Processing** w Data Science obejmuje:

1. **String operations** - podstawowe operacje na tekście
2. **Regular expressions** - wzorce i pattern matching
3. **Normalization** - standaryzacja tekstu
4. **Encoding handling** - obsługa różnych kodowań
5. **Performance optimization** - efektywne przetwarzanie

```python
import pandas as pd
import numpy as np
import re
import string
from collections import Counter
import unicodedata
import warnings
warnings.filterwarnings('ignore')

# Konfiguracja
pd.set_option('display.max_colwidth', 100)
```

---

### 🔤 Podstawowe operacje na stringach

```python
print("=== PODSTAWOWE OPERACJE NA STRINGACH ===")

# Przykładowe dane tekstowe
messy_data = pd.DataFrame({
    'names': ['  John DOE  ', 'jane smith', 'BOB JOHNSON', '  mary WILLIAMS  ', 'Tom Brown Jr.'],
    'emails': ['john.doe@COMPANY.COM', 'janesmith@gmail.com', 'bob@Company.com', 
               'mary.williams@COMPANY.COM', 'tom.brown.jr@company.com'],
    'phones': ['(555) 123-4567', '555.234.5678', '5551234567', '555-345-6789', '(555)456-7890'],
    'addresses': ['123 Main St, New York, NY', '456 Oak Ave, Los Angeles, CA',
                  '789 Pine Rd, Chicago, IL', '321 Elm St, Houston, TX', 
                  '654 Maple Dr, Phoenix, AZ'],
    'descriptions': ['Software Engineer with 5+ years experience in Python and SQL.',
                    'Data Scientist specializing in ML and analytics.',
                    'Product Manager with strong technical background.',
                    'UX Designer with expertise in user research.',
                    'DevOps Engineer focused on cloud infrastructure.']
})

print("Original messy data:")
print(messy_data)

# 1. Case operations
print("\n=== CASE OPERATIONS ===")
messy_data['names_lower'] = messy_data['names'].str.lower()
messy_data['names_upper'] = messy_data['names'].str.upper()
messy_data['names_title'] = messy_data['names'].str.title()
messy_data['names_capitalize'] = messy_data['names'].str.capitalize()

print("Case transformations:")
case_comparison = messy_data[['names', 'names_lower', 'names_title']].head(3)
print(case_comparison)

# 2. Whitespace handling
print("\n=== WHITESPACE HANDLING ===")
messy_data['names_stripped'] = messy_data['names'].str.strip()
messy_data['names_stripped_all'] = messy_data['names'].str.replace(r'\s+', ' ', regex=True)

print("Whitespace cleaning:")
whitespace_comparison = messy_data[['names', 'names_stripped']].head()
for idx, row in whitespace_comparison.iterrows():
    print(f"'{row['names']}' -> '{row['names_stripped']}'")

# 3. Length and character operations
print("\n=== LENGTH AND CHARACTER OPERATIONS ===")
text_stats = pd.DataFrame({
    'text': messy_data['descriptions'],
    'length': messy_data['descriptions'].str.len(),
    'word_count': messy_data['descriptions'].str.split().str.len(),
    'char_count_no_spaces': messy_data['descriptions'].str.replace(' ', '').str.len(),
    'contains_python': messy_data['descriptions'].str.contains('Python', case=False),
    'starts_with_data': messy_data['descriptions'].str.startswith('Data'),
    'ends_with_period': messy_data['descriptions'].str.endswith('.')
})

print("Text statistics:")
print(text_stats)

# 4. Splitting and extracting
print("\n=== SPLITTING AND EXTRACTING ===")

# Split names
name_parts = messy_data['names_stripped'].str.split(expand=True)
name_parts.columns = ['first_name', 'middle_name', 'last_name']
print("Split names:")
print(name_parts)

# Extract specific parts
messy_data['first_word'] = messy_data['descriptions'].str.split().str[0]
messy_data['last_word'] = messy_data['descriptions'].str.split().str[-1]

print("First and last words:")
print(messy_data[['descriptions', 'first_word', 'last_word']].head(3))

# 5. String replacement
print("\n=== STRING REPLACEMENT ===")

# Simple replacement
messy_data['emails_standardized'] = messy_data['emails'].str.lower()

# Multiple replacements
phone_cleaned = (messy_data['phones']
                .str.replace(r'[^\d]', '', regex=True)  # Remove non-digits
                .str.replace(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', regex=True))  # Format

messy_data['phones_cleaned'] = phone_cleaned

print("Phone number cleaning:")
phone_comparison = messy_data[['phones', 'phones_cleaned']]
for idx, row in phone_comparison.iterrows():
    print(f"'{row['phones']}' -> '{row['phones_cleaned']}'")
```

---

### 🔍 Regular Expressions

```python
print("=== REGULAR EXPRESSIONS ===")

# Przykłady wzorców regex
sample_text = pd.Series([
    "Contact us at info@company.com or call (555) 123-4567",
    "Visit our website: https://www.example.com for more info",
    "Our office hours are 9:00 AM - 5:00 PM, Monday-Friday",
    "Product ID: ABC-123-XYZ, Price: $99.99, SKU: #12345",
    "Date: 2023-12-15, Time: 14:30:00, Location: Building A"
])

print("Sample text data:")
for i, text in enumerate(sample_text):
    print(f"{i}: {text}")

# 1. Email extraction
print("\n=== EMAIL EXTRACTION ===")
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
emails_found = sample_text.str.extract(email_pattern, expand=False)
print("Extracted emails:")
print(emails_found)

# Find all emails (in case of multiple)
all_emails = sample_text.str.findall(email_pattern)
print("All emails found:")
print(all_emails)

# 2. Phone number extraction
print("\n=== PHONE NUMBER EXTRACTION ===")
phone_patterns = [
    r'\(\d{3}\)\s\d{3}-\d{4}',  # (555) 123-4567
    r'\d{3}-\d{3}-\d{4}',       # 555-123-4567
    r'\d{3}\.\d{3}\.\d{4}'      # 555.123.4567
]

for i, pattern in enumerate(phone_patterns):
    phones = sample_text.str.extract(pattern, expand=False)
    print(f"Pattern {i+1}: {phones.dropna().tolist()}")

# Combined phone pattern
combined_phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
all_phones = sample_text.str.extract(combined_phone_pattern, expand=False)
print(f"Combined pattern results: {all_phones.dropna().tolist()}")

# 3. URL extraction
print("\n=== URL EXTRACTION ===")
url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
urls = sample_text.str.extract(url_pattern, expand=False)
print(f"URLs found: {urls.dropna().tolist()}")

# 4. Price extraction
print("\n=== PRICE EXTRACTION ===")
price_pattern = r'\$\d+\.?\d*'
prices = sample_text.str.extract(price_pattern, expand=False)
print(f"Prices found: {prices.dropna().tolist()}")

# Convert to numeric
price_numeric = (sample_text.str.extract(r'\$(\d+\.?\d*)', expand=False)
                .astype(float))
print(f"Numeric prices: {price_numeric.dropna().tolist()}")

# 5. Date and time extraction
print("\n=== DATE AND TIME EXTRACTION ===")
date_pattern = r'\d{4}-\d{2}-\d{2}'
time_pattern = r'\d{2}:\d{2}:\d{2}'

dates = sample_text.str.extract(date_pattern, expand=False)
times = sample_text.str.extract(time_pattern, expand=False)

print(f"Dates: {dates.dropna().tolist()}")
print(f"Times: {times.dropna().tolist()}")

# 6. Complex pattern with multiple groups
print("\n=== COMPLEX PATTERNS ===")
product_pattern = r'Product ID: ([A-Z]{3}-\d{3}-[A-Z]{3}), Price: \$(\d+\.?\d*), SKU: #(\d+)'
product_info = sample_text.str.extract(product_pattern)
product_info.columns = ['product_id', 'price', 'sku']
print("Extracted product info:")
print(product_info.dropna())

# 7. Validation patterns
print("\n=== VALIDATION PATTERNS ===")

# Email validation
def validate_email(email_series):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return email_series.str.match(pattern)

# Phone validation  
def validate_phone(phone_series):
    pattern = r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
    return phone_series.str.match(pattern)

test_emails = pd.Series(['valid@email.com', 'invalid.email', 'also@valid.org'])
test_phones = pd.Series(['(555) 123-4567', '555-123-4567', 'invalid-phone'])

print("Email validation:")
print(pd.DataFrame({'email': test_emails, 'valid': validate_email(test_emails)}))

print("Phone validation:")
print(pd.DataFrame({'phone': test_phones, 'valid': validate_phone(test_phones)}))

# 8. Performance comparison
print("\n=== PERFORMANCE COMPARISON ===")

# Large dataset for testing
large_text = pd.Series(['Contact: john@example.com, Phone: (555) 123-4567'] * 10000)

import time

# Method 1: Using str.contains
start = time.time()
result1 = large_text.str.contains('@')
time1 = time.time() - start

# Method 2: Using regex compile
start = time.time()
compiled_pattern = re.compile('@')
result2 = large_text.str.contains(compiled_pattern)
time2 = time.time() - start

print(f"String contains: {time1:.4f} seconds")
print(f"Compiled regex: {time2:.4f} seconds")
print(f"Speedup: {time1/time2:.2f}x")
```

---

### 🌐 Text Normalization

```python
print("=== TEXT NORMALIZATION ===")

# Różnorodne dane tekstowe do normalizacji
diverse_text = pd.DataFrame({
    'mixed_text': [
        'Café naïve résumé',
        'MIXED CaSe TeXt',
        'Special chars: @#$%^&*()',
        'Multiple    spaces   and\ttabs',
        'Émojis 😀 and ümlaüts',
        'Numbers123mixed456with789text',
        'Punctuation!!! Too??? Much...',
        'Leading/trailing whitespace   '
    ],
    'messy_names': [
        '  José María García  ',
        'O\'Connor, Patrick',
        'van der Berg, Anna',
        'MacDonald, John',
        'Al-Rahman, Ahmed',
        '李小明 (Li Xiaoming)',
        'Müller-Schmidt, Hans',
        'St. James, Catherine'
    ]
})

print("Original diverse text:")
print(diverse_text)

# 1. Unicode normalization
print("\n=== UNICODE NORMALIZATION ===")

def normalize_unicode(text_series):
    """Normalize unicode characters"""
    return text_series.apply(lambda x: unicodedata.normalize('NFKD', str(x)))

def remove_accents(text_series):
    """Remove accents from text"""
    return (text_series
            .apply(lambda x: unicodedata.normalize('NFKD', str(x)))
            .str.encode('ascii', errors='ignore')
            .str.decode('ascii'))

diverse_text['unicode_normalized'] = normalize_unicode(diverse_text['mixed_text'])
diverse_text['accents_removed'] = remove_accents(diverse_text['mixed_text'])

print("Unicode normalization:")
unicode_comparison = diverse_text[['mixed_text', 'accents_removed']].head(3)
for idx, row in unicode_comparison.iterrows():
    print(f"'{row['mixed_text']}' -> '{row['accents_removed']}'")

# 2. Case normalization strategies
print("\n=== CASE NORMALIZATION ===")

def smart_title_case(text_series):
    """Smart title case that handles special cases"""
    # Słowa które nie powinny być capitalized (except at start)
    minor_words = {'of', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with'}
    
    def title_case_word(text):
        words = str(text).lower().split()
        if not words:
            return text
        
        # First word always capitalized
        result = [words[0].capitalize()]
        
        for word in words[1:]:
            if word in minor_words:
                result.append(word)
            else:
                result.append(word.capitalize())
        
        return ' '.join(result)
    
    return text_series.apply(title_case_word)

diverse_text['smart_title'] = smart_title_case(diverse_text['messy_names'])

print("Smart title case:")
title_comparison = diverse_text[['messy_names', 'smart_title']].head(4)
for idx, row in title_comparison.iterrows():
    print(f"'{row['messy_names']}' -> '{row['smart_title']}'")

# 3. Punctuation and special character handling
print("\n=== PUNCTUATION HANDLING ===")

def clean_punctuation(text_series, keep_periods=True):
    """Clean punctuation while preserving sentence structure"""
    def clean_text(text):
        text = str(text)
        # Remove excessive punctuation
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        text = re.sub(r'[.]{2,}', '.', text)
        
        if not keep_periods:
            text = text.translate(str.maketrans('', '', string.punctuation))
        
        return text
    
    return text_series.apply(clean_text)

diverse_text['punctuation_cleaned'] = clean_punctuation(diverse_text['mixed_text'])
diverse_text['punctuation_removed'] = clean_punctuation(diverse_text['mixed_text'], keep_periods=False)

print("Punctuation cleaning:")
punct_comparison = diverse_text[['mixed_text', 'punctuation_cleaned']].head(3)
for idx, row in punct_comparison.iterrows():
    print(f"'{row['mixed_text']}' -> '{row['punctuation_cleaned']}'")

# 4. Whitespace normalization
print("\n=== WHITESPACE NORMALIZATION ===")

def normalize_whitespace(text_series):
    """Normalize all types of whitespace"""
    return (text_series
            .str.replace(r'\s+', ' ', regex=True)  # Multiple spaces -> single space
            .str.replace(r'^\s+|\s+$', '', regex=True))  # Strip leading/trailing

diverse_text['whitespace_normalized'] = normalize_whitespace(diverse_text['mixed_text'])

print("Whitespace normalization:")
ws_comparison = diverse_text[['mixed_text', 'whitespace_normalized']].head(4)
for idx, row in ws_comparison.iterrows():
    print(f"'{row['mixed_text']}' -> '{row['whitespace_normalized']}'")

# 5. Complete text normalization pipeline
print("\n=== COMPLETE NORMALIZATION PIPELINE ===")

def comprehensive_text_clean(text_series):
    """Comprehensive text cleaning pipeline"""
    cleaned = text_series.copy()
    
    # Step 1: Basic cleaning
    cleaned = cleaned.astype(str)
    cleaned = cleaned.str.strip()
    
    # Step 2: Unicode normalization
    cleaned = cleaned.apply(lambda x: unicodedata.normalize('NFKD', x))
    
    # Step 3: Whitespace normalization
    cleaned = cleaned.str.replace(r'\s+', ' ', regex=True)
    
    # Step 4: Remove or normalize special characters
    cleaned = cleaned.str.replace(r'[^\w\s.-]', ' ', regex=True)
    
    # Step 5: Case normalization
    cleaned = cleaned.str.title()
    
    # Step 6: Final cleanup
    cleaned = cleaned.str.strip()
    
    return cleaned

diverse_text['fully_cleaned'] = comprehensive_text_clean(diverse_text['mixed_text'])

print("Complete normalization:")
complete_comparison = diverse_text[['mixed_text', 'fully_cleaned']]
for idx, row in complete_comparison.iterrows():
    print(f"'{row['mixed_text']}' -> '{row['fully_cleaned']}'")
```

---

### 🏎️ Performance Optimization

```python
print("=== PERFORMANCE OPTIMIZATION ===")

# Create large dataset for testing
np.random.seed(42)
large_dataset = pd.DataFrame({
    'text': [f"Sample text {i} with various content and lengths {np.random.randint(1000, 9999)}" 
             for i in range(100000)],
    'category': np.random.choice(['A', 'B', 'C'], 100000),
    'numbers': [f"{np.random.randint(100, 999)}-{np.random.randint(1000, 9999)}" 
                for _ in range(100000)]
})

print(f"Large dataset created: {large_dataset.shape}")
print("Sample data:")
print(large_dataset.head(3))

# 1. Vectorized vs loop operations
print("\n=== VECTORIZED VS LOOP OPERATIONS ===")

import time

# Method 1: Vectorized operations
start = time.time()
result_vectorized = large_dataset['text'].str.upper()
time_vectorized = time.time() - start

# Method 2: Apply with lambda
start = time.time()
result_apply = large_dataset['text'].apply(lambda x: x.upper())
time_apply = time.time() - start

# Method 3: List comprehension (don't do this for pandas!)
start = time.time()
result_list = [x.upper() for x in large_dataset['text']]
time_list = time.time() - start

print(f"Vectorized str.upper(): {time_vectorized:.4f} seconds")
print(f"Apply with lambda: {time_apply:.4f} seconds")
print(f"List comprehension: {time_list:.4f} seconds")
print(f"Vectorized is {time_apply/time_vectorized:.2f}x faster than apply")

# 2. Compiled regex vs string operations
print("\n=== COMPILED REGEX VS STRING OPERATIONS ===")

pattern = r'\d+'

# Method 1: String contains
start = time.time()
result_contains = large_dataset['text'].str.contains(pattern, regex=True)
time_contains = time.time() - start

# Method 2: Compiled regex
compiled_pattern = re.compile(pattern)
start = time.time()
result_compiled = large_dataset['text'].str.contains(compiled_pattern)
time_compiled = time.time() - start

print(f"String contains with regex: {time_contains:.4f} seconds")
print(f"Compiled regex: {time_compiled:.4f} seconds")
print(f"Speedup: {time_contains/time_compiled:.2f}x")

# 3. Memory-efficient processing
print("\n=== MEMORY-EFFICIENT PROCESSING ===")

def process_in_chunks(series, chunk_size=10000, operation=lambda x: x.str.upper()):
    """Process large series in chunks to save memory"""
    results = []
    
    for i in range(0, len(series), chunk_size):
        chunk = series.iloc[i:i+chunk_size]
        processed_chunk = operation(chunk)
        results.append(processed_chunk)
    
    return pd.concat(results, ignore_index=True)

# Test chunked processing
start = time.time()
chunked_result = process_in_chunks(large_dataset['text'], 
                                  operation=lambda x: x.str.replace(r'\d+', 'NUM', regex=True))
time_chunked = time.time() - start

# Regular processing
start = time.time()
regular_result = large_dataset['text'].str.replace(r'\d+', 'NUM', regex=True)
time_regular = time.time() - start

print(f"Chunked processing: {time_chunked:.4f} seconds")
print(f"Regular processing: {time_regular:.4f} seconds")
print(f"Results equal: {chunked_result.equals(regular_result)}")

# 4. Caching expensive operations
print("\n=== CACHING EXPENSIVE OPERATIONS ===")

from functools import lru_cache

# Expensive text processing function
@lru_cache(maxsize=1000)
def expensive_text_process(text):
    """Simulate expensive text processing"""
    # Multiple operations that might be repeated
    processed = text.lower()
    processed = re.sub(r'\d+', 'NUM', processed)
    processed = re.sub(r'[^\w\s]', '', processed)
    return processed.strip()

# Create dataset with many duplicates
repeated_data = pd.Series(['Text sample 1', 'Text sample 2', 'Text sample 1'] * 10000)

# Without caching
start = time.time()
result_no_cache = repeated_data.apply(lambda x: expensive_text_process.__wrapped__(x))
time_no_cache = time.time() - start

# With caching
expensive_text_process.cache_clear()  # Clear cache first
start = time.time()
result_cached = repeated_data.apply(expensive_text_process)
time_cached = time.time() - start

print(f"Without caching: {time_no_cache:.4f} seconds")
print(f"With caching: {time_cached:.4f} seconds")
print(f"Speedup: {time_no_cache/time_cached:.2f}x")
print(f"Cache info: {expensive_text_process.cache_info()}")

# 5. Parallel processing with larger datasets
print("\n=== PARALLEL PROCESSING CONSIDERATIONS ===")

parallel_tips = """
🚀 PARALLEL PROCESSING TIPS

⚡ WHEN TO USE:
• Very large datasets (> 1M rows)
• Complex text processing operations
• Independent row operations
• CPU-bound tasks

🛠️ IMPLEMENTATION OPTIONS:
• multiprocessing.Pool with pandas chunks
• Dask for out-of-core processing
• Swifter library for easy parallelization
• Ray for distributed processing

📊 EXAMPLE PATTERN:
```python
import multiprocessing as mp
from functools import partial

def process_chunk(chunk, operation):
    return chunk.apply(operation)

def parallel_apply(series, operation, n_cores=None):
    if n_cores is None:
        n_cores = mp.cpu_count()
    
    chunks = np.array_split(series, n_cores)
    
    with mp.Pool(n_cores) as pool:
        func = partial(process_chunk, operation=operation)
        results = pool.map(func, chunks)
    
    return pd.concat(results, ignore_index=True)
```

⚠️  CONSIDERATIONS:
• Overhead cost for small datasets
• Memory usage with multiple processes
• Serialization costs for complex functions
• Not always faster due to GIL limitations
"""

print(parallel_tips)
```

---

### 💡 Best Practices Summary

```python
def text_processing_best_practices():
    """Najlepsze praktyki przetwarzania tekstu"""
    
    practices = """
    ✅ TEXT PROCESSING BEST PRACTICES
    
    🔤 STRING OPERATIONS:
    • Używaj pandas str accessor dla vectorized operations
    • Zawsze sprawdzaj czy dane są strings (.astype(str))
    • Handle missing values przed string operations
    • Używaj kompilowanych regex dla powtarzających się wzorców
    • Pamiętaj o case sensitivity w porównaniach
    
    🔍 REGULAR EXPRESSIONS:
    • Kompiluj wzorce używane wielokrotnie
    • Używaj raw strings (r'pattern') dla regex
    • Testuj wzorce na małych próbkach przed skalowaniem
    • Dokumentuj skomplikowane wzorce
    • Consider performance implications of complex patterns
    
    🌐 NORMALIZATION:
    • Ustal standardy normalizacji na początku projektu
    • Handle unicode characters appropriately
    • Preserve important punctuation for context
    • Test normalization with edge cases
    • Document all normalization steps
    
    🏎️ PERFORMANCE:
    • Profile text operations na dużych danych
    • Używaj vectorized operations zamiast apply gdy możliwe
    • Cache expensive operations dla powtarzających się wartości
    • Consider chunked processing dla bardzo dużych datasets
    • Monitor memory usage podczas text processing
    
    ⚠️  COMMON PITFALLS:
    • Nie testowanie na różnorodnych danych tekstowych
    • Ignorowanie edge cases (null, empty strings)
    • Over-normalization prowadząca do utraty informacji
    • Używanie apply zamiast vectorized operations
    • Brak walidacji wyników text processing
    """
    
    print(practices)

text_processing_best_practices()

# Practical text processing checklist
checklist = """
📋 TEXT PROCESSING CHECKLIST

✅ BEFORE PROCESSING:
□ Identify text columns and their purposes
□ Check for missing values and null strings
□ Examine sample data for patterns
□ Determine required normalization level
□ Plan validation strategies

✅ DURING PROCESSING:
□ Start with small samples for testing
□ Use vectorized operations when possible
□ Handle encoding issues early
□ Validate regex patterns thoroughly
□ Monitor memory and performance

✅ AFTER PROCESSING:
□ Validate results with sample data
□ Check for unintended data loss
□ Document all transformations
□ Create reusable functions for future use
□ Test edge cases and error handling

✅ PRODUCTION CONSIDERATIONS:
□ Handle new/unseen text patterns
□ Monitor processing performance
□ Log text processing errors
□ Version control text processing rules
□ Plan for scaling requirements
"""

print(checklist)
```

---

### 🎯 Następny krok

Poznaj więcej zaawansowanych technik w:
- **Feature Engineering - Text Features** - TF-IDF, embeddings, sentiment analysis
- **Natural Language Processing** - tokenization, stemming, NER
- **Machine Learning for Text** - classification, clustering, topic modeling
- **Advanced Text Analytics** - semantic analysis, entity extraction