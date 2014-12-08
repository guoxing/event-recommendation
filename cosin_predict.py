import pickle, json
import util, genData

def genMatrix():
    with open(genData.REVIEW_PHX_TRAIN) as f:
        train = json.load(f)

    with open(genData.USER_HAS_REVIEW) as f:
        users = json.load(f)

    userDict = util.getUserIdMapping()
    n = len(users)

    ratings = [{} for _ in range(n)]
    square_sum = [0 for _ in range(n)]
    for review in train:
        user_idx = userDict[review['user_id']]
        ratings[user_idx][review['business_id']] = review['stars']
        square_sum[user_idx] += review['stars'] ** 2

    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        print i
        for j in range(n):
            if i == j: continue
            total_sum = 0
            for buz_id in ratings[i]:
                if buz_id in ratings[j]:
                    total_sum += ratings[i][buz_id] * ratings[j][buz_id]
            if square_sum[i] == 0 or square_sum[j] == 0:
                continue
            matrix[i][j] = total_sum / (square_sum[i] * square_sum[j]) ** 0.5
    with open('./yelp/user_cosin_matrix.pickle', 'w') as f:
        pickle.dump(matrix, f)
    return matrix

with open('./yelp/user_cosin_matrix.pickle') as f:
    matrix = pickle.load(f)

util.predict(matrix)
