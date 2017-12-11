import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

tmdf = pd.read_csv('tmdb-movies.csv')
print(tmdf.info())
print(tmdf.shape)
'''Here we look at the general shape and format of our data.
We check for missing values.'''
print(tmdf[tmdf['genres'].isnull()])
'''Since we found some, and there aren't many, just go ahead and fill them in 
manually.'''
tmdf = pd.read_csv('tmdb_movies_filled.csv')
print(tmdf[tmdf['genres'].isnull()])

#Let's count how many rows have missing data
i = 0
for index, row in tmdf.iterrows():
    if row['budget_adj'] == 0:
        i += 1
print(i)

tmdf_nonzero = tmdf[tmdf['revenue_adj'] != 0]
tmdf_final = tmdf_nonzero[tmdf_nonzero['budget_adj'] != 0]
i = 0
for index, row in tmdf_final.iterrows():
    if row['budget_adj'] == 0:
        i += 1
    if row['revenue_adj'] == 0:
        i += 1
print(i)
#Now we know that none of the entries have values of 0 for budget or revenue 
#(I also checked user scores and runtime -- all good)
#Our final data set has 3,855 data points

tmdf_final.to_csv('tmdf_final.csv', index=False)

'''Now we look at ratings vs budget'''
#Histogram of data
tmdf_final['vote_average'].hist();
plt.title('Distribution of User Ratings')
plt.xlabel('Rating')
plt.ylabel('Count');

#Let's add the movie "quality designation". First let's figure out the relevant stats for user score
tmdf_final['vote_average'].describe()