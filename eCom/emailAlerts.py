import smtplib
from email.message import EmailMessage

# whenever a person signs in send them a message
sender = "bruisercars145@gmail.com"
password = "Quality@1234"
host = ""


def sendEmail(email,content,subject):
    em = EmailMessage()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    try:
        # Authentication
        s.login(sender, password)
    except:
        print('Incorrect Username or Password:\n')
        return 
    em["To"] = email
    em["From"] = sender
    em["Subject"] = subject
    em.set_content(content)
    s.send_message(em)
    s.quit()





