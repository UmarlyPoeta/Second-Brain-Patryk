When you left 10 hours ago, you worked on Advanced Merging and Concatenating, chapter 3 of the course Joining Data with pandas. Here is what you covered in your last lesson:

You learned about advanced techniques for merging and concatenating DataFrames in pandas, focusing on filtering joins like semi-joins and anti-joins, and how to validate and combine data structures efficiently. Here are the key points:

- **Semi-joins**: You discovered that a semi-join filters the left DataFrame to only those rows that have a matching value in the right DataFrame. Unlike an inner join, it returns just the columns from the left DataFrame without duplicates. For instance, to find genres present in a table of top songs, you first performed an inner join and then used the `isin()` method to filter the genres.
    
- **Anti-joins**: You learned that an anti-join returns rows from the left DataFrame that do not have a matching row in the right DataFrame, again only returning columns from the left DataFrame. This was demonstrated by finding genres not present in the top tracks table, using a left join with the `indicator` argument set to True, and then filtering with the `_merge` column.
    
- **Concatenating DataFrames**: The lesson covered using `pandas.concat` to vertically combine DataFrames, which is crucial when you want to append rows from one DataFrame to another.
    
- **Data validation**: You learned techniques for validating your combined data structures to ensure accuracy and integrity in your data analysis.
    

Here's a snippet of code you worked with, demonstrating how to perform a semi-join:

```
# Merge the non_mus_tck and top_invoices tables on tid
tracks_invoices = non_mus_tcks.merge(top_invoices, on='tid')

# Use .isin() to subset non_mus_tcks to rows with tid in tracks_invoices
top_tracks = non_mus_tcks[non_mus_tcks['tid'].isin(tracks_invoices['tid'])]

# Group the top_tracks by gid and count the tid rows
cnt_by_gid = top_tracks.groupby(['gid'], as_index=False).agg({'tid':'count'})

# Merge the genres table to cnt_by_gid on gid and print
print(cnt_by_gid.merge(genres, on='gid'))
```

This code exemplifies how to merge tables and filter them to get meaningful insights, such as identifying top revenue-generating non-musical tracks by genre.

The goal of the next lesson is to teach you how to merge and concatenate DataFrames in pandas, specifically focusing on vertical concatenation, to combine data from various sources for comprehensive analysis.