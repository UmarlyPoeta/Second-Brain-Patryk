



Let's see how we convert exploratory data analysis into action! We'll start by looking at class frequencies.

## 2. Why perform EDA?

00:09 - 00:23

Recall that EDA is performed for a variety of reasons, like detecting patterns and relationships in data, generating questions or hypotheses, or to prepare data for machine learning models.

1. 1 Image credit: https://unsplash.com/@simonesecci

## 3. Representative data

00:23 - 00:52

There's one requirement our data must satisfy regardless of our plans after performing EDA - it must be representative of the population we wish to study. For example, if we collect data with the aim of analyzing the relationship between education level and income in the USA, then we would need to collect this data from adults residing in the USA, and can't rely on data from residents of France.

1. 1 Image credits: https://unsplash.com/@cristina_glebova; https://unsplash.com/@nimbus_vulpis

## 4. Categorical classes

00:52 - 01:16

With categorical data, one of the most important considerations is about the representation of classes, which is another term for labels. For example, say we collect data on people's attitudes to marriage. As part of our data collection we find out their marital status, with the classes including single, married, and divorced.

## 5. Class imbalance

01:16 - 01:51

When we perform EDA we realize only 50 people were married, while 700 were divorced and the remaining 250 were single. Do we think that this sample accurately represents the general public's opinion about marriage? Are divorced people more likely to have a negative view towards marriage? This is an example of class imbalance, where one class occurs more frequently than others. This can bias results, particularly if this class does not occur more frequently in the population.

## 6. Class frequency

01:51 - 02:02

We've been counting the number of observations per class using pandas dot-value_counts, like here, where we see how many flights went to different destinations in our planes dataset.

## 7. Relative class frequency

02:02 - 02:33

Say that we know 40 percent of internal Indian flights go to Delhi. We can use value_counts method again, but this time set the normalize keyword argument equal to True. This returns the relative frequencies for each class, showing that Delhi only represents 11-point-eight-two percent of destinations in our dataset. Again, this could suggest that our data is not representative of the population - in this case, internal flights in India.

## 8. Cross-tabulation

02:33 - 02:51

Another method for looking at class frequency is cross-tabulation, which enables us to examine the frequency of combinations of classes. Let's look at flight route frequencies. We'll start by calling pandas-dot-crosstab function.

## 9. Select index

02:51 - 02:58

Next we select the column to use as the index for the table, in this case the Source.

## 10. Select columns

02:58 - 03:10

Lastly, we pass the Destination. Values in this column will become the names of the columns in the table, and the values will be the count of combined observations.

## 11. Cross-tabulation

03:10 - 03:17

We see the most popular route is from Delhi to Cochin, making up 4318 flights.

## 12. Extending cross-tabulation

03:17 - 03:35

Say we know the median price for all internal flight routes in India. Here they are for the routes in our dataset, measured in Indian Rupees. We can calculate the median price for these routes in our DataFrame, and compare the difference to these expected values.

## 13. Aggregated values with pd.crosstab()

03:35 - 04:02

We do this by adding two keyword arguments to pd-dot-crosstab. We pass the Price column to the values argument, and use aggfunc to select what aggregated calculation we want to perform. We can pass a summary statistic as a string, in this case setting it equal to median. The results show median values for all possible routes in the dataset.

## 14. Comparing sample to population

04:02 - 04:17

Comparing our prices with the expected values, most are similar. However, routes from Banglore to Delhi and New Delhi are more expensive in our dataset, suggesting they aren't representative of the population.

## 15. Let's practice!

04:17 - 04:22

Now it's your turn to look at class frequencies!