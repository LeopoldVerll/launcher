import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QDialog, QLabel, QGridLayout
import os
import re
import random

from Updater_Module.main import updater
from constants import *


library_folder_path = "library"


class MainApp(QMainWindow):
    def __init__(self, folder_path):
        super(MainApp, self).__init__()

        self.folder_path = folder_path
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Launcher")

        central_widget = QLabel(self)

        self.setCentralWidget(central_widget)

        layout = QGridLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)

        # Получаем список папок в указанной директории
        folders = [folder for folder in os.listdir(self.folder_path) if
                   os.path.isdir(os.path.join(self.folder_path, folder))]

        row, col = 0, 0
        cols = (len(folders) ** (1/2)) // 1
        if cols > 5:
            cols = 5

        # Создаем кнопки для каждой папки
        for folder in folders:
            button = QPushButton(folder, self)

            if len(folders) > 15:
                button.setFixedSize(100, 50)
                button.setFont(QtGui.QFont("Times New Roman", 5))
            else:
                button.setFixedSize(200, 50)
                button.setFont(QtGui.QFont("Times New Roman", 15))
            button.clicked.connect(lambda checked, path=os.path.join(self.folder_path, folder):
                                   self.on_folder_button_click(path))
            layout.addWidget(button, row, col)
            button.setStyleSheet("background-color: white;")

            row += 1
            if row > cols:  # Переход на следующий ряд после второй колонки
                row = 0
                col += 1

        self.setMinimumSize(400, 400)
        self.setFixedSize(220 * int(cols), 220 * int(cols))
        self.setMaximumSize(1500, 800)
        central_widget.setLayout(layout)
        self.adjustSize()

        image = get_image()
        if image:
            pixmap = QPixmap(image)

            target_width = 220 * int(cols + 1)
            target_height = 220 * int(cols + 1)
            pixmap = pixmap.scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            central_widget.setPixmap(pixmap)
            central_widget.setAlignment(Qt.AlignCenter)
            central_widget.setStyleSheet("background-color: black;")

    def on_folder_button_click(self, folder_path):
        folder_dialog = FolderDialog(folder_path, self)
        folder_dialog.exec_()


class FolderDialog(QDialog):
    def __init__(self, folder_path, main_app):
        super(FolderDialog, self).__init__()

        self.main_app = main_app  # Сохраняем ссылку на экземпляр MainApp

        self.folder_path = folder_path
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Лаунчер 0.1.1")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Получаем список .exe файлов в указанной директории
        exe_files = [file for file in os.listdir(self.folder_path) if file.endswith(".exe")]

        # Создаем кнопки для каждого .exe файла
        for exe_file in exe_files:
            button = QPushButton(exe_file, self)
            button.setFixedSize(200, 50)
            button.clicked.connect(lambda checked, path=os.path.join(self.folder_path, exe_file): self.run_selected_exe(path))
            layout.addWidget(button)

        self.setLayout(layout)

    def run_selected_exe(self, exe_path):
        # Получаем путь к директории, где находится .exe файл
        exe_dir = os.path.dirname(exe_path)
        exe_name = os.path.basename(exe_path)

        try:
            # Устанавливаем текущий рабочий каталог
            os.chdir(exe_dir)

            os.startfile(exe_name)

        except Exception as e:
            print(f"Error executing {exe_path}: {e}")
        finally:

            # Восстанавливаем текущий рабочий каталог после выполнения .exe файла
            # Узнаем абсолютный путь
            abs_path = os.path.abspath(".")

            # Используем регулярное выражение для удаления всего, что находится после второго с конца слеша
            root_path = re.sub(r'[\\\/][^\\\/]+[\\\/][^\\\/]+$', '', abs_path)
            # Переключаемся та полученный корневой путь
            os.chdir(root_path)

            # Закрыть текущее диалоговое окно
            self.accept()


def get_image():
    # Выбираем случайное изображение из папки backgrounds
    backgrounds_folder = "backgrounds"
    background_files = [file for file in os.listdir(backgrounds_folder) if file.endswith((".jpg", ".png", ".jpeg"))]

    if background_files:
        selected_background = random.choice(background_files)
        background_path = os.path.join(backgrounds_folder, selected_background)

        return background_path

    return False


if __name__ == '__main__':
    if updater(REPOSITORY_OWNER, REPOSITORY_NAME, CURRENT_VERSION, ASSET_NAME):
        sys.exit()

    app = QApplication(sys.argv)

    mainWin = MainApp(library_folder_path)
    mainWin.show()

    sys.exit(app.exec_())
