from email.message import EmailMessage
import asyncio
import aiosmtplib
import emailSecret

from exception import NotValidEmailException

class EmailSender:
    def __init__(self):
        pass

    subjectTxt = "About your job application"
    rejectTxt = """
Your application was great but unfortunately we do not have position for you\n\nHope you find this valuable.\n\nBest regards Ileska
    """
    interviewTxt = """
Your application was great and we would like to have a internview with you\n\nHope you find this valuable.\n\nBest regards Ileska
    """

    def sendMail(self, fromWho:str, toWho:str, subject:str, content:str):
        if not toWho.endswith("@ileska.fi"):
            return

        msg = EmailMessage()
        msg["From"] = fromWho
        msg["To"] = toWho
        msg["Subject"] = subject
        msg.set_content(content)

        aiosmtplib.send(
            msg,
            hostname=emailSecret.emailhost, 
            port=emailSecret.emailport,
            username=emailSecret.emailusername,
            password=emailSecret.emailpassword,
            use_tls=True,
        )

    def sendRejectMail(self, toWho:str):
        if not toWho.endswith("@ileska.fi"):
            raise NotValidEmailException
        self.sendMail(emailSecret.emailusername, toWho, self.subjectTxt, self.rejectTxt)

    def sendInterviewMail(self, toWho:str):
        if not toWho.endswith("@ileska.fi"):
            raise NotValidEmailException
        self.sendMail(emailSecret.emailusername, toWho, self.subjectTxt, self.interviewTxt)

emailSender = EmailSender()