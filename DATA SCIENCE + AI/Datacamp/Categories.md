You learned about managing categorical data in pandas, focusing on how to set, add, and remove categories from a Series. This is crucial for data cleaning and preparation, allowing for more efficient storage and faster computations. Here's a quick recap:

- **Setting Categories**: You discovered how to use `astype` to convert a column to a categorical type and `cat.set_categories` to define its categories. This method is essential for specifying which values are valid for a Series, dropping any values not listed.
    
    ```
    dogs['coat'].astype('category').cat.set_categories(['short', 'medium', 'long'], inplace=True)
    ```
    

- **Adding Categories**: The `cat.add_categories` method allows you to add new categories to a Series without affecting the existing data. This is useful when new data may contain additional categories not previously considered.
    
- **Removing Categories**: With `cat.remove_categories`, you can remove categories from a Series. This action sets any data points that had the removed category to NaN, effectively cleaning the data of unwanted or obsolete categories.
    

These tools are part of pandas' powerful capabilities for handling categorical data, making it easier to clean, process, and analyze information within your DataFrame.

The goal of the next lesson is to teach you how to clean and organize categorical data in Pandas by updating category names and collapsing multiple categories into broader ones.