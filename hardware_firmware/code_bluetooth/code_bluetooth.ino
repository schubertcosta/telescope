#include <SoftwareSerial.h>
#include <stdio.h>
#include <string.h>

#define bluetoothRX 10
#define bluetoothTX 11

SoftwareSerial bluetooth(bluetoothRX, bluetoothTX); // RX | TX

String deviceString = "";
bool deviceStringComplete = false;

void bluetoothEvent();

void getCoordinates(String inputData, float *coordinates);

void setup()
{ 
  Serial.begin(9600);
  Serial.println("Application Started");
}

void loop()
{  
  bluetooth.begin(9600);
  bluetooth.listen();
  bluetoothEvent();
  if (deviceString == "IS_ALIVE") {
    bluetooth.write("YES");
    Serial.println("Connected!");
  }else if(deviceString != ""){
    float coordinates[2];
    getCoordinates(deviceString, coordinates);

    // values ready to be used in coordinates[2]
  }
}

void getCoordinates(String inputData, float *coordinates){
  char delim[] = ",";
  char* cstr = new char[inputData.length() +1]; 
  strcpy(cstr, inputData.c_str()); 
  char *ptr = strtok(cstr, delim);

  coordinates[0] = atof(ptr);
  coordinates[1] = atof(strtok(NULL, delim));
}

void bluetoothEvent()
{
  deviceString.reserve(30);
  deviceString = "";
  while (bluetooth.available()) {
    char inchar = (char) bluetooth.read();
    if (inchar == '\r')
        bluetooth.end();
    else
      deviceString += inchar;
  }

  delay(300);
}
  
