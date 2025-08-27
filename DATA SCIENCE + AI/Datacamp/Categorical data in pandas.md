## Categorical data in pandas

You learned about handling categorical data in pandas, a crucial skill for data analysis, especially when dealing with datasets that include categorical information. Here are the key points you covered:

- **Understanding Data Types in pandas**: You saw how pandas assigns data types to columns, with numerical values getting an `int64` type and strings being stored as `object` by default. This is important because the way data is stored can affect both memory usage and performance.
- **Converting to Categorical Data Type**: You learned to convert columns with string values to the `category` data type using the `.astype('category')` method. This conversion is beneficial for memory efficiency and can make operations on the data faster.
- **Creating Categorical Series**: Two methods were discussed for creating a categorical pandas Series. The first method involves using `pd.Series()` with the `dtype` argument set to `category`, and the second method uses `pd.Categorical()`, which allows specifying an order for the categories.
- **Memory Efficiency**: A significant advantage of categoricals is their memory efficiency. You compared the memory usage of a column stored as `object` type versus `category` type, noting a substantial reduction in memory usage with the latter.

Here's an example of creating an ordered categorical Series, which you practiced:

```
medals = pd.Categorical(medals_won, categories=["Bronze", "Silver", "Gold"], ordered=True)
```

This lesson equipped you with the knowledge to efficiently work with categorical data in pandas, enabling you to optimize data processing and analysis tasks.

The goal of the next lesson is to learn how to use the `groupby` method in pandas for analyzing and handling categorical data by grouping datasets based on specific categories and applying functions to these groups for detailed analysis.