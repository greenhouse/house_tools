__filename = 'termprint.py'
__fname = 'termprint'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')

from .xlogger import *
import os
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
#import appscript # $ python3.7 -m pip install appscript

logenter(__filename, f" IMPORTs complete:- STARTING -> file '{__filename}' . . . ", simpleprint=True, tprint=True)

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

loginfo(__filename, f"\n CLASSES & FUNCTIONS initialized:- STARTING -> additional '{__filename}' run scripts (if applicable) . . .", simpleprint=True)
loginfo(__filename, f"\n  DONE Executing additional '{__filename}' run scripts ...", simpleprint=False)
print('#======================================================================#')
