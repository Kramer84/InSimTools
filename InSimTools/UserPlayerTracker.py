class UserLiveDataTracker:
    """Class to track what a user is doing, and some of his data
    Maybe add some flags (admin etc.)
    """
    def __init__(self, ncn):
        # Connection info
        self.UCID           = ncn.UCID  # user id
        self.UName          = ncn.UName  #username
        self.isAdmin        = ncn.Admin  # 1 if true
        self.PName          = ncn.PName # nickname
        self.RemoteConnFlag = ncn.Flags

        self.CName = "" #Car selection

        self.Mode    = 0 #What the useris seeing right now
        self.SubMode = 0 #What the user sees if presses eg F9 while driving etc
        self.SelType = 0 #What the users selects if is in edition mode, 0 if nothing selected

    def update_interface_mode(self, cim):
        self.Mode     = cim.Mode
        self.SubMode  = cim.SubMode
        self.SelType  = cim.SelType

    def update_car_selection(self, slc):
        self.CName = slc.CName



class PlayerLiveDataTracker:
    """Class to track what a player is doing in a race.
    One User can theoreticaly have multiple players with AI
    """
    def __init__(self, npl):
        # General data
        self.UCID   = npl.UCID          # players UCID
        self.PLID   = npl.PLID          # player's newly assigned unique id
        self.PName  = npl.PName         # Player name / alias
        self.PType  = npl.PType         # bit 0: female / bit 1: AI / bit 2: remote
        self.Flags  = npl.Flags         # player flags
        self.Plate  = npl.Plate         # number plate - NO ZERO AT END!
        self.CName  = npl.CName         # car name
        self.SName  = npl.SName         # skin name - MAX_CAR_TEX_NAME
        self.Tyres  = npl.Tyres         # compounds
        self.H_Mass = npl.H_Mass        # added mass (kg)
        self.H_TRes = npl.H_TRes        # intake restriction
        self.Model  = npl.Model         # driver model
        self.RWAdj  = npl.RWAdj
        self.FWAdj  = npl.FWAdj
        self.Sp2    = npl.Sp2
        self.Sp3    = npl.Sp3
        self.SetF   = npl.SetF          # setup flags (see below)
        self.NumP   = npl.NumP          ## number in race - ZERO if this is a join request
        self.Config = npl.Config
        self.Fuel   = npl.Fuel
        self.Pass   = npl.Pass          # passengers byte

        print("{} with id {} is connected. Nickname : {}".format(self.UName, self.UCID, self.PName))

        # Race Data
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

    def update_car_selection(self, slc):
        self.CName = slc.CName

    def update_lap_times(self, lap):
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

    def update_node_lap(self, info):
        self.Lap = info.Lap
        self.Position = info.Position
