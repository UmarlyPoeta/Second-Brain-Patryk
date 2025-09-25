## Updating categories

You learned about updating and collapsing categories in Pandas Series, focusing on how to clean and organize categorical data within your DataFrame. Here are the key points:

- **Renaming Categories**: You discovered that using the `cat.rename_categories()` method allows for the renaming of categories within a Series. For instance, renaming "Unknown Mix" to "Unknown" in a dataset can be achieved by passing a dictionary to this method, where the key is the current category and the value is the new category name.
    
- **Using Lambda Functions for Renaming**: You saw how lambda functions can be applied to rename categories, such as converting "male" and "female" to "Male" and "Female" in title case. This method is useful for batch operations on categories.
    
- **Collapsing Categories**: You learned the process of collapsing categories into broader ones using the `.replace()` method, which is helpful when simplifying categorical data. For example, collapsing various specific color categories into a primary color like "black".
    
- **Preserving Categorical Data Type**: It was highlighted that after using `.replace()`, the Series might lose its categorical data type, turning into an object data type. To maintain the categorical nature, you should convert the Series back to a categorical data type using `.astype('category')`.
    

Here's a snippet of code from the lesson that demonstrates renaming categories and converting them to uppercase:

```
# Create the my_changes dictionary
my_changes = {"Maybe?": "Maybe"}

# Rename the categories listed in the my_changes dictionary
dogs["likes_children"] = dogs["likes_children"].cat.rename_categories(my_changes)

# Use a lambda function to convert all categories to uppercase using upper()
dogs["likes_children"] =  dogs["likes_children"].cat.rename_categories(lambda c: c.upper())

# Print the list of categories
print(dogs["likes_children"].cat.categories)
```

This lesson equipped you with practical skills for handling categorical data, making your data cleaner and more accessible for analysis.

The goal of the next lesson is to teach you how to manage and manipulate categorical data in pandas, focusing on reordering categories within a Series for better data analysis and visualization.