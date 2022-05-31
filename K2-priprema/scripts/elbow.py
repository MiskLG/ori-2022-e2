# --- ODREDJIVANJE OPTIMALNOG K --- #
from kmeans import KMeans
import matplotlib.pyplot as plt

plt.figure()
sum_squared_errors = []
for n_clusters in range(2, 10):
    kmeans = KMeans(n_clusters=n_clusters, max_iter=100, normalize=True)
    kmeans.fit(data)
    sse = kmeans.sum_squared_error()
    sum_squared_errors.append(sse)

plt.plot(sum_squared_errors)
plt.xlabel('# of clusters')
plt.ylabel('SSE')
plt.show()