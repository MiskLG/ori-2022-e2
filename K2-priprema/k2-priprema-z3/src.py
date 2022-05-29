import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split

def load_data():
    X = []
    y = []

    with open('../data/customer_churn.csv', 'r') as file:
        for line in file:
            data = line.split(',')
            try:
                X.append([str(data[4]), str(data[5]), float(data[6]), float(data[17]), float(data[14]), float(data[8])])
                y.append(str(data[20]))
            except:
                pass
    return X, y


if __name__ == '__main__':
    X, y = load_data()
    Xcopy = X.copy()
    enc = OrdinalEncoder().fit([m[1:3] for m in X])
    X = enc.transform([m[1:3] for m in X])
    X = [np.append(X[i], (Xcopy[i][3:6])) for i in range(0, len(X))]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1337)

    print(X_train)
    ## Finish regression
    reg = LogisticRegression(random_state=1337, max_iter=1000).fit(X_train, y_train)
    print(reg.score(X_test, y_test))