import igraph as ig

# Initiate the graph
graph = ig.Graph(1)

# Add nodes aka vertices
graph.add_vertices(2)

# Add edges
graph.add_edges([(0, 1), (1, 2)])

# Delete edges
# graph.delete_edges()

# Delete vertices
# graph.delete_vertices()

# To get the id of an edge between two nodes
# graph.get_eid(nodeID_one, nodeID_two)

graph.add_edges([(2,0)])
graph.add_vertices(3)
graph.add_edges([(2,3),(3,4),(4,5),(5,3)])

# Draw graphs
#  Deterministic generators produce the same graph if you call them with exactly the same parameters, while stochastic
# generators produce a different graph every time.

#print(graph)

# Doesn't work
print(ig.summary(graph))

