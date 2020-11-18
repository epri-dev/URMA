# this function finds attack paths from all edge state(s) to target state in the graph
# the function takes the graph, target state and source IP as input and find paths between them


# first we import all necessary module exploit
import json
from graph_tool.all import *
import time
import numpy as np
import re
from collections import deque
import csv


def attack_paths_ip_to_target(g, start, target_IP, max=10000): 
    

    if start >= g.num_vertices():
        print ("TODO: Raise error")
        return []

        # print "==== Searching for path to node index ", start, "in the graph ===="
    paths =[]
    q = deque()
    threshold=0

    label=g.vp["label"][start]
    src_IP=re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", label)[0]

    if src_IP==target_IP:
        print('attack graph source IP and target IP is same')
    else:
        IP_track=False
        for oe in g.vertex(start).out_edges():
            q.append(([int(oe.target())], [(start, int(oe.target()))], 0))


        while len(q):
            u = q.popleft()
            key = u[0].pop(0)


            if g.vp["shape"][key] == "AND":
                src_IP=0
                conds = map(lambda x:x.target(), g.vertex(key).out_edges())
                for cond in conds:
                    if g.vp["shape"][cond] == "LEAF":
                        label=g.vp["label"][cond]
                        src_IP=re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", label)
                        if 'nfsExportInfo' in label:
                            src_IP=re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", label)[1]
                        elif len(src_IP)!=0:
                            src_IP=re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", label)[0]


                    if src_IP==target_IP:
                        IP_track=True
                        break

                # attacker = False
                newkeys = False
                loop = False
                w = 0


                for oe in g.vertex(key).out_edges():

                    new = int(oe.target())

                    edge = (key, new)

                    if edge in u[1]:
                        loop = True
                    else:
                        u[1].append(edge)


                    if g.vp["shape"][new] == "OR":
                        u[0].append(new)
                        newkeys = True


                threshold=threshold+1
                if threshold==200000:
                    break

                if loop:
                    print ("Discard loop path")
                elif IP_track:
                    paths.append([u[1], u[2]])
                    #print(paths)
                    IP_track=False

                elif len(u[0]) > 0:
                    q.append((u[0], u[1], w + u[2]))


            elif g.vp["shape"][key] == "OR":  
                for oe in g.vertex(key).out_edges():
                    new = int(oe.target())
                    edge = (key, new)
                    if edge not in u[1]:
                        q.append((u[0]+[new], u[1]+[(key, new)], 0))
                        
    return paths
