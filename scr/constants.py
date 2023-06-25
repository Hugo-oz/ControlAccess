#Commands for comunication between microcontroller and python
READ_ERROR = '0'
ACTION_IN_DOOR = '1'
ACTION_OUT_DOOR = '2'
COMMAND_IN_DOOR = '3'
COMMAND_OUT_DOOR = '4'
TEST_COMMAND = '9'

#Serial communication settings. Use the same Baud Rate as your microcontroller
PORT = "COM"
BAUD_RATE = 9600

#Server settings. IMPORTANT: avoid spaces and tabs.
SERVER_NAME = '' #Use your own server name
DATA_BASE = '' #Use your own database name

#Select the camera to use in each door
IN_CAMERA = 0
OUT_CAMERA = 1

#Path to save the image taken
IMAGE_PATH = "image.png"

#Tesseract folder path
TESSERACT_PATH = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'