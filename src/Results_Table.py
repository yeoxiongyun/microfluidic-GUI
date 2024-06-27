from tkinter import *
from tkinter import ttk

class Results_Table(ttk.Treeview):
    def __init__(self,master):
        super().__init__()
##        self.table2_hori_scroll = Scrollbar(self.master,orient='horizontal')
##        self.table2_hori_scroll.grid(row=11)
        self.master  = master
        self.frame1  = Frame(self.master)
        self.frame2  = Frame(self.master)
        self.frame1.pack(fill=BOTH,expand=1)
        self.frame2.pack(fill=BOTH,expand=1)
        self.table1_vert_scroll = Scrollbar(self.frame1)
        self.table2_vert_scroll = Scrollbar(self.frame2)
        self.table1_vert_scroll.pack(side=RIGHT,fill=Y)
        self.table2_vert_scroll.pack(side=RIGHT,fill=Y)
        self.table1 = ttk.Treeview(self.frame1,yscrollcommand=self.table1_vert_scroll.set)
        self.table2 = ttk.Treeview(self.frame2,yscrollcommand=self.table2_vert_scroll.set)
        self.table1.pack(fill=BOTH,expand=1)
        self.table2.pack(fill=BOTH,expand=1)
        self.table1.pack(side=TOP)
        self.table2.pack(side=BOTTOM)
        self.table1_vert_scroll.config(command=self.table1.yview)
        self.table2_vert_scroll.config(command=self.table2.yview)
        self.table1_headings = ['No.',
                                'Component Name',
                                'Hydraulic Resistance (Ns/m⁵)',
                                'Flow Rate (uL/s)',
                                'Remarks',
                                'Flow Time (s)'
                                ]
        self.table2_headings = ['Port No.',
                                'Port Pressure (bar)',
                                'Remarks'
                                ]
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('Treeview',
                             background='light grey',
                             foreground='black',
                             fieldbackground='silver',
                             rowheight=25)
        self.style.map('Treeview',background=[('selected','silver')])
        self.table1.tag_configure('SOLVED',background='light green')
        self.table2.tag_configure('SOLVED',background='light green')
        self.table1['columns'] = tuple(self.table1_headings)
        self.table2['columns'] = tuple(self.table2_headings)
        self.table1.column( '#0',width=0,stretch=NO)
        self.table1.heading('#0',text='',anchor=CENTER)
        self.table2.column( '#0',width=0,stretch=NO)
        self.table2.heading('#0',text='',anchor=CENTER)

        for heading in self.table1_headings:
            self.table1.column(heading,anchor=CENTER,width=len(heading)*5+70,stretch=YES) ## stretching = YES
            self.table1.heading(heading,text=heading,anchor=CENTER)

        for heading in self.table2_headings:
            self.table2.column(heading,anchor=CENTER,width=len(heading)*3+70,stretch=YES) ## stretching = YES
            self.table2.heading(heading,text=heading,anchor=CENTER)

        self.data  = []
        self.lines = ''
        self.print_port = False
        self.line_counter = 0

    def open(self):
        with open('RESULT.DAT') as f:
            self.data = []
            self.print_port = False
            self.lines = f.readlines()
            self.line_counter = 0
            for line in self.lines:
                self.line_counter += 1
                line = line.replace('D+00','')
                line = line.replace('0.000000','0')
                if 'RESULTS OF PRESSURE OF PORTS' in line or 'bar' in line:
                    self.print_port = True
                    continue
                if self.line_counter >= 5 and not self.print_port and len(line) > 10:
                    self.tag(self.table1,line,line.replace('LINE','').split())
                elif self.print_port:
                    self.tag(self.table2,line,line.split())
    
    def tag(self,table,line,val):
        self.data.append(val)
        if 'SOLVED' in line:
            table.insert(parent='',index='end',iid=val[0],text='',values=val,tags='SOLVED')
        else:
            table.insert(parent='',index='end',iid=val[0],text='',values=val)
