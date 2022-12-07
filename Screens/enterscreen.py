import re
from kivy.uix.screenmanager import Screen, FadeTransition

class ENTERScreen(Screen):
    def check(self):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
        if self.email.text != "" and re.match(pattern, self.email.text) is not None:
            self.email.helper_text_color_normal = "white"
            self.email.helper_text_color_focus = "white"
            self.email.helper_text = ""
            if len(self.password.text) >= 8:
                self.password.helper_text_color_normal = "white"
                self.password.helper_text_color_focus = "white"
                # вход в emias по логину паролю
            else:
                self.password.helper_text = "Пароль слишком короткий "
                self.password.helper_text_color_normal = "red"
                self.password.helper_text_color_focus = "red"
        else:
            self.email.helper_text = "Введите корректный Email!"
            self.email.helper_text_color_normal = "red"
            self.email.helper_text_color_focus = "red"

    def oms(self):
        self.manager.transition = FadeTransition(clearcolor=(1, 1, 1, 1))
        self.manager.current = "oms"

    def mos(self):
        self.manager.transition = FadeTransition(clearcolor=(1, 1, 1, 1))
        self.manager.current = "mos"

    pass