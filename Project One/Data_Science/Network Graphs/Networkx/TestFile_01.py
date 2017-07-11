import networkx as nx
import matplotlib.pyplot as plt

# Make a graph
graph = nx.Graph()

node_one = 'one'
node_two = 'two'
node_three = 'three'
node_four = 'four'
node_five = 'five'
# How to add nodes:
graph.add_node(node_two)
graph.add_node(node_five)

# How to add an edge between nodes, aka connect them
graph.add_edge(node_two, node_five)

# How to add nodes implicitly:
graph.add_edge(node_four, node_one)

# How to add edges from a list:
#graph.add_edges_from([(2,5), (1,3)])

# Print the info of the graph
print(nx.info(graph))

# Draw the graph (in the background) & show the graph
nx.draw(graph, with_labels=True)
plt.show()



