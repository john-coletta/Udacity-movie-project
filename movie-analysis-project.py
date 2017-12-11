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

#Now lets add 'quality' to the df. They will be 4 levels: poor, below_avg, good, great

def qualityfnc(df):
    if df['vote_average'] < 5.7:
        return 'poor'
    elif 5.7 <= df['vote_average'] < 6.2:
        return 'below average'
    elif 6.2<= df['vote_average'] < 6.7:
        return 'good'
    else:
        return 'great'
    
tmdf_final['quality'] = tmdf_final.apply(qualityfnc, axis=1)
print(tmdf_final.head())

#Now let's make a box plot of the average budget for each category
sns.set(style='white', palette='muted')
budget_quality = tmdf_final.groupby('quality').mean()['budget_adj']
labels = ['poor','below average','good','great']
budgets = []
for x in labels:
    budgets.append(budget_quality[x])
    
plt.plot(budgets, 'o')
plt.ylabel('Budget (Ten Mil. Dollars)')
plt.xlabel('Quality')
plt.title('Quality vs Budget')
plt.xticks([0,1,2,3], labels)
plt.savfig('qualitybudget.png')
plt.show()
print(budget_quality)
#Another plot
ax = sns.stripplot(x='quality', y='budget_adj', data=tmdf_final, order=['poor','below average','good','great'], jitter=True)
ax.set(xlabel='Quality', ylabel='Budget (Hundred Mil. Dollars)', title='Quality vs Budget');
plt.savfig('qualitybudgetboxplot.png')
plt.show()

#Now let's look at movie length
tmdf_final['revenue_adj'].hist();
plt.title('Distribution of Adjusted Revenue')
plt.xlabel('Adjusted Revenue')
plt.ylabel('Count')
plt.show()

#Making categories for revenue
def successfnc(df):
    if df['revenue_adj'] < revenues[4]:
        return 'flop'
    elif revenues[4] <= df['revenue_adj'] < revenues[5]:
        return 'below average'
    elif revenues[5]<= df['revenue_adj'] < revenues[6]:
        return 'successful'
    else:
        return 'very successful'
    
tmdf_final['success'] = tmdf_final.apply(successfnc, axis=1)

#Now let's plot the average runtime for each category
runtime_success = tmdf_final.groupby('success').mean()['runtime']
labels1 = ['flop','below average','successful','very successful']
runtimes = []
for x in labels1:
    runtimes.append(runtime_success[x])
    
plt.plot(runtimes, 'o')
plt.ylabel('Runtime (Min)')
plt.xlabel('Success')
plt.title('Success vs Runtime')
plt.xticks([0,1,2,3], labels1)
plt.savfig('runtimesucces.png')
plt.show()
print(runtime_success)

#Boxplot of data
ax = sns.boxplot(x='success', y='runtime', data=tmdf_final, order=['flop','below average','successful','very successful'])
ax.set(xlabel='Success', ylabel='Runtime (Min)', title='Success vs Runtime');
plt.savfig('runtimeboxplot.png')
plt.show()

#Scatter plot of runtime vs quality
tmdf_final.plot.scatter('runtime','vote_average');
plt.xlabel('Runtime (Min)')
plt.ylabel('Average Vote Score')
plt.title('Runtime vs Average Score');
plt.savfig('runtimequalityscatter.png')
plt.show()

#Make a line of best fit
ax = sns.regplot(x='runtime',y='vote_average', data=tmdf_final)
ax.set(xlabel='Runtime (Min)', ylabel='Average Vote Score', title='Runtime vs Average Score');

slope, intercept, rvalue, pvalue, stderr = stats.linregress(tmdf_final['runtime'],tmdf_final['vote_average'])

print('The R value is {}, which is very low and shows that there is not a strong correlation \nbetween our two variables.'.format(rvalue))

'''Finaly, let's look at genres'''
tmdf_final['genres'] = tmdf_final['genres'].apply(lambda x: x.split('|'))

#Generate a dictionary of all the genres
genres = {}
for index, row in tmdf_final.iterrows():
    for x in row['genres']:
        if x not in genres:
            genres[x] = 1
        else:
            genres[x] += 1
			
#We are going to make dictionaries that have the genre as a key and the average rating and average revenue as values
genre_rating = {}
for index, row in tmdf_final.iterrows():
    for x in row['genres']:
        if x not in genre_rating:
            genre_rating[x] = row['vote_average']
        else:
            genre_rating[x] += row['vote_average']
            
for g in genre_rating:
    genre_rating[g] = genre_rating[g] / genres[g]
    
genre_rev = {}
for index, row in tmdf_final.iterrows():
    for x in row['genres']:
        if x not in genre_rev:
            genre_rev[x] = row['revenue_adj']
        else:
            genre_rev[x] += row['revenue_adj']
            
for g in genre_rev:
    genre_rev[g] = genre_rev[g] / genres[g]
	
#making labels, a multi-step process
genre_labels = []
for key in genres:
    genre_labels.append(key)
    
genre_ratings = []
for x in genre_labels:
    genre_ratings.append(genre_rating[x])

genre_labels2 = list(genre_labels)
for x in range(len(genre_labels2)):
    genre_labels2[x] = genre_labels2[x] + ' ({})'.format(genres[genre_labels2[x]])
    

    
plt.figure(figsize=(20,6))    
sns.set_style('whitegrid')
ax = sns.stripplot(x=genre_labels2, y=genre_ratings, color='b', size=7)
ax.set(xlabel='Genre (Total Count)', ylabel='Average Rating', title='Average Rating by Genre')

for tick in ax.get_xticklabels():
    tick.set_rotation(45)
	
plt.savfig('genrerating.png')
plt.show()
#Now revenue
genre_revs = []
for x in genre_labels:
    genre_revs.append(genre_rev[x])
    
plt.figure(figsize=(20,6))    
sns.set_style('whitegrid')
ax = sns.stripplot(x=genre_labels2, y=genre_revs, color='b', size=7)
ax.set(xlabel='Genre (Total Count)', ylabel='Average Revenue (Hudred Mil. Dollars)', title='Average Revenue by Genre')

for tick in ax.get_xticklabels():
    tick.set_rotation(45)
	
plt.savfig('genrerevenue.png')
plt.show()