import sys
import socket
import string
import thread
import traceback

class IRCError(Exception):
	pass

#contains global settings for the user
class User:
	def __init__(self,nick,realname=None):
		self.nick=nick
		self.log=None
		if realname==None:
			realname=nick
		self.realname=realname
	
	def openlog(self,filename):
		self.log=open(filename,"a")

class Channel:
	def __init__(self,name,server):
		self.name=name
		self.server=server
		self.data=[] #list of dicts

	def sendcmd(self,cmd,params=None):
		#support for the pseudo-command "ME"
		if cmd=="ME":
			cmd="PRIVMSG"
			if params!=None:
				params="\x01ACTION %s\x01"%params
		if params!=None:
			self.server.connection.send("%s %s :%s\r\n"%(cmd,self.name,params))
		else:
			self.server.connection.send("%s %s\r\n"%(cmd,self.name,params))
	
	def sendmsg(self,msg):
		self.server.connection.send("PRIVMSG %s :%s"%(self.name,msg))
	
	def get_data(self):
		ret=self.data
		self.data=[]
		return ret

class Server:
	def __init__(self,name,port=6667):
		self.name=name
		self.port=port
		self.connection=None
		self.data=""
		self.exit=False
		#global context
		self.channels={"*":Channel("*",self)}
		
	#used to handle data sent from the server
	def pingpong(self):
		try:
			while True:
				if self.exit:
					self.exit=False
					break
				buffer=self.connection.recv(1024)
				tmp=string.split(buffer,'\n')
				#get rid of trailing \r
				buffer=tmp.pop()
				for line in tmp:
					line=string.split(string.rstrip(line),' ')
					#hackerish way to avoid ill-formatted messages
					if len(line)<2:
						continue
					if line[0].upper()=="PING":
						self.connection.send("PONG %s\r\n"%line[1])
					else:
						if '!' in line[0]:
							user=line[0][1:string.find(line[0],'!')]
						else:
							user=line[0][1:]
						cmd=line[1]
						chan=line[2]
						parameters=string.join(line[3:],' ')[1:]
						#to make it easier on interface users, make a pseudo-command "me"
						if cmd=="PRIVMSG":
							cmd="MSG"
							if parameters[:len(" ACTION")].upper()=="\x01ACTION" and parameters[-1]==chr(1):
								cmd="ME"
								parameters=parameters[len(" ACTION "):-1]
						#add an unknown context to the channels
						if chan not in self.channels:
							self.channels[chan]=Channel(chan,self)
						self.channels[chan].data.append({"user":user,"cmd":cmd,"params":parameters})
		except:
			exit()
	
	def connect(self,user):
		self.connection=socket.socket()
		self.connection.connect((self.name,self.port))
		self.connection.send("NICK %s\r\n"%user.nick)
		self.connection.send("USER %s %s bla :%s\r\n"%(user.nick,self.name,user.realname))
		thread.start_new_thread(self.pingpong,())
	
	def disconnect(self):
		self.data=""
		self.exit=True
		self.connection.close()
		self.connection=None
		self.channels={}
		
	def join(self,channel):
		self.connection.send("JOIN :%s\r\n"%channel)
		self.channels[channel]=Channel(channel,self)