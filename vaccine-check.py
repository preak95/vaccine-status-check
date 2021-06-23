import json
import requests
import time
from tkinter import *  
from tkinter import messagebox  
	
centers = {
    41255 : "Ballarpur RH",
    702005 : "2 Natyagruh Ballarpur 45 Above",
    41256 : "Ballarpur UPHC",
    668001: "Natyagrah Ballarpur (18-44)"
    #709873: "Visapur PHC",
    #653002: "Kothari",
    #43129: "Palasgaon"
}

def handler(pincodes, date, agelimit):
    api_endpoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"
    
    center_detail = ""
    message = ""

    for code in pincodes:
        headers = {
            "Host": "cdn-api.co-vin.in",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8",
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
            #print("API response for: " + str(code) + " was: {}".format(res.json()))
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
        count = 1
        if res.json()["centers"]:
            
            flag = 0
            for center in res.json()["centers"]: 
                if center["center_id"] in  centers :
                    print("Found center {}:\n".format(center["name"]))
                    session_count = 0
                    for session in center["sessions"]:
                        session_count += 1
                        if session["available_capacity"] > 0 and session["min_age_limit"] == agelimit and session["date"] == date:
                            print("Current center: {}".format(center["name"]))
                            center_detail += "\n" + str(count) + ". {}".format(center["name"])
                            flag = 1
                            center_detail += "\nAvailability: {}".format(session["available_capacity"])

                            print("Current message " + str(center_detail))
                        else:
                            print("\t{} - {}+ No vaccine yet! {} {}\n".format(center["name"],session["min_age_limit"], session["available_capacity"], session["date"]))
                            #print("** NOT AVAILABLE: {} **".format(center["center_id"]))

                    if flag == 1:
                        count+=1
                    
            print("-----------------------------------------")

            if flag == 1:     
                message += "The vaccine is now available for the day: {} for PIN: {}\n{} \n\n".format(date, code, center_detail)

    if message:
        print(message)
        top = Tk()  
        top.geometry("600x400")  
        a = Label(top, text=message)
        a.pack()
        #top.withdraw()
        top.mainloop()  
        


# Set you pincode and date here
pincodes = ["442701"]
date = "24-06-2021"
age_limit = 45

# Time interval for checks in seconds
interval = 3

while True:
	handler(pincodes, date, age_limit)
	time.sleep(interval)