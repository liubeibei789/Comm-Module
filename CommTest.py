from Comm import Comm
import os
import time

numOfPeers = 1               # number of peers to talk to
CommComp1 = Comm(numOfPeers)  # instantiate the Comm class
CommComp1.do(numOfPeers, [os.path.join('.','fileTran','entity_1'), os.path.join('.','fileTran','entity_2')],
            [os.path.join('.','fileRecv','entity_1'), os.path.join('.','fileRecv','entity_2')],
            ['10.206.203.243', '10.152.144.160'])

# ########################################################################################
# print '.......simulation going on.........'
# time.sleep(5)
# print '.....simulation done. ready for transmission .........'
# ########################################################################################
#
# CommComp2 = Comm(numOfPeers)  # instantiate the Comm class
# CommComp2.do(numOfPeers, [os.path.join('.','fileTran','entity_1'), os.path.join('.','fileTran','entity_2')],
#             [os.path.join('.','fileRecv','entity_1'), os.path.join('.','fileRecv','entity_2')],
#             ['10.206.203.243', '10.152.144.160'])
#
# ########################################################################################
# print '.......simulation going on.........'
# time.sleep(5)
# print '.....simulation done. ready for transmission .........'
# ########################################################################################
#
# CommComp3 = Comm(numOfPeers)  # instantiate the Comm class
# CommComp3.do(numOfPeers, [os.path.join('.','fileTran','entity_1'), os.path.join('.','fileTran','entity_2')],
#             [os.path.join('.','fileRecv','entity_1'), os.path.join('.','fileRecv','entity_2')],
#             ['10.206.203.243', '10.152.144.160'])
#
# ########################################################################################
# print '.......simulation going on.........'
# time.sleep(5)
# print '.....simulation done. ready for transmission .........'
# ########################################################################################
#
