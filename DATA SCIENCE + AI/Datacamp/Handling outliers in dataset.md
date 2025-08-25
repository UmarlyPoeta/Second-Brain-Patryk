When you left 18 hours ago, you worked on Data Cleaning and Imputation, chapter 2 of the course Exploratory Data Analysis in Python. Here is what you covered in your last lesson:

You learned about handling outliers, which are observations significantly different from other data points. For instance, in a dataset of house prices, a house priced at five million dollars could be an outlier if the median is $400,000, unless factors like location and size justify the price. Key points covered include:

- **Understanding Outliers**: Recognizing that outliers can skew data analyses and may not accurately represent the dataset.
- **Identifying Outliers**: Using the interquartile range (IQR) to mathematically define outliers. The IQR is the difference between the 75th and 25th percentiles, and outliers are typically any values 1.5 times the IQR above the 75th percentile or below the 25th percentile.
- **Calculating IQR and Outlier Thresholds**:
    
    ```
    IQR = Series.quantile(0.75) - Series.quantile(0.25)
    upper_limit = 75th_percentile + 1.5 * IQR
    lower_limit = 25th_percentile - 1.5 * IQR
    ```
    

- **Decision Making on Outliers**: Deciding whether to keep, adjust, or remove outliers based on their relevance and accuracy.
- **Impact of Removing Outliers**: Observing how outlier removal can lead to a more normally distributed dataset, which is crucial for many statistical tests and machine learning models.

You practiced identifying outliers using visualizations and learned techniques to remove them, thereby preparing your dataset for further analysis.

The goal of the next lesson is to teach how to import, convert, manipulate, and visualize DateTime data in pandas for effective time-series analysis.
