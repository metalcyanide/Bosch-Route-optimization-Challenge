import googlemaps 

def getnodedata(file_location):
    f = open(file_location)
    lines = f.readlines()
    placesToVisit = []
    placeDict = dict()
    
    for i in lines:
        curr = i.split()
        peopleatplace = int(curr[0]) #no.of persons
        currplace = " ".join(curr[2:])
        if currplace in placeDict.keys():
            placeDict[currplace] = placeDict.get(currplace) + peopleatplace
        else :
            placeDict[currplace] = peopleatplace

    return placeDict

#get distance matrix

def genDistanceMatrix(file_location = '/home/metalcyanide/cp/sample.txt', api_key):
    gmaps = googlemaps.Client(key=api_key) 
    placeDict = dict()
    placeDict = getnodedata(file_location)
    print(placeDict.keys())
    distancedict = dict()
    # return 0
    for i in placeDict.keys():
        print(i)
        tempDict = dict()
        for j in placeDict.keys():
            print(j)
            my_dist = gmaps.distance_matrix(i,j)
            print(my_dist)
            if not(my_dist['rows'][0]['elements'][0]['status'] == "OK"):
                continue
            distancevalue = int(my_dist['rows'][0]['elements'][0]['distance']['value'])
            tempDict[j] = distancevalue
        distancedict[i] = tempDict
    
    return distancedict

apikey = "YOUR_API_KEY"
mydict = dict()
mydict = genDistanceMatrix(apikey)
print(mydict)
