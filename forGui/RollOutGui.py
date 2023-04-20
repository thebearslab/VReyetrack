# moves and calibrates .mp4 video according to user specifications
# goal: eye tracking analysis
# author: Fevronia Van Sickle
# version: 4/18/23

import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import class_process_video
# import procFirst
# import compare_eye_anno
import subprocess

#Gui to analyse eye tracking 
class RollOutMethodInterface(tk.Tk):
    def __init__(self,newVideoPath=None, newDataPath=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #set window configurations
        # widthxheightxhorizontalxvertical
        self.geometry("700x550+430+200")
        self.title("Roll Out Method Gui")

        # # Create a style
        # style = ttk.Style()
        # style.theme_use('clam')

        #create container for windows on top of the root
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, CalibrationPage, GetterPage, TadaPage):
            frame = F(container, self, newVideoPath=newVideoPath, newDataPath=newDataPath)
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

# first page
class HomePage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        
        self.title_label = ttk.Label(self, text="Home Page")

         # welcome text and file instructions
        welcomeLabel = tk.Label(self, text="Welcome!", font=(
            'Times New Roman', 27))
        # welcomeLabel.place(x=20, y=20)
        welcomeLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel1 = tk.Label(self, text="Please select your mp4 video file from the available directories.", font=(
            'Times New Roman', 15))
        # instructionLabel1.place(x=20, y=80)
        instructionLabel1.pack(side='top', anchor='w', pady = 40, padx=10)

        # SELECT file
        selectFileButton = tk.Button(
            self, text="Select .mp4 File", command=self.selectVideoFile)
        # selectFileButton.place(x=20, y=120)
        selectFileButton.pack(side='top', anchor='w', pady = 20, padx=10)

        #get eyetrack data
        instructionLabel3 = tk.Label(self, text="Please select .xml eyetrack data file from the available directories.", font=(
            'Times New Roman', 15))
        # instructionLabel3.place(x=20, y=80)
        instructionLabel3.pack(side='top', anchor='w', pady = 40, padx=10)

        # SELECT file
        selectFileButton = tk.Button(
            self, text="Select .xml File", command=self.selectXMLFile)
        # selectFileButton.place(x=20, y=120)
        selectFileButton.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel2 = tk.Label(self, text="Your video and data will appear inside the 'Eyetrack' folder on your desktop.", font=(
            'Times New Roman', 15))
        # instructionLabel2.place(x=20, y=180)
        instructionLabel2.pack(side='top', anchor='w', padx=10)

        nextLabel = tk.Label(self, text="After you have made your selections, press 'Next' to continue.", font=(
            'Times New Roman', 15),)
        # nextLabel.place(x=20, y=200)
        nextLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        #goes to next page
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(CalibrationPage))
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
        self.path = filePath

        self.count = 0
        # place videoFile into Eyetrack Folder
        self.newEyetrackFolder(self.count)

    # adds new folder to user desktop and places video inside
    def newEyetrackFolder(self, count):

        # creates new folder
        homeDir = os.path.expanduser('~')
        folder = "EyeTrack"

        # creates an Eyetrack folder in the desktop
        try:
            os.makedirs(os.path.join(homeDir, "Desktop", folder))
        except:
            # breaks from try/except
            folder = "Eyetrack" + str(count)
            count += 1
            self.newEyetrackFolder(count)


        # save path to videoFile
        oldVideoPath = self.path
        print(oldVideoPath)
        # get video file name from path
        videoFileName = os.path.basename(oldVideoPath)
        print(videoFileName)

        newVideoPath = os.path.join(homeDir, "Desktop", folder, videoFileName)
        print(newVideoPath)
        shutil.move(oldVideoPath, newVideoPath)

    # select the directory holding the video file
    def selectXMLFile(self):

        filetypes = (
            ('video files', '*.xml'),
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
        self.path = filePath

        # place dataFile into Eyetrack/data Folder
        self.newDataFolder()

    # adds new folder to Eyetrack folder and places dataFile inside
    def newDataFolder(self):

        # creates new folder
        homeDir = os.path.expanduser('~')
        dataFolder = "Data"
        participantFolder = "001"
        destinationFolder = "WSU_ED_001"

        # creates an Eyetrack folder in the desktop
        try:
            os.makedirs(os.path.join(homeDir, "Desktop/Eyetrack", dataFolder, participantFolder, destinationFolder))
        except:
            # breaks from try/except
            passed = True

        # save path to videoFile
        oldDataPath = self.path
        print(oldDataPath)
        # get video file name from path
        dataFileName = os.path.basename(oldDataPath)
        print(dataFileName)

        newDataPath = os.path.join(homeDir, "Desktop/Eyetrack", dataFolder + "/" + participantFolder, dataFileName)
        print(newDataPath)
        shutil.move(oldDataPath, newDataPath)

# second page
class CalibrationPage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Calibration Page")
         # welcome text and file instructions
        choicesLabel = tk.Label(self, text="Video Stills Settings", font=(
            'Times New Roman', 27))
        choicesLabel.pack(side='top', anchor='w', pady = 20, padx=10)

        instructionLabel1 = tk.Label(self, text="You may find that cropping your video stills vertically and flipping them horizontally to be helpful \n Please select if you would like to do so.", font=(
            'Times New Roman', 15))
        instructionLabel1.pack(side='top', anchor='w', pady = 40, padx=10)

        #choices
        instructionLabel2 = tk.Label(self, text="Would you like your images cropped or flipped?", font=(
            'Times New Roman', 15))
        instructionLabel2.pack(side='top', anchor='w', padx=10)

        #crop check box
        self.checkState1 = tk.IntVar()
        self.check1 = tk.Checkbutton(self, text="crop video", font=(
            'Times New Roman', 16), variable=self.checkState1)
        self.check1.pack(padx=10, pady=10)

        #flip check box 
        self.checkState2 = tk.IntVar()
        self.check2 = tk.Checkbutton(self, text="flip video", font=(
            'Times New Roman', 16), variable=self.checkState2)
        self.check2.pack(padx=10, pady=10)

        #set interval
        instructionLabel3 = tk.Label(self, text="Our code is set to split the video into stills at 0.5 second intervals.\nPlease select the interval you would like to use.", font=(
            'Times New Roman', 15))
        instructionLabel3.pack(side='top', anchor='w', padx=10)
        self.interval = tk.DoubleVar()
        spinbox = tk.Spinbox(self, from_=0, to=3, increment=0.5, textvariable=self.interval)
        spinbox.pack(padx=10, pady=10)

        # go back button 
        self.home_button = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(HomePage))
        self.home_button.pack()

        self.processVideoButton = tk.Button(self, text="Process Video", command=self.controlSettings)
        self.processVideoButton.pack()

        #goes to next page
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(GetterPage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

    #control settings
    def controlSettings(self):

        #crop
        if self.checkState1.get() == 0:
            cropBool = 0
        else:
            cropBool = 1

        #flip
        if self.checkState2.get() == 0:
            flipBool = 0
        else:
            flipBool = 1

        #interval
        interval = self.interval.get()
        interval = float(interval)

        #process the video
        self.newVideoPath = '/Users/fevroniavansickle/Desktop/EyeTrack'
        self.frames = class_process_video.processVideo(self.newVideoPath, self.interval)
        self.frames.setOutputPath()
        self.frames.captureAtInterval(interval)
        self.frames.cropFrames(cropBool)
        self.frames.flipFrames(flipBool)


# third page
class GetterPage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):

        # start labelling button 
        self.labelMeButton = tk.Button(self, text="Start Annotating Frames", command=self.startLabelMe)
        self.labelMeButton.pack()

        #calculate results button
        self.showPointsButton = tk.Button(self, text="Calculate hitting points", command=self.giveTable)
        self.showPointsButton.pack()

        self.showResultButton = tk.Button(self, text="Calculate results", command=self.giveResults)
        self.showResultButton.pack()

        # go back button 
        self.home_button = tk.Button(self, text="Go back", command=lambda: self.controller.show_frame(CalibrationPage))
        self.home_button.pack()

        #next button
        self.nextButton = tk.Button(self, text="Next", command=lambda: self.controller.show_frame(TadaPage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

    def startLabelMe(self):
        subprocess.Popen(['labelme'])

    #process hitting points
    def giveTable(self):
        # os.system('python /Users/fevroniavansickle/Desktop/BEARS/VReyetrack/forGui/process.py')
        # os.system('python procFirst.py')
        print("this is giveTable")
        # self.dirname = '/Users/fevroniavansickle/Desktop/Eyetrack/Data'
        # self.points = process.Process(self.dirname)
        # self.points.check_point_on_sphere(cx, cy, cz, point, r)
        # self.points.getHittingPoint()
        # self.points.unity_to_python_point(old)
        # self.points.rotate_vec_by_quaternion(self,quat, vec)
        # self.points.get_hit_point_draw(self, combined_ray, linecolor)
        # self.points.transform_to_equirectangular(self, point, geo_w, geo_h, color)
        # self.points.writeCSV()

    def giveResults(self):
        print("this is giveResults")


# fourth page
class TadaPage(tk.Frame):
    def __init__(self, parent, controller, newVideoPath, newDataPath):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.newVideoPath = newVideoPath
        self.newDataPath = newDataPath
        self.create_widgets()

    def create_widgets(self):
        print("do this")

        #home button
        self.nextButton = tk.Button(self, text="Home", command=lambda: self.controller.show_frame(HomePage))
        self.nextButton.pack(side='top', anchor='w', pady = 20, padx=10)

appROM = RollOutMethodInterface()
appROM.mainloop()
