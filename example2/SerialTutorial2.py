
import os 
from serial import Serial 
import time
from datetime import datetime 

nextCompassPoll = 0.0 ;

compassPollMsg = b'CMP:\n' 

serialDevDir='/dev/serial/by-id' 

if ( os.path.isdir(serialDevDir) ):
    serialDevices = os.listdir(serialDevDir) 

    if ( len(serialDevices) > 0 ):

        serialDevicePath = os.path.join(serialDevDir, serialDevices[0])

        serial = Serial(port=serialDevicePath, baudrate=19200, timeout=0.2) 

        while( True ):

            receivedMsg = serial.readline() 

            if ( (len(receivedMsg) >= 4) and (receivedMsg[3] == b':'[0])):

                tag = receivedMsg[0:3] 
                value = receivedMsg[4:]

                if ( tag == b'TIM' ):
                    hhmmTime= datetime.now().strftime('%H:%M') 
                    sendMsg = b'TIM:' + hhmmTime.encode('UTF-8')
                    serial.write(sendMsg + b'\n')

                elif ( tag == b'DAT' ):
                    hhmmTime= datetime.now().strftime('%d-%b-%Y') 
                    sendMsg = b'DAT:' + hhmmTime.encode('UTF-8')
                    serial.write(sendMsg + b'\n')

                elif ( tag == b'CMP' ):
                    print('Compass Bearing = ' + value.decode('UTF-8'))

            currentTime = time.time() 

            if ( currentTime > nextCompassPoll ):
                serial.write(compassPollMsg)
                nextCompassPoll = currentTime + 2.0
    else:

        print('No serial devices connected') 

else:

    print(serialDevDir + ' does not exist') 



