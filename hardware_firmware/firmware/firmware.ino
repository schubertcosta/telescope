#include <AccelStepper.h>
#include <SoftwareSerial.h>
#include <stdio.h>
#include <string.h>

#define bluetoothRX 10
#define bluetoothTX 11
#define AZ_MOTOR_DIR 6
#define AZ_MOTOR_PIN 5
#define AL_MOTOR_DIR 7
#define AL_MOTOR_PIN 8
#define motorInterfaceType 1

SoftwareSerial bluetooth(bluetoothRX, bluetoothTX); // RX | TX

AccelStepper azMotor(motorInterfaceType, AZ_MOTOR_PIN, AZ_MOTOR_DIR);
AccelStepper alMotor(motorInterfaceType, AL_MOTOR_PIN, AL_MOTOR_DIR);

String deviceString = "";
bool deviceStringComplete = false;

void bluetoothEvent();

void getCoordinates(String inputData, float *coordinates);

void setup()
{ 
  Serial.begin(9600);
  Serial.println("Application Started");
  
  azMotor.setMaxSpeed(1000);
  azMotor.setAcceleration(50);
  azMotor.setSpeed(200);
  
  alMotor.setMaxSpeed(1000);
  alMotor.setAcceleration(50);
  alMotor.setSpeed(200);
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

    azMotor.moveTo(coordinates[0]);
    alMotor.moveTo(coordinates[1]);

    while(azMotor.distanceToGo() != 0)
        azMotor.run();
    while(alMotor.distanceToGo() != 0)
        alMotor.run();
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
  
