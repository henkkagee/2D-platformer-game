from enum import Enum
from player import Player
from coordinates import Coordinates
        

class PixelType(Enum):      # Kentän ruututyypit
    EMPTY = 0
    WHITE = 1
    BLACK = 2
    RED = 3
    GREEN = 4
    BLUE = 5
    DANGER = 6
    
class Map():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map = [[0 for i in range(y)] for j in range(x)]
    
    def print_map(self):        # Debuggausta varten
        for i in range(0, self.x):
            for j in range(0, self.y):
                print (self.map[i][j],)
            print('')
            
class Game():
    
    def __init__(self, GUI):
        
        self.map = None
        self.player = None
        self.fin = False
        self.gui = GUI
        self.exit = False
    
    def clear(self):
        self.map = None
        self.player = None
        self.fin = False
        self.exit = False
        
    def collision(self):            # Tarkistaa pelaajan vasemmalla ja oikealla puolella olevat ruudut, palauttaa 1 mikäli pelaajan vasemmalla on este, 2 mikäli oikealla on este
        
        if self.player.offset.x < 0:        
            if self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40)][self.player.coordinates.y - int((self.player.offset.y+ 10) / 40)] != PixelType.WHITE and \
                self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40)][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.BLACK and \
                self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40)][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.DANGER:
                return 1
            elif self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40) + 1][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.WHITE and \
                self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40) + 1][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.BLACK and \
                self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40) + 1][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.DANGER:
                return 2
            else:
                return 0
            
        else:
            if self.map.map[self.player.coordinates.x - int((self.player.offset.x - 40) / 40) -1][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.WHITE and \
                self.map.map[self.player.coordinates.x - int((self.player.offset.x - 40) / 40) -1][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.BLACK and \
                self.map.map[self.player.coordinates.x - int((self.player.offset.x -40) / 40)][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.DANGER:
                return 1
            elif self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40) -1][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.WHITE and \
                self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40) -1][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.BLACK and \
                self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40) -1][self.player.coordinates.y - int((self.player.offset.y+10) / 40)] != PixelType.DANGER:
                return 2
            else:
                return 0
    
    def resolvecollision(self):     # Laskee pelaajan liikkeen mikäli collision() palauttaa nollasta poikkeavan arvon 
        
        collision = self.collision()
        if collision != 0:
                if collision == 2:
                    move = self.player.xspeed
                    self.player.offset.x -= move
                elif collision == 1:
                    move = self.player.xspeed
                    self.player.offset.x -= move
                    
    def ycollision(self):           # Tarkistaa pelaajan yllä olevat ruudut laskee liikkeen niiden mukaisesti
        
        if self.player.offset.x < 0:
            
            if (self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40)][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1] != PixelType.WHITE and \
                self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40)][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1 ] != PixelType.BLACK and \
                self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40)][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1 ] != PixelType.DANGER) or \
            (self.map.map[self.player.coordinates.x - int((self.player.offset.x - 40) / 40)][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1] != PixelType.WHITE and \
             self.map.map[self.player.coordinates.x - int((self.player.offset.x - 40) / 40)][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1 ] != PixelType.BLACK and \
             self.map.map[self.player.coordinates.x - int((self.player.offset.x - 40) / 40)][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1 ] != PixelType.DANGER):
            
                self.player.offset.y -= self.player.yspeed
                self.player.yspeed = 0
            
        else:
                
            if (self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40)- 1][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1] != PixelType.WHITE and \
                 self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40)][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1 ] != PixelType.BLACK and \
                 self.map.map[self.player.coordinates.x - int(self.player.offset.x / 40)][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1 ] != PixelType.DANGER) or \
            (self.map.map[self.player.coordinates.x - int((self.player.offset.x - 40) / 40) - 1][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1] != PixelType.WHITE and \
             self.map.map[self.player.coordinates.x - int((self.player.offset.x - 40) / 40)-1][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1 ] != PixelType.BLACK and \
             map[self.player.coordinates.x - int((self.player.offset.x - 40) / 40)-1][self.player.coordinates.y - int((self.player.offset.y) / 40) - 1 ] != PixelType.DANGER):
            
                self.player.offset.y -= self.player.yspeed
                self.player.yspeed = 0
        
        
    def gravity(self, player, mapp):     # Tarkistaa pelaajan alla olevat ruudut ja palauttaa nollan mikäli pelaaja ei voi enää liikkua alaspäin
        
        if player.offset.x < 0:
            
            if (mapp[player.coordinates.x - int(player.offset.x / 40)][player.coordinates.y - int((player.offset.y + 39) / 40) + 1] != PixelType.WHITE and \
                mapp[player.coordinates.x - int(player.offset.x / 40)][player.coordinates.y - int((player.offset.y + 39) / 40) + 1 ] != PixelType.BLACK and \
                mapp[player.coordinates.x - int(player.offset.x / 40)][player.coordinates.y - int((player.offset.y + 39) / 40) + 1 ] != PixelType.DANGER) or \
            (mapp[player.coordinates.x - int((player.offset.x - 40) / 40)][player.coordinates.y - int((player.offset.y + 39) / 40) + 1] != PixelType.WHITE and \
             mapp[player.coordinates.x - int((player.offset.x - 40) / 40)][player.coordinates.y - int((player.offset.y + 39) / 40) + 1 ] != PixelType.BLACK and \
             mapp[player.coordinates.x - int((player.offset.x - 40) / 40)][player.coordinates.y - int((player.offset.y + 39) / 40) + 1 ] != PixelType.DANGER):
            
                return 0
            else:
                return 1
            
        else:
                
            if (mapp[player.coordinates.x - int(player.offset.x / 40)- 1][player.coordinates.y - int((player.offset.y + 39) / 40) + 1] != PixelType.WHITE and \
                 mapp[player.coordinates.x - int(player.offset.x / 40)][player.coordinates.y - int((player.offset.y + 39) / 40) + 1 ] != PixelType.BLACK and \
                 mapp[player.coordinates.x - int(player.offset.x / 40)][player.coordinates.y - int((player.offset.y + 39) / 40) + 1 ] != PixelType.DANGER) or \
            (mapp[player.coordinates.x - int((player.offset.x - 40) / 40) - 1][player.coordinates.y - int((player.offset.y + 39) / 40) + 1] != PixelType.WHITE and \
             mapp[player.coordinates.x - int((player.offset.x - 40) / 40)-1][player.coordinates.y - int((player.offset.y + 39) / 40) + 1 ] != PixelType.BLACK and \
             mapp[player.coordinates.x - int((player.offset.x - 40) / 40)-1][player.coordinates.y - int((player.offset.y + 39) / 40) + 1 ] != PixelType.DANGER):
            
                return 0
            else:
                return 1
    
    def resolvegravity(self):       # Kutsuu gravity()-funktiota ja laskee pelaajan liikkeen sen mukaisesti
        if self.gravity(self.player, self.map.map) == 1:
            self.player.yspeed -= self.player.yacceleration
            self.player.offset.y += self.player.yspeed / 7
        else:
            self.player.yspeed = 0
            if self.map.map[int(self.player.coordinates.x - int(self.player.offset.x / 40))][int(self.player.coordinates.y - int(self.player.offset.y + 1) / 40 + 1)] != PixelType.WHITE:
                self.player.offset.y += 2
                
            
    def checkstate(self):           # Tarkistaa onko pelaaja maalissa ja/tai elossa
        if self.map.map[self.player.coordinates.x - int(self.player.offset.x/40)][self.player.coordinates.y - int(self.player.offset.y/40)] == PixelType.BLACK:
            self.fin = True
        if self.map.map[self.player.coordinates.x - int(self.player.offset.x/40)][self.player.coordinates.y - int(self.player.offset.y/40)] == PixelType.DANGER:
            self.player.alive = False
            self.fin = True
            
    def load_map(self, imgname):    # Lataa kentän 24-bittisestä BMP-tiedostosta
        self.clear()
        img = open(imgname, 'rb')
        filetype = img.read(2)
        if filetype[0] != 66 and filetype[1] != 77:     # ASCII 66 = B, 77 = M
            print("Invalid filetype: not BMP")
            img.close
            return 0, "Invalid filetype: not BMP"
        img.read(15)                    # skipping header
        x = img.read(4)
        x = x[1]
        padding = x % 4
        y = img.read(4)
        y = y[1]
        img.read(2)
        bitsperpixel = img.read(2)
        if bitsperpixel[1] != 24:
            print("Incorrect bits per pixel! Must be 24. Is {}.".format(bitsperpixel[1]))
            img.close
            return 0, "Incorrect bits per pixel! Must be 24."
        gamemap = Map(x, y)
        print("map size: x: {}, y: {}".format(gamemap.x, gamemap.y))
        
        img.read(25)                    # skipping header
        byte = img.read(3)
        if not byte:
            print("Empty map")
            img.close
            return 0, "Error: Empty map"
        pixels_read = 1
        row = 0
        while byte:                     # accessing pixel RGB values
            if byte[0] == 0 and byte[1] == 0 and byte[2] == 0:
                gamemap.map[pixels_read - 1][(y - 1)-row] = PixelType.BLACK
            elif byte[0] == 0 and byte[1] == 0 and byte[2] == 255:
                gamemap.map[pixels_read - 1][(y - 1)-row] = PixelType.RED
            elif byte[0] == 0 and byte[1] == 255 and byte[2] == 0:
                gamemap.map[pixels_read - 1][(y - 1)-row] = PixelType.GREEN
            elif byte[0] == 255 and byte[1] == 0 and byte[2] == 0:
                if self.player is None:
                    gamemap.map[pixels_read - 1][(y - 1)-row] = PixelType.WHITE
                    self.player = Player(pixels_read - 1, (y-1)-row)
                else:
                    print("There can only be one player in the map!")
                    img.close
                    return 0, "Error: Too many players on the map! There can only be one."
            elif byte[0] == 255 and byte[1] == 255 and byte[2] == 255:
                gamemap.map[pixels_read - 1][(y - 1)-row] = PixelType.WHITE
            elif byte[0] == 0 and byte[1] == 255 and byte[2] == 255:
                gamemap.map[pixels_read -1][(y-1)-row] = PixelType.DANGER
            else:
                print("Pixel is other colour: {}".format(byte))
                print("test: {} {} {}".format(byte[0], byte[1], byte[2]))
                gamemap.map[pixels_read - 1][(y - 1)-row] = PixelType.EMPTY
            if pixels_read == x:
                row += 1
                pixels_read = 0
                img.read(padding)
            byte = img.read(3)
            pixels_read += 1
        img.close
        self.map = gamemap
        return 1, "Map loading successful."
    
