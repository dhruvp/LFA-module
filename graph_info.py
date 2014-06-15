import networkx as nx
from ConvertTextToGraph import *
from CliqueFinder import *


converters = [ConvertGPlusToGraph()]
graph_names = ["GPlus"]
algos = [SimpleLFA(), Louvain()]
algo_names = ["SimpleLFA", "Louvain", "RecursiveLFA"]
with open ("graphinfo.txt", "w") as text_file:
    for i in range(len(converters)):
        converter = converters[i]
        (G, gt_communities) = converter.returnGraph()
        text_file.write("Graph name: " + graph_names[i] + "\n")
        text_file.write("Number of nodes: " + str(len(G.nodes())) + "\n")
        text_file.write("Number of edges: " + str(len(G.edges())) + "\n")
        text_file.write("Number of true communities: " + str(len(gt_communities)))
        for j in range(len(algos)):
            clusters = algos[j].findClusters(G)
            text_file.write("Algorithm: " + algo_names[j] + "\n")
            text_file.write("Number of found clusters: " + str(len(clusters)) + "\n")
        text_file.write("\n"+"\n")
