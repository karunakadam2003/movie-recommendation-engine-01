import pandas as pd
from surprise import SVD, NMF, NormalPredictor, KNNBasic ,KNNWithMeans ,KNNWithZScore
from surprise import Reader, Dataset, accuracy
from surprise.model_selection import cross_validate, GridSearchCV, train_test_split
import pickle
import streamlit as st

# Downloading Movie Ratings Data

st.title('Algorithms Analysis that a web-streaming app used for Recommendation Engine.')
ratings = pd.read_csv("ratings.csv",usecols = ['userId','movieId','rating'])
reader = Reader(rating_scale = (0.5, 5.0))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Cross Validate the algorithms to benchmark the best performing algorithm
benchmark = []
for algorithm in [SVD(), NMF(), NormalPredictor(), KNNBasic(), KNNWithMeans(), KNNWithZScore()]:
    results = cross_validate(algorithm, data, measures=['RMSE'], cv=3, verbose=False)
    # Get results & append algorithm name
    df_results = pd.DataFrame.from_dict(results).mean(axis=0)
    df_results = df_results.append(pd.Series([str(algorithm).split(' ')[0].split('.')[-1]],index=['Algorithm']))
    print(df_results)
    st.write(df_results)
    benchmark.append(df_results)
# Root Mean Squared Error to compare the performance of different models.
# As SVD has the least RMSE value we will tune the hyper-parameters of SVD.

# Hyperparameter tuning on SVD using Grid search to pick out best params
param_grid = {'n_factors': [25, 30, 35, 40, 100], 'n_epochs': [15, 20, 25], 'lr_all': [0.001, 0.003, 0.005, 0.008], 'reg_all': [0.08, 0.1, 0.15, 0.02]}
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
gs.fit(data)
algo = gs.best_estimator['rmse']
print(gs.best_score['rmse'])
print(gs.best_params['rmse'])


st.write(gs.best_score['rmse'])
st.write(gs.best_params['rmse'])

params = gs.best_params
factors = params['rmse']['n_factors']
epochs = params['rmse']['n_epochs']
lr_value = params['rmse']['lr_all']
reg_value = params['rmse']['reg_all']

# Split the dataset into train and test data
trainset, testset = train_test_split(data, test_size=0.2)
# Assign the best parameters to SVD model
svd_model = SVD(n_factors=factors, n_epochs=epochs, lr_all=lr_value, reg_all=reg_value)
predictions = svd_model.fit(trainset).test(testset)
st.write("Accuracy: ",{accuracy.rmse(predictions)})

trainset = data.build_full_trainset()   # Build on entire data set
algo = SVD(n_factors=factors, n_epochs=epochs, lr_all=lr_value, reg_all=reg_value)
algo.fit(trainset)



pickle.dump(trainset, open("trainset.pkl",'wb')) # Pickle the trainset
#Serializing the model
pickle.dump(algo, open("model.pkl",'wb')) # Pickle the model
