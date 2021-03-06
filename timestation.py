import xmltodict
import csv
import requests
import os.path
from collections import Counter
doc = xmltodict.parse(open("bikeStations.xml").read())
stations = {}
stationstime = Counter()
stationscount = Counter()
bikes = []
journeys = {}
#print doc
#print len(doc['stations']['station'][0])
#print doc['stations']['station'][0].keys()
for station in  doc['stations']['station']:
	stations.update({station['terminalName']:(station['lat'],station['long'])})
with open('2013-3rd-quarter.csv') as csvfile:
	bikesreader = csv.DictReader(csvfile)
	for bike in  bikesreader:
		if bike['Start terminal'] in stations and bike['End terminal'] in stations:
			duration = bike['Duration'].replace('h','').replace('m','').replace('s','').split()
			duration_secs = int(duration[0])*3600 +int(duration[1])*60 + int(duration[2])
			stationstime[bike['Start terminal']]+=duration_secs
			stationscount[bike['Start terminal']]+=1

			bike.update({'startgeo':stations[bike['Start terminal']]})
			bike.update({'endgeo':stations[bike['End terminal']]})
			bike.update({'startend':bike['Start terminal']+'_'+bike['End terminal']})
			bikes.append( bike)
			journeys.update({bike['startend']:(bike['startgeo'],bike['endgeo'])})
	print len(bikes)
	print(stationstime.most_common())
	stationsavg = {}
	for key in stationstime.keys():
		stationsavg[key]=round(stationstime[key]*1.0/stationscount[key]);
	print(stationsavg)
	g = open('stationstime.txt','w')
	for key,val in stationsavg.iteritems():
		g.write(key+','+str(val)+'\n')

	exit()
	for key,j in journeys.iteritems():
		if not os.path.isfile("googledirections/"+key):
			start = ','.join(j[0])
			end = ','.join(j[1])
			print start,end
			apikey = "AIzaSyDAk6Qe-QxiuSQi4M41RUt0RK7dKjS3sR0" #m2
			apikey = "AIzaSyAJdK4qxDTTEpT2ha1bjnPyxQBGFOMDW6U" #6
			apikey = "AIzaSyAMCocd925ayO9xxf4wwT-XkL94Gf8GuzY" #L
			url = "https://maps.googleapis.com/maps/api/directions/json?origin="+start+"&destination="+end+"&sensor=false&key="+apikey +"&avoid=highways&mode=bicycling"
			r = requests.get(url)
			if  "xceed" in r.text: break
			w = open("googledirections/"+key,'w')
			w.write(r.text.encode('utf-8'))
			w.close()
	print len(journeys)
