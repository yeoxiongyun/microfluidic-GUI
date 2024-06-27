from tkinter import *
from tkinter import ttk

class Table(ttk.Treeview):
    def __init__(self,master,headings,data):
        super().__init__()
        self.master = master
        self.hori_scroll = Scrollbar(master,orient='horizontal')
        self.hori_scroll.pack(side=BOTTOM,fill=X)
        self.vert_scroll = Scrollbar(master)
        self.vert_scroll.pack(side=RIGHT,fill=Y)
        
        self.table = ttk.Treeview(master,yscrollcommand=self.vert_scroll.set,
                                         xscrollcommand=self.hori_scroll.set)
        self.hori_scroll.config(command=self.table.xview)
        self.vert_scroll.config(command=self.table.yview)
        self.table.pack()

        self.table['columns'] = tuple(headings)
        self.table.column('#0', width=0,stretch=NO)
        self.table.heading('#0',text='',anchor=CENTER) ## stretching = NO
        self.table.headings = headings

        self.frame = Frame(master)
        self.frame.pack(pady=20)
        self.add_entry_labels = []
        self.add_entry_boxes  = []
        self.boxes            = []
        for heading in headings:
            self.table.column(heading,anchor=CENTER,width=len(heading)*3+70,stretch=YES) ## stretching = YES
            self.table.heading(heading,text=heading,anchor=CENTER)
            self.add_entry_labels.append(Label(self.frame,text=heading,width=15,font=('Arial',10)))
            self.add_entry_boxes.append(Entry(self.frame,width=10))

        for i in range(len(self.add_entry_labels)):
            self.add_entry_labels[i].grid(row=0,column=i)
            self.add_entry_boxes[i].grid(row=1,column=i)
        self.iid_val = 0
        self.data = data
        
        self.add_button             = Button(master, text='Add Entry'      ,bd=0,width=15,height=1,command=self.add)
        self.update_button          = Button(master, text='Update Selected',bd=0,width=15,height=1,command=self.update)
        self.delete_selected_button = Button(master, text='Delete Selected',bd=0,width=15,height=1,command=self.delete)
        self.clear_button           = Button(master, text='Clear All'      ,bd=0,width=15,height=1,command=self.clear)
        self.close_button           = Button(master, text='Close Window'   ,bd=0,width=15,height=1,command=self.master.withdraw)

        self.table_buttons = x = [self.add_button,self.update_button,self.delete_selected_button,self.clear_button,self.close_button]
        for button in self.table_buttons:
            button.pack(side=LEFT,anchor=S)

        if data[0]:
            for dat in data:
                self.table.insert(parent='',index='end',iid=self.iid_val,text='',values=dat)
                self.iid_val += 1

    def get(self):
        self.data = []
        for dat in self.table.get_children():
            self.data.append(self.table.item(dat,'values'))
        return self.data
    
    def add(self):
        for box in self.add_entry_boxes: # get data in entry box
            self.boxes.append(box.get())
        if self.add_entry_boxes[0].get() != '' or self.add_entry_boxes[-1].get() != '': # first or last entry box cannot be empty (can change)
            self.table.insert(parent='',index='end',iid=self.iid_val,text='',values=self.boxes)
        self.iid_val += 1
        self.boxes.clear()
        for entry in self.add_entry_boxes: # clear entry boxes after data is transferred
            entry.delete(0,END)

    def add_from_canvas(self):
        self.table.insert(parent='',index='end',iid=self.iid_val,text='',values=self.boxes)
        self.iid_val += 1
        self.boxes.clear()
    
    def update(self):
        selected = self.table.focus()[0] # or self.table.selection()[0]
        selected_values = self.table.item(selected,'values')
        if self.add_entry_boxes[0].get():
            for box in self.add_entry_boxes: # get data in entry box
                self.boxes.append(box.get())
            self.table.item(selected,text='',values=self.boxes)
            self.boxes.clear()
            for entry in self.add_entry_boxes: # clear boxes after data is transferred
                entry.delete(0,END)
            
        else:
            for i in range(len(self.add_entry_boxes)):
                self.add_entry_boxes[i].insert(0,selected_values[i])

    def delete(self):
        selected = self.table.selection()
        for record in selected:
            self.table.delete(record)
    
    def clear(self):
        for record in self.table.get_children():
            self.table.delete(record)

    def append(self,new_data):
        self.table.insert(parent='',index='end',iid=self.iid_val,text='',values=new_data)
        self.iid_val += 1
