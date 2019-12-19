import googlemaps 

'''
given a file location and delimiter
returns dictionary with names of places and number of people at each place
'''
def getNodeData(file_location, delimiter = ' '):
    f = open(file_location)
    lines = f.readlines()
    placesToVisit = []
    placeDict = dict()
    
    for i in lines:
        curr = i.split(delimiter)
        peopleatplace = int(curr[0]) #no.of persons
        currplace = " ".join(curr[2:])
        if currplace in placeDict.keys():
            placeDict[currplace] = placeDict.get(currplace) + peopleatplace
        else :
            placeDict[currplace] = peopleatplace

    return placeDict

'''
This takes in the apikey required to access google apis
and a boolean getdistance to get the distance dictionary among various nodes or to get time dictionary among various nodes

'''
def genDistanceMatrix(api_key, getdistance = 1, needtoappendcity = [], file_location = '/home/metalcyanide/cp/sample.txt', city = "Bengaluru"):
    gmaps = googlemaps.Client(key=api_key) 
    placeDict = dict()
    placeDict = getNodeData(file_location)
    
    if(getdistance):
        distancedict = dict()
        for i in placeDict.keys():
            if i in needtoappendcity:
                i = i + ' , ' + city
            tempDict = dict()
            for j in placeDict.keys():
                if j in needtoappendcity:
                    j = j + ' , ' + city
                my_dist = gmaps.distance_matrix(i,j)

                distancevalue = int(my_dist['rows'][0]['elements'][0]['distance']['value'])
                tempDict[j] = distancevalue
            distancedict[i] = tempDict
        
        return distancedict
    else:
        timedict = dict()
        for i in placeDict.keys():
            if i in needtoappendcity:
                i = i + ' , ' + city
            tempDict = dict()
            for j in placeDict.keys():
                if j in needtoappendcity:
                    j = j + ' , ' + city
                my_dist = gmaps.distance_matrix(i,j)
               
                print(i)
                print(j)
                print(my_dist['rows'][0]['elements'][0])  
                timevalue = int(my_dist['rows'][0]['elements'][0]['duration']['value'])
                tempDict[j] = timevalue
            timedict[i] = tempDict
        
        return timedict

'''
This gives us latitude longitute and makes corrections for non-familiar names that confuses google apis
One assumpution made is city diameter is less than 100km
'''
def getlatlong(api_key, end = 'Bosch Bidadi',file_location = '/home/metalcyanide/cp/sample.txt', city = "Bengaluru" ):
    gmaps = googlemaps.Client(key=api_key) 
    placeDict = dict()
    placeDict = getNodeData(file_location)
    # print(placeDict.keys())
    needtoappendcity = []
    latlongdict = dict()
    for i in placeDict.keys():
        # print(i)
        my_dist = gmaps.distance_matrix(i,end)
        # print(my_dist)
        if not(my_dist['rows'][0]['elements'][0]['status'] == "OK"):
            needtoappendcity.append(i)
            i = i+ ' , ' + city
        if (my_dist['rows'][0]['elements'][0]['status'] == "OK") and (int(my_dist['rows'][0]['elements'][0]['distance']['value']) > 100000):
            needtoappendcity.append(i)
            i = i+ ' , ' + city
        my_dist = gmaps.directions(i,end)
        # print(my_dist[0]['legs'][0]['start_location'])
        lat = my_dist[0]['legs'][0]['start_location']['lat']
        lng = my_dist[0]['legs'][0]['start_location']['lng']
        latlong = [lat, lng]
        latlongdict[i] = latlong
    
    return latlongdict, needtoappendcity





'''
this is run only once for given set of names and result is stored 
but if we want to do traffic adjustments we need to process this entire data after fixed amount of time
'''
# apikey = "AIzaSyB05i3p1oxUBiV0Sgbv1CBrVpRwzHHbd04"
apikey = "YOUR_API_KEY"
latlongtxt = open('latlongdict.txt', 'w') 
invalidcitytxt = open('invalidcity.txt', 'w')
latlongdict = dict()
latlongdict, needtoappendcity = getlatlong(apikey,file_location = "/home/metalcyanide/github/Route-optimization-Inter-IIT/sampledata/sample.txt" )
print(latlongdict, file = latlongtxt)
print(needtoappendcity, file = invalidcitytxt)
latlongtxt.close()
invalidcitytxt.close()

timetxt = open('timedict.txt', 'w') 
timedict = dict()
timedict = genDistanceMatrix(apikey,getdistance = 0,needtoappendcity = needtoappendcity ,file_location = "/home/metalcyanide/github/Route-optimization-Inter-IIT/sampledata/sample.txt" )
print(timedict, file = timetxt)
timetxt.close()

distancetxt = open('distancedict.txt', 'w') 
distancedict = dict()
distancedict = genDistanceMatrix(apikey, needtoappendcity = needtoappendcity,file_location = "/home/metalcyanide/github/Route-optimization-Inter-IIT/sampledata/sample.txt" )
print(distancedict, file = distancetxt)
distancetxt.close()


    
