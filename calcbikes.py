import xmltodict
import csv
import requests
import os.path
from collections import Counter
import datetime
import os, errno

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else: raise

def unix_time(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta = dt - epoch
	return delta.total_seconds()

def unix_time_millis(dt): return unix_time(dt) * 1000.0

def bikestrdate(strt):
	return datetime.datetime.strptime(strt,'%m/%d/%Y %H:%M')

for filenum in range(0:10):
	with open('2013-3/'+str(filenum)) as csvfile:
		bikesreader = csv.DictReader(csvfile)
		for bike in  bikesreader:
			


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
	filename = '2013-3/'
	mkdir_p(filename)
	linecount = 0
	f = open(filename+str(linecount),'w')
	f.write('terminals,datetime,duration,bike_num\n')
	bikesreader = csv.DictReader(csvfile)
	for bike in  bikesreader:
		if bike['Start terminal'] in stations and bike['End terminal'] in stations:
			if linecount>1000 :
				f.close()
				f = open(filename+str(linecount/1000),'w')
				f.write('terminals,datetime,duration,bike_num\n')
			term_trip = str(bike['Start terminal'])+'_'+str(bike['End terminal'])
			duration = bike['Duration'].replace('h','').replace('m','').replace('s','').split()
			duration_secs = str(int(duration[0])*3600 +int(duration[1])*60 + int(duration[2]))
			start_epoch = str(unix_time(bikestrdate(bike['Start date'])))
			bike_num = bike['Bike#']
			f.write(','.join([term_trip,start_epoch,duration_secs,bike_num])+'\n')
			linecount+=1
	f.close()
#			stationstime[bike['Start terminal']]+=duration_secs
#			stationscount[bike['Start terminal']]+=1
#
#			bike.update({'startgeo':stations[bike['Start terminal']]})
#			bike.update({'endgeo':stations[bike['End terminal']]})
#			bike.update({'startend':bike['Start terminal']+'_'+bike['End terminal']})
#			bikes.append( bike)
#			journeys.update({bike['startend']:(bike['startgeo'],bike['endgeo'])})
#	print len(bikes)
#	print(stationstime.most_common())
#	stationsavg = {}
#	for key in stationstime.keys():
#		stationsavg[key]=round(stationstime[key]*1.0/stationscount[key]);
#	print(stationsavg)
#	g = open('stationstime.txt','w')
#	for key,val in stationsavg.iteritems():
#		g.write(key+','+str(val)+'\n')
#
#	exit()
#	for key,j in journeys.iteritems():
#		if not os.path.isfile("googledirections/"+key):
#			start = ','.join(j[0])
#			end = ','.join(j[1])
#			print start,end
#			apikey = "AIzaSyDAk6Qe-QxiuSQi4M41RUt0RK7dKjS3sR0" #m2
#			apikey = "AIzaSyAJdK4qxDTTEpT2ha1bjnPyxQBGFOMDW6U" #6
#			apikey = "AIzaSyAMCocd925ayO9xxf4wwT-XkL94Gf8GuzY" #L
#			url = "https://maps.googleapis.com/maps/api/directions/json?origin="+start+"&destination="+end+"&sensor=false&key="+apikey +"&avoid=highways&mode=bicycling"
#			r = requests.get(url)
#			if  "xceed" in r.text: break
#			w = open("googledirections/"+key,'w')
#			w.write(r.text.encode('utf-8'))
#			w.close()
#	print len(journeys)
