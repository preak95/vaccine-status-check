import json
from logging import Handler
import boto3
import requests
import datetime

sns_topic = "arn:aws:sns:ap-south-1:055697220840:win-win"

def lambda_handler(event, context):
    # TODO implement
    pincode = "442701"
    date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
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
    api_endpoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"
    sns = boto3.client('sns')
    
    res = requests.get(api_endpoint.format(pincode, date), headers=headers)
    
    try: 
        print("API response was: " + str(res.json()))
    except Exception as e:
        print("Response: " + str(res))
        print("Error: " + str(e))
    center_detail = ""
    if res.status_code != 200:
        print("Error response: " + str(res.reason))
        return {"Response": res.status_code}
    
    if res.json()["centers"]:
        print(res.json())
        count = 1
        for center in res.json()["centers"]:
            if center["center_id"] == "668001":
                center_detail += str(count) + ". Name: {}, Fee type: {}".format(center["name"], center["fee_type"])
        
                for session in center["sessions"]:
                    if session["available_capacity"] >= 0 and session["min_age_limit"] == 18: 
                        center_detail += "\n Date: {} Availability: {}".format(session["date"], session["available_capacity"])
        		
        message = "The vaccine is now available for the week following: {} for PIN: {}\n{}".format(date, pincode, center_detail)
        
        # Push to SNS topic 
        res = sns.publish(
            TopicArn=sns_topic,
            Message=message
        )
        count += 1
        
        print("SNS response was: " + str(res))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

