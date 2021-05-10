from datetime import date
import time
import requests
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib

application = app = Flask(__name__)
def callapi():
    newHeaders = {'user-agent': 'personal-trakcer', "Accept-Language": "en_US"}
    pin = '110029'
    d = str(date.today())
    today = d.split('-')
    today = '-'.join(today[::-1])
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}'.format(pin,today)
    r = requests.get(url,headers = newHeaders)
    result = r.json()
    results = result['centers']
    li = ['List:']
    for i in results:
        #print(i['name'],i['center_id'])
        for j in i['sessions']:
            if j["available_capacity"] >0:
                print(j["available_capacity"],j["date"])
                li.append(str(i['name']))
                li.append(str(j["available_capacity"]))
                li.append(str(j["date"]))
                li.append(';;;;')
            else:
                pass
                # print(j["date"],"NOPE")
    if len(li)>1:
        message = 'Subject: Email for Vaccine availability \n\n'+': '.join(li)
        sendmail(message)
        #s.sendmail(u_email, r_email, message)
    return r

def sendmail(message):
    u_email = 'tinydeveloperkush@gmail.com'
    u_Password = '@Kush1234'

    r_email = 'khush.grandhi@gmail.com'
    #smtplib.SMTP.connect()
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    s.login(u_email, u_Password)

    s.sendmail(u_email, r_email, message)
    s.quit()

@app.route("/")
def index():
    r = callapi()
    return r.json()
@app.before_first_request
def initialize():
    scheduler = BackgroundScheduler()
    scheduler.add_job(callapi, 'interval', seconds=120, id='my_job')
    scheduler.start()

if __name__ == '__main__': 
    app.run(debug = True) 
