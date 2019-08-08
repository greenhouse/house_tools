# house_tools
    misc utilities for python scripting support

# print_helpers.py
### def JSONResponse(dict):
### return json formatted string 
### mimetype="application/json"
    example...
    >>> lst = [1, 2, 3, 4]
    >>> dict = {'error':'none', 'payload':{'msg':'hello world', 'msg2':lst}}
    >>> JSONResponse(dict)
    "{
        'error':'none', 
        'payload': {
            'msg':'hello world', 
            'msg2': [
                        1, 
                        2, 
                        3, 
                        4
                   ]
            }
     }"

def stripStrWhiteSpaceByLine(strfix):
### strip leading & trailing whitespaces from multi-lined string
### split, strip, join 
    
        example...
            >>> strfix = '    hello    \n     world     \n     my friend    '
            >>> strnew = stripStrWhiteSpaceByLine(strfix)
            >>> strnew
            'hello\nworld\nmy friend'

### truncate number to specified decimal digits amount (rounds down)
### ref: https://stackoverflow.com/a/39165933/2298002
    def truncate(number, digits, bDecReturn=False):
        example.. bDecReturn=False, returns float, else returns 'import decimal'
            >>> fVal = 0.12345
            >>> iDecPlace = 4
            >>> truncate(fVal, iDecPlace, bDecReturn=False)
            0.1234

### support method, neatly print Exception 'e'  
    def printException(e, debugLvl=0):
        example...
            >>> e = Exception 
            >>> printException(e, debugLvl=0)
            ' Exception Caught _ e: {e}'
            >>> printException(e, debugLvl=1)
            ' Exception Caught _ e.args: {e.args}'
            >>> printException(e, debugLvl=2)
            ' Exception Caught _ type(e): {type(e)}'

### read and print cli args from user input
    def readCliArgs():
        example...
         $ python3.7 test.py -a hello -b world
             Reading CLI args...
             Number of arguments: 5
             Argument List: ['test.py', '-a', 'hello', '-b', 'world']
             Argv[0]: test.py
             Argv[1]: -h
             Argv[2]: hello
             Argv[3]: -b
             Argv[4]: world
             DONE reading CLI args...

### given a list.. creates, prints & returns that list in string format
### option to print list indexes
### defaults to utilize list comprehention with 'enumerate'
    def getPrintListStr(lst=[], strListTitle='list', useEnumerate=True, goIdxPrint=False, goPrint=True):
        example...
            >>> lst = ['hello world', 'this is a test', 3, 4]
            >>> strListTitle = 'test print my list'
            >>> lstStr = getPrintListStr(lst, strListTitle='list', goIdxPrint=False)
            test print my list _ (w/o indexes) _ count 4:
            hello world
            this is a test
            3
            4
            >>> lstStr
            ['hello world', 'this is a test', '3', '4']
            
            >>> lstStr = getPrintListStr(lst=[], strListTitle='list', goIdxPrint=True)
            test print my list _ (w/ indexes) _ count 4:
            0: hello world
            1: this is a test
            2: 3
            3: 4
            >>> lstStr
            ['hello world', 'this is a test', '3', '4']
            


### given a list of tuples.. creates, prints & returns that list in string format
### option to print list indexes
### defaults to utilize list comprehention with 'enumerate'
    def getPrintListStrTuple(lst=[], strListTitle='list', useEnumerate=True, goIdxPrint=False, goPrint=True):
        example...
            >>> lst_up = [('hello world',), ('this', 'is', 'a test'), (3,), (4, 5)]
            >>> strListTitle = 'test print my list tup'
            >>> lstTupStr = getPrintListStr(lst_up, strListTitle, goIdxPrint=False)
            test print my list tup _ (w/o indexes) _ count 4:
            ('hello world',)
            ('this', 'is', 'a test')
            (3,)
            (4, 5)
            >>> lstTupStr
            ['(hello world)', '(this, is, a test)', '(3)', '(4, 5)']
            
            >>> lstTupStr = getPrintListStr(lst=[], strListTitle='list', goIdxPrint=True)
            test print my list tup _ (w/ indexes) _ count 4:
            0: ('hello', 'world')
            1: ('this', 'is', 'a test')
            2: (3,)
            4: (4, 5)
            >>> lstTupStr
            ['(hello world)', '(this, is, a test)', '(3)', '(4, 5)']




_END_
