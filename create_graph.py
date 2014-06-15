from comparator import *
from Algorithms import *
from Scorer import *
from ConvertTextToGraph import *

import time

#place the list of algorithms you wish to run in this list
#eg. algoList = [Louvain(), FLFA(), ILFA()]
algoList = [ILFA()]

#place the names of the algorithms here for your convenience when printed
#eg. algoNames = ['Louvain', 'FLFA', 'ILFA']
algNames = ['ILFA']

#choose which dataset to convert into a graph here
#eg. converter = ConvertLesMisToGraph()

converter = ConvertLesMisToGraph()

(G, gt_communities) = converter.returnGraph()

with open ("Output_ILFA.txt", "w") as text_file:
    k=0

    #iterate through each algorithm in your list
    for algorithm in algoList:
        t = time.time()

        #find all your clusters/communities
        clique_clusters = algorithm.findClusters(G)
        elapsed = time.time() - t
        comparer = ClusterComparer()

        #choose your scoring mechanism. Choices are FScorer() and JacardScorer()
        fscorer = FScorer()
        t1 = time.time()


        #find the error of the estimated communities and the true communities
        error_score = comparer.calculateErrorScoreStanford(clique_clusters,gt_communities, fscorer)
        comparator_time = time.time()-t1
        text_file.write(algNames[k] + "\n")
        text_file.write(str(error_score) + "\n")
        text_file.write("Time taken: "+str(elapsed) + "\n")
        text_file.write("\n")
        text_file.write("Num communities: " + str(len(clique_clusters)))
        text_file.write("\n")
        k += 1
