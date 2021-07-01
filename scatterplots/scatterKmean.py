import matplotlib.pyplot as plt
import json

x = []
y = []

f = open("location_data.json")
data = json.load(f)

for point in data:
    if point["lat"] == 0.0 or point["lon"] == 0.0:
        continue
    else:
        x.append(point["lat"])
        y.append(point["lon"])

plt.plot(x, y, '.', color='black', markersize=3)

# add home
home_x = [-37.84578427926508]
home_y = [145.29495516728795]
plt.plot(home_x, home_y, '.', color="red", markersize=8)

plt.show()
