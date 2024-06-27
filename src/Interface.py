from Menu_Bar_Class  import *

from Channel_B_Class import *
from Channel_S_Class import *
from Chamber_Class   import *
from Valve_Class     import *
from Port_Class      import *

from tkinter import *
from functools import partial

def create_grid(master):
    w = h = 100000
    # creates all horizontal & vertical lines at intervals of 10
    for i in range(-w, w, 10):
        master.create_line([(i, -h),(i, h)],width=1,fill='light grey', tag='grid_line')
    for i in range(-h, h, 10):
        master.create_line([(-w, i),(w, i)],width=1,fill='light grey', tag='grid_line')
    # master.delete('grid_line') # will only remove the grid_line

class MF_GUI():
    def __init__(self):
        self.root   = Tk()
        self.root.title('Microfluidic Simulator')
        self.root.geometry('700x500')
        self.frame  = Frame(self.root,bg='dark grey',width=800,height=500)
        self.frame1 = Frame(self.frame,bg='light blue',width=10000,height=3)
        self.frame2 = Frame(self.frame,bg='silver',width=10000,height=100)
        self.canvas = Canvas(self.frame,bg='white',width=10000,height=10000) # systemTransparent
        self.frame1.pack_propagate(False)
        self.frame2.pack_propagate(False)
        self.frame.pack(fill=BOTH)
        self.frame1.pack(fill=BOTH)
        self.frame2.pack(fill=BOTH)
        self.canvas.pack(fill=BOTH)

        self.canvasframe = Canvas(self.canvas,width=10000,height=100,bg='silver')
        self.canvasframe.grid_propagate(False)
        self.canvas.create_window((0,0),window=self.canvasframe,anchor=NW)
        

        self.grid = create_grid(self.canvas)

        self.p  = Port_Button(self.canvasframe,self.frame2)
        self.cs = Channel_S_Button(self.canvasframe,self.p,self.frame2)
        self.cb = Channel_B_Button(self.canvasframe,self.p,self.frame2)
        self.ch = Chamber_Button(self.canvasframe,self.p,self.frame2)
        self.v  = Valve_Button(self.canvasframe,self.p,self.frame2)

        self.canvas.bind('<Motion>',self.hide_all_windows,'+')        
        self.menu_bar = My_Menu(self.root,self.canvas,[self.p,self.cs,self.cb,self.ch,self.v])
        self.canvasframe.destroy()
        self.root.mainloop()

    def hide_all_windows(self,event):
        for port in self.p.ports.values():
            port.disp_win.withdraw()
        for chan in self.cs.channels.values():
            chan.disp_win.withdraw()
        
if __name__ == '__main__':
    gui = MF_GUI()
