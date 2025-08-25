## ⏰ Pandas - Time Series Analysis

_Analiza danych czasowych w Pandas_

---

### 📝 Wprowadzenie do Time Series

**Time Series Analysis** w Pandas oferuje:

1. **DateTime indexing** - efektywne indeksowanie czasowe
2. **Resampling** - zmiana częstotliwości danych
3. **Rolling operations** - operacje w oknach czasowych
4. **Seasonal analysis** - analiza sezonowości
5. **Time zone handling** - obsługa stref czasowych

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Konfiguracja
pd.set_option('display.max_rows', 10)
plt.style.use('seaborn-v0_8')
```

---

### 📅 Tworzenie i manipulacja dat

```python
print("=== TWORZENIE DATETIME OBJECTS ===")

# 1. Date ranges
date_range = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
print(f"Daily range: {len(date_range)} dni")

# Różne częstotliwości
freq_examples = {
    'Hourly': pd.date_range('2023-01-01', periods=24, freq='H'),
    'Business Days': pd.date_range('2023-01-01', periods=10, freq='B'),
    'Monthly': pd.date_range('2023-01-01', periods=12, freq='M'),
    'Weekly': pd.date_range('2023-01-01', periods=52, freq='W'),
    'Quarterly': pd.date_range('2023-01-01', periods=4, freq='Q')
}

for name, dates in freq_examples.items():
    print(f"{name}: {dates[:3].tolist()}...")

# 2. Parsing strings to datetime
date_strings = ['2023-01-15', '15/01/2023', '2023-01-15 14:30:00']
parsed_dates = [pd.to_datetime(date_str) for date_str in date_strings]
print(f"\nParsed dates: {parsed_dates}")

# 3. Tworzenie danych czasowych
np.random.seed(42)
ts_data = pd.Series(
    np.random.randn(365).cumsum() + 100,
    index=pd.date_range('2023-01-01', periods=365, freq='D'),
    name='value'
)

print(f"\nTime series sample:")
print(ts_data.head())
print(f"Index type: {type(ts_data.index)}")

# 4. DateTime properties
dates = pd.to_datetime(['2023-01-15', '2023-06-15', '2023-12-15'])
dt_df = pd.DataFrame({'date': dates})

dt_df['year'] = dt_df['date'].dt.year
dt_df['month'] = dt_df['date'].dt.month
dt_df['day_of_week'] = dt_df['date'].dt.day_name()
dt_df['quarter'] = dt_df['date'].dt.quarter
dt_df['day_of_year'] = dt_df['date'].dt.dayofyear
dt_df['is_weekend'] = dt_df['date'].dt.dayofweek >= 5

print(f"\nDateTime properties:")
print(dt_df)
```

---

### 🔍 Indexowanie i selekcja czasowa

```python
print("=== INDEXOWANIE CZASOWE ===")

# Tworzenie przykładowych danych
business_data = pd.DataFrame({
    'sales': np.random.normal(1000, 200, 365),
    'customers': np.random.poisson(50, 365),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 365)
}, index=pd.date_range('2023-01-01', periods=365, freq='D'))

print("Sample data:")
print(business_data.head())

# 1. Selekcja po datach
print("\n=== SELEKCJA CZASOWA ===")

# Konkretny dzień
jan_15 = business_data['2023-01-15']
print(f"January 15th: Sales = {jan_15['sales']:.2f}")

# Cały miesiąc
january_data = business_data['2023-01']
print(f"January data shape: {january_data.shape}")

# Zakres dat
q1_data = business_data['2023-01':'2023-03']
print(f"Q1 data shape: {q1_data.shape}")

# Boolean indexing z datami
summer_data = business_data[(business_data.index.month >= 6) & 
                           (business_data.index.month <= 8)]
print(f"Summer data shape: {summer_data.shape}")

# Weekends only
weekend_data = business_data[business_data.index.dayofweek >= 5]
print(f"Weekend data shape: {weekend_data.shape}")

# 2. Loc i iloc z datetime
print("\n=== LOC/ILOC Z DATETIME ===")

# Loc with datetime
loc_sample = business_data.loc['2023-06-01':'2023-06-07', 'sales']
print(f"Week in June sales: {loc_sample.mean():.2f}")

# iLoc - pozycyjne
first_week = business_data.iloc[:7]
print(f"First week average sales: {first_week['sales'].mean():.2f}")

# 3. At and iat dla single values
single_value = business_data.at['2023-01-01', 'sales']
print(f"New Year's Day sales: {single_value:.2f}")

# 4. Query method z datetime
high_sales_summer = business_data.query(
    "sales > 1200 and index.month in [6, 7, 8]"
)
print(f"High sales summer days: {len(high_sales_summer)}")

# Wizualizacja selekcji
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Cały rok
business_data['sales'].plot(ax=axes[0, 0], title='Full Year Sales', alpha=0.7)
axes[0, 0].grid(True, alpha=0.3)

# Tylko styczeń
january_data['sales'].plot(ax=axes[0, 1], title='January Sales', color='red')
axes[0, 1].grid(True, alpha=0.3)

# Weekendy vs weekdays
business_data.groupby(business_data.index.dayofweek < 5)['sales'].mean().plot(
    kind='bar', ax=axes[1, 0], title='Weekday vs Weekend Sales'
)
axes[1, 0].set_xticklabels(['Weekend', 'Weekday'], rotation=0)

# Seasonality
monthly_avg = business_data.groupby(business_data.index.month)['sales'].mean()
monthly_avg.plot(ax=axes[1, 1], title='Monthly Average Sales', marker='o')
axes[1, 1].set_xlabel('Month')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

### 🔄 Resampling

```python
print("=== RESAMPLING ===")

# Tworzenie danych o wysokiej częstotliwości
hourly_data = pd.DataFrame({
    'temperature': 20 + 5 * np.sin(np.arange(24*30) * 2 * np.pi / 24) + np.random.normal(0, 1, 24*30),
    'humidity': 50 + 10 * np.cos(np.arange(24*30) * 2 * np.pi / 24) + np.random.normal(0, 2, 24*30)
}, index=pd.date_range('2023-01-01', periods=24*30, freq='H'))

print(f"Original hourly data shape: {hourly_data.shape}")
print("Sample:")
print(hourly_data.head())

# 1. Downsampling (agregacja)
print("\n=== DOWNSAMPLING ===")

# Daily aggregation
daily_avg = hourly_data.resample('D').mean()
daily_max = hourly_data.resample('D').max()
daily_min = hourly_data.resample('D').min()

print(f"Daily average shape: {daily_avg.shape}")
print("Daily averages sample:")
print(daily_avg.head())

# Weekly aggregation z różnymi funkcjami
weekly_stats = hourly_data.resample('W').agg({
    'temperature': ['mean', 'min', 'max', 'std'],
    'humidity': ['mean', 'min', 'max', 'std']
})

print(f"\nWeekly stats sample:")
print(weekly_stats.head())

# Custom aggregation functions
def temperature_range(series):
    return series.max() - series.min()

custom_agg = hourly_data.resample('D').agg({
    'temperature': [temperature_range, 'mean'],
    'humidity': ['mean', lambda x: x.quantile(0.9)]
})

print(f"\nCustom aggregation sample:")
print(custom_agg.head())

# 2. Upsampling (interpolacja)
print("\n=== UPSAMPLING ===")

# Start with daily data
daily_simple = pd.DataFrame({
    'value': np.random.randn(30).cumsum()
}, index=pd.date_range('2023-01-01', periods=30, freq='D'))

# Upsample to hourly
hourly_upsampled = daily_simple.resample('H').asfreq()
print(f"Upsampled with NaN: {hourly_upsampled.isna().sum().sum()} missing values")

# Forward fill
hourly_ffill = daily_simple.resample('H').ffill()
print(f"Forward fill missing: {hourly_ffill.isna().sum().sum()}")

# Interpolation
hourly_interp = daily_simple.resample('H').interpolate()
print(f"Interpolated missing: {hourly_interp.isna().sum().sum()}")

# Visualizacja resampling
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Original hourly data (first week)
week_data = hourly_data['2023-01-01':'2023-01-07']
week_data['temperature'].plot(ax=axes[0, 0], title='Hourly Temperature (Week 1)', alpha=0.7)
axes[0, 0].grid(True, alpha=0.3)

# Daily resampling
daily_avg['2023-01-01':'2023-01-07']['temperature'].plot(
    ax=axes[0, 1], title='Daily Average Temperature', marker='o', linewidth=2
)
axes[0, 1].grid(True, alpha=0.3)

# Comparison of aggregation methods
comparison_data = pd.DataFrame({
    'Daily Mean': daily_avg['temperature'],
    'Daily Max': daily_max['temperature'],
    'Daily Min': daily_min['temperature']
})
comparison_data['2023-01-01':'2023-01-14'].plot(
    ax=axes[1, 0], title='Different Aggregation Methods'
)
axes[1, 0].grid(True, alpha=0.3)

# Upsampling comparison
daily_simple.loc['2023-01-01':'2023-01-07'].plot(
    ax=axes[1, 1], label='Original Daily', marker='o', linewidth=2
)
hourly_interp.loc['2023-01-01 00:00':'2023-01-07 23:00'].plot(
    ax=axes[1, 1], label='Interpolated Hourly', alpha=0.7
)
axes[1, 1].set_title('Upsampling with Interpolation')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

### 🪟 Rolling Windows

```python
print("=== ROLLING WINDOWS ===")

# Tworzenie noisy time series
np.random.seed(42)
noisy_data = pd.Series(
    np.random.randn(365).cumsum() + 100 + 10 * np.sin(np.arange(365) * 2 * np.pi / 365),
    index=pd.date_range('2023-01-01', periods=365, freq='D'),
    name='price'
)

print(f"Noisy data sample:")
print(noisy_data.head())

# 1. Rolling mean (moving average)
rolling_windows = {
    '7-day': noisy_data.rolling(window=7).mean(),
    '30-day': noisy_data.rolling(window=30).mean(),
    '90-day': noisy_data.rolling(window=90).mean()
}

print("\n=== MOVING AVERAGES ===")
for name, series in rolling_windows.items():
    print(f"{name} MA (last 5): {series.tail().round(2).tolist()}")

# 2. Rolling statistics
rolling_stats = pd.DataFrame({
    'price': noisy_data,
    'MA_7': noisy_data.rolling(7).mean(),
    'MA_30': noisy_data.rolling(30).mean(),
    'std_7': noisy_data.rolling(7).std(),
    'min_30': noisy_data.rolling(30).min(),
    'max_30': noisy_data.rolling(30).max()
})

print(f"\nRolling stats sample:")
print(rolling_stats.tail())

# 3. Bollinger Bands
def bollinger_bands(series, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    
    return rolling_mean, upper_band, lower_band

bb_mean, bb_upper, bb_lower = bollinger_bands(noisy_data, window=20, num_std=2)

# 4. Custom rolling functions
def rolling_sharpe(returns, window=30):
    """Rolling Sharpe ratio"""
    return returns.rolling(window).mean() / returns.rolling(window).std() * np.sqrt(252)

# Calculate returns
returns = noisy_data.pct_change()
sharpe_ratio = rolling_sharpe(returns, window=30)

# 5. Expanding windows
expanding_stats = pd.DataFrame({
    'expanding_mean': noisy_data.expanding().mean(),
    'expanding_std': noisy_data.expanding().std(),
    'expanding_min': noisy_data.expanding().min(),
    'expanding_max': noisy_data.expanding().max()
})

print(f"\nExpanding stats sample:")
print(expanding_stats.tail())

# Wizualizacja rolling operations
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Moving averages
noisy_data.plot(ax=axes[0, 0], label='Original', alpha=0.5)
rolling_windows['7-day'].plot(ax=axes[0, 0], label='7-day MA', linewidth=2)
rolling_windows['30-day'].plot(ax=axes[0, 0], label='30-day MA', linewidth=2)
axes[0, 0].set_title('Moving Averages')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Bollinger Bands
noisy_data.plot(ax=axes[0, 1], label='Price', color='black')
bb_mean.plot(ax=axes[0, 1], label='20-day MA', color='blue')
bb_upper.plot(ax=axes[0, 1], label='Upper Band', color='red', linestyle='--')
bb_lower.plot(ax=axes[0, 1], label='Lower Band', color='red', linestyle='--')
axes[0, 1].fill_between(noisy_data.index, bb_upper, bb_lower, alpha=0.2, color='red')
axes[0, 1].set_title('Bollinger Bands')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Rolling volatility
rolling_stats['std_7'].plot(ax=axes[1, 0], label='7-day Volatility', color='purple')
rolling_stats['std_7'].rolling(30).mean().plot(ax=axes[1, 0], label='30-day MA of Volatility', color='orange')
axes[1, 0].set_title('Rolling Volatility')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Expanding vs rolling mean
expanding_stats['expanding_mean'].plot(ax=axes[1, 1], label='Expanding Mean')
rolling_windows['30-day'].plot(ax=axes[1, 1], label='30-day Rolling Mean')
axes[1, 1].set_title('Expanding vs Rolling Mean')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Performance comparison
print(f"\n=== PERFORMANCE COMPARISON ===")
import time

# Time different window operations
large_series = pd.Series(np.random.randn(100000))

operations = {
    'Rolling Mean (100)': lambda x: x.rolling(100).mean(),
    'Rolling Std (100)': lambda x: x.rolling(100).std(),
    'Expanding Mean': lambda x: x.expanding().mean(),
    'Rolling Apply (custom)': lambda x: x.rolling(100).apply(lambda y: y.max() - y.min())
}

for name, operation in operations.items():
    start_time = time.time()
    result = operation(large_series)
    end_time = time.time()
    print(f"{name}: {end_time - start_time:.4f} seconds")
```

---

### 🌍 Time Zones

```python
print("=== TIME ZONES ===")

# 1. Naive vs timezone-aware datetimes
naive_dt = pd.Timestamp('2023-06-15 14:30:00')
aware_dt = pd.Timestamp('2023-06-15 14:30:00', tz='UTC')

print(f"Naive datetime: {naive_dt}")
print(f"Timezone-aware: {aware_dt}")
print(f"Naive timezone: {naive_dt.tz}")
print(f"Aware timezone: {aware_dt.tz}")

# 2. Creating timezone-aware data
utc_range = pd.date_range('2023-06-15', periods=24, freq='H', tz='UTC')
local_data = pd.Series(np.random.randn(24), index=utc_range, name='temperature')

print(f"\nTimezone-aware series:")
print(local_data.head())

# 3. Converting timezones
timezones = ['US/Eastern', 'US/Pacific', 'Europe/London', 'Asia/Tokyo']
converted_series = {}

for tz in timezones:
    converted_series[tz] = local_data.tz_convert(tz)
    print(f"{tz}: {converted_series[tz].index[0]}")

# 4. Localizing naive timestamps
naive_series = pd.Series(
    np.random.randn(24),
    index=pd.date_range('2023-06-15', periods=24, freq='H'),
    name='sales'
)

# Localize to different timezones
localized = naive_series.tz_localize('US/Eastern')
print(f"\nLocalized series index:")
print(localized.index[:3])

# 5. Working with different timezone data
ny_data = pd.Series(
    np.random.randn(48),
    index=pd.date_range('2023-06-15', periods=48, freq='H', tz='US/Eastern'),
    name='ny_sales'
)

london_data = pd.Series(
    np.random.randn(48), 
    index=pd.date_range('2023-06-15', periods=48, freq='H', tz='Europe/London'),
    name='london_sales'
)

# Combine data from different timezones
combined = pd.DataFrame({'NY': ny_data, 'London': london_data})
print(f"\nCombined timezone data shape: {combined.shape}")
print("Sample:")
print(combined.head())

# 6. Business applications
def market_hours_filter(data, start_hour=9, end_hour=17):
    """Filter data to business hours only"""
    return data.between_time(f'{start_hour:02d}:00', f'{end_hour:02d}:00')

# Apply business hours filter
ny_business_hours = market_hours_filter(ny_data)
london_business_hours = market_hours_filter(london_data)

print(f"\nBusiness hours data:")
print(f"NY: {len(ny_business_hours)} hours")
print(f"London: {len(london_business_hours)} hours")

# Visualization of timezone effects
fig, axes = plt.subplots(2, 1, figsize=(15, 10))

# Same UTC time in different timezones
utc_base = pd.date_range('2023-06-15 12:00', periods=24, freq='H', tz='UTC')
sample_data = pd.Series(range(24), index=utc_base)

for tz in ['UTC', 'US/Eastern', 'Asia/Tokyo']:
    converted = sample_data.tz_convert(tz)
    axes[0].plot(converted.index, converted.values, marker='o', label=f'{tz}')

axes[0].set_title('Same Data in Different Timezones')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Business hours comparison
ny_bh_hourly = ny_business_hours.groupby(ny_business_hours.index.hour).mean()
london_bh_hourly = london_business_hours.groupby(london_business_hours.index.hour).mean()

axes[1].plot(ny_bh_hourly.index, ny_bh_hourly.values, marker='o', label='NY Business Hours')
axes[1].plot(london_bh_hourly.index, london_bh_hourly.values, marker='s', label='London Business Hours')
axes[1].set_title('Average Values by Hour (Business Hours Only)')
axes[1].set_xlabel('Hour of Day')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Common timezone operations
timezone_operations = """
🌍 COMMON TIMEZONE OPERATIONS

📍 CREATION:
• pd.Timestamp('2023-01-01 12:00', tz='UTC')
• pd.date_range('2023-01-01', periods=24, freq='H', tz='UTC')

🔄 CONVERSION:
• series.tz_localize('UTC')  # naive → aware
• series.tz_convert('US/Eastern')  # UTC → Eastern

⏰ BUSINESS LOGIC:
• between_time('09:00', '17:00')  # business hours
• at_time('12:00')  # specific time
• groupby(data.index.tz_convert('local').hour)  # local hour

🔍 ANALYSIS:
• Compare market hours across regions
• Account for daylight saving time
• Synchronize global events
"""

print(timezone_operations)
```

---

### 📊 Seasonal Decomposition

```python
print("=== SEASONAL DECOMPOSITION ===")

# Create time series with trend, seasonality, and noise
np.random.seed(42)
dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')

# Components
trend = np.linspace(100, 200, len(dates))
yearly_seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
weekly_seasonal = 5 * np.sin(2 * np.pi * np.arange(len(dates)) / 7)
noise = np.random.normal(0, 5, len(dates))

# Combined time series
ts = pd.Series(trend + yearly_seasonal + weekly_seasonal + noise, 
               index=dates, name='sales')

print(f"Time series with seasonality:")
print(f"Period: {ts.index.min()} to {ts.index.max()}")
print(f"Shape: {ts.shape}")

# Manual seasonal decomposition
def simple_seasonal_decompose(series, period):
    """Simple seasonal decomposition"""
    # Trend (using centered moving average)
    trend = series.rolling(window=period, center=True).mean()
    
    # Detrended series
    detrended = series - trend
    
    # Seasonal component (average for each period)
    seasonal = detrended.groupby(series.index.dayofyear % period).transform('mean')
    
    # Residual
    residual = detrended - seasonal
    
    return trend, seasonal, residual

# Decompose with annual seasonality
trend_comp, seasonal_comp, residual_comp = simple_seasonal_decompose(ts, 365)

# Create DataFrame with components
decomposition = pd.DataFrame({
    'original': ts,
    'trend': trend_comp,
    'seasonal': seasonal_comp,
    'residual': residual_comp
})

print(f"\nDecomposition sample:")
print(decomposition.head())

# Statistics of components
print(f"\nComponent statistics:")
for col in decomposition.columns:
    if col != 'original':
        variance_explained = 1 - (decomposition[col].var() / ts.var())
        print(f"{col.capitalize()}: {variance_explained:.3f} variance explained")

# Advanced: Using scipy for better decomposition
try:
    from scipy import signal
    
    # Seasonal-Trend decomposition using LOESS (STL)
    # This is a simplified version - in practice use statsmodels.tsa.seasonal.seasonal_decompose
    def stl_decompose(series, period):
        """Simplified STL decomposition"""
        # Trend using savgol filter
        trend = pd.Series(signal.savgol_filter(series.values, 
                                              window_length=min(period*2+1, len(series)//4*2+1), 
                                              polyorder=1),
                         index=series.index)
        
        # Detrended
        detrended = series - trend
        
        # Seasonal (more sophisticated averaging)
        seasonal = detrended.groupby([series.index.month, series.index.day]).transform('mean')
        
        # Residual
        residual = detrended - seasonal
        
        return trend, seasonal, residual
    
    stl_trend, stl_seasonal, stl_residual = stl_decompose(ts, 365)
    
    print(f"\nSTL decomposition completed")
    
except ImportError:
    print(f"\nSciPy not available for advanced decomposition")
    stl_trend, stl_seasonal, stl_residual = trend_comp, seasonal_comp, residual_comp

# Visualization
fig, axes = plt.subplots(4, 1, figsize=(15, 12))

# Original series
ts.plot(ax=axes[0], title='Original Time Series', color='black')
axes[0].grid(True, alpha=0.3)

# Trend
trend_comp.plot(ax=axes[1], title='Trend Component', color='red', linewidth=2)
axes[1].grid(True, alpha=0.3)

# Seasonal
seasonal_comp['2023'].plot(ax=axes[2], title='Seasonal Component (2023)', color='green')
axes[2].grid(True, alpha=0.3)

# Residual
residual_comp.plot(ax=axes[3], title='Residual Component', color='purple', alpha=0.7)
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Seasonal patterns analysis
print(f"\n=== SEASONAL PATTERNS ANALYSIS ===")

# Monthly seasonality
monthly_pattern = ts.groupby(ts.index.month).agg(['mean', 'std'])
print(f"Monthly patterns:")
print(monthly_pattern.round(2))

# Day of week seasonality  
dow_pattern = ts.groupby(ts.index.dayofweek).agg(['mean', 'std'])
dow_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
dow_pattern.index = dow_names
print(f"\nDay of week patterns:")
print(dow_pattern.round(2))

# Visualization of seasonal patterns
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Monthly seasonality
monthly_pattern['sales']['mean'].plot(kind='bar', ax=axes[0], 
                                     title='Monthly Average Sales')
axes[0].set_xlabel('Month')
axes[0].set_ylabel('Average Sales')
axes[0].grid(True, alpha=0.3)

# Day of week seasonality
dow_pattern['sales']['mean'].plot(kind='bar', ax=axes[1], 
                                 title='Day of Week Average Sales')
axes[1].set_xlabel('Day of Week')
axes[1].set_ylabel('Average Sales')
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

### 💡 Best Practices

```python
def time_series_best_practices():
    """Najlepsze praktyki analizy time series"""
    
    practices = """
    ✅ TIME SERIES BEST PRACTICES
    
    📅 DATA HANDLING:
    • Zawsze używaj datetime index dla time series
    • Sprawdź i obsłuż missing timestamps  
    • Wybierz odpowiedną częstotliwość danych
    • Handle timezone conversions early
    • Validate data continuity and gaps
    
    🔄 RESAMPLING:
    • Choose appropriate aggregation functions
    • Be careful with upsampling - consider interpolation
    • Account for business calendars (holidays, weekends)
    • Document resampling decisions
    • Validate aggregation makes business sense
    
    🪟 ROLLING OPERATIONS:
    • Select window size based on data frequency
    • Consider seasonal patterns in window size
    • Use expanding windows for cumulative metrics
    • Handle edge cases (insufficient data points)
    • Optimize for performance with large datasets
    
    📊 SEASONAL ANALYSIS:
    • Identify multiple seasonal patterns
    • Account for changing seasonality over time
    • Use appropriate decomposition methods
    • Validate seasonal patterns make business sense
    • Document seasonal assumptions
    
    ⚠️  COMMON PITFALLS:
    • Ignoring timezone effects in global data
    • Inappropriate aggregation functions
    • Not handling missing data properly
    • Over-smoothing with too large windows
    • Assuming stationarity without testing
    """
    
    print(practices)

time_series_best_practices()
```

---

### 🎯 Następny krok

Poznasz **Data Cleaning - Text Processing**:

- String operations and cleaning
- Regular expressions in pandas
- Text normalization techniques
- Handling multilingual text
- Performance optimization for text processing