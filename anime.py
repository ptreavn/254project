import pandas as pd
import numpy as np
import csv as cv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import argparse

# helper function for creating bag of words


def create_soup(x):
    result = x['Anime Title']

    if x['Studio'] != 'n/a':
        result += ' ' + x['Studio']
    if x['Source Material'] != 'n/a':
        result += ' ' + x['Source Material']
    if x['Genre'] != 'n/a':
        result += ' ' + x['Genre']
    if x['VAs'] != 'n/a':
        result += ' ' + x['VAs']

    punc = '[],\'\"'

    for ele in result:
        if ele in punc:
            result = result.replace(ele, "")

    return result

# helper function for recommendation algorithms


def get_recs(id, cosine_sim):
    # get the index of the anime that matches the id
    id2 = '\'' + str(id) + '\''
    idx = (df.loc[df['Id'] == id2].index[0])

    # find sim score of the inputed anime with all other animes
    sim_scores = list(enumerate(cosine_sim[idx]))

    # sort based on sim scores desc
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # get recommended animes index
    anime_indices = [i[0] for i in sim_scores]
    for i in range(len(sim_scores)):
        if i > 10:
            break
        else:
            print(df['Anime Title'].iloc[anime_indices[i]])

    # return df['Anime Title'].iloc[anime_indices]


if __name__ == "__main__":
    # reading in arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--number_of_anime', type=int, default=1)
    parser.add_argument('--anime_id', type=int)
    args = parser.parse_args()

    if args.number_of_anime > 1 or args.anime_id:
        if args.number_of_anime > 1:
            user_animes = []
            prompt = int(input("Enter the anime ids: "))

            for i in range(1, args.number_of_anime):
                ele = int(input())
                user_animes.append(ele)

        # read csv file into dataframe
        df = pd.read_csv('top_and_bottom_anime.csv')
        # print(df.shape)

        # preprocessing the csv file
        data = range(len(df))
        for i in data:
            if df.loc[i]['VAs'] == ' \'\'':
                df = df.drop(labels=i, axis=0)

        # make a bag of words csv from database of animes
        df['soup'] = df.apply(create_soup, axis=1)
        df.to_csv("anime_soup.csv", index=None)

        # cosine similarity algorithm
        count = CountVectorizer()
        count_matrix = count.fit_transform(df['soup'])
        count_matrix.shape

        cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
        df = df.reset_index()

        for i in user_animes:
            get_recs(i, cosine_sim2)
    else:
        raise Exception(
            "python .\\anime.py --number_of_anime \'or\' --anime_id \'id number\'")
