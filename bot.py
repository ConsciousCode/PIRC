import imp
import os
import time

class Bot(object):
	class Module(object):
		def check_meta(self,mod):
			if "version" not in dir(mod.metadata):
				mod.metadata.version=-1
			if "description" not in dir(mod.metadata):
				mod.metadata.description=""

		def __init__(self,module):
			if type(module)==str:
				self.mod=imp.load_source("",module)
			else:
				self.mod=module
			#load metadata
			self.check_meta(self.mod)
			if "active" not in dir(self.mod):
				self.mod.active=True
			self.active=self.mod.active
			self.name=self.mod.metadata.name
			self.version=self.mod.metadata.version
			self.description=self.mod.metadata.description
			self.action=self.mod.action
		
	class Service(Module):
		def __init__(self,module):
			super(Bot.Service,self).__init__(module)
	
	class Modifier(Module):
		def __init__(self,module):
			super(Bot.Modifier,self).__init__(module)
	
	class Reaction(Module):
		def __init__(self,module):
			super(Bot.Reaction,self).__init__(module)
	
	class Stream(object):
		def __init__(self,wrapped):
			self.io=wrapped
			self.types={}
		
		def get_data(self):
			return self.io.get_data()
		
		def send(self,data):
			return self.io.send(data)
	
	def __init__(self,name,version="",description=""):
		self.name=name
		self.version=version
		self.description=description
		self.io=[]
		self.types={"Service":({},Bot.Service),"Modifier":({},Bot.Modifier),"Reaction":({},Bot.Reaction)}
	
	def load_module(self,fname):
		mod=imp.load_source("",fname)
		self.types[mod.metadata.type][0].update({mod.metadata.name.lower():self.types[mod.metadata.type][1](mod)})
		if "init" in dir(mod):
			mod.init(self)
	
	def load_modules(self,directory):
		#load modules
		listing=os.listdir(directory)
		for f in listing:
			path=os.path.splitext(f)
			if path[1]==".py":
				self.load_module(directory+path[0]+path[1])
	
	def add_stream(self,stream):
		self.io.append(stream)
		stream.types=self.types
		for type in self.types:
			if type not in stream.types:
				stream.types[type]={}
				for mod in self.types[type][0]:
					stream.types[type].update({mod:self.types[type][0][mod].active})
	
	def run(self):
		while True:
			out=[]
			#run through services
			for service in self.types["Service"][0]:
				if self.types["Service"][0][service].active:
					result=self.types["Service"][0][service].action(self,io)
				if result!=None:
					out.append(result)
			for io in self.io:
				data=io.get_data()
				if data==None or len(data)==0:
					continue
				for a in data:
					for reaction in self.types["Reaction"][0]:
						result=None
						if self.types["Reaction"][0][reaction].active:
							result=self.types["Reaction"][0][reaction].action(self,io,a)
						if result!=None:
							out.append(result)
				for line in out:
					for modifier in self.types["Modifier"][0]:
						if self.types["Modifier"][0][modifier].active:
							line=self.types["Modifier"][0][modifier].action(self,io,line)
					print line
					io.send(line)
				time.sleep(1)