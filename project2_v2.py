# ПРОМЕЖУТОЧНЫЙ ВАРИАНТ; ПОКА РЕАЛИЗОВАНЫ НЕ ВСЕ ЗАПЛАНИРОВАННЫЕ ДЕТАЛИ
import sys
import sqlite3
import pygame
from pygame.locals import *
import random
import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit, QGraphicsOpacityEffect
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont, QPixmap


WIDTH = 900
HEIGHT = 800
FPS = 60
DATA = {
    'level1': (10, 9, 0),
    'level2': (20, 6, 0),
    'level3': (30, 3, 0)
}
FOOD = {
    'potato.png': (0, 100),
    'carrot.png': (200, 100),
    'apple.png': (400, 100)
}


def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class NoValueError(Exception):
    pass


class NoUserInDatabaseError(Exception):
    pass


class WrongPasswordError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class AuthorisationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 100, WIDTH, HEIGHT)
        self.setWindowTitle('Маша + каша')

        self.background = QPixmap('raspberries.png')
        self.background.scaled(WIDTH, HEIGHT)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.5)
        self.background_display = QLabel(self)
        self.background_display.resize(WIDTH, HEIGHT)
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

        self.authorisation_error = QMessageBox(self)

    def data_is_ok(self):
        entered_login = self.login_input.text()
        entered_password = self.password_input.text()
        if not entered_password or not entered_login:
            raise NoValueError
        connection = sqlite3.connect('users_database.db')
        cursor = connection.cursor()
        user_data = cursor.execute('SELECT * FROM Users WHERE login = ?',
                                   (entered_login,)).fetchone()
        connection.commit()
        connection.close()
        if not user_data:
            raise NoUserInDatabaseError
        if entered_password != user_data[1]:
            raise WrongPasswordError
        return True

    def open_main_menu(self):
        try:
            if self.data_is_ok():
                self.remember_user()
                self.login_input.clear()
                self.password_input.clear()
                self.main_menu = MainMenu()
                self.main_menu.show()
        except NoValueError:
            self.edit_error_message('Кажется, вы забыли ввести логин или пароль')
            self.authorisation_error.show()
        except NoUserInDatabaseError:
            self.edit_error_message('Такого пользователя не существует')
            self.authorisation_error.show()
        except WrongPasswordError:
            self.edit_error_message('Неверный пароль')
            self.authorisation_error.show()

    def open_registration_window(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()

    def edit_error_message(self, message):
        self.authorisation_error.setIcon(QMessageBox.Critical)
        self.authorisation_error.setText("Error")
        self.authorisation_error.setInformativeText(message)
        self.authorisation_error.setWindowTitle("Error")

    def remember_user(self):
        with open('users.txt', mode='w') as file:
            entered_login = self.login_input.text()
            file.write(entered_login)


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(350, 100, WIDTH, HEIGHT)
        self.setWindowTitle('Меню')

        self.font1 = QFont('Times New Roman', 30)
        self.font1.setBold(True)

        self.background = QPixmap('raspberries.png')
        self.background.scaled(WIDTH, HEIGHT)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.5)
        self.background_display = QLabel(self)
        self.background_display.resize(WIDTH, HEIGHT)
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
        self.level1.clicked.connect(self.run_minigame)

        self.level2 = QPushButton('Уровень II', self)
        self.level2.setFont(QFont('Times New Roman', 15))
        self.level2.resize(275, 120)
        self.level2.move(325, 370)
        self.level2.setStyleSheet('QPushButton {background-color: pink;}')
        self.level2.clicked.connect(self.run_minigame)

        self.level3 = QPushButton('Уровень III', self)
        self.level3.setFont(QFont('Times New Roman', 15))
        self.level3.resize(275, 120)
        self.level3.move(325, 515)
        self.level3.setStyleSheet('QPushButton {background-color: pink;}')
        self.level3.clicked.connect(self.run_minigame)

        self.achievements = QPushButton('🏆', self)
        self.achievements.setFont(QFont('Times New Roman', 15))
        self.achievements.resize(100, 100)
        self.achievements.move(410, 660)
        self.achievements.setStyleSheet('QPushButton {background-color: pink;}')

        self.results = QMessageBox(self)

    def run_minigame(self):
        if self.sender() == self.level1:
            self.minigame = CatchingRaspberries(DATA['level1'][0], DATA['level1'][1])
        elif self.sender() == self.level2:
            self.minigame = CatchingRaspberries(DATA['level2'][0], DATA['level2'][1])
        elif self.sender() == self.level3:
            self.minigame = CatchingRaspberries(DATA['level3'][0], DATA['level3'][1])
        self.minigame.run()
        self.edit_results_message()
        self.results.show()

    def edit_results_message(self):
        with open('results.txt') as file:
            data = file.readlines()
        if int(data[0]) == 0:
            self.results.setText('К сожалению, ты проиграл...')
        elif int(data[0]) == -1:
            self.results.setText('Похоже, ты вышел из игры...')
        elif int(data[0]) == 10:
            self.results.setText('Поздравляю, ты выиграл!')
        self.results.setInformativeText(f'Малины собрано: {int(data[1])}\nМалины пропущено: {int(data[2])}')
        self.results.setIcon(QMessageBox.Information)
        self.results.setWindowTitle("Конец игры")


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

        self.registration_error = QMessageBox(self)

    def registration_is_done(self):
        try:
            new_login = self.reg_login_input.text()
            new_password = self.reg_password_input.text()
            if not new_login or not new_password:
                raise NoValueError
            connection = sqlite3.connect('users_database.db')
            cursor = connection.cursor()
            checking = cursor.execute('SELECT * FROM Users WHERE login = ?',
                                      (new_login,)).fetchone()
            if checking:
                raise UserAlreadyExistsError
            cursor.execute('INSERT INTO Users (login, password) VALUES (?, ?)',
                           (new_login, new_password))
            connection.commit()
            connection.close()
            connection2 = sqlite3.connect('records_database.db')
            cursor2 = connection2.cursor()
            cursor2.execute('INSERT INTO Records (login, level1, level2, level3) VALUES (?, ?, ?, ?)',
                            (new_login, 0, 0, 0))
            connection2.commit()
            connection2.close()
            self.close()
        except NoValueError:
            self.edit_error_message('Кажется, вы забыли ввести логин или пароль')
            self.registration_error.show()
        except UserAlreadyExistsError:
            self.edit_error_message('Пользователь с таким логином уже существует')
            self.registration_error.show()

    def edit_error_message(self, message):
        self.registration_error.setIcon(QMessageBox.Critical)
        self.registration_error.setText("Error")
        self.registration_error.setInformativeText(message)
        self.registration_error.setWindowTitle("Error")


class CatchingRaspberries:
    def __init__(self, good_limit, bad_limit):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Собери малину")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.good_limit = good_limit
        self.bad_score = 0
        self.bad_limit = bad_limit
        self.time_ranges = 0
        self.is_passed = False
        self.is_quit = False
        self.font = pygame.font.SysFont("Times New Roman", 24)
        self.raspberries = pygame.sprite.Group()
        self.basket = pygame.sprite.Group()
        self.background = load_image('forest.png')
        Basket(self.basket)
        Raspberry(self.raspberries)

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_quit = True
                    running = False

            if self.bad_score > self.bad_limit:
                running = False

            if self.score >= self.good_limit:
                self.is_passed = True
                running = False

            if self.time_ranges == 120:
                Raspberry(self.raspberries)
                self.time_ranges = 0
            self.raspberries.draw(self.screen)
            self.raspberries.update()

            self.basket.draw(self.screen)
            self.basket.update()

            self.draw_score()
            pygame.display.flip()
            self.time_ranges += 1
            self.clock.tick(FPS)
        # if self.is_passed:
            # self.minigame2 = CookingPorridge()
            # self.minigame2.run()
        self.remember_result()
        pygame.quit()

    def draw_score(self):
        score_surface = self.font.render(f"Собрано: {self.score}", True, (255, 255, 255))
        score_surface2 = self.font.render(f"Потеряно: {self.bad_score}", True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), Rect(0, 0, 150, 80))
        self.screen.blit(score_surface, (10, 10))
        self.screen.blit(score_surface2, (10, 40))

    def remember_result(self):
        with open('results.txt', mode='w') as file:
            if self.is_quit:
                file.write('-1\n')
            elif self.is_passed:
                file.write('10\n')
            else:
                file.write('00\n')
            file.write(str(self.score) + '\n')
            file.write(str(self.bad_score) + '\n')


class Raspberry(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('raspberry.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(150, WIDTH - 50)
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 2

    def update(self):
        if not pygame.sprite.collide_mask(self, win.main_menu.minigame.basket.sprites()[0]):
            self.rect = self.rect.move(0, self.speed)
        else:
            win.main_menu.minigame.score += 1
            self.kill()
        if (self.rect.y + self.rect.h) > HEIGHT:
            win.main_menu.minigame.bad_score += 1
            self.kill()


class Basket(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('basket.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 650
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3

    def update(self, *args):
        if pygame.key.get_pressed()[K_LEFT]:
            if self.rect.x >= self.speed:
                self.rect = self.rect.move(-self.speed, 0)
        elif pygame.key.get_pressed()[K_RIGHT]:
            if self.rect.x <= (WIDTH - self.speed):
                self.rect = self.rect.move(self.speed, 0)


class CookingPorridge:
    def __init__(self):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Приготовь кашу")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.ingredients = pygame.sprite.Group()
        self.pot = pygame.sprite.Group()
        Pot(self.pot)
        for ingr in FOOD:
            Ingredient(self.ingredients, image_file=ingr, x=FOOD[ingr][0], y=FOOD[ingr][1])

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                else:
                    self.ingredients.update(event)

            self.pot.draw(self.screen)
            self.ingredients.draw(self.screen)

            pygame.display.flip()
        pygame.quit()

    def remember_result(self):
        with open('results.txt', mode='w') as file:
            pass


class Pot(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('pot.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500
        self.mask = pygame.mask.from_surface(self.image)


class Ingredient(pygame.sprite.Sprite):
    def __init__(self, *group, image_file, x, y):
        super().__init__(*group)
        self.image = load_image(image_file, -1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.moving = False

    def update(self, *args):
        if args and args[0].type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(args[0].pos):
                self.moving = True
        elif args and args[0].type == MOUSEBUTTONUP:
            self.moving = False
            if pygame.sprite.collide_mask(self, win.main_menu.minigame.minigame2.pot.sprites()[0]):
                self.kill()
        elif args and args[0].type == MOUSEMOTION and self.moving:
            self.rect.move_ip(args[0].rel)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AuthorisationWindow()
    win.show()
    sys.exit(app.exec())