
"""
session = {
    SESSION_ID: {
    
        'username':{
            'email'
            'password'
            'last_login' }   
}
}
"""

from datetime import datetime
import pytz
SESSION_ID = "user_data"

class Data:
    def __init__(self,  request , username , last_login):
        self.username =  username
        self.last_login = last_login
        self.session = request.session

        #becasue after user logged out all sessions get cleared . so: 
        if SESSION_ID not in self.session:
            self.session[SESSION_ID] = {}
        if self.username not in self.session[SESSION_ID]:
            self.session[SESSION_ID][username] = {}
    
    
    def save_data(self,email):
        self.session[SESSION_ID][self.username] = {
            "email": email , 
            "last_login": self.last_login,
        }
        self.save()

    def save_last_login(self,request):
        current_time = str(datetime.now(tz=pytz.timezone("Asia/Tehran")))
        self.session[SESSION_ID][self.username]["last_login"] = current_time
        self.save()
        request.user.last_login = self.session[SESSION_ID][self.username]["last_login"]
        request.user.save()

    def save(self):
        self.session.modified = True



from django.core.mail import send_mail
def send_otp_code(code,email):
    subject = "Your otp code"
    message = f"Your otp code is: {code}"
    sender_email = "matin.amani101013@gmail.com"
    recipient_list = [email]

    send_mail(subject,message,sender_email,recipient_list)
    


import string , random
def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters,k=12))