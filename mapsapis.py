import googlemaps 

'''
given a file location and delimiter
returns dictionary with names of places and number of people at each place
'''
def getNodeDataTXT(file_location, delimiter = ','):
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


def getNodeData(file_location, delimiter = ',', start = 'Bosch Bidadi', startloc = (12.7972, 77.4239)):
    f = open(file_location)
    lines = f.readlines()
    placesToVisit = []
    placeDict = dict()
    peopleDict = dict()
    placeDict[start] = startloc
    peopleDict[start] = 0
    
    for i in lines:
        i = i.replace("\"", '').strip("\n")
        curr = i.split(delimiter)
        peopleatplace = 1 #no.of persons
        currplace = curr[2]
        lat = float(curr[3])
        lng = float(curr[4])
        latlong = tuple([lat, lng])
        if currplace in placeDict.keys():
            placeDict[currplace] = latlong
            peopleDict[currplace] = peopleDict.get(currplace) + peopleatplace
        else :
            placeDict[currplace] = latlong
            peopleDict[currplace] = peopleatplace
    print(peopleDict) #this gives dictionary with places as keys and no.of people at that place as value
    print(placeDict) #this gives dictionary with place names as keys and (lat, lng) co-ordinates as value
    return placeDict, peopleDict


'''
This takes in the apikey required to access google apis
and a boolean getdistance to get the distance dictionary among various nodes or to get time dictionary among various nodes

'''
def genDistanceMatrix(api_key, getdistance = 1, needtoappendcity = [], file_location = '/home/metalcyanide/cp/sample.txt', city = "Bengaluru"):
    gmaps = googlemaps.Client(key=api_key)  #connecting with google maps 
    placeDict = dict()
    placeDict, peopleDict = getNodeData(file_location)
    
    distancedict = dict()
    timedict = dict()

    for i in placeDict.keys():
        tempDict = dict()
        temptimDict = dict()
        for j in placeDict.keys():
            my_dist = gmaps.distance_matrix(placeDict[i],placeDict[j])

            print(i)
            print(j)
            print(my_dist['rows'][0]['elements'][0])
            distancevalue = int(my_dist['rows'][0]['elements'][0]['distance']['value'])
            timevalue = int(my_dist['rows'][0]['elements'][0]['duration']['value'])

            tempDict[j] = distancevalue
            temptimDict[j] = timevalue
        distancedict[i] = tempDict
        timedict[i] = temptimDict
    
    return distancedict, timedict

'''
This gives us latitude longitute and makes corrections for non-familiar names that confuses google apis
One assumpution made is city diameter is less than 100km
'''
def getlatlong(api_key, end = 'Bosch Bidadi',file_location = '/home/metalcyanide/cp/sample.txt', city = "Bengaluru" ):
    gmaps = googlemaps.Client(key=api_key) 
    placeDict = dict()
    placeDict = getNodeData(file_location)
    needtoappendcity = []
    latlongdict = dict()
    for i in placeDict.keys():
        my_dist = gmaps.distance_matrix(i,end)
        if not(my_dist['rows'][0]['elements'][0]['status'] == "OK"):
            needtoappendcity.append(i)
            i = i+ ' , ' + city
        if (my_dist['rows'][0]['elements'][0]['status'] == "OK") and (int(my_dist['rows'][0]['elements'][0]['distance']['value']) > 100000):
            needtoappendcity.append(i)
            i = i+ ' , ' + city
        my_dist = gmaps.directions(i,end)
        lat = my_dist[0]['legs'][0]['start_location']['lat']
        lng = my_dist[0]['legs'][0]['start_location']['lng']
        latlong = [lat, lng]
        latlongdict[i] = latlong
    
    return latlongdict, needtoappendcity





'''
this is run only once for given set of names and result is stored 
but if we want to do traffic adjustments we need to process this entire data after fixed amount of time
'''
apikey = "AIzaSyB05i3p1oxUBiV0Sgbv1CBrVpRwzHHbd04"

'''
this is for data where lat long is not given.
'''
# apikey = "YOUR_API_KEY"
# latlongtxt = open('latlongdict.txt', 'w') 
# invalidcitytxt = open('invalidcity.txt', 'w')
# latlongdict = dict()
# latlongdict, needtoappendcity = getlatlong(apikey,file_location = "/home/metalcyanide/github/Route-optimization-Inter-IIT/sampledata/data1.csv" )
# print(latlongdict, file = latlongtxt)
# print(needtoappendcity, file = invalidcitytxt)
# latlongtxt.close()
# invalidcitytxt.close()

timetxt = open('timedict.txt', 'w') 
timedict = dict()
distancedict = dict()
distancedict, timedict = genDistanceMatrix(apikey,file_location = "/home/metalcyanide/github/Route-optimization-Inter-IIT/sampledata/data1.csv" )
print(timedict, file = timetxt)
timetxt.close()

distancetxt = open('distancedict.txt', 'w') 
print(distancedict, file = distancetxt)
distancetxt.close()


    
