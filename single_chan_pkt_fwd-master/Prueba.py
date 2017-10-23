#!/usr/bin/python
#coding: UTF-8

import time
import sys
import RPi.GPIO as GPIO
import urllib2

baseURL1 = 'http://api.thingspeak.com/update?api_key=MIHD9Q35CQZML30X'
baseURL2 = 'http://api.thingspeak.com/update?api_key=XUP9Z0LRP65JLQ20'
baseURL3 = 'http://api.thingspeak.com/update?api_key=B1NIY0Y0MFIH3OF7'
baseURL4 = 'http://api.thingspeak.com/update?api_key=U8I7B3HDIIA5F85D'
baseURL5 = 'http://api.thingspeak.com/update?api_key=DGS4DOX4D085GID0'
baseURL6 = 'http://api.thingspeak.com/update?api_key=6J8918IMAA8R4MXW'
baseURL7 = 'http://api.thingspeak.com/update?api_key=A7360BNCN23KV12Y'
baseURL8 = 'http://api.thingspeak.com/update?api_key=L38XT6S1NATAFT5U'
baseURL9 = 'http://api.thingspeak.com/update?api_key=GF1QOASTELRC0NTN'
baseURL10 = 'http://api.thingspeak.com/update?api_key=OL7SO60G7H8TX34D'
baseURL15a = 'http://api.thingspeak.com/update?api_key=GQF6ZWLNQMV71RQV'
baseURL15b = 'http://api.thingspeak.com/update?api_key=YO7E44KURDSJJ3TF'

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
        k=0
        l=0
        m=0
        n=0
        o=0
        p=0
        q=0
        r=0
        s=0
        t=0
        u=0
        v=0
        w=0
        x=0
        y=0
        z=0
        za=0
        zb=0
        
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
######################   AÑO
            for i in line:
                if(i!=","):
                    k=k+1
                else:
                    break
            if k==4:
                YEAR=int(float((line[0]+line[1]+line[2]+line[3])))
                #print(YEAR)

            ######################  MES
            for i in line[k+1:]:
                if(i!=","):
                    l=l+1
                else:
                    break
            if l==1:
                MONTH=int(float((line[k+1])))
                #print(MONTH)
            if l==2:
                MONTH=int(float((line[k+1]+line[k+2])))
                #print(MONTH)

            ###################### DÍA
            for i in line[k+l+2:]:
                if(i!=","):
                    m=m+1
                else:
                    break
            if m==1:
                DAY=int(float((line[k+l+2])))
                #print(DAY)
            elif m==2:
                DAY=int(float((line[k+l+2]+line[k+l+3])))
                #print(DAY)

            ###################### HORA
            for i in line[k+l+m+3:]:
                if(i!=","):
                    n=n+1
                else:
                    break
            if n==1:
                HOUR=int(float((line[k+l+m+3])))
                #print(HOUR)
            elif n==2:
                HOUR=int(float((line[k+l+m+3]+line[k+l+m+4])))
                #print(HOUR)

            ###################### MINUTO
            for i in line[k+l+m+n+4:]:
                if(i!=","):
                    o=o+1
                else:
                    break
            if o==1:
                MINUTE=int(float((line[k+l+m+n+4])))
                
                #print(MINUTE)
            elif o==2:
                #print("a")
                MINUTE=int(float((line[k+l+m+n+4]+line[k+l+m+n+5])))
                #print(MINUTE)

            ###################### SECOND
            for i in line[k+l+m+n+o+5:]:
                if(i!=","):
                    p=p+1
                else:
                    break
            if p==1:
                SECOND=int(float((line[k+l+m+n+o+5])))
                #print(SECOND)
            elif p==2:
                SECOND=int(float((line[k+l+m+n+o+5]+line[k+l+m+n+o+6])))
                #print(SECOND)

            ###################### ID
            for i in line[k+l+m+n+o+p+6:]:
                if(i!=","):
                    q=q+1
                else:
                    break
            if q==1:
                ID=int(float((line[k+l+m+n+o+p+6])))
                #print(ID)
            elif q==2:
                ID=int(float((line[k+l+m+n+o+p+6]+line[k+l+m+n+o+p+7])))
                #print(ID)

            ###################### HUM
            for i in line[k+l+m+n+o+p+q+7:]:
                if(i!=","):
                    r=r+1
                else:
                    break
            if r==1:
                HUM=int(float((line[k+l+m+n+o+p+q+7])))
                #print(HUM)
            elif r==2:
                HUM=int(float((line[k+l+m+n+o+p+q+7]+line[k+l+m+n+o+p+q+8])))
                #print(HUM)

            ###################### PRES
            for i in line[k+l+m+n+o+p+q+r+8:]:
                if(i!=","):
                    s=s+1
                else:
                    break
            if s==1:
                PRES=int(float((line[k+l+m+n+o+p+q+r+8])))
                #print(PRES)
            elif s==2:
                PRES=int(float((line[k+l+m+n+o+p+q+r+8]+line[k+l+m+n+o+p+q+r+9])))
                #print(PRES)
            elif s==3:
                PRES=int(float((line[k+l+m+n+o+p+q+r+8]+line[k+l+m+n+o+p+q+r+9]+line[k+l+m+n+o+p+q+r+10])))
                #print(PRES)
            elif s==4:
                PRES=int(float((line[k+l+m+n+o+p+q+r+8]+line[k+l+m+n+o+p+q+r+9]+line[k+l+m+n+o+p+q+r+10]+line[k+l+m+n+o+p+q+r+11])))
                #print(PRES)
            elif s==5:
                PRES=int(float((line[k+l+m+n+o+p+q+r+8]+line[k+l+m+n+o+p+q+r+9]+line[k+l+m+n+o+p+q+r+10]+line[k+l+m+n+o+p+q+r+11]+line[k+l+m+n+o+p+q+r+12])))
                #print(PRES)
            elif s==6:
                PRES=int(float((line[k+l+m+n+o+p+q+r+8]+line[k+l+m+n+o+p+q+r+9]+line[k+l+m+n+o+p+q+r+10]+line[k+l+m+n+o+p+q+r+11]+line[k+l+m+n+o+p+q+r+12]++line[k+l+m+n+o+p+q+r+13])))
                #print(PRES)

            ###################### TEMP
            for i in line[k+l+m+n+o+p+q+r+s+9:]:
                if(i!=","):
                    t=t+1
                else:
                    break
            if t==1:
                TEMP=int(float((line[k+l+m+n+o+p+q+r+s+9])))
                #print(TEMP)
            elif t==2:
                if line[k+l+m+n+o+p+q+r+s+9]=="-":
                    TEMP=-1*int(float(line[k+l+m+n+o+p+q+r+s+10]))
                else:
                    TEMP=int(float((line[k+l+m+n+o+p+q+r+s+9]+line[k+l+m+n+o+p+q+r+s+10])))            
                #print(TEMP)
            elif t==3:
                if line[k+l+m+n+o+p+q+r+s+9]=="-":
                    TEMP=-1*int(float(line[k+l+m+n+o+p+q+r+s+10]+line[k+l+m+n+o+p+q+r+s+11]))
                else:
                    TEMP=int(float((line[k+l+m+n+o+p+q+r+s+9]+line[k+l+m+n+o+p+q+r+s+10]+line[k+l+m+n+o+p+q+r+s+11])))
                #print(TEMP)

            ###################### LIGTH
            for i in line[k+l+m+n+o+p+q+r+s+t+10:]:
                if(i!=","):
                    u=u+1
                else:
                    break
            if u==1:
                LIGTH=int(float((line[k+l+m+n+o+p+q+r+s+t+10])))
                #print(LIGTH)
            elif u==2:
                LIGTH=int(float((line[k+l+m+n+o+p+q+r+s+t+10]+line[k+l+m+n+o+p+q+r+s+t+11])))
                #print(LIGTH)
            elif u==3:
                LIGTH=int(float((line[k+l+m+n+o+p+q+r+s+t+10]+line[k+l+m+n+o+p+q+r+s+t+11]+line[k+l+m+n+o+p+q+r+s+t+12])))
                #print(LIGTH)
            elif u==4:
                LIGTH=int(float((line[k+l+m+n+o+p+q+r+s+t+10]+line[k+l+m+n+o+p+q+r+s+t+11]+line[k+l+m+n+o+p+q+r+s+t+12]+line[k+l+m+n+o+p+q+r+s+t+13])))
                #print(LIGTH)

            ###################### EARTH
            for i in line[k+l+m+n+o+p+q+r+s+t+u+11:]:
                if(i!=","):
                    v=v+1
                else:
                    break
            if v==1:
                EARTH=int(float((line[k+l+m+n+o+p+q+r+s+t+u+11])))
                #print(EARTH)
            elif v==2:
                EARTH=int(float((line[k+l+m+n+o+p+q+r+s+t+u+11]+line[k+l+m+n+o+p+q+r+s+t+u+12])))
                #print(EARTH)
            elif v==3:
                EARTH=int(float((line[k+l+m+n+o+p+q+r+s+t+u+11]+line[k+l+m+n+o+p+q+r+s+t+u+12]+line[k+l+m+n+o+p+q+r+s+t+u+13])))
               # print(EARTH)
            elif v==4:
                EARTH=int(float((line[k+l+m+n+o+p+q+r+s+t+u+11]+line[k+l+m+n+o+p+q+r+s+t+u+12]+line[k+l+m+n+o+p+q+r+s+t+u+13]+line[k+l+m+n+o+p+q+r+s+t+u+14])))
               #print(EARTH)
            ###################### BATTERY
            for i in line[k+l+m+n+o+p+q+r+s+t+u+v+12:]:
                if(i!=","):
                    w=w+1
                else:
                    break
            if w==1:
                BATTERY=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+12])))
                #print(EARTH)
            elif w==2:
                BATTERY=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+12]+line[k+l+m+n+o+p+q+r+s+t+u+v+13])))
                #print(EARTH)
            elif w==3:
                BATTERY=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+12]+line[k+l+m+n+o+p+q+r+s+t+u+v+13]+line[k+l+m+n+o+p+q+r+s+t+u+v+14])))
               # print(EARTH)
            elif w==4:
                BATTERY=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+12]+line[k+l+m+n+o+p+q+r+s+t+u+v+13]+line[k+l+m+n+o+p+q+r+s+t+u+v+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+15])))
                #print(BATTERY)

            if ID==15:
                ####################velocidad del viento
                for i in line[k+l+m+n+o+p+q+r+s+t+u+v+w+13:]:
                    if(i!=","):
                        x=x+1
                    else:
                        break
                if x==1:
                    VIENTO=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+13])))
                #print(EARTH)
                elif x==2:
                    VIENTO=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+13]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+14])))
                #print(EARTH)
                elif x==3:
                    VIENTO=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+13]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+15])))
               # print(EARTH)
                elif x==4:
                    VIENTO=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+13]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+16])))
                #print(BATTERY)
                elif x==5:
                    VIENTO=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+13]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+16]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+17])))
                #print(BATTERY)

                ########################direccion del viento
                for i in line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+14:]:
                    if(i!=","):
                        y=y+1
                    else:
                        break
                if y==1:
                    DIRECCION=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+14])))
                #print(EARTH)
                elif y==2:
                    DIRECCION=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+15])))
                #print(EARTH)
                elif y==3:
                    DIRECCION=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+16])))
                elif y==4:
                    DIRECCION=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+16]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+17])))
                #print(BATTERY)
                elif y==5:
                    DIRECCION=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+16]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+17]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+18])))
                #print(BATTERY)

                ####################LLUVIA
                for i in line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+15:]:
                    if(i!=","):
                        z=z+1
                    else:
                        break
                if z==1:
                    LLUVIA=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+15])))
                    #print(LLUVIA)
                elif z==2:
                    LLUVIA=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+16])))
                    #print(LLUVIA)
                elif z==3:
                    LLUVIA=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+16]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+17])))
               # print(EARTH)
                elif z==4:
                    LLUVIA=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+16]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+17]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+18])))
                #print(BATTERY)
                elif z==5:
                    LLUVIA=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+16]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+17]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+18]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+19])))
                #print(BATTERY)
                ####################rssi
                for i in line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+16:]:
                    if(i!=","):
                        za=za+1
                    else:
                        break
                for i in line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+17:]:
                    if(i!=","):
                        zb=zb+1
                    else:
                        break
                if zb==1:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+17])))
                    print(RSSI)
                elif zb==2:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+17]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+18])))
                    print(RSSI)
                elif zb==3:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+17]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+18]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+19])))
                    print(RSSI)
                elif zb==4:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+17]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+18]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+19]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+20])))
                    print(RSSI)
                elif zb==5:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+17]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+18]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+19]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+20]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+za+21])))
                    print(RSSI)

                
            else:
                ####################velocidad del viento
                for i in line[k+l+m+n+o+p+q+r+s+t+u+v+w+13:]:
                    if(i!=","):
                        za=za+1
                    else:
                        break
                for i in line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+14:]:
                    if(i!=","):
                        zb=zb+1
                    else:
                        break
                if zb==1:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+14])))
                    print(RSSI)
                elif zb==2:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+15])))
                    print(RSSI)
                elif zb==3:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+16])))
                    print(RSSI)
                elif zb==4:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+16]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+17])))
                    print(RSSI)
                elif zb==5:
                    RSSI=int(float((line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+14]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+15]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+16]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+17]+line[k+l+m+n+o+p+q+r+s+t+u+v+w+za+18])))
                #print(BATTERY)
            
                


            print(line)
            
            if ID==1:
                f = urllib2.urlopen(baseURL1 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==2:
                f = urllib2.urlopen(baseURL2 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==3:
                f = urllib2.urlopen(baseURL3 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==4:
                f = urllib2.urlopen(baseURL4 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==5:
                f = urllib2.urlopen(baseURL5 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==6:
                f = urllib2.urlopen(baseURL6 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==7:
                f = urllib2.urlopen(baseURL7 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==8:
                f = urllib2.urlopen(baseURL8 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==9:
                f = urllib2.urlopen(baseURL9 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==10:
                f = urllib2.urlopen(baseURL10 + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                f.read()
                f.close()
            elif ID==15:
                f = urllib2.urlopen(baseURL15a + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s&field7=%s" % (LIGTH, EARTH, PRES, HUM, TEMP,BATTERY,RSSI))
                print("ya")
                f.read()
                f.close()
                time.sleep(16)
                f = urllib2.urlopen(baseURL15b + "&field1=%s&field2=%s&field3=%s" % (VIENTO,DIRECCION,LLUVIA))
                print("ya")
                f.read()
                f.close()
                
            time.sleep(16)
        else:
            print("Archivo vacío o cadena con error")
     
                          
     infile.close()

     infile=open('/home/pi/Desktop/single_chan_pkt_fwd-master/datos.txt', 'w')
     infile.close()

     time.sleep(1)

 except(IndexError):
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
     
