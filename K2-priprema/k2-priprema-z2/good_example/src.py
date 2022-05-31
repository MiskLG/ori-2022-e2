from kmeans import KMeans
from sklearn.preprocessing import Normalizer
import numpy as np
import matplotlib.pyplot as plt


def load_data():
    X = []
    y = []

    with open('../../data/customer_churn.csv', 'r') as file:
        for line in file:
            data = line.split(',')
            try:
                X.append([float(data[16]), float(data[7])])
                y.append(str(data[20]))
            except:
                pass
    X = np.array(X)
    y = np.array(y)
    return X, y

def euclidean_distance(x, y):
    sq_sum = 0
    for xi, yi in zip(x, y):
        sq_sum += (yi - xi) ** 2

    # vracamo sqrt(sq_sum)
    return sq_sum ** 0.5


if __name__ == '__main__':
    X, y = load_data()
    kmeans = KMeans(n_clusters=2,normalize=True).fit(X)

    ## elbow
    plt.figure()
    sum_squared_errors = []
    for n_clusters in range(2, 10):
        kmeans = KMeans(n_clusters=n_clusters, max_iter=10, normalize=True)
        kmeans.fit(X)
        sse = kmeans.sum_squared_error()
        sum_squared_errors.append(sse)

    plt.plot(sum_squared_errors)
    plt.xlabel('# of clusters')
    plt.ylabel('SSE')
    plt.show()

    kmeans = KMeans(n_clusters=2, max_iter=10, normalize=True)
    kmeans.fit(X)
    X = kmeans.data_
    plt.figure()
    colors = ['blue','green']
    cluster_data = [[0,0] for m in kmeans.clusters_]
    # decent code goes through every point and
    for point in zip(X, y):
        index = 0
        distance = np.inf
        for i in range(0, kmeans.n_clusters_):
            calc_distance = euclidean_distance(point[0], kmeans.clusters_[i].center_)
            if  calc_distance < distance:
                index = i
                distance = calc_distance
        if point[1] == 'TRUE\n':
            cluster_data[index][0] += 1
        else:
            cluster_data[index][1] += 1
        plt.scatter(point[0][0], point[0][1], c=colors[index])

    plt.scatter(kmeans.clusters_[0].center_[0], kmeans.clusters_[0].center_[1], marker='x', c='red')
    plt.scatter(kmeans.clusters_[1].center_[0], kmeans.clusters_[1].center_[1], marker='x', c='red')

    print(cluster_data[0][0] / (cluster_data[0][0] + cluster_data[0][1]))
    print(cluster_data[1][0] / (cluster_data[1][0] + cluster_data[1][1]))
    plt.show()
