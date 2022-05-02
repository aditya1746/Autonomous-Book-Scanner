
#include <ros.h>
#include <Servo.h>
#include <std_msgs/String.h>

Servo pageTurner;
Servo pageLifter;

ros::NodeHandle nh;

int x;

void setup() {
 Serial.begin(57600);  //115200
 Serial.setTimeout(1);

 pageTurner.attach(3);
 pageLifter.attach(5);

 pageTurner.write(0);

 delay(5000);
}

void callback(const std_msgs::String& msg)
{

    /*for (pos = 0; pos <=180; pos += 1) { // goes from 180 degrees to 0 degrees
    pageLifter.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }

  for (pos = 180; pos >= someValue; pos -= 1) { // goes from 180 degrees to 0 degrees
    pageLifter.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }*/

  for(int n = 1;n<=5;n++)
  {
    digitalWrite(13,LOW);
    delay(5000);
    digitalWrite(13,HIGH);
    delay(500);
  }

  delay(15000);

  for (int pos = 0; pos <=180; pos += 1) { // goes from 180 degrees to 0 degrees
    pageTurner.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }

  delay(2000);

  for (int pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    pageTurner.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}

ros::Subscriber<std_msgs::String> sub("main_topic", &callback);

void loop() {
 
 nh.spinOnce();
}