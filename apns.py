__filename = 'apns.py'
__fname = 'apns'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')
from .xlogger import *
import ssl
import json
import socket
import struct
import binascii
import logging
#from controllers import xlogger
#from globals import globals
import sys


#logging.basicConfig(filename=globals.GLOBAL_PATH_DEV_LOGS, level=logging.DEBUG)
#logging.info(' ')
#logging.info('logging started -> controllers.apns.py')
logenter(__filename, f" IMPORTs complete:- STARTING -> file '{__filename}' . . . ", simpleprint=True, tprint=True)

sock = None

###############################################
############ pub - actions ############
###############################################
def sendApnsTokenDictMsg(token, dict, msg, use_dev_cert=False):
    funcname = f'({__filename}) sendApnsTokenDictMsg({token}, {dict}, {msg})'
    logenter(funcname, simpleprint=False, tprint=True)

    certfile = 'apns-prod-noenc.pem'
    if use_dev_cert:
        certfile = 'apns-dev-noenc.pem'

    result = open_apns_socket(certfile, use_dev_cert)
    if result==False:
        logerror(funcname, '\n\n FAILED open_apns_socket', '')
        return False

    payload = {'PAYLOAD':dict, 'aps':{'alert':msg, 'badge':1, 'sound':'default'}}

    try:
        result = send_apns_msg(token, payload)
        if result==False:
            logerror(funcname, '\n\n FAILED send_apns_msg for apns_dt: %s' % token, 'PAYLOAD dict: %s' % dict)
            close_apns_socket()
            return False

        loginfo(funcname, 'push succeeded for ios_apns_token: %s' % token, 'PAYLOAD dict: %s' % dict)
    except Exception as e: # ref: https://docs.python.org/2/tutorial/errors.html
        #print type(e)       # the exception instance
        #print e.args        # arguments stored in .args
        #print e             # __str__ allows args to be printed directly
        logerror(funcname, '\n\n send_apns_msg Exception: %s' % e, '')
        close_apns_socket()
        return False

    close_apns_socket()
    logexit(funcname, '', '')
    return True

###############################################
############ priv - APPLE link ############
###############################################
def open_apns_socket(certfile, use_dev_cert=False):
    funcname = f'({__filename}) open_apns_socket(certfile={certfile})'
    logenter(funcname, simpleprint=False, tprint=True)

    # APNS server address (use 'gateway.push.apple.com' for production server)
    apns_address = ('gateway.push.apple.com', 2195)
    
    if use_dev_cert:
        # APNS server address (use 'gateway.sandbox.push.apple.com' for development server)
        apns_address = ('gateway.sandbox.push.apple.com', 2195)
    
    # create socket and connect to APNS server using SSL
    s = socket.socket()
    
    global sock
    try:
        sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23, certfile=certfile)
    except:
        e = sys.exc_info()[0]
        logerror(funcname, "\n\n EXCEPTION somewhere global sock.wrap_sockets %s" % e, "")
        return False

    try:
        sock.connect(apns_address)
    except:
        e = sys.exc_info()[0]
        logerror(funcname, "\n\n EXCEPTION somewhere global sock.connect %s" % e, "")
        return False

    logging.info(' ')
    logging.info(' ')
    logging.info('APNS SSL connection opened')
    logging.info(' ')

    return True

def send_apns_msg(token, payload):
    funcname = f'({__filename}) send_apns_msg({token}, {payload})'
    logenter(funcname, simpleprint=False, tprint=True)

    try:
        token = binascii.unhexlify(token)    # generate APNS notification packet
    except Exception as e: # ref: https://docs.python.org/2/tutorial/errors.html
        #print type(e)       # the exception instance
        #print e.args        # arguments stored in .args
        #print e             # __str__ allows args to be printed directly
        strE_0 = f"\n\n Exception hit... \n somewhere binascii.unhexlify(token) '{funcname}'; \n\nreturning False\n"
        strE_1 = f"\n\n __Exception__: \n{e}\n __Exception__"
        logerror(funcname, strE_0, strE_1, simpleprint=False)
        return False
    
    try:
        payload = json.dumps(payload)
        fmt = "!cH32sH{0:d}s".format(len(payload))
        #fmt = "!cH32sH{0:d}s".format(len(bytes(payload, "utf-8")))
        #fmt = "!BH32sH%ds".format(len(payload))
    except Exception as e: # ref: https://docs.python.org/2/tutorial/errors.html
        #print type(e)       # the exception instance
        #print e.args        # arguments stored in .args
        #print e             # __str__ allows args to be printed directly
        strE_0 = f"\n\n Exception hit... \n somewhere format(len(payload)) '{funcname}'; \n\nreturning False\n"
        strE_1 = f"\n\n __Exception__: \n{e}\n __Exception__"
        return False

    try:
        cmd = '\x00'
        loginfo(funcname, f'encoding fmt...', simpleprint=True)
        fmt = bytes(fmt, "utf-8")
        loginfo(funcname, f'encoding fmt... DONE', simpleprint=True)
        loginfo(funcname, f'encoding cmd...', simpleprint=True)
        cmd = bytes(cmd, "utf-8")
        loginfo(funcname, f'encoding cmd... DONE', simpleprint=True)
        loginfo(funcname, f'encoding payload...', simpleprint=True)
        payload = bytes(payload, "utf-8")
        loginfo(funcname, f'encoding payload... DONE', simpleprint=True)
        loginfo(funcname, f'encoding token...', simpleprint=True)
        token = bytes(token, "utf-8")
        loginfo(funcname, f'encoding token... DONE', simpleprint=True)
        msg = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
        #msg = struct.pack(fmt, cmd, len(token), token, len(payload), bytes(payload, "utf-8"))
        #msg = struct.pack(fmt, cmd, len(token), token, len(bytes(payload, "utf-8")), payload)
    except Exception as e: # ref: https://docs.python.org/2/tutorial/errors.html
        #print type(e)       # the exception instance
        #print e.args        # arguments stored in .args
        #print e             # __str__ allows args to be printed directly
        strE_0 = f"\n\n Exception hit... \n somewhere struct.pack '{funcname}'; \n\nreturning False\n"
        strE_1 = f"\n\n __Exception__: \n{e}\n __Exception__"
        strE_2 = f"\n\n __Exception__: \n{type(e)}\n __Exception__"
        strE_3 = f"\n\n __Exception__: \n{e.args}\n __Exception__"
        strE_4 = strE_1 + strE_2 + strE_3
        logerror(funcname, strE_0, strE_4, simpleprint=False)
        return False

    loginfo(funcname, 'msg created...', '')
    
    try:
        global sock
        sock.write(msg)
    except:
        logerror(funcname, "EXCEPTION somewhere global sock.write(msg)", "")
        return False

    logexit(funcname, 'Sending APNS finished', '')
    return True

def close_apns_socket():
    funcname = f'({__filename}) close_apns_socket'
    logenter(funcname, simpleprint=False, tprint=True)

    global sock
    if sock:
        sock.close()
    
    logging.info(' ')
    logging.info('APNS SSL connection closed')
    logging.info(' ')
    logging.info(' ')



#====================================================#
#====================================================#

loginfo(__filename, f"\n CLASSES & FUNCTIONS initialized:- STARTING -> additional '{__filename}' run scripts (if applicable) . . .", simpleprint=True)
loginfo(__filename, f"\n  DONE Executing additional '{__filename}' run scripts ...", simpleprint=False)
print('#======================================================================#')
