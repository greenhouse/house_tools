__filename = 'email_smtp.py'
print(f'GO {__filename} -> starting IMPORTs')
from .xlogger import *
import os
import re
from random import randrange
from datetime import datetime, timedelta
from flask import render_template
import smtplib

logenter(__filename, f"\n IMPORTs complete:- STARTING -> file '{__filename}' . . . ", simpleprint=False, tprint=True)

SES_SERVER = sites.gms_SES_SERVER
SES_PORT = sites.gms_SES_PORT
SES_FROMADDR = sites.gms_SES_FROMADDR
SES_LOGIN = sites.gms_SES_LOGIN
SES_PASSWORD = sites.gms_SES_PASSWORD

SES_ADMIN = sites.gms_admin_email
SES_RECEIVER = sites.gms_post_receiver

def sendEmailTest(test_id=-1, dev_msg='nil'):
    funcname = f'({__filename}) sendEmailTest'
    receiver = SES_RECEIVER
    sender = SES_ADMIN
    subject = f"server test email [{test_id}]"
    body = f"Server test email body...\n\n\n     dev_msg: {dev_msg}\n\n\n _END_\n\n"
    sendTextEmail(sender, receiver, subject, body)

def sendGmsPostSumbit(iType=0, uname='uname_nil', strTime='time_nil', title='title_nil', strHtml='html_nil'):
    funcname = f'({__filename}) sendEmailTest'
    receiver = SES_RECEIVER
    sender = SES_ADMIN

    strType = "unknown"
    if iType == 1: # job
        strType = 'job'
    if iType == 2: # candidate
        strType = 'cand'
    
    subject = f"GMS_post_{strType}_{uname}_{strTime}"
    body = f"{title}\n\n{strHtml}\n\n_END_\n\n"
    sendTextEmail(sender, receiver, subject, body)

#=====================================================#
# legacy misc
#=====================================================#
def sendEmailServerErrorDb(sourceFunc, dbquery, dev_msg):
    funcname = f'({__filename}) sendEmailServerErrorDb'
    receiver = SES_ADMIN
    sender = SES_ADMIN
    subject = f"server ERROR->DB! [func: {sourceFunc}]"
    body = f"Server database error occurred during...\n\n\n     dbquery: {sourceFunc}\n\n\n within function: {dbquery}\n\n Developer Msg: {dev_msg}\n\n"
    sendTextEmail(sender, receiver, subject, body)

def sendEmailServerException(sourceFunc, e, code_msg):
    funcname = f'({__filename}) sendEmailServerException'
    receiver = SES_ADMIN
    sender = SES_ADMIN
    subject = f"server EXCEPTION! [func: {sourceFunc}]"
    body = f"Server exception occurred within function: {sourceFunc}\n\n Python Code Msg: {code_msg}\n\n\n [exception_]: \n{e}\n[_exception]"
    sendTextEmail(sender, receiver, subject, body)


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


def sendTextEmail(sender_email, recipient_email, subject, text):
    funcname = f'({__filename}) sendTextEmail'
    funparams = f"From: {sender_email}\r\nTo: %s\r\nSubject: {subject}\r\nBody: \n{text}\n\n" % ",".join([recipient_email])
    #logenter(funcname, funparams, simpleprint=False, tprint=True)
    loginfo(funcname, 'START -> sendTextEmail', simpleprint=True)
    try:
        msg = f"From: {sender_email}\r\nTo: %s\r\nSubject: {subject}\r\n\r\n" % ",".join([recipient_email])
        server = smtplib.SMTP_SSL(SES_SERVER, SES_PORT)
        #server.set_debuglevel(1)
        server.ehlo()
        server.login(SES_LOGIN, SES_PASSWORD)
        logalert(funcname, 'START -> server.sendmail', simpleprint=False)
        logalert(funcname, f'msg... \n {msg}\n', simpleprint=False)
        #logalert(funcname, f'text... \n {text}\n', simpleprint=False)
        server.sendmail(sender_email, recipient_email, msg + text)
        logalert(funcname, 'END -> server.sendmail', simpleprint=False)
        server.quit()
        loginfo(funcname, 'END -> sendTextEmail SUCCESS', '\n', simpleprint=True)
        return True

    except Exception as e: # ref: https://docs.python.org/2/tutorial/errors.html
        #print type(e)       # the exception instance
        #print e.args        # arguments stored in .args
        #print e             # __str__ allows args to be printed directly
        iDebugLvl = 3
        logerror(funcname, f"  Exception caught during send email attempt: {e} \n", f"\n  attempting to re-send email with 'server.set_debuglevel({iDebugLvl})' enabled\n")
        try:
            msg = f"From: {sender_email}\r\nTo: %s\r\nSubject: {subject}\r\n\r\n" % ",".join([recipient_email])
            server = smtplib.SMTP_SSL(SES_SERVER, SES_PORT)
            server.set_debuglevel(iDebugLvl)
            server.ehlo()
            server.login(SES_LOGIN, SES_PASSWORD)
            server.sendmail(sender_email, recipient_email, msg + text)
            server.quit()
            loginfo(logfuncname, 're-send email succeeded this time! wtf?!?', f'FuncParamsPassed... \n{funparams}\n')
            return True
        except Exception as e:
            logerror(funcname, f"  email re-send Exception... \n{e}\n  returning False and continuing callstack\n", f"\nFuncParamsPassed... \n{funparams}\n")
            return False

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
