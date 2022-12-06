
ISS_STATE_FLAGS = {
  1 : "ISS_GAME",     # in game (or MPR)
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


VIEW_TYPES = {
  0: "VIEW_FOLLOW",   # - arcade
  1: "VIEW_HELI",     # - helicopter
  2: "VIEW_CAM",      # - tv camera
  3: "VIEW_DRIVER",   # - cockpit
  4: "VIEW_CUSTOM",   # - custom
  5: None}            #VIEW_MAX


DISCONNECT_REASONS = {
  0 : "LEAVR_DISCO",    # 0 - none
  1 : "LEAVR_TIMEOUT",    # 1 - timed out
  2 : "LEAVR_LOSTCONN",   # 2 - lost connection
  3 : "LEAVR_KICKED",   # 3 - kicked
  4 : "LEAVR_BANNED",   # 4 - banned
  5 : "LEAVR_SECURITY",   # 5 - security
  6 : "LEAVR_CPW",      # 6 - cheat protection wrong
  7 : "LEAVR_OOS",      # 7 - out of sync with host
  8 : "LEAVR_JOOS",     # 8 - join OOS (initial sync failed)
  9 : "LEAVR_HACK",     # 9 - invalid packet
  10 :"LEAVR_NUM"}


SETUP_FLAGS = {
  1 : "SETF_SYMM_WHEELS",
  2 : "SETF_TC_ENABLE",
  4 : "SETF_ABS_ENABLE"}

# Different possible viewmodes a player can have
CIM_MODES = {
  0 :"CIM_NORMAL",             # 0 - not in a special mode
  1 : "CIM_OPTIONS",            # 1
  2 : "CIM_HOST_OPTIONS",       # 2
  3 : "CIM_GARAGE",             # 3
  4 : "CIM_CAR_SELECT",         # 4
  5 : "CIM_TRACK_SELECT",       # 5
  6 : "CIM_SHIFTU", 7: None}             # 6 - free view mode

# Different possible vote actions :
VOTE_ACTIONS = {
  0 : "VOTE_NONE",
  1 : "VOTE_END",
  2 : "VOTE_RESTART",
  3 : "VOTE_QUALIFY"}


# Different possible info views you can get while driving
CIM_NORMAL_SUBMODES = {
  0 : "NRM_NORMAL",
  1 : "NRM_WHEEL_TEMPS",        # F9
  2 : "NRM_WHEEL_DAMAGE",       # F10
  3 : "NRM_LIVE_SETTINGS",      # F11
  4 : "NRM_PIT_INSTRUCTIONS",   # F12
  5 : "NRM_NUM"}


# Different viewpoints you can have while in garage
CIM_GARAGE_SUBMODES = {
  0 : "GRG_INFO",
  1 : "GRG_COLOURS",
  2 : "GRG_BRAKE_TC",
  3 : "GRG_SUSP",
  4 : "GRG_STEER",
  5 : "GRG_DRIVE",
  6 : "GRG_TYRES",
  7 : "GRG_AERO",
  8 : "GRG_PASS",
  9 : "GRG_NUM"}


CIM_SHIFTU_SUBMODES = {
  0 : "FVM_PLAIN",              # no buttons displayed
  1 : "FVM_BUTTONS",            # buttons displayed (not editing)
  2 : "FVM_EDIT",               # edit mode
  3 : "FVM_NUM"}


PIT_LANE_FACTS = {
  0 : "PITLANE_EXIT",   # 0 - left pit lane
  1 : "PITLANE_ENTER",    # 1 - entered pit lane
  2 : "PITLANE_NO_PURPOSE", # 2 - entered for no purpose
  3 : "PITLANE_DT",     # 3 - entered for drive-through
  4 : "PITLANE_SG",     # 4 - entered for stop-go
  5 : "PITLANE_NUM"}

# Pit Work Flags
PIT_WORK_FLAGS = {
  0 : "PSE_NOTHING",    # bit 0 (1)
  1 : "PSE_STOP",     # bit 1 (2)
  2 : "PSE_FR_DAM",     # bit 2 (4)
  3 : "PSE_FR_WHL",     # etc...
  4 : "PSE_LE_FR_DAM",
  5 : "PSE_LE_FR_WHL",
  6 : "PSE_RI_FR_DAM",
  7 : "PSE_RI_FR_WHL",
  8 : "PSE_RE_DAM",
  9 : "PSE_RE_WHL",
  10 : "PSE_LE_RE_DAM",
  11 : "PSE_LE_RE_WHL",
  12 : "PSE_RI_RE_DAM",
  13 : "PSE_RI_RE_WHL",
  14 : "PSE_BODY_MINOR",
  15 :"PSE_BODY_MAJOR",
  16 : "PSE_SETUP",
  17 : "PSE_REFUEL",
  18 : "PSE_NUM"}


CARS = {"XF GTI" : 1,
  "XR GT" : 2,
  "XR GT TURBO" : 4,
  "RB4 GT" : 8,
  "FXO TURBO" : 0x10,
  "LX4" : 0x20,
  "LX6" : 0x40,
  "MRT5" : 0x80,
  "UF 1000" : 0x100,
  "RACEABOUT" : 0x200,
  "FZ50" : 0x400,
  "FORMULA XR" : 0x800,
  "XF GTR" : 0x1000,
  "UF GTR" : 0x2000,
  "FORMULA V8" : 0x4000,
  "FXO GTR" : 0x8000,
  "XR GTR" : 0x10000,
  "FZ50 GTR" : 0x20000,
  "BMW SAUBER F1.06" : 0x40000,
  "FORMULA BMW FB02" : 0x80000}
