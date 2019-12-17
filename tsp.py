import copy

distancematrix = [
    [0, 7.33, 9, 12],
    [7.33, 0, 6.43, 4.2],
    [9, 6.43, 0, 8],
    [12, 4.2, 8, 0]
]

nodekeys = [0,1,2,3]
start = nodekeys[0]

endpoints = nodekeys[1:]

dp = {}

for i in endpoints:
    dp[(start,i), i] = distancematrix[start][i]

print(dp)


# def tspsolve(nodekeys, distancematrix, start):
#     path = [start]
#     #get next city to visit and add to the list


#     return path


def dpcost(currset, end, distancematrix):
    currset = tuple(currset)
    if (currset,end) in dp.keys():
        return dp[currset,end]
    
    # pathnew = dict()
    
    setnew = copy.deepcopy(list(currset))
    setnew.remove(end)
    setnew = tuple(setnew)
    minlist = []
    for j in currset:
        if j != end and j!=start:
            minlist.append(dpcost(setnew,j,distancematrix) + distancematrix[j][end])
    
    minimum = min(minlist)

    dp[currset,end] = minimum

    return dp[currset,end]

def createdp(currset,start = 0):
    for i in currset:
        if i != start:
            dpcost(currset,i, distancematrix)
    
def findpath(distancematrix, dp, currset, path = [], start= 0):
    currsetstart = tuple(currset)
    currset.remove(start)
    prevval = start
    path.append(start)
    while(len(currset) > 1):
        
        minimum = dp[currsetstart,currset[0]] + distancematrix[currset[0]][prevval]
        minval = currset[0]
        for i in currset:
            if(minimum > dp[currsetstart,i] + distancematrix[i][prevval]):
                minimum = dp[currsetstart,i] + distancematrix[i][prevval]
                minval = i
        path.append(minval)
        currsetstart = copy.deepcopy(list(currsetstart))
        currsetstart.remove(minval)
        currsetstart = tuple(currsetstart)
        currset.remove(minval)
        prevval = minval
    
    path.append(currset[0])
    path.append(start)
    path.reverse()
    return path

        
        
createdp(nodekeys)
print(findpath(distancematrix,dp,nodekeys, []))








print(dp)

