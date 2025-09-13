#define WAIT_BUT A0   // кнопка включения режима ожидания
#define START_BUT A1
#define LAMP1 10     // левая светодиодная лента
#define LAMP2 9     // правая светодиодная лента
#define BEEPER 12    // пьезоизлучатель
#define BACKLIGHT_LEFT 0 // подсветка
#define BACKLIGHT_RIGHT 13

#define PROJECTOR1 A2
#define PROJECTOR2 A3


//------------------------------------------keypad_part
#include <Keypad.h>
const byte Keypad_ROWS = 4;
const byte Keypad_COLS = 3;
char Keypad_Keys[Keypad_ROWS][Keypad_COLS] = {
  {'E','D','C'}, 
  {'H','G','B'},
  {'N','F','A'},
  {'K','J','I'},
};
byte Keypad_rowPins[Keypad_ROWS] = {8, 7, 6, 5}; 
byte Keypad_colPins[Keypad_COLS] = {4, 3, 2}; 
Keypad BinoforKeypad = Keypad( makeKeymap(Keypad_Keys), Keypad_rowPins, Keypad_colPins, Keypad_ROWS, Keypad_COLS);
char PressedKey = 0;
//------------------------------------------keypad_part

// -=---------------------------------------dfplayer_part
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

SoftwareSerial mySerial(11, 12); // RX, TX
DFRobotDFPlayerMini myDFPlayer;
// -=---------------------------------------dfplayer_part

#include <Wire.h> // библиотека для управления устройствами по I2C 
#include <LCD_1602_RUS.h> // подключаем библиотеку LCD_1602_RUS
LCD_1602_RUS lcd(0x27,16,2); // присваиваем имя LCD для дисплея

#include <Servo.h>              // подключение библиотеки для работы с сервоприводом
Servo Set_pd;

#include <EEPROM.h>             // подключение библиотеки для работы с энергонезависимой памятью
struct { // создание структуры для сохранения в нее настроек
    double interval;
    int brigtness;
    int quantity;
    unsigned long time;
    double lenght;
    bool blink_type;
    bool train_type;
    bool mute = 0;
} set;
// создане глобальных переменных для настроек
double INTERVAL = 0.2, LENGHT = 0.2;
int BRIGHTNESS = 100, QUANTITY = 2;
unsigned long TIME = 10;
bool BLINK_TYPE = 0, TRAIN_TYPE = 0, MUTE = 0;
// создание переменных-счетчиков для разных частей кода
long last_time = 0, last_time1 = 0, last_time_for_projector1 = 0, last_time_for_projector2 = 0;
int count = 0, last_count = 0;
// создание булевых переменных-флагов для разных частей кода
bool f = 0, sep_blink = 0, waiting = 0, join_blink = 0, a1 = 0, save_settings_flag = 0, enc_hold = 0;
bool a0 = 1, settings_flag = 1, flag = 1;

bool flag_left_eye_text = 0, flag_left_eye = 0, flag_right_eye_text = 0, flag_right_eye = 0, flag_zasvet = 0, flag_both_eyes_text = 0;

int8_t arrow = 0;     // позиция стрелки

void setup() {
  // объявление пинов
  pinMode(WAIT_BUT, INPUT_PULLUP);
  pinMode(START_BUT, INPUT_PULLUP);

  pinMode(LAMP1, OUTPUT);
  pinMode(LAMP2, OUTPUT);
  pinMode(BEEPER, OUTPUT);
  pinMode(BACKLIGHT_LEFT, OUTPUT);
  pinMode(BACKLIGHT_RIGHT, OUTPUT);

  digitalWrite(BACKLIGHT_LEFT, 0);
  digitalWrite(BACKLIGHT_RIGHT, 0);
  digitalWrite(LAMP2, 0);
  digitalWrite(LAMP1, 0);

  pinMode(PROJECTOR1, OUTPUT);
  pinMode(PROJECTOR2, OUTPUT);
  // получение настроек из энергонезависимой памяти
  EEPROM.get(0, set);
  INTERVAL = set.interval; BRIGHTNESS = set.brigtness; QUANTITY = set.quantity; TIME = set.time; LENGHT = set.lenght; BLINK_TYPE = set.blink_type; TRAIN_TYPE = set.train_type; MUTE = set.mute;
  
  lcd.init();        // инициализация дисплея
  lcd.backlight();   // включение подсветки дисплея
  lcd.clear();       // очистка дисплея
  mySerial.begin(9600);
  myDFPlayer.begin(mySerial);
  myDFPlayer.volume(30);
  //Serial.begin(9600);
}

void loop() {
  check_buttons();
  train_auto();
  PressedKey = BinoforKeypad.getKey();
  if (PressedKey == 'C') settings_flag = !settings_flag;
  else if (PressedKey == 'J') {
    lcd.clear();
    printRussian("   СОВМЕСТНОE", 0, 0);
    printRussian("    МИГАНИЕ", 0, 1);
    BLINK_TYPE = 0;
    delay(1500);
  }
  else if (PressedKey == 'I') {
    lcd.clear();
    printRussian("   РАЗДЕЛЬНОЕ", 0, 0);
    printRussian("    МИГАНИЕ", 0, 1);
    BLINK_TYPE = 1;
    delay(1500);
  }
  else if (PressedKey == 'K') {
    TRAIN_TYPE = !TRAIN_TYPE;
    lcd.clear();
    if (!TRAIN_TYPE) printRussian("     РУЧНОЙ", 0, 0);
    else             printRussian(" АВТОМАТИЧЕСКИЙ", 0, 0);
    printRussian("     РЕЖИМ", 0, 1);
    delay(1500);
  }
  else if (PressedKey == 'G') {
    MUTE = !MUTE;
    printRussian("     РЕЖИМ      ", 0, 0);
    if (MUTE) printRussian("   БЕЗ ЗВУКА    ", 0, 1);
    else printRussian("   СО ЗВУКОМ     ", 0, 1);
    delay(1500);
  }
  if (settings_flag) {                                                           // если энкодер не был нажат
    if (save_settings_flag) {settings_are_saved();} 
    // сохранение настроек в энергонезависимую память и вывод надписи "настройки сохранены!"
    else interface(); // вывод времени и количества засветов
    if (f == false) {
      last_time = millis();
      last_count = count;
    }
    f = 1;
    if (sep_blink) zasvet(1);                // выбор режимов тренировки или ожидания в зависимости от положения кнопок
    else if (join_blink) zasvet(0);
    else if (waiting) zasvet(2);
    else {
      f = false;
      analogWrite(LAMP2, 0);
      analogWrite(LAMP1, 0);
      last_time1 = millis();
      last_time = millis();
    }
  }
  else change_settings();                                                                 // если энкодер был нажат
}

void change_settings() {
  last_time = millis(); save_settings_flag = 1;
  if (!flag) {
    lcd.clear();
    settings();
    flag=1;
    enc_hold = 0;
  }
  enc_hold=0;
  if (PressedKey) { // при повороте ручки энкодера в любую сторону
    lcd.clear();
    if (PressedKey == 'B') { // при повороте вправо
      if (arrow == 0) INTERVAL += 0.1;
      if (arrow == 1 && BRIGHTNESS != 100) BRIGHTNESS++;
      if (arrow == 2) QUANTITY++;
      if (arrow == 3) TIME++;
      if (arrow == 4) LENGHT += 0.1;
    } 
    else if (PressedKey == 'E') {
      arrow++;
      if (arrow > 4) arrow = 0;
    }
    else if (PressedKey == 'A') { // при повороте влево
      if (arrow == 0 && INTERVAL > 0) INTERVAL -= 0.1;
      if (INTERVAL < 0) INTERVAL = 0;
      if (arrow == 1 && BRIGHTNESS != 0) BRIGHTNESS--;
      if (arrow == 2 && QUANTITY != 0) QUANTITY--;
      if (arrow == 3 && TIME != 0) TIME--;
      if (arrow == 4 && LENGHT > 0) LENGHT -= 0.1;
      if (LENGHT < 0) LENGHT = 0;
    }
    else if (PressedKey == 'D') {
      arrow--;
      if (arrow < 0) arrow = 4;
    }
    settings();
  }
}
void check_buttons() {
  if (!TRAIN_TYPE) {
      digitalWrite(BACKLIGHT_LEFT, 1);
      digitalWrite(BACKLIGHT_RIGHT, 1);
    }
    else {
      digitalWrite(BACKLIGHT_LEFT, 0);
      digitalWrite(BACKLIGHT_RIGHT, 0);
    }
  if (join_blink || sep_blink || waiting) {
    digitalWrite(BACKLIGHT_LEFT, 0);   // включение и отключение подсветки
    digitalWrite(BACKLIGHT_RIGHT, 0);
  }
  else if (!TRAIN_TYPE)  {
    digitalWrite(BACKLIGHT_LEFT, 1);
    digitalWrite(BACKLIGHT_RIGHT, 1);
  }
  if (!digitalRead(START_BUT) && !TRAIN_TYPE) {
    if (!BLINK_TYPE) join_blink = !join_blink;
    else sep_blink = !sep_blink;
    delay(150);
  }
  else if (!digitalRead(START_BUT) && TRAIN_TYPE) { flag_left_eye_text = 1;}
  if (!digitalRead(WAIT_BUT) && !TRAIN_TYPE) {waiting = !waiting; delay(150);}

  if (PressedKey == 'F' && !TRAIN_TYPE) {
    last_time_for_projector1 = millis();
    while (millis()-last_time_for_projector1 <= LENGHT*1000) digitalWrite(PROJECTOR1, 1);
    digitalWrite(PROJECTOR1, 0);
  }

  if (PressedKey == 'H' && !TRAIN_TYPE) {
    last_time_for_projector2 = millis();
    while (millis()-last_time_for_projector2 <= LENGHT*1000) digitalWrite(PROJECTOR2, 1);
    digitalWrite(PROJECTOR2, 0);
  }
}
void settings() {// функция для вывода меню настроек
  if (arrow<2) {
    printRussian("ИНТЕРВАЛ:", 1, 0); lcd.setCursor(13, 0); lcd.print(INTERVAL); 
    printRussian("ЯРКОСТЬ:", 1, 1); printRight(BRIGHTNESS, 0, 1);
  }
  else if (arrow>=2 && arrow<4) {
    printRussian("КОЛИЧЕСТВО:", 1, 0);  printRight(QUANTITY, 1, 0);
    printRussian("ВРЕМЯ:", 1, 1); lcd.setCursor(12, 1); printTime(TIME);
  }
  else {
    printRussian("ДЛИНА:", 1, 0); lcd.setCursor(13, 0); lcd.print(LENGHT);
    printRussian("               ", 1, 1);
  }
  if (arrow%2==0) lcd.setCursor(0, 0);
  else lcd.setCursor(0, 1);
  lcd.write(126);
}
void interface() {// функция для вывода интерфейса во время проведения засвета
    printRussian("ВРЕМЯ     КОЛ-ВО", 0, 0);
    lcd.setCursor(0, 1);  printTime(TIME - (millis()-last_time)/1000); printRussian("          ", 4, 1); 
    if (count<10) lcd.print(' '); lcd.print(count);

    flag=false;
}
// функция для сохранения настроек в энергонезависимую память и вывода соответствующей надписи на дисплей
void settings_are_saved() {
    save_settings_flag = false;
    enc_hold = 0;
    
    printRussian("НАСТРОЙКИ       ", 0, 0);
    printRussian("      СОХРАНЕНЫ!", 0, 1);

    set.interval=INTERVAL; set.brigtness=BRIGHTNESS; set.quantity=QUANTITY; set.time=TIME; set.lenght=LENGHT; set.blink_type = BLINK_TYPE; set.train_type = TRAIN_TYPE; set.mute = MUTE;


    EEPROM.put(0, set);
    arrow = 0;
    delay(1500);
}
void printRussian(String s, byte symb, byte str) { // функция для вывода русских символов на дисплей
  lcd.setCursor(symb, str);
  lcd.print(s);
}
void printRight(int num, bool type, bool str) {    // функция для вывода чисел в ближе к правой границе дисплея
  if (type == 0) {
    lcd.setCursor(15, str); lcd.print("%");
    if (num >= 100) lcd.setCursor(12, str);
    else if (num>9) lcd.setCursor(13, str);
    else lcd.setCursor(14, str);
    lcd.print(num);
  } 
  else {
    if (num >= 100) lcd.setCursor(13, str);
    else if (num>9) lcd.setCursor(14, str);
    else lcd.setCursor(15, str);
    lcd.print(num);
  }
}
void printTime(int time) {                         // функция для вывода времени
  lcd.print(time/60); 
  lcd.print(":"); 
  if (time%60 < 10) lcd.print(0); 
  lcd.print(time%60);
}
void zasvet(int type) {                                                // функция для основной тренировки
  if (type == 2) {
    if (millis()-last_time1 > TIME*1000) {
        Serial.println("ТРЕНИРОВКА ЗАВЕРШЕНА");
        waiting = false;
      }
  }
  else {
  if (millis() - last_time <= TIME*1000) {
    int INTER = INTERVAL*1000;
    int pwm = map(BRIGHTNESS, 0, 100, 0, 255);
    pwm = constrain(pwm, 0, 255);
    if (INTER == 0) {analogWrite(LAMP1, pwm); analogWrite(LAMP2, pwm);} // если интервал равен 0, не отключать св. ленты
    else {
      if (millis()- last_time1 > INTERVAL*1000) {
        last_time1 = millis();
        if (type == 1) {                                                     // включить режим тренировки поочередного мигания 
          if (a1 == 1) {analogWrite(LAMP2, pwm); a1 = false;}
          else {analogWrite(LAMP2, 0); a1 = 1;}
          if (a0 == 1) {analogWrite(LAMP1, pwm); a0 = false;}
          else {analogWrite(LAMP1, 0); a0 = 1;}
        }
        else if (type == 0) {                                                          // включить режим тренировки совместного мигания 
          if (a1 == 1) {analogWrite(LAMP2, pwm); analogWrite(LAMP1, pwm); a1 = false;}
          else {analogWrite(LAMP1, 0); analogWrite(LAMP2, 0); a1 = 1;}
      }
    }
  }
    int last_count = count;
  }
  else {                                        // после прохождения определенного, настраиваемого в настройках времени
    digitalWrite(LAMP1, 0);
    digitalWrite(LAMP2, 0);
    if (last_count == count) {
      count++;
      // при достижении определенного количества выполненных засветов играть музыку с помощью пьезоизлучателя
      if (count == QUANTITY) {
        myDFPlayer.play(9);
        delay(1500);
      }
      else {
        myDFPlayer.play(7);
        delay(1500);
      }
      sep_blink = false;
      join_blink = false;
    }
  }
  }
}

void train_auto() {
  if (flag_left_eye_text) {
    myDFPlayer.play(1);
    digitalWrite(BACKLIGHT_LEFT, 1);
    flag_left_eye_text = 0;
    flag_left_eye = 1;
    delay(2000);
  }
  if (flag_left_eye) {
    last_time_for_projector1 = millis();
    while (millis()-last_time_for_projector1 <= LENGHT*1000) digitalWrite(PROJECTOR1, 1);
    digitalWrite(PROJECTOR1, 0);
    flag_left_eye = 0;
    flag_right_eye_text = 1;
    digitalWrite(BACKLIGHT_LEFT, 0);
  }
  if (flag_right_eye_text) {
    myDFPlayer.play(3);
    digitalWrite(BACKLIGHT_RIGHT, 1);
    flag_right_eye_text = 0;
    flag_right_eye = 1;
    delay(2000);
  }
  if (flag_right_eye) {
    last_time_for_projector2 = millis();
    while (millis()-last_time_for_projector2 <= LENGHT*1000) digitalWrite(PROJECTOR2, 1);
    digitalWrite(PROJECTOR2, 0);
    flag_right_eye = 0;
    flag_both_eyes_text = 1;
    digitalWrite(BACKLIGHT_RIGHT, 0);
  }
  if (flag_both_eyes_text) {
    myDFPlayer.play(5);
    delay(2000);
    flag_both_eyes_text = 0;
    flag_zasvet = 1;
  }
  if (flag_zasvet) {
    if (!BLINK_TYPE) join_blink = !join_blink;
    else sep_blink = !sep_blink;
    flag_zasvet = 0;
  }
  if (!digitalRead(WAIT_BUT) && TRAIN_TYPE) {
    sep_blink = 0; join_blink = 0; waiting = !waiting; 
    delay(150); 
    analogWrite(LAMP1, 0); 
    analogWrite(LAMP2, 0);
    last_time = millis();}
}
