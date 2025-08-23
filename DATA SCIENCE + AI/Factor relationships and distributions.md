![[fact_dist.pdf]]

**Transcript**

## 1. Factor relationships and distributions

00:00 - 00:10

We previously looked at relationships between numerical variables. Of course, categorical variables, or factors, also have relationships.

## 2. Level of education: male partner

00:10 - 00:28

We haven't explored the categorical variables related to education level yet. Let's fix that! Checking the value_counts for education_man, we see that most men have an education level between primary and professional, with a few men in the "None" or "Other" categories.

## 3. Exploring categorical relationships

00:28 - 00:50

Categorical variables are harder to summarize numerically, so we often rely on visualizations to explore their relationships. Perhaps we are interested in the relationship between marriage duration and the education level of the man in the dissolved marriage. We could begin by making a histogram of the distribution of marriage duration

## 4. Exploring categorical relationships

00:50 - 01:18

and then layer in the information we have on male education level by setting education_man as the hue argument. The resulting histogram reinforces what we saw in value_counts: we have a lot of information on males with professional-level education. However, because the education levels are stacked on top of each other, the relationship between marriage duration and male education level isn't super clear.

## 5. Kernel Density Estimate (KDE) plots

01:18 - 01:57

Seaborn's Kernel Density Estimate or KDE plots address this issue. Similar to histograms, KDEs allow us to visualize distributions. KDEs are considered more interpretable, though, especially when multiple distributions are shown as they are here. Notice that the location of the peak marriage duration for each level of the male partner's education is more identifiable in this KDE plot than it was in the histogram. However, due to the smoothing algorithm used in KDE plots, the curve can include values that don't make sense, so it's important to set good smoothing parameters.

## 6. Kernel Density Estimate (KDE) plots

01:57 - 02:13

Here's an example: zooming in on the KDE plot showing the distribution of male education levels, we can see that the distribution seems to suggest that some couples had marriage durations of less than zero. That's impossible!

## 7. Kernel Density Estimate (KDE) plots

02:13 - 02:44

To fix this, we can use the cut keyword argument. cut tells Seaborn how far past the minimum and maximum data values the curve should go when smoothing is applied. When we set cut equal to zero, the curve will be limited to values between the minimum and maximum x values, here, the minimum and maximum values for marriage duration. The plot now shows only marriage durations greater than or equal to one year, the shortest marriage duration in the dataset.

## 8. Cumulative KDE plots

02:44 - 03:03

If we're interested in the cumulative distribution function, we can set the cumulative keyword argument to True. This graph describes the probability that marriage duration is less than or equal to the value on the x-axis for each level of male partner education.

## 9. Relationship between marriage age and education

03:03 - 03:21

Perhaps we are interested in whether divorced couples who got married when they were older typically have higher levels of education. We can create columns representing the approximate age at marriage for men and women by subtracting each partner's birth year from the marriage year.

## 10. Scatter plot with categorical variables

03:21 - 03:42

Then, we create a scatterplot using these variables on the x and y-axis. It looks like there is a positive correlation between them! Indeed, the Pearson correlation coefficient is 0.69. But the x and y values in scatter plots must be numerical. How do we introduce education level into our visual?

## 11. Scatter plot with categorical variables

03:42 - 04:01

One way to do this is to set the hue argument, which assigns a color to each data point based on values in a given column. Here, we set hue equal to education_man. The results suggest that men with a professional education level, represented with orange dots, may tend to get married later.

## 12. Let's practice!

04:01 - 04:05

Now it's your turn!