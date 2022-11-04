


class LiveServerState:
	def __init__(self):
		self.hostName = "" #Name of the server
		self.hostPassword = "" #Not sure if needed

		self.trackChosen = ""
		self.Weather = 0  # 0 Nice weather 1 , 2 .. etc

		self.layoutLoaded = -1 #-1 if no layout is loaded, else its its index in the liost below
		self.layoutNames = []  # multiple layouts possible for the same track. 

		self.N_Connections = 0
		self.N_Players = 0 
		





class LiveRaceData:
	def __init__(self):
		pass

class LivePlayerData:
	"""Data for one player ? 
	"""
	def __init__(self):
		pass
