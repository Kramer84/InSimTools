import pyinsim
import traceback #Cause async and stuff..


def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)


class ServerStateManager:
    """Class to manage the server state.

    - Initialize InSim
    - Connect / Disconnect / Reconnect
    - Ban Data ? 
    - Error Handling ?   
    """
    def __init__(self, insim_obj):
        self.ISO = insim_obj #insim_object
        self.bind_listners()

    

    ######################################################################
    ######### InSim Event Listners. This are functions to react to a packet sent by LFS
    ######### Generic Listners
    def _inSim_Initialization_Event_Listner(self, insim):
        print("\nFunc 1 returns :", autostring(insim))
        print('InSim initialized')

    def _inSim_Closing_Event_Listner(self, insim):
        print("\nFunc 2 returns :", autostring(insim))
        print('InSim connection closed')

    def _inSim_Error_Event_Listner(self, insim):
        print("\nFunc 2 returns :", autostring(insim))
        print('InSim encountered an error. Traceback:\n')
        traceback.print_exc()

    def _inSim_All_Event_Listner(self, insim, packet):
        print("\nFunc 2 returns :", autostring(insim))
        print('InSim Event Caught.')
        print(vars(packet))

    def _inSim_Outgauge_Event_Listner(self, insim):
        print("\nFunc 2 returns :", autostring(insim))
        print('InSim Outgauge Event Catched.')

    def _inSim_OutSim_Event_Listner(self, insim):
        print("\nFunc 2 returns :", autostring(insim))
        print('OutSim Event Catched.')

    def _inSim_Timeout_Event_Listner(self, insim):
        print("\nFunc 2 returns :", autostring(insim))
        print('Timeout Error Catched')

    ######### Message And User Input Listners
    def _inSim_Message_Command_Out_Listner(self,insim, mso):
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

    def _inSim_Message_To_Host_Listner(self,insim, iii):
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
        self.send_msg_player(msg_cmd=msg) #Sends to yourself




    ######################################################################
    ########## Binding Listners

    def bind_listners(self):
        ## Generic Listners
        self.ISO.bind(pyinsim.EVT_INIT,     self._inSim_Initialization_Event_Listner)
        self.ISO.bind(pyinsim.EVT_CLOSE,    self._inSim_Closing_Event_Listner)
        self.ISO.bind(pyinsim.EVT_ERROR,    self._inSim_Error_Event_Listner)
        self.ISO.bind(pyinsim.EVT_ALL,      self._inSim_All_Event_Listner)
        self.ISO.bind(pyinsim.EVT_OUTGAUGE, self._inSim_Outgauge_Event_Listner)
        self.ISO.bind(pyinsim.EVT_OUTSIM,   self._inSim_OutSim_Event_Listner)
        self.ISO.bind(pyinsim.EVT_TIMEOUT,  self._inSim_Timeout_Event_Listner)
        ## Input  Listners
        self.ISO.bind(pyinsim.ISP_MSO,       self._inSim_Message_Command_Out_Listner)
        self.ISO.bind(pyinsim.ISP_III,       self._inSim_Message_To_Host_Listner)

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



if __name__=="__main__":
    print('There we go! ')
    insim = pyinsim.insim('127.0.0.1', 58672, Admin='YourAdminPassword')
    ServerStateManager(insim)
    pyinsim.run()