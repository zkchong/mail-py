#
# Filename: mail2.py
# Note that this script runs on Python2.
# Last modified on 15-Oct-2014.
#
import os
import argparse
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


#-----------------------------------------------------------------------
# This function will send email. 
#-----------------------------------------------------------------------
def send_mail(send_from, send_to, subject, text, files, server, username, password):
    assert type(send_to)==list
    assert type(files)==list
    
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    msg.attach( MIMEText(text) )
    
    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
    
    smtp = smtplib.SMTP(server) #port 465 or 587
    smtp.set_debuglevel(True)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

# ----------------------------------------------------------------------


if __name__ == '__main__': 
    #-----------------------------------------------------------------------
    # Define the command line arguements.
    #-----------------------------------------------------------------------
    parser = argparse.ArgumentParser( argument_default = '')
    parser.add_argument ('--send_from', required = True, help = 'Sender\' email address.') 
    parser.add_argument ('--send_to_list', required = True, help = 'Receiver\' email address.')
    parser.add_argument ('--subject', required = False, help = 'subject of the email.')
    parser.add_argument ('--content', required = False, help = 'Content of the email.')
    parser.add_argument ('--attachment_list', required = False, help = 'File to be attached.')
    parser.add_argument ('--server', required = True, help = 'SMTP server address.')
    parser.add_argument ('--username', required = True, help = 'User''s username.')
    parser.add_argument ('--password', required = True, help = 'User''s password.')
    
    
    #-----------------------------------------------------------------------
    # Verify the arguments
    #-----------------------------------------------------------------------
    arg = parser.parse_args()
    print ("Recived arguement: %s" % arg)

    send_from = arg.send_from
    
    #send_to_list = [s.strip() for s in arg.send_to_list.split(",")]
    send_to_list = arg.send_to_list.split(",")
    
    subject = arg.subject
    content = arg.content
    
    attachment_list = [s.strip() for s in arg.attachment_list.split(",")]
    if arg.attachment_list == '':
        attachment_list = []
    
    server = arg.server
    username = arg.username
    password = arg.password
    
    send_mail(send_from, send_to_list, subject, content, attachment_list, server, username, password)
    
    
        
