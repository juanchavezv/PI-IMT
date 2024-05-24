#include <Servo.h>
#include <ezButton.h>

Servo l_x_servo;
Servo l_y_servo;
Servo r_x_servo;
Servo r_y_servo;

// Inputs for the joystick
#define joystick_x_PIN A0
#define joystick_y_PIN A1
#define joystick_button_PIN 2
#define save_user_button_PIN 7
#define verify_user_button_PIN 8

int joystick_x_val = 0; // To store value of the X axis
int joystick_y_val = 0; // To store value of the Y axis
int joystick_button_val = 0; // To store value of the button
bool joystick_button_state = true; //used to make a state system
ezButton joystick_button(joystick_button_PIN);

int save_user_button_val = 0;
bool save_user_button_state = false; //used to make a state system
ezButton save_user_button(save_user_button_PIN);

int verify_user_button_val = 0;
bool verify_user_button_state = false; //used to make a state system
ezButton verify_user_button(verify_user_button_PIN);

// Servomotor position (starts at 90°)
int l_x_servo_pos = 90;
int l_y_servo_pos = 90;
int r_x_servo_pos = 90;
int r_y_servo_pos = 90;

void setup() {
  Serial.begin(9600);
  joystick_button.setDebounceTime(50); // set debounce time to 50 milliseconds
  save_user_button.setDebounceTime(50);
  verify_user_button.setDebounceTime(50);
  
  // Left X axis servo setup
  l_x_servo.attach(3);
  l_x_servo.write(l_x_servo_pos);
  // Left Y axis servo setup
  l_y_servo.attach(4);
  l_y_servo.write(l_y_servo_pos);
  // Right X axis servo setup
  r_x_servo.attach(5);
  r_x_servo.write(r_x_servo_pos);
  // Right Y axis servo setup
  r_y_servo.attach(6);
  r_y_servo.write(r_y_servo_pos);
}

int servo_pos_update(int joystick_val, int servo_pos) {
  int joystick_map = map(joystick_val, 0, 1023, 0, 180);

  if (joystick_val > 600) { // Joystick moved significantly to one side  
    servo_pos += 2.5; 
  }
  else if (joystick_val < 400) { // Joystick moved significantly
    servo_pos += -2.5; 
  }
  servo_pos = constrain(servo_pos, 60, 120);
  return servo_pos;
}

void save_user_data() {
  Serial.print(l_x_servo_pos);
  Serial.print(",");
  Serial.print(l_y_servo_pos);
  Serial.print(",");
  Serial.print(r_x_servo_pos);
  Serial.print(",");
  Serial.println(r_y_servo_pos);
}

void decode_serial_input(String input) {
  int commaIndex1 = input.indexOf(',');
  int commaIndex2 = input.indexOf(',', commaIndex1 + 1);
  int commaIndex3 = input.indexOf(',', commaIndex2 + 1);

  String lx = input.substring(0, commaIndex1);
  String ly = input.substring(commaIndex1 + 1, commaIndex2);
  String rx = input.substring(commaIndex2 + 1, commaIndex3);
  String ry = input.substring(commaIndex3 + 1);

  l_x_servo_pos = lx.toInt();
  l_y_servo_pos = ly.toInt();
  r_x_servo_pos = rx.toInt();
  r_y_servo_pos = ry.toInt();

  l_x_servo.write(l_x_servo_pos);
  l_y_servo.write(l_y_servo_pos);
  r_x_servo.write(r_x_servo_pos);
  r_y_servo.write(r_y_servo_pos);
}

void loop() {
  joystick_button.loop(); // MUST call the loop() function first
  save_user_button.loop();
  verify_user_button.loop();

  // read joystick values
  joystick_x_val = analogRead(joystick_x_PIN);
  joystick_y_val = analogRead(joystick_y_PIN);
  joystick_button_val = joystick_button.getState();
  save_user_button_val = save_user_button.getState();
  verify_user_button_val = verify_user_button.getState();
 
  if (joystick_button.isReleased()) {
    joystick_button_state = !joystick_button_state;
  }

  if (joystick_button_state) {
    l_x_servo_pos = servo_pos_update(joystick_x_val, l_x_servo_pos);
    l_x_servo.write(l_x_servo_pos);
    delay(50);
    l_y_servo_pos = servo_pos_update(joystick_y_val, l_y_servo_pos);
    l_y_servo.write(l_y_servo_pos);
    delay(50);
  } else {
    r_x_servo_pos = servo_pos_update(joystick_x_val, r_x_servo_pos);
    r_x_servo.write(r_x_servo_pos);
    delay(50);
    r_y_servo_pos = servo_pos_update(joystick_y_val, r_y_servo_pos);
    r_y_servo.write(r_y_servo_pos);
    delay(50);
  }

  if (save_user_button.isReleased()) {
    save_user_button_state = !save_user_button_state;
  }

  if (save_user_button_state) {
    save_user_button_state = !save_user_button_state;
  }

  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    decode_serial_input(input);
  }
  save_user_data();
}
