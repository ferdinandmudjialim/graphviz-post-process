# This version is working for the coloring, but relies on the order of the labeled edges in the dot file, which is somewhat sketchy.

import os
import pydot

def sp_to_edge(edge_label): # does this work for exploits with more than 2 preconditions?
    path = []
    for e in edges:
        if e.get_label() == edge_label: # b/c of graph and dot structure, first edge found in dot is SP (??? what about ties?)
            path.append([e.get_destination()])
            path.append([e.get_source()])
            break
    depth = depth_nodes[path[-1][0]]
    while depth != 0:
        temp = []
        depth -= 1
        curr = path[-1]
        above = depth_lookup[depth]
        for n1 in above:
            for n2 in curr:
                if n2 in adj[n1] and n1 not in temp:
                    temp.append(n1)
        path.append(temp)
    path.reverse()
    return path

if __name__ == "__main__":
    colors = ["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#00916e","#6699cc","#8e6b67","#666370","#353531"]

    # converts relative to absolute path
    dirname = os.path.dirname(__file__)
    dotfile = os.path.join(dirname, "testing.dot")
    outfile = os.path.join(dirname, "")

    print("Reading from", dotfile)
    graph = pydot.graph_from_dot_file(dotfile)[0]
    nodes = graph.get_node_list()
    edges = graph.get_edge_list()

    # graph.set_rankdir("LR")

    adj = {}
    depth_lookup = {} # depth -> node
    depth_nodes = {} # node -> depth
    for n in nodes:
        adj[n.get_name()] = []
    for e in edges:
        index = int(e.get_label()) % len(colors)
        e.set_color(colors[index])
        e.set_fontcolor(colors[index])

        # populate adjacency list
        src = e.get_source() # node name
        dest = e.get_destination()
        adj[src].append(dest)

    # BFS coloring according to depth of node, also populates depth hashtables
    q = []
    q.append(nodes[0].get_name()) # assumes one possible starting node (init state)
    current_nodes = 1
    next_nodes = 0
    depth = 0
    while q:
        node_str = q.pop(0)
        current_nodes -= 1

        depth_nodes[node_str] = depth
        if depth not in depth_lookup:
            depth_lookup[depth] = []
        depth_lookup[depth] += [node_str]

        node_ref = graph.get_node(node_str)[0] # Node
        node_ref.set_style("filled")
        node_ref.set_fillcolor(colors[depth % len(colors)])
        for n in adj[node_str]:
            if n not in q:
                q.append(n)
                next_nodes += 1
        if current_nodes == 0:
            current_nodes = next_nodes
            next_nodes = 0
            depth += 1


    # graph.write(outfile)
    # print("Generated dot file to", outfile)
    target = "3"
    print("Shortest paths to target edge", target, "are:", sp_to_edge(target))
