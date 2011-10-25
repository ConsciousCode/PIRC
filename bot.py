class Bot:
	class Module:
		def __init__(self,fname):
			mod=__import__(fname)
			#load metadata
			check_meta(mod)
			self.name=mod.metadata.name
			self.version=mod.metadata.version
			self.description=mod.metadata.description
		
		def check_meta(self,mod):
			if "metadata" not in dir(mod):
				raise NameError("Module doesn't have the required metadata class.")
			if "name" not in dir(mod.metadata):
				raise NameError("metadata.name field is not specified.")
			if "version" not in dir(mod.metadata):
				mod.metadata.version=-1
			if "description" not in dir(mod.metadata):
				mod.metadata.description=""
		
	class Service(Module):
		def __init__(self,fname):
			super(self,fname)
			if "service" not in dir(mod):
				raise NameError("Service module doesn't name a service")
			self.service=mod.service
	
	class Modifier(Moduel):
		pass
	
	def __init__(self,name,version=-1,description=""):
		self.name=name
		self.version=version
		self.description=description
		self.io={}