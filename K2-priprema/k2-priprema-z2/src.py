from sklearn.cluster import KMeans
from sklearn.preprocessing import Normalizer
import numpy as np
import matplotlib.pyplot as plt


def load_data():
    X = []
    y = []

    with open('../data/customer_churn.csv', 'r') as file:
        for line in file:
            data = line.split(',')
            try:
                X.append([float(data[16]), float(data[7])])
                y.append(str(data[20]))
            except:
                pass
    return X, y


def normilize(X):
    X = np.rot90(X)
    trans = Normalizer('l2')
    X = trans.transform(X)
    X = np.rot90(X)
    X = np.rot90(X)
    X = np.rot90(X)
    return X

def distance(x,y):
    return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

if __name__ == '__main__':
    X, y = load_data()
    X = normilize(X)
    kmeans = KMeans(n_clusters=2).fit(X)

    cluster1good=0
    cluster2good=0
    cluster1bad=0
    cluster2bad=0

    for point in zip(X,y):
        distance1 = distance(kmeans.cluster_centers_[0], point[0])
        distance2 = distance(kmeans.cluster_centers_[1], point[0])
        index = distance1 < distance2
        if index:
            if point[1] == 'TRUE\n':
                cluster1good += 1
            else:
                cluster1bad += 1
            plt.scatter(point[0][0],point[0][1],c='blue')
        else:
            if point[1] == 'TRUE\n':
                cluster2good += 1
            else:
                cluster2bad += 1
            plt.scatter(point[0][0],point[0][1],c='green')

    plt.scatter(kmeans.cluster_centers_[0][0], kmeans.cluster_centers_[0][1], marker='x', c='red')
    plt.scatter(kmeans.cluster_centers_[1][0], kmeans.cluster_centers_[1][1], marker='x', c='red')

    print(kmeans.cluster_centers_)
    print(cluster1good/(cluster1bad+cluster1good))
    print(cluster2good/(cluster2bad+cluster2good))
    plt.show()
