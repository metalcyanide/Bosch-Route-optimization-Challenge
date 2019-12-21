# importing dependencies 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
import sys 
from statistics import mean 
   
# # creating data 
# mean_01 = np.array([0.0, 0.0]) 
# cov_01 = np.array([[1, 0.3], [0.3, 1]]) 
# dist_01 = np.random.multivariate_normal(mean_01, cov_01, 10) 
   
# mean_02 = np.array([6.0, 7.0]) 
# cov_02 = np.array([[1.5, 0.3], [0.3, 1]]) 
# dist_02 = np.random.multivariate_normal(mean_02, cov_02, 10) 
   
# mean_03 = np.array([7.0, -5.0]) 
# cov_03 = np.array([[1.2, 0.5], [0.5, 1,3]]) 
# dist_03 = np.random.multivariate_normal(mean_03, cov_01, 10) 
   
# mean_04 = np.array([2.0, -7.0]) 
# cov_04 = np.array([[1.2, 0.5], [0.5, 1,3]]) 
# dist_04 = np.random.multivariate_normal(mean_04, cov_01, 10) 
   
# data = np.vstack((dist_01, dist_02, dist_03, dist_04)) 
# np.random.shuffle(data) 

latlongdict = { 'BTM 2nd stage': (12.9125291, 77.5982493), 'Koramangala': (12.9350054, 77.6115462), 'Anand Ashram': (12.9268719, 77.5990938), 'Vijaya Bank Adugodi': (12.9378759, 77.5944627), 'Hulimavu Gate': (12.8881313, 77.5914776), 'Adugodi': (12.9435045, 77.6075158), 'Austin Town': (12.9567638, 77.6129863), 'Viveknagar': (12.9521797, 77.6188548), 'Adugodi Signal': (12.9436745, 77.6077108), 'Mico Layout': (12.9164844, 77.6016567), 'Ashram HDFC Bank': (12.9485816, 77.5797068), 'Lakkasandra Bus Stop': (12.9368414, 77.6004492), 'Arakere BTS Layout': (12.9229302, 77.5663966), 'Aneypalya': (12.9478156, 77.6027586), 'Arakere Layout': (12.9229302, 77.5663966), 'Bannerghatta Road': (12.9089725, 77.5979482), 'Arakere Gate': (12.889589, 77.5976873), 'Sagar Appolo Hospital': (12.9268719, 77.5990938), 'Canara Bank': (12.9481897, 77.6002658), 'BPL Stop': (12.887181, 77.5970994), 'Mico Signal': (12.9442415, 77.6026388), 'Udupi Guarden': (12.9176934, 77.6089431), 'BTM': (12.9164844, 77.6016567), 'Jayadeva Hospital Junction': (12.9175363, 77.5999589), 'Arekere Gate': (12.889589, 77.5976873), 'Ashram Bus Stop': (12.9268719, 77.5990938), 'Ashram': (12.9268719, 77.5990938), 'Spar Stop': (12.9640503, 77.5711259), 'Koramangala Police Station': (12.9408786, 77.6198734), 'Gottigere': (12.8560296, 77.5886844), 'Silk Board': (12.9169078, 77.6216554), 'Dairy Circle': (12.9389163, 77.6008787), 'Thilaknagar': (12.9218711, 77.5986135), 'Koramangala Depot': (12.9420488, 77.6232414)}
data = []
for i in latlongdict.keys():
    data.append(latlongdict[i])

data = np.asarray(data)

# print(data)

# function to compute euclidean distance 
def distance(p1, p2): 
    return np.sum((p1 - p2)**2) 

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
            data.shape[0]), :].tolist())
    temp_data=data.tolist()
    temp_data.append('dummy')
    
   
    ## compute remaining no_of_clusters - 1 centroids 
    for c_id in range(no_of_clusters-1): 
          
        ## initialize a list to store distances of data 
        ## points from nearest centroid 
        dist = [] 
        for i in range(data.shape[0]):
            if [data[i,:].tolist()]*len(centroids)!=centroids:
                temp_sum=1
                for j in range(c_id+1):
                    #dist.append(distance(data[i,:],centroids[c_id]))
                    temp_sum *= distance(data[i,:],centroids[j])**2
                dist.append(temp_sum)
            else:
                dist.append(0)
        pdf=(dist/sum(dist)).tolist()
        pdf.append(0)
        next_centroid = np.random.choice(temp_data,p=pdf)
        centroids.append(next_centroid)
    return centroids 
   
def classify_a_point(point, groups):
    index=-1
    dist=[]
    for i in range(len(groups)):
        temp_dist=[]
        for j in range(len(groups[i])):
            temp_dist.append(distance(point,groups[i][j]))
        dist.append((mean(temp_dist),i))
    m=sys.maxsize
    for d in dist:
        if d[0]<m:
            m=d[0]
            index=d[1]
    
    return index

def inversedict(placeDict):
    inversedict = dict()
    for i in placeDict.keys():
        inversedict[placeDict[i]] = i
    
    return inversedict

def cluster(data, no_of_clusters, placeDict, peopleDict):
    groups=initialize(data, no_of_clusters)
    groups=[[element] for element in groups]
    groupstuple=[[] for element in groups]

    for i in range(len(groups)):
        for j in groups[i]:
            groupstuple[i].append(tuple(j))

    clusterDict = dict()
    placeInvDict = inversedict(placeDict)

    for i in range(data.shape[0]):
        group_no = classify_a_point(data[i,:], groups)
        if groups[group_no][0] != data[i,:].tolist():
            groups[group_no].append(data[i,:])
            groupstuple[group_no].append(tuple(data[i,:]))
    for i in range(no_of_clusters):
        clusterDict[i] = groupstuple[i]

    numpeople = dict()

    for i in clusterDict:
        clusterdetails = clusterDict[i]
        clusterdetails = list(set(clusterdetails))
        clusterDict[i] = clusterdetails
        
    for i in range(no_of_clusters):
        count = 0
        places = []

        for j in clusterDict[i]:
           places.append(str(placeInvDict[j]))
           count +=peopleDict[placeInvDict[j]]
        clusterDict[i] = places
        numpeople[i] = count
    return groups, clusterDict, numpeople

def plot_clusters(groups, numclusters):
    for i in range(0, numclusters):
        plt.scatter(*zip(*groups[i]),[6])
    
    plt.show()

def findSuitablek(data, minimum, maximum):
    mumcluster = minimum
    groups, clusterDict, numpeople = cluster(data, numcluster) 
    diff = []
    for i in range(minimum, maximum+1):
        groups = cluster(data,numcluster)
        minlen = min([len(i) for i in groups])
        maxlen = max([len(i) for i in groups])
        diff.append(maxlen - minlen)
    mindiff = min(diff)
    for i in len(diff):
        if(diff[i] == mindiff):
            return i+minimum


def groupclusters(data, numcluster, seats):
    groups, clusterDict, numpeople = cluster(data, numcluster)
    gcluster = [[], [], []]

    for i in groups:
        if(len(groups) < 0.6 * seats):
            gcluster[0].append(i)
        elif (len(groups) <1.2 * seats):
            gcluster[1].append(i)
        else:
            gcluster[2].append(i)
    
    for i in gcluster[2]:
        getgroup = cluster(i, len(i)/(0.85 * seats))
        for j in getgroup:
            gcluster[1].append(i)
    
    return gcluster[1]

peopleDict = {'Bosch Bidadi': 0, 'BTM 2nd stage': 1, 'Koramangala': 7, 'Anand Ashram': 1, 'Vijaya Bank Adugodi': 1, 'Hulimavu Gate': 1, 'Adugodi': 1, 'Austin Town': 2, 'Viveknagar': 5, 'Adugodi Signal': 22, 'Mico Layout': 4, 'Ashram HDFC Bank': 1, 'Lakkasandra Bus Stop': 2, 'Arakere BTS Layout': 1, 'Aneypalya': 1, 'Arakere Layout': 1, 'Bannerghatta Road': 4, 'Arakere Gate': 1, 'Sagar Appolo Hospital': 1, 'Canara Bank': 4, 'BPL Stop': 1, 'Mico Signal': 6, 'Udupi Guarden': 2, 'BTM': 5, 'Jayadeva Hospital Junction': 2, 'Arekere Gate': 5, 'Ashram Bus Stop': 1, 'Ashram': 1, 'Spar Stop': 1, 'Koramangala Police Station': 3, 'Gottigere': 2, 'Silk Board': 1, 'Dairy Circle': 1, 'Thilaknagar': 2, 'Koramangala Depot': 1}
placeDict = {'Bosch Bidadi': (12.7972, 77.4239), 'BTM 2nd stage': (12.9125291, 77.5982493), 'Koramangala': (12.9350054, 77.6115462), 'Anand Ashram': (12.9268719, 77.5990938), 'Vijaya Bank Adugodi': (12.9378759, 77.5944627), 'Hulimavu Gate': (12.8881313, 77.5914776), 'Adugodi': (12.9435045, 77.6075158), 'Austin Town': (12.9567638, 77.6129863), 'Viveknagar': (12.9521797, 77.6188548), 'Adugodi Signal': (12.9436745, 77.6077108), 'Mico Layout': (12.9164844, 77.6016567), 'Ashram HDFC Bank': (12.9485816, 77.5797068), 'Lakkasandra Bus Stop': (12.9368414, 77.6004492), 'Arakere BTS Layout': (12.9229302, 77.5663966), 'Aneypalya': (12.9478156, 77.6027586), 'Arakere Layout': (12.9229302, 77.5663966), 'Bannerghatta Road': (12.9089725, 77.5979482), 'Arakere Gate': (12.889589, 77.5976873), 'Sagar Appolo Hospital': (12.9268719, 77.5990938), 'Canara Bank': (12.9481897, 77.6002658), 'BPL Stop': (12.887181, 77.5970994), 'Mico Signal': (12.9442415, 77.6026388), 'Udupi Guarden': (12.9176934, 77.6089431), 'BTM': (12.9164844, 77.6016567), 'Jayadeva Hospital Junction': (12.9175363, 77.5999589), 'Arekere Gate': (12.889589, 77.5976873), 'Ashram Bus Stop': (12.9268719, 77.5990938), 'Ashram': (12.9268719, 77.5990938), 'Spar Stop': (12.9640503, 77.5711259), 'Koramangala Police Station': (12.9408786, 77.6198734), 'Gottigere': (12.8560296, 77.5886844), 'Silk Board': (12.9169078, 77.6216554), 'Dairy Circle': (12.9389163, 77.6008787), 'Thilaknagar': (12.9218711, 77.5986135), 'Koramangala Depot': (12.9420488, 77.6232414)}

groups , clusterDict,numpeople = cluster(data, 2, placeDict, peopleDict)



print(len(clusterDict[0]))
print(len(clusterDict[1]))

print(clusterDict)
print(numpeople)
plot_clusters(groups, 2)

