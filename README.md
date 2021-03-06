# SQLAlchemy Homework - Surfs Up!

![surfs-up.png](/Instructions/Images/surfs-up.png)

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following outlines what you need to do.

Using this date, retrieve the last 12 months of precipitation data by querying the 12 preceding months of data. **Note** you do not pass in the date as a variable to your query.

![precipitation.png](/Output/precipitation.png)

Design a query to retrieve the last 12 months of temperature observation data (TOBS) of the most activate station.

Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?

![temperature.png](/Output/temperature.png)


Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.

![ttest.png](/Output/ttest.png)

You are looking to take a trip from August first to August seventh of this year, but are worried that the weather will be less than ideal. Using historical data in the dataset find out what the temperature has previously looked like.

![tripavgtemp.png](/Output/tripavgtemp.png)

Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures. You are provided with a function called `daily_normals` that will calculate the daily normals for a specific date. This date string will be in the format `%m-%d`. Be sure to use all historic TOBS that match that date string.

![rainsummary.png](/Output/rainsummary.png)
