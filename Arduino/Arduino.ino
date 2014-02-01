/*
KHK LightShow Hardware Control v1.0
Author: Dan Boehm
Credit: Samuel Hurley
Copyright: 2011

This is the software responsible for providing the switching control
to exactly one switching module for the KHK LightShow system.
The software is designed to work with two boxes running concurrently,
with each box being controlled by its own Arduino Diecimila.

The current implementation of KHK LightShow consists of up to 24
independant lighting circuits on a bang-bang (on-off) implementation.
These are binarily controlled using the digital-IO pins.
0 is off, & 1 is on.

This software recieves serial communication, and decodes that data
in order to determine which of 12 light circuits it should switch.
*/

//Constants
#define ZERO_PIN 2
#define NUM_PINS 12

void setup() {
  Serial.begin(9600);
  Serial.println("hello world");
  for(int i = ZERO_PIN; i < ZERO_PIN + NUM_PINS;  i++) {
    //Serial.println(i);
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
}

void loop() {
  //digitalWrite(13, HIGH);
  if(Serial.available() > 0) {
    byte startByte = Serial.read();
    //digitalWrite(2, HIGH);
    //Serial.print(startByte, DEC);
    //Serial.println(' ');
    
    if(startByte == 255) {
      boolean takeCmd = true;
      do {
        if(Serial.available() >= 2) {
          byte id = Serial.read();
          byte state = Serial.read();
          //Serial.print(id, DEC);
          //Serial.print(' ');
          //Serial.println(state, DEC);
          
          if(id < NUM_PINS & id >= 0) {
            int pin = id + ZERO_PIN;
            
            if(state == 0) {
              Serial.println("LOW");
              digitalWrite(pin, LOW);
            }
            else {
              Serial.println("HIGH");
              digitalWrite(pin, HIGH);
            }
          }
          
          takeCmd = false;
        }
      } while(takeCmd);
    }
  }
}
