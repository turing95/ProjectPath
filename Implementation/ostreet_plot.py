import osmnx as ox
import matplotlib.pyplot as plt


place_name = "Como, CO, Lombardy, Italy"

graph = ox.graph_from_place(place_name)

# print(type(graph))

fig, ax = ox.plot_graph(graph)

plt.show()
