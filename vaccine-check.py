import json
import requests
import time
from tkinter import *  
from tkinter import messagebox  

def handler(pincodes, date):
    api_endpoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"
    
    center_detail = ""
    message = ""

    for code in pincodes:
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
        res = requests.get(api_endpoint.format(code, date), headers=headers)
        #res = requests.get(api_endpoint.format(code, date))

        try: 
            print("API response for: " + str(code) + " was: " + json.dumps(res.json()))
        except Exception as e:
            print("Response: " + str(res))
            print("Error: " + str(e))
        center_detail = ""
        if res.status_code != 200:
            print("Error response: " + str(res.reason))
            return {"Response": res.status_code}
    
        if res.status_code != 200:
            print("Error response: " + str(res.reason))
            return {"Response": res.status_code}
    
        if res.json()["centers"]:
            count = 1
            for center in res.json()["centers"]:
                center_detail += str(count) + ". Name: {}, Fee type: {}".format(center["name"], center["fee_type"])

                for session in center["sessions"]:
                    center_detail += "\n\t Date: {} Availability: {}".format(session["date"], session["available_capacity"])

            message = "The vaccine is now available for the week following: {} for PIN: {}\n{} \n\n".format(date, code, center_detail)

            count += 1

    if center_detail:
        print(message)
        top = Tk()  
        top.geometry("100x100")  
        messagebox.showinfo("Available",message)    
        top.mainloop()  


# Set you pincode and date here
pincodes = ["442701", "442402"]
date = "09-05-2021"

# Time interval for checks in seconds
interval = 300

while True:
	handler(pincodes, date)
	time.sleep(interval)