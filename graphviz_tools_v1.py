# Initial base version

import os
import pydot

if __name__ == "__main__":
    colors = ["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#00916e","#6699cc","#8e6b67","#666370","#353531"]

    # converts relative to absolute path
    dirname = os.path.dirname(__file__)
    dotfile = os.path.join(dirname, "edges_db.dot")
    outfile = os.path.join(dirname, "outfile.dot")

    print("Reading from", dotfile)
    graph = pydot.graph_from_dot_file(dotfile)[0]
    nodes = graph.get_node_list()
    edges = graph.get_edge_list()
    adj = {}
    for i in range(len(nodes)):
        adj[i] = []
    for e in edges:
        index = int(e.get_label()) % len(colors)
        e.set_color(colors[index])
        e.set_fontcolor(colors[index])

        # populate adjacency list
        src = int(e.get_source())
        dest = int(e.get_destination())
        adj[src].append(dest)

    # BFS coloring according to depth of node
    q = []
    q.append(0)
    current_nodes = 1
    next_nodes = 0
    depth = 0
    while q:
        node = q.pop(0) # int
        current_nodes -= 1
        node_ref = graph.get_node(str(node))[0] # Node
        node_ref.set_style("filled")
        node_ref.set_fillcolor(colors[depth])
        for n in adj[node]:
            if n not in q:
                q.append(n)
                next_nodes += 1
        if current_nodes == 0:
            current_nodes = next_nodes
            next_nodes = 0
            depth += 1


    graph.write(outfile)
    print("Generated dot file to", outfile)
