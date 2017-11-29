# imports
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.neighbors import NearestNeighbors

class DBSCANKMeans():
    """Class to perform DBSCAN and Kmeans in series"""
    def __init__(self, **params):
        """Initialize variables
        
        Inputs:
            scale [0]: value to scale dimension d of data for min_points estimate in DBSCAN
                       default 0 means scale by number of samples divided by 500
            q [80]: quantile (percent) of k-nearest-neighbor for eps estimate in DBSCAN
        """
        # default parameters
        self.scale = 0
        self.q = 80
        
        if params:
            if "q" in params:
                self.q = params["q"]
            if "scale" in params:
                self.scale = params["scale"]
        
    def fit(self, X, **stand):
        """Fit dbscan parameters to data
        
        Inputs:
            X: dataframe (n_data, n_features)
            stand [False]: to standardize data or not (optional)
            plot [False]: to plot k nearest-neighbor graph or not (optional)
            
        Outputs:
            eps: esp parameter for dbscan
            min_points: min_points parameter for dbscan
        """
        # pass variable
        self.X = X
        if self.scale==0:
            self.scale = max(2, np.rint(self.X.shape[0]/1000))
        
        # standardize features
        if stand:
            if "stand" in stand:
                if bool(stand["stand"]):
                    self.X = (self.X-self.X.mean(axis=0))/self.X.std(axis=0)
        
        # set min_points parameter
        self.min_points = self.scale*self.X.shape[1]

        # initialize nearest-neighbor object
        nbrs = NearestNeighbors(n_neighbors=self.min_points,
                                metric="euclidean")
        
        # fit nearest-neighbors
        nbrs_fit = nbrs.fit(self.X)
        self.kdist, self.kind = nbrs_fit.kneighbors(self.X)
        
        # estimate eps paramter
        self.eps = np.percentile(self.kdist[:, -1], q=self.q)
        
        # optional plot
        if stand:
            if "plot" in stand:
                if bool(stand["plot"]):
                    self.plot_knn()
                    
        # clean up
        return self.eps, self.min_points
                    
    def fit_predict(self, X, **stand):
        """Fit dbscan parameters to data
        
        Inputs:
            X: dataframe (n_data, n_features)
            stand [False]: to standardize data or not (optional)            
        Output:
            label_kmeans: labeled pitches
        """
         # pass variable
        self.X = X
        if self.scale==0:
            self.scale = max(2, np.rint(self.X.shape[0]/1000))
            
        # standardize features
        if stand:
            if "stand" in stand:
                if bool(stand["stand"]):
                    self.X = (self.X-self.X.mean(axis=0))/self.X.std(axis=0)
        
        # set min_points parameter
        self.min_points = int(self.scale*self.X.shape[1])

        # initialize nearest-neighbor object
        nbrs = NearestNeighbors(n_neighbors=self.min_points,
                                metric="euclidean")
        
        # fit nearest-neighbors
        nbrs_fit = nbrs.fit(self.X)
        self.kdist, self.kind = nbrs_fit.kneighbors(self.X)
        
        # estimate eps paramter
        self.eps = np.percentile(self.kdist[:, -1], q=self.q)
        
        # initialize dbscan object
        dbscan = DBSCAN(eps=self.eps,
                        min_samples=self.min_points,
                        metric="euclidean",)
        
        # fit and predict labels with dbscan
        self.label_dbscan = dbscan.fit_predict(self.X)

        # use pandas to calculate centroids
        self.X_grouped = pd.concat([self.X.reset_index(drop=True),
                                    pd.Series(self.label_dbscan, name="ptype")],
                                    axis=1)

        # calculate centroids and number of clusters
        self.centroids_init = self.X_grouped.groupby("ptype").mean().iloc[1:, :]
        self.k = self.centroids_init.shape[0]
        
        # perform K-means
        kmeans = KMeans(n_clusters=self.k,
                        init=self.centroids_init,
                        n_init=1)
        self.label_kmeans = kmeans.fit_predict(self.X)

        # clean up
        return self.label_kmeans
        
    def plot_knn(self):
        """Return plot of sorted distances for a given K nearest neighbor"""     
        # sort distances for plotting
        kk = np.sort(self.kdist[:, -1])

        # plot sorted distance as a function of data point index
        plt.plot(kk)
        plt.xlabel("Observation index")
        plt.ylabel("Euclidean distance")
        plt.axhline(y=np.percentile(kk, q=self.q),
                    color='k',
                    ls='dashed',)
        plt.show()