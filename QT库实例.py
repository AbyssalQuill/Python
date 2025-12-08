import sys
from PyQt5.QtWidgets import *


#窗口
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5")
        self.setGeometry(100,100,400,400)
        self.UI()
        self.show()
    def UI(self):
        self.label = QLabel("Hello World",self)
        self.label.move(150,150)
        self.label.setStyleSheet("font-size:20px;color:red;")


#运行
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())