__filename = 'print_helpers.py'
cStrDividerExcept = '***************************************************************'
cStrDivider = '#================================================================#'
print(f'GO {__filename} -> starting IMPORTs')
import random
from flask import Response
import sys, os, traceback
import decimal
import json

def getStrJsonPretty(miscJson={}):
    funcname = f'<{__filename}> strJsonPretty'
    #print('\n',funcname,' _ ENTER\n')
    strJsonPrint = json.dumps(miscJson, indent = 4)
    #strLineD = '\n%s__data__\n%s\n%s__data__\n' % (cStrExtSpace01,str(strJsonPrint),cStrExtSpace01)
    #strLineD = '%s__data__\n%s' % (cStrExtSpace01,str(strJsonPrint))
    strLineD = f' __data__\n{strJsonPrint}'
    return strLineD

def JSONResponse(dict):
    return Response(json.dumps(dict), mimetype="application/json" )

def printEndAndExit(source_func, exit_code=-1):
    print('', cStrDivider, f'END _ {source_func} _ sys.exit({exit_code})', cStrDivider, '', sep='\n')
    sys.exit(exit_code)

#ref: https://stackoverflow.com/a/3568748/2298002
def randomizeString(strInput):
    print(f'input string:  {strInput}')
    strOutput = ''.join([str(w) for w in random.sample(strInput, len(strInput))])
    print(f'output string: {strOutput}')
    return strOutput

def stripStrWhiteSpaceInDict(dictStr):
    funcname = f'<{__filename}> stripStrWhiteSpaceInDict'
    print(f'\n{funcname} _ ENTER')
    dict_strip = {}
    for key in dictStr:
        strfix = str(dictStr[key])
        dict_strip[key] = stripStrWhiteSpaceByLine(strfix)
    print(f'{funcname} _ EXIT', '\n')
    return dict_strip

# split, strip, join
def stripStrWhiteSpaceByLine(strfix):
    funcname = f'<{__filename}> stripStrWhiteSpaceByLine'
    #print(f'\n{funcname} _ ENTER')
    lst_strfix = strfix.split('\n')
    lst_strfix_strip = []
    for x in lst_strfix:
        lst_strfix_strip.append(x.strip())
    strfixstrip = '\n'.join(lst_strfix_strip)
    #print(f'{funcname} _ EXIT', '\n')
    return strfixstrip

#ref: https://stackoverflow.com/a/39165933/2298002
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
    
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#    print(traceback.format_exc())
    strTrace = traceback.format_exc()
    #print(exc_type, fname, exc_tb.tb_lineno)
    print('', cStrDividerExcept, f' type: {exc_type}', f' file: {fname}', f' line_no: {exc_tb.tb_lineno}', f' traceback: {strTrace}', cStrDividerExcept, sep='\n')

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

