from coordinates import Coordinates

class Player():
    
    def __init__(self, x, y):
        
        self.coordinates = Coordinates(x,y)
        self.alive = True
        
        self.xspeed = 0
        self.xacceleration = 1
        self.yspeed = 0
        self.yacceleration = 2
        
        self.maxspeed = 3
        
        self.offset = Coordinates(0,0)
        
        self.movingleft = False             # Signaali GUI:n näppäinpainalluksesta
        self.movingright = False            # Signaali GUI:n näppäinpainalluksesta
        
        self.jumpcond = 0                   # Hypyn "ajastin"
        self.jumping = False                # Signaali GUI:n näppäinpainalluksesta
        
    def move(self):
        
        if self.movingleft == True:
            self.left()
            self.offset.x += self.xspeed
            
        elif self.movingright == True:
            self.right()
            self.offset.x += self.xspeed
            
        else:
            if self.xspeed > 0:
                self.xspeed = self.xspeed - self.xacceleration
                if self.xspeed < 0:
                    self.xspeed = 0
                    
            elif self.xspeed < 0:
                self.xspeed = self.xspeed + self.xacceleration
                if self.xspeed > 0:
                    self.xspeed = 0
                    
        if self.jumpcond > 0:
            self.offset.y += self.yspeed
            self.jumpcond -= 1
        if self.jumping == True:
            if self.jumpcond > 0:
                self.yspeed += self.yacceleration
            else:
                self.jumping = False
            self.jumpcond -= 1
          
    def jump(self):
        if self.jumpcond > 20:
            return
        self.jumpcond = 60
        self.yspeed += self.yacceleration * 2
    
    def left(self):
       
        self.xspeed += self.xacceleration
        if self.xspeed > self.maxspeed:
            self.xspeed = self.maxspeed
        
    def right(self):
                
        self.xspeed -= (self.xacceleration)
        if self.xspeed < -self.maxspeed:
            self.xspeed = -self.maxspeed
    