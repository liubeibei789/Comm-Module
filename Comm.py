# This is a multi-threaded communication python script,
# transmitting a series of files one by one to another machine,
# while receiving files from any incoming connection.
# Author: Beibei Liu (liubeibei789@gmail.com), created: 03/2018
# Please refer to README.txt before running this script

# !usr/bin/python

import socket
import threading
import time
import os
import sys


class Comm(object):

    ############################################
    # __init__: constructor:
    # args:
    # numOfPeers: number of peers to communicate with
    ############################################
    def __init__(self, numOfPeers):

        self.quitFlag = 0  # if 1: server closed (server)
        self.exitFlag = 0  # if 1: client stops transmitting files (client)
        self.timeOut = 100     # maximum number of connecting trials (client)
        self.interval = 2     # try re-connecting every 3 second (client)
        self.maxConnect = 5   # maximum number of connections allowed (server)
        self.recvBufSize = 1024  # receiving buffer size
        self.lock = threading.Lock()  # for the shared parameter self.exitFlag & self.quitFlag, etc.

        self.numOfPeers = numOfPeers  # 1  # number of peers to communicate with
        self.peerIp = '127.0.0.1'
        self.myPort = 1111   # this is the default port, if not working, change it
        self.peerPort = 1111 # this is the default port, if not working, change it

        #self.fileList = [[]]

        ####### print the host name and host ip ############
        self.hostName = socket.gethostname()
        print('Host name:' + self.hostName)

        self.myIp = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
            [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
             [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

        print('Host ip: ' + self.myIp)

    ############################################
    # getList() function:
    # go through the files for each peer, put file directories to fileList
    # args:
    # tranFolderList: a list, each element is a folder directory for a given peer
    # return:
    # fileList: a list, each element is a list of files for a given peer
    ############################################
    def getList(self, tranFolderList):
        fileList = []
        print 'directories of files for all peers are:'
        for p in range(self.numOfPeers):
            fileListTemp = []
            print '*********** file list for peer '+ str(p) + ': ***********'
            for root, dirs, files in os.walk(tranFolderList[p]):
                for file in files:
                    if file == '.DS_Store':  # for the case of mac operating system, to skip .DS_Store file
                        continue
                    fullDir = os.path.join(root, file)
                    print fullDir
                    fileListTemp.append(fullDir) # fileListTemp: for a given peer (1-dim list)
            fileList.append(fileListTemp) # for all peers (2-dim, list of list)
            print 'number of files: '+ str(len(fileListTemp))
        return fileList

    ##################################################################
    # listen to a port for all possible incoming connections
    # write the receiving messages to files, naming with the ip of incoming connection
    # files from different users are stored in separate folders, naming with the ip of incoming connection
    ##################################################################
    def receive(self, recvFolderList, peerIpList):
        print 'receive() begins' # start listening
        sockRecv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockRecv.bind((self.myIp, self.myPort))
        sockRecv.listen(self.maxConnect)

        dict_peer = {}  # dictionary: key: peer host ip, value: structure with 2 members
                            # member 1: name of receiving folder
                            # member 2: number of connections from this ip

        ######### create the dictionary ########
        for i in range(len((peerIpList))):
            dict_peer[peerIpList[i]] = [recvFolderList[i], 0]
            if not os.path.exists(recvFolderList[i]):
                os.mkdir(recvFolderList[i])

        ########### main loop ############
        while self.quitFlag == 0:
            #================== waiting for a new connection ==================
            print 'enter receive()' 
            connection, addr = sockRecv.accept()  # blocked here
            if addr[0] == self.myIp:  # the signal for exit or quit(to break the block)
                break
            print self.hostName + ' accepts a connection from:' + str(addr)
            fileNameRecvTemp = socket.gethostbyaddr(addr[0])
            print 'peer name is:', fileNameRecvTemp[0]

            # ============== update this new connection in dictionary ==============
            if addr[0] in dict_peer:
                recvFolderName = dict_peer[addr[0]][0]  # member 1: receiving folder name
                dict_peer[addr[0]][1] += 1  # member 2: number of connections from this ip

                buf = connection.recv(self.recvBufSize)  # the first round is file name
                bufFileName = buf.split('endMarker')[0]   # file = fileName + 'endMarker' + fileContent
                if bufFileName == 'dummy':  # closing signal
                    print 'closing signal'
                    break
                print 'received file directory is:' + os.path.join(recvFolderName, bufFileName)
                fd = open(os.path.join(recvFolderName, bufFileName), 'w')

                print '************ content: ************'
                buf = buf.split('endMarker')[1]
                while buf:
                    sys.stdout.softspace = 0  # avoid space between two buffer prints
                    print buf
                    fd.write(buf)
                    buf = connection.recv(self.recvBufSize)
                print '**********************************'
                connection.send('feedback: ' + self.hostName + ' has received ' + bufFileName)
                connection.close()
            else:
                print 'unrecognized incoming connection!'
        sockRecv.close()
        print 'receive() done'


    ##################################################################
    # transmit() function:
    # transmit a bunch of files specified by givenFileList to the given peer
    # args:
    # givenFileList: list of files to transmit (for a given peer)
    ##################################################################
    def transmit(self, givenFileList, peerIp):

        print 'transmit() begins'
        for k in range(len(givenFileList)):
            if self.exitFlag == 0:
                print 'enter transmit()'  # start a new transmission
                time.sleep(1)
                fileName = os.path.basename(givenFileList[k])
                print 'going to send: ' + fileName
                isConnected = 0       # if 1: host is connected to server
                j = 1
                while j <= self.timeOut and isConnected == 0:
                    print 'trial ', str(j)
                    sockTran = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket creation must be in for loop
                    try:
                        sockTran.connect((peerIp, self.peerPort))
                        print 'connected'
                        isConnected = 1
                    except:
                        print 'connecting...'
                        time.sleep(self.interval)
                        j += 1

                sockTran.send(fileName+'endMarker')
                fd = open(givenFileList[k], 'r')
                if fd != -1:
                    print 'open succeed'
                line = fd.readline()
                while line:
                    sockTran.send(line)
                    print line,
                    line = fd.readline()
                sockTran.close()
        print 'transmit() done'

        sockClose = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockClose.connect((peerIp, self.peerPort))
        sockClose.send('dummyendMarker')
        sockClose.close()
        print 'dummy sent'
    ##################################################################
    # when receiving is done, to close server, type 'q' (for quit)
    # when transmitting is done, to stops client, type 'e' (for exit)
    ##################################################################
    def terminate(self):
        while self.quitFlag == 0 or self.exitFlag == 0:
            try:
                instruction = raw_input()
                if instruction == 'e':
                    print 'client stops transmitting'
                    sockExit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sockExit.connect((self.myIp, self.myPort))
                    self.lock.acquire()
                    self.exitFlag = 1
                    self.lock.release()
                    print self.hostName + ' \'s transmission finished'
                elif instruction == 'q':
                    print 'server closed'
                    self.lock.acquire()
                    self.quitFlag = 1
                    self.lock.release()
                    sockQuit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sockQuit.connect((self.myIp, self.myPort))
                    print self.hostName + ' \'s server closed'
                else:
                    print 'to close the server, type: q; to stop transmitting, type: e'
            except:
                pass
            finally:
                pass
        print 'terminate() done'

##################################################################
# main
##################################################################
#if __name__ == '__main__':
    def do(self, numOfPeers, tranFolderList, recvFolderList, peerIpList):

        # numOfPeers = 1
        # testComm = Comm(numOfPeers)

        fileList = []
        #tranFolderList = [os.path.join('.','fileTran','entity_1'), os.path.join('.','fileTran','entity_2')]
        fileList = self.getList(tranFolderList)

        #recvFolderList = [os.path.join('.','fileRecv','entity_1'), os.path.join('.','fileRecv','entity_2')]
        #peerIpList = ['10.206.203.243', '10.152.144.160']

        ###### clear up the receiving folder #########
        for i in range(len(recvFolderList)):
            for root, dirs, files in os.walk(recvFolderList[i], topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

        ########## multi-threaded ###############
        threads = []

        #====================== thread 1: receive ======================
        # listening for the connection
        t1 = threading.Thread(target=self.receive, args=(recvFolderList, peerIpList))
        threads.append(t1)

        # ====================== thread 2: terminate ======================
        # for possible human interrupt during the transmission
        t2 = threading.Thread(target=self.terminate)
        threads.append(t2)

        # ====================== thread 3 and more: transmit ======================
        # for each transmission, a new thread is created
        for i in range(numOfPeers):  # i: peer index, fileList: two-dimension
            t3 = threading.Thread(target=self.transmit, args=(fileList[i], peerIpList[i])) # fileList[i]: file list of peer i
            threads.append(t3)

        ############## start the threads ###########
        for t in threads:
            t.start()

        ######### blocked here, wait for termination of all threads ###########
        # for t in threads:
        #     t.join()

        for i in range(numOfPeers):
            threads[i+2].join()
            print 'join================'
        t1.join()
        #print 'join===========-------------==='

