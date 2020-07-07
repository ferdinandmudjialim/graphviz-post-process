#!/usr/bin/env python

"""Version 2 is working for the coloring, but relies on the order of the labeled edges in the dot file, which is somewhat questionable. 
   Version 3 seeks to fix this behavior by doing it the hard (but correct) way. 
   Note: Assumes the initial node name is "0"
"""

import os
import argparse
import pydot


# TODO: Split up color and depth in BFS? Maybe...
def bfs_color_depth(adj, edges, graph, depth_lookup, depth_nodes): 
    """Populate depth hashtables, and performs BFS coloring of nodes and edges (colors based on depth).

    Args:
        adj:
        edges:
        graph:
        depth_lookup:
        depth_nodes:
    """
    # TODO: change colors for better visibility / variety?
    colors = ["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00",
              "#00916e","#6699cc","#8e6b67","#666370","#353531"]

    # Color edges
    for e in edges:
        index = int(e.get_label()) % len(colors)
        e.set_color(colors[index])
        e.set_fontcolor(colors[index])

    # Color nodes & get depths with BFS
    q = []
    q.append("0") # only one possible starting node (init state)
    current_nodes = 1
    next_nodes = 0
    depth = 0
    while q: 
        node_name = q.pop(0)
        current_nodes -= 1

        depth_nodes[node_name] = depth
        if depth not in depth_lookup:
            depth_lookup[depth] = []
        depth_lookup[depth] += [node_name]

        try:
            node_ref = graph.get_node(node_name)[0]
        except IndexError:
            print("ERROR: Node does not exist! (BFS operation)")
            raise

        node_ref.set_style("filled")
        node_ref.set_fillcolor(colors[depth % len(colors)])
        
        for n in adj[node_name]:
            if n not in q: 
                q.append(n)
                next_nodes += 1
                
        if current_nodes == 0: # ready to go down one level in depth
            current_nodes = next_nodes
            next_nodes = 0
            depth += 1


def sp_to_edge(adj, edges, depth_lookup, depth_nodes, target_edge_label):
    """Get shortest path to desired edge (by name)

    Args: 
        adj:
        edges:
        depth_lookup:
        depth_nodes:
        target_edge_label:
        
    """
    # Get the target edges that are at minimum depth (thus, shortest path)
    to_scan = []
    for e in edges:
        if e.get_label() == target_edge_label:
            element = [e.get_destination(), depth_nodes[e.get_destination()]]
            if not to_scan:
                to_scan.append(element)
            else:
                if element[1] < to_scan[0][1]: # New min depth/path found
                    to_scan = [element] # Reset and add new min
                elif element[1] == to_scan[0][1]:
                    to_scan.append(element)

    if not to_scan:
        raise IndexError("ERROR: No matching edges found for target!")
    
    min_depth = to_scan[0][1]

    # Scan above the minimum depth for adjacent "parent" nodes and add to path
    def bubble_up(node_list, depth, path):
        while depth != 0: 
            node_list_new = []
            for n1 in depth_lookup[depth]: # TODO: how to optimize this further? maybe with edge depths hashtable? 
                for n2 in node_list: 
                    if n2 in adj[n1] and n1 not in node_list_new: 
                        node_list_new.append(n1)
            path.append(node_list_new)
            node_list = node_list_new
            depth -= 1
        path.reverse()
    
    for el in to_scan: 
        depth = min_depth
        node = [el[0]]
        path = [node]
        bubble_up(node, depth-1, path)
        print(path)


def main(in_file, out_file, target_edge): 
    
    should_output = should_find_sp = False
    if out_file != None:
        should_output = True
    if target_edge != None: 
        should_find_sp = True

    print("Reading from", in_file)
    try: 
        graph = pydot.graph_from_dot_file(in_file)[0]
    except TypeError:
        print("ERROR: Syntax error in dot file!")
        raise

    nodes = graph.get_node_list()
    edges = graph.get_edge_list()

    if len(nodes) == 0: 
        raise IndexError("ERROR: No explicit nodes found in graph!") 
    if len(edges) == 0: 
        raise IndexError("ERROR: No explicit edges found in graph!")

    adj = {}
    depth_lookup = {} # depth : node
    depth_nodes = {} # node : depth
    for n in nodes: 
        adj[n.get_name()] = []
    
    # Populate adjacency list
    for e in edges:
        src = e.get_source() # node name
        dest = e.get_destination()
        adj[src].append(dest)

    bfs_color_depth(adj, edges, graph, depth_lookup, depth_nodes)

    if should_output:
        graph.write(out_file)
        print("Generated dot file to", out_file)

    if should_find_sp:
        print("Shortest paths to target edge", target_edge, "are:")
        sp_to_edge(adj, edges, depth_lookup, depth_nodes, target_edge)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a dot file (GraphViz) to generate a colored version. \
                                                 Can also find shortest path to a target edge.")
    parser.add_argument("input", help="path to dot file to process")
    parser.add_argument("output", help="path to dot file to output")
    parser.add_argument("-t", "--target", help="finds shortest path(s) to target edge")
    args = parser.parse_args()
    main(args.input, args.output, args.target)
    