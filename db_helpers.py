__filename = 'db_helpers.py'
cStrDivider = '#================================================================#'
print(f'GO {__filename} -> starting IMPORTs')

import sites #required: sites/__init__.py
from .xlogger import *
#from utilities import * #imports 'from sites import *'
#import json
#from flask import Response
#from re import *

'''
# https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
# https://docs.sqlalchemy.org/en/13/dialects/mysql.html#module-sqlalchemy.dialects.mysql.pymysql
    mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
# https://pymysql.readthedocs.io/en/latest/user/examples.html
    #NOTE: '$ pip3' == '$ python3.6 -m pip'
        $ python3 -m pip install PyMySQL
        $ python3.7 -m pip install PyMySQL
    '''
import pymysql.cursors

logenter(__filename, " IMPORTs complete:- STARTING -> file '{__filename}' . . . ", simpleprint=True, tprint=True)

#db_connect from sites/__init__.py
dbUser = sites.dbUserGms
dbPw = sites.dbPwGms
dbName = sites.dbNameGms
dbHost = sites.dbHostGms

db = None
cur = None

strErrCursor = "global var cur == None, returning -1"
strErrConn = "FAILED to connect to db"

#====================================================#
##              db connection support               ##
#====================================================#
def open_database_connection():
    funcname = f'({__filename}) open_database_connection'
    logenter(funcname, simpleprint=False, tprint=False)

    # Connect to DB #
    try:
        global db, cur

        # legacy manual db connection #
        db = pymysql.connect(host=dbHost,
                             user=dbUser,
                             password=dbPw,
                             db=dbName,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()

        if cur == None:
            logerror(funcname, "database cursor received (cur) == None; returning None", "FAILED to connect to db", simpleprint=False)
            return -1

        loginfo(funcname, ' >> CONNECTED >> to db successfully!', simpleprint=True)
    except:
        logerror(funcname, "exception hit", "FAILED to connect to db", simpleprint=False)
        return -1
    finally:
        return 0

def close_database_connection():
    funcname = f'({__filename}) close_database_connection'
    logenter(funcname, simpleprint=False, tprint=False)

    global db, cur
    if db == None:
        logerror(funcname, "global var db == None; returning", "FAILED to close db connection", simpleprint=False)
        return

    db.commit()
    db.close()

    db = None
    cur = None
    loginfo(funcname, ' >> CLOSED >> db successfully!', simpleprint=True)

def procValidatePIN(strPIN=''):
    funcname = f'({__filename}) procValidatePIN({strPIN})'
    logenter(funcname, simpleprint=False, tprint=True)

    #============ open db connection ===============#
    global cur
    if open_database_connection() < 0:
        return -1

    if cur == None:
        logerror(funcname, strErrCursor, strErrConn, simpleprint=False)
        return -1

    #============ perform db query ===============#
    try:
        strOutResult = ''
#        argsTup = (strPIN,strOutResult)
        argsTup = (strPIN,'p_out')
        procArgs = cur.callproc(f"ValidatePIN", argsTup)
        loginfo(funcname, f" >> '{funcname}' RESULT procArgs: {procArgs};", simpleprint=True)
        rowCnt = cur.execute(f"select @_ValidatePIN_1;")
        rows = cur.fetchall()
        
#        rowCnt = cur.execute(f"call ValidatePIN({strPIN});")
#        rows = cur.fetchall()
        loginfo(funcname, f" >> '{funcname}' RESULT rowCnt: {rowCnt};", simpleprint=True)

        print(f' >> Printing... rows', *rows, sep='\n ')
        print(f' >> Printing... rows[0]:', rows[0])
#        result = rows
#        lst_result = [elem for elem in rows[0].values()]
#        result = int(rows[0]['result'])
        result = int(rows[0]['@_ValidatePIN_1'])
    
#        result = procArgs
    except Exception as e: # ref: https://docs.python.org/2/tutorial/errors.html
        #============ handle db exceptions ===============#
        strE_0 = f"Exception hit... \nFAILED to call '{funcname}'; \n\nreturning -1"
        strE_1 = f"\n __Exception__: \n{e}\n __Exception__"
        logerror(funcname, strE_0, strE_1, simpleprint=False)
        result = -1
    finally:
        #============ close db connection ===============#
        close_database_connection()

        return result

#====================================================#
#====================================================#

loginfo(__filename, f"\n CLASSES & FUNCTIONS initialized:- STARTING -> additional '{__filename}' run scripts (if applicable) . . . \n\n", simpleprint=True)
print('\n')
print('#======================================================================#')
loginfo(__filename, f"\n  DONE Executing additional '{__filename}' run scripts ... \n", simpleprint=True)
