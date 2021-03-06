#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import logging
import asyncore, socket
from time import time
from bitstring import ConstBitStream
import coords
 
logging.basicConfig(level=logging.DEBUG, format="%(filename)s: %(funcName)s - %(levelname)s: %(message)s")
 
# \brief Implementation of the server side connection for 'Stellarium Telescope Protocol'

#  Manages the execution thread to the server side connection with Stellarium
class Telescope_Channel(asyncore.dispatcher): 
    ## Class constructor
    #
    # \param conn_sock Connection socket
    def __init__(self, conn_sock, queue):
        self.is_writable = False
        self.buffer = ''
        asyncore.dispatcher.__init__(self, conn_sock)
        self.queue = queue
 
    ## Indicates the socket is readable
    #
    # \return Boolean True/False
    def readable(self):
        return True
 
    ## Indicates the socket is writable
    #
    # \return Boolean True/False
    def writable(self):
        return self.is_writable
 
    ## Close connection handler
    #
    def handle_close(self):
        logging.debug("Disconnected")
        self.close()
 
    ## Reading socket handler
    #    
    # Reads and processes client data, and throws the proper signal with coordinates as parameters
    def handle_read(self):
        #format: 20 bytes in total. Size: intle:16
        #Incomming messages comes with 160 bytes..
        data0 = self.recv(160)
        if data0:            
            data = ConstBitStream(bytes=data0, length=160)
            # print ("All: %s" % data.bin)
 
            msize = data.read('intle:16')
            mtype = data.read('intle:16')
            mtime = data.read('intle:64')
 
            # RA: 
            ant_pos = data.bitpos
            ra = data.read('hex:32')
            data.bitpos = ant_pos
            ra_uint = data.read('uintle:32')
 
            # DEC:
            ant_pos = data.bitpos
            dec = data.read('hex:32')
            data.bitpos = ant_pos
            dec_int = data.read('intle:32')
 
            logging.debug("Size: %d, Type: %d, Time: %d, RA: %d (%s), DEC: %d (%s)" % (msize, mtype, mtime, ra_uint, ra, dec_int, dec))
            (sra, sdec, stime) = coords.eCoords2str(float("%f" % ra_uint), float("%f" % dec_int), float("%f" %  mtime))
 
            logging.debug("sra: %s, Sdec: %s, Stime: %s" % (sra, sdec, stime))
            #Sends back the coordinates to Stellarium
            self.act_pos(coords.hourStr_2_rad(sra), coords.degStr_2_rad(sdec))
            
            self.queue.put([sra, sdec, stime])

 
    ## Updates the field of view indicator in Stellarium
    #
    # \param ra Right ascension in signed string format
    # \param dec Declination in signed string format
    def act_pos(self, ra, dec):
        (ra_p, dec_p) = coords.rad_2_stellarium_protocol(ra, dec)
 
        times = 10 #Number of times that Stellarium expects to receive new coords //Absolutly empiric..
        for i in range(times):
            self.move(ra_p, dec_p)
 
    ## Sends to Stellarium equatorial coordinates
    #
    #  Receives the coordinates in float format. Obtains the timestamp from local time
    #
    # \param ra Ascensi??n recta.
    # \param dec Declinaci??n.
    def move(self, ra, dec):
        msize = '0x1800'
        mtype = '0x0000'
        aux_format_str = 'int:64=%r' % time()
        localtime = ConstBitStream(aux_format_str.replace('.', ''))
        #print "move: (%d, %d)" % (ra, dec)
 
        sdata = ConstBitStream(msize) + ConstBitStream(mtype)
        sdata += ConstBitStream(intle=localtime.intle, length=64) + ConstBitStream(uintle=ra, length=32)
        sdata += ConstBitStream(intle=dec, length=32) + ConstBitStream(intle=0, length=32)
        self.buffer = sdata
        self.is_writable = True
        self.handle_write()
 
    ## Transmission handler
    #
    def handle_write(self):
        self.send(self.buffer.bytes)
        self.is_writable = False
 
## \brief Implementation of the server side communications for 'Stellarium Telescope Protocol'.
#
#  Each connection request generate an independent execution thread as instance of Telescope_Channel
class Telescope_Server(asyncore.dispatcher):
 
    ## Class constructor
    #
    # \param port Port to listen on
    def __init__(self, queue, port=10001):
        asyncore.dispatcher.__init__(self, None)
        self.tel = None
        self.port = port
        self.queue = queue
 
#     ## Starts thread
#     #
#     # Sets the socket to listen on
    def run(self):
        logging.info(self.__class__.__name__+" running.")
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('localhost', self.port))
        self.listen(1)
        self.connected = False
        asyncore.loop()
 
#     ## Handles incomming connection
#     #
#     # Stats a new thread as Telescope_Channel instance, passing it the opened socket as parameter
    def handle_accept(self):
        self.conn, self.addr = self.accept()
        logging.debug('%s Connected', self.addr)
        self.connected = True
        self.tel = Telescope_Channel(self.conn, self.queue)
 
    ## Closes the connection
    #
    def close_socket(self):
        if self.connected:
            self.conn.close()
 
# Run a Telescope Server
if __name__ == '__main__':
    try:
        Server = Telescope_Server()
        Server.run()
    except KeyboardInterrupt:
        logging.debug("\nBye!")