class Scorer (object):
    def score(self, cluster1, cluster2):
        raise NotImplementedError("Should've implemented this")

class JacardScorer(Scorer):
    def score(self, cluster1, cluster2):
        matches=0
        mismatches=0
        for node in cluster1:
            if node in cluster2:
                matches+=1
            else:
                mismatches+=1
        if matches<len(cluster2):
            mismatches+=len(cluster2)-matches
        jScore = float(matches)/(matches+mismatches)
        return jScore


class FScorer(Scorer):

    def score(self, cluster1, cluster2):
        matches=0
        for node in cluster1:
            if node in cluster2:
                matches+=1
        precision = float(matches)/float(len(cluster1))
        recall = float(matches)/float(len(cluster2))
        if (precision+recall)!=0:
            fScore = 2*(precision*recall)/float(precision+recall)
        else:
            fScore = 0
        return fScore
