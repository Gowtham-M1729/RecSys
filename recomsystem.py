import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df=pd.read_csv("Netflix_Data/NetflixData.csv",index_col=False)
filledna=df.fillna('')


def clean_data(x):
        return str.lower(x.replace(" ", ""))


features=['title','director','cast','listed_in','description']
filledna=filledna[features]


for feature in features:
    filledna[feature] = filledna[feature].apply(clean_data)


def create_soup(x):
    return x['title']+ ' ' + x['director'] + ' ' + x['cast'] + ' ' +x['listed_in']+' '+ x['description']


filledna['soup'] = filledna.apply(create_soup, axis=1)


count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(filledna['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

filledna=filledna.reset_index()


indices = pd.Series(filledna.index, index=filledna['title'])


def get_recommendations_new(title, cosine_sim=cosine_sim2):
    title=title.replace(' ','').lower()
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df['title'].iloc[movie_indices]



# get_recommendations_new('PK', cosine_sim2)




