import os
import time
import sys
import random
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
 
pnconf = PNConfiguration()
 
pnconf.publish_key = 'pub-c-bf95ca0b-8488-4488-be1e-057c9acdc089'
pnconf.subscribe_key = 'sub-c-ec10a3ee-8cf5-11e7-91ed-aa3b4df5deac'

pubnub = PubNub(pnconf)
print("ok")


def publish_callback(result, status):
    pass
    # Handle PNPublishResult and PNStatus


while(1):
    lig=random.randrange(15)
    pres=random.randrange(15)
    hum=random.randrange(15)
    temp=random.randrange(15)
    bat=random.randrange(15)
    ssr=random.randrange(15)
    rai=random.randrange(15)
    wspe=random.randrange(15)
    wdir=random.randrange(15)
    
    pubnub.publish().channel('agrostick08').message({'eon':{'Light':lig,'Pressure':pres,'Humidity':hum,'Temperature':temp,'Battery':bat,'SSR':ssr}}).async(publish_callback)
    
    print(time.time())
    time.sleep(0.5)
