import Stream as st
import PreProcess as prp
import DetectStart
import Command
import recognition as rc


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
from threading import Thread


class Sound_analyzer(Thread):
    def __init__(self, name, reason):
        Thread.__init__(self)
        self.name = name
        self.reason = reason
    
    def run(self):
        """Запуск потока"""
        st.Record()
        text_raw = rc.recognition()
        preprocessing_text = prp.PreProcess(text_raw)
        self.reason.text_command.setText(preprocessing_text)
        print(preprocessing_text)
        Command.command(preprocessing_text)

        

class ProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)

        self.setValue(0)
        self.timer = QTimer(self, timeout=self.onTimeout)

    def onTimeout(self):
        if self.value() >= 100:
            self.timer.stop()
            return
        self.setValue(self.value() + 1)

    def start(self):
        self.timer.start(50)

class MainWindow(QMainWindow):
    """
        Объявление чекбокса и иконки системного трея.
        Инициализироваться будут в конструкторе.
    """
    check_box = None
    tray_icon = None
    text_command = None
    btn_record = None
    progress_bar = None
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setWindowIcon(QtGui.QIcon('img/icon.png'))
        self.setMinimumSize(QSize(150, 150))             # Устанавливаем размеры
        self.setWindowTitle("DeepSpeech")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
 
        grid_layout = QGridLayout(self)         # Создаём QGridLayout
        central_widget.setLayout(grid_layout)   # Устанавливаем данное размещение в центральный виджет
        #grid_layout.addWidget(QLabel("Application, which can minimize to Tray", self), 0, 0)
 

        self.progress_bar = ProgressBar(self, minimum=0, maximum=100, textVisible=False, objectName="GreenProgressBar")
        grid_layout.addWidget(self.progress_bar, 1, 0)


        # Добавляем чекбокс, от которого будет зависеть поведение программы при закрытии окна
        self.text_command = QLabel(self)
        grid_layout.addWidget(self.text_command, 2, 0)

        self.btn_record = QPushButton('Start')
        grid_layout.addWidget(self.btn_record, 3, 0)
        self.btn_record.clicked.connect(self.click_record)

        # Инициализируем QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon('img/icon.png'))
        self.tray_icon.activated.connect(self.onTrayIconActivated)
 
        '''
            talk - сказать команду
            show - показать окно
            hide - скрыть окно
            exit - выход из программы
        '''
        
        talk_action = QAction("Talk", self)
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)

        talk_action.triggered.connect(self.click_record)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(talk_action)
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    # Переопределение метода closeEvent, для перехвата события закрытия окна
    # Окно будет закрываться только в том случае, если нет галочки в чекбоксе
    def closeEvent(self, event):
        if True:
            event.ignore()
            self.hide()
    
    def click_record(self):
        self.progress_bar.setValue(0)
        self.progress_bar.start()
        analyz = Sound_analyzer('Analyz', self)
        analyz.start()

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            #"Tray icon one clicked"
            pass
        elif reason == QSystemTrayIcon.DoubleClick:
            self.show

StyleSheet = '''
#GreenProgressBar {
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}
#GreenProgressBar::chunk {
    border-radius: 6px;
    background-color: #009688;
}
'''

app = QApplication(sys.argv)
app.setStyleSheet(StyleSheet)
mw = MainWindow()
mw.show()
sys.exit(app.exec())



