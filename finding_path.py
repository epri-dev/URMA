# this function finds attack paths from all edge state(s) to target state in the graph
# the function takes the graph and target state as input and find paths

# We need to import the graph_tool module itself
from graph_tool.all import *
from collections import deque
import csv


def search_all_attack_paths(graph, start, max=10000): # 'start' represents target state
    # max=100000 limit the number of paths as sometimes it just explodes based on attack graph
    # TODO: Raise error instead
    if start >= graph.num_vertices():
        print ("TODO: Raise error")
        return []

    # print "==== Searching for path to node index ", start, "in the graph ===="
    paths = []
    q = deque()

    for oe in graph.vertex(start).out_edges():
        q.append(([int(oe.target())], [(start, int(oe.target()))], 0))

    while len(q):
        u = q.popleft()
        key = u[0].pop(0)

        if graph.vp["shape"][key] == "AND":  # AND node
            # attacker = False
            newkeys = False
            loop = False

            w = 0
            for oe in graph.vertex(key).out_edges():
                new = int(oe.target())

                edge = (key, new)
                if edge in u[1]:
                    loop = True
                else:
                    u[1].append(edge)
                    
                if graph.vp["shape"][new] == "OR":
                    u[0].append(new)
                    newkeys = True

            if loop:
                print ("Discard loop path")
            elif len(u[0]) > 0:
                q.append((u[0], u[1], w + u[2]))
            else:
                paths.append([u[1], u[2]])
                #print ("PATH Lenght : ", len (paths), " : ", paths[len (paths) -1])
                if len(paths) >= max:
                    return paths

        elif graph.vp["shape"][key] == "OR":  
            for oe in graph.vertex(key).out_edges():
                new = int(oe.target())
                edge = (key, new)
                if edge not in u[1]:
                    q.append((u[0]+[new], u[1]+[(key, new)], 0))

    return paths