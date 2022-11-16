//WASHTAG as a project of Hackaton2022 NOI Techpark
//Challenge of LVH
//Microcontroller = ESP32 with WiFi and Bluetooth
//This code is reading the RFID sensordata, converting it and hosting a local website to publish the data for other devices.

#include <WiFi.h>
#include <WebServer.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 5  //slave select pin
#define RST_PIN 27  //reset select pin

//defining variables as a String
String byteString;
String oldbyteString;
String string1 = "";

int a=0;

const int refreshRate = 2000;   //clockspeed for the website to refresh the data

unsigned long milliseconds;

const char* ssid = "SSID";  // Enter your SSID here
const char* password = "PASSWORD";  //Enter your networks password here

WebServer server(80);    //Port number

MFRC522 mfrc522(SS_PIN, RST_PIN);    // instatiate a MFRC522 reader object.
MFRC522::MIFARE_Key key;             //create a MIFARE_Key struct named 'key', which will hold the card information

void setup() {
  Serial.begin(115200);         // Initialize serial communications with the PC
  delay(500);
  SPI.begin();               // Init SPI bus
  mfrc522.PCD_Init();        // Init MFRC522 card (in case you wonder what PCD means: proximity coupling device)
  Serial.println("Scan a MIFARE Classic card");

  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;//keyByte is defined in the "MIFARE_Key" 'struct' definition in the .h file of the library
  }

  //connect to your local wi-fi network
  Serial.println("Connecting to ");
  Serial.println(ssid);
  delay(500);
  WiFi.begin(ssid, password);

  //check wi-fi is connected to wi-fi network
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");    //loading dots...
  }
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  
  Serial.println(WiFi.localIP());

  server.on("/", handle_OnConnect);
  server.onNotFound(handle_NotFound);
  server.begin();
  Serial.println("HTTP server started");
}

byte readbackblock[18];   //This array is used for reading out a block. The MIFARE_Read method requires a buffer that is at least 18 bytes to hold the 16 bytes of a block.
byte Washtag[16];

//Code running in a permanent loop
void loop(){

  //Converting byte datatype to string for the website, only reacts to new values.
  //If there is more than one RFID Tag scanned during the refreshtime, the string will be added to the mainstring("byteString") and will get separatet with a "#"
  if (String((char *)Washtag) != string1){
    string1 = String((char *)Washtag);
    byteString = byteString + string1 + "#";
  }

  //Resets the mainstring variable ("byteString") displayed on the website
  if (millis() >= milliseconds + refreshRate){
    byteString = "0";
    milliseconds = millis();
  }
  
  server.handleClient();

  mfrc522.PCD_Init();

  // Look for new cards (in case you wonder what PICC means: proximity integrated circuit card)
  if ( ! mfrc522.PICC_IsNewCardPresent()) {   //if PICC_IsNewCardPresent returns 1, a new card has been found and we continue
    return;   //if it did not find a new card is returns a '0' and we return to the start of the loop
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {   //if PICC_ReadCardSerial returns 1, the "uid" struct (see MFRC522.h lines 238-45)) contains the ID of the read card.
    return;   //if it returns a '0' something went wrong and we return to the start of the loop
  }

  readBlock(block, readbackblock);    //read the block back

    //Serial.print("read block: ");
  for (int j=0 ; j<16 ; j++)    //print the block contents
  {
    Washtag[j] = readbackblock[j];
  }  

  //Serial.println("read block: ");
  for (int j=0 ; j<16 ; j++)    //print the block contents
  {
    Serial.write (Washtag[j]);    //Serial.write() transmits the ASCII numbers as human readable characters to serial monitor
  }
}

//handles connection
void handle_OnConnect(){
  server.send(200, "text/html", SendHTML()); 
}

//handles case: 404
void handle_NotFound(){
  server.send(404, "text/plain", "Not found");
}

//HTML website
String SendHTML(){
  String ptr = "<!DOCTYPE html> <html>\n";
  ptr +="<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
  ptr +="<title>ESP32 Hello World</title>\n";
  ptr +="<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
  ptr +="body{margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;}\n";
  ptr +="p {font-size: 24px;color: #444444;margin-bottom: 10px;}\n";
  ptr +="</style>\n";
  ptr +="</head>\n";
  ptr +="<body>\n";
  ptr +="<div id=\"webpage\">\n";
  ptr +="<table>\n";
  ptr +="<tr>\n";
  ptr +="<td>" + byteString +"</td>\n";
  ptr +="</tr>\n";
  ptr +="</table>\n";
  ptr +="<h1> WashTag </h1>\n";
  ptr +="</div>\n";
  ptr +="</body>\n";
  ptr +="</html>\n";
  return ptr;
}

//reads RFID chip
int readBlock(int blockNumber, byte arrayAddress[]){
  int largestModulo4Number=blockNumber/4*4;
  int trailerBlock=largestModulo4Number+3;    //determine trailer block for the sector

  //authentication of the desired block for access
  byte status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));

  if (status != MFRC522::STATUS_OK) {
    return 3;   //return "3" as error message
  }

  byte buffersize = 18;   //we need to define a variable with the read buffer size, since the MIFARE_Read method below needs a pointer to the variable that contains the size... 
  status = mfrc522.MIFARE_Read(blockNumber, arrayAddress, &buffersize);   //&buffersize is a pointer to the buffersize variable; MIFARE_Read requires a pointer instead of just a number
  if (status != MFRC522::STATUS_OK) {
    return 4;   //return "4" as error message
  }
}

//For further explaination please visit https://youtu.be/dQw4w9WgXcQ
