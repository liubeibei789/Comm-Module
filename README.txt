README

This is a multi-threaded communication python script (python 2.7),
transmitting a series of files one by one to another machine,
while receiving files from any incoming connection.

author: Beibei Liu (liubeibei789@gmail.com)
created: 03/2018

******* architecture *******:

/Comm/
----/Comm.py
----/FileTran/
----/FileRecv/
----/README.txt

******* functions *******:

Comm.py: the python script to run
FileTran/: the folder to put the files to be transmitted
FileRecv/: the folder where received files are located
README.txt: instructions

******* instructions on running this script *******:

1. Change your directory to the ../Comm/, otherwise it can not find the FileTran/ and FileRecv/ folder

2. Put all the txt files you to transmit in FileTran/ folder.
   Name the files with a sequence number as suffix (e.g. FileTran_1.txt, FileTran_2.txt...)
   Check the FileRecv/ folder to make sure it is cleared before running the script.

3. Type: sudo(optional) python Comm.py followed by two parameters separated by a space,

parameter 1: host name. It can be any name you like (e.g. PowerEnd, WaterEnd...)

parameter 2: ip address of the target machine. Type 'ipconfig' in command window/terminal of the target machine,
find out the item 'ipv4 address: xxx.xxx.xxx.xxx', it is the ip address of this machine (e.g. 10.144.153.230).

(note: sudo is added only when you are in linux environment)




