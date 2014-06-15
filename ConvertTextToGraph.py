import networkx as nx
import os
import re
import random
#import scipy.sparse as sp


class ConvertLesMisToGraph(object):


    def findId(self, character, nameToId, matchings):
        if character in nameToId:
            return nameToId[character]
        elif character in matchings:
            return nameToId[matchings[character]]
        else:
            print(character)


    
    def returnGraph(self):
        G = nx.read_gml('lesmis.gml')
        G.remove_node(73)
        G.remove_node(74)
        G.remove_node(4)
        G.remove_node(9)
        G.remove_node(33)
        G.remove_node(43)
        clusters = []
        cluster = {}
        characterList = ["Valjean" , "Plutarch", "Hucheloup", "Courfeyrac", "Feuilly", "Prouvaire", "Combeferre","Enolras", "Mabeuf", "Marius", "Gavroche", "Bossuet", "Joly", "Grantaire", "Bahorel", "Burgon", "Jondrette", "Boulatruelle", "Vaubois", "Toussaint", "Cosette", "Gillenormand","Magnon", "Baroness", "Pontmercy", "Babet", "Gueulemer", "Javert", "Thenardier", "Montparnasse", "Claquesous", "Brujon", "Eponine", "Anzelma", "Listolier", "Tholomyes", "Fantine", "Marguerite", "Fameuil", "Blacheville", "Favourite", "Perpetue", "Dahlia", "Zephine", "Brevet", "Chenildieu", "Cochepaille", "Houcheloup","Isabeau", "Gervais", "Labarre", "Bamatabois", "Valjean", "Simplice", "Scaufflaire", "Judge", "Champmathieu", "Cravatte", "Myriel", "Napoleon", "Baptistine", "Count", "Magloire", "Champtercier", "Geborand", "Innocente", "Fauchelevent", "Gribier", "Leblanc"] 
        characters = dict((c,1) for c in characterList)
        prefixList = ["Mademoiselle", "Father", "Aunt", "Madame"]
        prefixes = dict((p,1) for p in prefixList)
        folder = 'datasets'
        with open (folder+"/"+"lesmis.txt") as file:
            for line in file:
                words = line.split()
                for i in range(len(words)):
                    if words[i] == "CHAPTER":
                        clusters.append(cluster)
                        cluster = {}
                    elif words[i] in characters:
                        cluster[words[i]] = 1
                    elif words[i] in prefixes:
                        if i+1 < len(words) and words[i+1] in characterList:
                            cluster[words[i] + " " + words[i+1]] = 1
                            i += 1
        gt_communities = []
        for i in range(len(clusters)):
            subCluster = False
            for j in range(len(clusters)):
                if len(clusters[i]) < len(clusters[j]):
                    subset = True
                    for character in clusters[i]:
                        if character not in clusters[j]:
                            subset = False
                            break
                    if subset:
                        subCluster = True
                        break
            if not subCluster:
                gt_communities.append(clusters[i])
    
        nameToId = {}
        for key in G.node:
            nameToId[str(G.node[key]['label'])] = key

        matchings = {"Plutarch":"MotherPlutarch", "Hucheloup":"MmeHucheloup", "Mademoiselle Hucheloup": "MmeHucheloup", "Enolras": "Enjolras", "Burgon":"Brujon", "Vaubois": "MlleVaubois", "Madame Vaubois":"MlleVaubois", "Mademoiselle Vaubois":"MlleVaubois", "Baroness":"BaronessT", "Houcheloup":"MmeHucheloup", "Madame Houcheloup": "MmeHucheloup", "Mademoiselle Houcheloup": "MmeHucheloup", "Baptistine":"MlleBaptistine", "Madame Baptistine": "MlleBaptistine", "Mademoiselle Baptistine": "MlleBaptistine", "Magloire": "MmeMagloire", "Madame Magloire": "MmeMagloire", "Mademoiselle Magloire":"MmeMagloire", "Innocente":"MotherInnocent", "Madame Thenardier" :"MmeThenardier","Father Champmathieu":"Champmathieu","Father Fauchelevent":"Fauchelevent","Mademoiselle Gillenormand":"MlleGillenormand", "Father Gillenormand":"Gillenormand","Aunt Gillenormand":"LtGillenormand","Father Mabeuf":"Mabeuf","Father Hucheloup":"MmeHucheloup","Madame Pontmercy":"MmePontmercy", "Leblanc":"Valjean", "Mademoiselle Cosette":"Cosette"}     

        for cluster in gt_communities:
            for key in cluster.keys():
                cluster[self.findId(key, nameToId, matchings)] = cluster.pop(key)
        return (G, gt_communities)

class ConvertOrkutToGraph(object):
    def returnGraph(self):
        G=nx.Graph()
        gt_communities=[]
        groups=0
        i=0
        with open('com-orkut.all.cmty.txt') as file:
            for line in file:
                nodes_arr = line.split()
                gt_communities.append(dict((n,1) for n in nodes_arr))
                G.add_nodes_from(nodes_arr)
                groups += 1
                if groups >1000:
                    break
        with open('com-orkut.ungraph.txt') as file:
            for line in file:
                nodes_arr = line.split()
                if (G.has_node(nodes_arr[0]) and G.has_node(nodes_arr[1])):
                    G.add_edge(nodes_arr[0], nodes_arr[1])
        return (G, gt_communities)

class ConvertIMDBToGraph(object):
    def returnGraph(self):
        G=nx.Graph()
        gt_communities=[]
        movies=0
        i=0
        folder = 'datasets'
        with open(folder+'/'+'actor.txt') as file:
            for line in file:
                nodes_arr = line.split()
                nodes=dict((n,1) for n in nodes_arr)
                for node in nodes_arr:
                    for k in range(len(nodes_arr)):
                        if nodes_arr[k]!=node:
                            G.add_edge(node,nodes_arr[k])
                            i+=1
                gt_communities.append(nodes)
                movies+=1
                if movies%1000==0:
                    print(movies)
        return (G, gt_communities)


class ConvertIMDBToGraph5Percent(object):
    def returnGraph(self):
        G=nx.Graph()
        gt_communities=[]
        movies=0
        i=0
        folder = 'datasets'
        with open(folder+'/'+'actor.txt') as file:
            for line in file:
                nodes_arr = line.split()
                nodes=dict((n,1) for n in nodes_arr)
                for node in nodes_arr:
                    for k in range(len(nodes_arr)):
                        if nodes_arr[k]!=node:
                            G.add_edge(node,nodes_arr[k])
                            i+=1
                gt_communities.append(nodes)
                movies+=1
                if movies%1000==0:
                    print(movies)
        numEdges = G.number_of_edges()
        numToRemove = 0.05 * float(numEdges)
        print ("edges to remove: " + str(numToRemove))
        edges_to_remove = []
        n = 1
        for edge in G.edges():
            if len(edges_to_remove) < numToRemove:
                edges_to_remove.append(edge)
            else:
                s = int(random.random() * n)
                if s < numToRemove:
                    edges_to_remove[s] = edge
            n += 1
        G.remove_edges_from(edges_to_remove)
        return (G, gt_communities)


class ConvertIMDBToGraph1Percent(object):
    def returnGraph(self):
        G=nx.Graph()
        gt_communities=[]
        movies=0
        i=0
        folder = 'datasets'
        with open(folder+'/'+'actor.txt') as file:
            for line in file:
                nodes_arr = line.split()
                nodes=dict((n,1) for n in nodes_arr)
                for node in nodes_arr:
                    for k in range(len(nodes_arr)):
                        if nodes_arr[k]!=node:
                            G.add_edge(node,nodes_arr[k])
                            i+=1
                gt_communities.append(nodes)
                movies+=1
                if movies%1000==0:
                    print(movies)

        numEdges = G.number_of_edges()
        numToRemove = 0.01 * float(numEdges)
        print ("edges to remove: " + str(numToRemove))
        edges_to_remove = []
        n = 1
        for edge in G.edges():
            if len(edges_to_remove) < numToRemove:
                edges_to_remove.append(edge)
            else:
                s = int(random.random() * n)
                if s < numToRemove:
                    edges_to_remove[s] = edge
            n += 1
        G.remove_edges_from(edges_to_remove)
        return (G, gt_communities)

class ConvertIMDBToGraph10Percent(object):
    def returnGraph(self):
        G=nx.Graph()
        gt_communities=[]
        movies=0
        i=0
        folder = 'datasets'
        with open(folder+'/'+'actor.txt') as file:
            for line in file:
                nodes_arr = line.split()
                nodes=dict((n,1) for n in nodes_arr)
                for node in nodes_arr:
                    for k in range(len(nodes_arr)):
                        if nodes_arr[k]!=node:
                            G.add_edge(node,nodes_arr[k])
                            i+=1
                gt_communities.append(nodes)
                movies+=1
                if movies%1000==0:
                    print(movies)
        numEdges = G.number_of_edges()
        numToRemove = 0.1 * float(numEdges)
        print ("edges to remove: " + str(numToRemove))
        edges_to_remove = []
        n = 1
        for edge in G.edges():
            if len(edges_to_remove) < numToRemove:
                edges_to_remove.append(edge)
            else:
                s = int(random.random() * n)
                if s < numToRemove:
                    edges_to_remove[s] = edge
            n += 1
        G.remove_edges_from(edges_to_remove)
        return (G, gt_communities)

class ConvertIMDBToGraph25Percent(object):
    def returnGraph(self):
        G=nx.Graph()
        gt_communities=[]
        movies=0
        i=0
        folder = 'datasets'
        with open(folder+'/'+'actor.txt') as file:
            for line in file:
                nodes_arr = line.split()
                nodes=dict((n,1) for n in nodes_arr)
                for node in nodes_arr:
                    for k in range(len(nodes_arr)):
                        if nodes_arr[k]!=node:
                            G.add_edge(node,nodes_arr[k])
                            i+=1
                gt_communities.append(nodes)
                movies+=1
                if movies%1000==0:
                    print(movies)
        numEdges = G.number_of_edges()
        numToRemove = 0.25 * float(numEdges)
        print ("edges to remove: " + str(numToRemove))
        edges_to_remove = []
        n = 1
        for edge in G.edges():
            if len(edges_to_remove) < numToRemove:
                edges_to_remove.append(edge)
            else:
                s = int(random.random() * n)
                if s < numToRemove:
                    edges_to_remove[s] = edge
            n += 1
        G.remove_edges_from(edges_to_remove)
        return (G, gt_communities)


class ConvertIMDBToGraph50Percent(object):
    def returnGraph(self):
        G=nx.Graph()
        gt_communities=[]
        movies=0
        i=0
        folder = 'datasets'
        with open(folder+'/'+'actor.txt') as file:
            for line in file:
                nodes_arr = line.split()
                nodes=dict((n,1) for n in nodes_arr)
                for node in nodes_arr:
                    for k in range(len(nodes_arr)):
                        if nodes_arr[k]!=node:
                            G.add_edge(node,nodes_arr[k])
                            i+=1
                gt_communities.append(nodes)
                movies+=1
                if movies%1000==0:
                    print(movies)
        numEdges = G.number_of_edges()
        numToRemove = 0.5 * float(numEdges)
        print ("edges to remove: " + str(numToRemove))
        edges_to_remove = []
        n = 1
        for edge in G.edges():
            if len(edges_to_remove) < numToRemove:
                edges_to_remove.append(edge)
            else:
                s = int(random.random() * n)
                if s < numToRemove:
                    edges_to_remove[s] = edge
            n += 1
        G.remove_edges_from(edges_to_remove)
        return (G, gt_communities)
    

class ConvertFacebookToGraph(object):
    def returnGraph(self):
        G = nx.Graph()
        gt_communities=[]
        circles=0
        i=0
        folder = 'datasets/facebook'
        for filename in os.listdir(folder):
            name_arr = filename.split('.')
            if name_arr[1]=='circles':
                with open(folder+'/'+filename) as file:
                    for line in file:
                        nodes = line.split()
                        gt_communities.append(dict((n,1) for n in nodes[1:]))
                        circles+=1
            elif name_arr[1]=='edges':
                with open(folder+'/'+filename) as file:
                    for line in file:
                        nodes = line.split()
                        G.add_edge(nodes[0],nodes[1])
        return (G, gt_communities)


class ConvertGPlusToGraph(object):
    def returnGraph(self):
        G = nx.Graph()
        gt_communities=[]
        circles=0
        i=0
        folder = 'gplus'
        for filename in os.listdir(folder):
            name_arr = filename.split('.')
            if name_arr[1]=='circles':
                with open(folder+'/'+filename) as file:
                    for line in file:
                        nodes = line.split()
                        gt_communities.append(dict((n,1) for n in nodes[1:]))
                        circles+=1
            elif name_arr[1]=='edges':
                with open(folder+'/'+filename) as file:
                    for line in file:
                        nodes = line.split()
                        G.add_edge(nodes[0],nodes[1])
        return (G, gt_communities)

class ConvertPrimeNumbersToGraph(object):
    def getPrimes(self):
        primes = []
        for i in range(2,1001):
            if self.is_prime(i):
                primes.append(i)
        return primes
    def returnGraph(self):
        G = nx.Graph()
        primes = self.getPrimes();
        gt_communities = {}
        for i in range(2, 1001):
            for j in primes:
                if i % j == 0:
                    if j in gt_communities:
                        gt_communities[j][str(i)] = 1
                    else:
                        gt_communities[j] = {str(i): 1}
        G.add_nodes_from(map(lambda x: str(x),range(2, 1001)))
        for community in gt_communities.values():
            for node in community:
                for other_node in community:
                    G.add_edge(str(node), str(other_node))
        return (G, gt_communities.values())

    def is_prime(self, a):
        return all(a % i for i in xrange(2, a))

class ConvertCShow1ToGraph(object):
    def returnGraph(self):
        G = nx.Graph()
        gt_communities=[]
        circles=0
        i=0
        community={}
        folder = 'datasets/CShow'
        filename = 'saas_chow_2010_clusters_truth.txt'
        with open(folder+'/'+filename) as file:
            for line in file:
                if line[0]=='%':
                    if len(community)>0:
                        gt_communities.append(community)
                        for person1 in community:
                            for person2 in community:
                                if person1 != person2:
                                    G.add_edge(person1,person2)
                        community={}
                else:

                    names=re.findall("'([^'}]*)'", line)
                    for name in names:
                        community[name]=1
        return (G, gt_communities)


class ConvertCShow2ToGraph(object):
    def returnGraph(self):
        G = nx.Graph()
        gt_communities=[]
        circles=0
        i=0
        community={}
        folder = 'datasets/CShow'
        filename = 'saas_chow_2011_clusters_truth.txt'
        with open(folder+'/'+filename) as file:
            for line in file:
                if line[0]=='%':
                    if len(community)>0:
                        gt_communities.append(community)
                        for person1 in community:
                            for person2 in community:
                                if person1 != person2:
                                    G.add_edge(person1,person2)
                        community={}
                else:

                    names=re.findall("'([^'}]*)'", line)
                    for name in names:
                        community[name]=1
        return (G, gt_communities)
