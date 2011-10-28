import imp

class Bot(object):
	class Module(object):
		def check_meta(self,mod):
			if "metadata" not in dir(mod):
				raise NameError("Module doesn't have the required metadata class.")
			if "name" not in dir(mod.metadata):
				raise NameError("metadata.name field is not specified.")
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
			self.name=self.mod.metadata.name
			self.version=self.mod.metadata.version
			self.description=self.mod.metadata.description
			if "action" not in dir(self.mod):
				raise NameError("Module doesn't give an action")
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
			self.services={}
			self.modifiers={}
			self.reactions={}
		
		def get_data(self):
			return self.io.get_data()
		
		def send(self,data):
			return self.io.send(data)
	
	def __init__(self,name,version="",description=""):
		self.name=name
		self.version=version
		self.description=description
		self.io=[]
		self.services=[]
		self.modifiers=[]
		self.reactions=[]
	
	def load_module(self,fname):
		mod=imp.load_source(fname)
		if mod.metadata.type=="Service":
			self.services.append(Bot.Service(mod))
		elif mod.metadata.type=="Modifier":
			self.modifiers.append(Bot.Modifer(mod))
		elif mod.metadata.type=="Reaction":
			self.reactions.append(Bot.Reaction(mod))
		else:
			raise TypeError("Invalid module type")
		if "init" in dir(mod):
			mod.init(self)
	
	def load_modules(self,directory):
		#load modules
		listing=os.listdir(cmddir)
		for f in listing:
			path=os.path.splitext(f)
			if path[1]==".py":
				self.load_module(path[0])
	
	def add_stream(self,stream):
		self.io.append(stream)
		for service in self.services:
			stream.services.update({service.name:service.active})
		for modifier in self.modifiers:
			stream.modifiers.update({modifier.name:modifier.active})
		for reaction in self.reactions:
			stream.reactions.update({reaction.name:reaction.active})
	
	def run(self):
		while True:
			out=[]
			#run through services
			for service in self.services:
				result=service.action(self)
				if result!=None:
					out.append(result)
			for io in self.io:
				data=io.get_data()
				if data==None or len(data)==0:
					continue
				for a in data:
					for reaction in self.reactions:
						result=reaction.action(self,a)
						if result!=None:
							out.append(result)
				for line in out:
					for modifier in self.modifiers:
						if modifier.active:
							line=modifier.action(self,line)
					io.send(line)