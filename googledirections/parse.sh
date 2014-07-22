#!/bin/bash

args=("$@")
#echo $# argu
echo $args
lsr=$(ls $1*)
echo "{" >$1
for arg in $lsr
do
	echo '"'${arg}'":' >>$1
	jq '{distance: .routes[].legs[].distance.value, duration: .routes[].legs[].duration.value,polyline: .routes[].overview_polyline.points, id: "'"${arg}"'" }' $arg >>$1
	echo ',' >>$1
done

echo '"xxxxx":{}}'>>$1
