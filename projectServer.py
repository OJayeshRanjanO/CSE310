
from socket import *
import thread

#A class for the discussion groups that are formed, where the client 
#can choose to join and unjoin
class discussionGroup:
	def __init__(self, dgName):
		self.name = dgName
		self.message = []
		self.clients = []

#class for message contains the user who posted, the Time that it was posted, it's subject, and message body
class Message:
	def __init__(self, username, postTime, subject, body):
		self.username = username
		self.postTime = postTime
		self.subject = subject
		self.body = body
		self.id = uniqueMessageID

#Client classs that contains the username and connection address in order to respond to the client, and the groups the client has joined
class Client:
	def __init__(self, connection):
		self.username = ''
		self.connection = connection
		self.groups = []

#intialize the 15 groups
def init():
        g0 = discussionGroup('Group 0')
        groups.append(g0)
        g1 = discussionGroup('Group 1')
        groups.append(g1)
        g2 = discussionGroup('Group 2')
        groups.append(g2)
        g3 = discussionGroup('Group 3')
        groups.append(g3)
        g4 = discussionGroup('Group 4')
        groups.append(g4)
        g5 = discussionGroup('Group 5')
        groups.append(g5)
        g6 = discussionGroup('Group 6')
        groups.append(g6)
        g7 = discussionGroup('Group 7')
        groups.append(g7)
        g8 = discussionGroup('Group 8')
        groups.append(g8)
        g9 = discussionGroup('Group 9')
        groups.append(g9)
        g10 = discussionGroup('Group 10')
        groups.append(g10)
        g11 = discussionGroup('Group 11')
        groups.append(g11)
        g12 = discussionGroup('Group 12')
        groups.append(g12)
        g13 = discussionGroup('Group 13')
        groups.append(g13)
        g14 = discussionGroup('Group 14')
        groups.append(g14)


#Find a group that the given username is in, searches from group 0 to group i and returns the integer i indicating the groupID number
def findGroupByUserName(userName):
    i=0
    for group in groups:
        for client in group.clients:
            if client.userName == userName:
                return i
        i=i+1
    return -1


#Finds a client through the username and groupID
def findClient(username,groupID):
    for client in groups[groupID].clients:
        if client.userName==username:
            return client
    return -1

def findMessage(messageID,messageGroup):
    i=0
    for group in groups:
        for message in group.messages:
            if message.id == messageID:
                messageGroup.append(i)
                return message
        i=i+1
    messageGroup.append(-1)
    return -1















