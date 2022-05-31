from sklearn.preprocessing import Normalizer
import numpy as np
import random as random
import copy as copy


class Cluster(object):

    def __init__(self, center):
        self.center_ = center
        self.data_ = []  # podaci koji pripadaju ovom klasteru

    def recalculate_center(self):
        # centar klastera se racuna kao prosecna vrednost svih podataka u klasteru
        new_center = [0 for i in range(len(self.center_))]
        for datum in self.data_:
            for i in range(len(datum)):
                new_center[i] += datum[i]

        n = len(self.data_)
        if n != 0:
            self.center_ = [x / n for x in new_center]


class KMeans(object):

    def __init__(self, n_clusters=8, max_iter=10, normalize=False):
        """
        :param n_clusters_: broj grupa (klastera)
        :param max_iter_: maksimalan broj iteracija algoritma
        :param normalize_: boolean da li da se podaci normalizuju ili ne
        :return: None

        Normalizer radi za 2 ili vise dimenzije, za jednu dimenziju moguce da treba da se podese podaci
        """
        self.data_ = None
        self.n_clusters_ = n_clusters
        self.max_iter_ = max_iter
        self.clusters_ = []
        self.normalize_ = normalize

    def fit(self, X):
        self.data_ = X  # lista N-dimenzionalnih podataka
        if self.normalize_:
            self.normalize_data()

        # kada algoritam zavrsi, u self.clusters treba da bude "n_clusters" klastera (tipa Cluster)

        # dimenzije prostora
        dimensions = len(self.data_[0])
        # Napravimo n random tacaka i postavimo ih kao center klastera
        self.get_random_points()

        iter_no = 0
        did_not_move = False
        while iter_no <= self.max_iter_ and (not did_not_move):
            # Ispraznimo podatke koji pripadaju klasteru
            for cluster in self.clusters_:
                cluster.data_ = []

            for chunk in self.data_:
                # Nadjemo indeks klastera kom pripada tacka
                cluster_index = self.predict(chunk)
                # Dodamo tu tacku u taj klaster da bismo mogli izracunati centar
                self.clusters_[cluster_index].data_.append(chunk)

            # Preracunamo centar
            did_not_move = True
            for cluster in self.clusters_:
                old_center = copy.deepcopy(cluster.center_)
                cluster.recalculate_center()

                if ((cluster.center_ == old_center).all()) and did_not_move:
                    did_not_move = False

            iter_no += 1

        return self

    def predict(self, chunk):
        # podatak pripada onom klasteru cijem je centru najblizi (po euklidskoj udaljenosti)
        # kao rezultat vratiti indeks klastera kojem pripada
        if self.data_ is None:
            exit("FIT DATA FIRST")
        min_distance = None
        cluster_index = None
        for index in range(len(self.clusters_)):
            distance = self.euclidean_distance(chunk, self.clusters_[index].center_)
            if min_distance is None or distance < min_distance:
                cluster_index = index
                min_distance = distance

        return cluster_index

        # Euklidsko rastojanje izmedju dvije tacke

    def euclidean_distance(self, x, y):
        sq_sum = 0
        for xi, yi in zip(x, y):
            sq_sum += (yi - xi) ** 2

        # vracamo sqrt(sq_sum)
        return sq_sum ** 0.5

    def get_random_points(self):
        points = []
        for i in range(self.n_clusters_):
            point = self.data_[random.randint(0, len(self.data_)-1)]
            breakp = False
            for p in points:
                if (p == point).all():
                    breakp = True
            if breakp:
                i -= 1
                continue
            points.append(point)
            self.clusters_.append(Cluster(point))

    def sum_squared_error(self):
        # SSE (sum of squared error)
        # unutar svakog klastera sumirati kvadrate rastojanja izmedju podataka i centra klastera
        if self.data_ is None:
            exit("FIT DATA FIRST")
        sse = 0
        for cluster in self.clusters_:
            for chunk in cluster.data_:
                sse += self.euclidean_distance(cluster.center_, chunk)

        return sse ** 2

    def normalize_data(self):
        self.data_ = np.rot90(self.data_)
        trans = Normalizer('l2')
        self.data_ = trans.transform(self.data_)
        self.data_ = np.rot90(self.data_)
        self.data_ = np.rot90(self.data_)
        self.data_ = np.rot90(self.data_)

