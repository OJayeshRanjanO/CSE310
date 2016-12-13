import sys
import os
import fnmatch
import socket
currentUserID = "" #This will hold the user id info
clientSocket = None
#DISCUSSIONS IS INPUT FROM SERVER THIS IS JUST TO TEST GROUPS
fromServerAG= "Group 1`Group 2`Group 3`Group 4`Group 5`Group 6"
def main():
	argv = input("Type in your login ID: ")
	# global clientSocket
	# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# clientSocket.connect(("allv24.all.cs.stonybrook.edu", 6789))
	loginHandler(argv)
	while(1):
		argv = input("Enter command: ")
		argv = argv.split(" ")
		parseArgs(argv)
def parseArgs(argv):
	if argv[0] == "ag":
		agHandler(argv)
	elif argv[0] == "sg":
		sgHandler(argv)
	elif argv[0] == "rg":
		rgHandler(argv)
	elif argv[0] == "logout":
		print(str(currentUserID) + " is logging out")
		# clientSocket.close()
		sys.exit(0)
	else:
		print("Invalid command")

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
	print(argv)
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
	# postMessage = ["Message1","Message2","Message3","Message4","Message5","Message6"]
	# dateMessage = ["Nov 2016","Dec 2016","Jan 2017","Feb 2017","Mar 2017","Apr 2017"]
	# unread = 5
	# listRead = []
	# for i in range(len(postMessage)):
	# 	if(i < unread):
	# 		if(str(i+1) not in listRead)
	# 			print(str(i+1)+". N " + dateMessage[i] +" "+postMessage[i])
	# 		else:
	# 			print(str(i+1)+".   " + dateMessage[i] +" "+postMessage[i])				
	# 	else:
	# 		print(str(i+1)+".   " + dateMessage[i] +" "+postMessage[i])
 #    	if ((i+1) % n == 0 and i != 0) or i == len(postMessage) - 1:
	# 		userInput = input("Type:\nn lists the next "+str(n) +" posts\nListChoose: ").split(" ")
	#         if(userInput[0]=="n"):
	#             continue
	#         elif(userInput[0]=="r"):
	#         	listRead = userInput[0].split("-")

def agHandler(argv):
	if(len(argv)==1):
		n = 5
	elif (len(argv)==2):
		n = int(argv[1])
	else:
		print("Illegal arguements detected")
		return

	# argument = str.encode(argv[0])
	# clientSocket.sendall(argument)
	# serverGroupsName = clientSocket.recv(4096)#fromServerAG.split("`")
	# decodedString = serverGroupsName.decode("utf-8")
	# discussions = decodedString.split(",")
	discussions = fromServerAG.split("`")

	userData = open(currentUserID,"r+")
	userDataRead = userData.read()
	rawSubscribedGroupList = userDataRead.split("\n")#Lists all the groups the current user is suscribed to
	subscribedGroupList = []
	unReadMessages = []
	print(rawSubscribedGroupList)
	try:
		for i in range(len(rawSubscribedGroupList)):
			groupName = rawSubscribedGroupList[i].split("`")
			subscribedGroupList.append(groupName[0])
			unReadMessages.append(groupName[1])
		print(subscribedGroupList)
	except Exception:
		print("User data is corrupted, delete file to continue")

	for i in range(1, len(discussions)+1):
		if (discussions[i-1] not in subscribedGroupList):
			print(str(((i-1)%n)+1) + "\t( )\t" + discussions[i-1])
		else:
			print(str(((i-1)%n)+1) + "\t(s)\t" + discussions[i-1])
#    if ((i+1) % n == 0 and i != 0) or i == len(postMessage) - 1:
		if (i% n == 0 and i != 1) or i == len(discussions) :
			print("Current subs group: " + str(subscribedGroupList))
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
						print(index)
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
	print(subscribedGroupList)

	userData.close() #closing file
	os.remove(currentUserID) #removing file

	newList = []############# A brave workaround ##############
	print(subscribedGroupList)
	print(unReadMessages)
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
		n = int(argv[1])
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
	print(rawSubscribedGroupList)
	try:
		for i in range(len(rawSubscribedGroupList)):
			groupName = rawSubscribedGroupList[i].split("`")
			subscribedGroupList.append(groupName[0])
			unReadMessages.append(groupName[1])
		print(subscribedGroupList)
	except Exception:
		print("User data is corrupted, delete file and restart")
	print(subscribedGroupList)
	print(unReadMessages)

	newSubscribedGroupList = []
	newUnReadMessages = []
	iterate = min(len(unReadMessages),len(subscribedGroupList))
	for i in range(iterate): #existing list from file
		newSubscribedGroupList.append(subscribedGroupList[i]) #we will delete from this list and write this list to file
		newUnReadMessages.append(unReadMessages[i])


	for i in range(1, iterate+1):
		print(str(((i-1)%n)+1) + ".\t"+unReadMessages[i-1]+"\t" + subscribedGroupList[i-1])

		if (i% n == 0 and i != 1) or i == len(subscribedGroupList)+1 :
			# print("Current subs group: " + str(subscribedGroupList))
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
	print(newSubscribedGroupList)

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