import numpy as np
import pandas as pd
import holoviews as hv
import networkx as nx
import json
hv.extension('bokeh')
from bokeh.io import save, output_file, show


#%opts Graph [width=400 height=400]

#Open Json Files With JDilla connections
with open('rels.json') as fp:
    songs = json.load(fp)


#Create Edge List
edgeList = []

for edge in songs:
    connect = ()
    for k, v in edge.items():
        connect = connect + (v,)
    edgeList.append(connect)


#Create empty graph
dillaGraph = nx.Graph()

#Add edges to graph
for entry in edgeList:
    i = 0 
    j = 1
    dillaGraph.add_edge(entry[i],entry[j])



padding = dict(x=(-1.2, 1.2), y=(-1.2, 1.2))

#Display grap
#%%opts Graph [tools=['hover']]
#songs = nx.spring_layout(g, scale = 10)
#nx.draw(G = g, pos = songs,with_labels = True)
dillaGraph = hv.Graph.from_networkx(dillaGraph, nx.layout.spring_layout).redim.range(**padding)


renderer = hv.renderer('bokeh')
dG = renderer.get_plot(dillaGraph).state
#save(dillaGraph, 'dillaGraph.html')

show(dG)
