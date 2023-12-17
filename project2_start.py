import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit, QGraphicsOpacityEffect
from PyQt5.QtGui import QFont, QPixmap


class AuthorisationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 100, 900, 800)
        self.setWindowTitle('Маша + каша')

        self.background = QPixmap('raspberries.png')
        self.background.scaled(900, 800)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.5)
        self.background_display = QLabel(self)
        self.background_display.resize(900, 800)
        self.background_display.move(0, 0)
        self.background_display.setPixmap(self.background)
        self.background_display.setGraphicsEffect(self.opacity_effect)

        self.font1 = QFont('Times New Roman', 15)
        self.font1.setBold(True)

        self.font2 = QFont('Times New Roman', 20)
        self.font2.setBold(True)

        self.autorise = QLabel(self)
        self.autorise.resize(500, 100)
        self.autorise.move(130, 450)
        self.autorise.setFont(self.font2)
        self.autorise.setText("Авторизация пользователя")

        self.login = QLabel(self)
        self.login.resize(100, 100)
        self.login.move(100, 525)
        self.login.setFont(self.font1)
        self.login.setText("Логин:")

        self.password = QLabel(self)
        self.password.resize(100, 100)
        self.password.move(100, 600)
        self.password.setFont(self.font1)
        self.password.setText("Пароль:")

        self.login_input = QLineEdit(self)
        self.login_input.resize(300, 35)
        self.login_input.move(225, 560)
        self.login_input.setStyleSheet('QLineEdit {background-color: pink;}')

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.resize(300, 35)
        self.password_input.move(225, 635)
        self.password_input.setStyleSheet('QLineEdit {background-color: pink;}')

        self.data_enter = QPushButton('Играть', self)
        self.data_enter.setFont(QFont('Times New Roman', 15))
        self.data_enter.resize(150, 50)
        self.data_enter.move(280, 690)
        self.data_enter.setStyleSheet('QPushButton {background-color: pink;}')
        self.data_enter.clicked.connect(self.open_main_menu)

        self.registrate = QPushButton('Регистрация', self)
        self.registrate.setFont(QFont('Times New Roman', 15))
        self.registrate.resize(200, 100)
        self.registrate.move(595, 570)
        self.registrate.setStyleSheet('QPushButton {background-color: pink;}')
        self.registrate.clicked.connect(self.open_registration_window)

        self.pixmap1 = QPixmap('masha1.png')
        self.title_pic = QLabel(self)
        self.pixmap1 = self.pixmap1.scaled(275, 200)
        self.title_pic.resize(275, 400)
        self.title_pic.move(615, 100)
        self.title_pic.setPixmap(self.pixmap1)

        self.pixmap2 = QPixmap('description.png')
        self.title_text = QLabel(self)
        self.title_text.resize(600, 400)
        self.title_text.move(5, 100)
        self.title_text.setPixmap(self.pixmap2)

        self.pixmap3 = QPixmap('title_pygame.png')
        self.title = QLabel(self)
        self.title.resize(600, 200)
        self.title.move(250, 0)
        self.title.setPixmap(self.pixmap3)

    def open_registration_window(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()

    def open_main_menu(self):
        self.main_menu = MainMenu()
        self.main_menu.show()


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 100, 900, 800)
        self.setWindowTitle('Меню')

        self.font1 = QFont('Times New Roman', 30)
        self.font1.setBold(True)

        self.background = QPixmap('raspberries.png')
        self.background.scaled(900, 800)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.5)
        self.background_display = QLabel(self)
        self.background_display.resize(900, 800)
        self.background_display.move(0, 0)
        self.background_display.setPixmap(self.background)
        self.background_display.setGraphicsEffect(self.opacity_effect)

        self.choose_game = QLabel(self)
        self.choose_game.resize(500, 100)
        self.choose_game.move(240, 50)
        self.choose_game.setFont(self.font1)
        self.choose_game.setText("Выбери сложность:")

        self.level1 = QPushButton('Уровень I', self)
        self.level1.setFont(QFont('Times New Roman', 15))
        self.level1.resize(275, 120)
        self.level1.move(325, 225)
        self.level1.setStyleSheet('QPushButton {background-color: pink;}')

        self.level2 = QPushButton('Уровень II', self)
        self.level2.setFont(QFont('Times New Roman', 15))
        self.level2.resize(275, 120)
        self.level2.move(325, 370)
        self.level2.setStyleSheet('QPushButton {background-color: pink;}')

        self.level3 = QPushButton('Уровень III', self)
        self.level3.setFont(QFont('Times New Roman', 15))
        self.level3.resize(275, 120)
        self.level3.move(325, 515)
        self.level3.setStyleSheet('QPushButton {background-color: pink;}')

        self.achievements = QPushButton('🏆', self)
        self.achievements.setFont(QFont('Times New Roman', 15))
        self.achievements.resize(100, 100)
        self.achievements.move(410, 660)
        self.achievements.setStyleSheet('QPushButton {background-color: pink;}')


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 200, 600, 500)
        self.setWindowTitle('Регистрация')

        self.background = QPixmap('raspberries.png')
        self.background.scaled(600, 500)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.5)
        self.background_display = QLabel(self)
        self.background_display.resize(600, 500)
        self.background_display.move(0, 0)
        self.background_display.setPixmap(self.background)
        self.background_display.setGraphicsEffect(self.opacity_effect)

        self.font1 = QFont('Times New Roman', 15)
        self.font1.setBold(True)

        self.font2 = QFont('Times New Roman', 20)
        self.font2.setBold(True)

        self.registration = QLabel(self)
        self.registration.resize(500, 100)
        self.registration.move(130, 100)
        self.registration.setFont(self.font2)
        self.registration.setText("Регистрация пользователя")

        self.reg_login = QLabel(self)
        self.reg_login.resize(100, 100)
        self.reg_login.move(100, 175)
        self.reg_login.setFont(self.font1)
        self.reg_login.setText("Логин:")

        self.reg_password = QLabel(self)
        self.reg_password.resize(100, 100)
        self.reg_password.move(100, 250)
        self.reg_password.setFont(self.font1)
        self.reg_password.setText("Пароль:")

        self.reg_login_input = QLineEdit(self)
        self.reg_login_input.resize(300, 35)
        self.reg_login_input.move(225, 210)
        self.reg_login_input.setStyleSheet('QLineEdit {background-color: pink;}')

        self.reg_password_input = QLineEdit(self)
        self.reg_password_input.resize(300, 35)
        self.reg_password_input.move(225, 285)
        self.reg_password_input.setStyleSheet('QLineEdit {background-color: pink;}')

        self.new_data_enter = QPushButton('Ввести', self)
        self.new_data_enter.setFont(QFont('Times New Roman', 15))
        self.new_data_enter.resize(150, 50)
        self.new_data_enter.move(280, 340)
        self.new_data_enter.setStyleSheet('QPushButton {background-color: pink;}')
        self.new_data_enter.clicked.connect(self.registration_is_done)

    def registration_is_done(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AuthorisationWindow()
    win.show()
    sys.exit(app.exec())