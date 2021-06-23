import json
import datetime 
import requests
import time

tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")

api_endpoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=380&date={}"

center_detail = ""
message = ""

headers = {
            "Host": "cdn-api.co-vin.in",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        
# Get the details of vaccine availablity from the API
def handler():
    message = ""
    res = requests.get(api_endpoint.format(tomorrow))
    print(res.json())
    if res.json()["centers"]:
        count = 1
        center_detail = ""
        for center in res.json()["centers"]:
            for session in center["sessions"]:
                if session["available_capacity"] >= 0 and session["min_age_limit"] == 45: 
                    center_detail += str(count) + ". {} Availability: {}\n".format(center["name"], session["available_capacity"]) 
            
            message = "The vaccine is now available for following: {} for: \n{} \n\n".format(tomorrow, center_detail)
            count += 1 
    
        return message

    return "No centers"

interval = 90
while True:
	print(handler())
	time.sleep(interval)