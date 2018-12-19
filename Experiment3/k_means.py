from sklearn import metrics
from sklearn import datasets
from sklearn.cluster import  KMeans
dataset = datasets.load_iris()
X = dataset.data
y = dataset.target
kmeans_model = KMeans(n_clusters=3,random_state=1).fit(X)
labels = kmeans_model.labels_
print(metrics.silhouette_score(X,labels,metric='euclidean'))
