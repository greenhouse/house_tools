__filename = 'print_helpers.py'
cStrDividerExcept = '***************************************************************'
import sys
import decimal
import json
from flask import Response

def JSONResponse(dict):
    return Response(json.dumps(dict), mimetype="application/json" )

# split, strip, join
def stripStrWhiteSpaceByLine(strfix):
    funcname = f'<{__filename}> stripStrWhiteSpaceByLine'
    print(f'\n{funcname} _ ENTER\n')
    lst_strfix = strfix.split('\n')
    lst_strfix_strip = []
    for x in lst_strfix:
        lst_strfix_strip.append(x.strip())
    strfixstrip = '\n'.join(lst_strfix_strip)
    print(f'\n{funcname} _ EXIT\n')
    return strfixstrip

##ref: https://stackoverflow.com/a/39165933/2298002
def truncate(number, digits, bDecReturn=False):
    decimal.getcontext().rounding = decimal.ROUND_DOWN #default -> 'ROUND_HALF_EVEN'
    dec = decimal.Decimal(number)
    decTrunc1 = round(dec, digits+1)
    decTrunc2 = round(decTrunc1, digits)
    decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN #default -> 'ROUND_HALF_EVEN'

    if bDecReturn:
        return decTrunc2
    return float(decTrunc2)

def printException(e, debugLvl=0):
    #print type(e)       # the exception instance
    #print e.args        # arguments stored in .args
    #print e             # __str__ allows args to be printed directly
    print('', cStrDividerExcept, f' Exception Caught _ e: {e}', cStrDividerExcept, sep='\n')
    if debugLvl > 0:
        print('', cStrDividerExcept, f' Exception Caught _ e.args: {e.args}', cStrDividerExcept, sep='\n')
    if debugLvl > 1:
        print('', cStrDividerExcept, f' Exception Caught _ type(e): {type(e)}', cStrDividerExcept, sep='\n')

def readCliArgs():
    funcname = f'<{__filename}> readCliArgs'
    #print(f'\n{funcname} _ ENTER\n')
    print(f'\nReading CLI args...')
    argCnt = len(sys.argv)
    print(' Number of arguments: %i' % argCnt)
    print(' Argument List: %s' % str(sys.argv))
    for idx, val in enumerate(sys.argv):
        print(' Argv[%i]: %s' % (idx,str(sys.argv[idx])))
    print(f'DONE reading CLI args...')
    #print(f'\n{funcname} _ EXIT\n')

def getPrintListStr(lst=[], strListTitle='list', useEnumerate=True, goIdxPrint=False, goPrint=True):
    strGoIndexPrint = None
    if goIdxPrint:
        strGoIndexPrint = '(w/ indexes)'
    else:
        strGoIndexPrint = '(w/o indexes)'

    lst_str = None
    if useEnumerate:
        if goIdxPrint:
            lst_str = [f'{i}: {v}' for i,v in enumerate(lst)]
        else:
            lst_str = [f'{v}' for i,v in enumerate(lst)]
    else:
        if goIdxPrint:
            lst_str = [f'{lst.index(x)}: {x}' for x in lst]
        else:
            lst_str = [f'{x}' for x in lst]

    lst_len = len(lst)
    print(f'{strListTitle} _ {strGoIndexPrint} _ count {lst_len}:', *lst_str, sep = "\n ")
    return lst_str

def getPrintListStrTuple(lst=[], strListTitle='list', useEnumerate=True, goIdxPrint=False, goPrint=True):
    strGoIndexPrint = None
    if goIdxPrint:
        strGoIndexPrint = '(w/ indexes)'
    else:
        strGoIndexPrint = '(w/o indexes)'

    lst_str = None
    if useEnumerate:
        if goIdxPrint:
            lst_str = [f"{i}: {', '.join(map(str,v))}" for i,v in enumerate(lst)]
        else:
            lst_str = [f"{', '.join(map(str,v))}" for i,v in enumerate(lst)]
    else:
        if goIdxPrint:
            lst_str = [f"{lst.index(x)}: {', '.join(map(str,x))}" for x in lst]
        else:
            lst_str = [f"{', '.join(map(str,x))}" for x in lst]

    lst_len = len(lst)
    print(f'{strListTitle} _ {strGoIndexPrint} _ count {lst_len}:\n', *lst_str, sep = "\n ")
    return lst_str

