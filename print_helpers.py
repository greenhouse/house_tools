__filename = 'print_helpers.py'
import sys

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

