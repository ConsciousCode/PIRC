# -*- coding: utf-8 -*- 
import wx
import irc
import time
import thread
import string

class Frame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,id=wx.ID_ANY,title=u"PIRC",size=wx.Size(500,300))
		
		self.user=irc.User("Googol")
		self.irc=irc.Server("jq.dyndns-free.com")
		self.irc.connect(self.user)
		self.irc.join("#u413")
		self.channel=self.irc.channels["#u413"]
		
		thread.start_new_thread(self.get_data,())
		
		sizer=wx.BoxSizer(wx.VERTICAL)
		
		self.output=wx.TextCtrl(self,style=wx.TE_MULTILINE|wx.TE_READONLY,value="Welcome to PIRC")
		sizer.Add(self.output,1,wx.ALL|wx.EXPAND,5)
		
		self.input=wx.TextCtrl(self,wx.ID_ANY)
		sizer.Add(self.input,0,wx.ALL|wx.EXPAND,5)
		
		self.SetSizer(sizer)
		self.Layout()
		
		self.Bind(wx.EVT_SET_FOCUS,self.OnFocus)
		self.Bind(wx.EVT_CLOSE,self.OnClose)
		#self.output.Bind(wx.EVT_SET_FOCUS,self.OnFocus)
		self.input.Bind(wx.EVT_TEXT_ENTER,self.OnEnter)
		
		self.Centre(wx.BOTH)
		self.Show()
	
	def get_data(self):
		while True:
			for name in self.irc.channels:
				channel=self.irc.channels[name]
				for data in channel.get_data():
					if data["cmd"]=="MSG":
						self.output.AppendText("\r\n<%s> %s"%(data["user"],data["params"]))
					elif data["cmd"]=="ME":
						self.output.AppendText("\r\n***%s % s"%(data["user"],data["params"]))
					else:
						self.output.AppendText("\r\n%s %s %s"%(data["user"],data["cmd"],data["params"]))
			time.sleep(1)
	
	def OnFocus(self,event):
		self.input.SetFocus()
	
	def OnClose(self,event):
		self.irc.sendraw("QUIT %s"%self.user.quitmsg)
		self.irc.disconnect()
		self.Close()
		exit()
	
	def OnEnter(self,event):
		text=self.input.GetValue()
		if text!="":
			self.input.SetValue("")
			data=irc.parse_input(text)
			if data["command"]=="MSG":
				self.output.AppendText("\r\n<%s> %s"%(self.user.nick,data["arguments"][0]))
			elif data["command"]=="ME":
				self.output.AppendText("\r\n***%s %s"%(self.user.nick,data["arguments"][0]))
			self.channel.sendcmd(data["command"],string.join(data["arguments"]))
	
	def __del__(self):
		pass
	
if __name__=="__main__":
	app=wx.App(False)
	frame=Frame()
	app.MainLoop()