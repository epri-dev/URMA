# this function load the graph with parameters and data imported grom input file
# Input file so far supports CSV format; example file given- 'VERTICES.CSV' represents nodes and 'ARCS.CSV' edges of graph respectively

# We need to import the graph_tool module itself
from graph_tool.all import *
from collections import deque
import csv

def load_graph(g, vertices_csv_file, arcs_csv_file):
    #first we work creating vertex based on the data
    cve_it = csv.reader(open(vertices_csv_file))
    for row in cve_it:
        v = g.add_vertex()
        g.vp["nid"][v] = row[0]
        g.vp["label"][v] = row[1]
        g.vp["shape"][v] = row[2]
        
    # Now work with edges from the data
    cve_it = csv.reader(open(arcs_csv_file))
    for row in cve_it:
        src = find_vertex(g, g.vp['nid'], row[0])[0] # source vertex of the edge
        dst = find_vertex(g, g.vp['nid'], row[1])[0] # destination vertex of edge
        e = g.add_edge(src, dst)