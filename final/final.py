import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from wordcloud import WordCloud

pd.options.mode.chained_assignment = None

filenames = ['amazon_prime_titles.csv', 'disney_plus_titles.csv', 'hulu_titles.csv', 'netflix_titles.csv']
platforms = ['Amazon Prime', 'Disney+', 'Hulu', 'Netflix']

def preprocessing(filenames) -> pd.DataFrame:
    '''
    As is shown in the name... \\
    You have to call this function before all other functions.
    '''
    data = []
    for i in range(len(filenames)):
        data.append(pd.read_csv(filenames[i]))
        data[i].drop(columns=['show_id', 'director', 'cast'], inplace=True)
        '''
            There are dirty data in the column 'rating'.
            Some values in this column denotes the info of 'duration', not 'rating'
            I plan to clean the data here at the very beginning.
        '''
        for index, row in data[i].iterrows():
            if str(row['rating']).endswith('min') or str(row['rating']).endswith('Season') or str(row['rating']).endswith('Seasons'):
                data[i]['duration'][index] = data[i]['rating'][index]
                data[i]['rating'][index] = np.NaN
    return data

# preprocessing is above this line, specific figures and graphs functions are below this line

def type_ratio(data, platforms) -> None:
    '''
    save the ratio of types pie chart of the platforms
    '''
    labels = ['Movie', 'TV Show']
    # plt.axis('off')
    os.system("rm -rf ./type_ratio")
    os.system("mkdir type_ratio")
    for i in range(len(data)):
        num_movie = len(data[i][data[i]['type'] == 'Movie'])
        num_tv_show = len(data[i][data[i]['type'] == 'TV Show'])
        plt.figure()
        plt.pie([num_movie, num_tv_show], labels=labels, autopct='%.2f%%')
        plt.title('Type ratio of {}'.format(platforms[i]))
        plt.savefig('./type_ratio/{}_type_ratio.png'.format(platforms[i]), bbox_inches='tight')

def genres(data, platforms) -> None:
    '''
    save the genres pie chart of the platforms
    '''
    os.system("rm -rf ./genres")
    os.system("mkdir genres")
    for i in range(len(data)):
        topics = {}
        for labels in data[i]['listed_in']:
            for topic in labels.split(', '):
                topics[topic] = topics.setdefault(topic, 0) + 1

        # this part is to deal some dirty data
        if 'and Culture' in topics:
            topics['Culture'] = topics['and Culture']
            del topics['and Culture']

        thiner_topics = {}
        for k, v in topics.items():
            if v / len(data[i]) >= 0.1:
                thiner_topics[k] = v
            else:
                thiner_topics['Other'] = thiner_topics.setdefault('Other', 0) + v
        # dirty data processing ends

        plt.figure()
        plt.title('Genres of {}'.format(platforms[i]))
        plt.pie(thiner_topics.values(), labels=thiner_topics.keys(), autopct='%.2f%%', pctdistance=0.8)
        plt.savefig('./genres/{}_genres.png'.format(platforms[i]), bbox_inches='tight')

def added_date(data, platforms) -> None:
    '''
    save the charts of the adding date of the contents of each platform
    '''
    os.system("rm -rf ./contents_update")
    os.system("mkdir contents_update")
    for i in range(len(data)):
        temp = data[i][['date_added']].dropna()
        temp['year'] = temp['date_added'].apply(lambda x : x.split(', ')[-1])
        temp['month'] = temp['date_added'].apply(lambda x : x.lstrip().split(' ')[0])
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][::-1]
        df = temp.groupby('year')['month'].value_counts().unstack()
        for month in month_order:
            if month not in set(df.columns):
                df[month] = np.NaN
        df = df.fillna(0)[month_order].T

        plt.figure(figsize=(10, 7))
        plt.pcolor(df, cmap='afmhot_r', edgecolors='white', linewidths=2) # heatmap
        plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
        plt.yticks(np.arange(0.5, len(df.index), 1), df.index)

        plt.title('{} Contents Update'.format(platforms[i]))
        cbar = plt.colorbar()

        cbar.ax.tick_params(labelsize=8) 
        cbar.ax.minorticks_on()
        plt.savefig('./contents_update/{}_contents_update.png'.format(platforms[i]))

def minimum_age(data, platforms) -> None:
    '''
    quantify the minimum age to see the contents of each platform
    '''

    quantify_ratings = {
        'TV-Y': 2,
        'TV-Y7': 7,
        'TV-Y7-FV': 7,
        'TV-G': 0,
        'TV-PG': 7, # may be unsuitable for younger children
        'TV-14': 14,
        'TV-MA': 17,
        'TV-NR': np.nan,
        'G': 0,
        'PG': 7, # may be not suitale for children
        'PG-13': 13,
        'R': 17,
        'NC-17': 18,
        'NR': np.nan,
        'NOT_RATE': np.nan,
        'NOT RATED': np.nan,
        'UR': np.nan,
        'UNRATED': np.nan,
        'ALL': 0,
        'ALL_AGES': 0,
        '18+': 18,
        'AGES_18_': 18,
        'AGES_16_': 16,
        '16+': 16,
        '16': 16,
        '13+': 13,
        '7+': 7
    }

    for i in range(len(data)):
        print('The contents of {} have a mean age at {:.2f}'.format(platforms[i], np.mean(pd.Series([quantify_ratings[rating] for rating in data[i]['rating'].dropna()]).dropna())))

def producing_countries(data, platforms):
    '''
    find the most productive countries
    '''
    os.system("rm -rf ./producing_countries")
    os.system("mkdir producing_countries")
    for i in range(len(data)):
        countries = {}
        for labels in data[i]['country'].dropna():
            # print(labels)
            for country in labels.split(', '):
                countries[country] = countries.setdefault(country, 0) + 1
        countries = sorted(countries.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)
        print('On {}, there are {} countries involved in production.'.format(platforms[i], len(countries)))
        top_countries = []
        top_counts = []
        for name, counts in countries[:5]:
            top_countries.append(name)
            top_counts.append(counts)
        plt.figure(figsize=(10, 7))
        plt.title('Top producing countries on {}'.format(platforms[i]))
        plt.bar(top_countries, top_counts, data=top_counts)
        for country, counts in zip(top_countries, top_counts):
            plt.text(country, counts + 0.05, '%.0f' % counts, ha='center', va='bottom')
        plt.savefig('./producing_countries/{}_producing_countries.png'.format(platforms[i]))
        
def movie_duration_analysis(data):
    '''
    find the movie durations of all the platforms
    '''
    all_movie_duration = []
    for i in range(len(data)):
        movie_filtered = data[i][data[i]['type'] == 'Movie']

        # There are some very dirty data which have 'Seasons' instead of 'min' for movies.
        dirty = movie_filtered[(movie_filtered['duration'].str.endswith('Seasons')) | (movie_filtered['duration'].str.endswith('Season'))].index
        movie_filtered.drop(dirty, inplace=True)
        all_movie_duration.extend(movie_filtered['duration'].dropna().str.replace(' min', '').values.astype(int))

    plt.figure()
    sns.set(style='darkgrid')
    sns.kdeplot(data=all_movie_duration, shade=True)
    plt.xlabel('Duration of movies')
    plt.savefig('movie_duration_distribution.png')

def median_movie_duration_by_year(data):
    '''
    find the median of movie durations of all the platforms by year.
    '''
    all_movie_duration = pd.DataFrame(columns=['duration'], index=['release_year'])
    for i in range(len(data)):
        if i == 2:
            continue
        '''
        Here I jump over Hulu due to its dirty table!!!!!
        '''
        movie_filtered = data[i][data[i]['type'] == 'Movie']
        dirty = movie_filtered[(movie_filtered['duration'].str.endswith('Seasons')) | (movie_filtered['duration'].str.endswith('Season'))].index
        movie_filtered.drop(dirty, inplace=True)
        movie_filtered['duration'].dropna(inplace=True)
        movie_filtered['duration'] = movie_filtered['duration'].apply(lambda x: x.replace(' min', ''))
        movie_focus = movie_filtered.drop(columns=['title', 'type', 'country', 'date_added', 'rating', 'listed_in'])
        all_movie_duration = pd.concat([all_movie_duration, movie_focus])

    annual_movie_length_median = all_movie_duration.groupby(['release_year']).median()
    plt.plot(annual_movie_length_median.index, annual_movie_length_median['duration'].values)
    plt.savefig('annual_movie_length_median.png')
    
def description_wordcloud(data, platforms):
    '''
    Make wordclouds of descriptions 
    '''
    os.system("rm -rf ./wordcloud")
    os.system("mkdir wordcloud")

    for i in range(len(data)):
        
        descriptions = data[i]['description'].dropna()
        words = []
        for single_movie_description in descriptions:
            single_movie_description.replace(',.?:\'\";', '')
            words += re.sub(r'[^\w\s]', '', single_movie_description).split()
        cloud = WordCloud(width=1600, height=800, background_color='white').generate(' '.join(words))
        plt.axis('off')
        plt.imshow(cloud, interpolation='bilinear')
        plt.title('Wordcloud for {}'.format(platforms[i]))
        plt.savefig('./wordcloud/{}_wordcloud.png'.format(platforms[i]), bbox_inches='tight')


data = preprocessing(filenames)
type_ratio(data, platforms)
genres(data, platforms)
added_date(data, platforms)
minimum_age(data, platforms)
producing_countries(data, platforms)
movie_duration_analysis(data)
median_movie_duration_by_year(data)
description_wordcloud(data, platforms)