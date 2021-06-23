#!/bin/sh

#NOW=$(date +"%d-%m-%Y" --date="-1 day ago")
NOW="17-06-2021"
echo "Shell script implementation to check for vaccine availability for $NOW"

response=$(curl https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict\?district_id\=380\&date\=$NOW)

centers=$(echo $response | jq -r '.centers')

for center in $centers
do
    echo $center 
done

#echo $message
echo $centers