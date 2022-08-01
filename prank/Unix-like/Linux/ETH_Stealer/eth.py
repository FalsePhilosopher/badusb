from ast import For
from random import random
from turtle import clear
import colorama
import os 
from colorama import Fore
import random
import time
from numpy import character
import string
import socket
 
from threading import Thread
 
from pystyle import Colorate, Center, Write, Anime, Colors, System, Col
 
                
        
 
banner = r"""
                                                                    ..;===+.
                                                                .:=iiiiii=+=
                                                             .=i))=;::+)i=+,
                                                          ,=i);)I)))I):=i=;
                                                       .=i==))))ii)))I:i++
                                                     +)+))iiiiiiii))I=i+:'
                                .,:;;++++++;:,.       )iii+:::;iii))+i='
                             .:;++=iiiiiiiiii=++;.    =::,,,:::=i));=+'
                           ,;+==ii)))))))))))ii==+;,      ,,,:=i))+=:
                         ,;+=ii))))))IIIIII))))ii===;.    ,,:=i)=i+
                        ;+=ii)))IIIIITIIIIII))))iiii=+,   ,:=));=,
                      ,+=i))IIIIIITTTTTITIIIIII)))I)i=+,,:+i)=i+
                     ,+i))IIIIIITTTTTTTTTTTTI))IIII))i=::i))i='
                    ,=i))IIIIITLLTTTTTTTTTTIITTTTIII)+;+i)+i`
                    =i))IIITTLTLTTTTTTTTTIITTLLTTTII+:i)ii:'
                   +i))IITTTLLLTTTTTTTTTTTTLLLTTTT+:i)))=,
                   =))ITTTTTTTTTTTLTTTTTTLLLLLLTi:=)IIiii;
                  .i)IIITTTTTTTTLTTTITLLLLLLLT);=)I)))))i;
                  :))IIITTTTTLTTTTTTLLHLLLLL);=)II)IIIIi=:
                  :i)IIITTTTTTTTTLLLHLLHLL)+=)II)ITTTI)i=
                  .i)IIITTTTITTLLLHHLLLL);=)II)ITTTTII)i+
                  =i)IIIIIITTLLLLLLHLL=:i)II)TTTTTTIII)i'
                +i)i)))IITTLLLLLLLLT=:i)II)TTTTLTTIII)i;
              +ii)i:)IITTLLTLLLLT=;+i)I)ITTTTLTTTII))i;
             =;)i=:,=)ITTTTLTTI=:i))I)TTTLLLTTTTTII)i;
           +i)ii::,  +)IIITI+:+i)I))TTTTLLTTTTTII))=,
         :=;)i=:,,    ,i++::i))I)ITTTTTTTTTTIIII)=+'
       .+ii)i=::,,   ,,::=i)))iIITTTTTTTTIIIII)=+
      ,==)ii=;:,,,,:::=ii)i)iIIIITIIITIIII))i+:'
     +=:))i==;:::;=iii)+)=  `:i)))IIIII)ii+'
   .+=:))iiiiiiii)))+ii;
  .+=;))iiiiii)));ii+
 .+=i:)))))))=+ii+
.;==i+::::=)i=;
,+==iiiiii+,
`+=+++;`"""[1:]
 
 
 
ascii = """\n\n
▄▄▌  ▄• ▄▌▐▄• ▄ ▄▄▄▄▄            ▄▄▌   
██•  █▪██▌ █▌█▌▪•██  ▪     ▪     ██•  
██▪  █▌▐█▌ ·██·  ▐█.▪ ▄█▀▄  ▄█▀▄ ██▪   Made By 7LUX 
▐█▌▐▌▐█▄█▌▪▐█·█▌ ▐█▌·▐█▌.▐▌▐█▌.▐▌▐█▌▐▌
.▀▀▀  ▀▀▀ •▀▀ ▀▀ ▀▀▀  ▀█▄▀▪ ▀█▄▀▪.▀▀▀      '\n\n"""
 
 
 
def tg():
    System.Clear()
    System.Title("ETH STEALER - By 7LUX")
    print(Colorate.Horizontal(Colors.white_to_blue, Center.XCenter(banner)))
    time.sleep(1.5)
    miner()
def clear():
    os.system('cls') 
 
def miner():
    System.Title("ETH STEALER - By 7LUX")
    clear()
    print(Colorate.Horizontal(Colors.blue_to_red, Center.XCenter(ascii)))
    eth=input("How Much ETH Do You Want To Add To Your Wallet? : ")
    clear()
    print(Colorate.Horizontal(Colors.blue_to_red, Center.XCenter(ascii)))
    address=input("Enter Your ETH Adress: ")
    print("Ok...")
    character=string.ascii_lowercase+string.digits
    for _ in range(100000):#how much chance to find one wallet
        print(Fore.RED + "> %s | 0.00000 ETH" % "".join(random.sample(character, 32)))
    time.sleep(0.5)
    print(Fore.GREEN + f"> %s | {eth} ETH" % "".join(random.sample(character, 32)))
    time.sleep(0.5)
    print(Fore.LIGHTBLUE_EX + f"> Adding ETH To Your Wallet... | Wallet Adress : {address}""")
    input("Close: ")
 
    print('\n')
 
 
 
if __name__ == '__main__':
    tg()