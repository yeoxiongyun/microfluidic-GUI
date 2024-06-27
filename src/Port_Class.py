from tkinter import *
from functools import partial

class Port_Button:
    def __init__(self,master,button_place):
        self   = self
        self.master = master
        self.button = Button(button_place,text='Port',compound=TOP,command=self.click)
        self.button.grid(row=0,column=0)
        self.count  = 1
        self.place  = [50,50]
        self.ports  = {}
        self.new_ports = []

        self.delete_last_button = Button(button_place,text='undo',command=self.undo)
        self.delete_last_button.grid(row=1,column=0)
        
    def click(self):
        global new_port
        new_port = Port(self.master.master,self)
        new_port.create(self.place)
        new_port.center            = self.place.copy()
        new_port.num               = self.count
        self.ports[new_port.port]  = new_port
        self.new_ports.append(new_port)
        new_port.text              = new_port.master.create_text((new_port.center),text=new_port.num)
        new_port.canvas_enter_bind = new_port.master.tag_bind(new_port.port,'<Enter>',new_port.canvas_enter,'+')
        
        self.count    += 1
        self.place[0] += 10
        self.place[1] += 10
        if self.place[0] >= 200:
            self.place = [50,50]

    def undo(self):
        self.new_ports.pop().destroy('')        


class Port_Edit:
    def __init__(self,master,port):
        self.port   = port
        self.master = master
        self.window = master
        self.window.geometry(f'330x70-10000-10000')
        
        self.label = 'Port Pressure (bar)'
        self.font  = 'Helvetica 10'
        self.saved = False
        self.data  = []
        
        self.title         =  Label(self.window,text='Edit Port Information',font='Arial 10 bold underline',width=30,anchor=W)
        self.save_button   = Button(self.window,text='Save Changes',command=self.save_changes)#command=lambda:[printt,self.get_data]
        self.label         =  Label(self.window,text=self.label,font=self.font,bd=5,anchor=CENTER,width=20)
        self.port_pressure =  Entry(self.window,width=10,justify='right') 
        
        self.place()
        

    def place(self):
        self.title.grid(row=0,column=0,columnspan=2)
        self.save_button.grid(row=0,column=1)
        self.label.grid(row=3,column=0)
        self.port_pressure.insert(0,'')
        self.port_pressure.grid(row=3,column=1)
        
    def get_data(self):
        self.data = self.port_pressure.get()

    def save_changes(self):
        self.saved = True
        self.get_data()
        self.window.withdraw()
        
        self.port.pressure =  self.data
        self.port.display.pressure = self.data
        self.port.display.update()
        

class Port_Display:
    def __init__(self,master,port):
        self.port   = port
        self.master = master
        self.window = master
        self.window.title('Port Information')
        self.window.geometry('150x30-10000-10000')
        
        self.window.grid_columnconfigure(0,weight=1)
        self.window.grid_columnconfigure(1,weight=10)
        self.font   = 'Helvetica 10'
        self.width  = 15
        self.pressure = '-'
        self.label  = Label(self.window,text=' Port Pressure (bar) : ',
                            font=self.font,bd=5,anchor=W,width=self.width)
        self.value  = Label(self.window,text=self.pressure,font=self.font,
                            bd=5,anchor=E,width=self.width)
        self.row    = 1
        self.label.grid(row=self.row,column=0)
        self.value.grid(row=self.row,column=1)

    def update(self):
        self.value.config(text=self.pressure)



class Port:
    def __init__(self,master,port_button):
        self.port_button  = port_button
        self.master       = master
        self.radius       = 20
        self.port         = ''
        self.disp_win     = Toplevel(self.master)
        self.edit_win     = Toplevel(self.master)
        self.display      = Port_Display(self.disp_win,self)
        self.edit         = Port_Edit(   self.edit_win,self)

        self.label        = Label(self.master,text='')
        
        self.clicked      = False
        self.connected    = False
        self.connected_to = set()
        self.event_data   = {'x': 0, 'y': 0}
        self.pressure     = ''

        self.label.place(x=0,y=105)
        self.disp_win.withdraw()
        self.edit_win.withdraw()
    
    def canvas_enter(self,event):
        self.label.place_forget()
        self.master.itemconfig(self.port,fill='grey') # change colour
        self.bind()

    def create(self,center):
        self.port = self.create_circle(*center,self.radius,tags=('port'),fill='light grey')
    
    def create_circle(self, x, y, r, **kwargs):
        return self.master.create_oval(x-r,y-r,x+r,y+r,**kwargs)

    def get_cursor(self):
        cursor_x = self.master.winfo_pointerx() #- self.master.winfo_rootx()
        cursor_y = self.master.winfo_pointery() #- self.master.winfo_rooty()
        return (cursor_x,cursor_y)

    def hide_window(self,win,event):
        win.withdraw()

    def show_window(self,win,event):
        cx,cy = self.get_cursor()
        win.geometry(f'+{cx+10}+{cy+10}')
        win.update()
        win.overrideredirect(1)
        win.update()
        win.attributes('-topmost', True)
        win.update()
        win.deiconify()


    def destroy(self,event):
        self.port_button.count -= 1
        self.disp_win.destroy()
        self.edit_win.destroy()
        self.master.delete(self.port,self.text)


    def bind(self):
        self.master.unbind('<Enter>',self.canvas_enter_bind)
        
        self.master.tag_bind(self.port,'<1>',self.drag_start,'+')
        self.master.tag_bind(self.port,'<ButtonRelease-1>',self.drag_stop,'+')
        self.master.tag_bind(self.port,'<B1-Motion>',self.drag,'+')

        self.master.tag_bind(self.port,'<Double-1>',partial(self.show_window,self.edit_win),'+')
        self.master.tag_bind(self.text,'<Double-1>',partial(self.show_window,self.edit_win),'+')
        self.master.tag_bind(self.port,'<Enter>'   ,partial(self.show_window,self.disp_win),'+')
        self.master.tag_bind(self.text,'<Enter>'   ,partial(self.show_window,self.disp_win),'+')
        self.master.tag_bind(self.port,'<Leave>'   ,partial(self.hide_window,self.disp_win),'+')
        self.master.tag_bind(self.text,'<Leave>'   ,partial(self.hide_window,self.disp_win),'+')

        self.master.update()

    def drag_start(self,event):
        self.master.itemconfig(self.port,width=1.5)
        self.master.tag_raise(self.port)
        self.master.tag_raise(self.text)
        self.event_data['x'] = event.x
        self.event_data['y'] = event.y

    def drag_stop(self,event):
        self.master.itemconfig(self.port,width=1)
        self.event_data['x'] = 0
        self.event_data['y'] = 0

    def drag(self,event):
        delta_x = event.x - self.event_data['x']
        delta_y = event.y - self.event_data['y']
        self.center[0] += delta_x
        self.center[1] += delta_y
        self.master.move(self.port,delta_x, delta_y)
        self.master.move(self.text,delta_x, delta_y)
        self.event_data['x'] = event.x
        self.event_data['y'] = event.y
