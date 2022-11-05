import pyinsim
import traceback #Cause async and stuff..
import time


def autostring(str_byt):
    return str_byt.decode() if type(str_byt)==bytes else str_byt

def autobyte(str_byt):
    return str_byt if type(str_byt)==bytes else bytes(str_byt)


class InSimGeneralRequestsHandler:
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


    ######################################################################
    ########## InSim Base Actions

    def initial_requests(self):
        self.request_state_packet()
        self.request_AutoX_packet()


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


    ######################################################################
    ########## Information requests


    def request_state_packet(self):
        """From the IS_STA documentation:
        STAte packet, sent whenever the data in the packet changes. To request
    this packet send a ``IS_TINY`` with a ``ReqI`` of non-zero and a ``SubT`` of ``TINY_SST``.
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=1, SubT=pyinsim.TINY_SST)

    def request_AutoX_packet(self):
        """Sends a packet to LFS so that it sends back information about the layout. 
        """
        self.ISO.send(pyinsim.ISP_TINY, ReqI=1, SubT=pyinsim.TINY_AXI)




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


