from tkinter import *
from functools import partial

types          = ['Open','Close']

class Valve_Button:
    def __init__(self,master,port_button,button_place):
        self.port_button = port_button
        self.master = master
        self.button = Button(button_place,text='Valve',compound=TOP,command=self.click)
        self.button.grid(row=0,column=5)
        
        self.count  = 1
        self.place  = '-1[100,150]'
        self.valves = {}
        self.chas   = []

        self.valve_created = True

        self.delete_last_button = Button(button_place,text='undo',command=self.undo)
        self.delete_last_button.grid(row=1,column=5)


    def click(self):
        global cha
        if self.valve_created:
            cha     = Valve(self.master.master,self,self.port_button)
            cha.num = self.count
            cha.click_once_bind = cha.master.bind('<1>',cha.click_once,'+')

            self.valves[cha.valve] = cha
            self.chas.append(cha)
            self.count += 1

    def undo(self):
        self.chas.pop().destroy('')
    

class Valve_Display:
    def __init__(self,master,valve):
        self.valve   = valve
        self.master  = master
        self.window  = master
        self.window.title('Valve Information')
        self.window.geometry('250x160-10000-100000')
        
        self.window.grid_columnconfigure(1,weight=1)
        self.window.grid_columnconfigure(0,weight=2)
        
        self.font   = 'Helvetica 10'
        self.labels = [' Valve Type : ',
                       ' Valve Length (mm): ',
                       ' Valve Area (mm²)',
                       ' Hydraulic Res. (Ns/m⁵)',
                       ' Flow Rate (\u03BCL/s) : '
                       ]
        self.type       = '-'
        self.length     = '-'
        self.area       = '-'
        self.resistance = '-'
        self.flow_rate  = '-'
        self.values     = '-'
        self.update()

        
    def update(self):
        self.values = [
                       self.type,
                       self.length,
                       self.area,
                       self.resistance,
                       self.flow_rate,
                       ]
        
        self.row = 3
        for label in self.labels:
            self.label = Label(self.window,text=label,font=self.font,bd=5,anchor=W,width=25) # width = 15
            self.label.grid(row=self.row,column=0)
            a = self.row
            value = self.values[a-3]
            self.label = Label(self.window,text=value,font=self.font,bd=5,anchor=E,width=15) # width = 15
            self.label.grid(row=self.row,column=1)
            self.row += 1



class Valve_Edit:
    def __init__(self,master,valve):
        self.valve = valve
        self.master  = master
        self.window  = master
        self.window.geometry(f'630x120-10000-100000')# 900x100 630x150 original ('550x150+450+400')
        self.window.grid_columnconfigure(0,weight=2)
        self.window.grid_columnconfigure(1,weight=2)
        self.window.grid_columnconfigure(2,weight=2)
        self.window.grid_columnconfigure(3,weight=1)
        self.window.grid_columnconfigure(4,weight=2)
        

        
        self.font    = 'Helvetica 10'
        self.saved   = False
        self.data    = []
        self.values  = []
        self.col     = 0

        self.title       =  Label(self.window,text='Edit Valve Information',font='Arial 10 bold underline',width=30,anchor=W)
        self.save_button = Button(self.window,text='Save Changes',command=self.save_changes)

        self.labels = [
                       ' Type ',
                       ' Length (mm)',
                       ' Area (mm²)',
                       ' Hydraulic Res.(Ns/m⁵)',
                       ' Flow Rate (\u03BCL/s) : ',
                       ]
        

        self.place()

    def place(self):
        self.title.grid(row=0,column=0,columnspan=3)
        self.save_button.grid(row=0,column=4)
        for label in self.labels:
            self.label = Label(self.master,text=label,font=self.font,bd=1,anchor=CENTER,width=20)
            self.label.grid(row=3,column=self.col)
            self.col += 1
        for i in range(4,5): # range(4,7) for row 4-6  (labels @ row 3)
            self.selected_type = StringVar()
            self.selected_type.set(types[i-4])
            self.dropdown_types = OptionMenu(self.window,self.selected_type,*types)
            self.dropdown_types.grid(row=i+2,column=4)

            self.label = Label(self.window,text='Open ––>',font=self.font,bd=1,anchor=CENTER,width=20)
            self.label.grid(row=i,column=0)

            self.label = Label(self.window,text='Close ––>',font=self.font,bd=1,anchor=CENTER,width=20)
            self.label.grid(row=i+2,column=0)

            self.length = Entry(self.window,width=10,justify='center')
            self.length.insert(0,f'{0.1*(i-3)}')
            self.length.grid(row=i,column=1)

            self.area = Entry(self.window,width=10,justify='center')
            self.area.insert(0,'0.02')
            self.area.grid(row=i,column=2)

            self.resistance = Entry(self.window,width=10,justify='center')
            self.resistance.insert(0,'1.e10')
            self.resistance.grid(row=i,column=3)

            self.flow_rate = Entry(self.window,width=10,justify='center')
            self.flow_rate.insert(0,'')
            self.flow_rate.grid(row=i,column=4)

            self.length2 = Entry(self.window,width=10,justify='center')
            self.length2.insert(0,f'{0.1*(i-3)}')
            self.length2.grid(row=i+2,column=1)

            self.area2 = Entry(self.window,width=10,justify='center')
            self.area2.insert(0,'0.0002')
            self.area2.grid(row=i+2,column=2)

            self.resistance2 = Entry(self.window,width=10,justify='center')
            self.resistance2.insert(0,'1.e20')
            self.resistance2.grid(row=i+2,column=3)

            self.data = [self.selected_type,self.length,self.area,self.resistance,
                         self.length2,self.area2,self.resistance2,self.flow_rate]

    def get_data(self):
        self.values = []
        for dat in self.data:
            self.values.append(dat.get())

    def save_changes(self):
        self.saved = True
        self.get_data()

        self.valve.data = self.values.copy()
        self.valve.display.type        = self.values[0]
        self.valve.display.length      = self.values[1]
        self.valve.display.area        = self.values[2]
        self.valve.display.resistance  = self.values[3]
        self.valve.display.length2     = self.values[4]
        self.valve.display.area2       = self.values[5]
        self.valve.display.resistance2 = self.values[6]
        self.valve.display.flow_rate   = self.values[7]
        self.valve.display.update()
        
        self.window.withdraw()



class Valve:
    def __init__(self,master,valve_button,port_button):
        self.port_button     = port_button
        self.valve_button    = valve_button
        self.master          = master
        self.edit_win        = Toplevel(self.master)
        self.disp_win        = Toplevel(self.master)
        self.display         = Valve_Display(self.disp_win,self)
        self.edit            = Valve_Edit(   self.edit_win,self)
        
        
        self.front           = None
        self.back            = None
        self.front_no        = None
        self.back_no         = None
        self.length          = -1
        
        self.valve         = self.master.create_line(0,0,0,0,dash=(10,2),width=2,tags='valve',fill='purple')
        self.label           = Label(self.master,text='Click on 2 ports to create valve',bg='dark grey')
        self.data            = []
        self.line_data       = {'x1': 0,'y1': 0,'x2': 0,'y2': 0} # self.event_data = {'x': 0,'y': 0}
        

        self.click_twice_bind = -1
        self.dragged_bind     = -1
        self.move_bind        = -1
        self.cancel           = False

        self.label.place(x=0,y=10)
        self.disp_win.withdraw()
        self.edit_win.withdraw()



    def bind(self):
        self.master.unbind('<1>',self.click_once_bind)
        self.click_twice_bind = self.master.bind('<1>',self.click_twice,'+')
        self.move_bind        = self.master.bind('<Motion>',self.moving,'+')

        self.master.tag_bind(self.valve,'<Double-1>',partial(self.show_window,self.edit_win))
        self.master.tag_bind(self.valve,'<Enter>'   ,partial(self.show_window,self.disp_win))
        self.master.tag_bind(self.valve,'<Leave>'   ,partial(self.hide_window,self.disp_win))

    def moving(self,event):
        self.line_data['x2'] = event.x
        self.line_data['y2'] = event.y

        self.master.coords(self.valve,self.line_data['x1'], self.line_data['y1'],self.line_data['x2'], self.line_data['y2'])

        pass

    def dragged(self):
        front_coords         = self.master.coords(self.front)
        back_coords          = self.master.coords(self.back)
        self.line_data['x1'] = (front_coords[0]+front_coords[2])/2 # event.x
        self.line_data['y1'] = (front_coords[1]+front_coords[3])/2 # event.y
        self.line_data['x2'] = (back_coords[0]+back_coords[2])/2 # event.x
        self.line_data['y2'] = (back_coords[1]+back_coords[3])/2 # event.y

        self.master.coords(self.valve,self.line_data['x1'], self.line_data['y1'],
                                        self.line_data['x2'], self.line_data['y2'])

        if not self.cancel:
            self.dragged_job = self.master.after(100,self.dragged)

        
    def click_once(self,event):
        self.valve_button.valve_created = False
        r = 20
        x = event.x
        y = event.y
        n_overlap = self.master.find_overlapping(x-r,y-r,x+r,y+r)

        if len(n_overlap) > 1:
            for obj in n_overlap:
                if self.master.type(obj) == 'oval':
                    obj_coords           = self.master.coords(obj)
                    self.line_data['x1'] = (obj_coords[0]+obj_coords[2])/2 # event.x
                    self.line_data['y1'] = (obj_coords[1]+obj_coords[3])/2 # event.y
                    self.front_no = self.port_button.ports[obj].num
                    self.front = obj

                    self.label.config(text='Click on another port')
                    self.bind()
                    break
 
    def click_twice(self,event):
        r = 20
        x = event.x
        y = event.y
        n_overlap = self.master.find_overlapping(x-r,y-r,x+r,y+r)
        
        if len(n_overlap) > 1:
            for obj in n_overlap:
                if self.master.type(obj) == 'oval' and obj != self.front:
                    obj_coords           = self.master.coords(obj)
                    self.line_data['x2'] = (obj_coords[0]+obj_coords[2])/2 # event.x
                    self.line_data['y2'] = (obj_coords[1]+obj_coords[3])/2 # event.y
                    self.back_no = self.port_button.ports[obj].num
                    self.back = obj
                    
                    self.master.coords(self.valve,self.line_data['x1'], self.line_data['y1'],self.line_data['x2'], self.line_data['y2'])
                    self.label.config(text='Done!')
                    self.label.place_forget()
                    self.master.itemconfig(self.valve,dash=())
                    self.valve_button.valve_created = True

                    self.master.unbind('<1>',self.click_twice_bind)
                    self.master.unbind('<Motion>',self.move_bind)
                    self.dragged()
                    break

    def destroy(self,event):
        self.cancel = True
        self.master.delete(self.valve)
        self.edit_win.destroy()
        self.disp_win.destroy()
        self.master.after_cancel(self.dragged)
        
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
