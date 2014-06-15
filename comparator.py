import numpy

class ClusterComparer():
    def calculateErrorScore(clusterList1, matchedList):
        errorScore=0
#        n=260998
        k=len(clusterList1)
        for cluster in clusterList1:
            errorScore+=ClusterComparer.clusterScore(clusterList1[cluster],matchedList[cluster])
        errorScore = (1/k)*errorScore
        return errorScore

    def calculateErrorScoreStanford(self, clusterList1, clusterList2, scorer):
        score1 = self.findBestPairs(clusterList1, clusterList2, scorer)
        score2 = self.findBestPairs(clusterList2, clusterList1, scorer)
        print("SCORE1: "+str(score1))
        print("SCORE2: "+str(score2))
        totalScore = 0.5*(score1+score2)
        return totalScore


    def findBestPairs(self, clusterList1, clusterList2, scorer):
        i=0
        totalScore=0
        for cluster1 in clusterList1:
            bestScore=-1
            i+=1
            if i%100==0:
                print(i)
            for cluster2 in clusterList2:
                pair_score = scorer.score(cluster1, cluster2)
                if pair_score>bestScore:
                    bestScore=pair_score
                    if bestScore==1:
                        break
            totalScore+=bestScore
        totalScore = float(totalScore)/float(len(clusterList1))
        return totalScore


    def findSingleBestPair(cluster, clusterList2):
        match={}
        bestScore=float("inf")
        for gt_cluster in clusterList2:
            pair_score = ClusterComparer.clusterScore(cluster,gt_cluster)
            if pair_score<bestScore:
                match=gt_cluster
                bestScore=pair_score
        return match

