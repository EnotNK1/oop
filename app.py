from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from userservice.userservice import user_service
from database.database import database_service
from userservice.emailservise import send_email
import math

Window.size = (1100,700)
Window.title = "Разговорник"
Window.clearcolor = ("#4287f5")

class AythScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email_input = TextInput(hint_text='Enter your email', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.password_input = TextInput(password=True, hint_text='Enter your password', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.35})
        self.auth_button = Button(text='Log in', on_press=self.ayth, size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.10},
                                  background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.reg_button = Button(text='register', on_press=self.register, size_hint=(0.2, 0.08), pos_hint={'center_x': 0.2, 'center_y': -0.05},
                                 background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.recovery_button = Button(text='forgot password?', on_press=self.recovery_password, size_hint=(0.3, 0.08), pos_hint={'center_x': 0.75, 'center_y': -0.05},
                                      background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.incorrect_lable = Label(text='*incorrect email/password', pos_hint={'center_x': 0.5, 'center_y': 0.25}, font_size=15, color=("#e80e0e"))

        layout = self.create_layout()
        self.add_widget(layout)

    def create_layout(self):
        layout = FloatLayout(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, width=400, height=300)
        layout.add_widget(Label(text='Авторизация', pos_hint={'center_x': 0.5, 'center_y': 0.8}, font_size=30))
        self.incorrect_lable.opacity = 0
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.auth_button)
        layout.add_widget(self.reg_button)
        layout.add_widget(self.recovery_button)
        layout.add_widget(self.incorrect_lable)
        return layout

    def ayth(self, instance):
        if user_service.authorization(self.email_input.text, self.password_input.text) == "Successfully":
            self.manager.switch_to(MainScreen(self.email_input.text))
        else:
            self.incorrect_lable.opacity = 1

    def register(self, instance):
        self.manager.switch_to(RegistrationScreen())

    def recovery_password(self, instance):
        self.manager.switch_to(ForgotScreen())

class ForgotScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.back_button = Button(text='Back', on_press=self.back, size_hint=(0.2, 0.1), pos_hint={'center_x': -0.6, 'center_y': 1},
                                  background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.send_message = Button(text='Send message', on_press=self.send, size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                   background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.email_input = TextInput(hint_text='Enter your email', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.3})


        layout = self.create_layout()
        self.add_widget(layout)

    def create_layout(self):
        layout = FloatLayout(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, width=400, height=300)

        layout.add_widget(Label(text='Восстановление пароля', pos_hint={'center_x': 0.5, 'center_y': 0.6}, font_size=30))
        layout.add_widget(self.back_button)
        layout.add_widget(self.send_message)
        layout.add_widget(self.email_input)
        return layout

    def back(self, instance):
        self.manager.switch_to(AythScreen())

    def send(self, instance):
        user_service.reset_password(self.email_input.text)

class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.email_input = TextInput(hint_text='Enter your email', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.password_input = TextInput(password=True, hint_text='Enter your password', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.35})
        self.confirm_password_input = TextInput(password=True, hint_text='Confirn password', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.20})
        self.reg_button = Button(text='Create account', on_press=self.register, size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': -0.05},
                                 background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.login_button = Button(text='log in', on_press=self.ayth, size_hint=(0.2, 0.08), pos_hint={'center_x': 0.2, 'center_y': -0.2},
                                   background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.incorrect_lable = Label(text='password mismatch', pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                     font_size=15, color=("#e80e0e"))

        layout = self.create_layout()
        self.add_widget(layout)

    def create_layout(self):
        layout = FloatLayout(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, width=400, height=300)
        layout.add_widget(Label(text='Регистрация', pos_hint={'center_x': 0.5, 'center_y': 0.8}, font_size=30))
        self.incorrect_lable.opacity = 0
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.confirm_password_input)
        layout.add_widget(self.reg_button)
        layout.add_widget(self.login_button)
        layout.add_widget(self.incorrect_lable)
        return layout

    def register(self, instance):
        if self.password_input.text != self.confirm_password_input.text:
            self.incorrect_lable.text = "password mismatch"
            self.incorrect_lable.opacity = 1
        elif "@" not in self.email_input.text or "." not in self.email_input.text:
            self.incorrect_lable.text = "email is incorrect"
            self.incorrect_lable.opacity = 1
        elif len(self.password_input.text) < 5:
            self.incorrect_lable.text = "password must be more than 4 characters"
            self.incorrect_lable.opacity = 1
        elif user_service.register(self.email_input.text, self.password_input.text, self.confirm_password_input.text) == "Successfully":
            self.manager.switch_to(MainScreen(self.email_input.text))
        else:
            self.incorrect_lable.text = "this email is already taken"
            self.incorrect_lable.opacity = 1

    def ayth(self, instance):
        self.manager.switch_to(AythScreen())

class MainScreen(Screen):
    def __init__(self, email, **kwargs):
        super().__init__(**kwargs)

        self.email = email
        self.page = 0
        self.max_p = 0
        self.min_p = 0
        self.phrases = []
        self.search_phrases = []
        self.word1 = Label(text="", pos_hint={'center_x': 0.1, 'center_y': 0.6}, font_size=30)
        self.word2 = Label(text="", pos_hint={'center_x': 0.9, 'center_y': 0.6}, font_size=30)
        self.delete_button1 = Button(text='удалить', on_press=lambda instance: self.delete_word(self.word1.text, self.word2.text), size_hint=(0.16, 0.1),
                                    pos_hint={'center_x': -0.5, 'center_y': 0.6}, background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.word3 = Label(text="", pos_hint={'center_x': 0.1, 'center_y': 0.4}, font_size=30)
        self.word4 = Label(text="", pos_hint={'center_x': 0.9, 'center_y': 0.4}, font_size=30)
        self.delete_button2 = Button(text='удалить', on_press=lambda instance: self.delete_word(self.word3.text, self.word4.text), size_hint=(0.16, 0.1),
                                     pos_hint={'center_x': -0.5, 'center_y': 0.4}, background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.word5 = Label(text="", pos_hint={'center_x': 0.1, 'center_y': 0.2}, font_size=30)
        self.word6 = Label(text="", pos_hint={'center_x': 0.9, 'center_y': 0.2}, font_size=30)
        self.delete_button3 = Button(text='удалить', on_press=lambda instance: self.delete_word(self.word5.text, self.word6.text), size_hint=(0.16, 0.1),
                                     pos_hint={'center_x': -0.5, 'center_y': 0.2}, background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.word7 = Label(text="", pos_hint={'center_x': 0.1, 'center_y': 0}, font_size=30)
        self.word8 = Label(text="", pos_hint={'center_x': 0.9, 'center_y': 0}, font_size=30)
        self.delete_button4 = Button(text='удалить', on_press=lambda instance: self.delete_word(self.word7.text, self.word8.text), size_hint=(0.16, 0.1),
                                     pos_hint={'center_x': -0.5, 'center_y': 0}, background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.word9 = Label(text="", pos_hint={'center_x': 0.1, 'center_y': -0.2}, font_size=30)
        self.word10 = Label(text="", pos_hint={'center_x': 0.9, 'center_y': -0.2}, font_size=30)
        self.delete_button5 = Button(text='удалить', on_press=lambda instance: self.delete_word(self.word9.text, self.word10.text), size_hint=(0.16, 0.1),
                                     pos_hint={'center_x': -0.5, 'center_y': -0.2}, background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.word11 = Label(text="", pos_hint={'center_x': 0.1, 'center_y': -0.4}, font_size=30)
        self.word12 = Label(text="", pos_hint={'center_x': 0.9, 'center_y': -0.4}, font_size=30)
        self.delete_button6 = Button(text='удалить', on_press=lambda instance: self.delete_word(self.word11.text, self.word12.text), size_hint=(0.16, 0.1),
                                     pos_hint={'center_x': -0.5, 'center_y': -0.4}, background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.word13 = Label(text="", pos_hint={'center_x': 0.1, 'center_y': -0.6}, font_size=30)
        self.word14 = Label(text="", pos_hint={'center_x': 0.9, 'center_y': -0.6}, font_size=30)
        self.delete_button7 = Button(text='удалить', on_press=lambda instance: self.delete_word(self.word13.text, self.word14.text), size_hint=(0.16, 0.1),
                                     pos_hint={'center_x': -0.5, 'center_y': -0.6}, background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.pages = Label(text="1/1", pos_hint={'center_x': 0.5, 'center_y': -0.9}, font_size=15)
        self.word_input = TextInput(hint_text='Search', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.95})
        self.add_word_button = Button(text='Новая фраза', on_press=self.add_word, size_hint=(0.3, 0.1), pos_hint={'center_x': 1.6, 'center_y': -0.7},
                                      background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.search_word_button = Button(text='Поиск', on_press=self.search_word, size_hint=(0.15, 0.1), pos_hint={'center_x': 1, 'center_y': 0.95},
                                         background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.next_button = Button(text='>', on_press=self.next, size_hint=(0.1, 0.1), pos_hint={'center_x': 0.6, 'center_y': -0.9},
                                  background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.back_button = Button(text='<', on_press=self.back, size_hint=(0.1, 0.1), pos_hint={'center_x': 0.4, 'center_y': -0.9},
                                  background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.reset_button = Button(text='reset', on_press=self.reset, size_hint=(0.1, 0.1), pos_hint={'center_x': 1.6, 'center_y': 0.8},
                                   background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.profile_button = Button(text=f'{self.email}', on_press=self.profile, size_hint=(0.3, 0.1), pos_hint={'center_x': 1.6, 'center_y': 1.1},
                                     background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.void_lable = Label(text='Пусто', pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                     font_size=30, color=("#ffffff"))

        layout = self.create_layout()
        self.add_widget(layout)

    def create_layout(self):
        layout = FloatLayout(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, width=400, height=300)
        phrases = database_service.get_words(self.email)
        self.phrases = phrases
        self.max_p = len(self.phrases)
        self.pages.text = f'{(self.page+14)//14}/{math.ceil(self.max_p/14)}'
        print(self.max_p)
        print(phrases)
        i = 0
        j = 0
        list = [self.word1, self.word2, self.word3, self.word4, self.word5, self.word6, self.word7, self.word8,
                self.word9, self.word10, self.word11, self.word12, self.word13, self.word14]
        del_buttons = [self.delete_button1, self.delete_button2, self.delete_button3, self.delete_button4,
                       self.delete_button5, self.delete_button6, self.delete_button7]
        self.void_lable.opacity = 0

        if len(phrases) == 0:
            self.void_lable.opacity = 1
            for i in range(0, 7, 1):
                del_buttons[i].opacity = 0
                del_buttons[i].disabled = True
        if len(phrases) > 0:
            for i in range(0, len(phrases), 2):
                list[i].text = phrases[i]
                list[i+1].text = phrases[i+1]
                del_buttons[j].opacity = 1
                del_buttons[j].disabled = False
                print(list[i].text)

                j += 1
                if j > 6:
                    break

            for i in range(j, 7, 1):
                del_buttons[i].opacity = 0
                del_buttons[i].disabled = True

        layout.add_widget(self.add_word_button)
        layout.add_widget(self.word_input)
        layout.add_widget(self.search_word_button)
        layout.add_widget(self.next_button)
        layout.add_widget(self.back_button)
        layout.add_widget(self.reset_button)
        layout.add_widget(self.profile_button)
        layout.add_widget(self.pages)
        layout.add_widget(self.word1)
        layout.add_widget(self.word2)
        layout.add_widget(self.delete_button1)
        layout.add_widget(self.word3)
        layout.add_widget(self.word4)
        layout.add_widget(self.delete_button2)
        layout.add_widget(self.word5)
        layout.add_widget(self.word6)
        layout.add_widget(self.delete_button3)
        layout.add_widget(self.word7)
        layout.add_widget(self.word8)
        layout.add_widget(self.delete_button4)
        layout.add_widget(self.word9)
        layout.add_widget(self.word10)
        layout.add_widget(self.delete_button5)
        layout.add_widget(self.word11)
        layout.add_widget(self.word12)
        layout.add_widget(self.delete_button6)
        layout.add_widget(self.word13)
        layout.add_widget(self.word14)
        layout.add_widget(self.delete_button7)
        layout.add_widget(self.void_lable)
        return layout

    def add_word(self, instance):
        self.manager.switch_to(NewPhrase(self.email))

    def delete_word(self, word1, word2):
        # self.manager.switch_to(DelPhrase(self.word1.text, self.word2.text, self.email))
        self.manager.switch_to(DelPhrase(word1, word2, self.email))

    def profile(self, instance):
        self.manager.switch_to(Profile(self.email))

    def search_word(self, instance):
        self.search_phrases = database_service.get_words(self.email)
        self.phrases = []

        for i in range(0, len(self.search_phrases), 2):
            if self.word_input.text in self.search_phrases[i] or self.word_input.text in self.search_phrases[i+1]:
                self.phrases.append(self.search_phrases[i])
                self.phrases.append(self.search_phrases[i+1])

        self.page = 0
        self.max_p = len(self.phrases)
        self.pages.text = f'{(self.page + 14) // 14}/{math.ceil(self.max_p / 14)}'
        self.void_lable.opacity = 0

        list = [self.word1, self.word2, self.word3, self.word4, self.word5, self.word6, self.word7, self.word8,
                self.word9, self.word10, self.word11, self.word12, self.word13, self.word14]
        del_buttons = [self.delete_button1, self.delete_button2, self.delete_button3, self.delete_button4,
                       self.delete_button5, self.delete_button6, self.delete_button7]
        for k in range(0, 14, 2):
            list[k].text = ""
            list[k + 1].text = ""

        print("noy")
        j = 0
        k = 0
        if len(self.phrases) == 0:
            for i in range(0, 7, 1):
                del_buttons[i].opacity = 0
                del_buttons[i].disabled = True
            self.void_lable.opacity = 1

        if len(self.phrases) > 0:
            for i in range(self.page, len(self.phrases), 2):
                list[k].text = self.phrases[i]
                list[k+1].text = self.phrases[i+1]
                del_buttons[j].opacity = 1
                del_buttons[j].disabled = False

                k += 2
                j += 1
                if j > 6:
                    break

            for i in range(j, 7, 1):
                del_buttons[i].opacity = 0
                del_buttons[i].disabled = True


    def next(self, instance):
        if self.page + 14 < self.max_p:
            self.page = self.page + 14
            self.pages.text = f'{(self.page + 14) // 14}/{math.ceil(self.max_p / 14)}'
            list = [self.word1, self.word2, self.word3, self.word4, self.word5, self.word6, self.word7, self.word8,
                    self.word9, self.word10, self.word11, self.word12, self.word13, self.word14]
            del_buttons = [self.delete_button1, self.delete_button2, self.delete_button3, self.delete_button4,
                           self.delete_button5, self.delete_button6, self.delete_button7]
            for k in range(0, 14, 2):
                list[k].text = ""
                list[k + 1].text = ""

            print("noy")
            j = 0
            k = 0
            if len(self.phrases) > 0:
                for i in range(self.page, len(self.phrases), 2):
                    list[k].text = self.phrases[i]
                    list[k+1].text = self.phrases[i+1]
                    del_buttons[j].opacity = 1
                    del_buttons[j].disabled = False

                    k += 2
                    j += 1
                    if j > 6:
                        break

                for i in range(j, 7, 1):
                    del_buttons[i].opacity = 0
                    del_buttons[i].disabled = True

    def back(self, instance):
        if self.page - 14 >= 0:
            self.page = self.page - 14
            self.pages.text = f'{(self.page + 14) // 14}/{math.ceil(self.max_p / 14)}'
            list = [self.word1, self.word2, self.word3, self.word4, self.word5, self.word6, self.word7, self.word8,
                    self.word9, self.word10, self.word11, self.word12, self.word13, self.word14]
            del_buttons = [self.delete_button1, self.delete_button2, self.delete_button3, self.delete_button4,
                           self.delete_button5, self.delete_button6, self.delete_button7]

            for i in range(0, 14, 2):
                list[i].text = ""
                list[i + 1].text = ""

            j = 0
            k = 0
            if len(self.phrases) > 0:
                for i in range(self.page, len(self.phrases), 2):
                    list[k].text = self.phrases[i]
                    list[k+1].text = self.phrases[i + 1]
                    del_buttons[j].opacity = 1
                    del_buttons[j].disabled = False

                    j += 1
                    k += 2
                    if j > 6:
                        break

                for i in range(j, 7, 1):
                    del_buttons[i].opacity = 0
                    del_buttons[i].disabled = True

    def reset(self, instance):
        self.search_phrases = database_service.get_words(self.email)
        self.phrases = self.search_phrases

        self.page = 0
        self.max_p = len(self.phrases)
        self.pages.text = f'{(self.page + 14) // 14}/{math.ceil(self.max_p / 14)}'
        self.void_lable.opacity = 0

        list = [self.word1, self.word2, self.word3, self.word4, self.word5, self.word6, self.word7, self.word8,
                self.word9, self.word10, self.word11, self.word12, self.word13, self.word14]
        del_buttons = [self.delete_button1, self.delete_button2, self.delete_button3, self.delete_button4,
                       self.delete_button5, self.delete_button6, self.delete_button7]
        for k in range(0, 14, 2):
            list[k].text = ""
            list[k + 1].text = ""

        print("noy")
        j = 0
        k = 0
        if len(self.phrases) > 0:
            for i in range(self.page, len(self.phrases), 2):
                list[k].text = self.phrases[i]
                list[k + 1].text = self.phrases[i + 1]
                del_buttons[j].opacity = 1
                del_buttons[j].disabled = False

                k += 2
                j += 1
                if j > 6:
                    break

            for i in range(j, 7, 1):
                del_buttons[i].opacity = 0
                del_buttons[i].disabled = True

class NewPhrase(Screen):
    def __init__(self, email, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.word_input = TextInput(hint_text='Enter phrase', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.translate_input = TextInput(hint_text='Enter translate', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.35})
        self.confirm_button = Button(text='Confirm', on_press=self.confirm, size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': -0.05},
                                     background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.back_button = Button(text='Back', on_press=self.back, size_hint=(0.2, 0.1), pos_hint={'center_x': -0.6, 'center_y': 1},
                                  background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.incorrect_lable = Label(text='the length of the phrase must be more than 1 characters', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                     font_size=15, color=("#e80e0e"))

        layout = self.create_layout()
        self.add_widget(layout)

    def create_layout(self):
        layout = FloatLayout(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, width=400, height=300)
        layout.add_widget(Label(text='Новая фраза', pos_hint={'center_x': 0.5, 'center_y': 0.8}, font_size=30))
        self.incorrect_lable.opacity = 0
        layout.add_widget(self.word_input)
        layout.add_widget(self.translate_input)
        layout.add_widget(self.confirm_button)
        layout.add_widget(self.back_button)
        layout.add_widget(self.incorrect_lable)
        return layout

    def confirm(self, instance):
        if len(self.word_input.text) > 20 or len(self.translate_input.text) > 20:
            self.incorrect_lable.text = "phrase too long"
            self.incorrect_lable.opacity = 1
        elif len(self.word_input.text) < 2 or len(self.translate_input.text) < 2:
            self.incorrect_lable.text = "the length of the phrase must be more than 1 characters"
            self.incorrect_lable.opacity = 1
        elif user_service.add_phrase(self.email, self.word_input.text, self.translate_input.text) == "Successfully":
            self.manager.switch_to(MainScreen(self.email))
        else:
            self.incorrect_lable.text = "such a phrase already exists"
            self.incorrect_lable.opacity = 1

    def back(self, instance):
        self.manager.switch_to(MainScreen(self.email))

    def ayth(self, instance):
        self.manager.switch_to(AythScreen())

class DelPhrase(Screen):
    def __init__(self, word1, word2, email, **kwargs):
        super().__init__(**kwargs)
        self.word1 = word1
        self.word2 = word2
        self.email = email
        self.confirm_button = Button(text='Удалить', on_press=self.confirm, size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'center_y': -0.05},
                                     background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.back_button = Button(text='Back', on_press=self.back, size_hint=(0.2, 0.1), pos_hint={'center_x': -0.6, 'center_y': 1},
                                  background_color=("#ffffff"), color=("#0a0500"), background_normal='')

        layout = self.create_layout()
        self.add_widget(layout)

    def create_layout(self):
        layout = FloatLayout(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, width=400, height=300)
        layout.add_widget(Label(text='Удалить фразу?', pos_hint={'center_x': 0.5, 'center_y': 0.8}, font_size=40))
        layout.add_widget(Label(text=self.word1, pos_hint={'center_x': 0.1, 'center_y': 0.4}, font_size=30))
        layout.add_widget(Label(text=self.word2, pos_hint={'center_x': 0.9, 'center_y': 0.4}, font_size=30))
        layout.add_widget(self.confirm_button)
        layout.add_widget(self.back_button)
        return layout

    def confirm(self, instance):
        if user_service.deleet_phrase(self.email, self.word1, self.word2) == "Successfully":
            self.manager.switch_to(MainScreen(self.email))

    def back(self, instance):
        self.manager.switch_to(MainScreen(self.email))

    def ayth(self, instance):
        self.manager.switch_to(AythScreen())

class Profile(Screen):
    def __init__(self, email, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.back_button = Button(text='Back', on_press=self.back, size_hint=(0.2, 0.1), pos_hint={'center_x': -0.6, 'center_y': 1},
                                  background_color=("#ffffff"), color=("#0a0500"), background_normal='')
        self.log_out_button = Button(text='Log out', on_press=self.log_out, size_hint=(0.5, 0.2), pos_hint={'center_x': 1.6, 'center_y': -1},
                                     background_color=("#ffffff"), color=("#0a0500"), background_normal='')

        layout = self.create_layout()
        self.add_widget(layout)

    def create_layout(self):
        layout = FloatLayout(size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}, width=400, height=300)
        phrases = database_service.get_words(self.email)
        layout.add_widget(Label(text=f'{self.email}', pos_hint={'center_x': 0.5, 'center_y': 0.8}, font_size=30))
        layout.add_widget(Label(text=f'Количество записей: {len(phrases)//2}', pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=20))
        layout.add_widget(self.back_button)
        layout.add_widget(self.log_out_button)
        return layout

    def back(self, instance):
        self.manager.switch_to(MainScreen(self.email))

    def log_out(self, instance):
        self.manager.switch_to(AythScreen())

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AythScreen(name='ayth screen'))
        sm.add_widget(ForgotScreen(name='forgot screen'))
        sm.add_widget(RegistrationScreen(name='Register'))
        sm.add_widget(Profile(name='profile', email='email'))
        sm.add_widget(NewPhrase(name='new phrase screen', email='email'))
        sm.add_widget(MainScreen(name='main', email='email'))
        sm.add_widget(DelPhrase(name="del", word1="word1", word2="word2", email="email"))
        return sm
