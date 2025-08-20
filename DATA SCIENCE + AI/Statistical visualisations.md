When you left 2 days ago, you worked on Quantitative comparisons and statistical visualizations, chapter 3 of the course Introduction to Data Visualization with Matplotlib. Here is what you covered in your last lesson:

You explored how to use histograms for quantitative comparisons, focusing on the distribution of variables within datasets. Specifically, you learned:

- Histograms represent the distribution of a variable by showing the frequency of observations within certain ranges (bins) of values. This contrasts with bar charts, which compare the value of a variable across different categories.
- You used data from the 2016 Olympic Games, comparing the heights and weights of medal winners in men's gymnastics and rowing. This illustrated how histograms provide insight into the spread and central tendency of data, which is not possible with simple bar charts.
- To create histograms in Python, you used Matplotlib's `ax.hist` method. For example, plotting the distribution of weights for Olympic medalists in rowing and gymnastics was achieved with the following code:

```
fig, ax = plt.subplots()
ax.hist(mens_rowing["Weight"], histtype='step', label="Rowing", bins=5)
ax.hist(mens_gymnastics["Weight"], histtype='step', label="Gymnastics", bins=5)
ax.set_xlabel("Weight (kg)")
ax.set_ylabel("# of observations")
ax.legend()
plt.show()
```

- You learned to customize histograms by adjusting the number of bins for finer or coarser views of the data distribution and by using the `histtype='step'` option to prevent bars from occluding each other, making it easier to compare multiple distributions.

This lesson equipped you with the skills to visualize and compare the distributions of quantitative data, enhancing your data analysis capabilities.

The goal of the next lesson is to teach how to use statistical plotting techniques, like error bars and boxplots, to visually summarize and compare data distributions effectively.