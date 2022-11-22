import pyinsim
import traceback #Cause async and stuff..
import time

import CustomCallbackEvents as cce
import InSimRequests as isr


def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)


class ServerGeneralEventHandler:

    """Class to handle events sent by LFS.

    Generally, all it does, is bind an event to a method, and the method itself will then call
    a function defined elswhere (this code stays static so to say.)

    """
    def __init__(self, insim_obj, LiveServerState):

        self.LSS = LiveServerState


        self.connected = False # InSim connection OK
        self.ISO       = insim_obj #insim_object
        self.ISRH     = isr.InSimRequestsHandler(self.ISO)
        self.CBC       = cce.ServerGeneralEventCallbacks(self.ISO)
        self.bind_handlers()
        self.ISRH.initial_requests()

    def __call__(self, *args):
        print("Trying to call with args:")
        print(args)

    ######################################################################
    ########## InSim Event Handlers. This are functions to react to a packet sent by LFS.
    ########## Other functions will have to be included in them

    ########## Base Info Handlers
    #@_BIND(pyinsim.ISP_TINY)
    def _inSim_Tiny_Packet_Handler(self, insim, data):
        ReqI = data.ReqI
        SubT = data.SubT

        if SubT==pyinsim.TINY_MPE : # Multiplayer ended
            print('Host Ended')
        if SubT==pyinsim.TINY_REN : # Race ended (race setup screen)
            print('Race ended')
        if SubT==pyinsim.TINY_CLR : # All players cleared
            print('All players cleared')
        if SubT==pyinsim.TINY_AXC : # Autocross cleared
            print('AutoX layout cleared')
        if SubT==pyinsim.TINY_VTC : # Vote cancelled
            print('Vote Cancelled')

    def _inSim_Small_Packet_Handler(self, insim, data):
        ReqI = data.ReqI
        SubT = data.SubT
        UVal = data.UVal

        if SubT==pyinsim.SMALL_RTP : # Race Time packet (hundredths of a second since start of race or replay)
            print('Time since start:', UVal)
        if SubT==pyinsim.SMALL_ALC : # set or get allowed cars (TINY_ALC)
            print('Allowed Cars:', UVal)



    ########## Generic Handlers

    #@_BIND(pyinsim.EVT_INIT)
    def _inSim_Initialization_Event_Handler(self, insim):
        self.connected = True
        self.CBC.initialization_event_callback()


    #@_BIND(pyinsim.EVT_CLOSE)
    def _inSim_Closing_Event_Handler(self, insim):
        self.connected = False
        self.CBC.closing_event_callback()


    #@_BIND(pyinsim.ISP_VER)
    def _inSim_Version_Info_Handler(self, insim, data):
        print("version=",version,"\nproduct=",product,"\ninSimVer=",inSimVer)
        self.CBC.version_info_callback(data)


    #@_BIND(pyinsim.EVT_ERROR)
    def _inSim_Error_Event_Handler(self, insim):
        print('\nInSim encountered an error. Traceback:\n')
        traceback.print_exc()


    #@_BIND(pyinsim.EVT_ALL)
    def _inSim_All_Event_Handler(self, insim, packet):
        print("\nFunc all events returns :", autostring(insim))
        print('InSim Generic Event Caught : ')
        print(vars(packet))


    #@_BIND(pyinsim.EVT_OUTGAUGE)
    def _inSim_Outgauge_Event_Handler(self, insim):
        print('\nInSim Outgauge Event Catched.')
        print(autostring(insim))


    #@_BIND(pyinsim.EVT_OUTSIM)
    def _inSim_OutSim_Event_Handler(self, insim):
        print('\nOutSim Event Catched.')
        print(autostring(insim))


    #@_BIND(pyinsim.EVT_TIMEOUT)
    def _inSim_Timeout_Event_Handler(self, insim):
        print('\nTimeout Error Catched')
        print(autostring(insim))


    #@_BIND(pyinsim.ISP_STA)
    def _inSim_State_Packet_Handler(self, insim, state):
        self.LSS.update_state(state)



############## Connection Handlers

    #@_BIND(pyinsim.ISP_NCN)
    def _inSim_newConnection_handler(self, insim,  ncn):
        self.LSS.new_connection(ncn)


    #@_BIND(pyinsim.ISP_CNL)
    def _inSim_connection_left_handler(self, insim,  cnl):
        self.LSS.connection_left(cnl)


    #@_BIND(pyinsim.ISP_NPL)
    def _inSim_newPlayer_handler(self, insim,  npl):
        self.LSS.new_player(npl)


    #@_BIND(pyinsim.ISP_PLL)
    def _inSim_player_left_race_handler(self, insim,  pll):
        #PLayer Leave race (spectate - removed from player list)
        self.LSS.player_left(pll)



############## PLayer data handlers
    #@_BIND(pyinsim.ISP_CIM)
    def _inSim_Connection_Interface_Mode_Handler(self, insim, cim):
        """Connection interface mode info handler
        Gets a connections interface mode from a user
        """
        self.LSS.connections[cim.UCID].update_interface_mode(cim)


    #@_BIND(pyinsim.ISP_SLC)
    def _inSim_Car_Selected_Handler(self, insim, slc):
        self.LSS.connections[slc.UCID].update_car_selection(slc)



############## Racing Event handlers
    #@_BIND(pyinsim.ISP_LAP)
    def _inSim_Lap_Time_Handler(self, insim, lap):
        self.LSS.connections[self.LSS.plid_ucid_map[lap.PLID]].LPRD.update_lap_times(lap)

    #@_BIND(pyinsim.ISP_SPX)
    def _inSim_Split_Time_Handler(self, insim, spx):
        self.LSS.connections[self.LSS.plid_ucid_map[spx.PLID]].LPRD.update_split_times(spx)

    #@_BIND(pyinsim.ISP_PIT)
    def _inSim_Pitting_Event_Handler(self, insim, pit):
        self.LSS.connections[self.LSS.plid_ucid_map[pit.PLID]].LPRD.player_pitting(pit)

    #@_BIND(pyinsim.ISP_PSF)
    def _inSim_Pit_Finish_Handler(self, insim, psf):
        self.LSS.connections[self.LSS.plid_ucid_map[psf.PLID]].LPRD.pit_stop_finished(psf)

    #@_BIND(pyinsim.ISP_PLA)
    def _inSim_Pit_Lane_Handler(self, insim, pla):
        self.LSS.connections[self.LSS.plid_ucid_map[pla.PLID]].LPRD.player_in_pitlane(pla)

    #@_BIND(pyinsim.ISP_RES)
    def _inSim_Race_Result_Handler(self, insim, res):
        self.LSS.connections[self.LSS.plid_ucid_map[res.PLID]].LPRD.player_result(res)

    #@_BIND(pyinsim.ISP_AXO)
    def _inSim_Object_Hit_Handler(self, insim, axo):
        self.LSS.connections[self.LSS.plid_ucid_map[axo.PLID]].LPRD.player_hit_object(axo)


############## Car Tracking And Positions
    #@_BIND(pyinsim.ISP_NLP) # MAX 40 Cars are returned !!!
    def _inSim_Node_And_Lap_Packet_Handler(self, insim, nlp):
        self.LSS.node_lap_packet_dispatcher(nlp)


############## Map and layout handlers

    #@_BIND(pyinsim.ISP_AXI)
    def _inSim_AutoX_Layout_data_handler(self, insim, axi):
        self.LSS.LRD.LDH.update_state(axi)




############## Message And User Input Handlers

    #@_BIND(pyinsim.ISP_MSO)
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


    #@_BIND(pyinsim.ISP_III)
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
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ########## Binding Handlers

    def event_handler_map(self):
        event_handler_map = {"EVT_INIT" : "_inSim_Initialization_Event_Handler",
        "EVT_CLOSE" : "_inSim_Closing_Event_Handler",
        "ISP_VER" : "_inSim_Version_Info_Handler",
        "EVT_ERROR" : "_inSim_Error_Event_Handler",
        "EVT_ALL" : "_inSim_All_Event_Handler",
        "EVT_OUTGAUGE" : "_inSim_Outgauge_Event_Handler",
        "EVT_OUTSIM" : "_inSim_OutSim_Event_Handler",
        "EVT_TIMEOUT" : "_inSim_Timeout_Event_Handler",
        "ISP_STA" : "_inSim_State_Packet_Handler",
        "ISP_NCN" : "_inSim_newConnection_handler",
        "ISP_CNL" : "_inSim_connection_left_handler",
        "ISP_NPL" : "_inSim_newPlayer_handler",
        "ISP_PLL" : "_inSim_player_left_race_handler",
        "ISP_CIM" : "_inSim_Connection_Interface_Mode_Handler",
        "ISP_SLC" : "_inSim_Car_Selected_Handler",
        "ISP_LAP" : "_inSim_Lap_Time_Handler",
        "ISP_SPX" : "_inSim_Split_Time_Handler",
        "ISP_PIT" : "_inSim_Pitting_Event_Handler",
        "ISP_PSF" : "_inSim_Pit_Finish_Handler",
        "ISP_PLA" : "_inSim_Pit_Lane_Handler",
        "ISP_RES" : "_inSim_Race_Result_Handler",
        "ISP_AXO" : "_inSim_Object_Hit_Handler",
        "ISP_NLP" : "_inSim_Node_And_Lap_Packet_Handler",
        "ISP_AXI" : "_inSim_AutoX_Layout_data_handler",
        "ISP_MSO" : "_inSim_Message_Command_Out_Handler",
        "ISP_III" : "_inSim_Message_To_Host_Handler"}
        return event_handler_map

    def bind_handlers(self):
        """For binding, we just need to call all the _inSim_functions without arguments.
        """
        event_handler_map = self.event_handler_map()

        for event_str, handler_str in event_handler_map.items():
            self.ISO.bind(getattr(pyinsim,event_str), getattr(self,handler_str))

        print("bound")

    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
    ######################################################################
