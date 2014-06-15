import networkx as nx
import matplotlib.pyplot as plt
from comparator import *
from LFA_networkx import *
from dumbLFA import *
import numpy
import scipy
import community

G=nx.Graph()
i=0
current_node='0'
edges=[]
gt_communities=[]
match={}
visited={}
i=0
movies=0
with open('actor.txt') as file:
    for line in file:
        members={}
        nodes=line.split()
        for node in nodes:
            G.add_node(node)
            for k in range(len(nodes)):
                if nodes[k]!=node:
                    G.add_edge(node,nodes[k])
                    i+=1
        gt_communities.append(nodes)
        movies+=1
        if movies%100==0:
            print(movies)


partition = community.best_partition(G)
clusters={}
for movie in partition:
    if partition[movie] in clusters:
        clusters[partition[movie]].append(movie)
    else:
        clusters[partition[movie]]=[movie]
match_louvain = ClusterComparer.findBestPairs(clusters,gt_communities)
louvain_score = ClusterComparer.calculateErrorScore(clusters,match_louvain)
print(louvain_score)

##
##cliqueFinder = CliqueFinder(G)
##clique_clusters = cliqueFinder.findCliques1()
##match_clique = ClusterComparer.findBestPairs(clique_clusters, gt_communities)
##clique_score = ClusterComparer.calculateErrorScore(clique_clusters,match_clique)
##print("Simple LFAs")
##print(clique_score)
##
##LFARunner = LFANetworkX(G)
##clusters = LFARunner.run()
##match_lfa= ClusterComparer.findBestPairs(clusters, gt_communities)
##lfa_score = ClusterComparer.calculateErrorScore(clusters, match_lfa)
##print("OLD LFA")
##print(lfa_score)

##singleton_clusters = {}
##p=0
##for k in (G.nodes_iter()):
##    singleton_clusters[p]=[k]
##    p+=1
##    if p%100==0:
##        print(p)
##
##match_singleton = ClusterComparer.findBestPairs(singleton_clusters, gt_communities)
##singleton_score = ClusterComparer.calculateErrorScore(singleton_clusters,match_singleton)
##print(singleton_score)

##labels = sklearn.cluster.spectral_clustering(affinity=nx.adjacency_matrix(G), n_clusters=len(gt_communities))
##spectral_clusters={}
##for i in range(len(labels)):
##    if labels[i] not in spectral_clusters:
##        spectral_clusters[labels[i]] = [str(G.nodes()[i])]
##    else:
##        spectral_clusters[labels[i]].append(str(G.nodes()[i]))



##
##
##match_spectral = ClusterComparer.findBestPairs(spectral_clusters,gt_communities)
##spectral_score = ClusterComparer.calculateErrorScore(spectral_clusters,match_spectral)
##
##




##pos=nx.spring_layout(G)
##for cluster in clusters:
##    followers=[]
##    influencers=[]
##    leaders=[]
##    labels={}
##    if len(clusters[cluster].nodes)>2:
##        for node in clusters[cluster].nodes:
##            if node.category==0:
##                leaders.append(node.name)
##            elif node.influentialFollower:
##                influencers.append(node.name)
##            else:
##                followers.append(node.name)
##        print (str(cluster))
##        color=numpy.random.rand(3,1)
##        nodes_f=nx.draw_networkx_nodes(G,pos, nodelist=followers)
##        if nodes_f!=None:
##            nodes_f.set_color(color)
##        nodes_i = nx.draw_networkx_nodes(G,pos,nodelist=influencers)
##        if nodes_i!=None:
##            nodes_i.set_color(color)
##            nodes_i.set_edgecolor('k')
##            nodes_i.set_linewidth(3)
##        nx.draw_networkx_nodes(G,pos,nodelist=leaders,node_color='r')
####        if cluster==50:
####            nx.draw_networkx(G.subgraph(followers+influencers+leaders), alpha=0.3,labels=labels)
####            plt.show()
##nx.draw_networkx_edges(G, pos, alpha=0.3)
##plt.show()
##    
