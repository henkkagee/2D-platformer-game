import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton, QLabel, QFileDialog, QErrorMessage,\
    QMessageBox

from game import Game

from game import PixelType
from PyQt5.Qt import QRectF, QPixmap
from PyQt5.QtMultimedia import QSound

class MainGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = QtWidgets.QWidget()
        self.setWindowTitle("Y2-platformer")
        self.setCentralWidget(self.menu)
        background = QLabel(self.menu)
        background.setGeometry(0, 0, 500, 400)
        
        self.xsize = 40
        self.ysize = 40
        
        background.setPixmap(QtGui.QPixmap(os.getcwd() + "/assets/menubackground.png"))
        
        self.init_buttons(self.menu)

        self.setGeometry(600, 270, 500, 400)
        self.game = Game(self)
        self.show()
        self.setFocus()
        self.grabKeyboard()
        self.timer = QtCore.QTimer()
        self.started = False            # Est‰‰ QPaintEventin ajon ennen pelin alkua
        
        self.initdefaultconstants()
        self.readsettings()
        print("---{}---{}---{}---{}---{}---{}---{}---{}---".format(self.framerate, self.greentiletexture, self.redtiletexture, self.blacktiletexture, self.yellowtiletexture, self.playertexture, self.menubackground, self.gamebackground))
        
    def initdefaultconstants(self):     # alustaa vakioarvot
        self.framerate = 60
        self.greentiletexture = "grasstile.png" 
        self.redtiletexture = "crate.png"
        self.blacktiletexture = "fin.png"
        self.yellowtiletexture = "fire.png"
        self.playertexture = "plr.png"
        self.menubackground = "menubackground.png"
        self.gamebackground = "skybox.png"
        
    def readsettings(self):         # lukee settings.txt-tiedostosta mahdollisesti oletusarvoista poikkeavia tietoja
        try:
            
            with open(os.getcwd() + "/settings.txt", "r") as file:
                

                first = True
                for line in file:
                    if first == True:
                        if line != "Y2-platformer settings:\n":
                            raise IOError
                    else:
                        if line[0] == "#" or line[0] == "\n":
                            continue
                        line.strip(" ")
                        parts = line.split("=")
                        parts[1] = parts[1].rstrip()
                        print("test {}-{}-".format(parts[0], parts[1]))
                        if parts[0] == "framerate":
                            self.framerate = int(parts[1])
                        elif parts[0] == "greentiletexture":
                            self.greentiletexture = parts[1]
                        elif parts[0] == "redtiletexture":
                            self.redtiletexture = parts[1]
                        elif parts[0] == "blacktiletexture":
                            self.blacktiletexture = parts[1]
                        elif parts[0] == "yellowtiletexture":
                            self.yellowtiletexture = parts[1]
                        elif parts[0] == "playertexture":
                            self.playertexture = parts[1]
                        elif parts[0] == "menubackground":
                            self.menubackground = parts[1]
                        elif parts[0] == "gamebackground":
                            self.gamebackground = parts[1]
                    first = False
            file.closed
                
        
        except (IOError):
            self.dialog("Error", "Reading settings.txt failed, all values at default.")
            return
        
    def start_game(self):
        
        
        if self.game.map is None:
            print("Error: No map chosen!")
            error = QErrorMessage(self.menu)
            error.setWindowTitle("Error")
            error.showMessage("Error: No map chosen!")
            return
        
        self.setGeometry(600, 270, 600, 600)
        self.menu.hide()
        self.setCentralWidget(None)
        
        self.timer.timeout.connect(self.loop)
        self.started = True
        self.timer.start(1000 * (1/self.framerate))        # ms --- 16 ms -> ~60 fps

        
    def init_buttons(self, menu):
        
        start = QPushButton(menu)
        start.setText("Start")
        start.setGeometry(125, 25, 250, 50)
        start.setStyleSheet("background-color: white")
        start.clicked.connect(self.start_game)
        
        load = QPushButton(menu)
        load.setText("Load map")
        load.setGeometry(125, 175, 250, 50)
        load.setStyleSheet("background-color: white")
        load.clicked.connect(self.mapdialog)
        
        exitb = QPushButton(menu)
        exitb.setText("Exit")
        exitb.setGeometry(125, 325, 250, 50)
        exitb.clicked.connect(self.close)
        exitb.setStyleSheet("background-color: white")
        
    def mapdialog(self):    # Yritt‰‰ ladata kent‰n
        img = QFileDialog.getOpenFileName(self, 'Open 24-bit BMP image from \maps - directory', os.getcwd(), 'Image files (*.bmp)')
        if img[0]:
            success, msg = self.game.load_map(img[0])
            if success == 0:
                error = QErrorMessage(self.menu)
                error.setWindowTitle("Error")
                error.showMessage(msg)
                
    
    def dialog(self, txt1, txt2):   # Geneerinen teksti-ikkuna
        msg = QMessageBox(self)
        msg.setText(txt1)
        if txt2 != "":
            msg.setInformativeText(txt2)
        msg.exec()
    
        
    def paintEvent(self, event):    # Piirt‰‰ peliruudun
        
        if self.started == False:
            return
        qp = QtGui.QPainter()
        qp.begin(self)
        xcenter = self.xsize * 7    
        ycenter = self.ysize * 9
        xsize = self.xsize
        ysize = self.ysize
        xoffset = self.game.player.offset.x
        yoffset = self.game.player.offset.y
        
        howmanybackgroundpixmaps = self.game.map.x / 2
        source = QRectF(0, 0, 500, 1000)
        pixmap = QPixmap(os.getcwd() + "/assets/" + self.gamebackground)
        for i in range(int(-howmanybackgroundpixmaps / 2), int(howmanybackgroundpixmaps / 2)):
            target = QRectF(xcenter + i * 500 + (self.game.player.offset.x/3), -200 , 500, 1000)
            qp.drawPixmap(target, pixmap, source)
        
        for y in range(-10, 7):
            if y < 0:
                if (self.game.player.coordinates.y + y - int(yoffset/40)) < 0:
                    continue
            if y >= 0:
                if (self.game.player.coordinates.y + y - int(yoffset/40) >= self.game.map.y):
                    continue
            for x in range(-8, 9):
                if x < 0:
                    if (self.game.player.coordinates.x + x - int(xoffset/40)< 0):
                        continue
                if x >= 0:
                    if (self.game.player.coordinates.x + x - int(yoffset/40) >= self.game.map.x):
                        continue
                if self.game.map.map[self.game.player.coordinates.x + x - int(xoffset/40)][self.game.player.coordinates.y + y - int(yoffset/40)] == PixelType.BLACK:
                    
                    if xoffset % 40 == 0:
                        if yoffset % 40 == 0:
                            target = QRectF(xcenter + (x)*xsize + ((xoffset % 40)), ycenter + y*ysize + ((yoffset % 40)+40), xsize, ysize)
                        else:
                            target = QRectF(xcenter + (x)*xsize + ((xoffset % 40)), ycenter + y*ysize + (yoffset % 40), xsize, ysize)
                    else:
                        if yoffset % 40 == 0:
                            target = QRectF(xcenter + (x)*xsize + (xoffset % 40)-40, ycenter + y*ysize + ((yoffset % 40)+40), xsize, ysize)
                        else:
                            target = QRectF(xcenter + (x)*xsize + (xoffset % 40)-40, ycenter + y*ysize + (yoffset % 40), xsize, ysize)
                    source = QRectF(0, 0, 40, 40)
                    pixmap = QPixmap(os.getcwd() + "/assets/" + self.blacktiletexture)
                    qp.drawPixmap(target, pixmap, source)
                    
                elif self.game.map.map[self.game.player.coordinates.x + x - int(xoffset/40)][self.game.player.coordinates.y + y - int(yoffset/40)] == PixelType.RED:

                    if xoffset % 40 == 0:
                        if yoffset % 40 == 0:
                            target = QRectF(xcenter + (x)*xsize + ((xoffset % 40)), ycenter + y*ysize + ((yoffset % 40)+40), xsize, ysize)
                        else:
                            target = QRectF(xcenter + (x)*xsize + ((xoffset % 40)), ycenter + y*ysize + (yoffset % 40), xsize, ysize)
                    else:
                        if yoffset % 40 == 0:
                            target = QRectF(xcenter + (x)*xsize + (xoffset % 40)-40, ycenter + y*ysize + ((yoffset % 40)+40), xsize, ysize)
                        else:
                            target = QRectF(xcenter + (x)*xsize + (xoffset % 40)-40, ycenter + y*ysize + (yoffset % 40), xsize, ysize)
                    source = QRectF(0, 0, 40, 40)
                    pixmap = QPixmap(os.getcwd() + "/assets/" + self.redtiletexture)
                    qp.drawPixmap(target, pixmap, source)
                    
                elif self.game.map.map[self.game.player.coordinates.x + x - int(xoffset/40)][self.game.player.coordinates.y + y - int(yoffset/40)] == PixelType.GREEN:

                    if xoffset % 40 == 0:
                        if yoffset % 40 == 0:
                            target = QRectF(xcenter + (x)*xsize + ((xoffset % 40)), ycenter + y*ysize + ((yoffset % 40)+40), xsize, ysize)
                        else:
                            target = QRectF(xcenter + (x)*xsize + ((xoffset % 40)), ycenter + y*ysize + (yoffset % 40), xsize, ysize)
                    else:
                        if yoffset % 40 == 0:
                            target = QRectF(xcenter + (x)*xsize + (xoffset % 40)-40, ycenter + y*ysize + ((yoffset % 40)+40), xsize, ysize)
                        else:
                            target = QRectF(xcenter + (x)*xsize + (xoffset % 40)-40, ycenter + y*ysize + (yoffset % 40), xsize, ysize)
                    source = QRectF(0, 0, 40, 40)
                    pixmap = QPixmap(os.getcwd() + "/assets/" + self.greentiletexture)
                    qp.drawPixmap(target, pixmap, source)
                
                elif self.game.map.map[self.game.player.coordinates.x + x - int(xoffset/40)][self.game.player.coordinates.y + y - int(yoffset/40)] == PixelType.DANGER:
                    if xoffset % 40 == 0:
                        if yoffset % 40 == 0:
                            target = QRectF(xcenter + (x)*xsize + ((xoffset % 40)), ycenter + y*ysize + ((yoffset % 40)+40), xsize, ysize)
                        else:
                            target = QRectF(xcenter + (x)*xsize + ((xoffset % 40)), ycenter + y*ysize + (yoffset % 40), xsize, ysize)
                    else:
                        if yoffset % 40 == 0:
                            target = QRectF(xcenter + (x)*xsize + (xoffset % 40)-40, ycenter + y*ysize + ((yoffset % 40)+40), xsize, ysize)
                        else:
                            target = QRectF(xcenter + (x)*xsize + (xoffset % 40)-40, ycenter + y*ysize + (yoffset % 40), xsize, ysize)
                    source = QRectF(0, 0, 40, 40)
                    pixmap = QPixmap(os.getcwd() + "/assets/" + self.yellowtiletexture)
                    qp.drawPixmap(target, pixmap, source)
                    
                else:
                    continue

        target = QRectF(xcenter, ycenter, xsize, ysize)
        source = QRectF(0, 0, 40, 40)
        pixmap = QPixmap(os.getcwd() + "/assets/plr.png")
        qp.drawPixmap(target, pixmap, source)
        qp.end()
        
    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        if event.key() == QtCore.Qt.Key_A:
            self.game.player.movingleft = True
        elif event.key() == QtCore.Qt.Key_D:
            self.game.player.movingright = True
        if event.key() == QtCore.Qt.Key_Space:
            if self.game.player.yspeed < 0:
                return
            self.game.player.jump()
            self.game.player.jumping = True
            QSound.play(os.getcwd() + "/assets/jump.wav")
        if event.key() == QtCore.Qt.Key_Q:
            self.game.exit = True
          
    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        if event.key() == QtCore.Qt.Key_A:
            self.game.player.movingleft = False
        elif event.key() == QtCore.Qt.Key_D:
            self.game.player.movingright = False
        
    def loop(self):
      
            self.game.checkstate()
            if self.game.fin == True:
                self.game.fin = False
                self.timer.stop()
                if self.game.player.alive == True:
                    self.dialog("GOAL", "")
                else:
                    self.dialog("Game over", "")
                self.backtomenu()
            if self.game.exit == True:
                self.timer.stop()
                self.backtomenu()
                self.game.exit = False
            self.game.player.move()
            self.game.resolvecollision()
            self.game.resolvegravity()
            self.game.ycollision()
            self.repaint()
            
    def backtomenu(self):
        self.started = False
        self.menu = QtWidgets.QWidget()
        self.setWindowTitle("Y2-platformer")
        self.setCentralWidget(self.menu)
        background = QLabel(self.menu)
        background.setGeometry(0, 0, 500, 400)
        background.setPixmap(QtGui.QPixmap(os.getcwd() + "/assets/menubackground.png"))
        
        self.init_buttons(self.menu)

        self.setGeometry(600, 270, 500, 400)
        self.show()
        