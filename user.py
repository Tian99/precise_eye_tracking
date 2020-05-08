import sys
import math
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon, QPixmap

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle('User Input')
        self.setGeometry(30,30,600,400)
        self.label = QtWidgets.QLabel(self)
        self.pixmap = QPixmap('chosen_pic.png')
        self.setFixedSize(self.pixmap.width(), self.pixmap.height())

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawPixmap(self.rect(), self.pixmap)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 90))  
        qp.setBrush(br)   
        qp.drawRect(QtCore.QRect(self.begin, self.end))

        begin_x = self.begin.x()
        begin_y = self.begin.y()
        end_x = self.end.x()
        end_y = self.end.y()

        radius = abs(math.sqrt((end_x - begin_x)**2 + (end_y - begin_y)**2))/2
        print(radius)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        # self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
