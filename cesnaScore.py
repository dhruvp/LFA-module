import networkx as nx
import subprocess
from ConvertTextToGraph import *
from comparator import *
from Scorer import *
import time
import pdb

graph = 'LesMisGraph'
alglist = ['cesna', 'bigclam']

converter = ConvertLesMisToGraph()
(G, gt_communities) = converter.returnGraph()

for alg in alglist:
    print (alg)
    edgefile = "../snap/examples/"+alg+"/"+graph+".edges"
    featfile = "../snap/examples/"+alg+"/"+graph+".nodefeat"
    namefile = "../snap/examples/"+alg+"/"+graph+".nodefeatnames"

    with open (edgefile,"w") as text_file:
        for edge in G.edges():
            text_file.write(str(edge[0]))
            text_file.write("\t")
            text_file.write(str(edge[1]))
            text_file.write("\n")
    with open (featfile,"w") as text_file:
        x=5
    with open (namefile,"w") as text_file:
        x=5

    tic = time.time()
    subprocess.call(["../snap/examples/"+alg+"/./"+alg, "-i:"+edgefile, "-a:"+featfile, "-n:"+namefile, "-c:-1", "-o:"+alg+"-"])
    toc = time.time() - tic

    clique_clusters=[]
    
    with open (alg+"-"+"cmtyvv.txt", "r") as f:
        for line in f:
            nodes = line.split()
            cluster = dict((int(n),1) for n in nodes)
            clique_clusters.append(cluster)
                    
    comparer = ClusterComparer()
    fscorer=  FScorer()
    clique_score = comparer.calculateErrorScoreStanford(clique_clusters,gt_communities, fscorer)

    with open (alg+"-"+"ScoreOutput.txt", "w") as text_file:
        text_file.write(alg)
        text_file.write("\n")
        text_file.write(str(clique_score))
        text_file.write("\n")
        text_file.write("Elapsed Time: "+str(toc))
