#!/usr/bin/python


import time
import sys
import RPi.GPIO as GPIO
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
lectura=[]
pnconf = PNConfiguration()
pnconf.publish_key = 'pub-c-bf95ca0b-8488-4488-be1e-057c9acdc089'
pnconf.subscribe_key = 'sub-c-ec10a3ee-8cf5-11e7-91ed-aa3b4df5deac'
pubnub = PubNub(pnconf)

def publish_callback(result, status):
    pass
    # Handle PNPublishResult and PNStatus

LIGHT=0
VIENTO=0
DIRECCION=0
LLUVIA=0

reset = 0

while True:
 try:
     reset=0
     infile = open('/home/pi/Desktop/single_chan_pkt_fwd-master/datos.txt', 'r')
     for line in infile:
        reset=reset+1     
     infile.close()


     infile = open('/home/pi/Desktop/single_chan_pkt_fwd-master/datos.txt', 'r')
     for line in infile:
        
        for j in line:
            if( 48<=ord(j) and ord(j)<=58 ):
                bandera=0
            elif(ord(j)==44 or ord(j)==45 or ord(j)==10):
                bandera=0
            else:
                bandera=2
                break
            
        #print(bandera)
        if(bandera!=2):
            ######################   AnO
            message=line.split(",")

            for k in message:
                lectura.append(int(k))
                
            print(lectura)
            if len(lectura)== 15:
                ANO=lectura[0]
                MES=lectura[1]
                DIA=lectura[2]
                HORA=lectura[3]
                MINUTO=lectura[4]
                SEGUNDO=lectura[5]
                ID=lectura[6]
                HUM=lectura[7]
                PRES=lectura[8]
                TEMP=lectura[9]
                LIGHT=lectura[10]
                EARTH=lectura[11]
                BATTERY=lectura[12]
                RSSI=lectura[14]
                VIENTO=0
                DIRECCION=0
                LLUVIA=0
                
            elif len(lectura)== 18:
                ANO=lectura[0]
                MES=lectura[1]
                DIA=lectura[2]
                HORA=lectura[3]
                MINUTO=lectura[4]
                SEGUNDO=lectura[5]
                ID=lectura[6]
                HUM=lectura[7]
                PRES=lectura[8]
                TEMP=lectura[9]
                LIGHT=lectura[10]
                EARTH=lectura[11]
                BATTERY=lectura[12]
                VIENTO=lectura[13]
                DIRECCION=lectura[14]
                LLUVIA=lectura[15]
                RSSI==lectura[17]
              
                
            print('Light',LIGHT,'Earth',EARTH,'Humidity',HUM,'Pression',PRES,'Temperature',TEMP,'Battery',BATTERY,'RSSI',RSSI,'Wind',VIENTO,'Direction',DIRECCION,'Rain',LLUVIA)
            IDstring='%02d' % (ID)
            channelID='agrostick'+IDstring
            pubnub.publish().channel(channelID).message({'eon':{'Light':LIGHT,'Earth':EARTH,'Humidity':HUM,'Pression':PRES,'Temperature':TEMP,'Battery':BATTERY,'RSSI':RSSI,'Wind':VIENTO,'Direction':DIRECCION,'Rain':LLUVIA}}).async(publish_callback)
            print channelID
            
            time.sleep(0.2)
            for n in lectura[:]:
                  lectura.remove(n)
            print lectura
        else:
            print("Archivo vacio o cadena con error")
             
     
                          
     infile.close()
    
     infile=open('/home/pi/Desktop/single_chan_pkt_fwd-master/datos.txt', 'w')
     infile.close()
     time.sleep(2)
    

 except(IndexError,TypeError,ValueError):
     TIME=time.localtime()
     YEARP=TIME[0]
     MONTHP=TIME[1]
     DAYP=TIME[2]
     HOURP=TIME[3]
     MINUTEP=TIME[4]
     SECONDP=TIME[5]
     print("Error de indexado detectado")
     infile=open('/home/pi/Desktop/single_chan_pkt_fwd-master/datos.txt', 'w')
     infile.close()
     infile=open('/home/pi/Desktop/single_chan_pkt_fwd-master/errores.txt', 'a')
     infile.write("%s/%s/%s  %s:%s:%s  Error de indexado, mensaje con error\n" % (DAYP,MONTHP,YEARP,HOURP,MINUTEP,SECONDP))
     #break            ###Para cancelar proceso con ctrl+c
     time.sleep(2)
     
 except(IOError):
     TIME=time.localtime()
     YEARP=TIME[0]
     MONTHP=TIME[1]
     DAYP=TIME[2]
     HOURP=TIME[3]
     MINUTEP=TIME[4]
     SECONDP=TIME[5]
     print("Error Archivo no encontrado")
     infile=open('/home/pi/Desktop/single_chan_pkt_fwd-master/errores.txt', 'a')
     infile.write("%s/%s/%s  %s:%s:%s  Archivo no encontrado\n" % (DAYP,MONTHP,YEARP,HOURP,MINUTEP,SECONDP))
     #break            ###Para cancelar proceso con ctrl+c
     time.sleep(5)
     
 except:
     TIME=time.localtime()
     YEARP=TIME[0]
     MONTHP=TIME[1]
     DAYP=TIME[2]
     HOURP=TIME[3]
     MINUTEP=TIME[4]
     SECONDP=TIME[5]
     print("Error detectado")
     infile=open('/home/pi/Desktop/single_chan_pkt_fwd-master/errores.txt', 'a')
     infile.write("%s/%s/%s  %s:%s:%s  Error detectado, revisar internet\n" % (DAYP,MONTHP,YEARP,HOURP,MINUTEP,SECONDP))
     if(reset>=5):
        infile=open('/home/pi/Desktop/single_chan_pkt_fwd-master/datos.txt', 'w')
        infile.close()
     #break            ###Para cancelar proceso con ctrl+c
     time.sleep(2)
 
     
