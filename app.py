import tkinter as tk
from tkinter import ttk
from serial import Serial

from valve import Valve

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

VALVE_COUNT = 4
BTN_PADX, BTN_PADY = 5, 0
FRAME_PADDING = (20, 10)
VALVE_NAMES = [
    "Input 0", "Input 1", "Input 2", "Data"
]

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        
        self.serial_device = None
        self.valve_arr = [None for _ in range(VALVE_COUNT)]

        self.tcount = -1
        self.ty, self.px = list(), list()
    
    def setupWidgets(self):
        self.setupInputBtns()
        self.setupOutputWidget()
        self.setupDataCapture()
    
    def startSerialComm(self, port, baud, timeout):
        try:
            self.serial_device = Serial(port, baud, timeout=timeout)
            self.updateStatus(connected=True)
        except:
            self.updateStatus(connected=False)
            raise ConnectionError("Failed to connect to serial device.")

    def animatePlot(self, i):
        vrecv = False

        if not self.ani:
            raise ValueError("Plot animation never started.")
        
        try:
            rval = self.serial_device.readline().decode()
            vrecv = True
        except:
            vrecv = False
            self.updateStatus(connected=False)
            print("Serial device not responding.")
        try:
            pval = float(rval.split(':')[1])*-1.0
            vrecv = True
        except:
            vrecv = False
            print("Serial device sending unexpected data.")

        if vrecv:
            self.updateOutput(pvalue=pval)

            self.tcount = self.tcount + 1
            self.ty.append(self.tcount)
            self.px.append(pval)
            
            ax = plt.gcf().get_axes()[0]
            ax.cla()

            if self.tcount <= self.value_count:
                xmin, xmax = 0, self.value_count
            else:
                xmin, xmax = self.tcount - (self.value_count - 1), self.tcount
                self.px.pop(0)
                self.ty.pop(0)
            ax.set(xlim=(xmin, xmax), ylim=(self.ymin, self.ymax))
            ax.plot(self.ty, self.px)
            
            ax.set_title("Pressure-Time Scope")
            ax.set_ylabel("Neg. Pressure (PSI)")
            ax.set_xlabel("Time (s)")

    def setupPlot(self, value_count, ymin, ymax):
        self.value_count = value_count
        self.ymin = ymin
        self.ymax = ymax

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        canvas.get_tk_widget().grid(column=5, row=0, rowspan=5, padx=5, pady=5)

        plt.style.use('ggplot')

        plt.gcf().subplots(1, 1)

        plt.title("Pressure-Time Scope")
        plt.ylabel("Neg. Pressure (PSI)")
        plt.xlabel("Time (s)")
        plt.axis([0, self.value_count, self.ymin, self.ymax])

        self.ani = FuncAnimation(plt.gcf(), self.animatePlot, interval=1000, blit=False)

    def setupDataCapture(self):
        self.data_frame = ttk.LabelFrame(self, text="Data Capture", padding=FRAME_PADDING)
        self.data_frame.grid(column=0, row=3, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="nsew")
        
        self.data_btn = ttk.Button(self.data_frame, text="Start Capture", style="Accent.TButton")
        self.data_btn.grid(column=0, row=3, sticky="nsew", padx=BTN_PADX, pady=BTN_PADY)
        
        self.reset_btn = ttk.Button(self.data_frame, text="Reset Capture", style="Accent.TButton")
        self.reset_btn.grid(column=1, row=3, sticky="nsew", padx=BTN_PADX, pady=BTN_PADY)
        
        self.dwnld_btn = ttk.Button(self.data_frame, text="Download Data .csv", style="Accent.TButton")
        self.dwnld_btn.grid(column=2, row=3, sticky="nsew", padx=BTN_PADX, pady=BTN_PADY)
        
        self.data_lbl = ttk.Label(self.data_frame, text="Not capturing packets - 0 total data points captured.")
        self.data_lbl.grid(column=0, row=4, columnspan=4, sticky="nsew", padx=BTN_PADX, pady=(BTN_PADY + 10, 0))

    def setupOutputWidget(self):
        self.chnll_frame = ttk.LabelFrame(self, text="Output Values", padding=FRAME_PADDING)
        self.chnll_frame.grid(column=0, row=2, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="nsew")
        
        self.chnll_lbl = ttk.Label(self.chnll_frame, text="Channel 1: ")
        self.chnll_lbl.grid(column=0, row=2, columnspan=2, sticky="nsew")
        
        self.out_lbl = ttk.Label(self.chnll_frame, text="0.0 Neg. PSIG", background="#1c1c1c", padding=(5, 5), borderwidth=5)
        self.out_lbl.grid(column=3, row=2, columnspan=4, sticky="nsew")

    def setupInputBtns(self):
        self.input_frame = ttk.LabelFrame(self, text="Input Valves", padding=FRAME_PADDING)
        self.input_frame.grid(column=0, row=1, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="nsew")
        
        for vid in range(VALVE_COUNT):
            cstate = tk.IntVar()
            if not self.serial_device:
                raise ValueError("Serial communication never started.")
            cvalve = Valve(vid, cstate, self.serial_device)
            self.valve_arr[vid] = cvalve
            cbtn = ttk.Checkbutton(
                self.input_frame, text=VALVE_NAMES[vid], style="Toggle.TButton",
                variable = cstate, onvalue = 1, offvalue = 0, command=cvalve.update
            )
            cbtn.grid(column=vid, row=1, padx=BTN_PADX, pady=BTN_PADY)

    def setupStatusWidget(self):
        self.status_frame = ttk.LabelFrame(self, text="System Status", padding=FRAME_PADDING)
        self.status_frame.grid(column=0, row=0, padx=FRAME_PADDING, pady=FRAME_PADDING, sticky="nsew")
        
        self.serial_lbl = ttk.Label(self.status_frame, text="Serial Device:")
        self.serial_lbl.grid(column=0, row=0, columnspan=2, sticky="nsew")
        
        self.value_lbl = ttk.Label(self.status_frame, text="Connecting...")
        self.value_lbl.grid(column=2, row=0, columnspan=2, sticky="nsew")
    
    def updateStatus(self, connected):
        ONLINE_COLOR = "#1effa3"
        OFFLINE_COLOR = "#ec2227"
        # if online
        if connected:
            self.value_lbl.config(text="Online", foreground=ONLINE_COLOR)
        # if offline
        else:
            self.value_lbl.config(text="Offline", foreground=OFFLINE_COLOR)

    def updateOutput(self, pvalue):
        self.out_lbl.config(text="{:.2f} Neg. PSIG".format(pvalue))

    def updateDataCaptureLbl(self, capturing, dcount):
        cstr = "Capturing" if capturing else "Not Capturing"
        self.data_lbl.config(text="{} packets - {} total data points captured.".format(cstr, dcount))
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pneumatic Driver")

    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.setupStatusWidget()
    app.startSerialComm(port="COM11", baud=9800, timeout=1)
    app.setupWidgets()
    app.setupPlot(value_count=50, ymin=-0.25, ymax=15)

    app.pack(fill="both", expand=True)

    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()