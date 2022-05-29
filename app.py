import pickle
import streamlit as st
import requests
import pandas as pd
import surprise
from collections import defaultdict
import time
import pyrebase
from datetime import datetime
import json
from streamlit_lottie import st_lottie,st_lottie_spinner

# Configuration Key

firebaseConfig = {
  'apiKey': "AIzaSyBKiksfcBVH8SzkSFUof4WbfI9uhq0F6EY",
  'authDomain': "moviemania-fd222.firebaseapp.com",
  'projectId': "moviemania-fd222",
   'databaseURL' : "https://moviemania-fd222-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "moviemania-fd222.appspot.com",
  'messagingSenderId': "261609993182",
  'appId': "1:261609993182:web:7853c6b39d0e50095d234f",
  'measurementId': "G-3F4BC9GMYL"
}

st.set_page_config(page_title= "Movie_Mania",page_icon= ":tada:",layout="wide")
def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url('https://image.shutterstock.com/image-vector/online-cinema-art-movie-watching-260nw-584655766.jpg');
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

set_bg_hack_url()

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
# Database
db = firebase.database()
storage = firebase.storage()





# Deserializing the model

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

ratings_dict = pickle.load(open('rating_dict.pkl','rb'))
ratings = pd.DataFrame(ratings_dict)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json"

#lottie_json = load_lottieurl(lottie_url)

#st_lottie(lottie_json, key="hello",width=650,height = 600)

def fetch_poster(movie_id):
    print(movie_id)
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=020433237875b772d11d1b1dbfca89c1'
        print(url)
        data = requests.get(url)
        data = data.json()

        poster = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except KeyError:
        print(f"{movie_id}'s movie not found.")
        poster = "https://bitsofco.de/content/images/2018/12/broken-1.png"
    return poster

#pickle the output
def get_predictions_for_all_users():

    #pickle predictions

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

# with open('all_predictions.pkl', 'rb') as f :
#     all_predictions = pickle.load(f)
def get_predictions(user_id):
    all_predictions = get_predictions_for_all_users()
    # TODO: pickle this, so that you don't have call this function every time
    #pickle.dump(all_predictions, open("all_predictions.pkl", 'wb'))  # Pickle the trainset
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
    print(recommended_movie_ids)

    recommended_movies = movies[movies['movieId'].isin(recommended_movie_ids)]
    print(type(recommended_movies))
    recommended_movies_list = recommended_movies['title'].tolist()
    print(recommended_movies_list)
    recommended_movies = recommended_movies.to_string(index=False)
    print("Done")
    print(type(recommended_movies))

    posters = []
    print(recommended_movies)
    for i in recommended_movie_ids:
        print(i)
        print(fetch_poster(i))
        posters.append(fetch_poster(i))
    return recommended_movies_list,posters


st.sidebar.title("Movie Mania")

# Authentication
choice = st.sidebar.selectbox('Login/Signup',['Login','Sign up'])

email = st.sidebar.text_input('Please enter your email')
password = st.sidebar.text_input('Enter Password',type = 'password')
st.balloons()


def callback():
    st.session_state.button_clicked = True
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False
if choice == 'Sign up':
    handle = st.sidebar.text_input('Enter your app handle name',value = 'Default')
    submit = st.sidebar.checkbox('Take me to Movie Mania'  )

    if submit:
        try :
            user = auth.create_user_with_email_and_password(email,password)

            auth.send_email_verification(user['idToken'])
            auth.send_password_reset_email(email)
            st.success('Your account is created!')
            st.balloons()

            col1, col2 = st.columns(2)
            with col1:
                st.sidebar.image('images/movie-mania.jpg', width=300)
            with col2:
                st.sidebar.write('We have got you....')
                st.balloons()
        except:
            st.sidebar.text('Reenter your email.')
            print("Exception occured")

        # Sign in
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child(['Handle']).set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.title(' Welcome ', handle, ' To Movie Recommendations')
            st.info('Login via drop down selection')
            choice = st.checkbox("Login")
        except:
            st.sidebar.text("Invalid Credentials.")


if choice == 'Login':
        login =  st.sidebar.checkbox("Login")

        if login:
            user = auth.sign_in_with_email_and_password(email,password)
            user_id = st.selectbox(
                'Enter your user ID ', ratings['userId'].values
            )
            selected_movie_name = st.selectbox(
                'Select your favourite movie', movies['title'].values
            )

            recommendButton =  st.button("Show Recommendations")
            if recommendButton:
                print("In if")
                # recommend(selected_movie_name)
                # st.write(selected_movie_name)
                names, posters = get_predictions(user_id)
                print("Found Predictions")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.text(names[0])
                    st.image(posters[0])
                with col2:
                    st.text(names[1])
                    st.image(posters[1])

                with col3:
                    st.text(names[2])
                    st.image(posters[2])
                with col4:
                    st.text(names[3])
                    st.image(posters[3])
                with col5:
                    st.text(names[4])
                    st.image(posters[4])
                st.success("Thank you for visiting Movie Mania")








