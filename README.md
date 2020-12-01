# sqlalchemy-challenge

Use Python and SQLAlchemy to do basic climate analysis and data exploration of sqllite climate database. 
All of the following analysis is completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

Design a query to retrieve the last 12 months of precipitation data.

Select only the date and prcp values.

Load the query results into a Pandas DataFrame and set the index to the date column.

Sort the DataFrame values by date.

Plot the results using the DataFrame plot method.

# Station Analysis

A query to calculate the total number of stations.

A query to find the most active stations.

List the stations and observation counts in descending order.

Find the  station that has the highest number of observations

query to retrieve the last 12 months of temperature observation data (TOBS).

Plot the results as a histogram with bins=12.

# Flask App

A Flask API based on the queries .

List all routes that are available.

/api/v1.0/precipitation
/api/v1.0/stations
/api/v1.0/<start> and /api/v1.0/<start>/<end>

Query the station and measurement tables in the database. Convert the result of these
queries into JSON and display.  

