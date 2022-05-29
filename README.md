**# Hi, I'm Karuna! 👋**

# movie-recommendation-engine-



# Movie Recommendation Using Multiple Machine Learning Algorithms


The idea is to make use of filtering and clustering techniques to suggest items of interest to users.
Upon usage, the recommender system will be able to understand the user better and suggest movies that are more likely to be rated higher.
## Appendix

Here are the average RMSE, MAE and total execution time of various algorithms (with their default parameters) on a 3-fold cross-validation procedure.

We will use __RMSE__(Root Mean Square Error) as our accuracy metric for the predictions.

We will be comparing SVD, NMF, Normal Predictor, KNN Basic and will be using the one which will have least RMSE value.


-  __Normal Predictor__: It predicts a random rating based on the distribution of the training set, which is assumed to be normal. It's a basic algorithm that does not do much work but that is still useful for comparing accuracies.

- __SVD__: It got popularized by Simon Funk during the Netflix prize and is a Matrix Factorized algorithm. If baselines are not used, it is equivalent to PMF.

- __NMF__: It is based on Non-negative matrix factorization and is similar to SVD.

- __KNN Basic__: This is a basic collaborative filtering algorithm method.

- __KNNWithMeans__:A basic collaborative filtering algorithm, taking into account the mean ratings of each user.
	
- __KNNWithZScore__:A basic collaborative filtering algorithm, taking into account the z-score normalization of each user.

## Deployment

This project is deployed on Heroku


[Deployed Project Link](https://movie-recommendation-engine-01.herokuapp.com/)
## Roadmap

- Cross Validate the algorithms to benchmark the best performing algorithm


- Root Mean Squared Error to compare the performance of different models.
- As SVD has the least RMSE value we will tune the hyper-parameters of SVD.

- Hyperparameter tuning on SVD using Grid search to pick out best parameters
- __No of ratings per item__
![newplot](https://user-images.githubusercontent.com/90612970/170855992-a57e0000-94e5-40ff-89d1-7afa1fab84c7.png)
- __User Interface__
![Movie recommendation system](https://user-images.githubusercontent.com/90612970/170856109-6b8d32cb-4b2b-4cad-857b-c77500cb3aaf.png)
## Demo

Insert gif or link to demo


## Presentation

[Presentation](https://www.canva.com/design/DAFB9pE8he8/C3QAQrCcVTupONYWyxXiKw/view?utm_content=DAFB9pE8he8&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink)


## Datasets

[movie.csv](https://docs.google.com/spreadsheets/d/1PosdcPTZXtHm3TUzZ-v4-WJUCwj6OMvzdoB_A_voqnU/edit?usp=sharing)

[ratings.csv](https://docs.google.com/spreadsheets/d/1jef371IQpU5PCf0oY4AcWrjDYeal5-8H58t1VcXOBgo/edit?usp=sharing)
