from tkinter import *
from functools import partial

shapes          = ['Circle','Square','Rectangle','Ellipse','Equilateral Triangle',
                   'Isosceles Trapezoid','Half Circle','Any Shape']
component_type  = ('Channel','Bend','Chamber','Mixer','Valve')
channel_layers  = ['Top','Middle','Bottom','N/A']
pressure_scales = ['Bar','Pa','MPa']
length_scales   = ['mm','\03BCm','nm']
size_scales     = ['mm*mm','\03BCm*\03BCm','nm*nm']
area_scales     = ['mm2','\03BCm2','nm2']


class Channel_B_Button:
    def __init__(self,master,port_button,button_place):
        self.port_button = port_button
        self.master = master
        self.button = Button(button_place,text='Bend',compound=TOP,command=self.click)
        self.button.grid(row=0,column=2)
        
        self.count  = 1
        self.place  = '-1[100,150]'
        self.channels = {}
        self.chas     = []

        self.channel_created = True
        
        self.undo_button = Button(button_place,text='undo',command=self.undo)
        self.undo_button.grid(row=1,column=2)


    def click(self):
        global cha
        if self.channel_created:
            cha     = Channel_B(self.master.master,self,self.port_button)
            cha.num = self.count
            cha.click_once_bind = cha.master.bind('<1>',cha.click_once,'+')

            self.channels[cha.channel] = cha
            self.chas.append(cha)
            self.count += 1
    
    def undo(self):
        self.chas.pop().destroy('')
    

class Channel_B_Display:
    def __init__(self,master,channel):
        self.channel = channel
        self.master  = master
        self.window  = master
        self.window.title('Channel Information')
        self.window.geometry('250x190-10000-100000')
        
        self.window.grid_columnconfigure(0,weight=3)
        self.window.grid_columnconfigure(1,weight=1)
        self.font   = 'Helvetica 10'
        self.labels = [' Channel Shape : ',
                       ' Channel Radius (mm): ',
                       ' Bend Degree (\N{degree sign}): ',
                       ' Channel Width (\u03BCm): ',
                       ' Channel Height (\u03BCm): ',
                       ' Flow Rate (\u03BCL/s) : ',
                       ]
        self.shape     = '-'
        self.radius    = '-'
        self.degree    = '-'
        self.width     = '-'
        self.height    = '-'
        self.flow_rate = '-'
        self.values    = '-'
        self.update()

        
    def update(self):
        self.values = [
                       self.shape,
                       self.radius,
                       self.degree,
                       self.width,
                       self.height,
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



class Channel_B_Edit:
    def __init__(self,master,channel):
        self.channel = channel
        self.master  = master
        self.window  = master
        self.window.geometry(f'700x100-10000-100000')# 900x100 630x150 original ('550x150+450+400')
        self.window.grid_columnconfigure(0,weight=2)
        self.window.grid_columnconfigure(1,weight=1)
        self.window.grid_columnconfigure(2,weight=1)
        self.window.grid_columnconfigure(3,weight=1)
        self.window.grid_columnconfigure(4,weight=2)
        

        
        self.font    = 'Helvetica 10'
        self.saved   = False
        self.data    = []
        self.values  = []
        self.col     = 0

        self.title       =  Label(self.window,text='Edit Channel Information',font='Arial 10 bold underline',width=30,anchor=W)
        self.save_button = Button(self.window,text='Save Changes',command=self.save_changes)#command=lambda:[,self.get_data]

        self.labels = [
                       ' Shape ',
                       ' Radius (\u03BCm)',
                       ' Degree (\N{degree sign})',
                       ' Width (\u03BCm)',
                       ' Height (\u03BCm)',
                       ' Flow Rate (\u03BCL/s)',
                       ]
        

        self.place()

    def place(self):
        self.title.grid(row=0,column=0,columnspan=3)
        self.save_button.grid(row=0,column=5)
        for label in self.labels:
            self.label = Label(self.master,text=label,font=self.font,bd=1,anchor=CENTER,width=20)
            self.label.grid(row=3,column=self.col)
            self.col += 1
        for i in range(4,5): # range(4,7) for row 4-6  (labels @ row 3)
            self.selected_shape = StringVar()
            self.selected_shape.set(shapes[i-4+2])
            self.dropdown_shapes = OptionMenu(self.window,self.selected_shape,*shapes)
            self.dropdown_shapes.grid(row=i,column=0)

            self.radius = Entry(self.window,width=10,justify='center')
            self.radius.insert(0,f'{100*(i-3)}')
            self.radius.grid(row=i,column=1)

            self.degree = Entry(self.window,width=10,justify='center')
            self.degree.insert(0,f'{10*(i-3)}')
            self.degree.grid(row=i,column=2)

            self.width = Entry(self.window,width=10,justify='center')
            self.width.insert(0,f'{200+i-4}')
            self.width.grid(row=i,column=3)

            self.height = Entry(self.window,width=10,justify='center')
            self.height.insert(0,f'{100+i-4}')
            self.height.grid(row=i,column=4)

            self.flow_rate = Entry(self.window,width=10,justify='center')
            self.flow_rate.insert(0,'')
            self.flow_rate.grid(row=i,column=5)

            self.data = [self.selected_shape,self.radius,self.degree,self.width,self.height,self.flow_rate]

    def get_data(self):
        self.values = []
        for dat in self.data:
            self.values.append(dat.get())

    def save_changes(self):
        self.saved = True
        self.get_data()

        self.channel.data = self.values.copy()
        self.channel.display.shape     = self.values[0]
        self.channel.display.radius    = self.values[1]
        self.channel.display.degree    = self.values[2]
        self.channel.display.width     = self.values[3]
        self.channel.display.height    = self.values[4]
        self.channel.display.flow_rate = self.values[5]
        self.channel.display.update()
        
        self.window.withdraw()



class Channel_B:
    def __init__(self,master,channel_button,port_button):
        self.port_button  = port_button
        self.channel_button  = channel_button
        self.master          = master
        self.edit_win        = Toplevel(self.master)
        self.disp_win        = Toplevel(self.master)
        self.display         = Channel_B_Display(self.disp_win,self)
        self.edit            = Channel_B_Edit(   self.edit_win,self)
        
        
        self.front           = None
        self.back            = None
        self.front_no        = None
        self.back_no         = None
        self.radius          = -1
        
        self.channel         = self.master.create_line(0,0,0,0,dash=(10,2),width=2,tags='line',fill='blue')
        self.label           = Label(self.master,text='Click on 2 ports to create channel',bg='dark grey')
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

        self.master.tag_bind(self.channel,'<Double-1>',partial(self.show_window,self.edit_win))
        self.master.tag_bind(self.channel,'<Enter>'   ,partial(self.show_window,self.disp_win))
        self.master.tag_bind(self.channel,'<Leave>'   ,partial(self.hide_window,self.disp_win))

    def moving(self,event):
        self.line_data['x2'] = event.x
        self.line_data['y2'] = event.y

        self.master.coords(self.channel,self.line_data['x1'], self.line_data['y1'],self.line_data['x2'], self.line_data['y2'])

        pass

    def dragged(self):
        front_coords         = self.master.coords(self.front)
        back_coords          = self.master.coords(self.back)
        self.line_data['x1'] = (front_coords[0]+front_coords[2])/2 # event.x
        self.line_data['y1'] = (front_coords[1]+front_coords[3])/2 # event.y
        self.line_data['x2'] = (back_coords[0]+back_coords[2])/2 # event.x
        self.line_data['y2'] = (back_coords[1]+back_coords[3])/2 # event.y

        self.master.coords(self.channel,self.line_data['x1'], self.line_data['y1'],
                                        self.line_data['x2'], self.line_data['y2'])

        if not self.cancel:
            self.dragged_job = self.master.after(100,self.dragged)

        
    def click_once(self,event):
        self.channel_button.channel_created = False
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
                    
                    self.master.coords(self.channel,self.line_data['x1'], self.line_data['y1'],self.line_data['x2'], self.line_data['y2'])
                    self.label.config(text='Done!')
                    self.label.place_forget()
                    self.master.itemconfig(self.channel,dash=())
                    self.channel_button.channel_created = True

                    self.master.unbind('<1>',self.click_twice_bind)
                    self.master.unbind('<Motion>',self.move_bind)
                    self.dragged()
                    break

    def destroy(self,event):
        self.cancel = True
        self.master.delete(self.channel)
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
