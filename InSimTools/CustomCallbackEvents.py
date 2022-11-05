class ServerGeneralEventCallbacks :
    """This class will contain all the custom functions reacting to events
    in  LFS.

    The structure will be very similar to the ServerGeneralEventHandler
    """

    def __init__(self, insim_obj):
        SELF.ISO = insim_obj


    ########################################################################

    def initialization_event_callback(self, *args):
        pass

    def closing_event_callback(self, *args):
        pass

    def version_info_callback(self, *args):
        pass 