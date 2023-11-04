import pyinsim
import InSimHandlers as ish
import LiveDataManager as ldm
import InSimRequests as isr
import Enums as enums

if __name__ == "__main__":
	insim = pyinsim.insim(host='188.122.74.155', port=55942, Admin='suKR45_eff', Interval=500)
	LiveServerState = ldm.LiveServerState(insim)
	ServerGeneralEventHandler = ish.ServerGeneralEventHandler(insim, LiveServerState, True)
	pyinsim.run()
