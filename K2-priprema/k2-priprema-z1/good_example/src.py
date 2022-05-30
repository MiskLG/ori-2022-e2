from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from LinearRegressionClass import *

def load_data():
    X = []
    y = []

    with open('../../data/customer_churn.csv', 'r') as file:
        for line in file:
            data = line.split(',')
            try:
                X.append(float(data[16]))
                y.append([str(data[20])])
            except:
                pass
    return X, y

    return y


if __name__ == '__main__':
    X, y = load_data()
    ## can use both
    y = OneHotEncoder().fit_transform(y).toarray()
    y1 = OrdinalEncoder().fit_transform(y)
    y = [m[0] for m in y]
    reg = LinearRegression().fit(X, y)
    print(reg.predict(5))