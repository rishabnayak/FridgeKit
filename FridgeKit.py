import time,sys
import io
import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from picamera import PiCamera
from os import system
import RPi.GPIO as GPIO
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as CIImage
from twilio.rest import Client

cred = credentials.Certificate('/home/pi/Downloads/fridgekit-2018-firebase-adminsdk-wig17-26054cf441.json')

default_app = firebase_admin.initialize_app(cred)

db = firestore.client()
dataref =  db.collection(u'users').where(u'uname', u'==', u'rishab')
data = dataref.get()
getdata = next(data)
econtact = getdata.get('econtact')

account_sid = 'AC6acdb2a4ea804b400fcea7e220f6802d'
auth_token = '6286a0062217e5a3389802976b978d15'
client = Client(account_sid, auth_token)
camera = PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def COAlert(pin):
    message = client.messages \
        .create(
            body="Warning from your FridgeKit: high levels of CO2 present!",
            from_='+13396746836',
            to= econtact
             )
    return

def GasAlert(pin):
    message = client.messages \
        .create(
            body="Warning from your FridgeKit: high levels of flammable gas present!",
            from_='+13396746836',
            to= econtact
             )
    return

def pic(pin):
    camera.resolution = (1024, 768)
    camera.capture('pipic.jpg')
    app = ClarifaiApp(api_key='a8248cec12b340fb8a72faa082083aa9')
    model = app.models.get('food-items-v1.0')
    image = CIImage(file_obj=open('pipic.jpg', 'rb'))
    apiout = model.predict([image])
    out = (apiout["outputs"][0]["data"]["concepts"][0]["name"])
    dataref =  db.collection(u'users').where(u'uname', u'==', u'rishab')
    data = dataref.get()
    getdata = next(data)
    uid = getdata.get('uid')
    try:
      Inventory = getdata.get('Inventory')
      Inventory.append(out)
      print(Inventory)
      inv = {u'Inventory': Inventory}
      db.collection(u'users').document(uid).set(inv, merge = True)
    except:
      preinv = {u'Inventory': [out]
                }
      db.collection(u'users').document(uid).set(preinv, merge = True)
    return

GPIO.add_event_detect(17,GPIO.RISING, callback=pic)
GPIO.add_event_detect(2, GPIO.RISING, callback=COAlert, bouncetime=1000)
GPIO.add_event_detect(3, GPIO.RISING, callback=GasAlert, bouncetime=1000)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()