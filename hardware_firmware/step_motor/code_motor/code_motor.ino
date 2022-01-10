// Include the AccelStepper Library
#include <AccelStepper.h>

// Define pin connections
#define AZ_MOTOR_DIR 6
#define AZ_MOTOR_PIN 5
#define AL_MOTOR_DIR 7
#define AL_MOTOR_PIN 8

// Define motor interface type
#define motorInterfaceType 1

// Creates an instance
AccelStepper azMotor(motorInterfaceType, AZ_MOTOR_PIN, AZ_MOTOR_DIR);
AccelStepper alMotor(motorInterfaceType, AL_MOTOR_PIN, AL_MOTOR_DIR);

//float coordinates[2] = {200, 100};

void setup() {
  azMotor.setMaxSpeed(1000);
  azMotor.setAcceleration(6400);
  azMotor.setSpeed(200);
  azMotor.moveTo(6400);
  
  alMotor.setMaxSpeed(1000);
  alMotor.setAcceleration(6400);
  alMotor.setSpeed(200);
  alMotor.moveTo(6400);
}

void loop() {
  // Change direction once the motor reaches target position
  if (azMotor.distanceToGo() == 0) 
    azMotor.moveTo(-azMotor.currentPosition());

   
  if (alMotor.distanceToGo() == 0) 
    alMotor.moveTo(-alMotor.currentPosition());

  // Move the motor one step
  alMotor.run();
  azMotor.run();
}
