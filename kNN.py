import random 
# Choose one center uniformly at random from among the data points.
# For each data point x, compute D(x), the distance between x and the nearest center that has already been chosen.
# Choose one new data point at random as a new center, using a weighted probability distribution where a point x is chosen with probability proportional to D(x)2.
# Repeat Steps 2 and 3 until k centers have been chosen.
# Now that the initial centers have been chosen, proceed using standard k-means clustering.

#kmeans++ initialization of labels. data being a dictionary

def kMeansPPlusInitalization(data, distancematrix, numclusters):
    initialpoints = dict()
    initialpoints[numclusters] = [random.sample(data.keys(),1)]
    numclusters -=1
    while numclusters:
        initialpoints[numclusters] = getNextPoint(data.keys(), distancematrix, initialpoints)
        numclusters -=1

    return initialpoints
        


def getNextPoint(keys, distancematrix, initialpoints):
    genDistanceDict = dict()
    for i in keys:
        minimum = 999999999
        if i in initialpoints.values():
            continue
        for j in initialpoints.values():
            if(distancematrix[i][j] < minimum):
                minimum = distancematrix[i][j]
        genDistanceDict[i] = minimum
    

    
    #code for prob. pick to be written
    
    


#nearestPoints be the list of list of two elements with point and label
def classifyPoints(nearestPoints, givenPoint):



