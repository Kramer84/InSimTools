class ServerGeneralEventCallbacks :
    """This class will contain all the custom functions reacting to events
    in  LFS.

    The structure will be very similar to the ServerGeneralEventHandler
    """

    def __init__(self, insim_obj):
        SELF.ISO = insim_obj


    ########################################################################

    def initialization_event_callback(self, insim):
        print('\nInSim initialized')
        print(autostring(insim))
