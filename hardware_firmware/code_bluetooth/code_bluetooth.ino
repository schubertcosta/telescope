#include <SoftwareSerial.h>
#include <stdio.h>
#include <string.h>
SoftwareSerial EEBlue(10, 11); // RX | TX
void setup()
{ 
  Serial.begin(9600);
  EEBlue.begin(9600);
  Serial.println("Application Started. \n\n"); 
}

//function to convert string to byte array
byte[] string2ByteArray(bvte* input, byte[] output)
{
    int loop;
    int i;    
    byte[] output;
    loop = 0;
    i = 0;    
    while(input[loop] != '\0')
    {
        output[i++] = input[loop++];
    }
    return output;
}
 
void loop()
{
 String data_received;
 char* data_received_byte[100];

  if (EEBlue.available()){
    data_received = EEBlue.readString();
    data_received_byte = string2ByteArray(data_received, data_received_byte);
    if(data_received == "IS_ALIVE")
       EEBlue.write("YES");
    if(Serial.available() > 0)
      Serial.write(data_received_byte);
    //data_received_byte = '\0'
  }
    //Serial.write(EEBlue.read());
 
  // Feed all data from termial to bluetooth
  
}
