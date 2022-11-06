import pyinsim
import traceback #Cause async and stuff..
import time


def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)


class InSimRequestsHandler:
    """Class to manage the server state.

    - Server data / options
    - Connections / Players
    - Message handling / chat
    - Map data
    - Error Handling

    For each handler function, if a specific action is required, a function has to be defined.
    """
    def __init__(self, insim_obj):

        self.ISO = insim_obj #insim_object

    def initial_requests(self):
        self.request_state_packet()
        self.request_AutoX_packet()


    ######################################################################
    ########## InSim Base Actions

    def close_InSim_connection(self):
        """Sends packet signifying closing
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=1, SubT=pyinsim.TINY_CLOSE)


    ######################################################################
    ########## action? functions

    def send_cmd(self, msg_cmd="/help"):
        '''Sends a command to chat. Can be a simple chat too.
        '''
        msg_cmd = autobyte(msg_cmd)
        self.ISO.send(pyinsim.ISP_MST, Msg=msg_cmd)

    def send_msg_all(self, msg_cmd):
        """Sends the same message to everybody, and it should/could not be a command ??
        """
        msg_cmd = autobyte(msg_cmd="Msg2All")
        self.ISO.send(pyinsim.ISP_MSX, Msg=msg_cmd)


    def send_msg_player(self, UCID=0, PLID=0, msg_cmd="Msg2Player"):
        '''Sends a message to chat. Can be a command.
            UCID : connection's unique id (0 = host / 255 = all)
            PLID : player's unique id (if zero, use :attr:`UCID`)
            msg_cmd  : Message (128 characters)
        '''
        msg_cmd = autobyte(msg_cmd)
        self.ISO.send(pyinsim.ISP_MTC, UCID=UCID, PLID=PLID, Msg=msg_cmd)

    def send_key_press(self, ReqI=0, CharB='\x00', Flags=0):
        """Initialise a new IS_SCH packet.

        Args:
            ReqI  : 0
            CharB : key to press
            Flags : bit 0 : SHIFT / bit 1 : CTRL

        """
        CharB = autobyte(CharB)
        self.ISO.send(pyinsim.ISP_SCH, ReqI=ReqI, CharB=CharB, Flags=Flags)


    def set_state_flags_packet(self, ReqI=0, Flag=0, OffOn=0):
        """Send new IS_SFP packet.

        Args:
            ReqI  : ReqI as received in the request packet
            Flag  : ``ISS_*`` state flags ISS_STATE_FLAGS in enums or also in pyinsim
            OffOn  : 0 = off / 1 = on        """
        self.ISO.send(pyinsim.ISP_SFP, ReqI=ReqI, Flag=Flag, OffOn=OffOn)

    def set_car_camera(self, ViewPLID=0, InGameCam=0):
        """Set Car Camera - Simplified camera packet (not SHIFT+U mode)

        """

    ######################################################################
    ########## Information requests TINY

    def request_Version_packet(self, ReqI=1):
        """Sends a packet to cancel a vote
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_VER)

    def request_Vote_Cancel_packet(self, ReqI=1):
        """Sends a packet to cancel a vote
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_VTC)

    def request_Camera_Pos_packet(self, ReqI=1):
        """Sends a packet to LFS so that it sends back information about the layout.
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_SCP)

    def request_state_packet(self, ReqI=1):
        """send state info
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_SST)

    def request_Time_packet(self, ReqI=1):
        """get time in hundredths (i.e. SMALL_RTP)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_GTH)

    def request_Multiplayer_Info_packet(self, ReqI=1):
        """get multiplayer info (i.e. ISP_ISM)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_ISM)

    def request_All_Connection_Data_packet(self, ReqI=1):
        """get NCN for all connections
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_NCN)

    def request_All_Players_packet(self, ReqI=1):
        """get all players
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_NPL)

    def request_All_Results_packet(self, ReqI=1):
        """get all results
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_RES)

    def request_Node_Lap_packet(self, ReqI=1):
        """get all players (max 40) node lap paquet
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_NLP)

    def request_Multi_Car_Info_packet(self, ReqI=1):
        """Multi Car Info - if more than MCI_MAX_CARS in race then more than one is sent (MCI_MAX_CARS=16)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_MCI)

    def request_Reorder__Info_packet(self, ReqI=1):
        """get the player  start order ? Not sure bout this
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_REO)

    def request_Race_Start_packet(self, ReqI=1):
        """info request : send an IS_RST
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_RST)

    def request_AutoX_packet(self, ReqI=1):
        """Sends a packet to LFS so that it sends back information about the layout. send an IS_AXI - AutoX Info
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_AXI)

    def request_Replay_Information_packet(self, ReqI=1):
        """send an IS_RIP - Replay Information Packet
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_RIP)

    def request_All_New_Connection_Info_packet(self, ReqI=1):
        """get NCI for all guests (on host only)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_NCI)

    def request_All_Allowed_Cars_packet(self, ReqI=1):
        """send a SMALL_ALC (allowed cars)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_ALC)

    def request_AutoX_Multiple_objects_packet(self, ReqI=1):
        """send IS_AXM packets for the entire layout
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_AXM)

    def request_All_Selected_Cars_packet(self, ReqI=1):
        """send IS_SLC packets for all connections
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_SLC)

    def request_All_Allowed_Mods_packet(self, ReqI=1):
        """send IS_MAL listing the currently allowed mods
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_MAL)

    ######################################################################
    ########## Instruction requests SMALL

    def request_Start_Sending_Positions_Viewed_Car_packet(self, ReqI=1, packet_rate=0):
        """start sending positions - OutSim ?
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_SSP, UVal=packet_rate)

    def request_Start_Sending_Gauges_Viewed_Car_packet(self, ReqI=1, packet_rate=0):
        """start sending gauges - OutSim ?
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_SSG, UVal=packet_rate)

    def request_Send_Vote_Action_packet(self, ReqI=1, vote_action=0): # Vote actions : {0 : No vote, 1 : End_ race, 2 : restart, 3 : qualify}
        """report           : vote action
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_VTA, UVal=vote_action)

    # You can stop or start time in LFS and while it is stopped you can send packets to move
    # time in steps.  Time steps are specified in hundredths of a second.
    # Warning: unlike pausing, this is a "trick" to LFS and the program is unaware of time
    # passing so you must not leave it stopped because LFS is unusable in that state.
    # This packet is not available in live multiplayer mode.

    def request_Time_Stop_packet(self, ReqI=1, stop=0): # (1 - stop / 0 - carry on)
        """Stop and Start with this IS_SMALL:
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_TMS, UVal=stop)

    def request_Time_Step_packet(self, ReqI=1, step=0): # (number of hundredths of a second to update)
        """When STOPPED, make time step updates with this IS_SMALL:
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_STP, UVal=step)

    def request_Set_Node_Lap_Rate_packet(self, ReqI=1, interval=0): # (0 means stop, otherwise time interval: 40, 50, 60... 8000 ms)
        """ You can change the rate of NLP or MCI after initialisation by sending this IS_SMALL:
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_NLI, UVal=interval)

    def request_Set_Allowed_Cars_packet(self, ReqI=1, Cars=0): # (0 means no cars can be selected, 0xffffffff all cars can be selected)
        """ To set the allowed cars on the host (like /cars command) you can send this IS_SMALL:
        !!!! Only base cars, not mods!
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_NLI, UVal=Cars)

    def request_Set_Local_Car_Switches_packet(self, ReqI=1, Switch=0): #  Possible valmues LCS_SET_SIGNALS, LCS_SET_FLASH, LCS_SET_HEADLIGHTS, LCS_SET_HORN, LCS_SET_SIREN
        """ SMALL_LCS - set local car switches (lights, horn, siren)
        // Bits 0 to 7 are a set of flags specifying which values to set.  You can set as many
        // as you like at a time.  This is to allow you to set only the values you want to set
        // while leaving the others to be controlled by the user.
        // Depending on the above values, InSim will read some of the following values and try
        // to set them as required, if a real player is found on the local computer.

        // bits 8-9   (Switches & 0x0300) - Signal    (0 off / 1 left / 2 right / 3 hazard)
        // bit  10    (Switches & 0x0400) - Flash
        // bit  11    (Switches & 0x0800) - Headlights

        // bits 16-18 (Switches & 0x070000) - Horn    (0 off / 1 to 5 horn type)
        // bits 20-21 (Switches & 0x300000) - Siren   (0 off / 1 fast / 2 slow)
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_LCS, UVal=Switch)


    ######################################################################
    ########## Instruction requests TTC


    # This is only needed for AutoX layout object selection etc. Not implemented.


    ######################################################################
    ########## Changing LFS settings

    def change_screen_settings(self, Bits16=0, RR=0, Width=0, Height=0):
        """Function to change the settings of (your own?) screen.

            Bits16 : set to choose 16-bit
            RR     : refresh rate - zero for default
            Width  : 0 means go to window
            Height : 0 means go to window

        """
        self.ISO.send(pyinsim.IS_MOD, Bits16=Bits16, RR=RR, Width=Width, Height=Height)


