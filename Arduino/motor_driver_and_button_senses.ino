

#define AIN1 2   //controls direction of the motor with AIN2
#define AIN2 4   //if both are low: SHORT BREAK if both are high: STOP
#define PWMA 3   //control the speed of the motor

#define PRESSED LOW //change to HIGH if you use a pulldown resistor, this is LOW for pull-up.
#define BUTTONSTATEUNCHANGED 0
#define BUTTONDOWN 2
#define BUTTONUP 1
//buttonState HIGH LOW
#define debounceTime 50
const int bPin = 7; //this is the button pin, it uses a pull up resistor so default is +5V

int registeredState = !PRESSED; //the button is registered as HIGH
unsigned long lastChange = 0; //time of the last change from up to down or down to up in the button
unsigned long timeInThisState = 0; //how long have we been in the up or down state of the button
unsigned long durationInPreviousState = 0; //how long was it in the state we just left
//for example, if the button was pressed for 5s, and then let go (right now!), the values will be:
//lastChange = (currentTime) since start of the arduino code
//timeInThisState will be 0 (ms) - because we just changed
//durationInPreviousState will be 5000 (ms) because it was PRESSED for 5s.
//registeredState will be !PRESSED (which is HIGH voltage)


//if you want to reset the timer and time of the lastChange in state
//this is good for actions you want to be repeated in intervals
void resetTimeInThisState() {
  lastChange = millis(); //lastchange is right now!
  durationInPreviousState = timeInThisState;
  timeInThisState = 0;
}


//this function does the debounce and senses changes to buttonState
//it abuses global variables timeInThisState, lastChange and registeredState (see above)
int sensingChanges(int buttonState) {
  unsigned long t = millis(); //current millis time
  timeInThisState = t - lastChange; //this might get set to 0 later

  //if the button has switched
  //but can only switch as fast as debounceTime. So feel free to alter that if
  //you have better (or worse) buttons or you want the button presses to be 
  //sensed more slowly with noise (or some such)
  if(buttonState != registeredState && t-lastChange > debounceTime) { 
    //register the change in state
    lastChange = t; //what time was the last change
    durationInPreviousState = timeInThisState;
    timeInThisState = 0; //it just changed so no time has passed
    registeredState = buttonState; 
    if(buttonState == !PRESSED) {
      return BUTTONUP;
    }
    else {
      return BUTTONDOWN;
    }
  }
  return BUTTONSTATEUNCHANGED;
}


int dir = HIGH;
int on = 0;

void setDirectionAndSpeed(int dir, int speed) {
  digitalWrite(AIN1, dir);
  digitalWrite(AIN2, !dir);
  if(speed < 0)
    speed = 0;
  if(speed > 255) 
    speed = 255;
  analogWrite(PWMA,speed);
}

void brake() {
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);
  analogWrite(PWMA, 0);
}

void setup() {
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(PWMA, OUTPUT);
  
  brake();
  // Set up the serial port:
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(bPin, INPUT);
  
}

int didToggleOn = 0;

void loop() {
  // put your main code here, to run repeatedly:
  int result = sensingChanges(digitalRead(bPin)); //changes 4 other variables as well listed below
  //use result to know if there was a change
  //use registeredState if you just want to know high/low registered by arduino
  //use lastChange if you just want to know the time in millis since the last state change
  //use timeInThisState to know how long it was in this state.
  //use durationInPreviousState is how long the most recent state "was"
  int secondsTilStop = 1000;
  if(result == BUTTONUP) { //button went from pressed to not pressed (or from down to up) and is now in the not pressed (up) state
    if(durationInPreviousState < 100) {// :sanity checks--> and !didToggleOn and registeredState == PRESSED) {
      dir = !dir;
    }
    didToggleOn = 0;
  }
  else if(!didToggleOn and registeredState == PRESSED and timeInThisState > secondsTilStop) { //sanity: and result == BUTTONSTATEUNCHANGED 
    on = !on;
    didToggleOn = 1;
  }
  /*
  if(result == BUTTONDOWN) { //seeing a button being pushed down, change direction
    dir = !dir;
  }
  else if(result == BUTTONSTATEUNCHANGED  and registeredState == PRESSED) { //state didn't change and state is PRESSED
    if(timeInThisState > 1000) { //long press
      resetTimeInThisState();//reset the time    
      on = !on;  //turn things off/on
    }
  }
  else if(result == BUTTONSTATEUNCHANGED  and registeredState == !PRESSED and timeInThisState > 10000) {
    on = !on; //if the button isn't pressed it will turn itself on and off evey 10000 ms.
    resetTimeInThisState();
  }
  */
  setDirectionAndSpeed(dir,255*on); //using 255*1 and 255*0 to set the speed to max or 0 (start/stop)
}
