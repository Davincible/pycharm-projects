import networkx as nx
import matplotlib.pyplot as plt

graph = nx.Graph()
node_one = 'The first node'
node_two = 'The second node'
node_three = 'The third node'
node_four = 'The fourth node'
node_five = 'The sixth node'

sizes = []
nodes = [node_one, node_two, node_three, node_four, node_five]
graph.nodes(nodes)

for i in range(len(nodes)):
    sizes.append(200)
index = nodes.index(node_one)
sizes[index] = 500

graph.add_edge(node_one, node_five)
graph.add_edge(node_two, node_three)
graph.add_edge(node_two, node_one)
graph.add_edge(node_one, node_four)


# Print the info of the graph
print(nx.info(graph))

# Draw the graph (in the background) & show the graph
nx.draw_circular(graph, node_size=sizes, with_labels=True)
plt.show()



