"""
Visualization Program

This Python program provides a graphical visualization of a lens system with an object and its images, allowing you to explore the behavior of light and optics.

Usage:
1. Run the program.
2. The program displays a graphical interface with controls for adjusting the position, size, and focal length of the lens system.
3. Adjust the "Position" slider to change the position of the object relative to the lens system.
4. Use the "Size" slider to modify the size of the object.
5. The "Focale" slider lets you set the focal length of the lens.
6. The program will dynamically update and show the positions and characteristics of the object and its images.
7. Different colors represent different images produced by the lens system.

Key Components:
- The `CommandFrame` class provides sliders for adjusting position, size, and focal length.
- The `GraphCanvas` class displays the lens system and updates based on the user's input.
- The `Objet` class represents the object and its images, and it calculates their positions and characteristics.
- The `Lentille` class defines the lens and its properties, including focal length and height.

Notes:
- A real object has a positive position, while a virtual object has a negative position.
- The program uses optical principles to calculate and visualize the object's images formed by the lens.
- The number of displayed images can be adjusted by changing the 'nb_image' variable.

Explore the behavior of light and lenses by adjusting the controls and observing how the object's images change. This program is a useful tool for understanding optical concepts visually.
"""

from math import *
from tkinter import *
W = 500
H = 500
COLOR = '#aaa'
BG = 'black'
C=['red', 'green', 'blue', 'yellow', 'purple', 'brown', 'cyan']
POSITION = -100
HEIGHT = 100 
FOCALE = 50


class Command(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = 10
        self.focale = 10
        self.size = 10

        Scale(
            root, length=300, orient=HORIZONTAL, sliderlength=10,
            label='position :', from_=-250, to=250,
            command=self.get_position,relief=GROOVE, bd=2).pack(fill=X)

        Scale(
            root, length=300, orient=HORIZONTAL, sliderlength=10,
            label='size :', from_=-150, to=150,
            command=self.get_size,relief=GROOVE, bd=2).pack(fill=X)

        Scale(
            root, length=300, orient=HORIZONTAL, sliderlength=10,
            label='focale :', from_=-250, to=250,
            command=self.get_focale,relief=GROOVE, bd=2).pack(fill=X)

    def get_position(self, pos):
        self.position = int(pos)
        self.event_generate('<Control-Z>')
    
    def get_focale(self, focale):
        self.focale = int(focale)
        self.event_generate('<Control-Z>')
        
    def get_size(self, focale):
        self.size = int(focale)
        self.event_generate('<Control-Z>')
        


class Graph(Canvas):
    '''canvas'''    
    def __init__(self, *args, l=None, objet=None , nb_image = 3, com = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.mid_W = W / 2
        self.mid_H = H / 2
        self.nb_image =nb_image
        self.l = l
        self.objet = objet
        self.com = com

        self.draw_axe()
        self.master.bind('<Control-Z>', self.draw)

    def draw_axe(self):
        self.create_line((0, self.mid_H), (W, self.mid_H), fill='white') # axe optique
        self.l.pos = self.mid_W
        self.create_line(
            self.mid_W, self.mid_H + self.in_ech(self.l.height)/2, 
            self.mid_W, self.mid_H - self.in_ech(self.l.height)/2, 
            fill='white', width=2, arrow = BOTH)

    def in_ech(self,val):
        ech = 60
        return 50 * val
    
    def draw(self, event):
        self.delete(ALL)
        self.draw_axe()
        self.l.focale = self.com.focale
        self.objet.pos = self.com.position
        self.objet.height = self.com.size
        images = []
        images.append(self.objet)
        for i in range(self.nb_image+1):
            im = Objet(lentille=self.l)
            im.image(images[i-1])
            images.append(im)
        
        
        for i in range(0,len(images)):
            self.create_line(
            images[i].pos + self.mid_W,
            self.mid_H, 
            images[i].pos + self.mid_W,
            self.mid_H - images[i].height,
            fill = C[i], width = 2, arrow = LAST
        )
            if i < len(images)-1:
                self.create_line(
                    images[i].pos + self.mid_W,
                    self.mid_H - images[i].height,
                    images[i+1].pos + self.mid_W,
                    self.mid_H - images[i+1].height,
                    fill= COLOR
                )
                self.create_line(
                    images[i].pos + self.mid_W,
                    self.mid_H - images[i].height,
                    self.mid_W,
                    self.mid_H - images[i].height,
                    fill= COLOR
                )
                self.create_line(
                    self.mid_W,
                    self.mid_H - images[i].height,
                    images[i+1].pos + self.mid_W,
                    self.mid_H - images[i+1].height,
                    fill= COLOR
                )
            
        
class Objet:
    '''all about the object an it image'''
    def __init__(self, height=HEIGHT, pos=POSITION, lentille=None):
        self.pos = pos
        self.nature = self.nat(pos)
        self.sens = 1
        self.height = height
        self.lentille = lentille

    def nat(self, pos):
        return 'r' if pos >= 0 else 'v'

    def image(self, obj):
        if isinstance(obj, Objet):
            f = obj.lentille.focale
            d_OA = obj.pos

            self.pos = (f * d_OA) / (f + d_OA) if f + d_OA != 0 else 0.1
            self.nature = self.nat(self.pos)
            self.sens = self.pos / d_OA if d_OA != 0 else 0.1
            self.height = obj.height * abs(self.sens)

            if self.sens <= 0:
                self.height = -self.height


class Lentille:
    """about the lentille"""
    def __init__(self, nature='d', focale=FOCALE, height=4):
        self.focale = focale
        self.height = height
        self.pos = 0
        self.nature = 'c' if focale > 0 else "d"
        self.vergence = 1 / self.focale
    

if __name__ == '__main__':
    root = Tk()
    root.update()
    lentille = Lentille()
    objet = Objet(lentille=lentille)
    
    com = Command(root)
    plan = Graph(root, l=lentille,nb_image=2, objet=objet, com=com, width=W, height=H, bg=BG)
    plan.pack()
    com.pack()

    root.mainloop()