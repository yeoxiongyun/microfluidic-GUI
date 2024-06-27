from Results_Table import *
from Table_Class import *
from tkinter import *
from functools import partial
import os, subprocess, sys, time

def open_file(file):
    if sys.platform == 'win32':
        os.startfile(file)
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener,file])

################################################################################
VISCOSITY = '0.89d0'
DENSITY   = '997.D0'

components = {
              'CIRCLE'                  : 1,
              'SQUARE'                  : 2,
              'RECTANGLE'               : 3,
              'ELLIPSE'                 : 4,
              'EQUILATERAL TRIANGLE'    : 5,
              'ISOSCELES TRAPEZOID'     : 6,
              'HALF CIRCLE'             : 7,
              'ANY SHAPE'               : 9,
              'BEND'                    : 10,
              'CHAMBER'                 : 20,
              'MIXER'                   : 30,
              'VALVE'                   : 40,

              'Open'                    : 0,
              'Close'                   : 1
              }

component_type  = ('Channel','Bend','Chamber','Mixer','Valve')

chamber_layers  = ['Top','Middle','Bottom','N/A']
pressure_scales = ['Bar','Pa','MPa']
length_scales   = ['mm','\03BCm','nm']
size_scales     = ['mm*mm','\03BCm*\03BCm','nm*nm']
area_scales     = ['mm2','\03BCm2','nm2']


class My_Menu:
    def __init__(self,master,canvas,buttons):
        self.master       = master
        self.canvas       = canvas
        self.menu         = Menu(self.master,tearoff=False)
        self.edit_menu    = Menu(self.menu,tearoff=False)
        self.input_menu   = Menu(self.menu,tearoff=False)
        self.text_menu    = Menu(self.menu,tearoff=False)
        self.view_menu    = Menu(self.menu,tearoff=False)
        self.results_menu = Menu(self.menu,tearoff=False)
        self.save_menu    = Menu(self.menu,tearoff=False)
        self.run_menu     = Menu(self.menu,tearoff=False)
        self.help_menu    = Menu(self.menu,tearoff=False)
        self.case_menu    = Menu(self.menu,tearoff=False)

        self.curr_zoom    = 1


        self.channel_b_win = Toplevel(self.master)
        self.channel_s_win = Toplevel(self.master)
        self.chamber_win   = Toplevel(self.master)
        self.mixer_win     = Toplevel(self.master)
        self.port_win      = Toplevel(self.master)
        self.valve_win     = Toplevel(self.master)
        self.channel_b_win.title('Edit Channel Information  |  Input 01')
        self.channel_s_win.title('Edit Channel Information  |  Input 01')
        self.chamber_win.title(  'Edit Chamber Information  |  Input 01')
        self.mixer_win.title(    'Edit Mixer Information  |  Input 01')
        self.port_win.title(     'Edit Port Information | Input 02')
        self.mixer_win.title(    'Edit Valve Information  |  Input 01')
        self.table_headings = ['Channel No.',
                               'Channel Type',
                               'Upwind Port No.',
                               'Downwind Port No.',
                               'Length (mm)',
                               'Width (\u03BCm)',
                               'Height (\u03BCm)',
                               'Port No.','Pressure(bar)','Channel No.','Flow Rate (\u03BCL/s)'
                               ]
        self.channel_table  = Table(self.channel_s_win,self.table_headings[:7],[[]])
        self.port_table     = Table(self.port_win,self.table_headings[7:],[[]])

        self.table_headings = ['Channel No.',
                               'Channel Type',
                               'Upwind Port No.',
                               'Downwind Port No.',
                               'Radius (\u03BCm)',
                               'Degree (\N{degree sign})',
                               'Width (\u03BCm)',
                               'Height (\u03BCm)'
                               ]
        self.channelb_table = Table(self.channel_b_win,self.table_headings,[[]])
        self.table_headings = ['Chamber No.',
                               'Chamber Type',
                               'Upwind Port No.',
                               'Downwind Port No.',
                               'Depth (mm)',
                               'Diameter (mm)',
                               ]
        self.chamber_table  = Table(self.chamber_win,self.table_headings,[[]])

        self.table_headings = ['Mixer No.',
                               'No. of Inlet(s)',
                               'No. of Outlet(s)',
                               'Upwind Port No.',
                               'Downwind Port No.',
                               'Length (mm)',
                               'Area (mm²)',
                               'Hydraulic Resistance (Ns/m⁵)'
                               ]
        self.mixer_table     = Table(self.mixer_win,self.table_headings,[[]])
        self.table_headings = ['Valve No.',
                               'Valve Type',
                               'Valve State',
                               'Upwind Port No.',
                               'Downwind Port No.',
                               'Length (mm) | Open',
                               'Area (mm²) | Open',
                               'Hydraulic Resistance (Ns/m⁵) | Open',
                               'Length (mm) | Close',
                               'Area (mm²) | Close',
                               'Hydraulic Resistance (Ns/m⁵) | Close'
                               ]

        self.valve_table     = Table(self.valve_win,self.table_headings,[[]])
        
        self.port_button     = buttons[0]
        self.channel_button  = buttons[1]
        self.channelb_button = buttons[2]
        self.chamber_button  = buttons[3]
        self.valve_button    = buttons[4]

        self.results_table  = None

        self.saved  = False
        self.config()
        self.channel_b_win.withdraw()
        self.channel_s_win.withdraw()
        self.chamber_win.withdraw()
        self.mixer_win.withdraw()
        self.port_win.withdraw()
        self.valve_win.withdraw()
        
    def config(self):
        self.master.config(menu=self.menu)

        self.menu.add_cascade(label='Edit',menu=self.edit_menu)                 # Edit Menu
        self.edit_menu.add_cascade(label='Input',menu=self.input_menu)          # Input Menu
        
        self.input_menu.add_command(label='Introduction',command=partial(open_file,'Introduction to Network Simulation Code.pdf'))
        self.input_menu.add_command(label='User Manual',command=partial(open_file,'User Manual of Network Simulation Code.pdf'))
        self.input_menu.add_separator()
        
        self.input_menu.add_command(label='Channel (Bend) Information'    ,command=partial(self.show_window,self.channel_b_win))
        self.input_menu.add_command(label='Channel (Straight) Information',command=partial(self.show_window,self.channel_s_win))
        self.input_menu.add_command(label='Chamber Information'           ,command=partial(self.show_window,self.chamber_win))
##        self.input_menu.add_command(label='Mixer Information'             ,command=partial(self.show_window,self.mixer_win))
        self.input_menu.add_command(label='Port Information'              ,command=partial(self.show_window,self.port_win))
        self.input_menu.add_command(label='Valve Information'             ,command=partial(self.show_window,self.valve_win))
        self.input_menu.add_separator()
        self.input_menu.add_cascade(label='Text Files',menu=self.text_menu)
        self.text_menu.add_command(label='Input 01',command=partial(open_file,'INP01.DAT'))
        self.text_menu.add_command(label='Input 02',command=partial(open_file,'INP02.DAT'))
        

        self.menu.add_cascade(label='View',menu=self.view_menu)                 # View Menu
        self.view_menu.add_cascade(label='Results',menu=self.results_menu)      # Results Menu
        self.results_menu.add_command(label='New Window',command=self.open_result_in_window)
        self.results_menu.add_command(label='Text File',command=partial(open_file,'RESULT.DAT'))
        
        self.view_menu.add_separator()
        self.view_menu.add_command(label='Actual Size',command=partial(self.zoom,'reset'))
        self.view_menu.add_command(label='Zoom In',command=partial(self.zoom,'in'))
        self.view_menu.add_command(label='Zoom Out',command=partial(self.zoom,'out'))

        self.view_menu.add_separator()
        self.view_menu.add_command(label='Enter Full Screen',command=self.enter_fullscreen)
        self.view_menu.add_command(label='Exit Full Screen',command=self.exit_fullscreen)


        self.menu.add_cascade(label='Save',menu=self.save_menu)                 # Save Menu
        self.save_menu.add_command(label='Save Changes',command=self.SAVE)

        self.menu.add_cascade(label='Run',menu=self.run_menu)                   # Run Menu
        self.run_menu.add_command(label='Run Simulation',command=self.RUN)

        self.menu.add_cascade(label='Help',menu=self.help_menu)                 # Help Menu
        self.help_menu.add_command(label='GUI Tutorial',command=partial(open_file,'GUI_Tutorial.pdf'))

    def zoom(self,zoom_type):
        cx,cy = (self.canvas.winfo_width(),self.canvas.winfo_height())
        match zoom_type:
            case 'in':
                self.canvas.scale(ALL,cx,cy,1.25,1.25)
                self.curr_zoom *= 1.25
            case 'out':
                self.canvas.scale(ALL,cx,cy,0.8,0.8)
                self.curr_zoom *= 0.8
            case 'reset':
                self.canvas.scale(ALL,cx,cy,1/self.curr_zoom,1/self.curr_zoom)
                self.curr_zoom = 1
        pass


    def enter_fullscreen(self):
        self.zoom('reset')
        self.master.attributes('-fullscreen',True)
    def exit_fullscreen(self):
        self.zoom('reset')
        self.master.attributes('-fullscreen',False)

    def open_result_in_window(self):
        newWindow = Toplevel(self.master)
        newWindow.title('Simulation Results')
        newWindow.geometry('825x550')
        newWindow.attributes('-topmost', True)
        newWindow.update()

        results_table = Results_Table(newWindow)
        results_table.open()
    
    def open_channel_window(self):
        self.channel_window.overrideredirect(1)
        self.channel_window.deiconify()
    def open_port_window(self):
        self.port_window.deiconify()

    def show_window(self,win):
        win.overrideredirect(True)
        win.update()
        win.attributes('-topmost', True)
        win.update()
        win.deiconify()

    

    def CLOSE(self):
        self.master.destroy()
    
    def SAVE(self):
        self.channel_table.clear()
        self.channelb_table.clear()
        self.port_table.clear()
        # transfer data to tables
        for port in self.port_button.ports.values():
            if port.pressure:
                self.port_table.boxes = [
                                         port.num,
                                         port.pressure,
                                         '',
                                         ''
                                         ]
                self.port_table.add_from_canvas()

        for channel in self.channel_button.channels.values():
            channel.data[0] = channel.data[0].upper()
            self.channel_table.boxes = [
                                        channel.num,
                                        components[channel.data[0]],
                                        channel.front_no,
                                        channel.back_no,
                                        channel.data[1],
                                        channel.data[2],
                                        channel.data[3]
                                        ]
            self.channel_table.add_from_canvas()
            if channel.data[4] != '':
                self.port_table.boxes = [
                                         '',
                                         '',
                                         channel.num,
                                         channel.data[4]
                                         ]
                self.port_table.add_from_canvas()

        for channel in self.channelb_button.channels.values():
            channel.data[0] = channel.data[0].upper()
            self.channelb_table.boxes = [
                                        channel.num,
                                        int(components[channel.data[0]]) + 10,
                                        channel.front_no,
                                        channel.back_no,
                                        channel.data[1],
                                        channel.data[2],
                                        channel.data[3],
                                        channel.data[4]
                                        ]
            self.channelb_table.add_from_canvas()
            if channel.data[5] != '':
                self.port_table.boxes = [
                                         '',
                                         '',
                                         channel.num,
                                         channel.data[5]
                                         ]
                self.port_table.add_from_canvas()

        for chamber in self.chamber_button.chambers.values():
            chamber.data[0] = chamber.data[0].upper()
            self.chamber_table.boxes = [
                                        chamber.num,
                                        int(components[chamber.data[0]]) + 20,
                                        chamber.front_no,
                                        chamber.back_no,
                                        chamber.data[1],
                                        chamber.data[2],
                                        ]
            self.chamber_table.add_from_canvas()
            if chamber.data[3] != '':
                self.port_table.boxes = [
                                         '',
                                         '',
                                         chamber.num,
                                         chamber.data[3]
                                         ]
                self.port_table.add_from_canvas()

        for valve in self.valve_button.valves.values():
            self.valve_table.boxes = [
                                        valve.num,
                                        41,
                                        components[valve.data[0]],
                                        valve.front_no,
                                        valve.back_no,
                                        valve.data[1],
                                        valve.data[2],
                                        valve.data[3],
                                        valve.data[4],
                                        valve.data[5],
                                        valve.data[6],
                                        ]
            self.valve_table.add_from_canvas()
            if valve.data[4] != '':
                self.port_table.boxes = [
                                         '',
                                         '',
                                         valve.num,
                                         valve.data[4]
                                         ]
                self.port_table.add_from_canvas()
            
        
        self.saved = True
    
    def RUN(self):
        if not self.saved:
            self.SAVE()
        write_inp01 = [f'''Input Data for Microfluidic Network
\nViscosity (m Pa s), Density (kg/m³)
{VISCOSITY}, {DENSITY}

Channel/Component Information
''']
        write_inp02 = ['''Port/Channel Input Information for Network

1st Column
1 For Port & Pressure\n2 For Channel & Flow Rate

2nd Column
Port / Channel Number

3rd Column
Pressure (bar) or Flow Rate (uL/s)\n
''']
        for dat in self.port_table.get():
            if dat[1] != '':
                write_inp02[0] += '1 '
                write_inp02[0] += dat[0] + ' '
                write_inp02[0] += dat[1] + '\n'
            elif dat[3] != '':
                write_inp02[0] += '2 '
                write_inp02[0] += dat[2] + ' '
                write_inp02[0] += dat[3] + '\n'
        
        for dat in self.channel_table.get():
            write_inp01[0] += dat[1] + ' '
            write_inp01[0] += dat[2] + ' '
            write_inp01[0] += dat[3] + '\n'
            write_inp01[0] += dat[4] + '\n'
            write_inp01[0] += dat[5] + ' '
            write_inp01[0] += dat[6] + '\n\n'
        
        for dat in self.channelb_table.get():
            write_inp01[0] += dat[1] + ' '
            write_inp01[0] += dat[2] + ' '
            write_inp01[0] += dat[3] + '\n'
            write_inp01[0] += dat[4] + ' '
            write_inp01[0] += dat[5] + '\n'
            write_inp01[0] += dat[6] + ' '
            write_inp01[0] += dat[7] + '\n\n'

        for dat in self.chamber_table.get():
            write_inp01[0] += dat[1] + ' '
            write_inp01[0] += dat[2] + ' '
            write_inp01[0] += dat[3] + '\n'
            write_inp01[0] += dat[4] + '\n'
            write_inp01[0] += dat[5] + '\n\n'

        for dat in self.valve_table.get():
            write_inp01[0] += dat[1] + ' '
            write_inp01[0] += dat[2] + ' '
            write_inp01[0] += dat[3] + '\n'
            write_inp01[0] += dat[4] + '\n'
            write_inp01[0] += dat[5] + ' '
            write_inp01[0] += dat[6] + ' '
            write_inp01[0] += dat[7] + '\n'
            write_inp01[0] += dat[8] + ' '
            write_inp01[0] += dat[9] + ' '
            write_inp01[0] += dat[10] + '\n\n'
       
        with open('INP01.DAT','w') as f:
            f.writelines(write_inp01)
        with open('INP02.DAT','w') as f:
            f.writelines(write_inp02)
        if sys.platform == 'win32':
            os.startfile('network.exe')
        else:
            opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
            subprocess.call([opener, 'network.exe'])
        self.saved = False
        time.sleep(1)
        self.open_result_in_window()
        if os.path.exists('INP01.dat') and os.path.exists('INP02.dat'):
            pass
        else:
            pass
