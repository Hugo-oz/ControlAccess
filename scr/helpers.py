import constants as const
import serial
import pytesseract
import cv2
import pyodbc
from datetime import datetime


#Set tesseract folder and serial communication
pytesseract.pytesseract.tesseract_cmd = const.TESSERACT_PATH
Serial = serial.Serial(const.PORT, const.BAUD_RATE)
Serial.flush()

#Capture an image and save it
def captureImage(camID):
    #Star video capture with the specified camID
    cam = cv2.VideoCapture(camID, cv2.CAP_DSHOW)

    #Image resolution: 1920x1080
    cam.set(3, 1920)
    cam.set(4, 1080)

    #Capture frame and save it in the specified path and name
    ifRead, frame = cam.read()
    if ifRead == True:
        cv2.imwrite(const.IMAGE_PATH, frame)
        print("Photo taken correctly")
    else:
        print("Camera error")
    cam.release()

#Open the image and extract the text
def extractText(imagePath):
    image = cv2.imread(imagePath)
    text = pytesseract.image_to_string(image)
    return text

#Find the user in the data base by register and return the success status of this search
def findSqlUser(register, action):
    try:
        searchStatus = False
        #Strt cnection with the database
        connection=pyodbc.connect("DRIVER={SQL Server};SERVER='{0}';DATABASE='{1}';".format(const.SERVER_NAME, const.DATA_BASE))
        cursor=connection.cursor()
        print ("Connected to Data Base")

        #Extract all the rows from UserInfo table
        cursor.execute("SELECT * FROM UserInfo")
        rows=cursor.fetchall()
        for row in rows:
            #Search in the database if there the register user
            if row[1] == register:
                #If the user already In or Out, return false status
                if row[4] == action: 
                    print("Credential already validated")
                    searchStatus = False
                else:
                    #Show the data from the found user
                    print("User found: {}".format(row))

                    #Uptdate the status of the user
                    cursor.execute("UPDATE UserInfo SET Status='{0}' WHERE RegisterCURP='{1}'".format(action, register))
                    connection.commit()

                    #Take the actual time and register a new access in the UserAccess table
                    current_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                    cursor.execute("insert into UserAccess(Date, UserName, UserType, Action) values ('{0}','{1}', '{2}', '{3}')".format(current_time, row[0], row[3], action))
                    connection.commit()
                    searchStatus = True
                    break
            else:
                print("User not found")
    except Exception as ex:
        print (ex)
    finally:
        connection.close()
        print("Connection closed")
        return searchStatus

#Identify the card type and return the register
def identifyCardType(rawText):
    #Keyword in credential is used in order to identify the card type
    if rawText.find("ESTUDIANTE") > 0:
        print("Card type: Student")
        index = rawText.find("Registro")
        if index > 0:
            #Find the keyword of the register and then return the register avoiding spaces, newlines and tabs.
            register = rawText[index+9:index+18].strip(' \n\t')
            print(register)
            return register
    elif rawText.find("ELECTORAL") > 0:
        print("Card type: Visitant")
        index = rawText.find("CLAVE DE ELECTOR")
        if index > 0:
            #Find the keyword of the register and then return the register avoiding spaces, newlines and tabs.
            register = rawText[index+15:index+33].strip(' \n\t')
            print(register)
            return register
    else:
        print("Read error")

#Main function
def ControlAccess():
    #Loop reading the command from microcontroller
    while True:
        command = Serial.readline().decode('ascii').strip()

        if(command == const.COMMAND_IN_DOOR):
            print("Capturing data")

            #Capture the image from the selected camera
            captureImage(const.IN_CAMERA)

            #Extract text from the image
            rawText = str(extractText(const.IMAGE_PATH))

            #Identify the card type and get the register
            register = identifyCardType(rawText)

            #Gets the status of the search and send the command to the microcontroller
            searchStatus = findSqlUser(register, "In")
            if searchStatus:
                Serial.write(b'1')
            else:
                Serial.write(b'0')

        if(command == const.COMMAND_OUT_DOOR):
            print("Capturing data")

            #Capture the image from the selected camera
            captureImage(const.OUT_CAMERA)

            #Extract text from the image
            rawText = str(extractText(const.IMAGE_PATH))

            #Identify the card type and get the register
            register = identifyCardType(rawText)

            #Gets the status of the search and send the command to the microcontroller
            searchStatus = findSqlUser(register, "Out")
            if searchStatus:
                Serial.write(b'2')
            else:
                Serial.write(b'0')

        if(command == const.READ_ERROR):
            Serial.write(b'0')