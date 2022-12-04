import pyinsim
import traceback #Cause async and stuff..
import time

import CustomCallbackEvents as cce
import InSimRequests as isr
import Enums


def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)


class ServerGeneralEventHandler(isr.InSimRequestsHandler):

    """Class to handle events sent by LFS.

    Generally, all it does, is bind an event to a method, and the method itself will then call
    a function defined elswhere (this code stays static so to say.) OR :
    -> Rather create a new class inheriting from this one, and overwrite the methods you need,
    so you still have an image of all the drivers / track etc. at all time.

    You have a flag to diasable the server state tracking if it is really not needed.

    When you override a function, always use super().old_method() to call the old method beforehand,
    this will make sure that the server state will still be updated.

    As it has inherited from the requests handler, you have access to all possible requests from here too.

    """
    def __init__(self, insim_obj, LiveServerState, update_lss=True):

        super().__init__(insim_obj)

        self.LSS        = LiveServerState
        self.update_lss = update_lss
        self.connected  = False # InSim connection OK
        self.ISO        = insim_obj #insim_object
        self.bind_handlers()
        self.CBC        = cce.ServerGeneralEventCallbacks(self.ISO)

    def __call__(self, *args):
        print("Trying to call with args:")
        print(args)

    ######################################################################
    ########## InSim Event Handlers. This are functions to react to a packet sent by LFS.
    ########## Other functions will have to be included in them

    ########## Base Info Handlers
    def _inSim_Tiny_Packet_Handler(self, insim, data): # pyinsim.ISP_TINY
        ReqI = data.ReqI
        SubT = data.SubT

        if SubT==pyinsim.TINY_NONE : # (keep alive packet)
            self.send_keep_alive_packet() # Must reply with tiny None to keep alive
        if SubT==pyinsim.TINY_REPLY : # response to request_if_connection_up
            self.send_keep_alive_packet()
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
        if SubT==pyinsim.SMALL_VTA : # handle vote action, can be canceled, forced immidatly etc.
            # self.set_race_order can only be called after this has been received!
            print('Vote action :' Enums.VOTE_ACTIONS[UVal])




    ########## Button Event Handlers
    def _inSim_Button_Function_Event_Handler(self, insim, data):
        """Button function event reception handler.
            ReqI     : 0
            SubT     : subtype, from ``BFN_*`` enumeration
            UCID     : connection sent from (0 = local / 255 = all)
            ClickID  : ID of button to delete (if ``SubT`` is ``BFN_DEL_BTN``)
            MaxClick : ID of last button to delete in range of buttons
            Inst     : used internally by InSim

            IS_BFN subtype :
                BFN_DEL_BTN, BFN_CLEAR //  0,1 - instructions , not handled here
                BFN_USER_CLEAR,     //  2 - info            : user cleared this insim instance's buttons
                BFN_REQUEST,        //  3 - user request    : SHIFT+B or SHIFT+I - request for buttons
        """

        Size     = data.Size
        Type     = data.Type
        ReqI     = data.ReqI
        SubT     = data.SubT
        UCID     = data.UCID
        ClickID  = data.ClickID
        MaxClick = data.MaxClick
        Inst     = data.Inst


    def _inSim_Button_Clicked_Event_Handler(self, insim, data):
        """Gets called when a clickable button is clicked.
           CFlags byte: click flags:
            #define ISB_LMB         1       // left click
            #define ISB_RMB         2       // right click
            #define ISB_CTRL        4       // ctrl + click
            #define ISB_SHIFT       8       // shift + click
        """
        Size = data.Size    #8
        ReqI = data.ReqI    #ReqI as received in the IS_BTN
        UCID = data.UCID    #connection that clicked the button (zero if local)
        ClickID = data.ClickID  #button identifier originally sent in IS_BTN
        Inst = data.Inst    #used internally by InSim
        CFlags = data.CFlags    #button click flags - see below
        Sp3 = data.Sp3

    def _inSim_Text_Button_Typed_Handler(self, insim, data):
        """Gets called when a user writes in a textbox and presses Enter
        """
        Size = data.Size
        Type = data.Type
        ReqI = data.ReqI
        UCID = data.UCID
        ClickID = data.ClickID
        Inst = data.Inst
        TypeIn = data.TypeIn
        Sp3 = data.Sp3
        Text = data.Text

    ########## Generic Handlers

    def _inSim_Initialization_Event_Handler(self, insim): # pyinsim.EVT_INIT
        self.connected = True
        self.CBC.initialization_event_callback()


    def _inSim_Closing_Event_Handler(self, insim): # pyinsim.EVT_CLOSE
        self.connected = False
        self.CBC.closing_event_callback()


    def _inSim_Version_Info_Handler(self, insim, data): # pyinsim.ISP_VER
        print("version=",version,"\nproduct=",product,"\ninSimVer=",inSimVer)
        self.CBC.version_info_callback(version_data=data)


    def _inSim_Error_Event_Handler(self, insim): # pyinsim.EVT_ERROR
        print('\nInSim encountered an error. Traceback:\n')
        traceback.print_exc()


    def _inSim_All_Event_Handler(self, insim, packet): # pyinsim.EVT_ALL
        print("\nFunc all events returns :", autostring(insim))
        print('InSim Generic Event Caught : ')
        print(vars(packet))


    def _inSim_Outgauge_Event_Handler(self, insim): # pyinsim.EVT_OUTGAUGE
        print('\nInSim Outgauge Event Catched.')
        print(autostring(insim))


    def _inSim_OutSim_Event_Handler(self, insim): # pyinsim.EVT_OUTSIM
        print('\nOutSim Event Catched.')
        print(autostring(insim))


    def _inSim_Timeout_Event_Handler(self, insim): # pyinsim.EVT_TIMEOUT
        print('\nTimeout Error Catched')
        print(autostring(insim))


    def _inSim_State_Packet_Handler(self, insim, state): # pyinsim.ISP_STA
        if self.update_lss :
            self.LSS.update_state(state)



############## Connection Handlers

    def _inSim_newConnection_handler(self, insim,  ncn): # pyinsim.ISP_NCN
        if self.update_lss :
            self.LSS.new_connection(ncn)


    def _inSim_connection_left_handler(self, insim,  cnl): # pyinsim.ISP_CNL
        if self.update_lss :
            self.LSS.connection_left(cnl)


    def _inSim_newPlayer_handler(self, insim,  npl): # pyinsim.ISP_NPL
        if self.update_lss :
            self.LSS.new_player(npl)


    def _inSim_player_left_race_handler(self, insim,  pll): # pyinsim.ISP_PLL
        #PLayer Leave race (spectate - removed from player list)
        if self.update_lss :
            self.LSS.player_left(pll)



############## PLayer data handlers
    def _inSim_Connection_Interface_Mode_Handler(self, insim, cim): # pyinsim.ISP_CIM
        """Connection interface mode info handler
        Gets a connections interface mode from a user
        """
        if self.update_lss :
            self.LSS.connections[cim.UCID].update_interface_mode(cim)


    def _inSim_Car_Selected_Handler(self, insim, slc): # pyinsim.ISP_SLC
        if self.update_lss :
            self.LSS.connections[slc.UCID].update_car_selection(slc)



############## Racing Event handlers
    def _inSim_Lap_Time_Handler(self, insim, lap): # pyinsim.ISP_LAP
        if self.update_lss :
            self.LSS.players[lap.PLID].update_lap_times(lap)

    def _inSim_Split_Time_Handler(self, insim, spx): # pyinsim.ISP_SPX
        if self.update_lss :
            self.LSS.players[spx.PLID].update_split_times(spx)

    def _inSim_Pitting_Event_Handler(self, insim, pit): # pyinsim.ISP_PIT
        if self.update_lss :
            self.LSS.players[pit.PLID].player_pitting(pit)

    def _inSim_Pit_Finish_Handler(self, insim, psf): # pyinsim.ISP_PSF
        if self.update_lss :
            self.LSS.players[psf.PLID].pit_stop_finished(psf)

    def _inSim_Pit_Lane_Handler(self, insim, pla): # pyinsim.ISP_PLA
        if self.update_lss :
            self.LSS.players[pla.PLID].player_in_pitlane(pla)

    def _inSim_Race_Result_Handler(self, insim, res): # pyinsim.ISP_RES
        if self.update_lss :
            self.LSS.players[res.PLID].player_result(res)

    def _inSim_Object_Hit_Handler(self, insim, axo): # pyinsim.ISP_AXO
        if self.update_lss :
            self.LSS.players[axo.PLID].player_hit_object(axo)


############## Car Tracking And Positions # MAX 40 Cars are returned !!!
    def _inSim_Node_And_Lap_Packet_Handler(self, insim, nlp): # pyinsim.ISP_NLP
        if self.update_lss :
            self.LSS.node_lap_packet_dispatcher(nlp)


############## Map and layout handlers

    def _inSim_AutoX_Layout_data_handler(self, insim, axi): # pyinsim.ISP_AXI
        if self.update_lss :
            self.LSS.LRD.LDH.update_state(axi)




############## Message And User Input Handlers

    def _inSim_Message_Command_Out_Handler(self,insim, mso): # pyinsim.ISP_MSO
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


    def _inSim_Message_To_Host_Handler(self,insim, iii): # pyinsim.ISP_III
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
        "ISP_III" : "_inSim_Message_To_Host_Handler",
        "ISP_BTF" : "_inSim_Button_Function_Event_Handler",
        "ISP_BTC" : "_inSim_Button_Clicked_Event_Handler",
        "ISP_BTT" : "_inSim_Text_Button_Typed_Handler",
        "ISP_SMALL" : "_inSim_Small_Packet_Handler",
        "ISP_TINY" : "_inSim_Tiny_Packet_Handler",
        }
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
