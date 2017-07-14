import igraph as ig

graph = ig.Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])

graph.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
graph.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
graph.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
graph.es["is_formal"] = [False, False, True, True, True, False, True, False, False]


# Get the source and target of an edge with the attributes
# print(graph.es[2].source)
# print(graph.es[2].target)
# print(graph.es[2].tuple)

# If you add a new attribute by dictonary key, the rest of the objescts will automatically have None for that attribute.
# print(graph.vs[3].attributes())
# graph.vs[3]['foo'] = 'bar'
# print(graph.vs[3].attributes())

print('Total number of edges connected:', graph.degree(6))
print('Number of incomming edges:', graph.degree(6, type="in"))
print('Number of outgoing edges:', graph.degree(6, type="out"))

lay = graph.layout('kk')
ig.plot(graph, layout=lay)
