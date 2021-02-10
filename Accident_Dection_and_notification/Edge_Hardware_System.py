import RPi.GPIO as GPIO
import time
import serial
import thread
import urllib2
import os


from twilio import TwilioRestException     #Twilio API returns 400/500 HTTP response(invalid number, cant deliver sms to that number) ,twiliopython library will throw a TwilioRestException.
from twilio.rest import TwilioRestClient   #TwilioRestClient constructor accepts Twilio credentials (SID and Token)
import email
import email.utils


import smtplib
from email.MIMEMultipart import MIMEMultipart #is a class for mixed content types : msg.attach
from email.MIMEText import MIMEText  #is a class for content major type text
from email.MIMEBase import MIMEBase  #is a class used to add content type header and mime version
from email import encoders #used to encode the payloads like base64, base7 etc.


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38,1,pull_up_down=GPIO.PUD_UP)  #For alcohol
GPIO.setup(36,1,pull_up_down=GPIO.PUD_UP) #for interfacing water sensor

GPIO.setup(31,1,pull_up_down=GPIO.PUD_UP) #Horn 
GPIO.setup(33,1,pull_up_down=GPIO.PUD_UP) #Brake
GPIO.setup(35,1,pull_up_down=GPIO.PUD_UP)#right indicator
GPIO.setup(37,1,pull_up_down=GPIO.PUD_UP)#left indicator
GPIO.setup(32,1,pull_up_down=GPIO.PUD_UP)#piezo sensor

GPIO.setup(8,0)   #right indicator output
GPIO.setup(10,0) # left indicator output
GPIO.setup(40,0) # buzzer output

picser=serial.Serial('/dev/ttyUSB1',baudrate=9600,timeout=1) # object for serial communication with Pic
gpsser=serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=1) # object for serial communication with GPS TXR

data='#0$0' # variables initialized
lat='0'
lon='0'
temp='0'
rpm='0'
tim='0'
RI='0'
LI='0'
al='0'
b='0'
h='0'
m='0'
TS='0'
ST='0'


file=open("/home/pi/Desktop/bb.txt","w") # txt file created to write the dats on raspberry


def txn(idn,val): # upload to server - Function for transmission( server id of AWS '5622692', updated value in yy)
    try:
        request = urllib2.Request("https://aws.amazon.com/marketplace/pp/BatchIQ-Apache-NiFi-provided-by-BatchIQ-Profession/B01KZWVRCM?id=%d&value=%s"%(idn,val), headers={"Accept" : "text/html","User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "http://thewebsite.com",
            "Connection": "keep-alive"})    #<urllib2.Request instance at "hex code">
        contents = urllib2.urlopen(request).read() #OK$DATA : 5622692,yy
    except:
        print ''



def mail(to,sub):# function for mailing -mail( TO mail-id, subject)
    try:# try and except method adopted for mailing , even net connection not there also no error will come
        fromaddr = "2018ab04032wilpbits@gmail.com"
        toaddr = to
         
        msg = MIMEMultipart()
         
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = sub
         
        body = "HELP\n"+'Latitude='+lat+', Longitude='+lon+'\nDate & Time='+tim
         
        msg.attach(MIMEText(body, 'plain'))
         
        filename = "Image"
        attachment = open("/home/pi/Desktop/image.jpg", "rb")
         
        part = MIMEBase('application', 'octet-stream') #Content-Type: application/octet-stream MIME-Version: 1.0

        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
        msg.attach(part)
         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "Gmail Password here")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print 'Mail Sent'
    except:
        print 'Mailing Failed'

def mob(msg):
    account_sid = "AC4b0a0501ad51fbdeaf0029650efa872e" #My Account SID from www.twilio.com/console
    auth_token  = "Twilio Authentication Token here"  #My Auth Token from www.twilio.com/console

    client = TwilioRestClient(account_sid, auth_token) #<twilio.rest.client.TwilioRestClient object at "hex address">
    
    try:
    	    message = client.messages.create(body=msg,
    	    to="+919947099911",    # Replace with your phone number
    	    from_="+18329560543") # Replace with your Twilio number
    	    print 'sent'
    except:
    	    print 'msg failed'
        

def gps(threadName, delay):
    global lat
    global lon
    while(1):
        msg=gpsser.readline()       #to receive datas
        if 'GPRMC' in msg: # lat and long datas will be after "GPRMC" in the collected data from GPS
            lat=str(msg[20:28]) # string position from 22 to 28 will be latitude
            lon=str(msg[32:41]) # longitude
            print 'Location of Vehicle : Latitude='+lat,',Longitude='+lon
       
        time.sleep(delay)


def pic(threadName, delay):   #function for data collecting from pic
    global data
    global rpm
    global temp
    while(1):
        try:
            data=picser.readline()
    
            data=str(data)
    
            l=len(data)
            
            temp=str(data[data.index('#')+1:data.index('$')]) # Data format send from pic is 'hashxx$xxx'
            
            rpm=data[data.index('$')+1:l]

            print '\nVehicle Speed in rpm='+rpm
            print 'Engine Temperature='+temp
            
        except:
            print 'Waiting'
        
        time.sleep(delay)

        

def status(threadName, delay):
    global tim
    global RI
    global LI
    global al
    global h
    global b
    global m
    global TS
    global ST
    while(1):
        tim=str(time.ctime()) #system date and time   
        if(GPIO.input(35)==0):
            GPIO.output(8,1)
            print 'Right Indicator ON'
            RI='\nRight Indicator ON'
            RIS='RI ON,'
        else:
            GPIO.output(8,0)
            RI=''
            RIS='RIOFF,'
            
        if(GPIO.input(37)==0):
            GPIO.output(10,1)
            print 'Left Indicator ON'
            LI='\nLeft Indicator ON'
            LIS='LI ON|'
        else:
            GPIO.output(10,0)
            LI=''
            LIS='LIOFF|'

        if(GPIO.input(38)==0):
            print 'Alcohol Detected'
            al='\nAlcohol Detected'
            als='AD'
        else:
            als='AnD'
            al=''

        if(GPIO.input(31)==0):
            print 'Horn Pressed'
            h='\nHorn Pressed'
            HS='HP|'
            GPIO.output(40,1)
        else:
            GPIO.output(40,0)
            h=''
            HS='HnP|'
        if(GPIO.input(33)==0):
            print 'Brake Pressed'
            b='\nBrake Pressed'
            BS='BP|'
        else:
            b=''
            BS='BnP|'

            
        file=open("/home/pi/Desktop/bb.txt","w")
        file.write(" ")# write with blank data
        file.close()
        m='\n Here Is The Black Box Edge System Data, Saved During Accident\n '+tim+'\n Latitude='+lat+'\n Longitude='+lon+h+b+RI+LI+al+'\n Speed='+rpm+'\n Temperature='+temp
        file=open("/home/pi/Desktop/bb.txt","w")
        file.write(m)
        file.close()
        TS=tim[0:3]+tim[4:7]+tim[11:19]+' 2021|VehicleNo.:2018AB04032|'# collected date and time
        ST=RIS+LIS+HS+BS+als+'|Temp='+temp+'|RPM='+rpm+'|Lat='+lat+'|Lon='+lon # data collected as status of vehicle
        if(GPIO.input(36)==0):
            print 'Accident (Plunged into Water / Nearest River)'
            acc='Accident\n'+'Plunged into water\n'+'Location of the Vehicle : Latitude='+lat+'\nLongitude='+lon
            mob(acc)# calling function mob(msg) for sending message to mobile
            os.system("sudo fswebcam -r 320x240 /home/pi/Desktop/image.jpg") # calling command prompt and executing command to capture the image thru usb cam
            mail("2018ab04032wilpbits@gmail.com","Accident Detected") #calling function mail( TO mail id, Subject-line)
        time.sleep(delay)

def upload(threadName, delay):#continous upload to server
    
    while(1):
        yy=TS+ST
        print yy
        txn(5622692,yy)

        time.sleep(delay)
    




def accident(channel):
    if(GPIO.input(32)==0):
        print 'accident'
        GPIO.output(40,1)
        os.system("sudo fswebcam -r 320x240 /home/pi/Desktop/image.jpg")
        acc='Accident\n'+'Latitude='+lat+'\nLongitude='+lon
        mob(acc)
        mail("2018ab04032wilpbits@gmail.com","Accident Detected")
        GPIO.output(40,0)
    time.sleep(1)


    

GPIO.add_event_detect(32,GPIO.FALLING,callback=accident,bouncetime=300)# interrupt for sensing piezo, will call funcion accident
mob('Vehicle Sensor Edge Hardware prototype is ON')

try:
   thread.start_new_thread(gps, ("Thread-1", 1, ) )   #This thread return its idenfier, executes the function gps with tuple of argument lists. when function returns, thread silentlty exits.
   thread.start_new_thread(upload, ("Thread-1", 1, ) )
   thread.start_new_thread(pic, ("Thread-1", 1, ) )
   thread.start_new_thread(status, ("Thread-1", .5, ) )


except:
   print "Error: unable to start thread"

while 1:
   pass


 

