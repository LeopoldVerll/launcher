import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from Updater_Module.main import signals_main


class SimpleMessageBox(QWidget):
    def __init__(self):
        super().__init__()

        self.message_label = None
        self.init_ui()

    def init_ui(self):
        # Создаем вертикальный макет
        layout = QVBoxLayout()

        # Создаем метку для вывода сообщений
        self.message_label = QLabel('Нажмите кнопку', self)

        # # Создаем кнопки "ДА" и "НЕТ"
        # btn_yes = QPushButton('ДА', self)
        # btn_no = QPushButton('НЕТ', self)

        # Подключаем обработчики событий для кнопок
        # btn_yes.clicked.connect(self.show_yes_message)
        # btn_no.clicked.connect(self.show_no_message)

        # # Добавляем метку и кнопки к макету
        # layout.addWidget(self.message_label)
        # layout.addWidget(btn_yes)
        # layout.addWidget(btn_no)

        # Устанавливаем макет для основного окна
        self.setLayout(layout)

        # Устанавливаем размеры окна
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Проверка на обнову')

        signals_main.update_info_signal.connect(self.update_info_label_main)

    def update_info_label_main(self, message):
        self.message_label.setText(message)

    def show_yes_message(self):
        # Выводим сообщение при нажатии на кнопку "ДА"
        self.message_label.setText('Вы нажали "ДА"')

    def show_no_message(self):
        # Выводим сообщение при нажатии на кнопку "НЕТ"
        self.message_label.setText('Вы нажали "НЕТ"')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleMessageBox()
    window.show()
    sys.exit(app.exec_())
