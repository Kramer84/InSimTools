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

    def set_state_flag(self, ReqI=0, Flag=0, OffOn=0):
        """These flags can be set (and are accessed through pyinsim)
            ISS_SHIFTU_NO_OPT    - SHIFT+U buttons hidden
            ISS_SHOW_2D          - showing 2d display
            ISS_MPSPEEDUP        - multiplayer speedup option
            ISS_SOUND_MUTE       - sound is switched off
        """
        self.ISO.send(pyinsim.ISP_SFP, ReqI=ReqI, Flag=Flag, OffOn=OffOn)

    def set_car_camera(self, ReqI=0, ViewPLID=0, InGameCam=0):
        """Set Car Camera - Simplified camera packet (not SHIFT+U mode)
            ViewPLID  : UniqueID of player to view
            InGameCam : InGameCam (as reported in StatePack)
        """
        self.ISO.send(pyinsim.ISP_SCC, ReqI=ReqI, ViewPLID=ViewPLID, InGameCam=InGameCam)

    def set_full_camera_packet(self, ReqI=0, Pos=[0,0,0], H=0, P=0, R=0, ViewPLID=0, InGameCam=0, FOV=0.0, Time=0, Flags=0):
        """Cam Pos Pack - Full camera packet (in car OR SHIFT+U mode)  - can also be received.
            ReqI      : instruction : 0 / or reply : ReqI as received in the ``TINY_SCP``
            Pos       : Position vector
            H         : heading - 0 points along Y axis
            P         : pitch - 0 means looking at horizon
            R         : roll - 0 means no roll
            ViewPLID  : Unique ID of viewed player (0 = none)
            InGameCam : InGameCam (as reported in StatePack)
            FOV       : FOV in degrees
            Time      : Time to get there (0 means instant + reset)
            Flags     : state flags from ``ISS_*``

        """
        self.ISO.send(pyinsim.ISP_CCP, ReqI=ReqI, Pos=Pos, H=H, P=P, R=R, ViewPLID=ViewPLID, InGameCam=InGameCam, FOV=FOV, Time=Time, Flags=Flags)


    
    ######################################################################
    ########## InSim Buttons and action requests   
        # You can make up to 240 buttons appear on the host or guests (ID = 0 to 239).
        # You should set the ISF_LOCAL flag (in IS_ISI) if your program is not a host control
        # system, to make sure your buttons do not conflict with any buttons sent by the host.

        # LFS can display normal buttons in these four screens:

        # - main entry screen
        # - race setup screen
        # - in game
        # - SHIFT+U mode

        # The recommended area for most buttons is defined by:

        #define IS_X_MIN 0
        #define IS_X_MAX 110

        #define IS_Y_MIN 30
        #define IS_Y_MAX 170

        # If you draw buttons in this area, the area will be kept clear to
        # avoid overlapping LFS buttons with your InSim program's buttons.
        # Buttons outside that area will not have a space kept clear.
        # You can also make buttons visible in all screens - see below.


        # ClickID byte: this value is returned in IS_BTC and IS_BTT packets.

        # Host buttons and local buttons are stored separately, so there is no chance of a conflict between
        # a host control system and a local system (although the buttons could overlap on screen).

        # Programmers of local InSim programs may wish to consider using a configurable button range and
        # possibly screen position, in case their users will use more than one local InSim program at once.

        # TypeIn byte: if set, the user can click this button to type in text.

        # Lowest 7 bits are the maximum number of characters to type in (0 to 95)
        # Highest bit (128) can be set to initialise dialog with the button's text

        # On clicking the button, a text entry dialog will be opened, allowing the specified number of
        # characters to be typed in.  The caption on the text entry dialog is optionally customisable using
        # Text in the IS_BTN packet.  If the first character of IS_BTN's Text field is zero, LFS will read
        # the caption up to the second zero.  The visible button text then follows that second zero.

        # Text: 65-66-67-0 would display button text "ABC" and no caption

        # Text: 0-65-66-67-0-68-69-70-71-0-0-0 would display button text "DEFG" and caption "ABC"

        # Inst byte: mainly used internally by InSim but also provides some extra user flags

        #define INST_ALWAYS_ON  128     # if this bit is set the button is visible in all screens

        # NOTE: You should not use INST_ALWAYS_ON for most buttons.  This is a special flag for buttons
        # that really must be on in all screens (including the garage and options screens).  You will
        # probably need to confine these buttons to the top or bottom edge of the screen, to avoid
        # overwriting LFS buttons.  Most buttons should be defined without this flag, and positioned
        # in the recommended area so LFS can keep a space clear in the main screens.

        # BStyle byte: style flags for the button

        #define ISB_C1          1       # you can choose a standard
        #define ISB_C2          2       # interface colour using
        #define ISB_C4          4       # these 3 lowest bits - see below
        #define ISB_CLICK       8       # click this button to send IS_BTC
        #define ISB_LIGHT       16      # light button
        #define ISB_DARK        32      # dark button
        #define ISB_LEFT        64      # align text to left
        #define ISB_RIGHT       128     # align text to right

        # colour 0: light grey         (not user editable)
        # colour 1: title colour       (default:yellow)
        # colour 2: unselected text    (default:black)
        # colour 3: selected text      (default:white)
        # colour 4: ok                 (default:green)
        # colour 5: cancel             (default:red)
        # colour 6: text string        (default:pale blue)
        # colour 7: unavailable        (default:grey)

        # NOTE: If width or height are zero, this would normally be an invalid button.  But in that case if
        # there is an existing button with the same ClickID, all the packet contents are ignored except the
        # Text field.  This can be useful for updating the text in a button without knowing its position.
        # For example, you might reply to an IS_BTT using an IS_BTN with zero W and H to update the text.

    def send_create_button(self, ReqI=0, UCID=0, ClickID=0, Inst=0, BStyle=0, TypeIn=0, L=0, T=0, W=0, H=0, Text=b''):
        """Function to create a button with different functionalities, as described above
            ReqI    : non-zero (returned in ``IS_BTC`` and ``IS_BTT`` packets)
            UCID    : connection to display the button (0 = local / 255 = all)
            ClickID : button ID (0 to 239)
            Inst    : some extra flags from ``INST_*``
            BStyl   : button style flags from ``ISB_*``
            TypeIn  : max chars to type in
            L       : left: 0 - 200
            T       : top: 0 - 200
            W       : width: 0 - 200
            H       : height: 0 - 200
            Text    : 0 to 240 characters of text
        """
        self.ISO.send(pyinsim.ISP_BTN, ReqI=ReqI, UCID=UCID, ClickID=ClickID, Inst=Inst, BStyle=BStyle, TypeIn=TypeIn, L=L, T=T, W=W, H=H, Text=Text)


    def delete_button(self, ReqI=0, SubT=0, UCID=0, ClickID=0, MaxClick=0, Inst=0):
        """ To delete one button or a range of buttons or clear all buttons, send this packet
            SubT     : subtype, from ``BFN_*`` enumeration
            UCID     : connection to send to or from (0 = local / 255 = all)
            ClickID  : ID of button to delete (if ``SubT`` is ``BFN_DEL_BTN``)
            MaxClick : ID of last button to delete in range of buttons
            Inst     : used internally by InSim

        """
        self.ISO.send(pyinsim.ISP_BFN, ReqI=ReqI, SubT=SubT, UCID=UCID, ClickID=ClickID, MaxClick=MaxClick, Inst=Inst)        

        #enum // the fourth byte of IS_BFN packets is one of these
        #{
        #    BFN_DEL_BTN,        //  0 - instruction     : delete one button or range of buttons (must set ClickID)
        #    BFN_CLEAR,          //  1 - instruction     : clear all buttons made by this insim instance
        #    BFN_USER_CLEAR,     //  2 - info            : user cleared this insim instance's buttons
        #    BFN_REQUEST,        //  3 - user request    : SHIFT+B or SHIFT+I - request for buttons
        #};

        # NOTE: BFN_REQUEST allows the user to bring up buttons with SHIFT+B or SHIFT+I

        # SHIFT+I clears all host buttons if any - or sends a BFN_REQUEST to host instances
        # SHIFT+B is the same but for local buttons and local instances


    ######################################################################
    ########## InSim race actions

    def set_race_order(self, ReqI=0, PLID=[]):
        """REOrder (when race restarts after qualifying). The NumP value
            is filled in automatically from the PLID length.
            PLID : all PLIDs in new order
            """
        self.ISO.send(pyinsim.ISP_REO, ReqI=ReqI, PLID=PLID)        



    ######################################################################
    ########## action? functions


    def send_single_character(self, ReqI=0, CharB="", Flags=0):
        """Sends single character, with shift or ctrl
        Args:
            ReqI  : 0
            CharB : key to press
            Flags : bit 0 : SHIFT / bit 1 : CTRL
        """
        ch = autobyte(ch)
        self.ISO.send(pyinsim.ISP_SCH, ReqI=ReqI, CharB=CharB, Flags=Flags)

    def send_cmd(self, ReqI=0, Msg="/help"):
        '''Sends a command to chat. Can be a simple chat too.
        '''
        self.ISO.send(pyinsim.ISP_MST, ReqI=ReqI, Msg=autobyte(Msg))

    def send_msg_all(self, ReqI=0, Msg="Msg2All"):
        """Sends the same message to everybody, and it should/could not be a command ??
        """
        self.ISO.send(pyinsim.ISP_MSX, ReqI=ReqI, Msg=autobyte(Msg))

    def send_msg_local(self, ReqI=0, Sound=0, Msg=b''):
        """Sends a message to local machine, and it could be a command ??
        Sound : Sound from ``SND_*`` enumeration.
        """
        self.ISO.send(pyinsim.ISP_MSL, ReqI=ReqI, Sound=Sound, Msg=autobyte(Msg))

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

    def request_Reorder_Info_packet(self, ReqI=1):
        """get the player  start order ? Not sure bout this (get the IS_REO packet)
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


