
#include <WS2812.h>

#define outputPin 7  
#define LEDCount 120  

WS2812 LED(LEDCount); 
cRGB value;

byte incomingData[LEDCount*3];

void setup() {
 Serial.begin(9600);
 LED.setOutput(outputPin);
 LED.setColorOrderRGB(); 
 for(int i = 0; i < LEDCount*3; i++) {
  incomingData[i] = 0;
 }
 
}

void loop() {
  if(Serial.available()){  
 
    int i = 0;
    while(true){
      incomingData[i] = Serial.read();
      
       if(!Serial.available()){
        delay(9);
        if(!Serial.available()){break;}}
      i++;  
      if(i >=LEDCount*3) {
        i = 0;  
      }
    }
    for(int a = 0; a < LEDCount; a++){
      value.r = incomingData[(a*3)+1];
      value.g = incomingData[(a*3)+0];
      value.b = incomingData[(a*3)+2];
      //Serial.println(String(a)+":"+String(value.r)+" "+String(value.g)+" "+String(value.b));
      LED.set_crgb_at(a, value);
    }
    LED.sync();
  }
}
