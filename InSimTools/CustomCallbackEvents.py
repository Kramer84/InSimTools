class ServerGeneralEventCallbacks :
    """This class will contain all the custom functions reacting to events
    in  LFS.

    The structure will be very similar to the ServerGeneralEventHandler
    """

    def __init__(self, insim_obj):
        self.ISO = insim_obj

    ########################################################################

    def initialization_event_callback(self, *args):
        print('Initialized')

    def closing_event_callback(self, *args):
        print('Closed')

    def version_info_callback(self, *args):
        print("versiond")