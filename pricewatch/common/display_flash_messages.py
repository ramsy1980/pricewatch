from flask import flash, url_for


class DisplayFlashMessages:
    @staticmethod
    def phone_number_not_verified():
        link = f"<a href='{url_for('users.user_profile')}' class='underline'>update</a>"
        flash(f"Unable to send SMS notifications. Please {link} your phone number first", "yellow")
