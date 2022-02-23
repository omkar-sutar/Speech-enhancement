
from tkinter.font import Font
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from widgets import childFrame
from enhance import predict_all
from queue import Queue
import threading
import os

SCREEN0="screen0"
SCREEN1="screen1"

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Speech Enhancer")
        self.geometry("700x450")
        self.configure(background="#FFFFFF")
        self.mainframe=tk.Frame(self,height=360,width=660,background="#FFFFFF")
        self.mainframe.place(x=20,y=20)
        self.frame=None
        self.nextButton=tk.Button(text="Next",command=self.onclickNext,background="#0E6EFA",foreground="#FFFFFF",activebackground="#1765D8",activeforeground="#FFFFFF",border=0)
        self.nextButton.place(x=580,y=400,width=80,height=28)
        self.filenames=[]
        self.currentScreen=None
        self.processTerminated=False
        self.setScreen0()
    def setScreen0(self):
        self.currentScreen=SCREEN0
        if self.frame:
            self.frame.destroy()
        #self.frame=tk.Frame(self.mainframe,width=660,height=360,padx=10,pady=10,background="#FFFFFF")
        self.frame=childFrame(self.mainframe)
        self.frame.place(x=0,y=0)
        label=tk.Label(self.frame,text="Files selected: ",font=Font(size=11),background="#FFFFFF")
        label.place(x=0,y=0)
        self.entry=tk.Text(self.frame,border=2,relief="groove")
        self.entry.insert(tk.END,"No files selected.")
        self.entry.configure(state=tk.DISABLED)
        self.entry.insert(tk.END,"No files selected")
        self.entry.place(x=0,y=30,width=640,height=260)
        button=tk.Button(self.frame,text="Browse",command=self.add_files,background="#0E6EFA",foreground="#FFFFFF",activebackground="#1765D8",activeforeground="#FFFFFF",border=0)
        button.place(x=293,y=300,width=80,height=28)
    def add_files(self):
        filenames=fd.askopenfilenames(defaultextension=".wav")
        self.entry.configure(state=tk.NORMAL)
        self.entry.delete("1.0",tk.END)
        self.filenames+=filenames
        for filename in filenames:
            self.entry.insert(tk.END,filename+"\n")
        self.entry.configure(state=tk.DISABLED)
    def onclickNext(self):
        if self.currentScreen==SCREEN0:
            self.setScreen1()
        elif self.currentScreen==SCREEN1:
            self.destroy()
            exit()
    def setScreen1(self):
        self.currentScreen=SCREEN1
        if self.frame:
            self.frame.destroy()
        self.frame=childFrame(self.mainframe)
        self.frame.place(x=0,y=0)
        self.labelStatus=tk.Label(self.frame,text="Processing..",font=Font(size=11),background="#FFFFFF")
        self.labelStatus.place(x=0,y=0)
        self.progressbar=ttk.Progressbar(self.frame,orient='horizontal',mode='indeterminate')
        self.progressbar.place(x=165,y=40,width=300)
        self.progressbar.start(35)
        self.button=tk.Button(self.frame,text="Hide details",background="#d9d9d9",border=1,relief="ridge",command=self.alterDetails)
        self.showDetails=True
        self.button.place(x=0,y=95,width=80,height=28)
        self.entry=tk.Text(self.frame,border=2,relief="groove",state=tk.DISABLED)
        self.entry.place(x=0,y=140,width=640,height=200)
        self.frame.after(500,lambda :self.log("Preparing magic circles.."))
        self.frame.after(1500,lambda :self.log("Starting magic.."))
        self.messageQueue=Queue()
        self.after(50,self.periodicLogger)
        self.frame.after(1550,self.startProcess)

    def alterDetails(self):
        if self.showDetails==True:
            self.showDetails=False
            self.entry.configure(border=0,foreground="#FFFFFF")
            self.button.config(text="Show details")
        else:
            self.showDetails=True
            self.entry.configure(border=2,foreground="#000000")
            self.button.configure(text="Hide details")
    def log(self,text):
        self.entry.configure(state=tk.NORMAL)
        self.entry.insert(tk.END,text+"\n")
        self.entry.see(tk.END)
        self.entry.configure(state=tk.DISABLED)
    def startProcess(self):
        #disable next button
        self.nextButton.configure(state=tk.DISABLED)
        #First import the selected files
        input_dir=os.path.dirname(self.filenames[0])
        onlyfilenames=[os.path.basename(x) for x in self.filenames]
        try:
            threading.Thread(target=predict_all,daemon=True,args=(onlyfilenames,input_dir,self.messageQueue)).start()
        except Exception as e:
            self.messageQueue.put(str(e))
            self.messageQueue.put("Process terminated")
            self.processTerminated=True
            return
    def periodicLogger(self):
        message=None
        if self.currentScreen!=SCREEN1:
            return
        if not self.messageQueue.empty():
            message=self.messageQueue.get()
            self.log(message)
        if message=="Process terminated" or message=="Process finished":
            self.wrap_up()
            return
        self.frame.after(200,self.periodicLogger)
    def wrap_up(self):
        self.labelStatus.configure(text="Processing.. [Done]")
        self.progressbar.stop()
        self.progressbar.destroy()
        self.nextButton.configure(state=tk.NORMAL)
        self.nextButton.configure(text="Finish")

if __name__=="__main__":
    w=Window()
    w.mainloop()