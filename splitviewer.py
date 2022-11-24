# License 
# 'image: fullScreen.png'. This cover has been designed using images from Flaticon.com
# 'image: icon.png, favicon.ico'. This cover has been designed using images from logo.com

import sys,os
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

# 고객용 서브윈도우
class SubWindow(QWidget):

    def __init__(self):
        super().__init__()

        # ★ debug path ★
        # self.exePath = os.path.dirname(os.path.abspath(__file__))
        # self.tmpPath = os.path.dirname(os.path.abspath(__file__))

        # ★ build path ★
        self.exePath = os.path.dirname(os.path.abspath(sys.executable))
        try: self.tmpPath = sys._MEIPASS
        except Exception: self.tmpPath = os.path.abspath(".")

        # 창 기본세팅
        self.setWindowTitle('SubWindow')
        self.setWindowIcon(QIcon(self.tmpPath+"\img\icon.png"))
        self.setStyleSheet("background-color: black;")
        self.show()
        self.vbox=QVBoxLayout()
        
    # 작업윈도우에서 이미지 출력이끝나면 호출되는메서드
    def displayInfo(self,files):
        # 이전이미지는 제거 작업(메모리관리)
        # vbox의 자식 개체수만큼
        while self.vbox.count():
            # 자식개체와 해당 개체의 레이아웃 저장
            childWidget = self.vbox.takeAt(0)
            childLayout = childWidget.layout()
            if childLayout:
                # 자식개체의 레이아웃(hbox)의 자식 개체수만큼
                while childLayout.count():
                    childWidget2=childLayout.takeAt(0)
                    childLayout2=childWidget2.widget()
                    # hbox의 자식 개체(이미지) 의 상속관계를 해제후 destory)
                    if childLayout2:
                        childLayout2.setParent(None)
                        childLayout2.deleteLater()
                # vbox의 자식개체(hbox) 의 상속관계를 해제후 destory
                childLayout.setParent(None)
                childLayout.deleteLater()
        
        # 수평박스
        hbox=[QHBoxLayout(),QHBoxLayout()]
        
        # 제공받은 이미지 갯수만큼
        for f in files:
            c=f.replace('/','\\')
            pixmap = QPixmap(c)
            lbl_img = QLabel(self)
            # 해상도 가로 기준으로 이미지 리사이즈
            lbl_img.setPixmap(pixmap.scaledToWidth(int(self.size().width()/2)))
            # 센터정렬
            lbl_img.setAlignment(Qt.AlignCenter)
            # 이미지갯수 절반보다 작으면 위에 많으면 밑에
            if files.index(f)<(len(files)/2):
                hbox[0].addWidget(lbl_img)
            else:
                hbox[1].addWidget(lbl_img)
        
        # vbox 에 hbox 두개를 순서대로 추가후 레이아웃을 vbox로 설정
        self.vbox.addLayout(hbox[0])
        self.vbox.addLayout(hbox[1])
        self.setLayout(self.vbox)

# 작업자용 메인윈도우
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # ★ debug path ★
        # self.exePath = os.path.dirname(os.path.abspath(__file__))
        # self.tmpPath = os.path.dirname(os.path.abspath(__file__))

        # ★ build path ★
        self.exePath = os.path.dirname(os.path.abspath(sys.executable))
        try: self.tmpPath = sys._MEIPASS
        except Exception: self.tmpPath = os.path.abspath(".")

        # 윈도우 아이콘 설정
        self.setWindowIcon(QIcon(self.tmpPath+"\img\icon.png"))
        
        # 서브윈도우 생성
        self.subWindow = SubWindow()
        self.setAcceptDrops(True)

        # 작업자뷰 상단에 위치하는 조작용 버튼 레이아웃
        startInfoBox = QVBoxLayout()
        fullBtn = QPushButton()
        fullBtn.setIcon(QIcon(self.tmpPath+"\img//fullScreen.png"))
        self.setStyleSheet("QPushButton{background-color: rgb(151, 151, 141);border-radius: 20px;}QPushButton:hover{background-color: rgb(121, 121, 111);}")
        fullBtn.setIconSize(fullBtn.size())
        fullBtn.clicked.connect(self.fullScreen)
        startInfoBox.addWidget(fullBtn)

        # 멤버로 쓸수있게끔 vbox 생성
        # SubWindow 선언, dropevent 활성화
        self.vbox=QVBoxLayout()
        self.vbox.addLayout(startInfoBox)
        self.setLayout(self.vbox)
        self.move(self.subWindow.pos().x()+100,self.subWindow.pos().y()+100)

        # 창제목 및 기본 사이즈
        self.setWindowTitle('SplitViewer')

    # 작업자 뷰 조작용
    def closeEvent(self, QCloseEvent):        
        self.subWindow.close()
    def fullScreen(self):
        self.subWindow.showFullScreen()

    # drag&drop 이벤트
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()
    def dropEvent(self, event):
        self.setStyleSheet("QPushButton{border-radius: 0px;}")
        # 이전이미지는 제거 작업(메모리관리)
        while self.vbox.count():
            # 자식개체와 해당 개체의 레이아웃 저장
            childWidget = self.vbox.takeAt(0)
            childLayout = childWidget.layout()
            if childLayout:
                # 자식개체의 레이아웃(hbox)의 자식 개체수만큼
                while childLayout.count():
                    childWidget2=childLayout.takeAt(0)
                    childLayout2=childWidget2.widget()
                    # hbox의 자식 개체(이미지) 의 상속관계를 해제후 destory)
                    if childLayout2:
                        childLayout2.setParent(None)
                        childLayout2.deleteLater()
                # vbox의 자식개체(hbox) 의 상속관계를 해제후 destory
                childLayout.setParent(None)
                childLayout.deleteLater()
        
        # 수평박스
        hbox=[QHBoxLayout(),QHBoxLayout()]
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            c=f.replace('/','\\')
            # 이미지 생성
            pixmap = QPixmap(c)
            
            # 해상도 가로 기준으로 이미지 리사이즈 fitToScreenWidth
            pixmap= pixmap.scaledToWidth(int(self.size().width()/2))
            # 해상도 세로 기준으로 이미지 리사이즈 fitToScreenWidth
            #pixmap= pixmap.scaledToHeight(int(self.size().width()/2))
            
            # 아이콘형태로
            icon = QIcon()
            icon.addPixmap(pixmap)
            
            # 버튼
            btn = QPushButton()
            btn.setIcon(icon)
            btn.setIconSize(pixmap.size())
            btn.setObjectName(c)
            btn.clicked.connect(self.printImage)

            # 이미지갯수 절반보다 작으면 위에 많으면 밑에
            if files.index(f)<(len(files)/2):
                hbox[0].addWidget(btn)
            else:
                hbox[1].addWidget(btn)
        
        # vbox 에 hbox 두개를 순서대로 추가후 레이아웃을 vbox로 설정
        self.vbox.addLayout(hbox[0])
        self.vbox.addLayout(hbox[1])
        self.setLayout(self.vbox)
        
        # 드래그앤드랍으로 사용자에게 제공받은 파일들을 고객윈도우에 똑같이 제공 
        self.subWindow.displayInfo(files)
    
    # 이미지 클릭시 호출될 메서드
    def printImage(self):
        # 클릭한 버튼개체를 저장
        btn = self.sender()
        # 버튼의 이름을 저장
        filename=btn.objectName()
        # 버튼의이름(파일명)을 기반으로 프린트
        os.startfile(filename,"print")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
