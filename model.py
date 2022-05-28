import pandas as pd
from collections import defaultdict
import pickle

def get_predictions_for_all_users():

    trainset = pickle.load(open('trainset.pkl', 'rb'))
    svd_model = pickle.load(open('model.pkl', 'rb'))

    # Predict ratings for all pairs (u, i) that are NOT in the training set.
    testset = trainset.build_anti_testset()
    predicted_ratings_for_unrated_items = svd_model.test(testset)

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predicted_ratings_for_unrated_items:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)

    return top_n


def get_predictions(user_id):
    all_predictions = get_predictions_for_all_users()  # TODO: pickle this, so that you don't have call this function every time

    # Predict top 5 movie recommendations for the user
    n = 5
    for uid, user_ratings in all_predictions.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        all_predictions[uid] = user_ratings[:n]

    df_all_predictions = pd.DataFrame.from_dict(all_predictions)
    df_all_predictions_transpose = df_all_predictions.transpose()

    results = df_all_predictions_transpose.loc[user_id]
    print(results)
    recommended_movie_ids = [x[0] for x in results]

    movies = pd.read_csv("C:\Users\Karuna\PycharmProjects\MovieRecommendorSystem\movies.csv", usecols=['movieId', 'title'])

    recommended_movies = movies[movies['movieId'].isin(recommended_movie_ids)]
    recommended_movies = recommended_movies.to_string(index=False)
    return recommended_movies

# user_id = 67
# recommendations = get_predictions(user_id)
# print(recommendations)
