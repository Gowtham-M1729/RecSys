import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
pd.options.mode.chained_assignment = None

df = pd.read_csv("./Netflix_Data/disney_plus_shows.csv")


data = df[['title','plot','director','actors','imdb_rating','genre','plot']]
data['actors'] = data['actors'].str.split(',').fillna('')
data['genre_splitted'] = data['genre'].str.split(',').fillna('')
data['director'] = data['director'].fillna('')
data['plot'] = data['plot'].fillna('')


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''


features = ['actors', 'genre', 'director']
for feature in features:
    data[feature] = data[feature].apply(clean_data)


def create_soup(x):
    return ' '.join(x['actors']) + ' ' + x['director'] + ' ' + ' '.join(x['genre'] + ' '.join(x['plot']))


data['soup'] = data.apply(create_soup, axis=1)


count = CountVectorizer()
count_matrix = count.fit_transform(data['soup'])
sim_matrix = cosine_similarity(count_matrix,count_matrix)
data = data.reset_index()
mapping = pd.Series(data.index, index=data['title'])


def extended_recommender(m_name):
    m_index = mapping[m_name]
    similarity_score = list(enumerate(sim_matrix[m_index]))
    similarity_score = sorted(similarity_score,key=lambda x:x[1],reverse=True)
    similarity_score = similarity_score[1:10]
    indices = [i[0] for i in similarity_score]
    return data.title.iloc[indices]


# print(extended_recommender('Toy Story'))