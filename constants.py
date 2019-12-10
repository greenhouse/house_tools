__filename = 'constants.py'
__fname = 'constants'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print('GO {__filename} -> starting IMPORTs and globals decleration')

#=======================================================================#
                # json error key/values #
kErrArgs = "err_args"
kErrDb = "err_db"
kErrDbUsrExists = "err_db user exists"
kErrDbUsrNotExists = "err_db user not exists"
kErrS3 = "err_storage"
kErrMisc = "err_misc_server_unknown"
kErrPin = "err_invalid_pin"

vErrNone = 0
vErrArgs = 1
vErrDb = 2
vErrS3 = 3
vErrMisc = 4
vErrPin = 5
#=======================================================================#

#=======================================================================#
                # json error response variables #

err_resp_args = {'ERROR':vErrArgs, 'MSG':kErrArgs}
err_resp_db = {'ERROR':vErrDb, 'MSG':kErrDb, 'PAYLOAD':{'error':vErrDb}}
err_resp_db_usr_exist = {'ERROR':vErrDb, 'MSG':kErrDbUsrExists, 'PAYLOAD':{'error':vErrDb}}
err_resp_db_usr_not_exist = {'ERROR':vErrDb, 'MSG':kErrDbUsrNotExists, 'PAYLOAD':{'error':vErrDb}}
err_resp_s3 = {'ERROR':vErrS3, 'MSG':kErrS3, 'PAYLOAD':{'error':vErrS3}}
err_resp_misc = {'ERROR':vErrMisc, 'MSG':kErrMisc}
err_resp_pin = {'ERROR':vErrPin, 'MSG':kErrPin}

#=======================================================================#

#=======================================================================#
                # Common request keys #
#=======================================================================#

#=======================================================================#
                # Common request values #
#=======================================================================#

#=======================================================================#
                # Common database columns #
#=======================================================================#
#=======================================================================#

#=======================================================================#
                # Common database query keys #
#=======================================================================#
#=======================================================================#

# constants
cStrSpace = '   '
cStrDivider = '#----------------------------------------------------------------------------------------------------#'
cStrDivider2 = '#====================================================================================================#'
cStrDivider01 = cStrDivider
cStrDivider02 = '%s\n%s' % (cStrDivider,cStrDivider)

cStrExtSpace13 = '%s%s%s%s%s%s%s%s%s%s%s%s%s'%(cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace)
cStrExtSpace10 = '%s%s%s%s%s%s%s%s%s%s'%(cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace)
cStrExtSpace08 = '%s%s%s%s%s%s%s%s'%(cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace)
cStrExtSpace06 = '%s%s%s%s%s%s'%(cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace)
cStrExtSpace05 = '%s%s%s%s%s'%(cStrSpace,cStrSpace,cStrSpace,cStrSpace,cStrSpace)
cStrExtSpace04 = '%s%s%s%s'%(cStrSpace,cStrSpace,cStrSpace,cStrSpace)
cStrExtSpace03 = '%s%s%s'%(cStrSpace,cStrSpace,cStrSpace)
cStrExtSpace02 = '%s%s'%(cStrSpace,cStrSpace)
cStrExtSpace01 = '%s'%(cStrSpace,)
cStrExtSpace00 = ''

