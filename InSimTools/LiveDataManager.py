
from Enums import *


class LiveServerState:
    def __init__(self, insim_object):
        self.ISO      = insim_object
        self.hostName = "" #Name of the server
        self.hostPassword = "" #Not sure if needed

        self.iss_state_flag = None

        self.track = ""
        self.weather = 0  # 0 Nice weather 1 , 2 .. etc

        self.layoutLoaded = -1 #-1 if no layout is loaded, else its its index in the list below
        self.layoutNames = []  # multiple layouts possible for the same track. 

        self.nConnections = 0


        self.connections = {}
        self.plid_ucid_map = {} #player id user id maping as some events only return PLID

    def update_state(self, insim_state):
        self.serverStatus               = insim_state.ServerStatus # 0 = unknown / 1 = success / > 1 = fail
        self.nConnections               = insim_state.NumConns
        self.track                      = insim_state.Track
        self.weather                    = insim_state.Weather
        self.wind                       = insim_state.Wind 

        self.iss_state_flag             = ISS_STATE_FLAGS[insim_state.Flags]

    def new_connection(self, ncn):
        self.nConnections = ncn.Total
        LCPD = LiveConnectionPlayerData(ncn)
        self.connections[LCPD.UCID] = LCPD

    def new_player(self, npl):
        assert npl.UCID in self.connections.keys(), "Some problem here? UCID not in connections."
        self.plid_ucid_map[npl.PLID] = npl.UCID
        self.connections[npl.UCID].update_player_data(npl)

    def player_left(self, pll):
        UCID = self.plid_ucid_map[pll.PLID]
        self.connections[UCID].player_left_race(pll)
        del self.plid_ucid_map[pll.PLID]


class LiveConnectionPlayerData:
    """Data for one player ? 
    """
    def __init__(self, ncn):
        # Connection info  
        self.UCID    = ncn.UCID  # user id
        self.UName   = ncn.UName  #username  
        self.isAdmin = ncn.Admin  # 1 if true 
        self.PName   = ncn.Admin # nickname
        self.RemoteConnFlag = ncn.Flags


        self.connection_interface_mode = 0 #What the useris seeing right now
        self.connection_interface_submodes = 0 #What the user sees if presses eg F9 while driving etc
        self.selected_object_type = 0 #What the users selects if is in edition mode, 0 if nothing selected

        self.PLID   = None # player's newly assigned unique id
        self.PType  = None # bit 0: female / bit 1: AI / bit 2: remote
        self.Flags  = None # player flags
        self.Plate  = None # number plate - NO ZERO AT END!
        self.CName  = None # car name
        self.SName  = None # skin name - MAX_CAR_TEX_NAME
        self.Tyres  = None # compounds
        self.H_Mass = None # added mass (kg)
        self.H_TRes = None # intake restriction
        self.Model  = None # driver model
        self.Pass   = None # passengers byte
        self.SetF   = None # setup flags (see below)
        self.NumP   = None # number in race - ZERO if this is a join request

    def update_player_data(self, npl):
        self.PLID   = npl.PLID
        self.PType  = npl.PType
        self.Flags  = npl.Flags
        self.Plate  = npl.Plate
        self.CName  = npl.CName
        self.SName  = npl.SName
        self.Tyres  = npl.Tyres
        self.H_Mass = npl.H_Mass
        self.H_TRes = npl.H_TRes
        self.Model  = npl.Model
        self.Pass   = npl.Pass
        self.SetF   = npl.SetF
        self.NumP   = npl.NumP

    def player_left_race(self, pll):
        
        self.PLID,self.PType,self.Flags,self.Plate           = None
        self.CName,self.SName,self.Tyres,self.H_Mass         = None
        self.H_TRes,self.Model,self.Pass,self.SetF,self.NumP = None


    def update_car_selection(self, slc):
        self.CName = slc.CName

    def update_interface_mode(self, cim): 
        self.connection_interface_mode  = cim.Mode
        self.connection_interface_submodes = cim.SubMode
        self.selected_object_type = cim.SelType


class LiveRaceData:
    """Class managing the race in general. 

    """
    def __init__(self, insim_object):
        self.ISO = insim_object
        self.iss_state_flag = None

        ## Live Race Data / General Data
        self.players = {}  # PLID : LivePlayerData()
        self.nPlayers = 0
        self.raceInProg = 0 # 0 = no race / 1 = race / 2 = qualifying
        self.NumFinished = 0



        ## Settings for quali time, and race ength
        self.QualMins = 1 
        self.RaceLaps = -1  #Negative if not defined / used
        self.RaceHours = -1  #Negative if not defined

"""RaceLaps (rl): (various meanings depending on range)
    0       : practice
    1-99    : number of laps...   laps  = rl
    100-190 : 100 to 1000 laps... laps  = (rl - 100) * 10 + 100
    191-238 : 1 to 48 hours...    hours = rl - 190"""

    def update_state(self, insim_state):
        self.nPlayers     = insim_state.NumP
        self.raceInProg   = insim_state.RaceInProg 
        self.QualMins     = insim_state.QualMins 
        self.RaceLaps     = insim_state.RaceLaps 
        self.NumFinished  = insim_state.NumFinished 



class LivePlayerRaceData:
    """Class managing the various laps/ times of a player
    """ 
    def __init__(self, insim_object):
        self.best_time = 0
        self.best_split = []

        self.lap_times = []
        self.cur_lap_split_times = []
        self.split_times = [] # 2D list

        self.nLapsDone = 0
        self.player_flags = 0  # Blue / Yellow ...
        self.total_race_time = 0
        self.cur_penalty = 0
        self.num_pit_stops = 0
        self.fuel = 0

    def update_lap_times(self, lap):
        self.lap_times.append(lap.LTime)
        self.split_times.append(self.cur_lap_split_times)
        self.cur_lap_split_times = []






class LayoutDataHandling:
    """Class for storing layout data,
    storing info, paths etc.
    """
    def __init__(self):
        self.Size = None
        self.Type = None
        self.ReqI = None
        self.Zero = None
        self.AXStart = None
        self.NumCP = None
        self.NumO = None
        self.Name = None

    def update_state(self, axi):
        self.Size = axi.Size
        self.Type = axi.Type
        self.ReqI = axi.ReqI
        self.Zero = axi.Zero
        self.AXStart = axi.AXStart
        self.NumCP = axi.NumCP
        self.NumO = axi.NumO
        self.LName = axi.LName        



class LiveViewState:
    # Class for storing thing about the actual view,
    # or replays etc, whats happening,
    # who we're viewing etc. 
    def __init__(self, insim_object):
        self.ISO = insim_object
        self.iss_state_flag = None
        self.replay_speed = 1.0 #1.0 if normal
        self.inGameCam    = None #Which type of camera. 
        self.ViewPLID     = None #PLID of player being viewed, 0 if none

    def update_state(self, insim_state):
        self.iss_state_flag = ISS_STATE_FLAGS[insim_state.Flags]
        self.replay_speed = insim_state.ReplaySpeed
        self.inGameCam    = insim_state.InGameCam #Which type of camera. 
        self.ViewPLID     = insim_state.ViewPLID #PLID of player being viewed, 0 if none