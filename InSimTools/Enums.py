
ISS_STATE_FLAGS = { 1 : "ISS_GAME",     # in game (or MPR)
                    2 : "ISS_REPLAY",       # in SPR
                    4 : "ISS_PAUSED",       # paused
                    8 : "ISS_SHIFTU",       # SHIFT+U mode
                    16 : "ISS_DIALOG",      # in a dialog
                    32 : "ISS_SHIFTU_FOLLOW",       # FOLLOW view
                    64 : "ISS_SHIFTU_NO_OPT",       # SHIFT+U buttons hidden
                    128 : "ISS_SHOW_2D",        # showing 2d display
                    256 : "ISS_FRONT_END",      # entry screen
                    512 : "ISS_MULTI",      # multiplayer mode
                    1024 : "ISS_MPSPEEDUP",  # multiplayer speedup option
                    2048 : "ISS_WINDOWED",   # LFS is running in a window
                    4096 : "ISS_SOUND_MUTE",     # sound is switched off
                    8192 : "ISS_VIEW_OVERRIDE",  # override user view
                    16384 : "ISS_VISIBLE",   # InSim buttons visible
                    32768 : "ISS_TEXT_ENTRY",}   # in a text entry dialog

VIEW_TYPES = {0: "VIEW_FOLLOW",     # - arcade
              1: "VIEW_HELI",       # - helicopter
              2: "VIEW_CAM",        # - tv camera
              3: "VIEW_DRIVER",     # - cockpit
              4: "VIEW_CUSTOM", 5:None     # - custom
              }#VIEW_MAX


SETUP_FLAGS = {1 : "SETF_SYMM_WHEELS", 2 : "SETF_TC_ENABLE", 4 : "SETF_ABS_ENABLE"}

# Different possible viewmodes a player can have
CIM_MODES = { 0 :"CIM_NORMAL",             # 0 - not in a special mode
              1 : "CIM_OPTIONS",            # 1
              2 : "CIM_HOST_OPTIONS",       # 2
              3 : "CIM_GARAGE",             # 3
              4 : "CIM_CAR_SELECT",         # 4
              5 : "CIM_TRACK_SELECT",       # 5
              6 : "CIM_SHIFTU", 7: None}             # 6 - free view mode


# Different possible info views you can get while driving
CIM_NORMAL_SUBMODES = {
                0 : "NRM_NORMAL",
                1 : "NRM_WHEEL_TEMPS",        # F9
                2 : "NRM_WHEEL_DAMAGE",       # F10
                3 : "NRM_LIVE_SETTINGS",      # F11
                4 : "NRM_PIT_INSTRUCTIONS",   # F12
                5 : "NRM_NUM"}

# Different viewpoints you can have while in garage
CIM_GARAGE_SUBMODES = { 0 : "GRG_INFO",
                        1 : "GRG_COLOURS",
                        2 : "GRG_BRAKE_TC",
                        3 : "GRG_SUSP",
                        4 : "GRG_STEER",
                        5 : "GRG_DRIVE",
                        6 : "GRG_TYRES",
                        7 : "GRG_AERO",
                        8 : "GRG_PASS",
                        9 : "GRG_NU"M
}

CIM_SHIFTU_SUBMODES = {
       0 : "FVM_PLAIN",              # no buttons displayed
       1 : "FVM_BUTTONS",            # buttons displayed (not editing)
       2 : "FVM_EDIT",               # edit mode
       3 : "FVM_NUM"}