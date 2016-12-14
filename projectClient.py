import sys
import os
import fnmatch
import socket
currentUserID = "" #This will hold the user id info
clientSocket = None
#DISCUSSIONS IS INPUT FROM SERVER THIS IS JUST TO TEST GROUPS
def main():
	arguements = sys.argv
	global clientSocket
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		clientSocket.connect((arguements[1], int(arguements[2])))
	except Exception:
		print("Incorrect number of arguements provided")
		return

	argv = input("Type in your login ID: ")
	loginHandler(argv)
	while(1):
		argv = input("Enter command (help to display help menu): ")
		argv = argv.split(" ")
		parseArgs(argv)

def parseArgs(argv):
	if argv[0] == "ag":
		agHandler(argv)
	elif argv[0] == "sg":
		sgHandler(argv)
	elif argv[0] == "rg":
		rgHandler(argv)
	elif argv[0] == "help":
		helpMenu()
	elif argv[0] == "logout":
		print(str(currentUserID) + " is logging out")
		clientSocket.close()
		sys.exit(0)
	else:
		print("Invalid command")
def helpMenu():
	print("ag - Show all groups (Usage: ag n)")
	print("sg - Show subscribed groups (Usage: sg n)")
	print("rg - Read group (Usage: rg [gname] n)")
	print("logout - Logout current user (Usage: logout)")

def loginHandler(argv):
	print("Weclome " + argv)
	global currentUserID
	currentUserID = argv
	try:
		userData = open(currentUserID, 'r+')#read from existing file
		userData.close()
	except FileNotFoundError:
		userData = open(currentUserID, 'w+')#create new file
		userData.close()

def rgHandler(argv):#INCOMPLETE
	groupName = ""
	n = 0
	if(len(argv)==2):#Contains rg and the group name
		n = 2
		groupName = argv[1]
	elif (len(argv)==2):#Contains rg , group name and n
		groupName = argv[1]
		n = int(argv[2])
	else:
		print("Illegal arguements detected")
		return
	toSend = argv[0] +"`" + argv[1]

	argument = str.encode(toSend)
	clientSocket.sendall(argument)
	serverGroupsDates = clientSocket.recv(4096)
	serverGroupsSubjects = clientSocket.recv(4096)
	decodedStringSubject = serverGroupsSubjects.decode("utf-8")
	decodedStringDate = serverGroupsDates.decode("utf-8")
	rawPostMessage = decodedStringSubject.split("`")
	rawDateMessage = decodedStringDate.split("`")
	postMessage = []
	dateMessage = []
	for i in rawDateMessage:
		if(len(i) > 0):
			dateMessage.append(i)
	for i in rawPostMessage:
		if(len(i) > 0):
			postMessage.append(i)

	userData = open(currentUserID,"r+")
	userDataRead = userData.read()
	rawSubscribedGroupList = userDataRead.split("\n")
	subscribedGroupList = []
	unReadMessages = []

	for i in range(len(rawSubscribedGroupList)):
		if(len(rawSubscribedGroupList[i]) > 0):
			temp = rawSubscribedGroupList[i].split("`")
			subscribedGroupList.append(temp[0])
			unReadMessages.append(int(temp[1]))

	iterate = min(len(unReadMessages),len(subscribedGroupList))
	GID = 0
	for GID in range(iterate):
		if(subscribedGroupList[GID] == groupName):
			break
	unread = int(unReadMessages[GID])
	unread = len(postMessage) - unread

	sendToServer = ""
	for i in range(len(subscribedGroupList)):
		sendToServer = sendToServer + subscribedGroupList[i]+"`"#THIS IS WHAT I SEND TO SERVER
	sendToServer = "sg" + "`"+sendToServer

	userData.close()

	for i in range(min(len(postMessage),len(dateMessage))):
		if(i < unread):
			print(str((i%n)+1)+".\tN\t" + dateMessage[i] +" "+postMessage[i])
		else:
			print(str((i%n)+1)+".\t \t" + dateMessage[i] +" "+postMessage[i])

		if ((i+1) % n == 0 and i != 0) or i == len(postMessage) - 1:
			userInput = input("Type:\nn lists the next "+str(n) +" posts\np to post\nr to mark as read\n[id] to read a post\nq to exit\nChoose: ").split(" ")
			if(userInput[0]=="n"):
				continue
			# elif(userInput[0]=="r"):
			# 	if (len(userInput)>1) and  (len(userInput)<3):
			# 		tempRead = userInput[1].split("-")
			# 		if (len(tempRead)==1):
			# 			listRead = tempRead
			# 		elif (len(tempRead)==2):
			# 			for j in range(int(tempRead[0]),int(tempRead[1])+1):
			# 				listRead.append(str(j))
			# 		else:
			# 			print("Invalid arguments")
			# 	else:
			# 		print("Invalid arguments")
			elif (userInput[0]=="p"):
				subject = input("Enter subject: ")
				content=""
				while(True):
					ui = input("Enter content (Type 0x0 to finish typing): ")
					if(ui =="0x0"):
						break
					content = content + ui + "\\n"
				global post
				post = "p`"+currentUserID +"`"+ groupName +"`"+ subject +"`"+ content

				argument = str.encode(post)
				clientSocket.sendall(argument)

			elif (userInput[0] >= "1") or (userInput[0] <= (str(n))):
				messageIndex = (int(userInput[0])-1) + (int(i/n))*n
				toSend = dateMessage[messageIndex]
				toSend = "id`"+groupName+"`"+str(toSend)
				argumentID = str.encode(toSend)
				clientSocket.sendall(argumentID)
				post = clientSocket.recv(4096).decode("utf-8")
	            # post = "Nov 2016`Subject`Author`ContentLine1\\nContentLine2\\nContentLine3\\nContentLine4\\nContentLine5"
				serverPost = post.split("`")
				if(len(serverPost) == 4):
					print("Group: " + groupName)
					print("Subject: " + serverPost[1])
					print("Author: " + serverPost[2])
					print("Date: " + serverPost[0])
					RawContent = serverPost[3].split('\n')
					content = []
					for j in RawContent:
						if len(j) > 0:
							content.append(j)
					for j in range(len(content)):
						print(content[j])#this prints out the lines
						if((j+1)%n == 0 and j!=0) or j == len(content)-1:
							userInput = input("Type:\nn to read next " + str(n) + " lines\nq to exit post: ").split(" ")
							if userInput[0] == "n":
								if j == len(content):
									print("Nothing more to read.. Exiting Post\n")
									break
								continue
							elif userInput[0] == "q":
								print("Exiting Post\n")
								break
				else:
					print("Error occoured while recieving message")

			elif (userInput[0]=="q"):
				break

def agHandler(argv):
	if(len(argv)==1):
		n = 5
	elif (len(argv)==2):
		try:
			n = int(argv[1])
		except Exception:
			print("Illegal arguements detected")
			return
	else:
		print("Illegal arguements detected")
		return

	argument = str.encode(argv[0])
	clientSocket.sendall(argument)
	serverGroupsName = clientSocket.recv(4096)#fromServerAG.split("`")
	decodedString = serverGroupsName.decode("utf-8")
	discussions = decodedString.split(",")
	# discussions = fromServerAG.split("`")

	userData = open(currentUserID,"r+")
	userDataRead = userData.read()
	rawSubscribedGroupList = userDataRead.split("\n")#Lists all the groups the current user is suscribed to
	subscribedGroupList = []
	unReadMessages = []

	try:
		for i in range(len(rawSubscribedGroupList)):
			groupName = rawSubscribedGroupList[i].split("`")
			subscribedGroupList.append(groupName[0])
			unReadMessages.append(groupName[1])

	except Exception:
		print("User data is corrupted, delete file to continue")

	for i in range(1, len(discussions)+1):
		if (discussions[i-1] not in subscribedGroupList):
			print(str(((i-1)%n)+1) + "\t( )\t" + discussions[i-1])
		else:
			print(str(((i-1)%n)+1) + "\t(s)\t" + discussions[i-1])

		if (i% n == 0 and i != 1) or i == len(discussions) :

			userInput = input("Type:\ns to suscribe\nu to unsuscribe\nn to display next set of "+str(n) +" items\nq to quit\nChoose: ").split(" ")
			if userInput[0] == "n":
				continue
			elif userInput[0] == "q":
				break
			elif userInput[0] == "s":
				if (len(userInput) > 1):
					for j in range(1, len(userInput)):
						index = (int(userInput[j])+(i-n))-1

						if (index  > len(discussions)-1) or int(userInput[j]) < 1:
							print("Invalid index")
						else:
							if discussions[index] not in subscribedGroupList:
								subscribedGroupList.insert(0,discussions[index])
								unReadMessages.insert(0,"0")
								print("You have successfully suscribed to: " + discussions[index])
							else:
								print("You are already suscribed to " + discussions[index])
				else:
					print("Not enough arguements provided")
			elif userInput[0] == "u":
				if (len(userInput) > 1):
					for j in range(1, len(userInput)):
						x = int(((i-1)/n))*n
						index = (int(userInput[j])+x)-1
						if (index  > len(discussions)-1) or int(userInput[j]) < 1:
							print("Invalid index")
						else:
							if discussions[index] in subscribedGroupList:
								subscribedGroupListIndex = subscribedGroupList.index(discussions[index])
								subscribedGroupList.remove(discussions[index])
								unReadMessages.pop(subscribedGroupListIndex)
								print("You have successfully unsuscribed to: " + discussions[index])
							else:
								print("You cannot unsuscribe from a group that you are not suscribed to.")
				else:
					print("Not enough arguements provided")
			else:
				print("Command not found")

	userData.close() #closing file
	os.remove(currentUserID) #removing file

	newList = []############# A brave workaround ##############

	iterate = min(len(subscribedGroupList),len(unReadMessages))
	for i in range(int(iterate)):
		if len(subscribedGroupList[i]) > 1:
			string = subscribedGroupList[i] + "`" + unReadMessages[i]
			newList.append(string)

	userData = open(currentUserID,"w+")
	for i in range(len(newList)):
		userData.write(newList[i]+"\n")

	userData.close() #closing file

def sgHandler(argv):
	if(len(argv)==1):
		n = 5
	elif (len(argv)==2):
		try:
			n = int(argv[1])
		except Exception:
			print("Illegal arguements detected")
			return
	else:
		print("Illegal arguements detected")
		return

	#User data related to subscribed group is accessed from .txt file
	userData = 0
	try:
		userData = open(currentUserID, 'r+')#read from existing file
	except FileNotFoundError:
		print("User data is empty")
		return

	userData = open(currentUserID,"r+")
	userDataRead = userData.read()
	rawSubscribedGroupList = userDataRead.split("\n")#Lists all the groups the current user is suscribed to
	subscribedGroupList = []
	unReadMessages = []

	try:
		for i in range(len(rawSubscribedGroupList)):
			if(len(rawSubscribedGroupList[i]) > 0):
				groupName = rawSubscribedGroupList[i].split("`")
				subscribedGroupList.append(groupName[0])
				unReadMessages.append(groupName[1])
	except Exception:
		print("User data is corrupted, delete file and restart")

	newSubscribedGroupList = []
	newUnReadMessages = []
	iterate = min(len(unReadMessages),len(subscribedGroupList))
	for i in range(iterate): #existing list from file
		newSubscribedGroupList.append(subscribedGroupList[i]) #we will delete from this list and write this list to file
		newUnReadMessages.append(unReadMessages[i])

	sendToServer = ""
	for i in range(len(subscribedGroupList)):
		sendToServer = sendToServer + subscribedGroupList[i]+"`"#THIS IS WHAT I SEND TO SERVER
	sendToServer = "sg" + "`"+sendToServer

	argument = str.encode(sendToServer)
	clientSocket.sendall(argument)
	
	serverGroupsName = clientSocket.recv(4096)#fromServerAG.split("`")
	decodedString = serverGroupsName.decode("utf-8")
	fromServer = decodedString.split("`") #This is the return from the server

	discussions =[]
	for i in fromServer:
		if(len(i) > 0):
			discussions.append(i)

	for i in range(1, iterate+1):
		if(int(discussions[i-1])-int(unReadMessages[i-1]) > 0):
			print(str(((i-1)%n)+1) + ".\t"+str(int(discussions[i-1])-int(unReadMessages[i-1]))+"\t" + subscribedGroupList[i-1])
		else:
			print(str(((i-1)%n)+1) + ".\t \t" + subscribedGroupList[i-1])

		if (i% n == 0 and i != 1) or i == len(subscribedGroupList):
			userInput = input("Type:\nu to unsuscribe\nn to display next set of "+str(n) +" items\nq to quit\nChoose: ").split(" ")
			if userInput[0] == "n":
				continue
			elif userInput[0] == "q":
				break
			elif userInput[0] == "u":
				if (len(userInput) > 1):
					for j in range(1, len(userInput)):
						x = int(((i-1)/n))*n
						index = (int(userInput[j])+x)-1
						if (index  > len(subscribedGroupList)-1) or int(userInput[j]) < 1:
							print("Invalid index")
						else:
							if subscribedGroupList[index] in newSubscribedGroupList:
								newSubscribedGroupListIndex = newSubscribedGroupList.index(subscribedGroupList[index])
								newSubscribedGroupList.remove(subscribedGroupList[index])
								newUnReadMessages.pop(newSubscribedGroupListIndex)
								print("You have successfully unsuscribed to: " + subscribedGroupList[index])
							else:
								print("You cannot unsuscribe from a group that you are not suscribed to.")
				else:
					print("Not enough arguements provided")
			else:
				print("Command not found")

	userData.close() #closing file
	os.remove(currentUserID) #removing file

	newList = []############# A brave workaround ##############
	iterate = min(len(newSubscribedGroupList),len(newUnReadMessages))
	for i in range(iterate):
		if len(newSubscribedGroupList[i]) > 1:
			string = newSubscribedGroupList[i] + "`" + newUnReadMessages[i]
			newList.append(string)

	userData = open(currentUserID,"w+")
	for i in range(len(newList)):
		userData.write(newList[i]+"\n")

	userData.close() #closing file

main();