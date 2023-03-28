import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


class RollOutMethodInterface(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #set window configurations
        self.geometry("600x500+430+200")
        self.title("Roll Out Method Gui")

        # # Create a style
        style = ttk.Style()
        style.theme_use('clam')

        #create container for windows on top of the root
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, CalibrationPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

        # ask user if they want to exit the application
        # self.protocol("WM_DELETE_WINDOW", self.onClosing)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

     # asks user if they actually want to exit the app
    def onClosing(self):
        if messagebox.askyesno(message="Continue to quit?"):
            self.destroy()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        
        self.title_label = ttk.Label(self, text="Home Page")
         # welcome text and file instructions
        welcomeLabel = ttk.Label(self, text="Welcome!", font=(
            'Times New Roman', 27))
        # welcomeLabel.place(x=20, y=20)
        welcomeLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel1 = ttk.Label(self, text="Please select your mp4 video file from the available directories.", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel1.pack(side='top', anchor='w', pady = 40, padx=10)

        # SELECT file
        selectFileButton = ttk.Button(
            self, text="Select File", command=self.selectVideoFile)
        # selectFileButton.place(x=20, y=120)
        selectFileButton.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel2 = ttk.Label(self, text="Your video will appear inside the 'Eyetrack' folder on your desktop.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel2.pack(side='top', anchor='w', padx=10)

        nextLabel = ttk.Label(self, text="After you have made your selection, press 'Next' to continue.", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        nextLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        #goes to next page
        self.nextButton = ttk.Button(self, text="Next", command=lambda: self.controller.show_frame(CalibrationPage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

    # select the directory holding the video file
    def selectVideoFile(self):

        filetypes = (
            ('video files', '*.mp4'),
            ('All files', '*.*')
        )

        # open file dialog to select videoFile
        filePath = filedialog.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        # show what was selected
        messagebox.showinfo(
            title='Selected File',
            message=filePath
        )

        # self.path = os.path.dirname(filePath)
        self.path = filePath

        # place videoFile into Eyetrack Folder
        self.newFolder()

       # adds new folder to user desktop and places video inside

    def newFolder(self):

        # creates new folder
        homeDir = os.path.expanduser('~')
        folder = "EyeTrack"

        # creates an Eyetrack folder in the desktop
        try:
            os.makedirs(os.path.join(homeDir, "Desktop", folder))
        except:
            # breaks from try/except
            passed = True

        # save path to videoFile
        oldVideoPath = self.path
        print(oldVideoPath)
        # get video file name from path
        videoFileName = os.path.basename(oldVideoPath)
        print(videoFileName)

        newVideoPath = os.path.join(homeDir, "Desktop", folder, videoFileName)
        print(newVideoPath)
        shutil.move(oldVideoPath, newVideoPath)

    



class CalibrationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Calibration Page")
        self.title_label.pack()
        self.home_button = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame(HomePage))
        self.home_button.pack()


appROM = RollOutMethodInterface()
appROM.mainloop()
