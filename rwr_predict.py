import pickle, json, random
import genData, util

with open('./yelp/user_rwr_matrix.pickle') as f:
    matrix = pickle.load(f)

util.predict(matrix)
