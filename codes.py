from tkinter import *
import random
from PIL import Image, ImageTk
import tkinter.filedialog
from os import listdir
from os.path import isfile, join
class ButtonRow:
    def __init__(self,row,initial=0,**gridprops):
        self.buttons = []
        self.row = row
        self.initial=initial
        self.gridprops = gridprops
    def __add__(self,other):
        self.buttons.append(other)
        self.buttons[-1].grid(row=self.row,
                              column=self.initial+len(self.buttons),
                             **self.gridprops)
    def __iadd__(self,other):
        self+other
        return self
        
class App:
    button_properties = dict(width=20,height=5,justify="center")
    def __init__(self):
        self.chosen_path = "/mnt/beegfs/scratch-noraid/ktisanic/data/PeriodFinding/plots/ZTF lightcurves/check/NTerms1/"
        self.master = Tk()
        self.master.configure(background='white')
        self.Number_of_rows=0
        self.Number_of_columns=0
        
        self.construct_main_window()
        self.master.mainloop()
    def construct_main_window(self):
        self.master.wm_title("Lightcurve classifier")
        self.main_row = ButtonRow(1)
        self.main_row+=Button(self.master, 
                              text="Choose folder",
                              command=self.open_folder,
                              bg='white',
                              **self.button_properties)
        self.main_row+=Button(self.master, text="Start",
                              command=self.open_image,
                              bg='white',
                              **self.button_properties)
        self.main_row+=Button(self.master, text="Load classification file",
                              command=self.open_file,
                              bg='white',
                              **self.button_properties)
        self.main_row+=Button(self.master, text="Save classification file",
                              command=self.save_file,
                              bg='white',
                              **self.button_properties)
        self.label_row = ButtonRow(2,columnspan = 7, sticky = 'WE')
        self.chosen_path_var = StringVar()
        self.label_row+=Label(self.master,
                              textvariable=self.chosen_path_var,
                             bg='white')
        self.label_row2 = ButtonRow(3,columnspan = 3, sticky = 'WE')
        self.chosen_filename = StringVar()
        self.label_row2+=Label(self.master,textvariable=self.chosen_filename,
                              bg='white')
        self.action_row = ButtonRow(5)
        self.action_row+=Button(self.master, 
                              text="OK",
                              command=self.set_ok,bg='#bfffe3',
                              **self.button_properties)
        self.action_row+=Button(self.master, 
                              text="Bad",
                              command=self.set_bad,bg='#ffbfc1',
                              **self.button_properties)
        self.action_row+=Button(self.master, 
                              text="Unsure",
                              command=self.set_unsure,bg='#ccbfff',
                              **self.button_properties)
        self.action_row+=Button(self.master, 
                              text="Undo",
                              command=self.set_undo,bg='#f2ffbf',
                              **self.button_properties)
        self.action_row+=Button(self.master, 
                              text="Skip",
                              command=self.open_image,bg='#edbfff',
                              **self.button_properties)
        self.action_row+=Button(self.master, 
                              text="More terms",
                              command=self.set_needs_more_terms,
                                bg='white',
                              **self.button_properties)
    def set_ok(self):
        self.classifications.append((self.file,'ok'))
        self.open_image()
    def set_bad(self):
        self.classifications.append((self.file,'Bad'))
        self.open_image()
    def set_unsure(self):
        self.classifications.append((self.file,'Unsure'))
        self.open_image()
    def set_undo(self):
        del self.classifications[-1]
        self.open_image()
    def set_needs_more_terms(self):
        self.classifications.append((self.file,'More terms'))
        self.open_image()
    def open_image(self):
        
        for _ in range(10):
            self.file = self.files[random.randrange(len(self.files))]
            if '.png' in self.file:
                break
        self.chosen_filename.set('   '.join([
            self.file,
                f'N classified = {len(self.classifications)}']))        
        image = Image.open(self.chosen_path+self.file)
        photo = ImageTk.PhotoImage(image)
        label = Label(self.master, image = photo)
        label.image = photo
        label.grid(row=4,column=0,columnspan = 7, sticky = 'WE')
    def open_folder(self):
        self.classifications = []
        self.chosen_path = tkinter.filedialog.askdirectory(initialdir=self.chosen_path)+'/'
        self.chosen_path_var.set(self.chosen_path)
        self.files = [f for f in listdir(self.chosen_path) if 
                      isfile(join(self.chosen_path, f))]
    def save_file(self):
        self.filename = tkinter.filedialog.asksaveasfilename(initialdir=self.chosen_path)
        with open(self.filename,'w') as f:
            for line in self.classifications:
                print(','.join(line),file=f)
    def open_file(self):
        self.filename = tkinter.filedialog.askopenfilename(initialdir=self.chosen_path)
        with open(self.filename,'r') as f:
            for line in f:
                self.classifications.append(line.split(','))
            

