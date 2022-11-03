import pyinsim
import traceback #Cause async and stuff..
import time


def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)


class ServerGeneralEventHandler:
    """Class to manage the server state.

    - Server data / options
    - Connections / Players
    - Message handling / chat
    - Map data 
    - Error Handling   

    For each handler function, if a specific action is required, a function has to be defined. 
    """
    def __init__(self, insim_obj):
        self.conections = {}
        self.players = {}

        self.ISO = insim_obj #insim_object
        self.bind_handlers()

    

    ######################################################################
    ########## InSim Event Handlers. This are functions to react to a packet sent by LFS.
    ########## Other functions will have to be included in them
    ########## Generic Handlers
    def _inSim_Initialization_Event_Handler(self, insim):
        print('\nInSim initialized')
        print(autostring(insim))

    def _inSim_Closing_Event_Handler(self, insim):
        print('\nInSim connection closed')
        print(autostring(insim))

    def _inSim_Error_Event_Handler(self, insim):
        print('\nInSim encountered an error. Traceback:\n')
        traceback.print_exc()

    def _inSim_All_Event_Handler(self, insim, packet):
        print("\nFunc all events returns :", autostring(insim))
        print('InSim Event Caught.')
        print(vars(packet))

    def _inSim_Outgauge_Event_Handler(self, insim):
        print('\nInSim Outgauge Event Catched.')
        print(autostring(insim))

    def _inSim_OutSim_Event_Handler(self, insim):
        print('\nOutSim Event Catched.')
        print(autostring(insim))

    def _inSim_Timeout_Event_Handler(self, insim):
        print('\nTimeout Error Catched')
        print(autostring(insim))

    def _inSim_State_Packet_Handler(self, insim, state):
        print('\nGot state packet!')
        Type = state.Type
        Zero = state.Zero
        ReplaySpeed = state.ReplaySpeed
        Flags = state.Flags
        InGameCam = state.InGameCam
        ViewPLID = state.ViewPLID
        NumP = state.NumP
        NumConns = state.NumConns
        NumFinished = state.NumFinished
        RaceInProg = state.RaceInProg
        QualMins = state.QualMins
        RaceLaps = state.RaceLaps
        Track = state.Track
        Weather = state.Weather
        Wind = state.Wind 
        print("\tZero:", Zero,
              "\tReplaySpeed:", ReplaySpeed,
              "\tFlags:", Flags,
              "\tInGameCam:", InGameCam,
              "\tViewPLID:", ViewPLID,
              "\tNumP:", NumP,
              "\tNumConns:", NumConns,
              "\tNumFinished:", NumFinished,
              "\tRaceInProg:", RaceInProg,
              "\tQualMins:", QualMins,
              "\tRaceLaps:", RaceLaps,
              "\tTrack:", Track,
              "\tWeather:", Weather,
              "\tWind:", Wind)


############## Connection Handlers
    def _inSim_newConnection_handler(self, insim,  ncn):

        UCID = ncn.UCID
        UName = ncn.UName
        PName = ncn.PName
        Admin = ncn.Admin
        Total = ncn.Total
        Flags = ncn.Flags
        print('New connection: {}'.format(autostring(ncn.UName)))
        self.connections[UCID]= ncn

    def _inSim_connection_left_handler(self, insim,  cnl):

        UCID = cnl.UCID
        reason = cnl.Reason
        total = cnl.Total

        ncn = self.connections[UCID]
        # Delete the connection from the dict.
        del self.connections[UCID]
        print('Connection left: {}'.format(autostring(ncn.UName)))

    def _inSim_newPlayer_handler(self, insim,  npl):

        PLID = npl.PLID
        UCID = npl.UCID
        PType = npl.PType
        Flags = npl.Flags
        PName = npl.PName
        Plate = npl.Plate
        CName = npl.CName
        SName = npl.SName
        Tyres = npl.Tyres 
        H_Mass = npl.H_Mass
        H_TRes = npl.H_TRes
        Model = npl.Model
        Pass = npl.Pass
        Spare = npl.Spare
        SetF = npl.SetF
        NumP = npl.NumP
        print('New player: {}'.format(pyinsim.stripcols(autostring(npl.PName))))
        self.players[UCID]= npl

    def _inSim_player_left_handler(self, insim,  pll):

        PLID = pll.PLID
        # Get player from the players dict.
        npl = self.players[pll.PLID]
        # Delete them from the dict.
        del self.players[pll.PLID]
        print('Player left: {}'.format(pyinsim.stripcols(autostring(npl.PName)))) 

############## Map and layout handlers 
    def _inSim_AutoX_Layout_data_handler(self, insim, axi):
        Size = axi.Size
        Type = axi.Type
        ReqI = axi.ReqI
        Zero = axi.Zero
        AXStart = axi.AXStart
        NumCP = axi.NumCP
        NumO = axi.NumO
        LName = axi.LName
        print("Layout handler activated")
        print("\tSize:",Size,"\tType:",Type,"\tReqI:",ReqI,"\tZero:",Zero,"\tAXStart:",AXStart,"\tNumCP:",NumCP,"\tNumO:",NumO,"\tLName:",LName,)

############## Message And User Input Handlers
    def _inSim_Message_Command_Out_Handler(self,insim, mso):
        """MSg Out - system messages and user messages
        Args :
            mso : pyinsim.IS_MSO object
        """
        msg = autostring(mso.Msg)
        ucid = mso.UCID
        plid = mso.PLID
        user_type = mso.UserType

        print("Connection",ucid,"With ID", plid, "and type", user_type, "said:")
        print(msg)

    def _inSim_Message_To_Host_Handler(self,insim, iii):
        """InsIm Info - /i message from user to host's InSim
        Args :
            iii : pyinsim.IS_III object
        """
        msg = autostring(iii.Msg)
        ucid = iii.UCID
        plid = iii.PLID
        user_type = iii.UserType

        print("Connection",ucid,"With ID", plid, "and type", user_type, "sent to host:")
        print(msg)





    ######################################################################
    ########## Binding Handlers

    def bind_handlers(self):
        ## Generic Handlers
        self.ISO.bind(pyinsim.EVT_INIT,     self._inSim_Initialization_Event_Handler)
        self.ISO.bind(pyinsim.EVT_CLOSE,    self._inSim_Closing_Event_Handler)
        self.ISO.bind(pyinsim.EVT_ERROR,    self._inSim_Error_Event_Handler)
        self.ISO.bind(pyinsim.EVT_ALL,      self._inSim_All_Event_Handler)
        self.ISO.bind(pyinsim.EVT_OUTGAUGE, self._inSim_Outgauge_Event_Handler)
        self.ISO.bind(pyinsim.EVT_OUTSIM,   self._inSim_OutSim_Event_Handler)
        self.ISO.bind(pyinsim.EVT_TIMEOUT,  self._inSim_Timeout_Event_Handler)
        self.ISO.bind(pyinsim.ISP_STA,      self._inSim_State_Packet_Handler)

        ## Map and layout handlers
        self.ISO.bind(pyinsim.ISP_AXI,      self._inSim_AutoX_Layout_data_handler)

        ## Connection Handlers 
        self.ISO.bind(pyinsim.ISP_NCN,      self._inSim_newConnection_handler)
        self.ISO.bind(pyinsim.ISP_CNL,      self._inSim_connection_left_handler)
        self.ISO.bind(pyinsim.ISP_NPL,      self._inSim_newPlayer_handler)
        self.ISO.bind(pyinsim.ISP_PLL,      self._inSim_player_left_handler)

        ## Input  Handlers
        self.ISO.bind(pyinsim.ISP_MSO,      self._inSim_Message_Command_Out_Handler)
        self.ISO.bind(pyinsim.ISP_III,      self._inSim_Message_To_Host_Handler)


if __name__=="__main__":
    print('Here we go! ')
    insim = pyinsim.insim('127.0.0.1', 58672, Admin='YourAdminPassword')
    ServerGeneralEventHandler(insim)
    pyinsim.run()