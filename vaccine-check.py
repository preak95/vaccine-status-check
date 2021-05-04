import json
import requests
import time
from tkinter import *  
from tkinter import messagebox  

def handler(pincode, date):
    api_endpoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"
    
    # Get the details of vaccine availablity from the API
    res = requests.get(api_endpoint.format(pincode, date))
    
    print("API response was: " + json.dumps(res.json()))
    center_detail = ""
    if res.status_code != 200:
        print("Error response: " + str(res.reason))
        return {"Response": res.status_code}
    
    if res.json()["centers"]:
        count = 1
        for center in res.json()["centers"]:
        	center_detail += str(count) + ". Name: {}, Fee type: {}".format(center["name"], center["fee_type"])
    
        	for session in center["sessions"]:
        		center_detail += "\n Date: {} Availability: {}".format(session["date"], session["available_capacity"])
        		
        message = "The vaccine is now available for the week following: {} for PIN: {}\n{}".format(date, pincode, center_detail)
        
        count += 1

        top = Tk()  
        top.geometry("100x100")  
        messagebox.showinfo("Available",message)    
        top.mainloop()  


# Set you pincode and date here
pincode = "442701"
date = "09-05-2021"

# Time interval for checks in seconds
interval = 300

while True:
	handler(pincode, date)
	time.sleep(interval)