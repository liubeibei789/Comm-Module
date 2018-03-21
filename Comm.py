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
import shutil

class Comm(object):

    def __init__(self):

        self.quitFlag = 0  # if 1: server closed (server)
        self.exitFlag = 0  # if 1: client stops transmitting files (client)
        self.timeOut = 10     # maximum number of connecting trials (client)
        self.interval = 2     # try re-connecting every 3 second (client)
        self.maxConnect = 5   # maximum number of connections allowed (server)
        self.recvBufSize = 1024  # receiving buffer size
        self.inService = 1   # if 1: indicating it is during the configuration period
        self.myIp = '127.0.0.1'
        self.peerIp = '127.0.0.1'
        self.myPort = 1111   # this is the default port, if not working, change it
        self.peerPort = 1111 # this is the default port, if not working, change it
        self.ini = 0  # if 1: indicating the current machine is the one who initiate the transmission
        self.fileNameTran = []
        self.folderNameTran = []
        self.fileNameRecv = []
        self.numOfPairs = 1  # number of connection pairs

    ##################################################################
    # this function runs at the very beginning,
    # assisting the user to configure this Comm module
    ##################################################################
    def config(self):
        self.hostName = socket.gethostname()
        print('Your host name is:' + self.hostName)

        self.myIp = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
            [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
             [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

        print('Your host ip is: ' + self.myIp)
        print 'Please let your peer machine know your ip'
        time.sleep(1)
        self.numOfPairs = raw_input('How many entities are you going to communicate? Put number and enter:')
        # self.fileNameRecv = []
        for i in range(int(self.numOfPairs)):
            print('for entity_'+ str(i+1) +':')
            self.peerIp = raw_input('Input your peer machine \'s ip and enter:')

            folderNameTranTemp = socket.gethostbyaddr(self.peerIp)
            shutil.move('./fileTran/entity_'+str(i+1), './fileTran/'+ folderNameTranTemp[0])
            self.folderNameTran.append(folderNameTranTemp[0])
            fileNameTranTemp = raw_input('Input the shared part of all your transmitting file names (without underscore) and enter:')
            self.fileNameTran.append(fileNameTranTemp)

        ini_temp = raw_input('Are you the one who initiate the transmission? y/n and enter:')
        if ini_temp == 'y' or ini_temp == 'Y' or ini_temp == 'yes':
            self.ini = 1
        raw_input('Configuration done. Press enter to begin the transmission:')


    ##################################################################
    # listen to a port for all possible incoming connections
    # write the receiving messages to files, naming with the ip of incoming connection
    # files from different users are stored in separate folders, naming with the ip of incoming connection
    ##################################################################
    def receive(self):
        print 'receive() begins'
        i = 0
        sockRecv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sockRecv.bind((self.myIp, self.myPort))
        sockRecv.listen(self.maxConnect)

        dict_customer = {}

        while self.quitFlag == 0:
            print 'enter receive()'
            connection, addr = sockRecv.accept()

            if addr[0] == self.myIp:  # the signal for exit or quit
                break
            print 'accepted'
            print self.hostName + ' accepts a connection from:' + str(addr)
            fileNameRecvTemp = socket.gethostbyaddr(addr[0])
            print 'peer name is:', fileNameRecvTemp[0]
            if fileNameRecvTemp[0] in dict_customer:
                dict_customer[fileNameRecvTemp[0]] += 1
            else:
                dict_customer[fileNameRecvTemp[0]] = 1
                os.mkdir('fileRecv/' + fileNameRecvTemp[0])
            fd = open('./fileRecv/' + fileNameRecvTemp[0] + '/' + fileNameRecvTemp[0] + '_' + str(
                    dict_customer[fileNameRecvTemp[0]]) + '.txt', 'w')
            #self.fileNameRecv = socket.gethostbyaddr(addr[0])
            #print 'peer name is:', self.fileNameRecv[0]
            # if self.fileNameRecv[0] in dict_customer:
            #     dict_customer[self.fileNameRecv[0]] += 1
            # else:
            #     dict_customer[self.fileNameRecv[0]] = 1
            #     os.mkdir('fileRecv/'+ self.fileNameRecv[0])
            # fd = open('./fileRecv/' + self.fileNameRecv[0] + '/' + self.fileNameRecv[0] + '_' + str(dict_customer[self.fileNameRecv[0]]) + '.txt', 'w')
            print self.hostName + ' is receiving:'
            buf = connection.recv(self.recvBufSize)
            while buf:
                sys.stdout.softspace = 0  # avoid space between two buffer prints
                print buf
                fd.write(buf)
                buf = connection.recv(self.recvBufSize)
            connection.send('feedback: ' + self.hostName + ' has received ' + fileNameRecvTemp[0] + '_' + str(dict_customer[fileNameRecvTemp[0]]) + '.txt')
            self.fileNameRecv.append(fileNameRecvTemp[0])
            connection.close()
        sockRecv.close()
        print 'receive() done'


    ##################################################################
    # check if the last file expected from its peer is received,
    # if yes, then transmit the current file to its peer
    ##################################################################
    def transmit(self):

        i = 0
        print 'transmit() begins'
        while self.exitFlag == 0:
            for k in range(int(self.numOfPairs)):
                print '0000000000000', self.fileNameTran[k]
                print '1111111111111', self.folderNameTran[k]
                if(i > 0):
                    print '2222222222222', self.fileNameRecv[k]
                time.sleep(3)
                if (i == 0 and self.ini == 1):
                    print '============ 1 ============'
                if (i > 0 and os.path.exists('./fileRecv/' + self.fileNameRecv[k] + '/' + self.fileNameRecv[k] + '_' + str(i) + '.txt')):
                    print '============= 2 =========='
                    print './fileRecv/' + self.fileNameRecv[k] + '/' + self.fileNameRecv[k] + '_' + str(i) + '.txt'
                if os.path.isfile('./fileTran/' + self.folderNameTran[k] + '/' + self.fileNameTran[k] + '_' + str(i+1) + '.txt'):
                    print '============== 3 =========='
                    print './fileTran/' + self.folderNameTran[k] + '/' + self.fileNameTran[k] + '_' + str(i+1) + '.txt'

                if ((i == 0 and self.ini == 1) or (i > 0 and os.path.exists('./fileRecv/' + self.fileNameRecv[k] + '/' + self.fileNameRecv[k] + '_' + str(i) + '.txt'))) \
                            and os.path.isfile('./fileTran/' + self.folderNameTran[k] + '/' + self.fileNameTran[k] + '_' + str(i+1) + '.txt'):
                    print 'enter transmit()'
                    time.sleep(2)
                    i = i + 1
                    print 'going to send: ' + './fileTran/' + self.folderNameTran[k] + '/' + self.fileNameTran[k] + '_' + str(i) + '.txt'
                    isConnected = 0       # if 1: host is connected to server
                    #for j in range(self.timeOut):
                    j = 1
                    while j <= self.timeOut and isConnected == 0:
                        #if isConnected == 0:
                        print 'j= ', str(j)
                        sockTran = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket creation must be in for loop
                        try:
                            sockTran.connect((self.peerIp, self.peerPort))
                            print 'connected'
                            isConnected = 1
                        except:
                            print 'connecting...'
                            time.sleep(self.interval)
                            #continue
                            j = j + 1
                    fd = open('./fileTran/' + self.folderNameTran[k] + '/' + self.fileNameTran[k] + '_' + str(i) + '.txt', 'r')
                    line = fd.readline()
                    while line:
                        sockTran.send(line)
                        print line,
                        line = fd.readline()
                    sockTran.close()
        print 'transmit() done'

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
                    lock.acquire()
                    self.exitFlag = 1
                    lock.release()
                    print self.hostName + ' \'s transmission finished'
                elif instruction == 'q':
                    print 'server closed'
                    lock.acquire()
                    self.quitFlag = 1
                    lock.release()
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
if __name__ == '__main__':

    testComm = Comm()

    #shutil.move('./fileTran/beibei-optiplex-390.ecee.dhcp.asu.edu','./fileTran/entity_1')
    # shutil.move('./fileTran/beibeis-mbp.mobile.asu.edu', './fileTran/entity_2')

    testComm.config()
    threads = []
    lock = threading.Lock()
    t1 = threading.Thread(target=testComm.receive)
    t2 = threading.Thread(target=testComm.transmit)
    t3 = threading.Thread(target=testComm.terminate)
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)

    for t in threads:
        t.start()
    t2.join()
    t3.join()

