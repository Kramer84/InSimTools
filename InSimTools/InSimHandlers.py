import pyinsim
import traceback #Cause async and stuff..
import time

import LiveDataManager as LDM 

def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)



class ServerGeneralEventHandler:
    """Class to handle events sent by LFS.

    Generally, all it does, is bind an event to a method, and the method itself will then call 
    a function defined elswhere (this code stays static so to say.)

    """
    def __init__(self, insim_obj, callback_class, LiveServerState, LiveViewState, LiveRaceData):
        self.connections = {}
        self.players = {}

        self.LST = LiveServerState
        self.LVS = LiveViewState
        self.LRD = LiveRaceData

        self.connected = False # InSim connection OK
        self.ISO = insim_obj #insim_object
        self.CBC = callback_class
        self.bind_handlers()

    #####################################################################
    ########## Decorator for simplifying binding:
    def _CTED(self, event):
        # _callback_to_event_decorator
        def decorator(callback):
            def bind_callback_to_event():
                self.ISO.bind(event, callback)
            return bind_callback_to_event
        return decorator



    ######################################################################
    ########## InSim Event Handlers. This are functions to react to a packet sent by LFS.
    ########## Other functions will have to be included in them
    ########## Generic Handlers

    @self._CTED(pyinsim.EVT_INIT)
    def _inSim_Initialization_Event_Handler(self, insim):
        self.connected = True
        self.CBC.intialization_event_callback()

    
    @self._CTED(pyinsim.EVT_CLOSE)
    def _inSim_Closing_Event_Handler(self, insim):
        self.connected = False 
        self.CBC.closing_event_callback()

    
    @self._CTED(pyinsim.ISP_VER)
    def _inSim_Version_Info_Handler(self, insim, data):
        print("version=",version,"\nproduct=",product,"\ninSimVer=",inSimVer)
        self.CBC.version_info_callback(data)        
        
    
    @self._CTED(pyinsim.EVT_ERROR)
    def _inSim_Error_Event_Handler(self, insim):
        print('\nInSim encountered an error. Traceback:\n')
        traceback.print_exc()

    
    @self._CTED(pyinsim.EVT_ALL)
    def _inSim_All_Event_Handler(self, insim, packet):
        print("\nFunc all events returns :", autostring(insim))
        print('InSim Generic Event Caught : ')
        print(vars(packet))

    
    @self._CTED(pyinsim.EVT_OUTGAUGE)
    def _inSim_Outgauge_Event_Handler(self, insim):
        print('\nInSim Outgauge Event Catched.')
        print(autostring(insim))

    
    @self._CTED(pyinsim.EVT_OUTSIM)
    def _inSim_OutSim_Event_Handler(self, insim):
        print('\nOutSim Event Catched.')
        print(autostring(insim))

    
    @self._CTED(pyinsim.EVT_TIMEOUT)
    def _inSim_Timeout_Event_Handler(self, insim):
        print('\nTimeout Error Catched')
        print(autostring(insim))

    
    @self._CTED(pyinsim.ISP_STA)
    def _inSim_State_Packet_Handler(self, insim, state):
        self.LST.update_state(state)
        self.LVS.update_state(state)
        self.LRD.update_state(state)

    
    @self._CTED(pyinsim.ISP_MPE)
    def _inSim_Host_Ended_Handler(self, insim, ):
        # multiplayer ended
        print('Host Ended')

    @self._CTED(pyinsim.ISP_CIM)
    def _inSim_Connection_Interface_Mode_Handler(self, insim, cim):
        """Connection interface mode info handler
        Gets a connections interface mode from a user 
        """
        self.LST.connections[cim.UCID].update_interface_mode(cim)
        





############## PLayer data handlers
    
    @self._CTED(pyinsim.ISP_SLC)
    def _inSim_Car_Selected_Handler(self, insim, slc):
        self.LST.connections[slc.UCID].update_car_selection(slc)




############## Connection Handlers
    
    @self._CTED(pyinsim.ISP_NCN)
    def _inSim_newConnection_handler(self, insim,  ncn):
        self.LST.new_connection(ncn)

    
    @self._CTED(pyinsim.ISP_CNL)
    def _inSim_connection_left_handler(self, insim,  cnl):

        UCID = cnl.UCID
        reason = cnl.Reason
        total = cnl.Total

        ncn = self.connections[UCID]
        # Delete the connection from the dict.
        del self.connections[UCID]
        print('Connection left: {}'.format(autostring(ncn.UName)))

    
    @self._CTED(pyinsim.ISP_NPL)
    def _inSim_newPlayer_handler(self, insim,  npl):
        self.LST.update_player_data(npl)

    
    @self._CTED(pyinsim.ISP_PLL)
    def _inSim_player_left_race_handler(self, insim,  pll):
        #PLayer Leave race (spectate - removed from player list)
        self.LST.player_left(pll)
        print('Player left: {}'.format(pyinsim.stripcols(autostring(npl.PName)))) 


############## Racing Event handlers


############## Map and layout handlers 
    
    @self._CTED(pyinsim.ISP_AXI)
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
    
    @self._CTED(pyinsim.ISP_MSO)
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

    
    @self._CTED(pyinsim.ISP_III)
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
        """For binding, we just need to call all the _inSim_functions without arguments.
        """
        methods_and_attrs = dir(self)
        _inSim_functions = [name if name.startswith("_inSim_") for name in methods_and_attrs]
        (getattr(self, func)() for func in _inSim_functions)



if __name__=="__main__":
    print('Here we go! ')
    insim = pyinsim.insim('127.0.0.1', 58672, Admin='YourAdminPassword')
    ServerGeneralEventHandler(insim)
    pyinsim.run()