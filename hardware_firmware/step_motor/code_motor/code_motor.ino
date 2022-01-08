// Include the AccelStepper Library
#include <AccelStepper.h>

// Define pin connections
#define AZ_MOTOR_DIR 6
#define AZ_MOTOR_PIN 5

// Define motor interface type
#define motorInterfaceType 1

// Creates an instance
AccelStepper azMotor(motorInterfaceType, AZ_MOTOR_PIN, AZ_MOTOR_DIR);

float coordinates[2] = {200, 100};

void setup() {
  azMotor.setMaxSpeed(1000);
  azMotor.setAcceleration(50);
  azMotor.setSpeed(200);
  azMotor.moveTo(0);
}

void loop() {
  // Change direction once the motor reaches target position
  if (azMotor.distanceToGo() == 0) 
    azMotor.moveTo(-azMotor.currentPosition());

  // Move the motor one step
  azMotor.run();
}
