import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OrdinalEncoder

"""
    Multiple variable regression with ordinal encoder for everything except last column
"""

def load_data():
    X = []
    y = []

    with open('../data/customer_churn.csv', 'r') as file:
        for line in file:
            data = line.split(',')
            try:
                X.append([str(data[0]), int(data[1]), int(data[2]), str(data[3]), str(data[4]), float(data[16])])
                y.append(str(data[20]))
            except:
                pass
    return X, y


if __name__ == '__main__':
    X, y = load_data()
    Xcopy = X.copy()
    ## Create encoder with columns that u want to transform from text to number based categories
    enc = OrdinalEncoder().fit([m[:-1] for m in X])
    X = enc.transform([m[:-1] for m in X])

    ## Create new matrix with encoded values followed by values that didnt need to be changed
    F = [np.append(X[i], (Xcopy[i][-1])) for i in range(0, len(X))]
    #print(F)

    ## Finish regression
    reg = LogisticRegression(random_state=1337, max_iter=1000).fit(F, y)
    x = [[1,1,1,1,1,60]]
    print(reg.predict(x))
    print(reg.predict_proba(x))