import datetime
import joblib

import pandas as pd
import numpy as np
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import random
import implicit
from implicit.evaluation import  *
from implicit.als import AlternatingLeastSquares as ALS


HISTORY_PATH    = './data/history_test.csv'
FOOD_PATH       = './data/food_test.csv'

history = pd.read_csv(HISTORY_PATH)
food = pd.read_csv(FOOD_PATH)

history.columns = ['user_id', 'food_id', 'date(utc)']

data = history.merge(
    food, on='food_id'
)[['user_id', 'food_id', 'food_category', 'date(utc)']].sort_values(
    'user_id'
).reset_index(drop=True)

data['date(utc)'] = data['date(utc)'].astype('datetime64')

data.reset_index(inplace=True, drop=True)

train_df = data[['user_id', 'food_id', 'food_category']]
train_df['values'] = 1

train_sum = train_df.groupby(['user_id', 'food_category'])['values'].sum().reset_index()

user_id = list(np.sort(train_sum['user_id'].unique()))
food_category = list(train_sum['food_category'].unique())
values = list(train_sum['values'])

rows = train_sum['user_id'].astype('category').cat.codes
cols = train_sum['food_category'].astype('category').cat.codes

sparse_train = sparse.csr_matrix((values, (rows, cols)))

tmp = train_sum
tmp['cat_vec'] = cols
category = tmp.drop_duplicates('food_category').sort_values(by='cat_vec')['food_category'].to_list()

als_model = ALS(
    factors=64,
    regularization=0.01,
    iterations=30,
)

als_model.fit(sparse_train)

joblib.dump(als_model, './data/als_model.pkl') 
reverse_category = {name: i for i, name in enumerate(category)}
joblib.dump(reverse_category, './data/als_category.pkl')
print('DONE: ALS model created.')