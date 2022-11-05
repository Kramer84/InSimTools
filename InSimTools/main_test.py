import pyinsim
import InSimHandlers as ish
import LiveDataManager as ldm
import InSimRequests as isr 
import Enums as enums

if __name__ == "__main__":
	insim = pyinsim.insim(host='188.122.74.155', port=52473, Admin='Budapest123')
	LiveServerState = ldm.LiveServerState(insim)
	ServerGeneralEventHandler = ish.ServerGeneralEventHandler(insim, LiveServerState)
	pyinsim.run()