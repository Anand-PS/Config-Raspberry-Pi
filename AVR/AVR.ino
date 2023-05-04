#include <SoftwareSerial.h>
#include "PMButton.h"

PMButton button1(2);

bool developer_mode   = 0;    // make it 0 for normal mode
int debouncing_delay  = 30;   // in milli seconds

int character_length_delay    = 1000; // delay between each character
int word_length_delay         = 2000; // delay between each word
int sentence_length_delay     = 3000; // delay between each sentence

unsigned long key_pressed_millis  = 0;

bool char_joined         = 0;
bool word_joined         = 0;
bool sentence_completed  = 0;


int motor_pin     = A0;
int buzzer_pin    = 5;
int bt_state_pin  = 4;
int button_pin    = 2;
int led_pin       = 13;

int  received_data      = 0;
bool bluetooth_state  = 0;
bool bt_connected_flag  = 0;

String click_input      = "";
String input_word       = "";
String input_sentence   = ""; 

SoftwareSerial btSerial(12, 11); // RX, TX

void setup() 
{
  Serial.begin(9600);
  btSerial.begin(9600);
  
  pinMode(motor_pin,    OUTPUT);
  pinMode(buzzer_pin,   OUTPUT);
  pinMode(bt_state_pin, INPUT);
  pinMode(button_pin,   INPUT_PULLUP);
  pinMode(led_pin,      OUTPUT);

  button1.begin();
  
  //You can set button timing values for each button to fine tune interaction.
  button1.debounce(20);//Default is 10 milliseconds
  button1.dcGap(50);//Time between clicks for Double click. Default is 200 milliseconds
  button1.holdTime(200);//Default is 2 seconds
  button1.longHoldTime(2500);//Default is 5 seconds
  
//  while (!Serial) 
//  {
//    ; // wait for serial port to connect. Needed for native USB port only
//  }


  for(int i=0;i<3;i++)  // Boot successful
  {
    digitalWrite(buzzer_pin,HIGH);
    digitalWrite(led_pin,HIGH);
    delay(100);
    digitalWrite(buzzer_pin,LOW);
    digitalWrite(led_pin,LOW);
    delay(80);
  }

}

void useButonCheck()
{  
  if(button1.clicked())
  {
    key_pressed_millis = millis();
    
    char_joined         = 0;
    word_joined         = 0;
    sentence_completed  = 0;
    
    
    click_input+=".";

    if(developer_mode)
    {
      btSerial.println(".");
      
      digitalWrite(buzzer_pin,HIGH);
      digitalWrite(motor_pin,HIGH);
      delay(100);
      digitalWrite(buzzer_pin,LOW);
      digitalWrite(motor_pin,LOW);
    }
  }

  if(button1.held())
  {
    key_pressed_millis = millis();
    
    char_joined         = 0;
    word_joined         = 0;
    sentence_completed  = 0;
    
    
    click_input+="_";

    if(developer_mode)
    {
      btSerial.println("_");
      
      digitalWrite(buzzer_pin,HIGH);
      digitalWrite(motor_pin,HIGH);
      delay(200);
      digitalWrite(buzzer_pin,LOW);
      digitalWrite(motor_pin,LOW);
    }
  }
   
  if(button1.heldLong())
  {
      Send();
      sentence_completed = 1;  //to prevent continuous call of send() if time elapsed
  }
}
  

void timerHandler()
{
  if( (millis() - key_pressed_millis >= character_length_delay) || click_input.length() >= 5 && char_joined==0)
    {
       click_input    += " ";
       input_word     += click_input;
       click_input     = "";
       char_joined     = 1; // one English character completed
    }

  else if(millis() - key_pressed_millis >= word_length_delay  &&  word_joined == 0)
    {
       input_word     += "  ";
       input_sentence += input_word;
       word_joined     = 1;
    }

  else if(millis() - key_pressed_millis >= sentence_length_delay && sentence_completed == 0)
    {
       Send();
       sentence_completed = 1;
    }
}

void Send()
{
  btSerial.println(input_sentence);
  Serial.println("Data send");
  input_sentence = "";
}

void loop() 
{
  button1.checkSwitch();

  timerHandler();
  
  //used to see the state change
  useButonCheck();
  
  //read_user_input();
  
  read_sensors();

  //send_data();

  receive_data();

  if(developer_mode)
  {
    serial_feedback();
  }

  bt_connection_status_feedback();
}


void read_sensors()
{
  bluetooth_state = digitalRead(bt_state_pin);
}


void receive_data()
{
  if (btSerial.available()>0)
  {
    received_data = btSerial.read();

    if(received_data == '0')
    {
      digitalWrite(buzzer_pin,LOW);
      digitalWrite(motor_pin,LOW);
    }
    if(received_data == '1')
    {
      digitalWrite(motor_pin,HIGH);
    }
  
    if(received_data == '2')
    {
     digitalWrite(buzzer_pin,HIGH);
    }
  }
}


void bt_connection_status_feedback()
{
  if(bluetooth_state == 1 && bt_connected_flag == 0)
  {
    for(int i=0;i<2;i++)
    {
      digitalWrite(buzzer_pin,HIGH);
      digitalWrite(motor_pin,HIGH);
      delay(100);
      digitalWrite(buzzer_pin,LOW);
      digitalWrite(motor_pin,LOW);
      delay(80);
    }

    bt_connected_flag = 1;
  }

  if(bluetooth_state == 0 && bt_connected_flag == 1)
  {
      digitalWrite(buzzer_pin,HIGH);
      digitalWrite(motor_pin,HIGH);
      delay(500);
      digitalWrite(buzzer_pin,LOW);
      digitalWrite(motor_pin,LOW);
    

    bt_connected_flag = 0;
  }
}

void serial_feedback()
{
  Serial.print("BT state: ");
  Serial.print(bluetooth_state);

  Serial.print(" | Rx Data: ");
  Serial.print(received_data);

  Serial.print(" | Tx Data: ");
  //Serial.println(data_send);
}
