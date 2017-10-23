/*******************************************************************************
 *
 * Copyright (c) 2015 Thomas Telkamp
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * http://www.eclipse.org/legal/epl-v10.html
 *
 *******************************************************************************/

#include <string>
#include <sstream>
#include <map>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>
#include <iostream>
#include <cstdlib>
#include <sys/time.h>
#include <cstring>
#include <errno.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <netdb.h>
#include <time.h>
#include <fstream>



using namespace std;

#include "base64.h"

#include <wiringPi.h>
#include <wiringPiSPI.h>

#include<netdb.h> //hostent
#include<arpa/inet.h>



typedef bool boolean;
typedef unsigned char byte;

static const int CHANNEL = 0;

byte currentMode = 0x81;

char message[256];
char b64[256];

bool sx1272 = true;
int maxMessages = 10;

byte modemstat;
byte receivedbytes;
byte receivedpackets;

struct sockaddr_in si_other;
int s, slen=sizeof(si_other);
struct ifreq ifr;

uint32_t cp_nb_rx_rcv;
uint32_t cp_nb_rx_ok;
uint32_t cp_nb_rx_bad;
uint32_t cp_nb_rx_nocrc;
uint32_t cp_up_pkt_fwd;

enum sf_t { SF7=7, SF8, SF9, SF10, SF11, SF12 };

enum {
	EU868_F1 = 868100000, // g1 SF7-12
	EU868_F2 = 868300000, // g1 SF7-12 FSK SF7/250
	EU868_F3 = 868500000, // g1 SF7-12
	EU868_F4 = 868850000, // g2 SF7-12
	EU868_F5 = 869050000, // g2 SF7-12
	EU868_F6 = 869525000, // g3 SF7-12
	EU868_J4 = 864100000, // g2 SF7-12 used during join
	EU868_J5 = 864300000, // g2 SF7-12 ditto
	EU868_J6 = 864500000, // g2 SF7-12 ditto
};
/*******************************************************************************
 *
 * Configure these values!
 *
 *******************************************************************************/

// SX1272 - Raspberry connections
int csPin   = 6;  // SX1272 nss  on Pi GPIO1 
int dio0Pin = 7;  // SX1272 dio0 on Pi GPIO17
int rstPin  = 0;  // SX1272 rst  on Pi GPIO0 

// Set spreading factor (SF7 - SF12)
sf_t sf = SF7;

// Set center frequency
uint32_t  freq = 915000000; // in Mhz! (868.1)


////ID LORA TRANSMISSOR

int ID=0;

////HUMITY
int HUMITY=0;
////ALTITUDE
int ALTITUDE=0;
////PRES
int PRES=0;
////TEMP
int TEMP=0;

int rssi=0;

/* Informal status fields */
static char description[64] = "Singe Channel Gateway [v0.1]";  /* used for free form description */

// define servers
// TODO: use host names and dns
#define DEFAULTSERVER "52.169.76.203"      // router.eu.thethings.network
//"52.169.76.203"
//"40.114.249.243"
//#define SERVER2 "192.168.1.10"      // local
#define DEFAULTPORT 1700                   // The port on which to send data

// #############################################
// #############################################
std::map<std::string, std::pair<std::string, int> > serverList;


#define REG_FIFO                    0x00
#define REG_FIFO_ADDR_PTR           0x0D
#define REG_FIFO_TX_BASE_AD         0x0E
#define REG_FIFO_RX_BASE_AD         0x0F
#define REG_RX_NB_BYTES             0x13
#define REG_OPMODE                  0x01
#define REG_FIFO_RX_CURRENT_ADDR    0x10
#define REG_IRQ_FLAGS               0x12
#define REG_DIO_MAPPING_1           0x40
#define REG_DIO_MAPPING_2           0x41
#define REG_MODEM_CONFIG            0x1D
#define REG_MODEM_CONFIG2           0x1E
#define REG_MODEM_CONFIG3           0x26
#define REG_MODEM_STAT              0x18
#define REG_SYMB_TIMEOUT_LSB  		0x1F
#define REG_PKT_SNR_VALUE			0x19
#define REG_PAYLOAD_LENGTH          0x22
#define REG_IRQ_FLAGS_MASK          0x11
#define REG_MAX_PAYLOAD_LENGTH 		0x23
#define REG_HOP_PERIOD              0x24
#define REG_SYNC_WORD				0x39
#define REG_VERSION	  				0x42
#define REG_SYNC_CONFIG				0x27

#define SX72_MODE_RX_CONTINUOS      0x85
#define SX72_MODE_RX_SINGLE         0x86
#define SX72_MODE_TX                0x83
#define SX72_MODE_SLEEP             0x80
#define SX72_MODE_STANDBY           0x81

#define PAYLOAD_LENGTH              0x40

// LOW NOISE AMPLIFIER
#define REG_LNA                     0x0C
#define LNA_MAX_GAIN                0x23
#define LNA_OFF_GAIN                0x00
#define LNA_LOW_GAIN		    	0x20

// CONF REG
#define REG1                        0x0A
#define REG2                        0x84

#define SX72_MC2_FSK                0x00
#define SX72_MC2_SF7                0x70
#define SX72_MC2_SF8                0x80
#define SX72_MC2_SF9                0x90
#define SX72_MC2_SF10               0xA0
#define SX72_MC2_SF11               0xB0
#define SX72_MC2_SF12               0xC0

#define SX72_MC1_LOW_DATA_RATE_OPTIMIZE  0x01 // mandated for SF11 and SF12

// FRF
#define        REG_FRF_MSB              0x06
#define        REG_FRF_MID              0x07
#define        REG_FRF_LSB              0x08

#define        FRF_MSB                  0xD9 // 868.1 Mhz
#define        FRF_MID                  0x06
#define        FRF_LSB                  0x66

#define BUFLEN 2048  //Max length of buffer

#define PROTOCOL_VERSION  1
#define PKT_PUSH_DATA 0
#define PKT_PUSH_ACK  1
#define PKT_PULL_DATA 2
#define PKT_PULL_RESP 3
#define PKT_PULL_ACK  4

#define TX_BUFF_SIZE  2048
#define STATUS_SIZE	  1024

ofstream archivo;
ifstream archivolist;


void enableCS()
{
    digitalWrite(csPin, LOW);
}

void selectreceiver()
{
    digitalWrite(csPin, LOW);
}

 void unselectreceiver()
{
    digitalWrite(csPin, HIGH);
}

void disableCS()
{
    digitalWrite(csPin, HIGH);
}



byte readRegister(byte addr)
{
    unsigned char spibuf[2];

    enableCS();
    spibuf[0] = addr & 0x7F;
    spibuf[1] = 0x00;
    if(wiringPiSPIDataRW(CHANNEL, spibuf, 2) < 0)
	fprintf (stderr, "readRegister failed: %s\n", strerror (errno));
    unselectreceiver();

    return spibuf[1];
}

void writeRegister(byte addr, byte value)
{
    unsigned char spibuf[2];

    spibuf[0] = addr | 0x80;
    spibuf[1] = value;
    enableCS();
    wiringPiSPIDataRW(CHANNEL, spibuf, 2);

    disableCS();
}

void createFile(int iden )
{
   time_t now=time(0);
   tm *ltm=localtime(&now);
   
   archivo.open("/home/pi/Desktop/single_chan_pkt_fwd-master/datos.txt",ios::app|ios::in|ios::out);
   archivo << 1900+ltm->tm_year <<"," << 1 + ltm->tm_mon <<"," <<ltm->tm_mday <<"," <<ltm->tm_hour <<"," << ltm->tm_min <<","<<ltm->tm_sec << "," << message << "," <<rssi << endl; 
   archivo.close();	
   
   std::ostringstream name;
   name<<"/home/pi/Desktop/single_chan_pkt_fwd-master/datos/datos"<<iden<<".txt";
   //const char* cstr = file.str();
   const std::string tmp = name.str();
   const char* cstr = tmp.c_str();
   printf("%s",cstr);
   archivo.open(cstr,ios::app);
   archivo << 1900+ltm->tm_year <<"," << 1 + ltm->tm_mon <<"," <<ltm->tm_mday <<"," <<ltm->tm_hour <<":" << ltm->tm_min <<":"<<ltm->tm_sec << " Mensaje: " << message <<","<<rssi <<endl;  
   archivo.close();
   
}

boolean receivePkt(char *payload)
{

    // clear rxDone
    writeRegister(REG_IRQ_FLAGS, 0x40);

    int irqflags = readRegister(REG_IRQ_FLAGS);
    modemstat = readRegister(REG_MODEM_STAT);
    

    //  payload crc: 0x20
    if((irqflags & 0x20) == 0x20)
    {
        printf("CRC error\n");
        writeRegister(REG_IRQ_FLAGS, 0x20);
        return false;
    } else {

        byte currentAddr = readRegister(REG_FIFO_RX_CURRENT_ADDR);
        byte receivedCount = readRegister(REG_RX_NB_BYTES);
        
        receivedbytes = receivedCount;

        writeRegister(REG_FIFO_ADDR_PTR, currentAddr);

        for(int i = 0; i < receivedCount; i++)
        {
            payload[i] = (char)readRegister(REG_FIFO);
        }
    }
    if((int)receivedbytes>0)
    {return true;}
    else{return false;}
}

void SetupLoRa()
{
    printf("CS   : %i.\n",csPin);
    printf("DIO0 : %i.\n",dio0Pin);
    printf("RST  : %i.\n",rstPin);
    printf("Startup.\n");
    digitalWrite(rstPin, HIGH);
    delay(100);
    digitalWrite(rstPin, LOW);
    delay(100);

    printf("Reset.\n");

    byte version = readRegister(REG_VERSION);

    if (version == 0x22) {
        // sx1272
        printf("SX1272 detected, starting.\n");
        sx1272 = true;
    } else {
        // sx1276?
        digitalWrite(rstPin, LOW);
        delay(100);
        digitalWrite(rstPin, HIGH);
        delay(100);
        version = readRegister(REG_VERSION);
        if (version == 0x12) {
            // sx1276
            printf("SX1276 detected, starting.\n");
            sx1272 = false;
        } else {
            printf("Unrecognized transceiver.: %x\n", version);
            //printf("Version: 0x%x\n",version);
            exit(1);
        }
    }

    writeRegister(REG_OPMODE, SX72_MODE_SLEEP);

    // set frequency
    uint64_t frf = ((uint64_t)freq << 19) / 32000000;
    writeRegister(REG_FRF_MSB, (uint8_t)(frf>>16) );
    writeRegister(REG_FRF_MID, (uint8_t)(frf>> 8) );
    writeRegister(REG_FRF_LSB, (uint8_t)(frf>> 0) );

   // writeRegister(REG_SYNC_WORD, 0x34); // LoRaWAN public sync word

    if (sx1272) {
        if (sf == SF11 || sf == SF12) {
            writeRegister(REG_MODEM_CONFIG,0x0B);
        } else {
            writeRegister(REG_MODEM_CONFIG,0x0A);
        }
        
        writeRegister(REG_MODEM_CONFIG2,(sf<<4) | 0x04);
    } 
    
    else {
        if (sf == SF11 || sf == SF12) {
            writeRegister(REG_MODEM_CONFIG3,0x0C);
        } else {
            writeRegister(REG_MODEM_CONFIG3,0x04);
        }
        
    /////////////////////////////////////////////////////////////// ESTE REGISTRO CONFIGURA Bw(ANCHO DE BANDA) Y CODING RATE  
     
        //writeRegister(REG_MODEM_CONFIG,0x02);//00000010 ------> 1001=7.8kHz   001=4/5 CodingRate
        //writeRegister(REG_MODEM_CONFIG,0x12);//00010010 ------> 1001=10.4kHz   001=4/5 CodingRate
        //writeRegister(REG_MODEM_CONFIG,0x22);//00100010 ------> 1001=15.6kHz   001=4/5 CodingRate
        //writeRegister(REG_MODEM_CONFIG,0x32);//00110010 ------> 1001=20.8kHz   001=4/5 CodingRate
        //writeRegister(REG_MODEM_CONFIG,0x42);//01000010 ------> 1001=31.25kHz   001=4/5 CodingRate
        //writeRegister(REG_MODEM_CONFIG,0x52);//01010010 ------> 1001=41.7kHz   001=4/5 CodingRate
        //writeRegister(REG_MODEM_CONFIG,0x62);//01100010 ------> 1001=62.5kHz   001=4/5 CodingRate
        //writeRegister(REG_MODEM_CONFIG,0x72);//01110010 ------> 1001=125kHz   001=4/5 CodingRate
        //writeRegister(REG_MODEM_CONFIG,0x82);//10000010 ------> 1001=250kHz   001=4/5 CodingRate
        writeRegister(REG_MODEM_CONFIG,0x92);//10010010 ------> 1001=500kHz   001=4/5 CodingRate
        
        
        
    /////////////////////////////////////////////////////////////// ESTE REGISTRO CONFIGURA EL SPRENDING FACTOR
        writeRegister(REG_MODEM_CONFIG2,(12<<4) | 0x04);
    }

    if (sf == SF10 || sf == SF11 || sf == SF12) {
        writeRegister(REG_SYMB_TIMEOUT_LSB,0x05);
    } else {
        writeRegister(REG_SYMB_TIMEOUT_LSB,0x08);
    }
    writeRegister(REG_MAX_PAYLOAD_LENGTH,0x80);
    writeRegister(REG_PAYLOAD_LENGTH,PAYLOAD_LENGTH);
    writeRegister(REG_HOP_PERIOD,0xFF);
    writeRegister(REG_FIFO_ADDR_PTR, readRegister(REG_FIFO_RX_BASE_AD));

    // Set Continous Receive Mode
    writeRegister(REG_LNA, LNA_MAX_GAIN);  // max lna gain
   
   
    writeRegister(REG_OPMODE, SX72_MODE_RX_CONTINUOS);

}


void receivepacket() {

    long int SNR;
    int rssicorr;

   if(digitalRead(dio0Pin) == 1)
   {
        if(receivePkt(message)) {
            
            byte value = readRegister(REG_PKT_SNR_VALUE);
            if( value & 0x80 ) // The SNR sign bit is 1
            {
                // Invert and divide by 4
                value = ( ( ~value + 1 ) & 0xFF ) >> 2;
                SNR = -value;
            }
            else
            {
                // Divide by 4
                SNR = ( value & 0xFF ) >> 2;
            }
            
            if (sx1272) {
                rssicorr = 139;
            } else {
                rssicorr = 157;
            }
	    rssi=-1*(readRegister(0x1A)-rssicorr);
            printf("Packet RSSI: %d, ",readRegister(0x1A)-rssicorr);
            printf("RSSI: %d, ",readRegister(0x1B)-rssicorr);
            printf("SNR: %li, ",SNR);
            printf("Length: %i, ",(int)receivedbytes);
            
            printf("\n");

        
          
            printf("MENSAJE RECIBIDO :\n");
            printf("%s ",message);
            printf("\n");
            
            
            
            
            ///////////IDENTIFICAR ID
            int k=0;
			while(message[k] != ',' &&  k<=(int)receivedbytes ) {
				k++;
				}
				//printf("K= %d :\n", k);
		   if(k==1){
			   char a=message[0];
				ID= a -'0';
			   }
		   else if(k==2){
			   char a=message[0];
			   char b=message[1];
			    
				int ID1= (a -'0')*10;
				int ID2= (b -'0');
				ID=ID1+ID2;
			   }	
			else if(k==3){
			   char a=message[0];
			   char b=message[1];
			   char c=message[2];
				int ID1= (a -'0')*100;
				int ID2= (b -'0')*10;
				int ID3= (c -'0');
				ID=ID1+ID2+ID3;
			   }	   
			else if(k==4){
			   char a=message[0];
			   char b=message[1];
			   char c=message[2];
			   char d=message[3];
				int ID1= (a -'0')*1000;
				int ID2= (b -'0')*100;
				int ID3= (c -'0')*10;
				int ID4= (d -'0');
				ID=ID1+ID2+ID3+ID4;
			   }	   
			else if(k==5){
			   char a=message[0];
			   char b=message[1];
			   char c=message[2];
			   char d=message[3];
			   char e=message[4];
				int ID1= (a -'0')*10000;
				int ID2= (b -'0')*1000;
				int ID3= (c -'0')*100;
				int ID4= (d -'0')*10;
				int ID5= (e -'0');
				ID=ID1+ID2+ID3+ID4+ID5;
			   }	   
			printf("ID TRANSMISOR :\n");
            printf("%d ",ID);
            printf("\n");
            string idString = static_cast<ostringstream*>( &(ostringstream() << ID) )->str();
            string line="holo";
            archivolist.open("/home/pi/Desktop/single_chan_pkt_fwd-master/agrolist.txt",ios::app|ios::in|ios::out);
			if (archivolist.is_open()){
				  while(line!="END"){
					  cout << "Reading\n";
					  getline(archivolist,line); 
					  cout << line << endl;
					  
					  if(idString==line){
						  createFile(ID);
						  break;
						  }
					 
				  }
				   archivolist.close();
				  }
            
         
           
        } 
    } // dio0=1
  
}


int main(int argc, char *argv[] ) {
	
    
    std::stringstream desc;
    desc << "Single channel, ";
    desc << (double)freq/1000000 << "MHz, ";
    desc << "SF" << sf;
    strncpy(description, desc.str().c_str(), 64);
    
    wiringPiSetup () ;
    pinMode(csPin, OUTPUT);
    pinMode(dio0Pin, INPUT);
    pinMode(rstPin, OUTPUT);

   
    if(wiringPiSPISetup(CHANNEL, 500000) < 0)
		fprintf (stderr, "SPI Setup failed: %s\n", strerror (errno));
    
    SetupLoRa();

   

    printf("Listening at SF%i on %.6lf Mhz.\n", sf,(double)freq/1000000);

    //std::map<std::string, std::pair<std::string, int> >::iterator iter;
   
    printf("------------------\n");

    while(1) {
		
	
			receivepacket();
	
        for(int k=0;k<=(int)receivedbytes;k++)
        {
			message[k]=0;
			}
        delay(1);
    }

    return (0);

}

