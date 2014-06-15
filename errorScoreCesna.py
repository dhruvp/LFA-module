import networkx as nx
from ConvertTextToGraph import *
from comparator import *
from Scorer import *

converter = ConvertCShow2ToGraph()
(G, gt_communities) = converter.returnGraph()
clique_clusters=[]
with open ("cmtyvv-cesna.txt", "r") as f:
    for line in f:
        nodes = line.split()
        cluster = dict((n,1) for n in nodes)
        clique_clusters.append(cluster)

comparer = ClusterComparer()
fscorer=  FScorer()
clique_score = comparer.calculateErrorScoreStanford(clique_clusters,gt_communities, fscorer, G.number_of_nodes())
print(str(clique_score))

clique_clusters=[]

with open ("cmtyvv-bigclam.txt", "r") as f:
    for line in f:
        nodes = line.split()
        cluster = dict((n,1) for n in nodes)
        clique_clusters.append(cluster)

comparer = ClusterComparer()
fscorer=  FScorer()
clique_score = comparer.calculateErrorScoreStanford(clique_clusters,gt_communities, fscorer, G.number_of_nodes())
print(str(clique_score))
