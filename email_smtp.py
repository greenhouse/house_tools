__filename = 'email_smtp.py'
__fname = 'email_smtp'
cStrDivider = '#================================================================#'
print('', cStrDivider, f'START _ {__filename}', cStrDivider, sep='\n')
print(f'GO {__filename} -> starting IMPORTs and globals decleration')
from .xlogger import *
from .print_helpers import *
import os
import re
from random import randrange
from datetime import datetime, timedelta
from flask import render_template
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logenter(__filename, f" IMPORTs complete:- STARTING -> file '{__filename}' . . . ", simpleprint=True, tprint=True)

SES_SERVER = sites.SES_SERVER
SES_PORT = sites.SES_PORT
SES_FROMADDR = sites.SES_FROMADDR
SES_LOGIN = sites.SES_LOGIN
SES_PASSWORD = sites.SES_PASSWORD

SES_CORP_ADMIN = sites.corp_admin_email
SES_CORP_RECEPT = sites.corp_recept_email
SES_ADMIN = sites.admin_email
SES_RECEIVER = sites.post_receiver

def sendEmailTest(test_id=-1, dev_msg='nil'):
    funcname = f'({__filename}) sendEmailTest'
    receivers = [SES_RECEIVER]
    sender = SES_ADMIN
    subject = f"server test email [{test_id}]"
    body = f"Server test email body...\n\n\n     dev_msg: {dev_msg}\n\n\n _END_\n\n"
    return sendTextEmail(sender, receivers, subject, body)

def sendGmsPostConfirm(iType=0, uname='uname_nil', uemail='uemail_nil', strTime='time_nil', title='title_nil', strFormData='form_nil', strSubjAdd=''):
    funcname = f'({__filename}) sendGmsPostConfirm'
    #receivers = [SES_RECEIVER, uemail]
    receivers = [SES_RECEIVER, SES_CORP_ADMIN, SES_CORP_RECEPT, uemail]
    sender = SES_ADMIN

    strType = "unknown"
    if iType == 1: # job
        strType = 'job'
    if iType == 2: # candidate
        strType = 'cand'

    subject = f"GMS_post_{strType}_{uname}_({strSubjAdd})_{strTime}"
    msg = f"Hello {uname}, \nYour post has been successfully submitted for approval. \nThe information for your post is listed below. \nIf you have any questions or concerns, please feel free to 'reply-to-all' in this email!"
    body = f"{msg}\n\n{strFormData}\n\n_END_\n"
    return sendTextEmail(sender, receivers, subject, body)

def sendGmsPostSourceHTML(iType=0, uname='uname_nil', strTime='time_nil', title='title_nil', strHtml='html_nil', strSubjAdd=''):
    funcname = f'({__filename}) sendGmsPostSourceHTML'
    receivers = [SES_RECEIVER]
    sender = SES_ADMIN

    strType = "unknown"
    if iType == 1: # job
        strType = 'job'
    if iType == 2: # candidate
        strType = 'cand'

    subject = f"GMS_post_{strType}_{uname}_({strSubjAdd})_{strTime}_SOURCE"
    body = f"{title}\n\n{strHtml}\n\n_END_\n"
    return sendTextEmail(sender, receivers, subject, body)

#=====================================================#
# legacy misc
#=====================================================#
def sendEmailServerErrorDb(sourceFunc, dbquery, dev_msg):
    funcname = f'({__filename}) sendEmailServerErrorDb'
    receivers = [SES_RECEIVER]
    sender = SES_ADMIN
    subject = f"server ERROR->DB! [func: {sourceFunc}]"
    body = f"Server database error occurred during...\n\n\n     dbquery: {sourceFunc}\n\n\n within function: {dbquery}\n\n Developer Msg: {dev_msg}\n\n"
    sendTextEmail(sender, receivers, subject, body)

def sendEmailServerException(sourceFunc, e, code_msg):
    funcname = f'({__filename}) sendEmailServerException'
    receivers = [SES_RECEIVER]
    sender = SES_ADMIN
    subject = f"GMS_server_EXCEPTION! [func: {sourceFunc}]"
    body = f"Server exception occurred within function: {sourceFunc}\n\n Python Code Msg: {code_msg}\n\n\n [exception_]: \n{e}\n[_exception]"
    sendTextEmail(sender, receivers, subject, body)


#=====================================================#
## LEGACY
#=====================================================#
# Email validator Django uses
email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain

    
def validateEmail(email):
    return None if email == None else email_re.match(email)

def getCode(codeLen):
    charSet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    nchars = len(charSet)

    newCode = list()
    for i in range(codeLen):
        newCode.append(charSet[randrange(0,nchars)])

    return "".join(newCode)

def sendHTMLEmail(sender_email, recipient_email, subject, htmlTemplate, textTemplate, c={}):
    funcname = f'({__filename}) sendHTMLEmail'
    logenter(funcname, simpleprint=False, tprint=True)
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject.encode('utf-8')
    msg['From'] = sender_email.encode('utf-8')
    msg['To'] = recipient_email.encode('utf-8')
    #msg["Date"] = email.Utils.formatdate(localtime=True)

    # Create the body of the message (a plain-text and an HTML version).
    text = render_template(textTemplate, c=c)
    html = render_template(htmlTemplate, c=c)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    #s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    #s.sendmail(me, you, msg.as_string())
    #s.quit()

    server = smtplib.SMTP_SSL(SES_SERVER, SES_PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.login(SES_LOGIN, SES_PASSWORD)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
    
    return True

def sendTextEmail(sender_email, lst_recipients, subject, text):
    funcname = f'({__filename}) sendTextEmail'
    funparams = f"From: {sender_email}\r\nTo: %s\r\nSubject: {subject}\r\nBody: \n{text}" % ",".join(lst_recipients)
    #logenter(funcname, funparams, simpleprint=False, tprint=True)
    loginfo(funcname, f"START -> sendTextEmail w/ subject: '{subject}'", simpleprint=True)
    iDebugLvl = 3
    try:
        # note (RFC 5322): this syntax must remain (i.e. cannot pre-pend new line)
        msg = f"From: {sender_email}\r\nTo: %s\r\nSubject: {subject}\r\n\r\n" % ",".join(lst_recipients)
        server = smtplib.SMTP_SSL(SES_SERVER, SES_PORT)
        #server.set_debuglevel(iDebugLvl)
        server.ehlo()
        server.login(SES_LOGIN, SES_PASSWORD)
        logalert(funcname, f'\nHeader... \n{msg}', simpleprint=True)
        #logalert(funcname, f'\nText... \n{text}', simpleprint=False)
        strMsgEncode = getStrEncodeUTF8(msg + text)
        server.sendmail(sender_email, lst_recipients, strMsgEncode)
        server.quit()
        loginfo(funcname, 'END -> sendTextEmail SUCCESS', '\n', simpleprint=True)
        return True, 'no exception'

    except Exception as e: # ref: https://docs.python.org/2/tutorial/errors.html
        printException(e, debugLvl=2)
        logerror(funcname, f"  Exception caught during Send Email attempt\n", f"\n  ...ATTEMPTING to RE-SEND EMAIL with 'server.set_debuglevel({iDebugLvl})' enabled\n")
        try:
            server = smtplib.SMTP_SSL(SES_SERVER, SES_PORT)
            server.set_debuglevel(iDebugLvl)
            server.ehlo()
            server.login(SES_LOGIN, SES_PASSWORD)
            server.sendmail(sender_email, lst_recipients, msg + text)
            server.quit()
            loginfo(funcname, 're-send email succeeded this time! wtf?', f'FuncParamsPassed... \n{funparams}\n')
            return True, f'no exception on retry; first e: {e}'
        except UnicodeEncodeError as e:
            printException(e, debugLvl=2)
            logerror(funcname, f"  UnicodeEncodeError Exception caught during RE-SEND EMAIL attempt w/ 'server.set_debuglevel({iDebugLvl})' enabled\n", "\n  returning False and continuing callstack")
            return False, f'UnicodeEncodeError exception: {e}'
        except Exception as e:
            printException(e, debugLvl=2)
            strFunParamsRepr = f"\nFuncParamsPassed... repr(funparams)... \n\n{repr(funparams)}\n\n"
            strFuncParams = strFunParamsRepr + f"\nFuncParamsPassed... \n\n{funparams}\n\n"
            logerror(funcname, f"  Exception caught during RE-SEND EMAIL attempt w/ 'server.set_debuglevel({iDebugLvl})' enabled... {e}\n  returning False and continuing callstack", strFuncParams)
            return False, f'exception: {e}'

"""def queueEmail(sender_email, recipient_email, html, text):
    email_form = EmailQueueForm()
    if request.method == 'POST':
        if email_form.validate():
            _sender_email = sender_email
            _recipient_email = recipient_email
            _html = html
            _text = text
            _send_time = email_form.send_time.data
            _subject = email_form.subject.data

            now_time = datetime.now()
            nsec = int(_send_time) * 60
            delta_time = timedelta(seconds=nsec)
            new_send_time = now_time + delta_time

            new_email = EmailQueue(created=datetime.now(), status=0, type=0)
            new_email.sender_email = _sender_email
            new_email.recipient_email = _recipient_email
            new_email.subject = _subject
            new_email.html = _html
            new_email.text = _text
            new_email.send_time = new_send_time
            db.session.add(new_email)
            db.session.commit()
            flash('email added')

    return render_template('home/email_form.html', form=email_form)"""

loginfo(__filename, f"\n CLASSES & FUNCTIONS initialized:- STARTING -> additional '{__filename}' run scripts (if applicable) . . .", simpleprint=True)
loginfo(__filename, f"\n  DONE Executing additional '{__filename}' run scripts ...", simpleprint=False)
print('#======================================================================#')
