import sys
from sklearn.neighbors import NearestNeighbors
sys.setrecursionlimit(10000)

class MultiDBSCAN():
    """Multi-density DBSCAN
    
    Algorithm to discover clusters with different densities.
    Based on "Multi Density DBSCAN", Wesam and Saad, 2011.
    """
    def __init__(self, k, var):
        """Initialize multi_dbscan object
        
        Inputs:
            k: number of nearest neighbors
            var: variance, greater than 1
        """
        self.k = k
        self.var = var
        
    def fit_predict(self, X):
        """Fit multi-dbscan and predict labels
        
        Inputs:
            X: standardized data points [n_observations, n_features]
        """
        # pass input
        self.X = X
        
        # find K nearest neighbors
        nbrs = NearestNeighbors(n_neighbors=self.k,
                                metric="euclidean")
        nbrs_fit = nbrs.fit(self.X)
        self.k_dist, self.k_ind = nbrs_fit.kneighbors(self.X)
    
        # create average distance of k nearest neighbors for each point
        self.aDST = dict(enumerate(np.sum(self.k_dist, axis=1)/(self.k-1)))

        # initialize cluster at densest point
        self.clusters = {}
        self.nclust = 0
        while self.aDST:
            idat = min(self.aDST, key=self.aDST.get)
            self.clusters[self.nclust] = [idat]
            self.cluster_aDST = self.aDST[idat]
            self.aDST.pop(idat, None)
            self.cluster_expand(idat)
            if len(self.clusters[self.nclust])<20:
                self.clusters.pop(self.nclust, None)
            self.nclust += 1
        
        # clean up
        return self.clusters

    def cluster_expand(self, idat):
        """Expand cluster recursively"""
        for qq in self.k_ind[idat, :]:
            if (qq in self.aDST) and (self.aDST[qq]<=self.var*self.cluster_aDST):
                # add index to cluster
                self.clusters[self.nclust].append(qq)
                lcluster = len(self.clusters[self.nclust])
                self.cluster_aDST = (self.cluster_aDST*(lcluster-1)+self.aDST[qq])/lcluster
                self.aDST.pop(qq, None)
                self.cluster_expand(qq)