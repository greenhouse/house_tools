__filename = 'termprint.py'
cStrDivider = '#================================================================#'
print(f'GO {__filename} -> starting IMPORTs')

from .xlogger import *
import os
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
#import appscript # $ python3.7 -m pip install appscript

logenter(__filename, " IMPORTs complete:- STARTING -> file '{__filename}' . . . ", simpleprint=True, tprint=True)

def printToCLI(strMsg,strTTY):
    funcname = f'({__filename}) printToCLI'
    if strTTY == '':
        logalert(funcname, "found strTTY == '' returning w/o spawning new thread", tprint=False)
        return

    thread = threading.Thread(target = goTerminalTTY, args = (strMsg,strTTY))
    thread.start()

def goTerminalTTY(strMsg,strTermTTY):
    funcname = f'{__filename}) goTerminalTTY'
    if len(strTermTTY) > 0:
        #os.system("echo '{strMsg}' > {strTermTTY}")
        os.system("echo '{strMsg}' {strTermTTY}")

# '$ python3.7 depthsock.py TRX -p 15'
def launchTerminalPython(pyPath, strArgs):
    #example... >>> ascript = 'python3.7 ~/devbtc/git/altcoins/binance/depthsock.py TRX -p 15'
    ascript = f'python3.7 {pyPath} {strArgs}'
    appscript.app('Terminal').do_script(ascript)

