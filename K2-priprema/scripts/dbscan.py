import numpy as np
from sklearn.preprocessing import Normalizer

class Cluster(object):

    def __init__(self):
        self.data_ = []  # podaci koji pripadaju ovom klasteru


class DBScan(object):

    def __init__(self, epsilon=0.4, min_points=3, normalize=False):
        """
        :param epsilon: za epsilon okolinu
        :param min_points: minimalan broj tacaka unutar epsilon okoline
        :return: None
        """
        self.epsilon_ = epsilon
        self.min_points_ = min_points
        self.normalize_ = normalize
        self.data_ = None
        self.clusters_ = []

    def fit(self, data):
        # Prebacujem iz NumPy niza u listu
        self.data_ = np.array(data)
        if self.normalize_:
            self.normalize_data()
        self.data_ = self.data_.tolist()

        # Oznacim sve tacke kao 'not_visited'
        for point in self.data_:
            point.append('not_visited')

        # kada algoritam zavrsi, u self.clusters treba da budu klasteri (tipa Cluster)

        cluster_index = -1
        for point in self.data_:
            # Ako je tacka posjecenja
            if 'visited' == point[-1]:
                continue

            # Oznacimo je kao 'visited'
            point[-1] = 'visited'

            # Dobavimo 'komsije' te tacke
            neighbors = self.get_neighbors(point)

            if len(neighbors) < self.min_points_:
                point[-1] = 'noise'
            else:
                self.clusters_.append(Cluster())
                cluster_index += 1
                self.expand_cluster(point, neighbors, cluster_index)
        return self

    def expand_cluster(self, point, neighbors, cluster_no):
        # Dodamo tacku 'point' u klaster sa rednim brojem 'claster_no'
        self.clusters_[cluster_no].data_.append(point[:-1])

        # Za svaku tacku u skupu susjeda
        for pt in neighbors:
            # Ako nije oznacena - oznacimo je
            if 'visited' != pt[-1]:
                pt[-1] = 'visited'

                # Dobavimo njene komsije
                neighbors_pts = self.get_neighbors(pt)

                # Ako ima minimalan broj komsija
                if len(neighbors_pts) >= self.min_points_:
                    # Spojimo liste
                    neighbors.extend(neighbors_pts)

            # Provjeravamo da li se tacka nalazi u nekom klasteru
            point_in_cluster = False
            for c in self.clusters_:
                for cluster_point in c.data_:
                    if pt[:-1] == cluster_point:
                        point_in_cluster = True
                        break

                if point_in_cluster:
                    break

            # Ako tacka nije ni u jednom klasteru dodamo je
            if not point_in_cluster:
                self.clusters_[cluster_no].data_.append(pt[:-1])

    # Metoda koja vraca tacke koje su u epsilon okolini tacke 'point'
    def get_neighbors(self, point):
        points = []
        points.append(point)

        for pt in self.data_:
            if self.euclidean_distance(pt[:-1], point[:-1]) < self.epsilon_:
                points.append(pt)

        return points

        # Euklidsko rastojanje izmedju dvije tacke

    def euclidean_distance(self, x, y):
        sq_sum = 0
        for xi, yi in zip(x, y):
            sq_sum += (yi - xi) ** 2

        # Vracamo sqrt(sq_sum)
        return sq_sum ** 0.5

    def predict(self, chunk):
        chunk.append("hooter")
        nei = self.get_neighbors(chunk)
        nei.remove(chunk)
        nei = [n[:-1] for n in nei]
        nei = np.array(nei)
        nei = nei.tolist()
        print(nei)
        if len(nei) >= self.min_points_:
            for i in range(0, len(self.clusters_)):
                for data in self.clusters_[i].data_:
                    if data in nei:
                        return i

        return -1

    def normalize_data(self):
        self.data_ = np.rot90(self.data_)
        trans = Normalizer('l2')
        self.data_ = trans.transform(self.data_)
        self.data_ = np.rot90(self.data_)
        self.data_ = np.rot90(self.data_)
        self.data_ = np.rot90(self.data_)
