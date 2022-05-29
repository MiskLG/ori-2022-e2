from sklearn.linear_model import LogisticRegression


def load_data():
    X = []
    y = []

    with open('../data/customer_churn.csv', 'r') as file:
        for line in file:
            data = line.split(',')
            try:
                X.append([float(data[16])])
                y.append(str(data[20]))
            except:
                pass
    return X, y


if __name__ == '__main__':
    X, y = load_data()
    reg = LogisticRegression(random_state=1337, max_iter=1000).fit(X, y)
    x = [[5]]
    print(reg.predict(x))
    print(reg.predict_proba(x))