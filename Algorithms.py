import networkx as nx
import community
import pdb
# import sklearn.cluster


class CliqueFinder(object):
    def findClusters(G):
        return NotImplementedError("Should've implemented this")

    def isClique(self, c, graph):
        for node1 in c:
            for node2 in c:
                if node1 != node2:
                    if not graph.has_edge(node1,node2):
                        return False
        return True

    def isFollower(follower, graph):
        for neighbor in graph.neighbors_iter(follower):
            if (len(graph[neighbor]) > len(graph[follower])):
                return False
        return True

    def splitClusters(self, c, follower, graph):
        visited = {}
        subclusters = []
        for node in c:
            if node!= follower and node not in visited:
                subcluster = {}
                subcluster[node] = 1
                subcluster[follower] = 1
                visited[node] = 1
                for neighbor in graph[node]:
                    if neighbor != follower and neighbor in c:
                        subcluster[neighbor] = 1
                        visited[neighbor] = 1
                subclusters.append(subcluster)
        return subclusters
                        
##############################################################################


# class Spectral(CliqueFinder):
#     def findClusters(self, G, numClusters):
#         labels = sklearn.cluster.spectral_clustering(affinity=nx.adjacency_matrix(G), n_clusters=numClusters)
#         spectral_clusters={}
#         for i in range(len(labels)):
#             if labels[i] not in spectral_clusters:
#                 spectral_clusters[labels[i]] = [str(G.nodes()[i])]
#             else:
#                 spectral_clusters[labels[i]].append(str(G.nodes()[i]))
#         return spectral_clusters
#


##############################################################################
class Louvain(CliqueFinder):
    def findClusters(self, G):
        partition = community.best_partition(G)
        clusters={}
        for movie in partition:
            if partition[movie] in clusters:
                clusters[partition[movie]][movie]=1
            else:
                clusters[partition[movie]]={movie:1}
        return clusters.values()

##############################################################################
class Singleton(CliqueFinder):
    def findClusters(self, G):
        clusters=[]
        for node in G.nodes():
            clusters.append({node:1})
        return clusters


##############################################################################
class FLFA(CliqueFinder):
    def findClusters(self, G):
        sorted_nodes = sorted(G.nodes(), key= lambda node: len(G[node]))
        visited = {}
        clusters=[]
        i=0
        for node in sorted_nodes:
            if node not in visited:
                cluster={node:1}
                visited[node]=1
                for neighbor in G.neighbors_iter(node):
                    cluster[neighbor]=1
                    visited[neighbor]=1
                i+=1
                clusters.append(cluster)
        return clusters


##############################################################################

class FLFALFACliqueCheck(CliqueFinder):
    def findClusters(self, G):
        sorted_nodes = sorted(G.nodes(), key= lambda node: len(G[node]))
        visited = {}
        clusters=[]
        i=0
        for node in sorted_nodes:
            if node not in visited:
                cluster={node:1}
                visited[node]=1
                for neighbor in G.neighbors_iter(node):
                    cluster[neighbor]=1
                    visited[neighbor]=1
                i+=1
                clusters.extend(self.splitClusters(cluster, node, G))
        return clusters

##############################################################################

class ILFA(CliqueFinder):
    def findClusters(self, G):
        followers = self.findGlobalLeadersAndFollowers(G)
##        followers = self.findLeadersFollowers(G)
        sorted_nodes = sorted(G.nodes(), key = lambda n: len(G[n]))
        new_length = 0
        old_length = len(sorted_nodes)
        subgraph = G
        clusters=[]
        k=0
        t=0
        edges = {}
        while ((len(sorted_nodes)>0) and (new_length<old_length)):
            old_length = len(sorted_nodes)
            toRemove=[]
            print(subgraph.number_of_nodes())
            assigned = {}
            for follower in sorted_nodes:
                if follower not in assigned and (t==0 or subgraph.degree(follower)>0):
                    clusterMembers={follower:1}
                    validCluster = True
                    isFollower = True
                    subsetLeaders=[]
                    for neighbor in subgraph.neighbors_iter(follower):
                        clusterMembers[neighbor]=1
                        if (follower,neighbor) in edges or (neighbor,follower) in edges:
                            validCluster = False
                        if len(subgraph[neighbor]) > len(subgraph[follower]):
                            subsetLeaders.append(neighbor)
                        if (len(subgraph[neighbor]) < len(subgraph[follower])):
                            isFollower = False
                            break
                    if self.isClique(clusterMembers, subgraph):
                        toRemove.append(follower)
                        for node in clusterMembers:
                            if (len(subgraph[node])==len(subgraph[follower])):
                                toRemove.append(node)
                            assigned[node]=1
                        if validCluster:
                            clusters.append(clusterMembers)
                            for e in subgraph.subgraph(subsetLeaders).edges_iter():
                                edges[e] = 1
            subgraph.remove_nodes_from(toRemove)
            sorted_nodes = sorted(subgraph.nodes(), key = lambda n: subgraph.degree(n))
            new_length = len(sorted_nodes)
            t+=1
        return clusters

    def subset(c1, c2):
        if len(c2)<len(c1):
            return False
        else:
            for i in range(len(c1)):
                if c1[i] not in c2:
                    return False
            return True


    def findGlobalLeadersAndFollowers(self,graph):
        sorted_nodes =  sorted(graph.nodes(), key = lambda node: graph.degree(node))
        followers={}
        if len(sorted_nodes)>0:
            minDegree = graph.degree(sorted_nodes[0])
            for node in sorted_nodes:
                if (len(graph[node])>minDegree):
                    break
                followers[node]=1
        return followers


    def isClique(self, c, graph):
        for node1 in c:
            for node2 in c:
                if node1 != node2:
                    if not graph.has_edge(node1,node2):
                        return False
        return True