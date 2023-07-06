#include<stdio.h>
#include<wiringPi.h>
#include<time.h>

#define PINS_SIZE 4

int main(){
	if(wiringPiSetup() == -1) 
		return -1; 
	
	int pins[PINS_SIZE] = {2, 3, 4, 5};
	time_t current_time;
	struct tm time_value;
	int current_seconds;
	
	for (int i=0; i < PINS_SIZE; i++) 
		pinMode(pins[i], OUTPUT); 
	
	while (1) {
		time(&current_time);
		time_value = *localtime(&current_time);
		current_seconds = time_value.tm_sec;

		for (int i=0; i < PINS_SIZE; i++)
			digitalWrite(pins[i], (current_seconds%16 >> i) & 0b1);

		delay(1000);
	}

	return 0;
}
