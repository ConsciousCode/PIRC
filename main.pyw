import wx

class window(wx.Frame):
	def __init__(self):
		super(None,-1,"PIRC")

if __name__=="__main__":
	app=wx.App()
	mainwin=window()