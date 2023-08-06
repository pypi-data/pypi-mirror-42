"""
DansCrystalGUI.py
  Creates a graphical user interface for Dans_Diffraction software. 
  Based on tkinter.
  
  Usage:
      ipython -i -matplotlib tk DansCrystalGUI.py
  
  Requires:
      numpy, matplotlib, tkinter

By Dan Porter, PhD
Diamond
2019

Version 1.0
Last updated: 23/02/19

Version History:
10/11/17 0.1    Program created
23/02/19 1.0    Finished the basic program and gave it colours

@author: DGPorter
"""

# Built-ins
import sys, os

# Set TkAgg environment
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt # Plotting
import numpy as np
if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
else:
    import tkinter as tk
    import filedialog
    #from tkinter import messagebox

# Internal functions
from .classes_crystal import Crystal
from . import functions_general as fg
from . import functions_plotting as fp
from . import functions_crystallography as fc
from .classes_structures import Structures

structure_list = Structures()

__version__ = '1.0'

# Fonts
TF= ["Times", 10]
BF= ["Times", 14]
SF= ["Times New Roman", 14]
LF= ["Times", 14]
HF= ['Courier',12]
# Colours - background
bkg = 'snow'
ety = 'white'
btn = 'light slate blue'
opt = 'light slate blue'
# Colours - active
btn_active = 'grey'
opt_active = 'grey'
# Colours - Fonts
txtcol = 'black'
btn_txt = 'black'
ety_txt = 'black'
opt_txt = 'black'


class Crystalgui:
    """
    Provide options for plotting and viewing Crystal data
    """
    def __init__(self, xtl=None):
        """"Initialise Main GUI"""
        if xtl is None:
            self.xtl = Crystal()
        else:
            self.xtl = xtl
        
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title('Crystal  by D G Porter [dan.porter@diamond.ac.uk]')
        # self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)

        # Create Widget elements from top down
        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT,anchor=tk.N)
        
        # Filename (variable)
        f_file = tk.Frame(frame)
        f_file.pack(side=tk.TOP,expand=tk.YES,fill=tk.X)
        self.file = tk.StringVar(frame,self.xtl.filename)
        var = tk.Label(f_file, text='CIF file:', font=SF, width=10)
        var.pack(side=tk.LEFT,expand=tk.NO)
        var = tk.Label(f_file, textvariable=self.file, font=TF, width=50)
        var.pack(side=tk.LEFT, expand=tk.YES)
        var = tk.Button(f_file, text='Load CIF',font=BF, bg=btn, activebackground=btn_active, command=self.fun_loadcif)
        var.pack(side=tk.LEFT,expand=tk.NO,padx=5)
        
        # Name (variable)
        f_name = tk.Frame(frame)
        f_name.pack(side=tk.TOP,expand=tk.YES,fill=tk.X)
        self.name = tk.StringVar(frame,self.xtl.name)
        var = tk.Label(f_name, text='Name:', font=SF, width=10)
        var.pack(side=tk.LEFT)
        var = tk.Entry(f_name, textvariable=self.name, font=TF, width=40, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        var.bind('<Return>',self.update_name)
        var.bind('<KP_Enter>',self.update_name)

        # List of structures
        self.struct_list = tk.StringVar(frame, 'Structures')
        var = tk.OptionMenu(f_name, self.struct_list, *structure_list.list, command=self.fun_loadstruct)
        var.config(font=SF, width=10, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.RIGHT)
        
        # Buttons 1
        f_but = tk.Frame(frame)
        f_but.pack(side=tk.TOP)
        var = tk.Button(f_but, text='Lattice\nParameters', font=BF, bg=btn, activebackground=btn_active, command=self.fun_latpar)
        var.pack(side=tk.LEFT)
        var = tk.Button(f_but, text='Symmetric\nPositions', font=BF, bg=btn, activebackground=btn_active, command=self.fun_atoms)
        var.pack(side=tk.LEFT)
        var = tk.Button(f_but, text='Symmetry\nOperations', font=BF, bg=btn, activebackground=btn_active, command=self.fun_symmetry)
        var.pack(side=tk.LEFT)
        var = tk.Button(f_but, text='General\nPositions', font=BF, bg=btn, activebackground=btn_active, command=self.fun_structure)
        var.pack(side=tk.LEFT)
        
        # Buttons 2
        f_but = tk.Frame(frame)
        f_but.pack(side=tk.TOP)
        var = tk.Button(f_but, text='Plot\nCrystal', font=BF, bg=btn, activebackground=btn_active, command=self.fun_plotxtl)
        var.pack(side=tk.LEFT)
        var = tk.Button(f_but, text='Simulate\nStructure Factors', bg=btn, activebackground=btn_active, font=BF, command=self.fun_simulate)
        var.pack(side=tk.LEFT)

        # start mainloop
        # In interactive mode, this freezes the terminal
        # To stop this, need a way of checking if interactive or not ('-i' in sys.argv)
        # However sys in this file is not the same as sys in the operating script
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    ###################################################################################
    ############################## FUNCTIONS ##########################################
    ###################################################################################
    def fun_set(self):
        self.file.set(self.xtl.filename)
        self.name.set(self.xtl.name)
    
    def fun_get(self):
        self.xtl.name = self.name.get()
    
    def fun_loadcif(self):
        #root = Tk().withdraw() # from Tkinter
        defdir = os.path.join(os.path.dirname(__file__), 'Structures')
        #defdir = os.path.expanduser('~')
        filename = filedialog.askopenfilename(initialdir=defdir,
                                              filetypes=[('cif file', '.cif'), ('magnetic cif', '.mcif'),
                                                         ('All files', '.*')])  # from tkFileDialog
        if filename:
            self.xtl = Crystal(filename)
            self.fun_set()

    def fun_loadstruct(self, event=None):
        """Load from structure_list"""
        if self.struct_list.get() in structure_list.list:
            self.xtl = getattr(structure_list, self.struct_list.get()).build()
            self.fun_set()

    def update_name(self):
        newname = self.name.get()
        self.xtl.name = newname
    
    def fun_latpar(self):
        self.fun_set()
        Latpargui(self.xtl)
    
    def fun_atoms(self):
        self.fun_set()
        if np.any(self.xtl.Atoms.mxmymz()):
            Atomsgui(self.xtl,True,True)
        else:
            Atomsgui(self.xtl,True,False)
    
    def fun_structure(self):
        self.fun_set()
        if np.any(self.xtl.Structure.mxmymz()):
            Atomsgui(self.xtl,False,True)
        else:
            Atomsgui(self.xtl,False,False)
    
    def fun_symmetry(self):
        self.fun_set()
        Symmetrygui(self.xtl)
    
    def fun_plotxtl(self):
        self.fun_set()
        self.xtl.Plot.plot_crystal()
        plt.show()
    
    def fun_simulate(self):
        self.fun_set()
        Scatteringgui(self.xtl)

    def on_closing(self):
        """End mainloop on close window"""
        self.root.destroy()


class Latpargui:
    """
    View and edit the lattice parameters
    """
    def __init__(self,xtl):
        """"Initialise"""
        self.xtl = xtl
        self.Cell = xtl.Cell
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title(xtl.name+' Lattice Parameters')
        #self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)
        
        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT,anchor=tk.N)
        
        # Name
        #var = tk.Label(frame, text='Name: {}'.format(self.xtl.name))
        #var.pack(side=tk.TOP)
        
        # Lattice constants
        frm1 = tk.Frame(frame)
        frm1.pack(side=tk.TOP)
        
        self.a = tk.DoubleVar(frame,self.Cell.a)
        self.b = tk.DoubleVar(frame,self.Cell.b)
        self.c = tk.DoubleVar(frame,self.Cell.c)
        
        var = tk.Label(frm1, text='a:', width=10, font=SF)
        var.pack(side=tk.LEFT,padx=5,pady=5)
        var = tk.Entry(frm1, textvariable=self.a, width=10, font=TF, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT,padx=2,pady=5)
        var = tk.Label(frm1, text='b:', width=10, font=SF)
        var.pack(side=tk.LEFT,padx=5,pady=5)
        var = tk.Entry(frm1, textvariable=self.b, width=10, font=TF, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT,padx=2,pady=5)
        var = tk.Label(frm1, text='c:', width=10, font=SF)
        var.pack(side=tk.LEFT,padx=5,pady=5)
        var = tk.Entry(frm1, textvariable=self.c, width=10, font=TF, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT,padx=2,pady=5)
        
        # Lattice angles
        frm1 = tk.Frame(frame)
        frm1.pack(side=tk.TOP)
        
        self.alpha = tk.DoubleVar(frame,self.Cell.alpha)
        self.beta = tk.DoubleVar(frame,self.Cell.beta)
        self.gamma = tk.DoubleVar(frame,self.Cell.gamma)
        
        var = tk.Label(frm1, text='Alpha:', width=10, font=SF)
        var.pack(side=tk.LEFT,padx=5,pady=5)
        var = tk.Entry(frm1, textvariable=self.alpha, width=10, font=TF, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT,padx=2,pady=5)
        var = tk.Label(frm1, text='Beta:', width=10, font=SF)
        var.pack(side=tk.LEFT,padx=5,pady=5)
        var = tk.Entry(frm1, textvariable=self.beta, width=10, font=TF, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT,padx=2,pady=5)
        var = tk.Label(frm1, text='Gamma:', width=10, font=SF)
        var.pack(side=tk.LEFT,padx=5,pady=5)
        var = tk.Entry(frm1, textvariable=self.gamma, width=10, font=TF, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT,padx=2,pady=5)
        
        # Button
        frm1 = tk.Frame(frame)
        frm1.pack(side=tk.TOP)
        
        var = tk.Button(frm1, text='Update', command=self.fun_update, bg=btn, activebackground=btn_active, font=BF)
        var.pack()
    
    def fun_update(self):
        "Update lattice parameters, close window"
        a = self.a.get()
        b = self.b.get()
        c = self.c.get()
        alpha = self.alpha.get()
        beta = self.beta.get()
        gamma = self.gamma.get()
        
        self.Cell.latt([a,b,c,alpha,beta,gamma])
        
        # Close window
        self.root.destroy()


class Atomsgui:
    """
    View and edit the atomic positions
    """
    def __init__(self,xtl,symmetric_only=True,magnetic_moments=False):
        """Initialise"""
        self.xtl = xtl
        self.symmetric_only = symmetric_only
        self.magnetic_moments = magnetic_moments
        if symmetric_only:
            self.Atoms = xtl.Atoms
            ttl = xtl.name + ' Symmetric Atomic Sites'
        else:
            self.Atoms = xtl.Structure
            ttl = xtl.name + ' General Atomic Sites'
        
        if magnetic_moments:
            label_text = '    n   Atom   Label       u              v            w             Occ         Uiso      mx             my           mz             '
            default_width = 55
            mag_button = 'Hide Magnetic Moments'
        else:
            label_text = '    n   Atom   Label       u              v            w             Occ         Uiso'
            default_width = 55
            mag_button = 'Show Magnetic Moments'
        
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title(ttl)
        #self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)
        
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.YES)
        
        #--- label ---
        labframe = tk.Frame(frame,relief='groove')
        labframe.pack(side=tk.TOP, fill=tk.X)
        var = tk.Label(labframe, text=label_text, font=SF, justify='left')
        var.pack(side=tk.LEFT)
        
        #--- Button ---
        frm1 = tk.Frame(frame)
        frm1.pack(side=tk.BOTTOM, fill=tk.X)
        var = tk.Button(frm1, text='Update', font=BF, command=self.fun_update, bg=btn, activebackground=btn_active)
        var.pack(side=tk.RIGHT)
        var = tk.Button(frm1, text=mag_button, font=BF, command=self.fun_magnets, bg=btn, activebackground=btn_active)
        var.pack(side=tk.LEFT)
        
        #--- Text box ---
        frame_box = tk.Frame(frame)
        frame_box.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        
        # Scrollbars
        scanx = tk.Scrollbar(frame_box,orient=tk.HORIZONTAL)
        scanx.pack(side=tk.BOTTOM, fill=tk.X)
        
        scany = tk.Scrollbar(frame_box)
        scany.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Editable string box
        self.text = tk.Text(frame_box, width=default_width, height=10, font=HF, wrap=tk.NONE, bg=ety)
        self.text.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.YES)
        self.fun_set()
        
        self.text.config(xscrollcommand=scanx.set, yscrollcommand=scany.set)
        scanx.config(command=self.text.xview)
        scany.config(command=self.text.yview)

    def fun_set(self):
        "Get positions from crystal object, fill text boxes"
        # Build string
        str = ''
        if self.magnetic_moments:
            fmt = '%3.0f %4s %5s %7.4f %7.4f %7.4f   %4.2f %6.4f   %7.4f %7.4f %7.4f\n'
            for n in range(0,len(self.Atoms.u)):
                str += fmt % (n,self.Atoms.type[n],self.Atoms.label[n],\
                           self.Atoms.u[n],self.Atoms.v[n],self.Atoms.w[n],\
                           self.Atoms.occupancy[n],self.Atoms.uiso[n],\
                           self.Atoms.mx[n],self.Atoms.my[n],self.Atoms.mz[n])
        else:
            fmt = '%3.0f %4s %5s %7.4f %7.4f %7.4f   %4.2f %6.4f\n'
            for n in range(0,len(self.Atoms.u)):
                 str += fmt % (n,self.Atoms.type[n],self.Atoms.label[n],\
                               self.Atoms.u[n],self.Atoms.v[n],self.Atoms.w[n],\
                               self.Atoms.occupancy[n],self.Atoms.uiso[n])
            
        # Insert string in text box
        self.text.insert(tk.END,str)
    
    def fun_magnets(self):
        """"ReOpen window with magnetic moments"""
        
        # Close window
        self.root.destroy()
        
        Atomsgui(self.xtl,self.symmetric_only,not self.magnetic_moments)
    
    def fun_update(self):
        "Update atomic properties, close window"
        # Get string from text box
        str = self.text.get('1.0', tk.END)
        
        # Analyse string
        """
        values = np.genfromtxt(str)
        n = values[:,0]
        type = values[:,1]
        label = values[:,2]
        u = values[:,3]
        v = values[:,4]
        w = values[:,5]
        occ = values[:,6]
        uiso = values[:,7]
        """
        lines = str.splitlines()
        n = []
        type = []
        label = []
        u = []
        v = []
        w = []
        occ = []
        uiso = []
        mx = []
        my = []
        mz = []
        for ln in lines:
            items = ln.split()
            if len(items) < 8: continue
            n += [int(items[0])]
            type += [items[1]]
            label += [items[2]]
            u += [float(items[3])]
            v += [float(items[4])]
            w += [float(items[5])]
            occ += [float(items[6])]
            uiso += [float(items[7])]
            if self.magnetic_moments:
                mx += [float(items[8])]
                my += [float(items[9])]
                mz += [float(items[10])]
        
        self.Atoms.type = type
        self.Atoms.label = label
        self.Atoms.u = np.array(u)
        self.Atoms.v = np.array(v)
        self.Atoms.w = np.array(w)
        self.Atoms.occupancy = np.array(occ)
        self.Atoms.uiso = np.array(uiso)
        if self.magnetic_moments:
            self.Atoms.mx = np.array(mx)
            self.Atoms.my = np.array(my)
            self.Atoms.mz = np.array(mz)
        else:
            self.Atoms.mx = np.zeros(len(u))
            self.Atoms.my = np.zeros(len(u))
            self.Atoms.mz = np.zeros(len(u))
        
        if self.symmetric_only:
            # Apply symmetry if updating basic structure parameters
            self.xtl.generate_structure()
        
        # Close window
        self.root.destroy()


class Symmetrygui:
    """
    View and edit the symmetry operations
    """
    def __init__(self,xtl):
        "Initialise"
        self.xtl = xtl
        self.Symmetry = xtl.Symmetry
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title(xtl.name+' Symmetry Operations')
        #self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)
        
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP)
        
        #---Labels---
        label_frame = tk.Frame(frame,relief=tk.GROOVE)
        label_frame.pack(side=tk.TOP, fill=tk.X)
        var = tk.Label(label_frame, text='n', font=SF, justify=tk.CENTER, width=4, height=2, relief=tk.RIDGE)
        var.pack(side=tk.LEFT,pady=1)
        var = tk.Label(label_frame, text='Symmetry Operations', font=SF, justify=tk.CENTER, width=25, height=2,
                       relief=tk.RIDGE)
        var.pack(side=tk.LEFT,pady=1)
        var = tk.Label(label_frame, text='Magnetic Operations', font=SF, justify=tk.CENTER, width=25, height=2,
                       relief=tk.RIDGE)
        var.pack(side=tk.LEFT,pady=1)
        
        #---Edit Boxes---
        box_frame = tk.Frame(frame)
        box_frame.pack(side=tk.TOP, fill=tk.BOTH)
        
        # Vertical Scrollbar
        self.scany = tk.Scrollbar(box_frame, command=self.fun_scroll)
        self.scany.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Box 1: n
        self.text_1 = tk.Text(box_frame, width=4, height=10, font=SF, bg=ety)
        self.text_1.pack(side=tk.LEFT,pady=1,padx=1)
        # Box 1: Symmetry operations
        self.text_2 = tk.Text(box_frame, width=28, height=10, font=SF, bg=ety)
        self.text_2.pack(side=tk.LEFT,pady=1)
        # Box 1: Magnetic operations
        self.text_3 = tk.Text(box_frame, width=28, height=10, font=SF, bg=ety)
        self.text_3.pack(side=tk.LEFT,pady=1)
        
        # Mouse Wheel scroll:
        self.text_1.bind("<MouseWheel>", self.fun_mousewheel)
        self.text_2.bind("<MouseWheel>", self.fun_mousewheel)
        self.text_3.bind("<MouseWheel>", self.fun_mousewheel)
        
        self.text_1.config(yscrollcommand=self.fun_move)
        self.text_2.config(yscrollcommand=self.fun_move)
        self.text_3.config(yscrollcommand=self.fun_move)
        #scany.config(command=self.text1.yview)
        
        self.fun_set()
        
        # Button
        frm1 = tk.Frame(self.root)
        frm1.pack(side=tk.TOP)
        
        var = tk.Button(frm1, text='Update', command=self.fun_update, font=BF, bg=btn, activebackground=btn_active)
        var.pack()
    
    def fun_move(self, *args):
        "Move within text frame"
        self.scany.set(*args)
        self.text_1.yview('moveto',args[0])
        self.text_2.yview('moveto',args[0])
        self.text_3.yview('moveto',args[0])
    
    def fun_scroll(self, *args):
        "Move scrollbar"
        self.text_1.yview(*args)
        self.text_2.yview(*args)
        self.text_3.yview(*args)
    
    def fun_mousewheel(self, event):
        self.text_1.yview("scroll", event.delta,"units")
        self.text_2.yview("scroll",event.delta,"units")
        self.text_3.yview("scroll",event.delta,"units")
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"
    
    def fun_set(self):
        # Build string
        Nops = len(self.Symmetry.symmetry_operations)
        symstr = ''
        magstr = ''
        for n in range(Nops):
            self.text_1.insert(tk.END,'%3.0f\n'%n)
            sym = self.Symmetry.symmetry_operations[n].strip('\"\'')
            mag = self.Symmetry.symmetry_operations_magnetic[n].strip('\"\'').replace('x','mx').replace('y','my').replace('z','mz')
            symstr += '%25s\n' %(sym)
            magstr += '%25s\n' %(mag)
        
        # Insert string in text box
        self.text_2.insert(tk.END,symstr)
        self.text_3.insert(tk.END,magstr)
    
    def fun_update(self):
        # Get string from text box
        sym = self.text_2.get('1.0', tk.END) # symmetry operations
        mag = self.text_3.get('1.0', tk.END) # magnetic operations
        
        # remove 'm'
        mag = mag.replace('m','')
        
        # Analyse string
        sym_lines = sym.splitlines()
        mag_lines = mag.splitlines()
        
        if len(sym_lines) != len(mag_lines):
            print('Warning: The number of symmetry and magnetic operations are not the same!')
        
        sym_ops = []
        mag_ops = []
        for sym,mag in zip(sym_lines,mag_lines):
            if len(sym.strip()) == 0: continue
            if len(mag.strip()) == 0: mag = fc.symmetry_ops2magnetic([sym.strip()])[0]
            sym_ops += [sym.strip()]
            mag_ops += [mag.strip()]
        
        self.Symmetry.symmetry_operations = sym_ops
        self.Symmetry.symmetry_operations_magnetic = mag_ops
        self.Symmetry.generate_matrices()
        
        # Close window
        self.root.destroy()


class Scatteringgui:
    """
    Simulate scattering of various forms
    """
    def __init__(self, xtl):
        """Initialise"""
        self.xtl = xtl
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title('Scattering %s' % xtl.name)
        #self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)
        
        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT,anchor=tk.N)
        
        # Variatbles
        self.energy_kev = tk.DoubleVar(frame, 8.0)
        self.edge = tk.StringVar(frame, 'Edge')
        self.type = tk.StringVar(frame,'X-Ray')
        self.orientation = tk.StringVar(frame,'Reflection')
        self.direction_h = tk.IntVar(frame,0)
        self.direction_k = tk.IntVar(frame,0)
        self.direction_l = tk.IntVar(frame,1)
        self.theta_offset = tk.DoubleVar(frame,0.0)
        self.theta_min = tk.DoubleVar(frame,-180.0)
        self.theta_max = tk.DoubleVar(frame,180.0)
        self.twotheta_min = tk.DoubleVar(frame,-180.0)
        self.twotheta_max = tk.DoubleVar(frame,180.0)
        self.powder_units = tk.StringVar(frame, 'Two-Theta')
        self.hkl_check = tk.StringVar(frame,'0 0 1')
        self.hkl_result = tk.StringVar(frame,'I:%8.0f TTH:%6.2f'%(0,0))
        self.val_i = tk.IntVar(frame,0)
        self.hkl_magnetic = tk.StringVar(frame,'0 0 1')
        self.azim_zero = tk.StringVar(frame,'1 0 0')
        self.isres = tk.BooleanVar(frame,True)
        self.psival = tk.DoubleVar(frame,0.0)
        self.polval = tk.StringVar(frame,u'\u03c3-\u03c0')
        self.resF0 = tk.DoubleVar(frame,0.0)
        self.resF1 = tk.DoubleVar(frame, 1.0)
        self.resF2 = tk.DoubleVar(frame, 0.0)
        self.magresult = tk.StringVar(frame, 'I = --')

        # X-ray edges:
        self.xr_edges, self.xr_energies = self.xtl.Properties.xray_edges()

        #---Line 1---
        line1 = tk.Frame(frame)
        line1.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        var = tk.Label(line1, text='Scattering', font=LF)
        var.pack(side=tk.LEFT)
        
        var = tk.Button(line1, text='I16', font=BF, command=self.fun_i16, bg=btn, activebackground=btn_active)
        var.pack(side=tk.RIGHT)
        
        #---Line 2---
        line2 = tk.Frame(frame)
        line2.pack(side=tk.TOP,fill=tk.X,pady=5)
        
        # Energy
        var = tk.Label(line2, text='Energy (keV):',font=SF)
        var.pack(side=tk.LEFT)
        var = tk.OptionMenu(line2, self.edge, *self.xr_edges, command=self.fun_edge)
        var.config(font=SF, width=5, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line2, textvariable=self.energy_kev, font=TF, width=8, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        
        # Type
        types = ['X-Ray','Neutron','XRay Magnetic','Neutron Magnetic','XRay Resonant']
        var = tk.Label(line2, text='Type:',font=SF)
        var.pack(side=tk.LEFT)
        var = tk.OptionMenu(line2, self.type, *types)
        var.config(font=SF, width=10, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT)
        
        # Orientation
        orients = ['None','Reflection','Transmission']
        var = tk.OptionMenu(line2, self.orientation, *orients)
        var.config(font=SF, width=10, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT)
        
        # Direction
        var = tk.Label(line2, text='Direction:',font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line2, textvariable=self.direction_h, font=TF, width=2, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line2, textvariable=self.direction_k, font=TF, width=2, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line2, textvariable=self.direction_l, font=TF, width=2, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        
        #--- Line 3 ---
        line3 = tk.Frame(frame)
        line3.pack(side=tk.TOP,fill=tk.X,pady=5)
        
        # Theta offset
        var = tk.Label(line3, text='Offset:',font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line3, textvariable=self.theta_offset, font=TF, width=5, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        
        # Theta min
        var = tk.Label(line3, text='Min Theta:',font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line3, textvariable=self.theta_min, font=TF, width=5, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        
        # Theta max
        var = tk.Label(line3, text='Max Theta:',font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line3, textvariable=self.theta_max, font=TF, width=5, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        
        # TwoTheta min
        var = tk.Label(line3, text='Min TwoTheta:',font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line3, textvariable=self.twotheta_min, font=TF, width=5, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        
        # TwoTheta max
        var = tk.Label(line3, text='Max TwoTheta:',font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line3, textvariable=self.twotheta_max, font=TF, width=5, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        
        #--- Line 4 ---
        line4 = tk.Frame(frame)
        line4.pack(side=tk.TOP,fill=tk.X,pady=5)
        
        var = tk.Button(line4, text='Display Intensities', font=BF, command=self.fun_intensities, bg=btn,
                        activebackground=btn_active)
        var.pack(side=tk.LEFT)
        
        var = tk.Button(line4, text='Plot Powder', font=BF, command=self.fun_powder, bg=btn,
                        activebackground=btn_active)
        var.pack(side=tk.LEFT)

        xaxistypes = ['two-theta', 'd-spacing', 'Q']
        var = tk.Label(line4, text='Units:', font=SF)
        var.pack(side=tk.LEFT)
        var = tk.OptionMenu(line4, self.powder_units, *xaxistypes)
        var.config(font=SF, width=10, bg=opt, activebackground=opt_active)
        var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
        var.pack(side=tk.LEFT)
        
        # hkl check
        hklbox = tk.LabelFrame(line4, text='Quick Check')
        hklbox.pack(side=tk.RIGHT)
        var = tk.Entry(hklbox, textvariable=self.hkl_check, font=TF, width=6, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        var.bind('<Return>',self.fun_hklcheck)
        var.bind('<KP_Enter>',self.fun_hklcheck)
        var = tk.Label(hklbox, textvariable=self.hkl_result,font=TF, width=22)
        var.pack(side=tk.LEFT)
        var = tk.Button(hklbox, text='Check HKL', font=BF, command=self.fun_hklcheck, bg=btn,
                        activebackground=btn_active)
        var.pack(side=tk.LEFT, pady=2)
        
        #--- Line 5 ---
        line5 = tk.Frame(frame)
        line5.pack(side=tk.TOP,pady=5)

        #---HKL Planes---
        # i value
        var = tk.Label(line5, text='i:',font=SF)
        var.pack(side=tk.LEFT)
        var = tk.Entry(line5, textvariable=self.val_i, font=TF, width=3, bg=ety, fg=ety_txt)
        var.pack(side=tk.LEFT)
        
        # directions
        vframe = tk.Frame(line5)
        vframe.pack(side=tk.LEFT, padx=3)
        var = tk.Button(vframe, text='HKi', font=BF, command=self.fun_hki,width=5, bg=btn, activebackground=btn_active)
        var.pack()
        var = tk.Button(vframe, text='HiL', font=BF, command=self.fun_hil,width=5, bg=btn, activebackground=btn_active)
        var.pack()
        
        vframe = tk.Frame(line5)
        vframe.pack(side=tk.LEFT)
        var = tk.Button(vframe, text='iKL', font=BF, command=self.fun_ikl,width=5, bg=btn, activebackground=btn_active)
        var.pack()
        var = tk.Button(vframe, text='HHi', font=BF, command=self.fun_hhi,width=5, bg=btn, activebackground=btn_active)
        var.pack()

        #---X-ray Magnetic scattering----
        if np.any(self.xtl.Structure.mxmymz()):
            resbox = tk.LabelFrame(line5, text='X-Ray Magnetic Scattering')
            resbox.pack(side=tk.LEFT, fill=tk.Y, padx=3)

            # Resonant HKL, azimuthal reference
            vframe = tk.Frame(resbox)
            vframe.pack(side=tk.LEFT, fill=tk.Y, padx=3)

            hframe = tk.Frame(vframe)
            hframe.pack()
            var = tk.Label(hframe, text='       HKL:', font=SF, width=11)
            var.pack(side=tk.LEFT)
            var = tk.Entry(hframe, textvariable=self.hkl_magnetic, font=TF, width=6, bg=ety, fg=ety_txt)
            var.pack(side=tk.LEFT)
            var.bind('<Return>',self.fun_hklmag)
            var.bind('<KP_Enter>',self.fun_hklmag)

            hframe = tk.Frame(vframe)
            hframe.pack()
            var = tk.Label(vframe, text='Azim. Ref.:', font=SF, width=11)
            var.pack(side=tk.LEFT)
            var = tk.Entry(vframe, textvariable=self.azim_zero, font=TF, width=6, bg=ety, fg=ety_txt)
            var.pack(side=tk.LEFT)

            # Resonant value
            vframe = tk.Frame(resbox)
            vframe.pack(side=tk.LEFT, fill=tk.Y, padx=3)

            hframe = tk.Frame(vframe)
            hframe.pack()
            var = tk.Label(hframe, text='F0:', font=SF)
            var.pack(side=tk.LEFT)
            var = tk.Entry(hframe, textvariable=self.resF0, font=TF, width=3, bg=ety, fg=ety_txt)
            var.pack(side=tk.LEFT)

            hframe = tk.Frame(vframe)
            hframe.pack()
            var = tk.Label(hframe, text='F1:', font=SF)
            var.pack(side=tk.LEFT)
            var = tk.Entry(hframe, textvariable=self.resF1, font=TF, width=3, bg=ety, fg=ety_txt)
            var.pack(side=tk.LEFT)

            hframe = tk.Frame(vframe)
            hframe.pack()
            var = tk.Label(hframe, text='F2:', font=SF)
            var.pack(side=tk.LEFT)
            var = tk.Entry(hframe, textvariable=self.resF2, font=TF, width=3, bg=ety, fg=ety_txt)
            var.pack(side=tk.LEFT)

            vframe = tk.Frame(resbox)
            vframe.pack(side=tk.LEFT, fill=tk.Y, padx=3)

            # Polarisation
            poltypes = [u'\u03c3-\u03c3', u'\u03c3-\u03c0', u'\u03c0-\u03c3', u'\u03c0-\u03c0']
            hframe = tk.Frame(vframe)
            hframe.pack()
            var = tk.Label(hframe, text='Polarisation:', font=SF)
            var.pack(side=tk.LEFT)
            var = tk.OptionMenu(hframe, self.polval, *poltypes)
            var.config(font=SF, width=5, bg=opt, activebackground=opt_active)
            var["menu"].config(bg=opt, bd=0, activebackground=opt_active)
            var.pack(side=tk.LEFT)

            hframe = tk.Frame(vframe)
            hframe.pack()

            # Resonant tickbox
            var = tk.Checkbutton(hframe, text='Resonant', variable=self.isres, font=SF)
            var.pack(side=tk.LEFT, padx=6)
            # psi
            var = tk.Label(hframe, text='psi:', font=SF, width=4)
            var.pack(side=tk.LEFT)
            var = tk.Entry(hframe, textvariable=self.psival, font=TF, width=4, bg=ety, fg=ety_txt)
            var.pack(side=tk.LEFT)
            var.bind('<Return>',self.fun_hklmag)
            var.bind('<KP_Enter>',self.fun_hklmag)

            vframe = tk.Frame(resbox)
            vframe.pack(side=tk.LEFT, fill=tk.Y, padx=3)

            # Azimuth Button
            var = tk.Button(vframe, text='Calc. Mag. Inten.', font=BF, command=self.fun_hklmag, bg=btn,
                            activebackground=btn_active)
            var.pack()
            # Magnetic Result
            var = tk.Label(vframe, textvariable=self.magresult, font=SF, width=12)
            var.pack(fill=tk.Y)

            # Azimuth Button
            var = tk.Button(resbox, text='Simulate\n Azimuth', font=BF, command=self.fun_azimuth, width=7, bg=btn,
                            activebackground=btn_active)
            var.pack(side=tk.LEFT)

    def fun_set(self):
        "Set gui parameters from crystal"
        
        self.type.set(self.xtl._scattering_type)
        #self.energy_kev.set(8)
        self.theta_offset.set(self.xtl._scattering_theta_offset)
        self.theta_min.set(self.xtl._scattering_min_theta)
        self.theta_max.set(self.xtl._scattering_max_theta)
        self.twotheta_min.set(self.xtl._scattering_min_two_theta)
        self.twotheta_max.set(self.xtl._scattering_max_two_theta)
        
        if self.orientation.get() == 'Reflection':
            self.direction_h.set(self.xtl._scattering_specular_direction[0])
            self.direction_k.set(self.xtl._scattering_specular_direction[1])
            self.direction_l.set(self.xtl._scattering_specular_direction[2])
        else:
            self.direction_h.set(self.xtl._scattering_parallel_direction[0])
            self.direction_k.set(self.xtl._scattering_parallel_direction[1])
            self.direction_l.set(self.xtl._scattering_parallel_direction[2])
    
    def fun_get(self):
        "Set crytal parameters from gui"
        
        scat = self.xtl.Scatter
        scat._scattering_type = self.type.get()
        scat._energy_kev = self.energy_kev.get()
        scat._scattering_theta_offset = self.theta_offset.get()
        scat._scattering_min_theta = self.theta_min.get()
        scat._scattering_max_theta = self.theta_max.get()
        scat._scattering_min_two_theta = self.twotheta_min.get()
        scat._scattering_max_two_theta = self.twotheta_max.get()
        scat._powder_units = self.powder_units.get()
        
        if self.orientation.get() == 'Reflection':
            scat._scattering_specular_direction[0] = self.direction_h.get()
            scat._scattering_specular_direction[1] = self.direction_k.get()
            scat._scattering_specular_direction[2] = self.direction_l.get()
        elif self.orientation.get() == 'Transmission':
            scat._scattering_parallel_direction[0] = self.direction_h.get()
            scat._scattering_parallel_direction[1] = self.direction_k.get()
            scat._scattering_parallel_direction[2] = self.direction_l.get()
    
    def fun_i16(self):
        "Add I16 parameters"
        
        self.type.set('X-Ray')
        self.energy_kev.set(8.0)
        self.theta_offset.set(0)
        self.theta_min.set(-20)
        self.theta_max.set(150)
        self.twotheta_min.set(0)
        self.twotheta_max.set(130)

    def fun_edge(self, event=None):
        """X-ray edge option menu"""
        edge = self.edge.get()
        if self.edge.get() in self.xr_edges:
            idx = self.xr_edges.index(edge)
            self.energy_kev.set(self.xr_energies[idx])

    def fun_hklcheck(self, event=None):
        "Show single hkl intensity"
        
        self.fun_get()
        hkl = self.hkl_check.get()
        hkl = hkl.replace(',', ' ') # remove commas
        hkl = hkl.replace('(','').replace(')','') # remove brackets
        hkl = hkl.replace('[','').replace(']','') # remove brackets
        hkl = np.fromstring(hkl,sep=' ')
        I = self.xtl.Scatter.intensity(hkl)
        tth = self.xtl.Cell.tth(hkl)
        self.hkl_result.set('I:%8.0f TTH:%6.2f'%(I,tth))
    
    def fun_intensities(self):
        "Display intensities"
        
        self.fun_get()
        if self.orientation.get() == 'Reflection':
            string = self.xtl.Scatter.print_ref_reflections(min_intensity=-1, max_intensity=None)
        elif self.orientation.get() == 'Transmission':
            string = self.xtl.Scatter.print_tran_reflections(min_intensity=-1, max_intensity=None)
        else:
            string = self.xtl.Scatter.print_all_reflections(min_intensity=-1, max_intensity=None)
        StringViewer(string, 'Intensities %s' % self.xtl.name)
    
    def fun_powder(self):
        """Plot Powder"""
        self.fun_get()
        energy = self.energy_kev.get()
        min_q = fc.calQmag(self.twotheta_min.get(), energy)
        max_q = fc.calQmag(self.twotheta_max.get(), energy)
        if min_q < 0: min_q=0.0

        if self.xtl.Scatter._powder_units.lower() in ['tth', 'angle', 'twotheta', 'theta', 'two-theta']:
            minx = fc.cal2theta(min_q, energy)
            maxx = fc.cal2theta(max_q, energy)
        elif self.xtl.Scatter._powder_units.lower() in ['d', 'dspace', 'd-spacing', 'dspacing']:
            if min_q < 0.01: min_q = 0.5
            minx = 0
            maxx = fc.caldspace(min_q)
        else:
            minx = min_q
            maxx = max_q

        self.xtl.Plot.simulate_powder(energy)
        plt.xlim(minx, maxx)
        plt.show()
    
    def fun_hki(self):
        """Plot hki plane"""
        self.fun_get()
        i = self.val_i.get()
        self.xtl.Plot.simulate_hk0(i)
        plt.show()
    
    def fun_hil(self):
        """Plot hil plane"""
        self.fun_get()
        i = self.val_i.get()
        self.xtl.Plot.simulate_h0l(i)
        plt.show()
    
    def fun_ikl(self):
        """Plot ikl plane"""
        self.fun_get()
        i = self.val_i.get()
        self.xtl.Plot.simulate_0kl(i)
        plt.show()
    
    def fun_hhi(self):
        """Plot hhl plane"""
        self.fun_get()
        i = self.val_i.get()
        self.xtl.Plot.simulate_hhl(i)
        plt.show()
    
    def fun_simulate(self):
        """Unknown"""
        self.xtl.Scatter._energy_kev
        self.xtl.Scatter._polarised
        self.xtl.Scatter._polarisation_vector_incident

    def fun_hklmag(self, event=None):
        """"Magnetic scattering"""

        energy_kev = self.energy_kev.get()
        hkl = self.hkl_magnetic.get()
        hkl = hkl.replace(',', ' ')  # remove commas
        hkl = hkl.replace('(', '').replace(')', '')  # remove brackets
        hkl = hkl.replace('[', '').replace(']', '')  # remove brackets
        hkl = np.fromstring(hkl, sep=' ')

        azi = self.azim_zero.get()
        azi = azi.replace(',', ' ')  # remove commas
        azi = azi.replace('(', '').replace(')', '')  # remove brackets
        azi = azi.replace('[', '').replace(']', '')  # remove brackets
        azi = np.fromstring(azi, sep=' ')

        psi = self.psival.get()
        pol = self.polval.get()
        if pol == u'\u03c3-\u03c3':
            pol = 's-s'
        elif pol == u'\u03c3-\u03c0':
            pol = 's-p'
        elif pol == u'\u03c0-\u03c3':
            pol = 'p-s'
        else:
            pol = 'p-p'

        F0 = self.resF0.get()
        F1 = self.resF1.get()
        F2 = self.resF2.get()

        isres = self.isres.get()
        if isres:
            # Resonant scattering
            maginten = self.xtl.Scatter.xray_resonant_magnetic(
                hkl,
                energy_kev=energy_kev,
                azim_zero=azi, psi=psi,
                polarisation=pol,
                F0=F0, F1=F1, F2=F2)
        else:
            # Non-Resonant scattering
            maginten = self.xtl.Scatter.xray_nonresonant_magnetic(
                hkl,
                energy_kev=energy_kev,
                azim_zero=azi, psi=psi,
                polarisation=pol)

        self.magresult.set('I = %9.4g'%maginten)

    def fun_azimuth(self):
        """Simulate azimuthal magnetic scattering"""

        energy_kev = self.energy_kev.get()
        hkl = self.hkl_magnetic.get()
        hkl = hkl.replace(',', ' ')  # remove commas
        hkl = hkl.replace('(', '').replace(')', '')  # remove brackets
        hkl = hkl.replace('[', '').replace(']', '')  # remove brackets
        hkl = np.fromstring(hkl, sep=' ')

        azi = self.azim_zero.get()
        azi = azi.replace(',', ' ')  # remove commas
        azi = azi.replace('(', '').replace(')', '')  # remove brackets
        azi = azi.replace('[', '').replace(']', '')  # remove brackets
        azi = np.fromstring(azi, sep=' ')

        pol = self.polval.get()
        if pol == u'\u03c3-\u03c3':
            pol = 's-s'
        elif pol == u'\u03c3-\u03c0':
            pol = 's-p'
        elif pol == u'\u03c0-\u03c3':
            pol = 'p-s'
        else:
            pol = 'p-p'

        F0 = self.resF0.get()
        F1 = self.resF1.get()
        F2 = self.resF2.get()

        isres = self.isres.get()
        if isres:
            # Resonant scattering
            self.xtl.Plot.simulate_azimuth_resonant(
                hkl,
                energy_kev=energy_kev,
                azim_zero=azi,
                polarisation=pol,
                F0=F0, F1=F1, F2=F2)
            plt.show()
        else:
            # Non-Resonant scattering
            self.xtl.Plot.simulate_azimuth_nonresonant(
                hkl,
                energy_kev=energy_kev,
                azim_zero=azi,
                polarisation=pol)
            plt.show()


class StringViewer:
    """
    Simple GUI that displays strings
    """
    def __init__(self,string,title=''):
        "Initialise"
        # Create Tk inter instance
        self.root = tk.Tk()
        self.root.wm_title(title)
        #self.root.minsize(width=640, height=480)
        self.root.maxsize(width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.root.tk_setPalette(
            background=bkg,
            foreground=txtcol,
            activeBackground=opt_active,
            activeForeground=txtcol)
        
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.YES)
        
        #--- label ---
        #labframe = tk.Frame(frame,relief='groove')
        #labframe.pack(side=tk.TOP, fill=tk.X)
        #var = tk.Label(labframe, text=label_text,font=SF,justify='left')
        #var.pack(side=tk.LEFT)
        
        #--- Button ---
        frm1 = tk.Frame(frame)
        frm1.pack(side=tk.BOTTOM, fill=tk.X)
        var = tk.Button(frm1, text='Close', font=BF, command=self.fun_close, bg=btn, activebackground=btn_active)
        var.pack(fill=tk.X)
        
        #--- Text box ---
        frame_box = tk.Frame(frame)
        frame_box.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        
        # Scrollbars
        scanx = tk.Scrollbar(frame_box,orient=tk.HORIZONTAL)
        scanx.pack(side=tk.BOTTOM, fill=tk.X)
        
        scany = tk.Scrollbar(frame_box)
        scany.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Editable string box
        self.text = tk.Text(frame_box,width=40,height=30,font=HF,wrap=tk.NONE)
        self.text.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.YES)
        self.text.insert(tk.END,string)
        
        self.text.config(xscrollcommand=scanx.set,yscrollcommand=scany.set)
        scanx.config(command=self.text.xview)
        scany.config(command=self.text.yview)
    
    def fun_close(self):
        """close window"""
        self.root.destroy()

if __name__ == '__main__':
    from Dans_Diffraction import Crystal,MultiCrystal,Structures
    S = Structures()
    xtl = S.Diamond.build()
    Crystalgui(xtl)