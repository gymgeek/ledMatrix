
#include <WS2812.h>

#define outputPin 7  
#define LEDCount 120  

WS2812 LED(LEDCount); 
cRGB valOn;
cRGB valOff;

int iLed;
void setup() {
 Serial.begin(9600);
 LED.setOutput(outputPin);
 LED.setColorOrderRGB(); 
 valOn.r = 55;
 valOn.g = 55;
 valOn.b = 55;

 valOff.r = 0;
 valOff.g = 0;
 valOff.b = 0;
 
 
}
int data[120];
void loop() {
  if(Serial.available()){      
      int recv = Serial.read();      
      switch(recv) {
      case 255:
        iLed = 0;
        Serial.println("------");
        break;
      case 10:
        Serial.println("++++++");
        syncLeds();
        break;
      case 48:
        data[iLed] = 0;
        Serial.println(String(iLed));
        iLed++;
        break;
      case 49:
        data[iLed] = 1;
        Serial.println(String(iLed));
        iLed++;
        break;
     }
     
     
  }
}

void syncLeds() {

  for(int i = 0; i < 120; i++) {
      if (data[i] == 1) {
        LED.set_crgb_at(i, valOn);
      } else {
         LED.set_crgb_at(i, valOff);
      }
    }
    LED.sync();
}

