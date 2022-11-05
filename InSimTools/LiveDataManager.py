
from Enums import *


class LiveServerState:
    def __init__(self, insim_object):
        self.ISO      = insim_object
        self.hostName = "" #Name of the server
        self.hostPassword = "" #Not sure if needed

        self.iss_state_flag = None

        self.Track = ""
        self.weather = 0  # 0 Nice weather 1 , 2 .. etc
        self.wind = 0 

        self.layoutLoaded = -1 #-1 if no layout is loaded, else its its index in the list below
        self.layoutNames = []  # multiple layouts possible for the same track. 

        self.nConnections = 0

        self.LRD = LiveRaceData(self) #passing self, to directly acces maps
        self.LVS = LiveViewState(self)
        self.connections = {}          # LiveConnectionPlayerData dict

        self.plid_ucid_map = {}   # player id user id maping as some events only return PLID
        self.ucid_uname_map = {}  # user id user name mapping # for printing messages
        self.plid_pname_map = {}  # player id player name mapping # for printing messages

    def update_state(self, insim_state):
        self.serverStatus               = insim_state.Spare3 # 0 = unknown / 1 = success / > 1 = fail
        self.nConnections               = insim_state.NumConns
        self.Track                      = insim_state.Track
        self.weather                    = insim_state.Weather
        self.wind                       = insim_state.Wind 
        print(insim_state.Flags)
        self.iss_state_flag             = ISS_STATE_FLAGS[1]

        self.LRD.update_state(insim_state)
        self.LVS.update_state(insim_state)


    def new_connection(self, ncn):
        self.nConnections = ncn.Total
        self.ucid_uname_map[ncn.UCID] = ncn.UName
        lcpd = LiveConnectionPlayerData(ncn, self)
        self.connections[ncn.UCID] = lcpd

    def connection_left(self, cnl):
        self.nConnections = cnl.Total

        print('Connection left: {}'.format(autostring(self.ucid_uname_map[cnl.UCID])))
        
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_DISCO":      # 0 - none 
            pass # do something ? 
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_TIMEOUT":         # 1 - timed out
            pass # do something ? 
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_LOSTCONN":        # 2 - lost connection
            pass # do something ? 
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_KICKED":         # 3 - kicked
            pass # do something ? 
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_BANNED":         # 4 - banned
            pass # do something ? 
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_SECURITY":         # 5 - security
            pass # do something ? 
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_CPW":        # 6 - cheat protection wrong
            pass # do something ? 
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_OOS":        # 7 - out of sync with host
            pass # do something ? 
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_JOOS":       # 8 - join OOS (initial sync failed)
            pass # do something ? 
        if DISCONNECT_REASONS[cnl.Reason] == "LEAVR_HACK":       # 9 - invalid packet
            pass # do something ?     

        # Cleaning up, if necessary. 
        if cnl.UCID in list(plid_ucid_map.values()) :
            PLID = list(plid_ucid_map.keys())[list(plid_ucid_map.values()).index(cnl.UCID)]
            if PLID in list(plid_pname_map.keys()):
                del plid_pname_map[PLID]

        del self.ucid_uname_map[cnl.UCID]
        # Maybe saving here something? TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        del self.connections[cnl.UCID]

    def new_player(self, npl):
        assert npl.UCID in self.connections.keys(), "Some problem here? UCID not in connections."
        self.plid_ucid_map[npl.PLID] = npl.UCID
        self.plid_pname_map[npl.PLID] = npl.PName
        self.connections[npl.UCID].player_entered_race(npl)

    def player_left(self, pll):
        UCID = self.plid_ucid_map[pll.PLID]
        print('Player left: {}'.format(pyinsim.stripcols(autostring(self.plid_pname_map[pll.PLID])))) 
        self.connections[UCID].player_left_race(pll)
        del self.plid_pname_map[pll.PLID]
        del self.plid_ucid_map[pll.PLID]

    def node_lap_packet_dispatcher(self, nlp):
        self.LRD.update_state_nlp(nlp)
        for nl in nlp:
            self.connections[self.plid_ucid_map[nlp.PLID]].LPRD.update_node_lap(nlp)

class LiveConnectionPlayerData:
    """Data for one player ? 
    """
    def __init__(self, ncn, liveServerState):        
        # Connection info  
        self.LSS            = liveServerState
        self.UCID           = ncn.UCID  # user id
        self.UName          = ncn.UName  #username  
        self.isAdmin        = ncn.Admin  # 1 if true 
        self.PName          = ncn.PName # nickname
        self.RemoteConnFlag = ncn.Flags

        self.Mode    = 0 #What the useris seeing right now
        self.SubMode = 0 #What the user sees if presses eg F9 while driving etc
        self.SelType = 0 #What the users selects if is in edition mode, 0 if nothing selected

        self.LPRD = LivePlayerRaceData(self.LSS, self)

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
        print(self)

    def __repr__(self):
        return "{} with id {} is connected. Nickname : {}".format(self.UName, self.UCID, self.PName)

    def player_entered_race(self, npl):
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

    def update_interface_mode(self, cim): 
        self.Mode     = cim.Mode
        self.SubMode = cim.SubMode
        self.SelType          = cim.SelType

    def update_car_selection(self, slc):
        self.CName = slc.CName




class LivePlayerRaceData:
    """Class managing the various laps/ times of a player
    """ 
    def __init__(self, liveServerState, liveConnectionPlayerData):
        self.LSS = liveServerState #Object
        self.LCPD = liveConnectionPlayerData #Object

        self.UCID = self.LCPD.UCID # Constant :/ 

        self.BTime = 0

        self.LTimes = []
        self.STimesCur = []
        self.STimesTT = [] # 2D list

        self.Lap = 0 #Current lap
        self.Position = 0 
 
        self.LapsDone = 0
        self.Flags = 0  # Blue / Yellow ...
        self.TTime = 0
        self.Penalty = 0
        self.NumStops = 0
        self.Fuel = 0

        self.ResultNum = 0 # Quali or Finish position
        self.PSeconds = 0 # Penalty in s

    def update_LTimes(self, lap):
        self.LTimes.append(lap.LTime)
        self.STimesTT.append(self.STimesCur)
        self.STimesCur = []
        self.Flags = lap.Flags 
        self.Penalty = lap.Penalty 
        self.Fuel = lap.Fuel/2

        self.TTime = lap.ETime
        self.LapsDone = lap.LapsDone 
        self.NumStops = lap.NumStops

    def update_split_times(self, spx):
        self.STimesCur.append(STime)
        self.Penalty = spx.Penalty 
        self.Fuel = spx.Fuel/2

        self.TTime = spx.ETime
        self.NumStops = spx.NumStops

    def player_pitting(self, pit):
        self.Penalty = pit.Penalty 
        self.Flags = pit.Flags 
        
        FuelAdd = pit.FuelAdd/2
        Tyres = pit.Tyres
        Work = pit.Work

        self.TTime = pit.ETime
        self.LapsDone = pit.LapsDone 
        self.NumStops = pit.NumStops

    def pit_stop_finished(self, psf):
        STime = psf.STime

    def player_in_pitlane(self, pla):
        # Do some stuff... 
        if PIT_LANE_FACTS[pla.fact] == "PITLANE_EXIT":
            pass
        if PIT_LANE_FACTS[pla.fact] == "PITLANE_ENTER":
            pass
        if PIT_LANE_FACTS[pla.fact] == "PITLANE_NO_PURPOSE":
            pass
        if PIT_LANE_FACTS[pla.fact] == "PITLANE_DT":
            pass
        if PIT_LANE_FACTS[pla.fact] == "PITLANE_SG":
            pass
        if PIT_LANE_FACTS[pla.fact] == "PITLANE_NUM":
            pass

    def player_result(self, res):
        self.TTime = res.TTime
        self.BTime = res.BTime 
        self.NumStops = res.NumStops
        self.Confirm = res.Confirm # Confirmation flag
        self.LapsDone = res.LapsDone
        self.ResFlags = res.Flags 
        self.ResultNum = res.ResultNum
        self.PSeconds  = res.PSeconds

    def player_hit_object(self, axo):
        pass #Do stuff ? 

    def update_node_lap(self, nlp):
        self.Lap = nlp.Lap 
        self.Position = nlp.Position


class LiveRaceData:
    """Class managing the race in general. 

    """
    def __init__(self, LiveServerState):
        self.LSS = LiveServerState

        self.Track = self.LSS.Track
        self.LDH = LayoutDataHandling(self.Track)

        ## Live Race Data / General Data
        self.players = {}  # PLID : LivePlayerData()
        self.nPlayers = 0
        self.raceInProg = 0 # 0 = no race / 1 = race / 2 = qualifying
        self.NumFinished = 0

        ## Settings for quali time, and race ength
        self.QualMins = 1 
        self.RaceLaps = -1  #Negative if not defined / used
        self.RaceHours = -1  #Negative if not defined

    def update_state(self, insim_state):
        self.Track        = insim_state.Track
        self.nPlayers     = insim_state.NumP
        self.raceInProg   = insim_state.RaceInProg 
        self.QualMins     = insim_state.QualMins 
        self.RaceLaps,self.RaceHours = self.get_race_laps_meaning(insim_state.RaceLaps) 
        self.NumFinished  = insim_state.NumFinished 

    def update_state_nlp(self, nlp):
        self.nPlayers = nlp.NumP

    def get_race_laps_meaning(self, RaceLaps):
        if RaceLaps==0: #practice
            return 0, -1
        if 0<RaceLaps<100:
            return RaceLaps, -1
        if 99<RaceLaps<191:
            return (RaceLaps-100)*10+100, -1
        if 190<RaceLaps<239:
            return -1, RaceLaps-190


class LayoutDataHandling:
    """Class for storing layout data,
    storing info, paths etc.
    """
    def __init__(self, Track):
        self.Track = Track
        self.Size = None
        self.Type = None
        self.ReqI = None
        self.Zero = None
        self.AXStart = None
        self.NumCP = None
        self.NumO = None
        self.LName = None

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
    # Class for storing thing about the hosts? view,
    # or replays etc, whats happening,
    # who we're viewing etc. 
    def __init__(self, liveServerState):
        self.LSS = liveServerState
        self.iss_state_flag = None
        self.replay_speed = 1.0 #1.0 if normal
        self.inGameCam    = None #Which type of camera. 
        self.ViewPLID     = None #PLID of player being viewed, 0 if none

    def update_state(self, insim_state):
        self.iss_state_flag = ISS_STATE_FLAGS[insim_state.Flags]
        self.replay_speed = insim_state.ReplaySpeed
        self.inGameCam    = insim_state.InGameCam #Which type of camera. 
        self.ViewPLID     = insim_state.ViewPLID #PLID of player being viewed, 0 if none



def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)