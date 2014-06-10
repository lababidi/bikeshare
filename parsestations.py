import xmltodict
import csv
import requests
import os.path
doc = xmltodict.parse(open("bikeStations.xml").read())
stations = {}
bikes = []
journeys = {}
print doc
print len(doc['stations']['station'][0])
print doc['stations']['station'][0].keys()
for station in  doc['stations']['station']:
	print station
	stations.update({station['terminalName']:(station['lat'],station['long'])})
print stations
with open('2013-3rd-quarter.csv') as csvfile:
	bikesreader = csv.DictReader(csvfile)
	for bike in  bikesreader:
		print bike
		if bike['Start terminal'] in stations and bike['End terminal'] in stations:
			bike.update({'startgeo':stations[bike['Start terminal']]})
			bike.update({'endgeo':stations[bike['End terminal']]})
			bike.update({'startend':bike['Start terminal']+'_'+bike['End terminal']})
			bikes.append( bike)
			journeys.update({bike['startend']:(bike['startgeo'],bike['endgeo'])})
	print bikes
	print len(bikes)
	for key,j in journeys.iteritems():
		if not os.path.isfile("googledirections/"+key):
			start = ','.join(j[0])
			end = ','.join(j[1])
			print start,end
			apikey = "AIzaSyAJdK4qxDTTEpT2ha1bjnPyxQBGFOMDW6U" #6
			apikey = "AIzaSyAMCocd925ayO9xxf4wwT-XkL94Gf8GuzY" #L
			apikey = "AIzaSyDAk6Qe-QxiuSQi4M41RUt0RK7dKjS3sR0" #m2
			url = "https://maps.googleapis.com/maps/api/directions/json?origin="+start+"&destination="+end+"&sensor=false&key="+apikey +"&avoid=highways&mode=bicycling"
			r = requests.get(url)
			if  "xceed" in r.text: break
			w = open("googledirections/"+key,'w')
			w.write(r.text.encode('utf-8'))
			w.close()
	print len(journeys)
