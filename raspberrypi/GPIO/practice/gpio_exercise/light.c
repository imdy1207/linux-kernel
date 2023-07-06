#include<stdio.h>
#include<wiringPi.h>
#define PINS_SIZE 2


int main(){

	if(wiringPiSetup() == -1) 
		return -1; 
	
	int pins[2] = {2, 10};
	
	for (int i=0; i < PINS_SIZE; i++) {
		pinMode(pins[i], OUTPUT); 
	}

	for(;;) 
	{
		
		for (int i=0; i < PINS_SIZE; i++) {
			if (i%2 == 0) digitalWrite(pins[i], 0);
			else digitalWrite(pins[i], 1);
		}
		delay(1000);


		for (int i=0; i < PINS_SIZE; i++) {
			if (i%2 == 1) digitalWrite(pins[i], 0);
			else digitalWrite(pins[i], 1);
		}
		delay(1000); 
	}

	return 0;
}
