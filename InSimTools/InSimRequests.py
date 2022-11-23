import pyinsim
import traceback #Cause async and stuff..
import time


def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)


class InSimRequestsHandler:
    """Base class sending data to InSim. These methods are to be used as is.

    - Server data / options
    - Connections / Players
    - Message handling / chat
    - Map data

    """
    def __init__(self, insim_obj):

        self.ISO = insim_obj #insim_object



    ######################################################################
    ########## InSim Base Actions

    def request_Version_packet(self, ReqI=0):
        """Sends a packet to request the InSim version
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_VER)

    def request_state_packet(self, ReqI=0):
        """send state info
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_SST)

    def request_time_packet(self, ReqI=0):
        """get time in hundredths (i.e. SMALL_RTP)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_GTH)

    def request_multiplayer_info_packet(self, ReqI=0):
        """get multiplayer info (i.e. ISP_ISM)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_ISM)

    def request_all_connection_data_packet(self, ReqI=0):
        """get NCN for all connections
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_NCN)

    def request_all_players_packet(self, ReqI=0):
        """get all players
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_NPL)

    def request_all_new_connection_info_packet(self, ReqI=0):
        """get NCI for all guests (on host only)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_NCI)

    def close_insim_connection(self):
        """Sends packet signifying closing
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=0, SubT=pyinsim.TINY_CLOSE)

    def set_state_flags_packet(self, ReqI=0, Flag=0, OffOn=0):
        """Send new IS_SFP packet.

        Args:
            ReqI  : ReqI as received in the request packet
            Flag  : ``ISS_*`` state flags ISS_STATE_FLAGS in enums or also in pyinsim. As found in ENUMS
            OffOn  : 0 = off / 1 = on        """
        self.ISO.send(pyinsim.ISP_SFP, ReqI=ReqI, Flag=Flag, OffOn=OffOn)

    def reply_to_join_request(self,  ReqI=0, UCID=0, JRRAction = 1, X=0, Y=0, Zbyte=0, Flags=0, Index=0, Heading=0):
        """JOIN REQUEST - allows external program to decide if a player can join
            Set the ISF_REQ_JOIN flag in the IS_ISI to receive join requests
            A join request is seen as an IS_NPL packet with ZERO in the NumP field
            An immediate response (e.g. within 1 second) is required using an IS_JRR packet

            In this case, PLID must be zero and JRRAction must be JRR_REJECT or JRR_SPAWN
            If you allow the join and it is successful you will then get a normal IS_NPL with NumP set
            You can also specify the start position of the car using the StartPos structure

            IS_JRR can also be used to move an existing car to a different location
            In this case, PLID must be set, JRRAction must be JRR_RESET or higher and StartPos must be set

            To use default start point, StartPos should be filled with zero values

            To specify a start point, StartPos X, Y, Zbyte and Heading should be filled like an autocross
            start position, Flags should be 0x80 and Index should be zero

            Values for JRRAction byte :
                JRR_REJECT, JRR_SPAWN, JRR_2, JRR_3, JRR_RESET, JRR_RESET_NO_REPAIR, JRR_6, JRR_7
        """
        assert JRRAction in [0,1], "You can only accept or decline a request. Check JRRAction."
        self.ISO.send(pyinsim.ISP_JRR, ReqI=ReqI, UCID=UCID, JRRAction=JRRAction, X=X, Y=Y, Zbyte=Zbyte, Flags=Flags, Index=Index, Heading=Heading)


    ######################################################################
    ########## InSIM cars and mods management (allowing cars, getting info)..

    def request_all_allowed_cars(self, ReqI=0):
        """Request a SMALL_ALC packet (allowed cars)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_ALC)

    def request_all_allowed_mods(self, ReqI=0):
        """send IS_MAL listing the currently allowed mods
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_MAL)

    def set_all_allowed_cars(self, ReqI=0, Cars=0): # (0 means no cars can be selected, 0xffffffff all cars can be selected)
        """ To set the allowed cars on the host (like /cars command) you can send this IS_SMALL:
        !!!! Only base cars, not mods! Those are to be found in enums
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_ALC, UVal=Cars)

    def set_all_allowed_mods(self, ReqI=0, SkinID=[]):
        """Mods ALlowed - variable size
           You can set a list of up to 120 mods that are allowed to be used on a host
           Send empty list to clear the list and allow all mods to be used
        """
        self.ISO.send(pyinsim.ISP_MAL, ReqI=ReqI, SkinID=SkinID)

    def set_allowed_cars_player(self, ReqI=0, UCID=0, Cars=0):
        """You can send a packet to limit the cars that can be used by a given connection
            The resulting set of selectable cars is a subset of the cars set to be available
            on the host (by the /cars command or SMALL_ALC)
            UCID;       connection's unique id (0 = host / 255 = all)
            For example:
            Cars = 0          ... no cars can be selected on the specified connection
            Cars = 0xffffffff ... all the host's available cars can be selected
        """
        self.ISO.send(pyinsim.ISP_PLC, ReqI=ReqI,  UCID=UCID, Cars=Cars)

    def set_car_handicaps_all_drivers(self, ReqI=0, Zero=0, Info=[]):
        """You can send a packet to add mass and restrict the intake on each car model
            The same restriction applies to all drivers using a particular car model
            This can be useful for creating multi class hosts
            info is a list of pyinsim.CarHCP objects, one for each car for a class
            H_Mass and H_TRes for each car: XF GTI = 0 / XR GT = 1 etc"""
        self.ISO.send(pyinsim.ISP_HCP, ReqI=ReqI,  Zero=Zero, Info=Info)



    ######################################################################
    ########## InSim race actions

    def request_vote_cancel_packet(self, ReqI=0):
        """Sends a packet to cancel a vote
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_VTC)

    def request_all_results_packet(self, ReqI=0):
        """get all results
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_RES)

    def request_node_lap_packet(self, ReqI=0):
        """get all players (max 40) node lap paquet
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_NLP)

    def request_multi_car_info_packet(self, ReqI=0):
        """Multi Car Info - if more than MCI_MAX_CARS in race then more than one is sent (MCI_MAX_CARS=16)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_MCI)

    def request_reorder_info_packet(self, ReqI=0):
        """get the player  start order ? Not sure bout this (get the IS_REO packet)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_REO)

    def request_race_start_packet(self, ReqI=0):
        """info request : send an IS_RST
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_RST)

    def set_race_order(self, ReqI=0, PLID=[]):
        """REOrder (when race restarts after qualifying). The NumP value
            is filled in automatically from the PLID length.
            PLID : all PLIDs in new order
            You can send one to LFS in two different ways, to specify the starting order:
                1) In the race setup screen, to immediately rearrange the grid when the packet arrives
                2) In game, just before a restart or exit, to specify the order on the restart or exit
            If you are sending an IS_REO in game, you should send it when you receive the SMALL_VTA
            informing you that the Vote Action (VOTE_END / VOTE_RESTART / VOTE_QUALIFY) is about
            to take place.  Any IS_REO received before the SMALL_VTA is sent will be ignored.
            """
        self.ISO.send(pyinsim.ISP_REO, ReqI=ReqI, PLID=PLID)

    def move_car_to_position(self,  ReqI=0, UCID=0, PLID=0, JRRAction = 4, X=0, Y=0, Zbyte=0, Index=0, Heading=0):
        """SIMILAR TO JOIN REQUEST
            IS_JRR can also be used to move an existing car to a different location
            In this case, PLID must be set, JRRAction must be JRR_RESET or higher and StartPos must be set
            To specify a start point, StartPos X, Y, Zbyte and Heading should be filled like an autocross
            start position, Flags should be  and Index should be zero
            To move with car reset set JRRACTION to 4, if without then to 5
            Values for JRRAction byte :
                JRR_REJECT, JRR_SPAWN, JRR_2, JRR_3, JRR_RESET, JRR_RESET_NO_REPAIR, JRR_6, JRR_7
        """
        assert JRRAction > 3, "Check JRRAction for moving cars"
        self.ISO.send(pyinsim.ISP_JRR, ReqI=ReqI, UCID=UCID, PLID=PLID, JRRAction=JRRAction, X=X, Y=Y, Zbyte=Zbyte, Flags=0x80, Index=Index, Heading=Heading)


    ######################################################################
    ########## messages and keystrokes

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



    ######################################################################
    ########## Information requests TINY

    def request_replay_information_packet(self, ReqI=0):
        """send an IS_RIP - Replay Information Packet
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_RIP)

    def request_all_selected_cars_packet(self, ReqI=0):
        """send IS_SLC packets for all connections
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_SLC)



    ######################################################################
    ########## Instruction requests SMALL

    def request_start_sending_positions_viewed_car_packet(self, ReqI=0, packet_rate=0):
        """start sending positions - OutSim ?
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_SSP, UVal=packet_rate)

    def request_start_sending_gauges_viewed_car_packet(self, ReqI=0, packet_rate=0):
        """start sending gauges - OutSim ?
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_SSG, UVal=packet_rate)

    #shit#def request_Send_Vote_Action_packet(self, ReqI=0, vote_action=0): # Vote actions : {0 : No vote, 1 : End_ race, 2 : restart, 3 : qualify}
    #shit#    """request players vote, or somethin
    #shit#    """
    #shit#    self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_VTA, UVal=vote_action)

    # You can stop or start time in LFS and while it is stopped you can send packets to move
    # time in steps.  Time steps are specified in hundredths of a second.
    # Warning: unlike pausing, this is a "trick" to LFS and the program is unaware of time
    # passing so you must not leave it stopped because LFS is unusable in that state.
    # This packet is not available in live multiplayer mode.

    def request_time_stop_packet(self, ReqI=0, stop=0): # (1 - stop / 0 - carry on)
        """Stop and Start with this IS_SMALL:
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_TMS, UVal=stop)

    def request_time_step_packet(self, ReqI=0, step=0): # (number of hundredths of a second to update)
        """When STOPPED, make time step updates with this IS_SMALL:
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_STP, UVal=step)

    def request_set_node_lap_rate_packet(self, ReqI=0, interval=0): # (0 means stop, otherwise time interval: 40, 50, 60... 8000 ms)
        """ You can change the rate of NLP or MCI after initialisation by sending this IS_SMALL:
        """
        self.ISO.send(pyinsim.ISP_SMALL, ReqI=ReqI, SubT=pyinsim.SMALL_NLI, UVal=interval)

    def request_set_local_car_switches_packet(self, ReqI=0, Switch=0): #  Possible valmues LCS_SET_SIGNALS, LCS_SET_FLASH, LCS_SET_HEADLIGHTS, LCS_SET_HORN, LCS_SET_SIREN
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
    ########## Map and object handling

    def request_autox_packet(self, ReqI=0):
        """Sends a packet to LFS so that it sends back information about the layout. send an IS_AXI - AutoX Info
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_AXI)

    def request_autox_multiple_objects_packet(self, ReqI=0):
        """send IS_AXM packets for the entire layout
        Will send as many as necessary to describe it
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_AXM)

    def control_lights_objects(self, OCOAction=0, Index=0, Identifier=0, Data=0):
        """OBJECT CONTROL - currently used for switching start lights
        Args:
            OCOAction   : values from OCO_*
            Index       : specifies which lights you want to override:
                          AXO_START_LIGHTS / OCO_INDEX_MAIN
            Identifier  : identify particular start lights objects (0 to 63 or 255 = all)
            Data        : specifies particular bulbs using the low 4 bits
                    OCO_INDEX_MAIN:
                        bit 0 (1) : red1
                        bit 1 (2) : red2
                        bit 2 (4) : red3
                        bit 3 (8) : green
                    AXO_START_LIGHTS:
                        bit 0 (1) : red
                        bit 1 (2) : amber
                        bit 3 (8) : green
        """
        self.ISO.send(pyinsim.ISP_OCO, OCOAction=OCOAction, Index=Index, Identifier=Identifier, Data=Data)


    def control_multiple_autox_objects(self, ReqI=0, NumO=0, UCID=0, PMOAction=0, PMOFlags=0, Sp3=0, Info=[]):
        """AutoX Multiple objects
        Set the ISF_AXM_LOAD flag in the IS_ISI for info about objects when a layout is loaded.
        Set the ISF_AXM_EDIT flag in the IS_ISI for info about objects edited by user or InSim.

        You can also add or remove objects by sending IS_AXM packets.
        Some care must be taken with these - please read the notes in the documentation InSim.txt.

        """
        self.ISO.send(pyinsim.ISP_AXM, ReqI=ReqI, NumO=NumO, UCID=UCID, PMOAction=PMOAction, PMOFlags=PMOFlags, Sp3=Sp3, Info=Info)


    def send_target_to_connection(self, ReqI=0, SubT=pyinsim.TTC_NONE, UCID=0, B1=0, B2=0, B3=0):
        """General purpose 8 byte packet (Target To Connection)
        """
        self.ISO.send(pyinsim.ISP_TTC, ReqI=ReqI, SubT=SubT, UCID=UCID, B1=B1, B2=B2, B3=B3)


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
    ########## Camera - screenshots - replay - spectating...

    def request_camera_pos_packet(self, ReqI=0):
        """Sends a packet to LFS so that it sends back the Cam Pos Pack - Full camera packet (in car OR SHIFT+U mode)
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=ReqI, SubT=pyinsim.TINY_SCP)

    def send_car_camera_packet(self, ReqI=0, ViewPLID=0, InGameCam=0):
        """Set who to watch when spectating ?
        You can set the viewed car and selected camera directly with a special packet
        These are the states normally set in game by using the TAB and V keys
        NOTE: Set InGameCam or ViewPLID to 255 to leave that option unchanged.

        ViewPLID;   // Unique ID of player to view
        InGameCam;  // InGameCam (as reported in StatePack) :
              0: "VIEW_FOLLOW",   # - arcade
              1: "VIEW_HELI",     # - helicopter
              2: "VIEW_CAM",      # - tv camera
              3: "VIEW_DRIVER",   # - cockpit
              4: "VIEW_CUSTOM",   # - custom
        """
        self.ISO.send(pyinsim.ISP_SCC, ReqI=ReqI, ViewPLID=ViewPLID, InGameCam=InGameCam)

    def send_full_camera_packet(self, ReqI=0, Pos=[0,0,0], H=0, P=0, R=0, ViewPLID=0, InGameCam=0, FOV=0.0, Time=0, Flags=0):
        """Cam Pos Pack - Full camera packet (in car OR SHIFT+U mode)
        Args:
            ReqI      : instruction : 0 / or reply : ReqI as received in the ``TINY_SCP``
            Pos       : Position vector  "Vec": 3 ints (X, Y, Z) - 65536 means 1 metre
            H         : heading - 0 points along Y axis
            P         : pitch - 0 means looking at horizon
            R         : roll - 0 means no roll
            ViewPLID  : Unique ID of viewed player (0 = none)
            InGameCam : InGameCam (as reported in StatePack)
            FOV       : FOV in degrees
            Time      : Time to get there (0 means instant + reset)
            Flags     : state flags from ``ISS_*``

        The ISS state flags that can be set are:
            ISS_SHIFTU           - in SHIFT+U mode
            ISS_SHIFTU_FOLLOW    - FOLLOW view
            ISS_VIEW_OVERRIDE    - override user view
        # On receiving this packet, LFS will set up the camera to match the values in the packet,
        # including switching into or out of SHIFT+U mode depending on the ISS_SHIFTU flag.

        # If ISS_VIEW_OVERRIDE is set, the in-car view Heading, Pitch, Roll and FOV [not smooth]
        # can be set using this packet.  Otherwise normal in game control will be used.

        # Position vector (Vec Pos) - in SHIFT+U mode, Pos can be either relative or absolute.

        # If ISS_SHIFTU_FOLLOW is set, it's a following camera, so the position is relative to
        # the selected car.  Otherwise, the position is absolute, as used in normal SHIFT+U mode.

        # NOTE: Set InGameCam or ViewPLID to 255 to leave that option unchanged.

        # SMOOTH CAMERA POSITIONING
        # --------------------------

        # The "Time" value in the packet is used for camera smoothing.  A zero Time means instant
        # positioning.  Any other value (milliseconds) will cause the camera to move smoothly to
        # the requested position in that time.  This is most useful in SHIFT+U camera modes or
        # for smooth changes of internal view when using the ISS_VIEW_OVERRIDE flag.

        # NOTE: You can use frequently updated camera positions with a longer Time value than
        # the update frequency.  For example, sending a camera position every 100 ms, with a
        # Time value of 1000 ms.  LFS will make a smooth motion from the rough inputs.

        # If the requested camera mode is different from the one LFS is already in, it cannot
        # move smoothly to the new position, so in this case the "Time" value is ignored.
        """
        self.ISO.send(pyinsim.ISP_SCC, ReqI=0, Pos=[0,0,0], H=0, P=0, R=0, ViewPLID=0, InGameCam=0, FOV=0.0, Time=0, Flags=0)

    def send_replay_information_packet(self, ReqI=0, Error=0, MPR=0, Paused=0, Options=0, CTime=0, TTime=0, RName=b''):
        """You can load a replay or set the position in a replay with an IS_RIP packet.
        Replay positions and lengths are specified in hundredths of a second.
        LFS will reply with another IS_RIP packet when the request is completed.
        Args:
            ReqI    : request : non-zero / reply : same value returned
            Error   : 0 or 1 = OK / options from ``RIP_*``
            MPR     : 0 = SPR / 1 = MPR
            Paused  : request : pause on arrival / reply : paused state
            Options : various options from ``RIPOPT_*``
            CTime   : (hundredths) request : destination / reply : position
            TTime   : (hundredths) request : zero / reply : replay length
            RName   : zero or replay name: last byte must be zero
        NOTE about RName:
        In a request, replay RName will be loaded.  If zero then the current replay is used.
        In a reply, RName is the name of the current replay, or zero if no replay is loaded.
        """
        self.ISO.send(pyinsim.ISP_RIP, ReqI=ReqI, Error=Error, MPR=MPR, Paused=Paused, Options=Options, CTime=CTime, TTime=TTime, RName=autobyte(RName))

    def request_screenshot(self, ReqI=0, Error=0, BMP=b''):
        """You can instuct LFS to save a screenshot in data/shots using the IS_SSH packet.
        It will be saved as bmp / jpg / png as set in Misc Options.
        Name can be a filename (excluding extension) or zero - LFS will create a name.
        LFS will reply with another IS_SSH when the request is completed.
        Args:
            ReqI  : request : non-zero / reply : same value returned
            Error : 0 = OK / other values from ``SSH_*``
            BMP   : name of screenshot file: last byte must be zero"""
        self.ISO.send(pyinsim.ISP_SSH, ReqI=ReqI, Error=Error, BMP=autobyte(BMP))