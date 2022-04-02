int blue=3;
int green=5;
int red=9;
int R=0, G=0, B=0;
int i=0;

void rgb(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(red, red_light_value);
  analogWrite(green, green_light_value);
  analogWrite(blue, blue_light_value);
}

void setup(){
  Serial.begin(9600);
  pinMode(red,OUTPUT);
  pinMode(green,OUTPUT);
  pinMode(blue,OUTPUT);
}

void loop(){  
  if (Serial.available()){
    R = Serial.parseInt();
    G = Serial.parseInt();
    B = Serial.parseInt();
  }
  rgb(255-R,255-G,255-B);
  /*else if (timer==0){
    i=0;
    for (int fadeValue = 0 ; fadeValue <= 255; fadeValue += 5) {
    // sets the value (range from 0 to 255):
    analogWrite(red, 255-fadeValue);
    // wait for 30 milliseconds to see the dimming effect
    delay(50);
  }
  // fade out from max to min in increments of 5 points:
  for (int fadeValue = 255 ; fadeValue >= 0; fadeValue -= 5) {
    // sets the value (range from 0 to 255):
    analogWrite(red, 255-fadeValue);
    // wait for 30 milliseconds to see the dimming effect
    delay(50);
  }
  }*/
    }
/*int T1[]={255,0,0,255,100,0,255};
  int T2[]={0,255,0,255,0,255,255};
  int T3[]={0,0,255,0,255,255,255};
  for (i=0;i<7;i++){
     analogWrite(red,255-T1[i]);
     analogWrite(green,255-T2[i]);
     analogWrite(blue,255-T3[i]);
     delay(1000);
       }*/
    
  /*analogWrite(red,0);
  analogWrite(green,255);
  analogWrite(blue,255);
  delay(1);*/
