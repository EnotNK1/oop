from database.database import database_service
from userservice.emailservise import send_email
import uuid
from smtplib import SMTPRecipientsRefused
from psycopg2 import Error


class UserServise:

    def register(self, email, password, confirm_password):

        if password == confirm_password and len(email) > 5 and len(password) > 2:
            if database_service.register_user(email, password) == 0:
                return "Successfully"
            else:
                return "A email address has already been registered"
        else:
            return "Password mismatch"

    def authorization(self, email, password):

        if database_service.check_user(email, password) == 0:
            return "Successfully"
        else:
            return "error"

    def add_phrase(self, email, phrase, translate):

        temp = database_service.check_phrase(email, phrase, translate)
        print(temp)
        if temp == -1:
            if database_service.add_phrase(email, phrase, translate) == 0:
                return "Successfully"
            else:
                return "error"
        elif temp == 1:
            return "have"
        else:
            return "error"

    def deleet_phrase(self, email, phrase, translate):

        temp = database_service.check_phrase(email, phrase, translate)
        print(temp)
        if temp == -1:
            return "not have"
        elif temp == 1:
            database_service.delete_pharse_db(email, phrase, translate)
            return "Successfully"
        else:
            return "error"

    def reset_password(self, email) -> str:

        password = database_service.get_password_user(email)
        if password != -1:
            try:
                subject = "Password Reset"
                message = f"Your password is: {password}"
                send_email(email, subject, message)
                return "The password email has been sent"
            except SMTPRecipientsRefused:
                return "incorrect email"
        else:
            return "No user with this e-mail account was found"



user_service: UserServise = UserServise()
