from socket import *
import datetime
import thread

port = 3400
#groups[] holds objects in a list that hold the name of the group
#the clients in the group, and the messages in the group
groups = []

#Initial group map to map group names to their associated index in the group array
groupMap = {'Group.0'.strip():0,'Group.1'.strip():1,'Group.2'.strip():2,'Group.3'.strip():3,'Group.4'.strip():4,'Group.5'.strip():5,'Group.6'.strip():6,'Group.7'.strip():7,'Group.8'.strip():8,'Group.9'.strip():9,'Group.10'.strip():10,'Group.11'.strip():11,'Group.12'.strip():12,'Group.13'.strip():13,'Group.14'.strip():14,}


#global messageID counter to keep track of all messages added to the group
messageCounter = 0
class Message:
    def __init__(self,userName,postDate,subject,body):
        self.userName = userName
        self.postDate = postDate
        self.subject = subject
        self.body = body
FirstPost = Message("Admin(Client Developer) Jayesh","Jan 01 01:01:01","Welcome","\tParagraph1:First Line\nSecond Line\n\n\tParagraph2:First Line\nSecond Line")
SecondPost = Message("Admin(Server Developer) Patrick","Jan 01 01:01:01","To","\tParagraph1:First Line\nSecond Line\n\n\tParagraph2:First Line\nSecond Line")
ThirdPost = Message("Admin(QA) Christian","Jan 01 01:01:01","Group","\tParagraph1:First Line\nSecond Line\n\n\tParagraph2:First Line\nSecond Line")
FourthPost = Message("Admin(QA) Alexandria","Jan 01 01:01:01","34","\tParagraph1:First Line\nSecond Line\n\n\tParagraph2:First Line\nSecond Line")
class discussionGroup:
    def __init__(self, dgName):
        self.name = dgName
        self.message = [FirstPost,SecondPost,ThirdPost,FourthPost]
        
def init():
        g0 = discussionGroup('Group.0')
        groups.append(g0)
        g1 = discussionGroup('Group.1')
        groups.append(g1)
        g2 = discussionGroup('Group.2')
        groups.append(g2)
        g3 = discussionGroup('Group.3')
        groups.append(g3)
        g4 = discussionGroup('Group.4')
        groups.append(g4)
        g5 = discussionGroup('Group.5')
        groups.append(g5)
        g6 = discussionGroup('Group.6')
        groups.append(g6)
        g7 = discussionGroup('Group.7')
        groups.append(g7)
        g8 = discussionGroup('Group.8')
        groups.append(g8)
        g9 = discussionGroup('Group.9')
        groups.append(g9)
        g10 = discussionGroup('Group.10')
        groups.append(g10)
        g11 = discussionGroup('Group.11')
        groups.append(g11)
        g12 = discussionGroup('Group.12')
        groups.append(g12)
        g13 = discussionGroup('Group.13')
        groups.append(g13)
        g14 = discussionGroup('Group.14')
        groups.append(g14)

def handler(connectionSocket, addr):
    global messageCounter
    global groups
    while 1:
        request = connectionSocket.recv(4096)
        request = request.decode()
        print(request)

        inputCommand = request.split("`")
        if inputCommand[0] == "ag":
            print("you reached command ag")
            connectionSocket.send("Group.0,Group.1,Group.2,Group.3,Group.4,Group.5,Group.6,Group.7,Group.8,Group.9,Group.10,Group.11,Group.12,Group.13,Group.14")
            # messageSubject = str(groups[1].message[0].subject)
            # connectionSocket.send(messageSubject)
        elif inputCommand[0] == "sg":
            print("you reached command sg")
            toSend = ""
            for i in range(1,len(inputCommand)):
                if(len(inputCommand[i]) > 0):
                    newNumber = str(len(groups[groupMap[str(inputCommand[i])]].message))
                    toSend = toSend + "`" + newNumber
            connectionSocket.send(toSend)

        elif inputCommand[0] == "rg":
            groupID = groupMap[str(inputCommand[1])]
            dates = ""
            subjects = ""
            for i in range(len(groups[groupID].message)):
                dates = dates + "`" +str(groups[groupID].message[i].postDate)
                subjects = subjects + "`" + str(groups[groupID].message[i].subject)
            connectionSocket.send(dates)
            connectionSocket.send(subjects)

        #client wants to read a post
        elif inputCommand[0] == "id":
            groupName = str(inputCommand[1])
            groupID = groupMap[groupName]
            messageID = int(inputCommand[2])
            displayDate = str(groups[groupID].message[messageID].postDate)
            displaySubject = str(groups[groupID].message[messageID].subject)
            displayAuthor = str(groups[groupID].message[messageID].userName)
            displayContent = str(groups[groupID].message[messageID].body)
            connectionSocket.send(displayDate + "`" + displaySubject + "`" + displayAuthor + "`" + displayContent)

        elif inputCommand[0] == "p":
            postUsername = str(inputCommand[1])
            # print("Author: " + postUsername)
            postGroup = str(inputCommand[2])
            # print("Group: " + postGroup)
            postSubject = str(inputCommand[3])
            # print("Subject: " + postSubject)
            postContent = str(inputCommand[4])
            # print("Content: " + postContent)
            now = datetime.datetime.now()
            months =["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            postTime = str(months[int(now.month)-1]) + " " + str(now.day) + " " + str(now.hour)+":"+str(now.minute)+":"+str(now.second)
            # print("Time: " + postTime)
            groupID = groupMap[postGroup]
            messagePost = Message(postUsername,postTime,postSubject,postContent)
            groups[groupID].message.insert(0,messagePost)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("", port))
serverSocket.listen(1)

init()

print "\nStarted listening on port " + str(port) + "\n"
while True:
    connectionSocket, addr = serverSocket.accept()
    print "accepted connection and client added"

    #start a new thread for the user
    thread.start_new_thread(handler, (connectionSocket, addr))

