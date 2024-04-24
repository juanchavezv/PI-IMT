#include <Servo.h>
#include <ezButton.h>
Servo l_x_servo;
Servo l_y_servo;
Servo r_x_servo;
Servo r_y_servo;

// Inputs for the joystic
#define joystic_x_PIN A0
#define joystic_y_PIN A1
#define joystic_button_PIN 2

int joystic_x_val = 0; // To store value of the X axis
int joystic_y_val = 0; // To store value of the Y axis
int joystic_button_val = 0; // To store value of the button
bool joystic_button_state = true; //used to make a state system
ezButton button(joystic_button_PIN);

// Servomotor position (starts at 90°)
int l_x_servo_pos = 90;
int l_y_servo_pos = 90;
int r_x_servo_pos = 90;
int r_y_servo_pos = 90;

void setup() {
  Serial.begin(9600);
  button.setDebounceTime(50); // set debounce time to 50 milliseconds
  
  // Left X axis servo setup
  l_x_servo.attach(3);
  l_x_servo.write(l_x_servo_pos);
  // Left Y axis servo setup
  /*l_y_servo.attach(4);
  l_y_servo.write(l_y_servo_pos);
  // Right X axis servo setup
  r_x_servo.attach(5);
  r_x_servo.write(r_x_servo_pos);
  // Right Y axis servo setup
  r_y_servo.attach(6);
  r_y_servo.write(r_y_servo_pos);*/
}

int servo_pos_update(int joystic_val){
  
  int joystic_map = map(joystic_val, 0, 1023, 0, 180);
  int servo_pos;

  if (joystic_val > 507 || joystic_val < 497) { // Joystick moved significantly
    int delta = joystic_map > 90 ? 2 : -2; // Determine direction to move servo
    servo_pos += delta;
  }
  // Constrain the servo position to valid range (60 to 120)
  //servo_pos = constrain(servo_pos, 60, 120);
  return servo_pos;
}

void print_joystic(){
  Serial.print("x = ");
  Serial.print(joystic_x_val);
  Serial.print(", y = ");
  Serial.print(joystic_y_val);
  Serial.print(" : button = ");
  Serial.println(joystic_button_state);
}

void print_servo(){
  Serial.print("LEFT x = ");
  Serial.println(l_x_servo_pos);
}

void loop() {
  button.loop(); // MUST call the loop() function first

  // read joystic values
  joystic_x_val = analogRead(joystic_x_PIN);
  joystic_y_val = analogRead(joystic_y_PIN);
  joystic_button_val = button.getState();
 
  if (button.isReleased()) {
    joystic_button_state = ! joystic_button_state;
  }

  if (joystic_button_state) {
    l_x_servo_pos = servo_pos_update(joystic_x_val);
    l_x_servo.write(l_x_servo_pos);
    delay(50);
    l_y_servo_pos = servo_pos_update(joystic_y_val);
    l_y_servo.write(l_y_servo_pos);
    delay(50);
  } else {
    r_x_servo_pos = servo_pos_update(joystic_x_val);
    r_x_servo.write(r_x_servo_pos);
    delay(50);
    r_y_servo_pos = servo_pos_update(joystic_y_val);
    r_y_servo.write(r_y_servo_pos);
    delay(50);
  }

  //print_joystic();
  print_servo();
}