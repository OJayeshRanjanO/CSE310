import sys
import os
import fnmatch

def main():
	# print('Number of arguments:', len(sys.argv))
	# print('Argument List:', str(sys.argv))

		argv = sys.argv
		parseArgs(argv)

def parseArgs(argv):
	if argv[1] == "login":
		loginHandler(argv)
	elif argv[1] == "ag":
		agHandler(argv)
	elif argv[1] == "sg":
		sgHandler(argv)
	elif argv[1] == "rg":
		rgHandler(argv)
	elif argv[1] == "logout":
		return



def loginHandler(argv):
	print("User ID: " + argv[2])

def rgHandler(argv):
	if(len(argv)==):
		n = 2
	elif (len(argv)==3):
		n = argv[2]
	else:
		print("Illegal arguements detected")
		return


def agHandler(argv):
	if(len(argv)==2):
		n = 3
	elif (len(argv)==3):
		n = argv[2]
	else:
		print("Illegal arguements detected")
		return

	discussions = []#Grabs the list of all discussions for current user
	for file in os.listdir('.'):
		if fnmatch.fnmatch(file, '*.txt'):
			discussions.append(file)

	#User data related to subscribed group is accessed from .txt file
	userData = 0
	try:
		userData = open("userData", 'r+')#read from existing file
	except FileNotFoundError:
		userData = open("userData", 'w+')#create new file

	userDataRead = userData.read()
	subscribedGroupList = userDataRead.split("\n")
	# print("subscribed List: "+ str(subscribedGroupList))

	for i in range(1, len(discussions)+1):
		if (discussions[i-1] not in subscribedGroupList):
			print(str(i) + "\t( )\t" + discussions[i-1])
		else:
			print(str(i) + "\t(s)\t" + discussions[i-1])

		if (i% n == 0 and i != 1) or i == len(discussions) :
			print("Current subs group: " + str(subscribedGroupList))
			userInput = input("Type:\n s to suscribe\nu to unsuscribe\nn to display next set of "+str(n) +" items\nq to quit\nChoose: ").split(" ")
			if userInput[0] == "n":
				continue
			elif userInput[0] == "q":
				break
			elif userInput[0] == "s":
				if (len(userInput) > 1):
					for j in range(1, len(userInput)):
						if discussions[int(userInput[j])-1] not in subscribedGroupList:
							subscribedGroupList.append(discussions[int(userInput[j])-1])
							print("You have successfully suscribed to: " + discussions[int(userInput[j])-1])
						else:
							print("You are already suscribed to " + discussions[int(userInput[j])-1])
				else:
					print("Not enough arguements provided")
			elif userInput[0] == "u":
				if (len(userInput) > 1):
					for j in range(1, len(userInput)):
						if discussions[int(userInput[j])-1] in subscribedGroupList:
							subscribedGroupList.remove(discussions[int(userInput[j])-1])
							print("You have successfully unsuscribed to: " + discussions[int(userInput[j])-1])
						else:
							print("You cannot unsuscribe from a group that you are not suscribed to.")
				else:
					print("Not enough arguements provided")

	print(subscribedGroupList)

	userData.close() #closing file
	os.remove("userData") #removing file
	# print("File Removed!")

	newList = []############# A brave workaround ##############
	for a in subscribedGroupList:
		if len(a) > 1:
			newList.append(a)
		else:
			print("Fuck it")#Needs to be replaced with something more decent

	userData = open("userData","w+")
	for i in range(len(newList)):
		userData.write(newList[i]+"\n")

	userData.close() #closing file

def sgHandler(argv):
	if(len(argv)==2):
		n = 2
	elif (len(argv)==3):
		n = argv[2]
	else:
		print("Illegal arguements detected")
		return

	#User data related to subscribed group is accessed from .txt file
	userData = 0
	try:
		userData = open("userData", 'r+')#read from existing file
	except FileNotFoundError:
		print("User data is empty")
		return

	userDataRead = userData.read()
	subscribedGroupList = userDataRead.split("\n")

	newSubscribedGroupList = []
	for i in subscribedGroupList: #existing list from file
		newSubscribedGroupList.append(i) #we will delete from this list and write this list to file

	for i in range(1, len(subscribedGroupList)):
		print(str(i) + ".\tRR\t" + subscribedGroupList[i-1])

		if (i% n == 0 and i != 1) or i == len(subscribedGroupList) :
			# print("Current subs group: " + str(subscribedGroupList))
			userInput = input("Type:\n s to suscribe\nu to unsuscribe\nn to display next set of "+str(n) +" items\nq to quit\nChoose: ").split(" ")
			if userInput[0] == "n":
				continue
			elif userInput[0] == "q":
				break
			elif userInput[0] == "u":
				if (len(userInput) > 1):
					for j in range(1, len(userInput)):
						if subscribedGroupList[int(userInput[j])-1] in newSubscribedGroupList:
							newSubscribedGroupList.remove(subscribedGroupList[int(userInput[j])-1])
							print("You have successfully unsuscribed to: " + subscribedGroupList[int(userInput[j])-1])
						else:
							print("You cannot unsuscribe from a group that you are not suscribed to.")
				else:
					print("Not enough arguements provided")

	print(newSubscribedGroupList)

	userData.close() #closing file
	os.remove("userData") #removing file
	# print("File Removed!")

	newList = []############# A brave workaround ##############
	for a in newSubscribedGroupList:
		if len(a) > 1:
			newList.append(a)
		else:
			print("Fuck it")#Needs to be replaced with something more decent

	userData = open("userData","w+")
	for i in range(len(newList)):
		userData.write(newList[i]+"\n")

	userData.close() #closing file


main();