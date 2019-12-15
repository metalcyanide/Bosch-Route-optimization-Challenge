
# coding: utf-8



# importing dependencies 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import sys 
   
# creating data 
mean_01 = np.array([0.0, 0.0]) 
cov_01 = np.array([[1, 0.3], [0.3, 1]]) 
dist_01 = np.random.multivariate_normal(mean_01, cov_01, 100) 
   
mean_02 = np.array([6.0, 7.0]) 
cov_02 = np.array([[1.5, 0.3], [0.3, 1]]) 
dist_02 = np.random.multivariate_normal(mean_02, cov_02, 100) 
   
mean_03 = np.array([7.0, -5.0]) 
cov_03 = np.array([[1.2, 0.5], [0.5, 1,3]]) 
dist_03 = np.random.multivariate_normal(mean_03, cov_01, 100) 
   
mean_04 = np.array([2.0, -7.0]) 
cov_04 = np.array([[1.2, 0.5], [0.5, 1,3]]) 
dist_04 = np.random.multivariate_normal(mean_04, cov_01, 100) 
   
data = np.vstack((dist_01, dist_02, dist_03, dist_04)) 
np.random.shuffle(data) 

           
# function to compute euclidean distance 
def distance(p1, p2): 
    return np.sum((p1 - p2)**2) 
   
# initialisation algorithm 
def initialize(data, no_of_clusters): 
    ''' 
    intialized the centroids for K-means++ 
    inputs: 
        data - numpy array of data points having shape (200, 2) 
          
    '''
    ## initialize the centroids list and add 
    ## a randomly selected data point to the list 
    centroids = [] 
    centroids.append(data[np.random.randint( 
            data.shape[0]), :]) 
   
    ## compute remaining no_of_clusters - 1 centroids 
    for c_id in range(no_of_clusters - 1): 
          
        ## initialize a list to store distances of data 
        ## points from nearest centroid 
        dist = [] 
        for i in range(data.shape[0]): 
            point = data[i, :] 
            d = sys.maxsize 
              
            ## compute distance of 'point' from each of the previously 
            ## selected centroid and store the minimum distance 
            for j in range(len(centroids)): 
                temp_dist = distance(point, centroids[j]) 
                d = min(d, temp_dist) 
            dist.append(d) 
              
        ## select data point with maximum distance as our next centroid 
        dist = np.array(dist) 
        next_centroid = data[np.argmax(dist), :] 
        centroids.append(next_centroid) 
        dist = []  
    return centroids 

def classify_a_point(point, groups, k):
    index=-1
    dist=[]
    for i in range(len(groups)):
        for j in range(len(groups[i])):
            dist.append((distance(point,groups[i][j]),i))
    if len(dist)>k:
        dist=sorted(dist)[:k]
    else:
        dist=sorted(dist)
    #calculating frequencies of different groups
    freq=[0]*len(groups)
    #use if loops for no_of_clusters times 
    for e in dist:
        if e[1]==0:
            freq[0]+=1
        if e[1]==1:
            freq[1]+=1
        if e[1]==2:
            freq[2]+=1
        if e[1]==3:
            freq[3]+=1
    index = freq.index(max(freq))
    return index

def cluster(data, no_of_clusters, k):
    groups=initialize(data, no_of_clusters)
    groups=[[element] for element in groups]
    for i in range(data.shape[0]):
        group_no = classify_a_point(data[i,:], groups,k)
        groups[group_no].append(data[i,:])
    return groups


    
    
        
    
    
    
    



