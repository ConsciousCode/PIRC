import sys
import socket
import string
import thread
import traceback

class IRCError(Exception):
	pass
	
#parse the user input for commands
def parse_input(data):
	if data=="":
		return None
	words=data.split(' ')
	if words[0][0]=='/':
		out={"command":words[0][1:].upper(),"arguments":[]}
		if len(words)>1:
			if out["command"]=="PRIVMSG":
				out["arguments"].append(words[1])
				out["arguments"].append(string.join(words[2:]))
			out["arguments"]=string.join(words[1:])
	else:
		out={"command":"MSG","arguments":[string.join(words)]}
	return out
	
#contains global settings for the user
class User(object):
	def __init__(self,nick,realname=None,quitmsg="RAGEQUIT"):
		self.nick=nick
		self.log=None
		if realname==None:
			realname=nick
		self.realname=realname
		self.quitmsg=quitmsg
	
	def openlog(self,filename):
		self.log=open(filename,"a")

class Channel(object):
	def __init__(self,name,server):
		self.name=name
		self.server=server
		self.data=[] #list of dicts
	
	def __del__(self):
		self.sendcmd("PART %s"%self.name)
	
	def leave(self):
		self.sendraw("PART %s"%self.name)

	def sendcmd(self,cmd,params=None):
		#support for the pseudo-command "ME"
		if cmd=="ME":
			cmd="PRIVMSG"
			if params!=None:
				params="\x01ACTION %s\x01"%params
		elif cmd=="MSG":
			cmd="PRIVMSG"
		elif cmd=="LEAVE":
			cmd="PART"
		elif cmd=="RAW":
			if params!=None:
				words=params.split(' ')
				cmd=words[0]
				params=string.join(words[1:])
		elif cmd=="HELP":
			self.data.append("HELP command not yet implemented")
		params=params.replace('\\r\\n','\r\n')
		params=params.replace('\\n','\r\n')
		params=params.split('\r\n')
		out=""
		for param in params:
			if ' ' in param:
				out+="%s %s :%s\r\n"%(cmd,self.name,param)
			else:
				out+="%s %s %s\r\n"%(cmd,self.name,param)		
		self.server.sendraw(out)
	
	def sendmsg(self,msg):
		self.sendcmd("MSG",msg)
	
	send=sendmsg
	
	def get_data(self):
		ret=self.data
		self.data=[]
		return ret
	
	def sendraw(self,raw):
		self.server.connection.send(raw+"\r\n")

class Server(object):
	def __init__(self,name,port=6667):
		self.name=name
		self.port=port
		self.connection=None
		self.data=""
		self.user=""
		self.exit=False
		#global context
		self.channels={"*":Channel("*",self)}
	
	def __del__(self):
		for channel in self.channels:
			self.channels[channel].leave()
		self.sendraw("QUIT %s"%(self.user.quitmsg))
		self.connection.shutdown(socket.SHUT_RD)
		
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
		except Exception as e:
			print e
			exit()
	
	def sendraw(self,raw):
		self.connection.send(raw+'\r\n')
	
	def sendcmd(self,command,params=None):
		#support for the pseudo-command "ME"
		if cmd=="ME":
			cmd="PRIVMSG"
			if params!=None:
				params="\x01ACTION %s\x01"%params
		elif cmd=="MSG":
			cmd="PRIVMSG"
		elif cmd=="LEAVE":
			cmd="PART"
		elif cmd=="RAW":
			if params!=None:
				words=params.split(' ')
				cmd=words[0]
				params=string.join(words[1:])
		elif cmd=="HELP":
			self.data.append("HELP command not yet implemented")
		params=params.replace('\\r\\n','\r\n')
		params=params.replace('\\n','\r\n')
		params=params.split('\r\n')
		out=""
		for param in params:
			if ' ' in param:
				out+="%s %s :%s\r\n"%(cmd,self.name,param)
			else:
				out+="%s %s %s\r\n"%(cmd,self.name,param)		
		self.server.sendraw(out)
	
	def connect(self,user=None):
		self.user=user
		self.connection=socket.socket()
		self.connection.connect((self.name,self.port))
		if user!=None:
			self.connection.send("NICK %s\r\n"%user.nick)
			self.connection.send("USER %s %s bla :%s\r\n"%(user.nick,self.name,user.realname))
		thread.start_new_thread(self.pingpong,())
	
	def disconnect(self):
		self.data=""
		self.exit=True
		self.connection.close()
		self.connection=None
		self.channels={}
		
	def get_data(self):
		data=[]
		for chan in self.channels:
			data.append(self.channels[chan].get_data())
		return data
	
	def join(self,channel):
		self.connection.send("JOIN :%s\r\n"%channel)
		self.channels[channel]=Channel(channel,self)