
from Enums import *


# good stuff
# https://stackoverflow.com/questions/35988/c-like-structures-in-python

from UserPlayerTracker import UserLiveDataTracker, PlayerLiveDataTracker
######## From the InSim documentation :
# In LFS there is a list of connections AND a list of players in the race
# Some packets are related to connections, some players, some both

# If you are making a multiplayer InSim program, you must maintain two lists
# You should use the unique identifier UCID to identify a connection

# Each player has a unique identifier PLID from the moment he joins the race, until he
# leaves.  It's not possible for PLID and UCID to be the same thing, for two reasons:

# 1) there may be more than one player per connection if AI drivers are used
# 2) a player can swap between connections, in the case of a driver swap (IS_TOC)

######## The solution is to track Users and Players separately.

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
        self.connections = {}          # UserLiveDataTracker dict
        self.players = {}              # PlayerLiveDataTracker dict

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
        self.connections[ncn.UCID] = UserLiveDataTracker(ncn)


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
        self.players[npl.PLID] = PlayerLiveDataTracker(npl)

    def player_left(self, pll):
        print('Player left: {}'.format(pyinsim.stripcols(autostring(self.plid_pname_map[pll.PLID]))))
        del self.players[pll.PLID]
        del self.plid_pname_map[pll.PLID]
        del self.plid_ucid_map[pll.PLID]

    def node_lap_packet_dispatcher(self, nlp):
        self.LRD.update_state_nlp(nlp)
        for info in nlp.Info:
            self.players[info.PLID].update_node_lap(info)




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
        self.iss_state_flag = ISS_STATE_FLAGS[1] #insim_state.Flags
        self.replay_speed = insim_state.ReplaySpeed
        self.inGameCam    = insim_state.InGameCam #Which type of camera.
        self.ViewPLID     = insim_state.ViewPLID #PLID of player being viewed, 0 if none



def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)