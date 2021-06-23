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
            "Cache-Control": "cf-no-cache"
        }
        
        # Get the details of vaccine availablity from the API
        res = requests.get(api_endpoint.format(code, date), headers=headers)
        #res = requests.get(api_endpoint.format(code, date))

        try: 
            print("API response for: " + str(code) + " was: {}".format(res.json()))
            pass
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
        flag = 0
        if res.json()["centers"]:
            count = 1
            for center in res.json()["centers"]:
                if center["center_id"] in  [668001, 702005] :
                    print("Found center {}:\n".format(center["name"]))
                    
                    center_detail += str(count) + ". Name: {}, Fee type: {}".format(center["name"], center["fee_type"])
            
                    for session in center["sessions"]:
                        if session["available_capacity"] > 0 and session["min_age_limit"] == 18 and session["date"] =="23-06-2021": 
                            flag = 1
                            center_detail += "\n Date: {} Availability: {}".format(session["date"], session["available_capacity"])
                        else:
                            print("\t{}+ No vaccine yet! {}\n".format(session["min_age_limit"], session["available_capacity"]))

            if flag == 1:       
                message = "The vaccine is now available for the week following: {} for PIN: {}\n{} \n\n".format(date, code, center_detail)

            count += 1

    if message:
        print(message)
        top = Tk()  
        top.geometry("100x100")  
        messagebox.showinfo("Available",message)    
        top.mainloop()  


# Set you pincode and date here
pincodes = ["442701"]
date = "24-06-2021"

# Time interval for checks in seconds
interval = 3

while True:
	handler(pincodes, date)
	time.sleep(interval)