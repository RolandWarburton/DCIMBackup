# clustering dataset
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import json
import random

x1 = []
x2 = []

f = open("location_data.json")
data = json.load(f)

for point in data:
    if point["lat"] == 0.0 or point["lon"] == 0.0:
        continue
    else:
        x1.append(point["lat"])
        x2.append(point["lon"])

# create new plot and data
plt.plot()
X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
colors = ['b', 'b', 'b']
markers = ['.', ',', 'o', "v", "^", "<", ">", "1", "2", "3", "4", "s", "p", "*", "8"]


def get_random_color():
    r = random.randint(1, 8)
    if r == 1:
        return "blue"
    if r == 2:
        return "orange"
    if r == 3:
        return "green"
    if r == 4:
        return "red"
    if r == 5:
        return "magenta"
    if r == 6:
        return "steelblue"
    if r == 7:
        return "salmon"
    if r == 8:
        return "darkred"


color_labels = ["blue", "orange", "green", "red", "magenta", "steelblue", "salmon", "darkred"]

# KMeans algorithm
K = 8
kmeans_model = KMeans(n_clusters=K).fit(X)

plt.plot()
for i, l in enumerate(kmeans_model.labels_):
    plt.plot(x1[i], x2[i], color=color_labels[l], marker='.', ls='None')
    # plt.xlim([-38.1, -37.5])
    # plt.ylim([143, 147])

plt.show()
